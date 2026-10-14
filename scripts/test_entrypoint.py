"""Offline installed-skill checks. Synthetic media bytes are hash fixtures only."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from youtube_editorial import read_json, write_json, sha256, channel_profile
from youtube_description import assemble, signature_for, permission_for
from youtube_job import action_request
from test_prepare_paths import PreparePathTests

SKILL = Path(__file__).resolve().parents[1]
ENTRY = SKILL / 'scripts' / 'auto365_youtube.py'
EXAMPLE_BRIEF = SKILL / 'assets' / 'examples' / 'brief.example.json'
TEST_ROOT = Path.cwd() / 'tmp'
TEST_ROOT.mkdir(exist_ok=True)
PROFILE = read_json(SKILL / 'assets' / 'templates' / 'channel.example.json')
BRIEF = read_json(EXAMPLE_BRIEF)


def invoke(*args, entry=ENTRY, cwd=None):
    return subprocess.run([sys.executable, str(entry), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding='utf-8', errors='replace')


def configure(workspace):
    write_json(workspace / 'channel.json', PROFILE)
    write_json(workspace / 'products.json', {'products': [{'product_id':'synthetic-example','naming_status':'SOURCE_VERIFIED','canonical_name':'Synthetic test only'}]})


def fixture(workspace):
    import csv
    from youtube_description import description_sha256
    from youtube_editorial import title_characters
    configure(workspace)
    job = workspace / 'jobs' / 'synthetic'; revision = job / 'revisions' / 'description-r4'
    revision.mkdir(parents=True)
    video = job / 'hash-only.fixture'; video.write_bytes(b'NOT A VIDEO: synthetic hash bytes, no ASR/decode')
    digest = sha256(video)
    brief = copy.deepcopy(BRIEF); title = 'Synthetic runtime test'
    meta = {'title':title,'description':assemble(brief,PROFILE),'tags':['Auto365'],'hashtags':['#Auto365'],'chapters':[]}
    rules = read_json(SKILL / 'assets/templates/editorial-rules.json')
    record = {'state':'SYNTHETIC_TEST_ONLY','channel_id':PROFILE['channel_id'],'video_id':'synthetic-id','last_revision':'description-r4','action_request':{'mode':'prepare_only','authorized_actions':[],'channel_id':PROFILE['channel_id'],'source':'Synthetic fixture only'}}
    package = {'channel_id':PROFILE['channel_id'],'video_sha256':digest,'product_id':'synthetic-example','category':'lighting','rules_version':8,'title_options':[{'title':title,'character_count':title_characters(title)}],'selected_title_index':0,'keyword_selection':{'primary':{'phrase':'synthetic example','origin':'EDITORIAL_PROPOSAL'}},'metadata':{**meta,'description':'INTENTIONALLY STALE ROOT'},'user_approval':{'approved':False},'publication_authorized':False}
    write_json(job/'job.json',record);write_json(job/'editorial.json',package)
    write_json(job/'self-check.json',{'items':[]})
    write_json(job/'preparation.json',{'fixture_only':True,'state':'MEDIA_PREPARED','decode_passed':True,'channel_id':PROFILE['channel_id'],'video_sha256':digest,'video_path':str(video)})
    write_json(job/'media.json',{'format':{'duration':'60'}})
    write_json(job/'keyword-research.json',{'sources':[],'limits':['Synthetic fixture, no actual research performed'],'analytics':{'channel_id':PROFILE['channel_id']},'selected_tags':['Auto365'],'selected_hashtags':[{'hashtag':'#Auto365','reason':'Synthetic test only','origin':'EDITORIAL_PROPOSAL'}]})
    write_json(job/'source-lock.json',{'fixture_only':True});write_json(job/'transcript.reviewed.json',{'fixture_only':True,'segments':[]})
    for name,key in [('facts.csv','fact_columns'),('qa.csv','qa_columns')]:
        with (job/name).open('w',encoding='utf-8',newline='') as f:
            writer=csv.writer(f);writer.writerow(rules[key]);writer.writerow(['Synthetic test only']*len(rules[key]))
    write_json(revision/'brief.json',brief);write_json(revision/'metadata.proposed.json',meta)
    (revision/'description.after.txt').write_text(meta['description'],encoding='utf-8')
    write_json(revision/'review.json',{'fixture_only':True,'revision':'description-r4','channel_id':PROFILE['channel_id'],'video_id':'synthetic-id','rules_version':8,'after_sha256':description_sha256(meta['description']),'self_check':[{'id':key,'status':'Đạt','reason':'Synthetic structural fixture only'} for key in rules['self_check_ids']]})
    return job


class InstalledEntrypointTests(unittest.TestCase):
    def test_post_shorthand_initializes_full_authority_but_performs_no_actions(self):
        for request in ('đăng đi', 'đăng clip này', 'Đăng video này'):
            with tempfile.TemporaryDirectory(dir=TEST_ROOT) as temp:
                work = Path(temp); configure(work)
                result = invoke('init-job', '--workspace', work, '--job', 'jobs/new-clip',
                                '--request', request, '--video', 'https://example.com/source-video')
                self.assertEqual(result.returncode, 0, result.stderr)
                record = read_json(work / 'jobs/new-clip/job.json'); request_record = record['action_request']
                self.assertEqual(record['state'], 'RECEIVED')
                self.assertEqual(request_record['mode'], 'publish_now')
                self.assertEqual(request_record['channel_id'], PROFILE['channel_id'])
                self.assertTrue({'read_media','verify_sources','research_metadata','write_metadata','generate_thumbnail_imagegen','upload','publish','verify_result'} <= set(request_record['authorized_actions']))
                self.assertTrue(request_record['service_authorizations']['built_in_imagegen_thumbnail'])
                self.assertFalse(request_record['service_authorizations']['other_paid_services'])
                self.assertIsNone(record['video_id'])
        for message, expected in [('đăng đi nhưng chỉ chuẩn bị, chưa upload','prepare_only'),
                                  ('đăng clip này, chỉ lưu riêng tư','upload_private'),
                                  ('đăng clip này, không công khai','upload_unlisted')]:
            req = action_request(PROFILE, message, 'https://example.com/video')
            self.assertEqual(req['mode'], expected)
            self.assertNotIn('publish', req['authorized_actions'])
        restricted = action_request(PROFILE, 'đăng đi', 'https://example.com/video', mode='prepare_only')
        self.assertEqual(restricted['authorized_actions'], [])
        keep_fields = action_request(PROFILE, 'đăng đi, giữ nguyên title, giữ nguyên thumbnail', 'https://example.com/video')
        self.assertNotIn('edit_title', keep_fields['authorized_actions'])
        self.assertNotIn('generate_thumbnail_imagegen', keep_fields['authorized_actions'])
        reused = action_request(PROFILE, 'đăng đi', 'https://example.com/video', video_id='existing-id')
        self.assertNotIn('upload', reused['authorized_actions'])
        with self.assertRaises(ValueError): action_request(PROFILE, 'đăng đi', '')
        with self.assertRaises(ValueError): action_request(PROFILE, 'đăng đi rồi lên lịch', 'https://example.com/video')

    def test_missing_workspace_config_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as temp:
            work=Path(temp)
            result=invoke('init-job','--workspace',work,'--job','jobs/missing-profile','--request','đăng đi','--video','https://example.com/source-video')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('workspace/channel.json',result.stderr)
            self.assertFalse((work/'jobs/missing-profile/job.json').exists())

    def test_versions_and_environment_discovery(self):
        self.assertEqual([read_json(SKILL / 'assets/templates/editorial-rules.json')['version'],
                          read_json(SKILL / 'assets/templates/description-templates.json')['version'],
                          PROFILE['version']], [8, 2, 8])
        result = invoke('discover')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), {'auto365-writer', 'copywriting', 'content-strategy'})
        self.assertEqual(invoke('--help').returncode, 0)

    def test_render_retains_complete_narrative_and_rejects_truncation(self):
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as temp:
            work = Path(temp); configure(work)
            result = invoke('render', '--workspace', work, '--brief', EXAMPLE_BRIEF,
                            '--output-dir', 'out', cwd=work)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (work / 'out/description.after.txt').read_text(encoding='utf-8')
            self.assertEqual(text, assemble(BRIEF,PROFILE))
            for section in BRIEF['narrative_sections']:
                self.assertEqual(text.count(section['text']), 1)
                self.assertNotIn(section['evidence'], text)
            too_long = copy.deepcopy(BRIEF)
            too_long['narrative_sections'][0]['text'] = 'x' * 5001
            with self.assertRaises(ValueError): assemble(too_long, PROFILE)

    def test_validate_uses_selected_revision_and_preserves_results(self):
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as temp:
            work = Path(temp); job = fixture(work)
            args = ('validate', '--workspace', work, '--job', 'jobs/synthetic', '--revision', 'current', '--output-dir', 'checks/first')
            result = invoke(*args, cwd=work)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            check = read_json(work / 'checks/first/validation.json')
            self.assertEqual(check['revision'], 'description-r4')
            self.assertEqual(check['errors'], [])
            self.assertEqual(check['editorial_open_items'], [])
            self.assertNotEqual(invoke(*args).returncode, 0)
            self.assertNotEqual(invoke('validate', '--workspace', work, '--job', job,
                                      '--revision', 'missing', '--output-dir', 'checks/missing').returncode, 0)
            revision = job / 'revisions/description-r4'
            review = read_json(revision / 'review.json'); review['after_sha256'] = 'wrong'
            write_json(revision / 'review.json', review)
            self.assertNotEqual(invoke('validate', '--workspace', work, '--job', job,
                                      '--revision', 'current', '--output-dir', 'checks/bad-hash').returncode, 0)

    def test_configured_channel_is_dynamic_and_all_job_layers_match(self):
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as temp:
            work = Path(temp); job = fixture(work)
            alternate = 'UC' + 'X' * 22
            profile = copy.deepcopy(PROFILE); profile['channel_id'] = alternate
            profile_file = work / 'channel.json'; write_json(profile_file, profile)
            # Products fixture is already configured beside the external profile.
            self.assertEqual(channel_profile(profile_file)['channel_id'], alternate)
            for name in ('job.json', 'editorial.json', 'preparation.json', 'revisions/description-r4/review.json', 'revisions/description-r4/brief.json'):
                path = job / name; value = read_json(path); value['channel_id'] = alternate
                if 'action_request' in value: value['action_request']['channel_id'] = alternate
                write_json(path, value)
            # Analytics origin is also matched to the configured channel.
            research = read_json(job / 'keyword-research.json'); research['analytics']['channel_id'] = alternate
            write_json(job / 'keyword-research.json', research)
            result = invoke('validate', '--workspace', work, '--profile', profile_file, '--job', job,
                            '--revision', 'current', '--output-dir', 'checks/alternate')
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            for index, name in enumerate(('job.json', 'preparation.json', 'editorial.json', 'revisions/description-r4/review.json', 'revisions/description-r4/brief.json')):
                path = job / name; original = read_json(path); bad = copy.deepcopy(original)
                bad['channel_id'] = PROFILE['channel_id']; write_json(path, bad)
                with self.subTest(layer=name):
                    self.assertNotEqual(invoke('validate', '--workspace', work, '--profile', profile_file,
                                              '--job', job, '--revision', 'current', '--output-dir', f'checks/mismatch-{index}').returncode, 0)
                write_json(path, original)

    def test_hotlines_vat_and_extra_signature(self):
        lighting = signature_for(PROFILE, 'lighting'); film = signature_for(PROFILE, 'window_film')
        self.assertIn('☎ Tư vấn đèn đồ chơi xe: 0365 365 911\n☎ Hotline phản ánh chất lượng dịch vụ: 1900.9365', lighting)
        self.assertEqual(lighting.replace('Tư vấn đèn đồ chơi xe: 0365 365 911', 'Tư vấn phim cách nhiệt / PPF: 0587 365 365'), film)
        for category in ('camera', 'accessories'):
            self.assertEqual(signature_for(PROFILE, category), lighting)
        self.assertEqual(signature_for(PROFILE, 'ppf'), film)
        for category in PROFILE['signatures']:
            output = signature_for(PROFILE, category)
            self.assertNotIn('nhập sỉ', output)
            self.assertNotIn('0369.878787', output)
            self.assertEqual(output.count('☎ Tư vấn'), 1)
            self.assertEqual(output.count('☎ Hotline phản ánh chất lượng dịch vụ:'), 1)
        legacy = copy.deepcopy(PROFILE)
        legacy['signature_template'] = legacy['signature_template'].replace('☎ Hotline phản ánh', '☎ Hotline nhập sỉ: 0369.878787\n☎ Hotline phản ánh')
        with self.assertRaises(ValueError): signature_for(legacy, 'lighting')
        for extra in ('1900.9365', '0365 365 911', 'Giá chưa VAT', '[cần xác minh]', lighting, 'Tư vấn: 0365 365 365'):
            brief = copy.deepcopy(BRIEF); brief['cta'] = extra
            with self.subTest(extra=extra), self.assertRaises(ValueError): assemble(brief, PROFILE)
        self.assertFalse(permission_for({'channel_id':PROFILE['channel_id'],'action_request':{'mode':'prepare_only','authorized_actions':[],'channel_id':PROFILE['channel_id'],'source':'Synthetic test'}}, 'edit_description', 'description-r4', 'any-hash'))

    def test_bundle_relocates_without_original_windows_paths(self):
        with tempfile.TemporaryDirectory(dir=TEST_ROOT) as temp:
            work = Path(temp); configure(work); moved = work / 'another-location with spaces'
            shutil.copytree(SKILL, moved, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            result = invoke('render', '--workspace', work, '--brief', moved / 'assets/examples/brief.example.json',
                            '--output-dir', 'relocated-output', entry=moved / 'scripts/auto365_youtube.py', cwd=work)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((work / 'relocated-output/description.after.txt').read_text(encoding='utf-8'), assemble(BRIEF, PROFILE))


if __name__ == '__main__':
    unittest.main()
