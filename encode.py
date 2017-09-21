import argparse
import configparser
from phone_numbers_encoder import encode_phone_numbers_file
from encoding_scheme_builder import build_encoding


if __name__ == '__main__':
    # Default paths to read data from
    default_dictionary_path = 'docs/requirements/test_dictionary.txt'
    default_input_path = 'docs/requirements/test_input.txt'
    default_config_path = 'encoder_config.ini'

    # Set up argument parser for the script
    parser = argparse.ArgumentParser(description='Encode phone numbers.')
    parser.add_argument(
        '-i', '--input',
        type=str,
        dest='input_path',
        default=default_input_path,
        help='path to input file with phone numbers'
    )
    parser.add_argument(
        '-d', '--dictionary',
        type=str,
        dest='dictionary_path',
        default=default_dictionary_path,
        help='path to dictionary file with words that will be used for encoding'
    )
    parser.add_argument(
        '-c', '--config',
        type=str,
        dest='config_path',
        default=default_config_path,
        help='path to config file with digit to char mapping and '
             'sets of characters that will be ignored during encoding'
    )
    args = parser.parse_args()

    # Read config file
    config = configparser.ConfigParser()
    config.read(args.config_path)
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
    encoding = build_encoding(
        args.dictionary_path,
        mapping,
        dict_ignored_chars
    )

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
            input_path=args.input_path,
            encoding=encoding,
            ignored_chars=phone_number_ignored_chars):

        original_number = number_and_encoding[0]
        encoded_number = number_and_encoding[1]

        print(original_number + ': ' + encoded_number)
