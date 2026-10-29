"""Validate a character folder and print a plan; no inference or training."""
import argparse
import json
from pathlib import Path

STAGES = (
    'teacher generation (integration not implemented)',
    'fabrication and repetition checks (integration not implemented)',
    'd1 character-break scores (shadow only; integration not implemented)',
    'human review and frozen data splits',
    'shared SFT; parallel DPO / KTO / continued SFT',
    'document-graft controlled branch',
    'held-out behavioral and activation evaluation',
)

def within(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Character paths must remain inside the character folder')
    if not path.is_file():
        raise ValueError(f'Missing character file: {relative}')
    return path

def load_character(folder):
    root = Path(folder).resolve()
    data = json.loads((root / 'config.json').read_text())
    for key in ('id', 'status', 'bible', 'sources', 'student', 'judge', 'arms', 'evaluation'):
        if key not in data:
            raise ValueError(f'Missing field: {key}')
    within(root, data['bible'])
    sources = json.loads(within(root, data['sources']).read_text())
    if not isinstance(sources, list):
        raise ValueError('Source manifest must be an array')
    if data['judge']['mode'] != 'shadow_only':
        raise ValueError('This preview supports shadow-only judging')
    return data

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    data = load_character(args.folder)
    print(json.dumps({'character': data['id'], 'status': data['status'],
                      'execution': 'plan_only', 'stages': STAGES,
                      'arms': data['arms']}, indent=2))

if __name__ == '__main__':
    main()
