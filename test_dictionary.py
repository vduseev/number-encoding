import pytest
from main import *


def test_mapping_inversion():
    inverse_mapping = inverse_initial_mapping(MAPPING)

    assert inverse_mapping['e'] == '0'
    assert inverse_mapping['A'] == '5'
    assert inverse_mapping['i'] == '6'


@pytest.fixture(scope='module')
def inverse_mapping():
    return inverse_initial_mapping(MAPPING)


ENCODED_DICTIONARY = [
    ('Bo"', '78'),
    ('bo"s', '783'),
    ('da', '35'),
    ('fort', '4824'),
    ('je', '10'),
    ('mir', '562'),
    ('Mix', '562'),
    ('neu', '107'),
    ('o"d', '83'),
    ('so', '38'),
    ('Tor', '482'),
    ('Torf', '4824')
]


@pytest.mark.parametrize('word, expected', ENCODED_DICTIONARY)
def test_word_encoding(word, expected, inverse_mapping):
    assert encode_word(word, inverse_mapping) == expected


def test_build_encoding_dictionary(inverse_mapping):
    words = [x[0] for x in ENCODED_DICTIONARY]
    encoded_dictionary = build_encoding_dictionary(words, inverse_mapping)

    for encoding_pair in ENCODED_DICTIONARY:
        key = encoding_pair[1]
        word = encoding_pair[0]

        assert key in encoded_dictionary
        assert word in encoded_dictionary[key]
