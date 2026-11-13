"""Unit tests for agent-ci-log-root-cause-analyzer."""
import unittest
from agent_ci_log_root_cause_analyzer.analyzer import CILogAnalyzer

class TestCILogAnalyzer(unittest.TestCase):
    def test_extract_assertion(self):
        log = chr(10).join(['File "src/test_api.py", line 18, in test_api', '    assert res.status == 200', 'AssertionError: Expected 200 got 500'])
        sum_obj = CILogAnalyzer.parse_log(log)
        self.assertIsNotNone(sum_obj)
        self.assertEqual(sum_obj.failing_file, "src/test_api.py")
        self.assertEqual(sum_obj.line_num, 18)
        self.assertIn("AssertionError", sum_obj.error_message)

if __name__ == "__main__":
    unittest.main()
