"""Distills massive CI build logs down to specific failing assertions."""
import re
from typing import Dict, List, Optional, Tuple, Any

class RootCauseSummary:
    def __init__(self, failure_type: str, failing_file: Optional[str], line_num: Optional[int], error_message: str):
        self.failure_type = failure_type
        self.failing_file = failing_file
        self.line_num = line_num
        self.error_message = error_message

    def to_summary_text(self) -> str:
        return f"Failure [{self.failure_type}] at {self.failing_file}:{self.line_num} -> {self.error_message}"

class CILogAnalyzer:
    """Parses Python unittest/pytest logs to isolate exact failures."""

    @staticmethod
    def parse_log(raw_log: str) -> Optional[RootCauseSummary]:
        lines = raw_log.splitlines()

        # Look for AssertionError or Exception
        for idx, line in enumerate(lines):
            if "AssertionError" in line or "Error:" in line or "FAILED" in line:
                error_msg = line.strip()
                # Search backwards for File "... line ..."
                failing_file = None
                line_num = None
                for back in range(idx - 1, max(-1, idx - 10), -1):
                    file_match = re.search(r'File "([^"]+)", line (\d+)', lines[back])
                    if file_match:
                        failing_file = file_match.group(1)
                        line_num = int(file_match.group(2))
                        break

                f_type = error_msg.split(":")[0] if ":" in error_msg else "AssertionFailure"
                return RootCauseSummary(f_type, failing_file, line_num, error_msg)

        return None
