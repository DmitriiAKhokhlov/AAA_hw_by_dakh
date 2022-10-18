import unittest
from unittest.mock import patch
import func


class TestWhatIsYearNow(unittest.TestCase):
    @patch("func.json.load")
    @patch("func.urllib.request.urlopen")
    def test_dot_sep(self, urllib_mock, mock_json_load):
        s = dict({"currentDateTime": "01.03.2019"})
        mock_json_load.return_value = s
        self.assertEqual(func.what_is_year_now(), 2019)

    @patch("func.json.load")
    @patch("func.urllib.request.urlopen")
    def test_dash_sep(self, urllib_mock, mock_json_load):
        s = dict({"currentDateTime": "2019-03-01"})
        mock_json_load.return_value = s
        self.assertEqual(func.what_is_year_now(), 2019)

    @patch("func.json.load")
    @patch("func.urllib.request.urlopen")
    def test_incorrect_data(self, urllib_mock, mock_json_load):
        s = dict({"currentDateTime": "2019/03/01"})
        mock_json_load.return_value = s
        with self.assertRaises(ValueError) as ctx:
            func.what_is_year_now()
        self.assertEqual('Invalid format', str(ctx.exception))
# python -m unittest -q issue-05_test.py --cov=func