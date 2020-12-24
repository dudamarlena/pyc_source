# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/feldbauer/PycharmProjects/hubness/skhubness/utils/io.py
# Compiled at: 2019-10-11 04:29:10
# Size of source mod 2**32: 1040 bytes
import logging
from tempfile import mkstemp, NamedTemporaryFile
__all__ = [
 'create_tempfile_preferably_in_dir']

def create_tempfile_preferably_in_dir(suffix=None, prefix=None, directory=None, persistent: bool=False):
    """ Create a temporary file with precedence for directory if possible, in TMP otherwise.
    For example, this is useful to try to save into /dev/shm.
    """
    temp_file = mkstemp if persistent else NamedTemporaryFile
    try:
        handle = temp_file(suffix=suffix, prefix=prefix, dir=directory)
        warn = False
    except FileNotFoundError:
        handle = temp_file(suffix=suffix, prefix=prefix, dir=None)
        warn = True

    try:
        path = handle.name
    except AttributeError:
        _, path = handle

    if warn:
        logging.warning(f"Could not create temp file in {directory}. Instead, the path is {path}.")
    return path