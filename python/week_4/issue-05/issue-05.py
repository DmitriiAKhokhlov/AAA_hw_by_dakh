import unittest
from unittest.mock import patch
import func
import json


class TestWhatIsYearNow(unittest.TestCase):
    @patch("func.urllib.request.urlopen")
    def test_get_cases(self, urllib_mock):
        s = json.dumps({"currentDateTime": "01.03.2019"})
        urllib_mock.return_value.__enter__.return_value = s



        #with patch("func.urllib.request.urlopen") as mocked_get_cases:
        #s = json.dumps({'currentDateTime': '01.03.2019'})
        #mocked_get_cases.return_value.__enter__ = s
        self.assertEqual(func.what_is_year_now(), '2019')
#urllib.request.urlopen.return_value