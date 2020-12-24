# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/filesys/files.py
# Compiled at: 2019-01-24 16:56:47
import errno, os

class FileDoesNotExist(Exception):
    """File does not exist."""
    pass


def GetFileContents(filename):
    """Returns the contents of a file.

  Args:
    filename: path to a file.
  Returns:
    a string.
  Raises:
    FileDoesNotExist: if the file does not exist
    IOError: for other local IO errors
  """
    try:
        return open(filename).read()
    except IOError as e:
        if e.errno == errno.ENOENT:
            raise FileDoesNotExist(filename)
        raise


def IsFile(filename):
    """Returns whether the named file is a regular file.

  Args:
    filename: path to a file.
  Returns:
    bool: whether the file is a regular file.
  """
    return os.path.isfile(filename)


def IterFiles(directory):
    """yield all files beneath a directory."""
    for root, unused_dirs, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.join(root, f)