# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/constant2-project/constant2/pkg/superjson/pkg/atomicwrites.py
# Compiled at: 2018-12-19 11:16:54
import contextlib, io, os, sys, tempfile
try:
    import fcntl
except ImportError:
    fcntl = None

__version__ = '1.2.0'
PY2 = sys.version_info[0] == 2
text_type = unicode if PY2 else str

def _path_to_unicode(x):
    if not isinstance(x, text_type):
        return x.decode(sys.getfilesystemencoding())
    return x


DEFAULT_MODE = 'wb' if PY2 else 'w'
_proper_fsync = os.fsync
if sys.platform != 'win32':
    if hasattr(fcntl, 'F_FULLFSYNC'):

        def _proper_fsync(fd):
            fcntl.fcntl(fd, fcntl.F_FULLFSYNC)


    def _sync_directory(directory):
        fd = os.open(directory, 0)
        try:
            _proper_fsync(fd)
        finally:
            os.close(fd)


    def _replace_atomic(src, dst):
        os.rename(src, dst)
        _sync_directory(os.path.normpath(os.path.dirname(dst)))


    def _move_atomic(src, dst):
        os.link(src, dst)
        os.unlink(src)
        src_dir = os.path.normpath(os.path.dirname(src))
        dst_dir = os.path.normpath(os.path.dirname(dst))
        _sync_directory(dst_dir)
        if src_dir != dst_dir:
            _sync_directory(src_dir)


else:
    from ctypes import windll, WinError
    _MOVEFILE_REPLACE_EXISTING = 1
    _MOVEFILE_WRITE_THROUGH = 8
    _windows_default_flags = _MOVEFILE_WRITE_THROUGH

    def _handle_errors(rv):
        if not rv:
            raise WinError()


    def _replace_atomic(src, dst):
        _handle_errors(windll.kernel32.MoveFileExW(_path_to_unicode(src), _path_to_unicode(dst), _windows_default_flags | _MOVEFILE_REPLACE_EXISTING))


    def _move_atomic(src, dst):
        _handle_errors(windll.kernel32.MoveFileExW(_path_to_unicode(src), _path_to_unicode(dst), _windows_default_flags))


def replace_atomic(src, dst):
    """
    Move ``src`` to ``dst``. If ``dst`` exists, it will be silently
    overwritten.

    Both paths must reside on the same filesystem for the operation to be
    atomic.
    """
    return _replace_atomic(src, dst)


def move_atomic(src, dst):
    """
    Move ``src`` to ``dst``. There might a timewindow where both filesystem
    entries exist. If ``dst`` already exists, :py:exc:`FileExistsError` will be
    raised.

    Both paths must reside on the same filesystem for the operation to be
    atomic.
    """
    return _move_atomic(src, dst)


class AtomicWriter(object):
    """
    A helper class for performing atomic writes. Usage::

        with AtomicWriter(path).open() as f:
            f.write(...)

    :param path: The destination filepath. May or may not exist.
    :param mode: The filemode for the temporary file. This defaults to `wb` in
        Python 2 and `w` in Python 3.
    :param overwrite: If set to false, an error is raised if ``path`` exists.
        Errors are only raised after the file has been written to.  Either way,
        the operation is atomic.

    If you need further control over the exact behavior, you are encouraged to
    subclass.
    """

    def __init__(self, path, mode=DEFAULT_MODE, overwrite=False, **open_kwargs):
        if 'a' in mode:
            raise ValueError("Appending to an existing file is not supported, because that would involve an expensive `copy`-operation to a temporary file. Open the file in normal `w`-mode and copy explicitly if that's what you're after.")
        if 'x' in mode:
            raise ValueError('Use the `overwrite`-parameter instead.')
        if 'w' not in mode:
            raise ValueError('AtomicWriters can only be written to.')
        self._path = path
        self._mode = mode
        self._overwrite = overwrite
        self._open_kwargs = open_kwargs

    def open(self):
        """
        Open the temporary file.
        """
        return self._open(self.get_fileobject)

    @contextlib.contextmanager
    def _open(self, get_fileobject):
        f = None
        try:
            success = False
            with get_fileobject(**self._open_kwargs) as (f):
                yield f
                self.sync(f)
            self.commit(f)
            success = True
        finally:
            if not success:
                try:
                    self.rollback(f)
                except Exception:
                    pass

        return

    def get_fileobject(self, dir=None, **kwargs):
        """Return the temporary file to use."""
        if dir is None:
            dir = os.path.normpath(os.path.dirname(self._path))
        descriptor, name = tempfile.mkstemp(dir=dir)
        os.close(descriptor)
        kwargs['mode'] = self._mode
        kwargs['file'] = name
        return io.open(**kwargs)

    def sync(self, f):
        """responsible for clearing as many file caches as possible before
        commit"""
        f.flush()
        _proper_fsync(f.fileno())

    def commit(self, f):
        """Move the temporary file to the target location."""
        if self._overwrite:
            replace_atomic(f.name, self._path)
        else:
            move_atomic(f.name, self._path)

    def rollback(self, f):
        """Clean up all temporary resources."""
        os.unlink(f.name)


def atomic_write(path, writer_cls=AtomicWriter, **cls_kwargs):
    """
    Simple atomic writes. This wraps :py:class:`AtomicWriter`::

        with atomic_write(path) as f:
            f.write(...)

    :param path: The target path to write to.
    :param writer_cls: The writer class to use. This parameter is useful if you
        subclassed :py:class:`AtomicWriter` to change some behavior and want to
        use that new subclass.

    Additional keyword arguments are passed to the writer class. See
    :py:class:`AtomicWriter`.
    """
    return writer_cls(path, **cls_kwargs).open()