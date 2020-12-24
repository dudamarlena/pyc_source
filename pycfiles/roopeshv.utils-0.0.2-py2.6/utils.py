# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/roopeshv/utils/utils.py
# Compiled at: 2010-06-17 13:51:54
import datetime, os

def full_path(dir_):
    """Get the expanded path of directory ``dir_``
    
    Suppose, for existing users `~` is `/home/rv` and `~zope` 
    is `/usr/local/zope`.
::

    >>> full_path('~')
    '/home/rv'
    >>> full_path('~zope')
    '/usr/local/zope'

    For a non existant user `~test`, the result will be 
    current_directory/~test
::

    >>> full_path('~test')
    '/home/rv/expertpy/roopeshv.utils/roopeshv/utils/~test'

    """
    if dir_[0] == '~' and not os.path.exists(dir_):
        dir_ = os.path.expanduser(dir_)
    return os.path.abspath(dir_)


def join_path(*x):
    """Join the list to form a directory path
    
    This is just a convenience function.
::

    >>> join_path('~', 'test')
    '~/test'
    >>> join_path('/home/rv', 'test')
    '/home/rv/test'
    >>> join_path('test', 'README.txt')
    'test/README.txt'

    """
    return os.path.join(*x)


def is_directory(dir_):
    """determine if dir_ is a directory ``dir_``

::

    >>> is_directory('.')
    True
    >>> is_directory('~')
    True
    >>> is_directory('/')
    True
    >>> is_directory('no/such/directory')
    False

    """
    dir_ = full_path(dir_)
    return os.path.isdir(dir_)


def get_files_in(dir_, suffix=None):
    """get a list of files(absolute path) in directory ``dir_``
    or list of files of particular extension in that directory.
    
    if the extension of the file is present in the list of suffixes
    given in the suffix argument, then those files will be output

::

    # the .directory happens to exist in my computer, but for now
    # the function works as intended.
    
    >>> get_files_in('/home/')
    ['/home/.directory']
    >>> '/etc/passwd' in get_files_in('/etc/') 
    True

    """
    dir_ = full_path(dir_)
    return [ join_path(dir_, each) for each in os.listdir(full_path(dir_)) if not is_directory(join_path(dir_, each)) ]


def get_directories_in(dir_):
    """get a list of directories(absolute path) in directory ``dir_``

::

    >>> sorted(get_directories_in('/home/'))
    ['/home/guest', '/home/rv']
    >>> '/home/rv/Desktop' in get_directories_in('~')
    True

    """
    dir_ = full_path(dir_)
    return [ join_path(dir_, each) for each in os.listdir(full_path(dir_)) if is_directory(join_path(dir_, each)) ]


def get_latest_file_in(dir_, prefix=[]):
    """get the latest file in given directory, optionally of certain prefix

    With in a given directory, the function returns the recently modified file
    If a prefix or a list of prefixes is given then, the last modified file with
    that prefix is returned.
    """

    def _by_modified_time(file_):
        return os.stat(file_).st_mtime

    files = get_files_in(dir_)
    if isinstance(prefix, str):
        prefix = [
         prefix]
    files = [ file_ for file_ in files if prefix == [] or os.path.splitext(file_)[(-1)] in prefix ]
    sorted(files, key=_by_modified_time, reverse=True)
    return files[0]