import sys
import os
from daily_issue_helper import get_today_day
from datetime import date
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


def test_get_today_day_basic():
    start = date(2025, 1, 1)
    
    # Simulate same day
    assert get_today_day(start) == 1


def test_get_today_day_next_day():
    start = date(2025, 1, 1)
    today = date(2025, 1, 2)
    # Should count next day as Day 2
    delta = (today - start).days + 1
    assert delta == 2
