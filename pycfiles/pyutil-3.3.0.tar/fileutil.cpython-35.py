# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/fileutil.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 8875 bytes
"""
Futz with files like a pro.
"""
import errno, os, stat, tempfile
try:
    import bsddb
except ImportError:
    DBNoSuchFileError = None
else:
    DBNoSuchFileError = bsddb.db.DBNoSuchFileError

def read_file(filename, mode='rb'):
    """ Read the contents of the file named filename and return it in
    a string. This function closes the file handle before it returns
    (even if the underlying Python implementation's garbage collector
    doesn't). """
    fh = open(filename, mode)
    try:
        return fh.read()
    finally:
        fh.close()


def write_file(filename, data, mode='wb'):
    """ Write the string data into a file named filename. This
    function closes the file handle (ensuring that the written data is
    flushed from the perspective of the Python implementation) before
    it returns (even if the underlying Python implementation's garbage
    collector doesn't)."""
    fh = open(filename, mode)
    try:
        fh.write(data)
    finally:
        fh.close()


def rename(src, dst, tries=4, basedelay=0.1):
    return os.rename(src, dst)


def remove(f, tries=4, basedelay=0.1):
    return os.remove(f)


def rmdir(f, tries=4, basedelay=0.1):
    return os.rmdir(f)


class _Dir(object):
    __doc__ = '\n    Hold a set of files and subdirs and clean them all up when asked to.\n    '

    def __init__(self, name, cleanup=True):
        self.name = name
        self.cleanup = cleanup
        self.files = []
        self.subdirs = set()

    def file(self, fname, mode=None):
        """
        Create a file in the tempdir and remember it so as to close() it
        before attempting to cleanup the temp dir.

        @rtype: file
        """
        ffn = os.path.join(self.name, fname)
        if mode is not None:
            fo = open(ffn, mode)
        else:
            fo = open(ffn)
        self.register_file(fo)
        return fo

    def subdir(self, dirname):
        """
        Create a subdirectory in the tempdir and remember it so as to call
        shutdown() on it before attempting to clean up.

        @rtype: _Dir instance
        """
        ffn = os.path.join(self.name, dirname)
        sd = _Dir(ffn, self.cleanup)
        self.register_subdir(sd)
        make_dirs(sd.name)
        return sd

    def register_file(self, fileobj):
        """
        Remember the file object and call close() on it before attempting to
        clean up.
        """
        self.files.append(fileobj)

    def register_subdir(self, dirobj):
        """
        Remember the _Dir object and call shutdown() on it before attempting
        to clean up.
        """
        self.subdirs.add(dirobj)

    def shutdown(self):
        if self.cleanup:
            for subdir in hasattr(self, 'subdirs') and self.subdirs or []:
                subdir.shutdown()

            for fileobj in hasattr(self, 'files') and self.files or []:
                if DBNoSuchFileError is None:
                    fileobj.close()
                else:
                    try:
                        fileobj.close()
                    except DBNoSuchFileError:
                        pass

            if hasattr(self, 'name'):
                rm_dir(self.name)

    def __repr__(self):
        return '<%s instance at %x %s>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return self.__repr__()

    def __del__(self):
        try:
            self.shutdown()
        except:
            import traceback
            traceback.print_exc()


class NamedTemporaryDirectory(_Dir):
    __doc__ = '\n    Call tempfile.mkdtemp(), store the name of the dir in self.name, and\n    rm_dir() when it gets garbage collected or "shutdown()".\n\n    Also keep track of file objects for files within the tempdir and call\n    close() on them before rm_dir().  This is a convenient way to open temp\n    files within the directory, and it is very helpful on Windows because you\n    can\'t delete a directory which contains a file which is currently open.\n    '

    def __init__(self, cleanup=True, *args, **kwargs):
        """ If cleanup, then the directory will be rmrf'ed when the object is shutdown. """
        name = tempfile.mkdtemp(*args, **kwargs)
        _Dir.__init__(self, name, cleanup)


class ReopenableNamedTemporaryFile:
    __doc__ = '\n    This uses tempfile.mkstemp() to generate a secure temp file.  It then closes\n    the file, leaving a zero-length file as a placeholder.  You can get the\n    filename with ReopenableNamedTemporaryFile.name.  When the\n    ReopenableNamedTemporaryFile instance is garbage collected or its shutdown()\n    method is called, it deletes the file.\n    '

    def __init__(self, *args, **kwargs):
        fd, self.name = tempfile.mkstemp(*args, **kwargs)
        os.close(fd)

    def __repr__(self):
        return '<%s instance at %x %s>' % (self.__class__.__name__, id(self), self.name)

    def __str__(self):
        return self.__repr__()

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        remove(self.name)


def make_dirs(dirname, mode=511):
    """
    An idempotent version of os.makedirs().  If the dir already exists, do
    nothing and return without raising an exception.  If this call creates the
    dir, return without raising an exception.  If there is an error that
    prevents creation or if the directory gets deleted after make_dirs() creates
    it and before make_dirs() checks that it exists, raise an exception.
    """
    tx = None
    try:
        os.makedirs(dirname, mode)
    except OSError as x:
        tx = x

    if not os.path.isdir(dirname):
        if tx:
            raise tx
        raise IOError('unknown error prevented creation of directory, or deleted the directory immediately after creation: %s' % dirname)


def rmtree(dirname):
    """
    A threadsafe and idempotent version of shutil.rmtree().  If the dir is
    already gone, do nothing and return without raising an exception.  If this
    call removes the dir, return without raising an exception.  If there is an
    error that prevents deletion or if the directory gets created again after
    rm_dir() deletes it and before rm_dir() checks that it is gone, raise an
    exception.
    """
    excs = []
    try:
        os.chmod(dirname, stat.S_IWRITE | stat.S_IEXEC | stat.S_IREAD)
        for f in os.listdir(dirname):
            fullname = os.path.join(dirname, f)
            if os.path.isdir(fullname):
                rm_dir(fullname)
            else:
                remove(fullname)

        os.rmdir(dirname)
    except EnvironmentError as le:
        if le.args[0] != 2 and le.args[0] != 3 or le.args[0] != errno.ENOENT:
            excs.append(le)
    except Exception as le:
        excs.append(le)

    if os.path.exists(dirname):
        if len(excs) == 1:
            raise excs[0]
        if len(excs) == 0:
            raise OSError('Failed to remove dir for unknown reason.')
        raise OSError(excs)


def rm_dir(dirname):
    return rmtree(dirname)


def remove_if_possible(f):
    try:
        remove(f)
    except EnvironmentError:
        pass


def remove_if_present(f):
    try:
        remove(f)
    except EnvironmentError as le:
        if le.args[0] != 2 and le.args[0] != 3 or le.args[0] != errno.ENOENT:
            raise


def rmdir_if_possible(f):
    try:
        rmdir(f)
    except EnvironmentError:
        pass


def open_or_create(fname, binarymode=True):
    try:
        f = open(fname, binarymode and 'r+b' or 'r+')
    except EnvironmentError:
        f = open(fname, binarymode and 'w+b' or 'w+')

    return f


def du(basedir):
    size = 0
    for root, dirs, files in os.walk(basedir):
        for f in files:
            fn = os.path.join(root, f)
            size += os.path.getsize(fn)

    return size