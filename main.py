from dictionary import build_encoding
"""Basic design ideas:
1. Define the mapping
2. Read the whole dictionary of words
3. Calculate a hash or something similar for each dictionary word
"""


def print_encodings_for_phone_numbers(input_path, dictionary_path):
    """Finds, for a given phone number, all possible encodings by words,
    and prints them.

    :param input_path: path to txt file with phone numbers
    :param dictionary_path: path to txt file with dictionary
    :return:
    """

    encoding = build_encoding(dictionary_path)

    with open(input_path, mode='r') as dictionary_file:
        for line in dictionary_file:
            number =  line.rstrip('\n').rstrip('\r')

            # Only digits
            only_digits_number = number.replace('-', '').replace('/', '')

            # Find possible encodings by words using built encoding dictionary
            possible_encodings = get_phone_number_encodings(
                only_digits_number, encoding
            )

            for encoded_number in possible_encodings:
                print(number + ':' + encoded_number)


def get_phone_number_encodings(phone_number, encoding):
    """

    :param phone_number:
    :param encoding:
    :return:
    """

    encoded_numbers = set()  # Result set to be returned

    # Queue of partial encodings; Initial value is fake and will not produce
    # any results.
    queue = {''}

    while queue:
        # Each iteration some partial encoding is considered
        partial_encoding = queue.pop()

        # Partial encoding consists of several words separated by
        # space character.
        # Phone number parameter is given in digits only, without
        # any separators.
        # Hence, spaces are removed to correctly compare the lengths
        # of phone number and partial encoding.
        clean_partial_encoding = partial_encoding\
            .replace(' ', '').replace('-', '').replace('"', '')
        partial_encoding_length = len(clean_partial_encoding)

        # If partial encoding reached the length of the phone number,
        # then there are no more digits to be encoded.
        # Encoding is added to final result set. And it is not put back
        # in the queue.
        if partial_encoding_length == len(phone_number):
            encoded_numbers.add(partial_encoding)
            continue

        # Check what words fit into the part of the phone number
        # that is not encoded yet
        fitting_words = get_words_fitting_into_digit_string(
            phone_number[partial_encoding_length:],
            encoding
        )

        # If some words fit into that part, then build a new set of
        # partial encodings out of them, combining initial partial
        # encoding with fitting words.
        # Then add them back to the queue for further processing.
        if len(fitting_words) > 0:
            queue |= {
                partial_encoding + ' ' + sub_encoding
                for sub_encoding in fitting_words
            }
            continue

        # When no fitting words are found then encode one symbol of
        # phone number with itself, but only if no fitting words are
        # found and last character of encoding is not a digit already.
        if not is_last_char_digit(partial_encoding):
            queue |= {
                partial_encoding + ' '
                + phone_number[partial_encoding_length]
            }

        # Do not add anything back to the queue. Encoding is considered
        # invalid when nothing above worked.
        # Hence, drop this partial encoding out of final queue.
        pass

    return encoded_numbers


def get_words_fitting_into_digit_string(digit_string, encoding):
    """Takes a string consisting of digits and returns a set of words from
    encoding that fit into this string starting with the first character.

    == Example ==

    Let digit_string = 48245;
    Let encoding = {'4824': {'Torf', 'fort'}, '482': {'Tor'}, '5': {'a'}}

    Then following examples will be correct:
    * 48245 Torf
    * 48245 fort
    * 48245 Tor

    Torf, fort and Tor all fit into 42845 string.

    == Algorithm logic ==

    1. 4....
       no encoding
    2. 48...
       no encoding
    3. 482..
       'Tor' is found in encoding; add it to results
    4. 4824.
       'Torf' and 'fort' are found; add to results
    5. 48245
       no encoding; '5' does not count; algorithm only look for the whole
       48245 string in encoding dictionary
    
    :param digit_string:
    :param encoding:
    :return: 
    """

    fitting_words = set()

    pos = 1  # only encodings with len >= 1 are considered
    while pos <= len(digit_string):
        current_possible_encoding = digit_string[:pos]
        # If encoding is found for 0..current_end digits of string
        if current_possible_encoding in encoding:
            # This line takes the whole set of words, residing in encoding
            # dictionary under the current possible encoding key, and adds
            # them to the fitting encodings set.
            fitting_words |= encoding[current_possible_encoding]

        pos += 1

    return fitting_words


def is_last_char_digit(string):
    if len(string) > 0:
        if string[-1].isdigit():
            return True
    return False


if __name__ == '__main__':
    dictionary_path = 'test_dictionary.txt'
    phone_numbers_path = 'test_input.txt'

    print_encodings_for_phone_numbers(
        input_path=phone_numbers_path,
        dictionary_path=dictionary_path
    )
