import unittest
from datetime import datetime, timedelta
from online_status import format_last_seen

class TestFormatLastSeen(unittest.TestCase):

    def test_format_last_seen_online(self):
        self.assertEqual(format_last_seen("Online"), "Online")

    def test_format_last_seen_just_now(self):
        now = datetime.now()
        last_seen = now.isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Щойно")

    def test_format_last_seen_less_than_minute_ago(self):
        now = datetime.now()
        last_seen = (now - timedelta(seconds=45)).isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Менше хвилини тому")

    def test_format_last_seen_couple_of_minutes_ago(self):
        now = datetime.now()
        last_seen = (now - timedelta(minutes=30)).isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Пару хвилин тому")

    def test_format_last_seen_an_hour_ago(self):
        now = datetime.now()
        last_seen = (now - timedelta(hours=1, minutes=30)).isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Годину тому")

    def test_format_last_seen_today(self):
        now = datetime.now()
        last_seen = (now - timedelta(hours=2)).isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Сьогодні")

    def test_format_last_seen_yesterday_start_of_day(self):
        now = datetime.now()
        last_seen = (now - timedelta(days=1)).replace(hour=20, minute=0, second=0, microsecond=0).isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Вчора")

    def test_format_last_seen_this_week(self):
        now = datetime.now()
        last_seen = (now - timedelta(days=3)).replace(hour=10, minute=0, second=0, microsecond=0).isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Цього тижня")

    def test_format_last_seen_long_time_ago(self):
        now = datetime.now()
        last_seen = (now - timedelta(days=30)).replace(hour=10, minute=0, second=0, microsecond=0).isoformat()
        self.assertEqual(format_last_seen(last_seen, language="uk"), "Давно")

if __name__ == "__main__":
    unittest.main()