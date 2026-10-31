"""Offline regressions for the omitted timeline/copyright incident."""
import copy
import unittest
from pathlib import Path

from youtube_editorial import read_json
from youtube_description import assemble, signature_for, signature_errors

PROFILE = read_json(Path(__file__).resolve().parents[1] / 'assets/templates/channel.example.json')


class DescriptionCompletenessTests(unittest.TestCase):
    def brief(self):
        return {'category': 'lighting', 'format': 'long_form_horizontal',
                'opening_lines': ['Giới thiệu đúng sản phẩm trong clip.'],
                'duration_seconds': 90, 'chapters': [
                    {'start_seconds': n, 'title': title, 'verified': True,
                     'verification_evidence': 'Reviewed transcript and original video scene'}
                    for n, title in [(0, 'Giới thiệu'), (30, 'Cấu hình'), (60, 'Bảo hành')]]}

    def test_timeline_precedes_single_signature_and_copyright(self):
        output = assemble(self.brief(), PROFILE)
        self.assertLess(output.index('TIMELINE CHI TIẾT:'), output.index(PROFILE['signature_brand_line']))
        self.assertEqual(output.count('© Bản quyền video thuộc Auto365.'), 1)
        self.assertEqual(output.count(signature_for(PROFILE, 'lighting')), 1)

    def test_long_form_cannot_silently_skip_timeline(self):
        brief = self.brief(); brief['chapters'] = []
        with self.assertRaisesRegex(ValueError, 'timeline review'):
            assemble(brief, PROFILE)
        brief['timeline_review'] = {'decision': 'blocked', 'reason': 'Not checked yet', 'evidence': 'none'}
        with self.assertRaises(ValueError):
            assemble(brief, PROFILE)

    def test_evidenced_single_topic_exception_and_shorts_remain_possible(self):
        brief = self.brief(); brief['chapters'] = []
        brief['timeline_review'] = {'decision': 'not_applicable', 'reason': 'One continuous demonstration',
                                   'evidence': 'Full clip reviewed: no meaningful content transitions'}
        self.assertNotIn('TIMELINE', assemble(brief, PROFILE))
        brief['format'] = 'shorts'; brief.pop('timeline_review')
        self.assertNotIn('TIMELINE', assemble(brief, PROFILE))

    def test_copyright_and_hotlines_have_one_profile_source(self):
        for category in ('lighting', 'window_film', 'ppf'):
            brief = self.brief(); brief['category'] = category
            output = assemble(brief, PROFILE)
            self.assertEqual(output.count('© Bản quyền video thuộc Auto365.'), 1)
            self.assertEqual(output.count(PROFILE['signatures'][category]['phone']), 1)
        brief = self.brief(); brief['paragraphs'] = ['© Bản quyền video thuộc Auto365.']
        with self.assertRaisesRegex(ValueError, 'copyright'):
            assemble(brief, PROFILE)

    def test_unresolved_rights_and_missing_profile_notice_block_render(self):
        brief = self.brief(); brief['rights_review'] = {'status': 'unknown'}
        with self.assertRaisesRegex(ValueError, 'ownership'):
            assemble(brief, PROFILE)
        bad = copy.deepcopy(PROFILE)
        bad['signature_template'] = bad['signature_template'].split('\n©', 1)[0]
        with self.assertRaisesRegex(ValueError, 'copyright'):
            assemble(self.brief(), bad)

    def test_shorts_render_compact_signature_and_route_all_categories(self):
        for category, route in PROFILE['signatures'].items():
            with self.subTest(category=category):
                brief = self.brief()
                brief.update(format='shorts', category=category, chapters=[])
                output = assemble(brief, PROFILE)
                label = ('Tư vấn phim cách nhiệt / PPF' if category in ('window_film', 'ppf')
                         else 'Tư vấn đèn, đồ chơi xe')
                expected = (f"AUTO365 | Hệ thống nâng cấp xe toàn quốc\n"
                            f"☎ {label}: {route['phone']}\n"
                            "☎ Hotline phản ánh: 1900.9365")
                self.assertEqual(output, brief['opening_lines'][0] + '\n\n' + expected)
                self.assertEqual(signature_errors(output, PROFILE, category, 'shorts'), [])
                self.assertNotIn('©', output)
                self.assertNotIn('Trụ sở:', output)

    def test_shorts_validation_rejects_long_signature_and_duplicate_contacts(self):
        long_signature = signature_for(PROFILE, 'lighting')
        short_signature = signature_for(PROFILE, 'lighting', 'shorts')
        self.assertTrue(signature_errors(long_signature, PROFILE, 'lighting', 'shorts'))
        self.assertTrue(signature_errors(short_signature, PROFILE, 'lighting', 'long_form_horizontal'))
        brief = self.brief()
        brief.update(format='shorts', chapters=[], cta=long_signature)
        with self.assertRaises(ValueError):
            assemble(brief, PROFILE)


if __name__ == '__main__':
    unittest.main()
