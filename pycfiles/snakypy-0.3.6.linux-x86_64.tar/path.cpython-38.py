# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/path.py
# Compiled at: 2020-03-21 13:31:04
# Size of source mod 2**32: 1419 bytes
from pathlib import Path

def create(*args, multidir=()):
    """
    Function that creates single or multiple directories.

    E.g:

    >>> import snakypy
    >>> dirs = ("/tmp/foo/bar", "/tmp/foo/xyz")
    >>> snakypy.path.create("/tmp/bar", "/tmp/bar/foo")
    >>> snakypy.path.create(multidir=dirs)
    >>> snakypy.path.create("/tmp/bar", "/tmp/bar/foo", multidir=dirs)

    Arguments:
        **args {str}** -- You must receive one or more unique arguments.

    Keyword Arguments:
        **multidir {tuple}** -- You should receive a tuple with the paths to be created.
    """
    try:
        if args:
            for directory in args:
                path = Path(directory)
                path.mkdir(parents=True, exist_ok=True)

    except TypeError:
        raise TypeError('>>> Invalid type. You should receive only one argument at a time.')
    except Exception:
        raise Exception(f">>> An error occurred while creating directory: {args}")

    try:
        if len(multidir) > 0:
            for directory in multidir:
                path = Path(directory)
                path.mkdir(parents=True, exist_ok=True)

    except TypeError:
        raise TypeError('>>> You should receive a tuple.')
    except Exception:
        raise Exception(f">>> There was an error creating directories: {multidir}")