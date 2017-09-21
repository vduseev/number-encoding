from phone_numbers_encoder import print_encodings_for_phone_numbers


if __name__ == '__main__':
    dictionary_path = 'test_dictionary.txt'
    phone_numbers_path = 'test_input.txt'

    print_encodings_for_phone_numbers(
        input_path=phone_numbers_path,
        dictionary_path=dictionary_path
    )
