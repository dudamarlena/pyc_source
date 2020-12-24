# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/add.py
# Compiled at: 2018-03-24 02:07:47
# Size of source mod 2**32: 623 bytes
__doc__ = 'Add new file move setting.'
from .config import Config

def add_new_config(glob: str, path: str, is_regexp: bool=False) -> bool:
    """Add new path config.

    Arguments:
        glob {str} -- glob or regular expression text
        path {str} -- the path where the matched files move to

    Keyword Arguments:
        is_regexp {bool} -- if this parameter sets true,
                            the 'glob' parameter works as
                            regular expression (default: {False})

    Returns:
        bool -- is successful

    """
    config = Config()
    return config.add_glob_path(glob, path)