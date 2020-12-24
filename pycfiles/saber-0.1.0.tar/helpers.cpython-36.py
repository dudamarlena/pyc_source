# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/johngiorgi/Documents/Masters/Class/natural_language_computing/project/saber/saber/tests/resources/helpers.py
# Compiled at: 2018-12-05 13:10:25
# Size of source mod 2**32: 2221 bytes
"""Any and all helper functions for Sabers unit tests.
"""
import configparser, os
from ... import constants

def assert_type_to_idx_as_expected(actual, expected):
    """Asserts that a `type_to_idx` mapping is as expected. This involves checking that it contains
    the expected, keys, the expected values, and that the values are a consecutive mapping of
    integers beginning at 0.
    """
    if not all(word in actual['word'] for word in expected['word']):
        raise AssertionError
    else:
        if not all(char in actual['char'] for char in expected['char']):
            raise AssertionError
        else:
            if not all(id in range(0, len(actual['word'])) for id in actual['word'].values()):
                raise AssertionError
            elif not all(id in range(0, len(actual['char'])) for id in actual['char'].values()):
                raise AssertionError
            assert all(word in actual['word'] for word in constants.INITIAL_MAPPING['word'])
        assert all(word in actual['char'] for word in constants.INITIAL_MAPPING['word'])


def load_saved_config(filepath):
    """Load a saved config.ConfigParser object at 'filepath/config.ini'.

    Args:
        filepath (str): filepath to the saved config file 'config.ini'

    Returns:
        parsed config.ConfigParser object at 'filepath/config.ini'.
    """
    saved_config_filepath = os.path.join(filepath, 'config.ini')
    saved_config = configparser.ConfigParser()
    saved_config.read(saved_config_filepath)
    return saved_config


def unprocess_args(args):
    """Unprocesses processed config args.

    Given a dictionary of arguments ('arg'), returns a dictionary where all values have been
    converted to string representation.

    Returns:
        args, where all values have been replaced by a str representation.
    """
    unprocessed_args = {}
    for arg, value in args.items():
        if isinstance(value, list):
            unprocessed_arg = ', '.join(value)
        else:
            if isinstance(value, dict):
                dict_values = [str(v) for v in value.values()]
                unprocessed_arg = ', '.join(dict_values)
            else:
                unprocessed_arg = str(value)
        unprocessed_args[arg] = unprocessed_arg

    return unprocessed_args