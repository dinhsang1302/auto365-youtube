"""Portable local entrypoint. No browser writes, network calls or paid services."""
import argparse
import json
import os
from pathlib import Path
import sys
import unittest

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))


def discover_guidance():
    """Names, not old manifest paths, locate optional guidance in this environment."""
    codex_home = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex'))
    result = {}
    for name in ('auto365-writer', 'copywriting', 'content-strategy'):
        candidates = [Path.cwd() / '.agents' / 'skills' / name / 'SKILL.md',
                      codex_home / 'skills' / name / 'SKILL.md']
        found = next((path for path in candidates if path.is_file()), None)
        result[name] = {'available': found is not None,
                        'path': str(found) if found else None,
                        'fallback': 'Use bundled source/editorial rules; report missing guidance, never claim it was read.'}
    return result


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print('auto365-youtube: init-job | render | validate | prepare | check | discover')
        print('render/validate/prepare: --workspace PROJECT [--profile CHANNEL_JSON] plus command arguments.')
        print('validate requires --revision ID|current|root. check is offline; prepare decodes/ASRs NEW media.')
        return
    command, rest = sys.argv[1], sys.argv[2:]
    if command == 'discover':
        if rest:
            raise SystemExit('discover takes no arguments; it reads local skill locations only.')
        print(json.dumps(discover_guidance(), ensure_ascii=False, indent=2))
        return
    if command == 'check':
        if rest:
            raise SystemExit('check takes no arguments and only uses temporary synthetic fixtures.')
        suite = unittest.defaultTestLoader.discover(str(SCRIPT_DIR), pattern='test_entrypoint.py')
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if command not in ('init-job', 'render', 'validate', 'prepare'):
        raise SystemExit('Unknown command; use --help.')
    if not any(arg in ('--help', '-h') for arg in rest) and not any(arg == '--profile' or arg.startswith('--profile=') for arg in rest):
        from youtube_editorial import workspace_root
        common = argparse.ArgumentParser(add_help=False)
        common.add_argument('--workspace')
        options, _ = common.parse_known_args(rest)
        profile = workspace_root(options.workspace) / 'channel.json'
        if not profile.is_file():
            raise SystemExit('Missing workspace/channel.json. Copy assets/templates/channel.example.json outside the skill repo, or pass --profile explicitly.')
        rest += ['--profile', str(profile)]
    if command == 'init-job':
        import youtube_job
        sys.argv = [sys.argv[0], *rest]
        youtube_job.main()
    elif command == 'render':
        import youtube_description
        sys.argv = [sys.argv[0], *rest]
        youtube_description.main()
    else:
        import youtube_editorial
        sys.argv = [sys.argv[0], command, *rest]
        youtube_editorial.main()


if __name__ == '__main__':
    main()
