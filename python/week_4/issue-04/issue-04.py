from fit_transform import fit_transform


def test_empty_str():
    actual = str(fit_transform(''))
    expected = "[('', [1])]"
    assert actual == expected


def test_3_words():
    actual = str(fit_transform('abba', 'baab', 'baab'))
    expected = "[('abba', [0, 1]), ('baab', [1, 0]), ('baab', [1, 0])]"
    assert  actual == expected


def test_register():
    actual = str(fit_transform('AAA', 'aaa'))
    not_expected = "[('aaa', [1]), ('aaa', [1])]"
    assert actual != not_expected


def test_equal_strings():
    actual = str(fit_transform(*['aaa' for _ in range(10)]))
    in_actual = "('aaa', [1])"

    assert in_actual in actual


def test_raise():
    try:
        fit_transform(0)
    except TypeError as error_msg:
        assert error_msg
