# tests/test_daily_issue_helper.py
from daily_issue_helper import get_today_day
from datetime import date
import sys
import os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


def test_get_today_day():
    start = date(2025, 1, 1)
    assert get_today_day(start) == 3
