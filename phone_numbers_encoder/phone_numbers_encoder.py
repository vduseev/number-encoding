from phone_numbers_encoder.encoding_scheme_builder import\
    remove_characters, \
    build_encoding_from_file


def encode_and_print_phone_numbers(
        dictionary_path,
        input_path,
        digit_to_char_mapping,
        ignored_dict_chars,
        ignored_phone_number_chars):

    # Read dictionary file with words and map each word to the corresponding
    # digit string using digit to character mapping
    encoding = build_encoding_from_file(
        path=dictionary_path,
        given_mapping=digit_to_char_mapping,
        ignored_dict_chars=ignored_dict_chars
    )

    # For each encoding found print the phone number
    # followed by a colon, a single(!) space, and the encoding on one line;
    # trailing spaces are not allowed.
    # (as per numberencoding.txt requirements)
    for number, encoded_number in encode_phone_numbers_file(
            path=input_path,
            encoding=encoding,
            ignored_dict_chars=ignored_dict_chars,
            ignored_phone_number_chars=ignored_phone_number_chars):

        print(number + ': ' + encoded_number)


def encode_phone_numbers_file(
        path,
        encoding,
        ignored_dict_chars,
        ignored_phone_number_chars):
    """Finds, for a given phone number, all possible encodings by words,
    and yields original number with each possible encoding as a tuple

    :param path: path to txt file with phone numbers
    :param encoding: encoding dictionary used to encode phone numbers
    :param ignored_chars: list of chars to be ignored when encoding the number
    :return:
    """

    with open(path, mode='r') as phone_numbers_file:
        for line in phone_numbers_file:
            number = line.rstrip('\r').rstrip('\n')

            # Only digits
            digit_string = remove_characters(
                number,
                ignored_phone_number_chars
            )

            # Find possible encodings by words using built encoding
            for encoded_number in encode_digit_string(
                    digit_string=digit_string,
                    encoding=encoding,
                    ignored_dict_chars=ignored_dict_chars):

                yield number, encoded_number


def encode_digit_string(digit_string, encoding, ignored_dict_chars):
    """Yield each possible encoding for a phone number

    Encodings of phone numbers can consist of a single word or of multiple
    words separated by spaces. The encodings are built word by word from
    left to right. If and only if at a particular point no word at all from
    the dictionary can be inserted, a single digit from the phone number can
    be copied to the encoding instead. Two subsequent digits are never
    allowed.
    (as per numberencoding.txt requirements)

    :param digit_string:
    :param encoding:
    :return:
    """

    # Queue of partial encodings; Initial value is fake and will not produce
    # any results.
    queue = {''}

    while queue:
        # Each iteration some partial encoding is considered
        partial_encoding = queue.pop()

        # Partial encoding consists of several words separated by
        # space character. However, phone number parameter is given in
        # digits only, without any separators.
        # Hence, spaces between words and other ignored dict character are
        # removed to correctly compare the lengths of phone number and
        # partial encoding.
        clean_partial_encoding = remove_characters(
            partial_encoding, ignored_dict_chars + [' ']
        )
        partial_encoding_length = len(clean_partial_encoding)

        # If partial encoding reached the length of the phone number,
        # then there are no more digits to be encoded.
        # Encoding is added to final result set. And it is not put back
        # in the queue.
        if partial_encoding_length == len(digit_string):
            # encoded_numbers.add(partial_encoding)
            yield partial_encoding
            continue

        # Check what words fit into the part of the phone number
        # that is not encoded yet
        fitting_words = get_words_fitting_into_digit_string(
            digit_string=digit_string[partial_encoding_length:],
            encoding=encoding
        )

        # If some words fit into that part, then build a new set of
        # partial encodings out of them, combining initial partial
        # encoding with fitting words.
        # Then add them back to the queue for further processing.
        if len(fitting_words) > 0:
            combos_with_fitting_words = {
                partial_encoding
                + (' ' if len(partial_encoding) > 0 else '')
                + word for word in fitting_words
            }
            queue |= combos_with_fitting_words
            continue

        # When no fitting words are found then encode one symbol of
        # phone number with itself, but only if no fitting words are
        # found and last character of encoding is not a digit already.
        if not is_last_char_digit(partial_encoding):
            partial_encoding_plus_digit = {
                partial_encoding
                + (' ' if len(partial_encoding) > 0 else '')
                + digit_string[partial_encoding_length]
            }
            queue |= partial_encoding_plus_digit


def get_words_fitting_into_digit_string(digit_string, encoding):
    """Takes a string consisting of digits and returns a set of words from
    encoding that fit into this string starting with the first character.

    ## Example

    Let digit_string = 48245;
    Let encoding = {'4824': {'Torf', 'fort'}, '482': {'Tor'}, '5': {'a'}}

    Then following examples will be correct:
    * 48245 Torf
    * 48245 fort
    * 48245 Tor

    Torf, fort and Tor all fit into 42845 string.

    ## Algorithm logic

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
       48245 string in encoding encoding_scheme_builder

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
            # encoding_scheme_builder under the current possible encoding key,
            # and adds them to the fitting encodings set
            fitting_words |= encoding[current_possible_encoding]

        pos += 1

    return fitting_words


def is_last_char_digit(string):
    if len(string) > 0:
        if string[-1].isdigit():
            return True
    return False
