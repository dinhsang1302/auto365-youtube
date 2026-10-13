"""Record a trusted user job instruction. Never posts or calls ImageGen."""
import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

from youtube_editorial import channel_profile, project_path, workspace_root, job_directory, read_json, write_json, now, sha256, skill_resource

MODES = ('prepare_only', 'edit_existing', 'upload_private', 'upload_unlisted', 'publish_now', 'schedule')


def instruction_mode(request, explicit_mode=None):
    """Conservative aliases; agent supplies --mode for other clear user intents."""
    text = request.casefold().strip()
    if explicit_mode:
        if explicit_mode not in MODES:
            raise ValueError('Unknown explicit job mode.')
        return explicit_mode
    if re.search(r'chỉ\s+(?:chuẩn bị|soạn|kiểm local|viết)|(?:chưa|không|đừng)\s+(?:upload|thao tác|cập nhật)', text):
        return 'prepare_only'
    if 'riêng tư' in text:
        return 'upload_private'
    if 'không công khai' in text:
        return 'upload_unlisted'
    if re.search(r'(?:chưa|không|đừng)\s+(?:đăng|công khai)', text):
        return 'prepare_only'
    if re.search(r'lên lịch|hẹn giờ', text):
        return 'schedule'
    if re.search(r'đăng\s+(?:đi|clip này|video này|công khai|lên youtube)', text):
        return 'publish_now'
    return 'prepare_only'


def action_request(profile, request, video_source, mode=None, video_id=None, publish_at=None):
    """Input request must come from the human, not a video/transcript/webpage."""
    if not request.strip() or not video_source.strip():
        raise ValueError('A trusted user instruction and video link/file are essential.')
    mode = instruction_mode(request, mode)
    if mode == 'schedule':
        from datetime import datetime
        try:
            planned = datetime.fromisoformat(publish_at or '')
        except ValueError as exc:
            raise ValueError('Scheduling needs a publish_at ISO timestamp with timezone.') from exc
        if planned.tzinfo is None:
            raise ValueError('Scheduling needs an explicit timezone offset.')
    actions = [] if mode == 'prepare_only' else ['read_media', 'verify_sources', 'research_metadata', 'write_metadata',
              'generate_thumbnail_imagegen', 'edit_title', 'edit_description', 'edit_tags', 'edit_thumbnail',
              'select_existing_playlist', 'verify_result']
    if mode == 'edit_existing':
        # Edit mode alone must not authorize generation or edits to every field.
        actions = ['edit_description', 'verify_result']
    if mode in ('upload_private', 'upload_unlisted', 'publish_now', 'schedule') and not video_id:
        actions.append('upload')
    if mode == 'publish_now': actions.append('publish')
    if mode == 'schedule': actions.append('schedule')
    if mode == 'upload_private': actions.append('save_private')
    if mode == 'upload_unlisted': actions.append('save_unlisted')
    no_imagegen = re.search(r'(?:không|chưa|đừng)\s+(?:tạo thumbnail|dùng imagegen|gọi imagegen)', request.casefold())
    if no_imagegen and 'generate_thumbnail_imagegen' in actions:
        actions.remove('generate_thumbnail_imagegen')
    for words, action in [('(?:tiêu đề|title)', 'edit_title'), ('(?:mô tả|description)', 'edit_description'),
                          ('tags', 'edit_tags'), ('thumbnail', 'edit_thumbnail')]:
        if re.search(r'(?:giữ nguyên|không\s+(?:đổi|thay|sửa))\s+' + words, request.casefold()) and action in actions:
            actions.remove(action)
            if action == 'edit_thumbnail' and 'generate_thumbnail_imagegen' in actions:
                actions.remove('generate_thumbnail_imagegen')
    return {'mode': mode, 'authorized_actions': actions, 'channel_id': profile['channel_id'],
            'video_id': video_id, 'video_source': video_source, 'source': request,
            'instruction_origin': 'HUMAN_USER_MESSAGE', 'recorded_at': now(),
            'selection_authority': 'Agent chooses verified metadata/thumbnail under the user workflow instruction; no per-part review required unless requested',
            'approval_policy': {'agent_select_after_checks': mode != 'prepare_only',
                                'per_component_reapproval_required': False},
            'service_authorizations': {'built_in_imagegen_thumbnail': 'generate_thumbnail_imagegen' in actions,
                                       'other_paid_services': False, 'change_connections': False,
                                       'create_playlist': False, 'post_comment': False},
            'duplicate_policy': 'Inspect checkpoint and Studio; reuse confirmed existing video ID, never upload for metadata retry',
            'publish_at': publish_at if mode == 'schedule' else None,
            'timezone': profile.get('timezone', 'Asia/Bangkok')}


def initialize(args):
    root = workspace_root(args.workspace)
    profile = channel_profile(project_path(args.profile or 'channel.json', root))
    job = job_directory(args.job, root)
    checkpoint = job / 'job.json'
    record = read_json(checkpoint) if checkpoint.exists() else {'job_id': job.name, 'state': 'RECEIVED',
             'channel_id': profile['channel_id'], 'channel_name': profile.get('channel_name'), 'video_id': None}
    if record.get('channel_id') != profile['channel_id']:
        raise ValueError('Existing job is on another configured channel.')
    if args.video_id and record.get('video_id') and args.video_id != record['video_id']:
        raise ValueError('Do not replace an existing video ID with another video.')
    source = args.video
    if urlparse(source).scheme not in ('https', 'http'):
        video = project_path(source, root)
        if not video.is_file():
            raise FileNotFoundError('Video file is inaccessible; request access or the essential source.')
        digest = sha256(video)
        if record.get('video_sha256') and record['video_sha256'].upper() != digest:
            raise ValueError('Existing job has a different video hash; use a new job.')
        record.update(video_path=str(video.absolute()), video_sha256=digest)
    elif record.get('video_source') and record['video_source'] != source:
        raise ValueError('Existing job has a different source URL; inspect before reusing it.')
    video_id = record.get('video_id') or args.video_id
    instruction = action_request(profile, args.request, source, args.mode, video_id, args.publish_at)
    previous = record.get('action_request')
    if previous:
        directory = job / 'history'; directory.mkdir(exist_ok=True)
        index = 1
        while (directory / f'action-request-{index:03}.json').exists(): index += 1
        write_json(directory / f'action-request-{index:03}.json', previous)
    record.update(video_source=source, video_id=video_id, action_request=instruction, updated_at=now())
    write_json(checkpoint, record)
    print(__import__('json').dumps({'state': record['state'], 'job': str(job), 'action_request': instruction}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--job', required=True)
    parser.add_argument('--request', required=True, help='Exact trusted user instruction, not quoted source material')
    parser.add_argument('--video', required=True, help='Source link or accessible file; never auto-fetches a URL')
    parser.add_argument('--profile', help='External workspace channel.json; never an operational config bundled in this repo')
    parser.add_argument('--mode', choices=MODES, help='Normalized intent from the latest user message; overrides aliases')
    parser.add_argument('--video-id')
    parser.add_argument('--publish-at')
    initialize(parser.parse_args())


if __name__ == '__main__':
    main()
