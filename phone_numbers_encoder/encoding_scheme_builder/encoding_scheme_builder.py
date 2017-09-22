def build_encoding_from_file(path, given_mapping, ignored_dict_chars):

    # Standard mapping from requirements is given in an inconvenient format
    # for processing. It is inverted so that letter becomes the key.)
    char_to_digit_mapping = invert_mapping(given_mapping)

    # Read the whole words encoding_scheme_builder into the memory and build
    # encoding mapping out of it. This mapping will be used to encode
    # phone numbers.
    dictionary_words = []
    with open(path, mode='r') as dictionary_file:
        for line in dictionary_file:
            word = line.rstrip('\r').rstrip('\n')
            dictionary_words.append(word)

    # Each word is mapped to a digit string.
    # Certain chars are ignored during mapping
    encoding_mapping = map_words_to_numbers(
        words=dictionary_words,
        char_to_digit_mapping=char_to_digit_mapping,
        ignored_dict_chars=ignored_dict_chars
    )

    return encoding_mapping


def remove_characters(string, chars):
    result = string
    for char in chars:
        result = result.replace(char, '')
    return result


def invert_mapping(given_mapping):
    """Builds an inverted mapping where character is the key and corresponding
    digit is the value.

    :param given_mapping: initial mapping as dict
    :return: dict with inverted mapping
    """

    inverted_mapping = {}
    for key in given_mapping:
        for char in given_mapping[key]:
            inverted_mapping[char] = key

    return inverted_mapping


def map_words_to_numbers(words, char_to_digit_mapping, ignored_dict_chars):
    """Build a dict with encodings as keys and list of words having such
    encoding as values.

    Key     - is a string of digits encoded according to mapping dict.
    Value   - is a set of all words from encoding_scheme_builder file that
              are encoded by such string.

    :param words: list of all words from encoding_scheme_builder file
    :param char_to_digit_mapping: dict of character to digit mapping
    :param ignored_dict_chars: list of characters to ignore when encoding words
    :return: dict of numbers with sets of words encoded by them as values
    """

    # Encoded mapping with encoding as a key and a list of associated
    # words as a value.
    mapping = {}

    # For each word calculate the encoded value
    for word in words:
        word_encoding = encode_word_using_mapping(
            word=word,
            mapping=char_to_digit_mapping,
            ignored_dict_chars=ignored_dict_chars
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


def encode_word_using_mapping(word, mapping, ignored_dict_chars):
    """Represent given word as a string of digits according to the mapping
    given in the requirements.

    The words in the encoding_scheme_builder contain letters
    (capital or small, but the difference is ignored in the sorting), dashes
    - and double quotes " . For the encoding only the letters are used.

    :param word: word that needs to be converted to digit string
    :param mapping: dict of character to digit mapping
    :param ignored_dict_chars: list of characters to ignore when encoding words
    :return: string of digits representing given word
    """

    # remove umlaut symbol (represented by double quotes) and dashes
    clean_word = remove_characters(word, ignored_dict_chars)

    encoding = ''
    for char in clean_word:
        encoding += mapping[char]

    return encoding
