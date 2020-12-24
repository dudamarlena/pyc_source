# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/jinja2/jinja2/bccache.py
# Compiled at: 2019-07-30 18:47:04
# Size of source mod 2**32: 12794 bytes
"""
    jinja2.bccache
    ~~~~~~~~~~~~~~

    This module implements the bytecode cache system Jinja is optionally
    using.  This is useful if you have very complex template situations and
    the compiliation of all those templates slow down your application too
    much.

    Situations where this is useful are often forking web applications that
    are initialized on the first request.

    :copyright: (c) 2017 by the Jinja Team.
    :license: BSD.
"""
from os import path, listdir
import os, sys, stat, errno, marshal, tempfile, fnmatch
from hashlib import sha1
from jinja2.utils import open_if_exists
from jinja2._compat import BytesIO, pickle, PY2, text_type
if not PY2:
    marshal_dump = marshal.dump
    marshal_load = marshal.load
else:

    def marshal_dump(code, f):
        if isinstance(f, file):
            marshal.dump(code, f)
        else:
            f.write(marshal.dumps(code))


    def marshal_load(f):
        if isinstance(f, file):
            return marshal.load(f)
        else:
            return marshal.loads(f.read())


bc_version = 3
bc_magic = 'j2'.encode('ascii') + pickle.dumps(bc_version, 2) + pickle.dumps(sys.version_info[0] << 24 | sys.version_info[1])

class Bucket(object):
    __doc__ = "Buckets are used to store the bytecode for one template.  It's created\n    and initialized by the bytecode cache and passed to the loading functions.\n\n    The buckets get an internal checksum from the cache assigned and use this\n    to automatically reject outdated cache material.  Individual bytecode\n    cache subclasses don't have to care about cache invalidation.\n    "

    def __init__(self, environment, key, checksum):
        self.environment = environment
        self.key = key
        self.checksum = checksum
        self.reset()

    def reset(self):
        """Resets the bucket (unloads the bytecode)."""
        self.code = None

    def load_bytecode(self, f):
        """Loads bytecode from a file or file like object."""
        magic = f.read(len(bc_magic))
        if magic != bc_magic:
            self.reset()
            return
        checksum = pickle.load(f)
        if self.checksum != checksum:
            self.reset()
            return
        try:
            self.code = marshal_load(f)
        except (EOFError, ValueError, TypeError):
            self.reset()
            return

    def write_bytecode(self, f):
        """Dump the bytecode into the file or file like object passed."""
        if self.code is None:
            raise TypeError("can't write empty bucket")
        f.write(bc_magic)
        pickle.dump(self.checksum, f, 2)
        marshal_dump(self.code, f)

    def bytecode_from_string(self, string):
        """Load bytecode from a string."""
        self.load_bytecode(BytesIO(string))

    def bytecode_to_string(self):
        """Return the bytecode as string."""
        out = BytesIO()
        self.write_bytecode(out)
        return out.getvalue()


class BytecodeCache(object):
    __doc__ = "To implement your own bytecode cache you have to subclass this class\n    and override :meth:`load_bytecode` and :meth:`dump_bytecode`.  Both of\n    these methods are passed a :class:`~jinja2.bccache.Bucket`.\n\n    A very basic bytecode cache that saves the bytecode on the file system::\n\n        from os import path\n\n        class MyCache(BytecodeCache):\n\n            def __init__(self, directory):\n                self.directory = directory\n\n            def load_bytecode(self, bucket):\n                filename = path.join(self.directory, bucket.key)\n                if path.exists(filename):\n                    with open(filename, 'rb') as f:\n                        bucket.load_bytecode(f)\n\n            def dump_bytecode(self, bucket):\n                filename = path.join(self.directory, bucket.key)\n                with open(filename, 'wb') as f:\n                    bucket.write_bytecode(f)\n\n    A more advanced version of a filesystem based bytecode cache is part of\n    Jinja2.\n    "

    def load_bytecode(self, bucket):
        """Subclasses have to override this method to load bytecode into a
        bucket.  If they are not able to find code in the cache for the
        bucket, it must not do anything.
        """
        raise NotImplementedError()

    def dump_bytecode(self, bucket):
        """Subclasses have to override this method to write the bytecode
        from a bucket back to the cache.  If it unable to do so it must not
        fail silently but raise an exception.
        """
        raise NotImplementedError()

    def clear(self):
        """Clears the cache.  This method is not used by Jinja2 but should be
        implemented to allow applications to clear the bytecode cache used
        by a particular environment.
        """
        pass

    def get_cache_key(self, name, filename=None):
        """Returns the unique hash key for this template name."""
        hash = sha1(name.encode('utf-8'))
        if filename is not None:
            filename = '|' + filename
            if isinstance(filename, text_type):
                filename = filename.encode('utf-8')
            hash.update(filename)
        return hash.hexdigest()

    def get_source_checksum(self, source):
        """Returns a checksum for the source."""
        return sha1(source.encode('utf-8')).hexdigest()

    def get_bucket(self, environment, name, filename, source):
        """Return a cache bucket for the given template.  All arguments are
        mandatory but filename may be `None`.
        """
        key = self.get_cache_key(name, filename)
        checksum = self.get_source_checksum(source)
        bucket = Bucket(environment, key, checksum)
        self.load_bytecode(bucket)
        return bucket

    def set_bucket(self, bucket):
        """Put the bucket into the cache."""
        self.dump_bytecode(bucket)


