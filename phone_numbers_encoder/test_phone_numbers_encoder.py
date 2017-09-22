import pytest
from phone_numbers_encoder.phone_numbers_encoder import *
from phone_numbers_encoder.conftest import *


@pytest.mark.parametrize('string, expected', [
    ('', False),
    ('as ', False),
    ('4s', False),
    ('4\n', False),
    ('910', True),
    ('Ab"- Gos 5', True),
    ('Tor 4', True)
])
def test_is_last_char_digit(string, expected):
    assert is_last_char_digit(string) == expected


@pytest.mark.parametrize('digit_string, expected', [
    ('562482', {'mir', 'Mix'}),
    ('4824', {'Torf', 'fort', 'Tor'}),
    ('04824', set())
])
def test_get_words_fitting_into_digit_string(
        digit_string,
        expected,
        encoding):

    assert get_words_fitting_into_digit_string(
        digit_string,
        encoding
    ) == expected


@pytest.mark.parametrize('digit_string, expected', encoded_digit_strings())
def test_encode_digit_string(
        digit_string,
        expected,
        encoding,
        ignored_dict_chars):

    for encoded_number in encode_digit_string(
            digit_string=digit_string,
            encoding=encoding,
            ignored_dict_chars=ignored_dict_chars):

        assert encoded_number in expected


def test_encode_phone_numbers_file(
        tmpdir,
        phone_numbers_file,
        encoding,
        ignored_dict_chars,
        ignored_phone_number_chars,
        encoded_phone_numbers):
    tmp = tmpdir.join('phone_numbers.txt')
    tmp.write(phone_numbers_file)

    for number, encoded_number in encode_phone_numbers_file(
            path=tmp.realpath(),
            encoding=encoding,
            ignored_dict_chars=ignored_dict_chars,
            ignored_phone_number_chars=ignored_phone_number_chars):

        assert encoded_number in encoded_phone_numbers[number]


def test_encode_and_print_phone_numbers():
    pass
