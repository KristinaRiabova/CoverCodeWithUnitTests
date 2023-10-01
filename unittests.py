import unittest
from datetime import datetime, timedelta
from online_status import format_last_seen
from online_status import localize
from unittest.mock import Mock, patch
from online_status import load_user_data

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

class TestLocalize(unittest.TestCase):

    def test_localize_uk(self):
        translations = {
            "Just now": "Щойно",
            "Less than a minute ago": "Менше хвилини тому",
            "Couple of minutes ago": "Пару хвилин тому",
            "An hour ago": "Годину тому",
            "Today": "Сьогодні",
            "Yesterday": "Вчора",
            "This week": "Цього тижня",
            "Long time ago": "Давно",
        }

        for phrase, translation in translations.items():
            with self.subTest(phrase=phrase):
                self.assertEqual(localize(phrase, language="uk"), translation)

class TestLoadUserData(unittest.TestCase):

    @patch('online_status.requests.get')
    def test_load_user_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"userId": 1, "lastSeenDate": "2023-09-30T12:00:00Z"}]}
        mock_get.return_value = mock_response

        result = load_user_data(0)

        self.assertIsNotNone(result)
        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(result["data"][0]["userId"], 1)
        self.assertEqual(result["data"][0]["lastSeenDate"], "2023-09-30T12:00:00Z")

    @patch('online_status.requests.get')
    def test_load_user_data_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = load_user_data(0)

        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()