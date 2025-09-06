from daily_issue_helper import get_today_day
from datetime import date


def test_get_today_day():
    start = date(2025, 1, 1)
    today = date(2025, 1, 3)
    assert get_today_day(start, today) == 3
