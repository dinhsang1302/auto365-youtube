"""Offline media preparation and structural review for a YouTube editorial job.

This tool does not upload, change Studio, authorize publication, or call paid APIs.
The editor reviews frames, corrects ASR terms, locks sources and drafts metadata.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import re
import unicodedata
import copy
from pathlib import Path
import subprocess
from datetime import datetime, timezone

def skill_resource(relative):
    """Locate immutable bundled resources independently of the project or OS."""
    return Path(__file__).resolve().parents[1] / relative


def workspace_root(value=None):
    """Use an explicit project or cwd ancestry, never the installed script path."""
    if value:
        root = Path(value).resolve()
        if not root.is_dir():
            raise ValueError('Explicit workspace must be an existing project directory.')
        return root
    candidates = [Path.cwd(), *Path.cwd().parents]
    for root in candidates:
        if (root / 'youtube-editorial-rules.json').is_file():
            return root.resolve()
    raise ValueError('Supply --workspace pointing to a project with youtube-editorial-rules.json.')


def project_path(value, workspace):
    path = Path(value)
    return path if path.is_absolute() else workspace_root(workspace) / path


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    """Follow project resource pointers; maintain a single physical config."""
    path = Path(path).resolve()
    seen = set()
    while path not in seen:
        seen.add(path)
        value = json.loads(path.read_text(encoding='utf-8-sig'))
        if not isinstance(value, dict) or 'resource_ref' not in value:
            return value
        reference = Path(value['resource_ref'])
        if reference.is_absolute():
            raise ValueError('Resource pointers must be relative, not machine-specific.')
        path = (path.parent / reference).resolve()
    raise ValueError('Cyclic resource pointer.')


def write_json(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest().upper()


def channel_profile(path):
    profile = read_json(path)
    if not isinstance(profile.get('channel_id'), str) or not re.fullmatch(r'UC[A-Za-z0-9_-]{22}', profile['channel_id']):
        raise ValueError('A valid target channel ID must be supplied by channel.json.')
    # Local preparation needs a configured target, not a cached login claim.
    # Before any remote write the agent verifies the live Studio ID and role.
    return profile


def job_directory(path, workspace=None, create=True):
    root = workspace_root(workspace)
    path = Path(path)
    path = (path if path.is_absolute() else root / path).resolve()
    if path == root or root not in path.parents:
        raise ValueError('Derived job output must stay inside this workspace.')
    if create:
        path.mkdir(parents=True, exist_ok=True)
    elif not path.is_dir():
        raise FileNotFoundError(path)
    return path


def selected_revision(job, selection):
    """Explicit revision; current follows checkpoint, never directory sort order."""
    record = read_json(job / 'job.json') if (job / 'job.json').exists() else {}
    if selection == 'current':
        selection = (record.get('pending_local_revision', {}).get('id')
                     or record.get('last_revision'))
        if not selection:
            raise ValueError('No current revision checkpoint; select --revision root or a revision ID.')
    if selection == 'root':
        return job, 'root'
    if not selection or Path(selection).name != selection or selection in ('.', '..'):
        raise ValueError('Select a revision ID, current, or root; paths are not revision IDs.')
    directory = (job / 'revisions' / selection).resolve()
    if job.resolve() not in directory.parents or not directory.is_dir():
        raise ValueError('Selected revision is missing or outside the job.')
    return directory, selection


def validation_inputs(job, selection):
    """Use selected metadata AND review, with shared media/source context only."""
    directory, revision = selected_revision(job, selection)
    package = copy.deepcopy(read_json(job / 'editorial.json'))
    if revision == 'root':
        review = read_json(job / 'self-check.json') if (job / 'self-check.json').exists() else {}
        return package, review.get('items', []), directory, revision, None
    review = read_json(directory / 'review.json')
    if review.get('revision') != revision or review.get('channel_id') != package['channel_id']:
        raise ValueError('Selected review identity does not match revision/channel.')
    record = read_json(job / 'job.json')
    if review.get('video_id') != record.get('video_id'):
        raise ValueError('Selected review belongs to a different video.')
    package['metadata'] = read_json(directory / 'metadata.proposed.json')
    description = (directory / 'description.after.txt').read_text(encoding='utf-8')
    if description != package['metadata']['description']:
        raise ValueError('Selected description file differs from selected metadata.')
    if review.get('after_sha256') != hashlib.sha256(description.encode('utf-8')).hexdigest():
        raise ValueError('Selected revision content differs from its recorded SHA-256.')
    package['rules_version'] = review.get('rules_version', 0)
    package['user_approval'] = {'approved': bool(review.get('approved_at')),
                              'source': review.get('authorization_source')}
    # Root approval flags never become authority for another revision.
    package['publication_authorized'] = False
    items = review.get('self_check', [])
    if not isinstance(items, list):
        raise ValueError('Selected review uses an unsupported self-check schema; preserve history and review anew.')
    brief_path = directory / 'brief.json'
    return package, items, directory, revision, read_json(brief_path) if brief_path.exists() else None


def run(args, timeout=600):
    return subprocess.run(args, check=True, capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=timeout)


def title_characters(title):
    return len(unicodedata.normalize('NFC', title))


def validate_manual_chapters(chapters, duration):
    """Validate supplied boundaries, including the final chapter. No generation."""
    if not chapters:
        return []
    errors = []
    if len(chapters) < 3:
        errors.append('Manual chapters require at least three verified boundaries.')
    starts = [c.get('start_seconds') for c in chapters]
    if any(not isinstance(s, (int, float)) or not math.isfinite(s) for s in starts):
        return errors + ['Chapter boundaries must be finite numeric seconds.']
    if any(isinstance(s, bool) or int(s) != s for s in starts):
        errors.append('Published chapter boundaries must be verified whole seconds; never silently round.')
    if starts[0] != 0:
        errors.append('Manual chapters must begin at 00:00.')
    ends = starts[1:] + [duration]
    if any(end - start < 10 for start, end in zip(starts, ends)):
        errors.append('Every chapter, including the final one, must last at least 10 seconds.')
    if any(not c.get('verified') or not c.get('verification_evidence') for c in chapters):
        errors.append('Approximate or unevidenced chapter timestamps cannot be published.')
    return errors


def merge_exact_signature(description, default_description, signature):
    """Merge inspected defaults and exact signature blocks, retaining one signature.

    A differently worded signature needs editor review, not blind text deletion.
    This helper does not inspect Studio or certify the final saved description.
    """
    pieces = [part.replace(signature, '').strip() for part in [default_description, description]]
    if any('AUTO365 |' in part or re.search(r'(?:☎\s*)?(?:Tư vấn|Hotline)\s*:', part, re.I)
           for part in pieces):
        raise ValueError('A legacy or differently worded signature needs editor review before merging.')
    return '\n\n'.join([part for part in pieces if part] + [signature])


def prepare(args):
    root = workspace_root(args.workspace)
    profile = channel_profile(project_path(args.profile, root))
    # Windows sandbox can permit file reads while denying realpath/reparse queries
    # on Downloads. Inputs are read only; hash/open checks establish their identity.
    video = project_path(args.video, root)
    if not video.is_file():
        raise FileNotFoundError(video)
    job = job_directory(args.job, args.workspace)
    if (job / 'job.json').exists() and read_json(job / 'job.json').get('channel_id') != profile['channel_id']:
        raise ValueError('Existing job target differs from configured channel.')
    digest = sha256(video)
    checkpoint = job / 'preparation.json'
    if checkpoint.exists():
        old = read_json(checkpoint)
        if old['channel_id'] != profile['channel_id'] or old['video_sha256'] != digest:
            raise ValueError('Existing job belongs to a different video/channel; use a new job.')
        if old['state'] == 'MEDIA_PREPARED' and all((job / f).is_file() for f in old['artifacts']):
            print(json.dumps({'state': old['state'], 'reused': True, 'job': str(job)}))
            return
    state = {'state': 'READING_MEDIA', 'channel_id': profile['channel_id'],
             'video_path': str(video), 'video_sha256': digest, 'started_at': now(),
             'remote_actions': [], 'publication_authorized': False}
    write_json(checkpoint, state)
    try:
        media = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams',
                                '-of', 'json', str(video)]).stdout)
        write_json(job / 'media.json', media)
        duration = float(media['format']['duration'])
        if not any(s['codec_type'] == 'video' for s in media['streams']):
            raise ValueError('Input has no video stream.')
        has_audio = any(s['codec_type'] == 'audio' for s in media['streams'])
        run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(video), '-f', 'null', '-'])
        frames = job / 'frames'
        frames.mkdir(exist_ok=True)
        # Sample the entire timeline, up to ~60 thumbnails; sample != full visual review.
        interval = max(1, math.ceil(duration / 60))
        run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(video),
             '-vf', f'fps=1/{interval},scale=480:-2', str(frames / 'frame-%03d.jpg')])
        from PIL import Image, ImageDraw
        files = sorted(frames.glob('frame-*.jpg'))
        cols, cell_w, cell_h = 5, 480, 320
        sheet = Image.new('RGB', (cols * cell_w, math.ceil(len(files) / cols) * cell_h), 'white')
        draw = ImageDraw.Draw(sheet)
        timestamps = []
        for i, f in enumerate(files):
            image = Image.open(f).convert('RGB')
            x, y = (i % cols) * cell_w, (i // cols) * cell_h
            sheet.paste(image, (x, y + 20))
            seconds = round((i + 0.5) * interval, 2)
            draw.text((x + 6, y + 3), f'~{seconds}s', fill='black')
            timestamps.append({'path': str(f), 'approx_seconds': seconds})
        sheet.save(job / 'contact-sheet.jpg', quality=88)
        artifacts = ['media.json', 'contact-sheet.jpg', 'frames.json', 'transcript.raw.json']
        write_json(job / 'frames.json', {'interval_seconds': interval, 'samples': timestamps})
        if has_audio:
            model = project_path(args.model_dir, root)
            if not (model / 'model.bin').is_file():
                raise ValueError('A complete local faster-whisper model is required; downloads are disabled.')
            run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', str(video),
                 '-vn', '-ac', '1', '-ar', '16000', str(job / 'audio.wav')])
            os.environ['HF_HUB_OFFLINE'] = '1'
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            from faster_whisper import WhisperModel
            whisper = WhisperModel(str(model), device='cpu', compute_type='int8', local_files_only=True)
            segments, info = whisper.transcribe(str(job / 'audio.wav'), language='vi',
                                               beam_size=5, vad_filter=True)
            transcript = [{'start': s.start, 'end': s.end, 'text': s.text.strip()} for s in segments]
            asr = {'engine': 'faster-whisper', 'model_path': str(model),
                   'language': info.language, 'review_status': 'UNREVIEWED', 'segments': transcript}
            artifacts.append('audio.wav')
        else:
            asr = {'engine': None, 'review_status': 'NO_AUDIO', 'segments': []}
        write_json(job / 'transcript.raw.json', asr)
        state.update(state='MEDIA_PREPARED', finished_at=now(), artifacts=artifacts,
                     decode_passed=True, source_unchanged=(sha256(video) == digest))
        if not state['source_unchanged']:
            raise ValueError('Video changed while preparing the job.')
        write_json(checkpoint, state)
        print(json.dumps({'state': state['state'], 'job': str(job),
                          'duration': duration, 'frames': len(files), 'segments': len(asr['segments'])}))
    except Exception as exc:
        state.update(state='PREPARATION_FAILED', last_error=str(exc), failed_at=now())
        write_json(checkpoint, state)
        raise


def validate(args):
    root = workspace_root(args.workspace)
    profile_path = project_path(args.profile, root)
    profile = channel_profile(profile_path)
    job = job_directory(args.job, root, create=False)
    prep = read_json(job / 'preparation.json')
    package, reviewed_items, revision_dir, revision, brief = validation_inputs(job, args.revision)
    errors = []
    job_record = read_json(job / 'job.json') if (job / 'job.json').exists() else {}
    if job_record.get('channel_id') != profile['channel_id']:
        errors.append('Job record target differs from configured channel.')
    request = job_record.get('action_request')
    if request and request.get('channel_id') != profile['channel_id']:
        errors.append('Latest action request target differs from configured channel.')
    if package.get('remote_video_id') and package['remote_video_id'] != job_record.get('video_id'):
        errors.append('Root context and job record refer to different video IDs.')
    if prep['state'] != 'MEDIA_PREPARED' or not prep.get('decode_passed'):
        errors.append('Media preparation incomplete.')
    video_path = Path(prep['video_path'])
    if not video_path.is_file() and (job / 'input' / 'video.mp4').is_file():
        video_path = job / 'input' / 'video.mp4'
    if sha256(video_path) != prep['video_sha256']:
        errors.append('Video changed after preparation.')
    if package['channel_id'] != profile['channel_id'] or prep['channel_id'] != profile['channel_id']:
        errors.append('Job/package target channel mismatch.')
    if package['video_sha256'] != prep['video_sha256']:
        errors.append('Metadata and media hash mismatch.')
    titles = package['title_options']
    selected = package['selected_title_index']
    if not titles or len(titles) > 3 or selected not in range(len(titles)):
        errors.append('Expected one to three supported title options and a valid selection.')
    else:
        if package['metadata']['title'] != titles[selected]['title']:
            errors.append('Selected title and metadata differ.')
    for option in titles:
        if option.get('character_count') != title_characters(option['title']):
            errors.append('A title character count is missing or incorrect.')
    registry = read_json(profile_path.parent / 'products.json')
    product = next((p for p in registry['products'] if p['product_id'] == package['product_id']), None)
    if not product or product['naming_status'] != 'SOURCE_VERIFIED':
        errors.append('Product name has no verified source.')
    # Product wording belongs to the editorial review; a problem-led title does
    # not need to contain every brand/model/vehicle name.
    from youtube_description import signature_for, public_copy_errors, permission_for
    signature = signature_for(profile, package['category'])
    from youtube_description import signature_errors
    errors.extend(signature_errors(package['metadata']['description'], profile, package['category']))
    policy = root / 'youtube-editorial-rules.json'
    rules = read_json(policy if policy.is_file() else skill_resource('assets/templates/editorial-rules.json'))
    if brief is not None:
        from youtube_description import assemble
        try:
            if assemble(brief, profile) != package['metadata']['description']:
                errors.append('Selected metadata differs from the complete rendered brief; do not truncate sections.')
            if brief.get('chapters', []) != package['metadata'].get('chapters', []):
                errors.append('Selected brief and metadata chapter boundaries differ.')
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(str(exc))
    public_copy = package['metadata']['title'] + '\n' + package['metadata']['description']
    errors.extend(public_copy_errors(public_copy, package.get('pinned_comment_proposal', {}).get('text', '')))
    if len(package['metadata']['description']) > 5000:
        errors.append('Description exceeds platform character limit; never silently truncate.')
    if any(marker in public_copy for marker in ['[TODO]', '[PLACEHOLDER]', '[phạm vi mỗi đèn cần nghe lại]', 'GHI CHÚ NỘI BỘ']):
        errors.append('Public metadata contains an internal note or placeholder.')
    chapters = package['metadata'].get('chapters', [])
    duration = float(read_json(job / 'media.json')['format']['duration'])
    errors.extend(validate_manual_chapters(chapters, duration))
    keywords = package.get('keyword_selection', {})
    if not isinstance(keywords.get('primary'), dict) or not keywords['primary'].get('phrase'):
        errors.append('Exactly one primary keyword with origin is required.')
    if any(not entry.get('origin') for entry in [keywords.get('primary', {})] + keywords.get('secondary', [])):
        errors.append('Keyword proposals and measured queries need explicit origins.')
    if package.get('rules_version', 0) >= 3 and rules.get('keyword_research', {}).get('required_before_final_metadata'):
        research_path = job / 'keyword-research.json'
        if not research_path.exists():
            errors.append('Missing per-video keyword research or documented search-failure fallback.')
        else:
            research = read_json(research_path)
            research_channel = research.get('analytics', {}).get('channel_id')
            if research_channel and research_channel != profile['channel_id']:
                errors.append('Keyword research uses Analytics from a different channel.')
            if not research.get('sources') and not research.get('limits'):
                errors.append('Keyword research needs sources or an explicit search-failure limitation.')
            if research.get('selected_tags') is not None and research['selected_tags'] != package['metadata'].get('tags', []):
                errors.append('Selected Studio tags differ from the per-video researched tag set.')
            researched_hashtags = research.get('selected_hashtags')
            if researched_hashtags is not None:
                if [entry.get('hashtag') for entry in researched_hashtags] != package['metadata'].get('hashtags', []):
                    errors.append('Selected hashtags differ from the per-video researched hashtag set.')
                if any(not entry.get('reason') or not entry.get('origin') for entry in researched_hashtags):
                    errors.append('Selected hashtags need a video-specific reason and data origin.')
    comment = package.get('pinned_comment_proposal', {})
    if comment and (not comment.get('text') or comment.get('state') != 'PROPOSED_NOT_POSTED'):
        errors.append('A prepared pinned comment must stay a proposal until job-specific posting authority exists.')
    for filename, columns_key in [('facts.csv','fact_columns'), ('qa.csv','qa_columns')]:
        path = job / filename
        if not path.exists():
            errors.append(f'Missing internal table: {filename}.')
        else:
            with path.open(encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames != rules[columns_key] or not list(reader):
                    errors.append(f'Invalid columns or empty internal table: {filename}.')
    if set(x.get('id') for x in reviewed_items) != set(rules['self_check_ids']):
        errors.append('Expected all eight editorial self-checks.')
    if any(x.get('status') not in rules['review_statuses'] or not x.get('reason') for x in reviewed_items):
        errors.append('Self-checks need an allowed status and a reason.')
    if package.get('publication_authorized') and not permission_for(job_record, 'publish'):
        errors.append('A metadata flag cannot authorize publication without a matching job instruction.')
    if not (job / 'source-lock.json').exists() or not (job / 'transcript.reviewed.json').exists():
        errors.append('Missing source lock or reviewed transcript.')
    checks = {'checked_at': now(), 'state': 'STRUCTURAL_CHECK_PASSED' if not errors else 'CHECK_FAILED',
              'revision': revision, 'metadata_source': str(revision_dir / ('editorial.json' if revision == 'root' else 'metadata.proposed.json')),
              'review_source': str(revision_dir / ('self-check.json' if revision == 'root' else 'review.json')),
              'active_rules_version': rules['version'],
              'verified_media_path': str(video_path),
              'errors': errors, 'semantics': 'Requires editor source review; structural checks do not prove claims.',
              'user_review': 'APPROVED' if package.get('user_approval', {}).get('approved') else 'PENDING',
              'action_request': job_record.get('action_request'), 'remote_actions': [],
              'editorial_open_items': [x['id'] for x in reviewed_items if x.get('status') != 'Đạt'],
              'default_description_inspected': package.get('default_description_review', {}).get('inspected', False),
              'title_characters': title_characters(package['metadata']['title']),
              'description_characters': len(package['metadata']['description'])}
    output = job_directory(args.output_dir, root) if args.output_dir else revision_dir
    destination = output / 'validation.json'
    if destination.exists():
        raise ValueError('Validation output exists; use a new --output-dir to preserve history.')
    write_json(destination, checks)
    print(json.dumps(checks, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    p = subs.add_parser('prepare')
    p.add_argument('--video', required=True)
    p.add_argument('--job', required=True)
    p.add_argument('--profile', required=True)
    p.add_argument('--model-dir', required=True)
    p.add_argument('--workspace', help='Project root; defaults to cwd ancestry, not script location')
    p.set_defaults(func=prepare)
    v = subs.add_parser('validate')
    v.add_argument('--job', required=True)
    v.add_argument('--profile', required=True)
    v.add_argument('--workspace', help='Project root, independently of script installation path')
    v.add_argument('--revision', required=True, help='Exact revision ID, current checkpoint, or explicit root baseline')
    v.add_argument('--output-dir', help='New workspace directory for validation results; never overwrite history')
    v.set_defaults(func=validate)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
