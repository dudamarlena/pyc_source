# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/gitdata/assertion.py
# Compiled at: 2019-03-15 07:56:09
__doc__ = '\nThe assertion module provides functions that will raise an exception if\nthe asserted condition is not met.\n\nThe use of the FileNotFound exception makes this Python3 ready.\nMaking them functions keeps the exception definition localized.\n'
import os, errno
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

try:
    ChildProcessError
except NameError:
    ChildProcessError = IOError

def isdir(path, message):
    """
    Raise an exception if the given directory does not exist.

    :param path: The path to a directory to be tested
    :param message: A custom message to report in the exception

    :raises: FileNotFoundError
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(errno.ENOENT, ('{}: {}').format(message, os.strerror(errno.ENOENT)), path)


def isfile(path, message):
    """
    Raise an exception if the given file does not exist.

    :param path: The path to a file to be tested
    :param message: A custom message to report in the exception

    :raises: FileNotFoundError
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(errno.ENOENT, ('{}: {}').format(message, os.strerror(errno.ENOENT)), path)


def success(exitcode, message):
    """
    Raise an IO Error if the return code from a subprocess is non-zero

    :param exitcode: The return code from a subprocess run
    :param message: A custom message if the process failed
    :raises: ChildProcessError
    """
    if exitcode is not 0:
        raise ChildProcessError('Command returned non-zero exit status: %s' % message)