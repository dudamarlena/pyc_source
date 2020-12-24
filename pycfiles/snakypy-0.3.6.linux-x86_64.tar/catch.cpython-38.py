# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/utils/catch.py
# Compiled at: 2020-03-21 13:30:36
# Size of source mod 2**32: 1814 bytes
from subprocess import check_output
from snakypy.utils import decorators

@decorators.only_for_linux
def shell():
    """
    Function to get the currently activated shell.
    Note: snakypy.catch.extension(file)

    >>> import snakypy
    >>> snakypy.catch.shell()

    **output:**

    .. code-block:: shell

        'zsh'

    Returns:
        [str] -- Returns the name of the current shell.
    """
    from sys import platform
    if not platform.startswith('win'):
        s = check_output('echo $0', shell=True, universal_newlines=True)
        lst = s.strip('\n').strip('').split('/')
        return lst[2]


def extension(filename, first_dot=False):
    """Get a file extension

    >>> import snakypy
    >>> file = '/tmp/file.tar.gz'
    >>> snakypy.catch.extension(file)
    >>> snakypy.catch.extension(file, first_dot=True)

    **output:**

    .. code-block:: shell

        'gz'
        '.tar.gz'

    Arguments:
        **filename {str}** -- Receives the file name or its full path

    Keyword Arguments:
        **first_dot {bool}** -- If it is True, I return the extension from the first                             point found, that is, if the file has more than one point,                             the first one will be the capture point, otherwise it will                             take the last point found. (Default: {False})

    Returns:
        [object] -- Returns a string containing the extension or None.
    """
    if first_dot:
        import re
        m = re.search('(?<=[^/\\\\]\\.).*$', filename)
        if not m:
            return
        ext = m.group(0)
        return ext
    from os.path import splitext
    ext = splitext(filename)[1]
    if ext:
        return ext
    return


__all__ = [
 'shell', 'extension']