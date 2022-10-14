from morse import decode


def test_hello():
    assert decode('.... . .-.. .-.. ---   .-- --- .-. .-.. -..') == 'HELLOWORLD'


def test_empty_string():
    assert decode("") == ''


def test_sos():
    assert decode('... --- ...') == 'SOS'
