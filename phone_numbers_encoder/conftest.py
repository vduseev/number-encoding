"""
This is a set of py.test fixtures shared across multiple tests.
"""
import pytest


@pytest.fixture(scope='session')
def given_mapping():
    return {
        '0': {'e', 'E'},
        '1': {'J', 'N', 'Q', 'j', 'n', 'q'},
        '2': {'R', 'W', 'X', 'r', 'w', 'x'},
        '3': {'D', 'S', 'Y', 'd', 's', 'y'},
        '4': {'F', 'T', 'f', 't'},
        '5': {'A', 'M', 'a', 'm'},
        '6': {'C', 'I', 'V', 'c', 'i', 'v'},
        '7': {'B', 'K', 'U', 'b', 'k', 'u'},
        '8': {'L', 'O', 'P', 'l', 'o', 'p'},
        '9': {'G', 'H', 'Z', 'g', 'h', 'z'}
    }


@pytest.fixture(scope='session')
def inverted_mapping():
    return {
        'E': '0', 'e': '0', 'j': '1', 'n': '1', 'Q': '1', 'q': '1',
        'J': '1', 'N': '1', 'X': '2', 'W': '2', 'r': '2', 'w': '2',
        'x': '2', 'R': '2', 'y': '3', 'S': '3', 'D': '3', 'Y': '3',
        's': '3', 'd': '3', 't': '4', 'F': '4', 'T': '4', 'f': '4',
        'M': '5', 'A': '5', 'a': '5', 'm': '5', 'v': '6', 'I': '6',
        'i': '6', 'V': '6', 'c': '6', 'C': '6', 'u': '7', 'b': '7',
        'B': '7', 'U': '7', 'k': '7', 'K': '7', 'P': '8', 'l': '8',
        'o': '8', 'p': '8', 'L': '8', 'O': '8', 'h': '9', 'H': '9',
        'G': '9', 'g': '9', 'Z': '9', 'z': '9'
    }


@pytest.fixture(scope='session')
def ignored_dict_chars():
    return ['-', '"']


@pytest.fixture(scope='session')
def ignored_phone_number_chars():
    return ['-', '/']


@pytest.fixture(scope='session')
def words_and_encodings():
    return [
        ('an', '51'),
        ('blau', '7857'),
        ('Bo"', '78'),
        ('Boot', '7884'),
        ('bo"s', '783'),
        ('da', '35'),
        ('Fee', '400'),
        ('fern', '4021'),
        ('Fest', '4034'),
        ('fort', '4824'),
        ('je', '10'),
        ('jemand', '105513'),
        ('mir', '562'),
        ('Mix', '562'),
        ('Mixer', '56202'),
        ('Name', '1550'),
        ('neu', '107'),
        ('o"d', '83'),
        ('Ort', '824'),
        ('so', '38'),
        ('Tor', '482'),
        ('Torf', '4824'),
        ('Wasser', '253302')
    ]


@pytest.fixture(scope='session')
def dictionary_file():
    content = \
        'an\n'\
        'blau\n'\
        'Bo"\n'\
        'Boot\n'\
        'bo"s\n'\
        'da\n'\
        'Fee\n'\
        'fern\n'\
        'Fest\n'\
        'fort\n'\
        'je\n'\
        'jemand\n'\
        'mir\n'\
        'Mix\n'\
        'Mixer\n'\
        'Name\n'\
        'neu\n'\
        'o"d\n'\
        'Ort\n'\
        'so\n'\
        'Tor\n'\
        'Torf\n'\
        'Wasser'
    return content


@pytest.fixture(scope='session')
def phone_numbers_file():
    content = \
        '112\n'\
        '5624-82\n'\
        '4824\n'\
        '0721/608-4067\n'\
        '10/783--5\n'\
        '1078-913-5\n'\
        '381482\n'\
        '04824'
    return content


@pytest.fixture(scope='session')
def encoding():
    return {
        '51': {'an'},
        '7857': {'blau'},
        '78': {'Bo"'},
        '7884': {'Boot'},
        '783': {'bo"s'},
        '35': {'da'},
        '400': {'Fee'},
        '4021': {'fern'},
        '4034': {'Fest'},
        '4824': {'fort', 'Torf'},
        '10': {'je'},
        '105513': {'jemand'},
        '562': {'mir', 'Mix'},
        '56202': {'Mixer'},
        '1550': {'Name'},
        '107': {'neu'},
        '83': {'o"d'},
        '824': {'Ort'},
        '38': {'so'},
        '482': {'Tor'},
        '253302': {'Wasser'}
    }


@pytest.fixture(scope='session')
def encoded_digit_strings():
    return [
        ('562482', {'mir Tor', 'Mix Tor'}),
        ('4824', {'Torf', 'fort', 'Tor 4'}),
        ('107835', {'neu o"d 5', 'je bo"s 5', 'je Bo" da'}),
        ('381482', {'so 1 Tor'}),
        ('04824', {'0 Torf', '0 fort', '0 Tor 4'})
    ]


@pytest.fixture(scope='session')
def encoded_phone_numbers():
    return {
        '5624-82': {'mir Tor', 'Mix Tor'},
        '4824': {'Torf', 'fort', 'Tor 4'},
        '10/783--5': {'neu o"d 5', 'je bo"s 5', 'je Bo" da'},
        '381482': {'so 1 Tor'},
        '04824': {'0 Torf', '0 fort', '0 Tor 4'}
    }
