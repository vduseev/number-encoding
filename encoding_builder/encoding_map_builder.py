"""The following mapping from letters to digits is given
(see numberencoding.txt requirement - 20 Feb 2012):

E | J N Q | R W X | D S Y | F T | A M | C I V | B K U | L O P | G H Z
e | j n q | r w x | d s y | f t | a m | c i v | b k u | l o p | g h z
0 |   1   |   2   |   3   |  4  |  5  |   6   |   7   |   8   |   9

This mapping is used to build the inverse mapping where by referencing
a character a digit is returned.
"""
_GIVEN_MAPPING = {
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


def build_encoding(path):

    # Standard mapping from requirements is given in an inconvenient format
    # for processing. It is inverted so that letter becomes the key.
    char_to_digit_mapping = _invert_given_mapping(_GIVEN_MAPPING)

    # Read the whole words encoding_builder into the memory and build
    # encoding mapping out of it. This mapping will be used to encode
    # phone numbers.
    dictionary_words = []
    with open(path, mode='r') as dictionary_file:
        for line in dictionary_file:
            word = remove_characters(line, ['\n', '\r', '"', '-'])
            dictionary_words.append(word)

    encoding_mapping = _map_words_to_numbers(
        words=dictionary_words,
        char_to_digit_mapping=char_to_digit_mapping
    )

    return encoding_mapping


def remove_characters(string, chars):
    result = string
    for char in chars:
        result = result.replace(char, '')
    return result


def _invert_given_mapping(given_mapping):
    """Build an inverse mapping where character is the key and corresponding
    digit is the value.

    :param given_mapping: Initial mapping as given by the requirements
    :return: inverse mapping
    """

    inverse_mapping = {}
    for key in given_mapping:
        for char in given_mapping[key]:
            inverse_mapping[char] = key

    return inverse_mapping


def _map_words_to_numbers(words, char_to_digit_mapping):
    """Build a dict with encodings as keys and list of words having such
    encoding as values.

    Key     - is a string of digits encoded according to mapping dict.
    Value   - is a list [] of all words from encoding_builder file that
              are encoded by such string.

    :param words: list of all words from encoding_builder file
    :return: encoding encoding_builder
    """

    # Encoded encoding_builder with encoding as a key and a list of associated
    # words as a value.
    mapping = {}

    # For each word calculate the encoded value
    for word in words:
        word_encoding = _encode_word_with_char_to_digit_mapping(
            word,
            char_to_digit_mapping
        )

        # Check if some word already produced same encoding.
        if word_encoding in mapping:
            # If yes, add the current word as an additional encoding option.
            mapping[word_encoding].add(word)
        else:
            # If no, add a new key with the current word as the first list
            # value.
            mapping[word_encoding] = {word}

    return mapping


def _encode_word_with_char_to_digit_mapping(word, mapping):
    """Represent given word as a string of digits according to the mapping
    given in the requirements.

    The words in the encoding_builder contain letters
    (capital or small, but the difference is ignored in the sorting), dashes
    - and double quotes " . For the encoding only the letters are used.

    :param word:
    :param mapping:
    :return: String of digits representing given word
    """

    # remove umlaut symbol (represented by double quotes) and dashes
    clean_word = remove_characters(word, ['"', '-'])

    encoding = ''
    for char in clean_word:
        encoding += mapping[char]

    return encoding




