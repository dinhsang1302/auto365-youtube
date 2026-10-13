"""Exercise prepare path resolution without decoding media or running ASR."""
import contextlib
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import youtube_editorial as editorial


class PreparePathTests(unittest.TestCase):
    def test_prepare_uses_workspace_inputs_with_different_cwd(self):
        test_root = Path.cwd() / 'tmp'
        test_root.mkdir(exist_ok=True)
        for absolute in (False, True):
            with self.subTest(absolute=absolute), tempfile.TemporaryDirectory(dir=test_root) as temp:
                base = Path(temp).resolve()
                work, other = base / 'workspace', base / 'other-cwd'
                for directory in (work, other):
                    (directory / 'media').mkdir(parents=True)
                    (directory / 'models/local').mkdir(parents=True)
                    (directory / 'media/clip.mp4').write_bytes(directory.name.encode())
                    (directory / 'models/local/model.bin').write_bytes(directory.name.encode())
                editorial.write_json(work / 'channel.json', {'channel_id': 'UCfSB3t7meifCacbB4zOrW3w'})
                video, model = work / 'media/clip.mp4', work / 'models/local'
                args = SimpleNamespace(workspace=str(work), profile='channel.json', job='jobs/path-check',
                    video=str(video) if absolute else 'media/clip.mp4',
                    model_dir=str(model) if absolute else 'models/local')
                media = {'format': {'duration': '60'}, 'streams': [{'codec_type': 'video'}, {'codec_type': 'audio'}]}
                runner = Mock(return_value=SimpleNamespace(stdout=json.dumps(media)))
                pillow = SimpleNamespace(Image=Mock(), ImageDraw=Mock())
                class StopBeforeASR(Exception):
                    pass
                whisper = Mock(side_effect=StopBeforeASR('Path-only test stops before loading a model or ASR.'))
                with contextlib.chdir(other), patch.object(editorial, 'run', runner), \
                     patch.dict('sys.modules', {'PIL': pillow, 'faster_whisper': SimpleNamespace(WhisperModel=whisper)}), \
                     patch.dict(os.environ):
                    with self.assertRaises(StopBeforeASR):
                        editorial.prepare(args)
                self.assertEqual(Path(runner.call_args_list[0].args[0][-1]), video)
                for call in runner.call_args_list[1:]:
                    command = call.args[0]
                    self.assertEqual(Path(command[command.index('-i') + 1]), video)
                whisper.assert_called_once_with(str(model), device='cpu', compute_type='int8', local_files_only=True)
                self.assertEqual((Path(whisper.call_args.args[0]) / 'model.bin').read_bytes(), b'workspace')
                checkpoint = editorial.read_json(work / 'jobs/path-check/preparation.json')
                self.assertEqual(Path(checkpoint['video_path']), video)
                self.assertEqual(checkpoint['video_sha256'], editorial.sha256(video))
                self.assertFalse((other / 'jobs').exists())


if __name__ == '__main__':
    unittest.main()
