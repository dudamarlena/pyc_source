# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/hmaccontext.py
# Compiled at: 2017-04-16 10:12:20
# Size of source mod 2**32: 7003 bytes
from ctypes.util import find_library
from ._gcrypt import ffi
from . import errors
lib = ffi.dlopen(find_library('gcrypt'))

class HMACContext(object):
    """HMACContext"""

    def __init__(self, *args, **kwargs):
        """
        Create a MAC object for algorithm algo. flags may be given as an bitwise
        OR of constants described below. hd is guaranteed to either receive a valid
        handle or NULL. ctx is context object to associate MAC object with. ctx
        maybe set to NULL.
        """
        if len(args) == 1:
            if ffi.typeof(args[0]) != ffi.typeof('gcry_mac_hd_t'):
                raise TypeError('With only one arg, it should be a <gcry_mac_hd_t>, got {} instead'.format(type(args[0])))
            self.ctx = args[0]
            return
        else:
            self.algo = self.isvalid(kwargs['algo'])
            self.secure = kwargs.get('secure', True)
            if self.secure:
                flags = lib.GCRY_MAC_FLAG_SECURE
            else:
                flags = 0
            if self.secure:
                ctx_handle = ffi.new_allocator(alloc=(lib.gcry_malloc_secure), free=(lib.gcry_free))('gcry_mac_hd_t *')
            else:
                ctx_handle = ffi.new('gcry_mac_hd_t *')
        error = ffi.cast('gcry_error_t', 0)
        error = lib.gcry_mac_open(ctx_handle, self.algo, flags, ffi.NULL)
        if error > 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        self.ctx = ctx_handle[0]

    def __delete__(self):
        """
        Release all resources of MAC context h. h should not be used after a
        call to this function. A NULL passed as h is ignored. The function also
        clears all sensitive information associated with this handle.
        """
        lib.gcry_mac_close(self.get())

    def isvalid(self, algo):
        """
        We need to check if an algorithm is valid, and converts it to an int.
        """
        if isinstance(algo, str):
            algo = algo.encode()
        else:
            algo_int = lib.gcry_mac_map_name(algo)
            if algo_int == 0:
                raise Exception('Algorithm {} does not exist.'.format(algo.decode()))
            valid = lib.gcry_mac_algo_info(algo_int, lib.GCRYCTL_TEST_ALGO, ffi.NULL, ffi.NULL)
            if valid != 0:
                raise Exception('Algorithm {} is not available for use.'.format(algo.decode()))
        return algo_int

    def reset(self):
        """
        Reset the current context to its initial state. This is effectively
        identical to a close followed by an open and setting same key.
        """
        error = ffi.cast('gcry_error_t', 0)
        error = lib.gcry_mac_ctl(self.ctx, lib.GCRYCTL_RESET, ffi.NULL, 0)
        if error > 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)

    def write(self, data):
        """
        Pass length bytes of the data in buffer to the MAC object with handle
        h to update the MAC values.
        """
        if isinstance(data, str):
            data = data.encode()
        else:
            if not isinstance(data, bytes):
                raise TypeError('data must be of str or byte stype. got {} instead'.format(type(data)))
            buffer = ffi.new('char []', data)
            error = ffi.cast('gcry_error_t', 0)
            error = lib.gcry_mac_write(self.ctx, buffer, len(data))
            if error > 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)

    def read(self):
        """
        gcry_mac_read returns the MAC after finalizing the calculation. Function
        copies the resulting MAC value to buffer of the length length. If length
        is larger than length of resulting MAC value, then length of MAC is
        returned through length.
        """
        buffer = ffi.new('char [{}]'.format(self.maclen))
        error = ffi.cast('gcry_error_t', 0)
        length = ffi.new('size_t *')
        length[0] = self.maclen
        error = lib.gcry_mac_read(self.ctx, buffer, length)
        if error > 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        return ffi.string(buffer)

    def verify(self, data):
        """
        gcry_mac_verify finalizes MAC calculation and compares result with
        length bytes of data in buffer. Error code GPG_ERR_CHECKSUM is returned
        if the MAC value in the buffer buffer does not match the MAC calculated
        in object h. 
        """
        if isinstance(data, str):
            data = data.encode()
        else:
            if not isinstance(data, bytes):
                raise TypeError('data must be of type str or bytes, got {} instead.'.format(type(data)))
            buffer = ffi.new('char[{}]'.format(self.maclen), data)
            error = ffi.cast('gcry_error_t', 0)
            error = lib.gcry_mac_verify(self.ctx, buffer, self.maclen)
            if error > 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        return True

    def __getattr__(self, attr):
        if attr == 'maclen':
            return int(lib.gcry_mac_get_algo_maclen(self.isvalid(ffi.string(lib.gcry_mac_algo_name(self.algo)))))
        if attr == 'keylen':
            return int(lib.gcry_mac_get_algo_keylen(self.isvalid(ffi.string(lib.gcry_mac_algo_name(self.algo)))))

    def __setattr__(self, attr, value):
        if attr == 'key':
            if isinstance(value, str):
                value = value.encode()
        elif not isinstance(value, bytes):
            raise AttributeError('{} should be of type str or bytes, got {} instead'.format(attr, type(value)))
        else:
            key_buffer = ffi.new('char []', value)
            error = ffi.cast('gcry_error_t', 0)
            error = lib.gcry_mac_setkey(self.ctx, value, len(value))
            if error > 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
            if attr == 'iv':
                if isinstance(value, str):
                    value = value.encode()
                if not isinstance(value, bytes):
                    raise AttributeError('{} should be of type str or bytes, got {} instead'.format(attr, type(value)))
                iv_buffer = ffi.new('char []', value)
                error = ffi.cast('gcry_error_t', 0)
                error = lib.gcry_mac_setiv(self.ctx, value, len(value))
                if error > 0:
                    raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
            else:
                super(HMACContext, self).__setattr__(attr, value)