import argparse
import configparser
from phone_numbers_encoder import encode_and_print_phone_numbers


def parse_arguments():
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
    return args


def parse_config(config_path):
    # Read config file
    config = configparser.ConfigParser()
    config.read(args.config_path)
    config_list_separator = ', '

    # Get digit to character mapping from config
    mapping = {}
    for digit in config['MAPPING']:
        mapping[digit] = set(
            config['MAPPING'][digit].split(config_list_separator)
        )

    # Get list of characters that will be ignored in words during encoding
    ignored_dict_chars = \
        config['IGNORED_CHARACTERS']['in_dictionary']\
        .split(config_list_separator)

    # Get list of characters that will be ignored in phone number during
    # encoding process
    ignored_phone_number_chars = \
        config['IGNORED_CHARACTERS']['in_phone_number']\
        .split(config_list_separator)

    setattr(config, 'mapping', mapping)
    setattr(config, 'ignored_dict_chars', ignored_dict_chars)
    setattr(config, 'ignored_phone_number_chars', ignored_phone_number_chars)
    return config


if __name__ == '__main__':
    args = parse_arguments()
    cfg = parse_config(args.config_path)

    encode_and_print_phone_numbers(
        dictionary_path=args.dictionary_path,
        input_path=args.input_path,
        digit_to_char_mapping=cfg.mapping,
        ignored_dict_chars=cfg.ignored_dict_chars,
        ignored_phone_number_chars=cfg.ignored_phone_number_chars
    )
