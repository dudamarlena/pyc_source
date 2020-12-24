# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\autotest\decorator.py
# Compiled at: 2019-04-15 01:01:24
# Size of source mod 2**32: 1034 bytes
import os, shutil, logging, time
from functools import wraps

def log(filename):

    def wrapper(func):

        @wraps(func)
        def _wrapper(*args, **kwargs):
            logging.info('execution case in ' + filename + '-->' + _wrapper.__name__)
            result = func(*args, **kwargs)
            return result

        return _wrapper

    return wrapper


def clear_dir(dir):

    def wrapper(func):

        @wraps(func)
        def _wrapper(*args, **kwargs):
            for entry in os.scandir(dir):
                if entry.name.startswith('.'):
                    pass
                else:
                    if entry.is_file():
                        os.remove(entry.path)
                    else:
                        shutil.rmtree(entry.path)

            result = func(*args, **kwargs)
            return result

        return _wrapper

    return wrapper