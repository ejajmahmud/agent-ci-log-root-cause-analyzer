"""CLI for agent-ci-log-root-cause-analyzer."""
import sys
import argparse
from .analyzer import CILogAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Agent CI Log Root Cause Analyzer CLI")
    parser.add_argument("--demo", action="store_true", help="Run CI log analyzer demo")
    args = parser.parse_args()

    if args.demo:
        sample_log = """
Step 4/5: Running tests
Traceback (most recent call last):
  File "tests/test_auth.py", line 42, in test_login
    self.assertEqual(token, "valid_token")
AssertionError: None != 'valid_token'
FAILED (failures=1)
"""
        summary = CILogAnalyzer.parse_log(sample_log)
        print(f"[+] Distilled root cause: {summary.to_summary_text()}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
