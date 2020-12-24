# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stuart/Git/SWAT/pysac/astropy_helpers/astropy_helpers/utils.py
# Compiled at: 2015-11-25 06:17:20
# Size of source mod 2**32: 5174 bytes
import contextlib, imp, os, sys
try:
    from importlib import machinery as import_machinery
except ImportError:
    import_machinery = None

if sys.version_info[:2] >= (3, 3):
    from importlib import invalidate_caches
else:
    invalidate_caches = lambda : None

class _DummyFile(object):
    __doc__ = 'A noop writeable object.'
    errors = ''

    def write(self, s):
        pass

    def flush(self):
        pass


@contextlib.contextmanager
def silence():
    """A context manager that silences sys.stdout and sys.stderr."""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = _DummyFile()
    sys.stderr = _DummyFile()
    exception_occurred = False
    try:
        yield
    except:
        exception_occurred = True
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        raise

    if not exception_occurred:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


if sys.platform == 'win32':
    import ctypes

    def _has_hidden_attribute(filepath):
        """
        Returns True if the given filepath has the hidden attribute on
        MS-Windows.  Based on a post here:
        http://stackoverflow.com/questions/284115/cross-platform-hidden-file-detection
        """
        if isinstance(filepath, bytes):
            filepath = filepath.decode(sys.getfilesystemencoding())
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
            assert attrs != -1
            result = bool(attrs & 2)
        except (AttributeError, AssertionError):
            result = False

        return result


else:

    def _has_hidden_attribute(filepath):
        return False


def is_path_hidden(filepath):
    """
    Determines if a given file or directory is hidden.

    Parameters
    ----------
    filepath : str
        The path to a file or directory

    Returns
    -------
    hidden : bool
        Returns `True` if the file is hidden
    """
    name = os.path.basename(os.path.abspath(filepath))
    if isinstance(name, bytes):
        is_dotted = name.startswith(b'.')
    else:
        is_dotted = name.startswith('.')
    return is_dotted or _has_hidden_attribute(filepath)


def walk_skip_hidden(top, onerror=None, followlinks=False):
    """
    A wrapper for `os.walk` that skips hidden files and directories.

    This function does not have the parameter `topdown` from
    `os.walk`: the directories must always be recursed top-down when
    using this function.

    See also
    --------
    os.walk : For a description of the parameters
    """
    for root, dirs, files in os.walk(top, topdown=True, onerror=onerror, followlinks=followlinks):
        dirs[:] = [d for d in dirs if not is_path_hidden(d)]
        files[:] = [f for f in files if not is_path_hidden(f)]
        yield (root, dirs, files)


def write_if_different(filename, data):
    """Write `data` to `filename`, if the content of the file is different.

    Parameters
    ----------
    filename : str
        The file name to be written to.
    data : bytes
        The data to be written to `filename`.
    """
    assert isinstance(data, bytes)
    if os.path.exists(filename):
        with open(filename, 'rb') as (fd):
            original_data = fd.read()
    else:
        original_data = None
    if original_data != data:
        with open(filename, 'wb') as (fd):
            fd.write(data)


def import_file(filename):
    """
    Imports a module from a single file as if it doesn't belong to a
    particular package.
    """
    mode = 'U' if sys.version_info[0] < 3 else 'r'
    if name is None:
        basename = os.path.splitext(filename)[0]
        name = '_'.join(os.path.relpath(basename).split(os.sep)[1:])
    if import_machinery:
        loader = import_machinery.SourceFileLoader(name, filename)
        mod = loader.load_module()
    else:
        with open(filename, mode) as (fd):
            mod = imp.load_module(name, fd, filename, ('.py', mode, 1))
    return mod


if sys.version_info[0] >= 3:

    def iteritems(dictionary):
        return dictionary.items()


else:

    def iteritems(dictionary):
        return dictionary.iteritems()