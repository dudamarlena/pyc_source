# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/utils/stiff.py
# Compiled at: 2020-03-21 13:30:36
# Size of source mod 2**32: 2187 bytes
from os import walk, remove
from os.path import join
from shutil import rmtree
from threading import Thread

def cleaner(directory, *file, level=None):
    """
    **DANGER!** A function for cleaning objects and folders on the system.

    E.g:

    >>> import snakypy
    >>> snakypy.stiff.cleaner("/tmp/foo", level=0)
    >>> snakypy.stiff.cleaner("/tmp/foo", level=1)
    >>> snakypy.stiff.cleaner("/tmp/foo", "bar.txt")

    Arguments:
        **directory {str}** -- Directory where are the files to be destroyed

        ***file** -- Enter an N file name number (Optional)

    Keyword Arguments:
        **level {int}** -- This option receives 3 values, they are: 
                           Value 0 = If this value is set, the function revokes the                            unitary file exclusion option, that is, this option will                            exclude all files at the root of the informed directory.

                           Value 1 = If this value is set, the function revokes the unitary                            file exclusion option as well, however, it will exclude all                            subdirectories of the root directory, except the files contained                            in the root.

                           Value None = If this value is set, the function must receive at least                            one file name to be deleted. Can pass as many files as you want.

                           (default: {None})

    """
    data = next(walk(directory))
    if level == 0:
        for f in data[2]:
            remove(join(data[0], f))
        else:
            return 0

    if level == 1:
        for r, d, f in walk(directory, topdown=False):
            for item in d:
                t = Thread(target=(rmtree(join(r, item))), args=())
                t.start()
            else:
                return 1

    try:
        if file:
            for f in file:
                while True:
                    remove(join(data[0], f))

                return

    except FileNotFoundError as err:
        try:
            msg = '>>> There was an error removing the files'
            raise FileNotFoundError(msg, err)
        finally:
            err = None
            del err


__all__ = [
 'cleaner']