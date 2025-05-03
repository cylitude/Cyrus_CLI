import unittest
import sys
import io
import json
from linked_cli.cli import main as cli_main

class TestCLI(unittest.TestCase):
    """
    Test suite for the CLI interface:
    - help output
    - generation only
    - sort with seed + output JSON
    - search found (with header) & not found
    - zero-generation edge case
    """

    def run_cli(self, args):
        """
        Helper to simulate running the CLI.
        Captures stdout for inspection.
        """
        old_argv = sys.argv
        old_stdout = sys.stdout
        sys.argv = ['cli'] + args
        sys.stdout = io.StringIO()
        try:
            try:
                cli_main()  # invoke the CLI entry point
            except SystemExit:
                # argparse may call sys.exit() for --help
                pass
            return sys.stdout.getvalue()
        finally:
            sys.argv = old_argv
            sys.stdout = old_stdout

    def test_help(self):
        # PART: --help flag
        out = self.run_cli(['--help'])
        self.assertIn('usage:', out)
        self.assertIn('--generate', out)
        self.assertIn('--search', out)
        self.assertIn('--sort', out)

    def test_generate_only(self):
        # PART: generation only
        out = self.run_cli(['-g', '2'])
        self.assertIn('Generated 2 items.', out)
        # should NOT print any JSON lines since no sort/search
        self.assertNotIn('{"id":', out)

    def test_sort_with_seed(self):
        # PART: sorting with seed (deterministic output)
        out = self.run_cli(['--seed', '1', '-g', '3', '-o', 'asc'])
        # collect JSON lines
        json_lines = [l for l in out.splitlines() if l.startswith('{"id":')]
        self.assertEqual(len(json_lines), 3)
        # ensure each line is valid JSON with expected keys
        for line in json_lines:
            data = json.loads(line)
            self.assertIn('id', data)
            self.assertIn('name', data)
            self.assertIn('date', data)

    def test_search_found_and_header(self):
        # PART: search when item exists
        # 1) Generate & sort with seed to capture a known name
        out1 = self.run_cli(['--seed', '2', '-g', '4', '-o', 'asc'])
        json_lines = [l for l in out1.splitlines() if l.startswith('{"id":')]
        sample = json.loads(json_lines[1])  # pick second item
        name = sample['name']
        # 2) Search for that name
        out2 = self.run_cli(['--seed', '2', '-g', '4', '-s', name])
        self.assertIn('Retrieved Items:', out2)
        self.assertIn(f'"name": "{name}"', out2)

    def test_search_not_found(self):
        # PART: search when item missing
        out = self.run_cli(['-g', '1', '-s', 'NoSuchName'])
        self.assertIn('No item named NoSuchName', out)

    def test_zero_generate_and_sort(self):
        # PART: zero-generation + sort edge case
        out = self.run_cli(['--seed', '3', '-g', '0', '-o', 'desc'])
        self.assertIn('Generated 0 items.', out)
        # should not print any JSON lines for empty list
        json_lines = [l for l in out.splitlines() if l.startswith('{"id":')]
        self.assertEqual(len(json_lines), 0)

if __name__ == '__main__':
    # Allows running this test file directly
    unittest.main()
