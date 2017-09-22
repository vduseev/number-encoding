import pytest
from phone_numbers_encoder\
    .encoding_scheme_builder.encoding_scheme_builder import *
from phone_numbers_encoder.conftest import *


@pytest.mark.parametrize('string, removables, expected', [
    ('bo"', ['-', '/', '"'], 'bo'),
    ('bo"', ['-'], 'bo"'),
    ('As5/--d', ['/', '-', '\n'], 'As5d'),
    ('As5/--d\r\n', ['/', '-', '\n', '\r'], 'As5d')
])
def test_remove_characters(string, removables, expected):
    assert remove_characters(string, removables) == expected


def test_invert_mapping(given_mapping):
    inverted_mapping = invert_mapping(given_mapping)

    assert inverted_mapping['e'] == '0'
    assert inverted_mapping['a'] == '5'
    assert inverted_mapping['A'] == '5'
    assert inverted_mapping['i'] == '6'


@pytest.mark.parametrize('word, expected', words_and_encodings())
def test_encode_word_using_mapping(
        word,
        expected,
        inverted_mapping,
        ignored_dict_chars):

    assert encode_word_using_mapping(
        word, inverted_mapping, ignored_dict_chars
    ) == expected


def test_map_words_to_numbers(
        words_and_encodings,
        inverted_mapping,
        ignored_dict_chars):

    example = {pair[0]: pair[1] for pair in words_and_encodings}
    mapping = map_words_to_numbers(
        example.keys(), inverted_mapping, ignored_dict_chars
    )
    numbers = example.values()
    for number in numbers:
        words = mapping[number]
        for word in words:
            assert word in mapping[number]


def test_build_encoding_from_file(
        tmpdir,
        dictionary_file,
        given_mapping,
        ignored_dict_chars,
        encoding):
    tmp = tmpdir.join('dictionary.txt')
    tmp.write(dictionary_file)
    built_encoding = build_encoding_from_file(
        tmp.realpath(), given_mapping, ignored_dict_chars
    )
    assert built_encoding == encoding
