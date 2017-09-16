"""Basic design ideas:
1. Define the mapping
2. Read the whole dictionary of words
3. Calculate a hash or something similar for each dictionary word
"""


"""The following mapping from letters to digits is given
(see numberencoding.txt requirement - 20 Feb 2012):

E | J N Q | R W X | D S Y | F T | A M | C I V | B K U | L O P | G H Z
e | j n q | r w x | d s y | f t | a m | c i v | b k u | l o p | g h z
0 |   1   |   2   |   3   |  4  |  5  |   6   |   7   |   8   |   9

This mapping is used to build the inverse mapping where by referencing
a character a digit is returned.
"""
MAPPING = {
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


def inverse_initial_mapping(mapping):
    """Build an inverse mapping where character is the key and corresponding
    digit is the value.

    :param mapping: Initial mapping as given by the requirements
    :return: inverse mapping
    """
    inverse_mapping = {}
    for key in mapping:
        for char in mapping[key]:
            inverse_mapping[char] = key

    return inverse_mapping


def read_dictionary_file(path):
    """Read all the lines from the dictionary and return them as a list.

    :param path:
    :return:
    """
    with open(path, mode='r') as dictionary_file:
        # Read all lines from the file
        words = dictionary_file.readlines()

    return words


def build_encoding_dictionary(words):
    """Build a dict with encodings as keys and list of words having such
    encoding as values.

    Key     - is a string of digits encoded according to mapping dict.
    Value   - is a list [] of all words from dictionary file that are encoded
              by such string.

    :param words: list of all words from dictionary file
    :return: encoding dictionary
    """

    # Encoded dictionary with encoding as a key and a list of associated
    # words as a value.
    encoded_dictionary = {}

    # For each word calculate the encoded value
    for word in words:
        word_encoding = encode_word(word)

        # Check if some word already produced same encoding.
        if word_encoding in encoded_dictionary:
            # If yes, add the current word as an additional encoding option.
            encoded_dictionary[word_encoding].add(word)
        else:
            # If no, add a new key with the current word as the first list
            # value.
            encoded_dictionary[word_encoding] = [word]

    return encoded_dictionary


def encode_word(word, mapping):
    """

    The words in the dictionary contain letters
    (capital or small, but the difference is ignored in the sorting), dashes
    - and double quotes " . For the encoding only the letters are used.

    :param word:
    :param mapping:
    :return: String of digits representing given word
    """
    # remove umlaut symbol (represented by double quotes) and dashes
    clean_word = word.replace('"', '').replace('-', '')

    encoding = ''
    for char in clean_word:
        encoding += mapping[char]

    return encoding


def read_phone_numbers(path):
    """Generator function that yields a phone numbers for each line in the file.

    A phone number is an arbitrary(!) string of dashes - , slashes / and digits.

    :param path:
    :return:
    """
    with open(path, mode='r') as phone_numbers_file:
        for line in phone_numbers_file:
            yield line


def strip_phone_number(phone_number):
    """ Strips phone number of the dashes and slashes.

    :param phone_number:
    :return: Phone number string without dashes and slashes
    """
    return phone_number.replace('-', '').replace('/', '')


def get_phone_number_encodings(phone_number, encoding_dictionary):
    queue = {''}

    while queue:
        encoding = queue.pop()

        encoding_length = len(encoding.replace(' ', ''))

        # find fitting subencodings
        sub_encodings = get_encodings_fitting_in_chunk(
            phone_number[encoding_length:],
            encoding_dictionary
        )

        if len(sub_encodings) == 0:
            if not encoding[-1].isdigit():  # TODO: won't work because encoding is all digits
                queue += {encoding + ' ' + phone_number[encoding_length]}
        else:
            encodings = {
                encoding + ' ' + sub_encoding
                for sub_encoding in sub_encodings
            }
            queue += encodings

    return []


def get_encodings_fitting_in_chunk(chunk, encoding_dictionary):
    fitting_encodings = set()

    current_end = 1  # only encodings with len >= 1 are considered
    while current_end < len(chunk):
        # If encoding is found for 0..current_end digits of chunk
        if chunk[0:current_end] in encoding_dictionary:
            fitting_encodings.add(chunk[0:current_end])

        current_end += 1

    return fitting_encodings


if __name__ == '__main__':
    words = read_dictionary_file('')

    encoding_dictionary = build_encoding_dictionary(words)

    for phone_number in read_phone_numbers(''):

        just_digits = strip_phone_number(phone_number)

        phone_number_encodings = get_phone_number_encodings(
            phone_number,
            encoding_dictionary
        )

        print('\n'.join(phone_number_encodings))
