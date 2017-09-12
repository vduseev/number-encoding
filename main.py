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
"""
mapping = {
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


def read_dictionary(path):
    """Read all the lines from the dictionary and return them as a list.

    :param path:
    :return:
    """

    with open(path, mode='r') as dictionary_file:
        # Read all lines from the file
        words = dictionary_file.readlines()

    return words


def encode_dictionary(words):
    # Encoded dictionary with encoding as a key and a list of corresponding
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


def encode_word(word):
    return word
