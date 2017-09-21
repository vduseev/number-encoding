import configparser
from phone_numbers_encoder import encode_phone_numbers_file
from encoding_builder import build_encoding


if __name__ == '__main__':
    dictionary_path = 'dictionary.txt'
    phone_numbers_path = 'input.txt'

    # Read config file
    config = configparser.ConfigParser()
    config.read('encoder_config.ini')
    config_list_separator = ', '

    # Get digit to character mapping from config
    mapping = {}
    for digit in config['MAPPING']:
        mapping[digit] = config['MAPPING'][digit].split(config_list_separator)

    # Get list of characters that will be ignored in words during encoding
    dict_ignored_chars = \
        config['IGNORED_CHARACTERS']['in_dictionary']\
        .split(config_list_separator)

    # Read dictionary file with words and map each word to the corresponding
    # digit string using digit to character mapping
    encoding = build_encoding(dictionary_path, mapping, dict_ignored_chars)

    # Get list of characters that will be ignored in phone number during
    # encoding process
    phone_number_ignored_chars = \
        config['IGNORED_CHARACTERS']['in_phone_number']\
        .split(config_list_separator)

    # For each encoding found print the phone number
    # followed by a colon, a single(!) space, and the encoding on one line;
    # trailing spaces are not allowed.
    # (as per numberencoding.txt requirements)
    for number_and_encoding in encode_phone_numbers_file(
            input_path=phone_numbers_path,
            encoding=encoding,
            ignored_chars=phone_number_ignored_chars):

        original_number = number_and_encoding[0]
        encoded_number = number_and_encoding[1]

        print(original_number + ': ' + encoded_number)
