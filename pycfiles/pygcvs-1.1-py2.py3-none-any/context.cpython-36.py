# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/context.py
# Compiled at: 2017-04-16 10:14:29
# Size of source mod 2**32: 6719 bytes
from ctypes.util import find_library
from ._gcrypt import ffi
from . import errors
from . import ciphers
from .gctypes import mpi, sexpression, key
lib = ffi.dlopen(find_library('gcrypt'))

class Context(object):
    """Context"""

    def __init__(self, secmem=True, hw_disabled=[]):
        """
        We want to initialise our application.

        secmem is a boolean used to activate the use of secmem. Default to True
        hw_disabled is a list of hardware feature we want to explictly disable for any reason.
              /* Version check should be the very first call because it
                 makes sure that important subsystems are initialized. */
              if (!gcry_check_version (GCRYPT_VERSION))
                {
                  fputs ("libgcrypt version mismatch
", stderr);
                  exit (2);
                }

              /* We don't want to see any warnings, e.g. because we have not yet
                 parsed program options which might be used to suppress such
                 warnings. */
              gcry_control (GCRYCTL_SUSPEND_SECMEM_WARN);

              /* ... If required, other initialization goes here.  Note that the
                 process might still be running with increased privileges and that
                 the secure memory has not been initialized.  */

              /* Allocate a pool of 16k secure memory.  This make the secure memory
                 available and also drops privileges where needed.  */
              gcry_control (GCRYCTL_INIT_SECMEM, 16384, 0);

              /* It is now okay to let Libgcrypt complain when there was/is
                 a problem with the secure memory. */
              gcry_control (GCRYCTL_RESUME_SECMEM_WARN);

              /* ... If required, other initialization goes here.  */

              /* Tell Libgcrypt that initialization has completed. */
              gcry_control (GCRYCTL_INITIALIZATION_FINISHED, 0);
        """
        error = ffi.cast('gcry_error_t', 0)
        for hw_feature in hw_disabled:
            error = lib.gcry_control(lib.GCRYCTL_DISABLE_HWF, ffi.new('const char []', hw_feature.encode()), ffi.NULL)
            if error != 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)

        version = lib.gcry_check_version(ffi.new('const char []', '1.6.3'))
        if version == ffi.NULL:
            raise Exception('Cannot initialize gcrypt')
        error = lib.gcry_control(lib.GCRYCTL_INITIALIZATION_FINISHED_P)
        if error == 0:
            if secmem:
                error = lib.gcry_control(lib.GCRYCTL_SUSPEND_SECMEM_WARN)
                if error != 0:
                    raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)
                error = lib.gcry_control(lib.GCRYCTL_INIT_SECMEM, ffi.cast('int', 65536), ffi.cast('int', 0))
                if error != 0:
                    raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)
                error = lib.gcry_control(lib.GCRYCTL_RESUME_SECMEM_WARN)
                self.secmem = True
                if error != 0:
                    raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)
            else:
                self.secmem = False
            error = lib.gcry_control(lib.GCRYCTL_INITIALIZATION_FINISHED, ffi.cast('int', 0))
            if error != 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)

    @property
    def version(self):
        return ffi.string(lib.gcry_check_version(ffi.NULL)).decode()

    @property
    def algo(self):
        if self.cipher:
            return self.cipher.algo
        raise KeyError('No ciphers initialized.')

    @property
    def mode(self):
        if self.cipher:
            return self.cipher.mode
        raise KeyError('No ciphers initailized.')

    @property
    def key(self):
        return getattr(self.cipher, 'key', None)

    @key.setter
    def key(self, value):
        if self.cipher:
            self.cipher.key = value

    @property
    def iv(self):
        return getattr(self.cipher, 'iv', None)

    @iv.setter
    def iv(self, value):
        if self.cipher:
            self.cipher.iv = value

    @property
    def ctr(self):
        return getattr(self.cipher, 'ctr', None)

    @ctr.setter
    def ctr(self, value):
        if self.cipher:
            self.cipher.ctr = value

    @property
    def cipher(self):
        return self._cipher

    @cipher.setter
    def cipher(self, value):
        if not isinstance(value, ciphers.Cipher):
            raise KeyError('{} must be an instance of ciphers.Cipher, {} given.'.format(item, type(value)))
        self._cipher = value

    def mpi(self, obj):
        """
        This will generates a mpi and attributes it a class depending on the type of obj.
        """
        if isinstance(obj, int):
            return mpi.MPIint(obj)
        else:
            return mpi.MPIopaque(obj)