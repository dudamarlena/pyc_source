# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\filthypasswordgenerator\pwgenerator.py
# Compiled at: 2019-02-22 11:33:34
# Size of source mod 2**32: 3767 bytes
from random import randint, choice
import os, importlib, argparse

def load_dictionary():
    """
        Load dictionary.
    """
    module = importlib.import_module('filthypasswordgenerator.data.english')
    return getattr(module, 'dictionary')


def get_random_word(dictionary, min_word_length=3, max_word_length=8):
    """
        Returns a random word from the dictionary
    """
    while 1:
        word = choice(dictionary)
        if len(word) >= min_word_length and len(word) <= max_word_length:
            break

    return word


def get_random_separator(no_special_characters=False):
    """
        Returns a random separator
    """
    separators = ('-', '_', ':', ';', '.', '=', '+', '%', '*')
    if not no_special_characters:
        return choice(separators)
    return ''


def get_random_int(max_int_value):
    """
        Returns a random number between 0 and `max_int_value`
    """
    return randint(0, max_int_value)


def set_int_position(number_of_elements):
    """
        Set the position of the integer in the final password
    """
    return randint(0, number_of_elements - 1)


def pw(min_word_length=3, max_word_length=8, max_int_value=1000, number_of_elements=4, no_special_characters=False):
    """
        Generate a password
    """
    int_position = set_int_position(number_of_elements)
    dictionary = load_dictionary()
    password = ''
    for i in range(number_of_elements):
        if i == int_position:
            password += str(get_random_int(max_int_value))
        else:
            password += get_random_word(dictionary, min_word_length, max_word_length).title()
        if i != number_of_elements - 1:
            password += get_random_separator(no_special_characters)

    return password


def main():
    """
        Main method
    """
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--min_word_length', type=int, help='Minimum length for each word',
      default=3)
    parser.add_argument('-x', '--max_word_length', type=int, help='Maximum length for each word',
      default=8)
    parser.add_argument('-i', '--max_int_value', type=int, help='Maximum value for the integer',
      default=1000)
    parser.add_argument('-e', '--number_of_elements', type=int, help='Number of elements in the password (ie. 4 = 3 words + 1 integer)',
      default=4)
    parser.add_argument('-s', '--no_special_characters', action='store_true',
      help='Do not use special characters')
    args = parser.parse_args()
    print(pw(min_word_length=(args.min_word_length), max_word_length=(args.max_word_length),
      max_int_value=(args.max_int_value),
      number_of_elements=(args.number_of_elements),
      no_special_characters=(args.no_special_characters)))


def generate():
    """
        To use the module within another module
    """
    return pw()


if __name__ == '__main__':
    main()