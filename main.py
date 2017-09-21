from phone_numbers_encoder import phone_numbers_file_encoder
from encoding_builder import build_encoding


if __name__ == '__main__':
    dictionary_path = 'dictionary.txt'
    phone_numbers_path = 'input.txt'

    encoding = build_encoding(dictionary_path)

    for number_and_encoding in phone_numbers_file_encoder(
            input_path=phone_numbers_path,
            encoding=encoding):

        original_number = number_and_encoding[0]
        encoded_number = number_and_encoding[1]

        print(original_number + ': ' + encoded_number)
