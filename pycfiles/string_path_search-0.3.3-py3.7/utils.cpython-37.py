# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\string_path_search\utils.py
# Compiled at: 2019-08-09 20:26:02
# Size of source mod 2**32: 2013 bytes
"""Grab-bag of utility functions."""
import hashlib, logging, os, random, string, sys
LEVEL_STRINGS = {logging.DEBUG: 'DEBUG', logging.INFO: 'INFO', 
 logging.WARNING: 'WARNING', logging.ERROR: 'ERROR', 
 logging.CRITICAL: 'CRITICAL', logging.NOTSET: 'NOTSET'}
LOGGER = None

def random_string(length=5):
    """Return a random string of the desired length."""
    return ''.join(random.choices((string.ascii_uppercase + string.digits), k=length))


def calculate_md5(my_str):
    """Calculate the md5 digest of a string"""
    md5 = hashlib.md5()
    md5.update(my_str)
    return md5.hexdigest()


def make_dir_safe(path, raise_errors=True):
    """
    Create a directory. Optionally, suppress exceptions.

    Args:
        path -- The directory to create.

    Keyword_args
    """
    if os.path.isdir(path):
        return path
    try:
        os.makedirs(path, mode=511, exist_ok=True)
    except OSError as exc:
        try:
            eprint('ERROR: Path=%s does not exist and cannot be created. Errno=%d', path, exc.errno)
            if raise_errors:
                raise
            path = ''
        finally:
            exc = None
            del exc

    return path


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(args, file=sys.stderr, **kwargs)


def get_logger(log_level=logging.INFO, msg_format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)s- %(message)s', cls_name=__name__):
    """
    Instantiate a new logger.

    Args:
        log_level = One of the log reporting levels defined in the logging module
                    (Default:  logging.INFO)
        cls_name = Class name for this logger (Default: __name__)
    """
    logging.basicConfig(format=msg_format, level=log_level)
    return logging.getLogger(cls_name)


LOGGER = get_logger(cls_name=(os.path.basename(sys.argv[0])))