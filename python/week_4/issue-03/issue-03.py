import unittest
from fit_transform import fit_transform


class TestFitTransform(unittest.TestCase):
    def test_empty_str(self):
        actual = str(fit_transform(''))
        expected = "[('', [1])]"
        self.assertEqual(actual, expected)

    def test_3_words(self):
        actual = str(fit_transform('abba', 'baab', 'baab'))
        expected = "[('abba', [0, 1]), ('baab', [1, 0]), ('baab', [1, 0])]"
        self.assertEqual(actual, expected)

    def test_register(self):
        actual = str(fit_transform('AAA', 'aaa'))
        not_expected = "[('aaa', [1]), ('aaa', [1])]"
        self.assertFalse(actual == not_expected)

    def test_equal_strings(self):
        actual = str(fit_transform(*['aaa' for _ in range(10)]))
        in_actual = "('aaa', [1])"
        self.assertIn(in_actual, actual)

    def test_raise(self):
        self.assertRaises(TypeError, fit_transform, 0)