class FileSystemBytecodeCache(BytecodeCache):
    __doc__ = "A bytecode cache that stores bytecode on the filesystem.  It accepts\n    two arguments: The directory where the cache items are stored and a\n    pattern string that is used to build the filename.\n\n    If no directory is specified a default cache directory is selected.  On\n    Windows the user's temp directory is used, on UNIX systems a directory\n    is created for the user in the system temp directory.\n\n    The pattern can be used to have multiple separate caches operate on the\n    same directory.  The default pattern is ``'__jinja2_%s.cache'``.  ``%s``\n    is replaced with the cache key.\n\n    >>> bcc = FileSystemBytecodeCache('/tmp/jinja_cache', '%s.cache')\n\n    This bytecode cache supports clearing of the cache using the clear method.\n    "

    def __init__(self, directory=None, pattern='__jinja2_%s.cache'):
        if directory is None:
            directory = self._get_default_cache_dir()
        self.directory = directory
        self.pattern = pattern

    def _get_default_cache_dir(self):

        def _unsafe_dir():
            raise RuntimeError('Cannot determine safe temp directory.  You need to explicitly provide one.')

        tmpdir = tempfile.gettempdir()
        if os.name == 'nt':
            return tmpdir
        else:
            if not hasattr(os, 'getuid'):
                _unsafe_dir()
            dirname = '_jinja2-cache-%d' % os.getuid()
            actual_dir = os.path.join(tmpdir, dirname)
            try:
                os.mkdir(actual_dir, stat.S_IRWXU)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            try:
                os.chmod(actual_dir, stat.S_IRWXU)
                actual_dir_stat = os.lstat(actual_dir)
                if actual_dir_stat.st_uid != os.getuid() or not stat.S_ISDIR(actual_dir_stat.st_mode) or stat.S_IMODE(actual_dir_stat.st_mode) != stat.S_IRWXU:
                    _unsafe_dir()
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            actual_dir_stat = os.lstat(actual_dir)
            if actual_dir_stat.st_uid != os.getuid() or not stat.S_ISDIR(actual_dir_stat.st_mode) or stat.S_IMODE(actual_dir_stat.st_mode) != stat.S_IRWXU:
                _unsafe_dir()
            return actual_dir

    def _get_cache_filename(self, bucket):
        return path.join(self.directory, self.pattern % bucket.key)

    def load_bytecode(self, bucket):
        f = open_if_exists(self._get_cache_filename(bucket), 'rb')
        if f is not None:
            try:
                bucket.load_bytecode(f)
            finally:
                f.close()

    def dump_bytecode(self, bucket):
        f = open(self._get_cache_filename(bucket), 'wb')
        try:
            bucket.write_bytecode(f)
        finally:
            f.close()

    def clear(self):
        from os import remove
        files = fnmatch.filter(listdir(self.directory), self.pattern % '*')
        for filename in files:
            try:
                remove(path.join(self.directory, filename))
            except OSError:
                pass


class MemcachedBytecodeCache(BytecodeCache):
    __doc__ = "This class implements a bytecode cache that uses a memcache cache for\n    storing the information.  It does not enforce a specific memcache library\n    (tummy's memcache or cmemcache) but will accept any class that provides\n    the minimal interface required.\n\n    Libraries compatible with this class:\n\n    -   `werkzeug <http://werkzeug.pocoo.org/>`_.contrib.cache\n    -   `python-memcached <https://www.tummy.com/Community/software/python-memcached/>`_\n    -   `cmemcache <http://gijsbert.org/cmemcache/>`_\n\n    (Unfortunately the django cache interface is not compatible because it\n    does not support storing binary data, only unicode.  You can however pass\n    the underlying cache client to the bytecode cache which is available\n    as `django.core.cache.cache._client`.)\n\n    The minimal interface for the client passed to the constructor is this:\n\n    .. class:: MinimalClientInterface\n\n        .. method:: set(key, value[, timeout])\n\n            Stores the bytecode in the cache.  `value` is a string and\n            `timeout` the timeout of the key.  If timeout is not provided\n            a default timeout or no timeout should be assumed, if it's\n            provided it's an integer with the number of seconds the cache\n            item should exist.\n\n        .. method:: get(key)\n\n            Returns the value for the cache key.  If the item does not\n            exist in the cache the return value must be `None`.\n\n    The other arguments to the constructor are the prefix for all keys that\n    is added before the actual cache key and the timeout for the bytecode in\n    the cache system.  We recommend a high (or no) timeout.\n\n    This bytecode cache does not support clearing of used items in the cache.\n    The clear method is a no-operation function.\n\n    .. versionadded:: 2.7\n       Added support for ignoring memcache errors through the\n       `ignore_memcache_errors` parameter.\n    "

    def __init__(self, client, prefix='jinja2/bytecode/', timeout=None, ignore_memcache_errors=True):
        self.client = client
        self.prefix = prefix
        self.timeout = timeout
        self.ignore_memcache_errors = ignore_memcache_errors

    def load_bytecode(self, bucket):
        try:
            code = self.client.get(self.prefix + bucket.key)
        except Exception:
            if not self.ignore_memcache_errors:
                raise
            code = None

        if code is not None:
            bucket.bytecode_from_string(code)

    def dump_bytecode(self, bucket):
        args = (self.prefix + bucket.key, bucket.bytecode_to_string())
        if self.timeout is not None:
            args += (self.timeout,)
        try:
            (self.client.set)(*args)
        except Exception:
            if not self.ignore_memcache_errors:
                raise