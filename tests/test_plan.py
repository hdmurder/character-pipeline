import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
plan = module('plan')
compute = module('estimate_compute')

class Tests(unittest.TestCase):
    def test_golem(self):
        self.assertEqual(plan.load_character(ROOT / 'characters/golem-15')['status'], 'planned_untrained')
    def test_template(self):
        self.assertEqual(plan.load_character(ROOT / 'characters/_template')['judge']['mode'], 'shadow_only')
    def test_escape(self):
        with self.assertRaises(ValueError):
            plan.within(ROOT / 'characters/golem-15', '../../README.md')
    def test_compute(self):
        result = compute.estimate()
        self.assertEqual(result['gpu_hours_total'], [79, 156])
        self.assertEqual(result['405b_4bit_raw_GB'], 202.5)
    def test_missing_fields(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / 'config.json').write_text('{}')
            with self.assertRaises(ValueError):
                plan.load_character(d)

if __name__ == '__main__':
    unittest.main()
