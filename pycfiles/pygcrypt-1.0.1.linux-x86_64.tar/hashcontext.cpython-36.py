# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/hashcontext.py
# Compiled at: 2016-10-30 11:29:24
# Size of source mod 2**32: 6983 bytes
from ctypes.util import find_library
from ._gcrypt import ffi
from . import errors
lib = ffi.dlopen(find_library('gcrypt'))

class HashContext(object):
    __doc__ = '\n    This class implement and works with a context object used to manage a\n    hashing operation.\n    '

    def __init__(self, *args, **kwargs):
        """
        Create a message digest object for algorithm algo. flags may be given as an
        bitwise OR of constants described below. algo may be given as 0 if the
        algorithms to use are later set using gcry_md_enable. hd is guaranteed to
        either receive a valid handle or NULL.
        """
        if len(args) == 1:
            if not (isinstance(args[0], str) or isinstance(args[0], bytes)):
                if ffi.typeof(args[0]) == ffi.typeof('gcry_md_hd_t *'):
                    self.ctx = args[0][0]
                    return
            else:
                secure = kwargs.get('secure', True)
                hmac = kwargs.get('hmac', False)
                if secure:
                    flags = lib.GCRY_MD_FLAG_SECURE
                else:
                    flags = 0
            if hmac:
                flags ^= lib.GCRY_MD_FLAG_HMAC
        else:
            self.hmac = hmac
            algo = kwargs['algo']
            if isinstance(algo, str):
                algo = algo.encode()
            context = ffi.new('gcry_md_hd_t *')
            error = ffi.cast('gcry_error_t', 0)
            error = lib.gcry_md_open(context, self.isvalid(algo), ffi.cast('unsigned int', flags))
            if error > 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        self.ctx = context[0]

    def __delete__(self):
        """
        Release all resources of hash context h. h should not be used after a call
        to this function. A NULL passed as h is ignored. The function also zeroises
        all sensitive information associated with this handle.
        """
        lib.gcry_md_close(self.ctx)

    def isvalid(self, algo):
        """
        Test if a given algorithm exists and is available and return its int
        """
        if isinstance(algo, str):
            algo = algo.encode()
        else:
            algo_int = lib.gcry_md_map_name(algo)
            if algo_int == 0:
                raise Exception('Algorithm name {} is unknown.'.format(algo.decode()))
            error = ffi.cast('gcry_error_t', 0)
            error = lib.gcry_md_algo_info(algo_int, lib.GCRYCTL_TEST_ALGO, ffi.NULL, ffi.NULL)
            if error != 0:
                raise Exception('Algorithm {} is unavailable.'.format(algo.decode()))
        return algo_int

    def reset(self):
        """
        Reset the current context to its initial state. This is effectively
        identical to a close followed by an open and enabling all currently active
        algorithms.
        """
        lib.gcry_md_reset(self.ctx)

    def enable(self, algo):
        """
        Add the message digest algorithm algo to the digest object described by
        handle h. Duplicated enabling of algorithms is detected and ignored. 
        """
        error = ffi.cast('gcry_error_t', 0)
        error = lib.gcry_md_enable(self.ctx, self.isvalid(algo))
        if error > 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)

    def setkey(self, key):
        """
        For use with the HMAC feature, set the MAC key to the value of key of length
        keylen bytes. There is no restriction on the length of the key. 
        """
        if not self.hmac:
            raise TypeError('This hash context has not been initialised as a HMAC one.')
        else:
            if isinstance(key, str):
                key = key.encode()
            key_buffer = ffi.new('char []', key)
            error = ffi.cast('gcry_error_t', 0)
            error = lib.gcry_md_setkey(self.ctx, key_buffer, len(key))
            if error > 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)

    def copy(self):
        """
        Create a new digest object as an exact copy of the object described by
        handle handle_src and store it in handle_dst. The context is not reset and
        you can continue to hash data using this context and independently using
        the original context.
        """
        dst_ctx = ffi.new('gcry_md_hd_t *')
        error = ffi.cast('gcry_error_t', 0)
        error = lib.gcry_md_copy(dst_ctx, self.ctx)
        copied = HashContext(dst_ctx)
        copied.hmac = self.hmac
        return copied

    def write(self, data):
        """
        Pass length bytes of the data in buffer to the digest object with handle h
        to update the digest values. This function should be used for large blocks
        of data. 
        """
        if isinstance(data, str):
            data = data.encode()
        buffer = ffi.new('char []', data)
        lib.gcry_md_write(self.ctx, buffer, len(data))

    def read(self, algo=0):
        """
        gcry_md_read returns the message digest after finalizing the calculation.
        This function may be used as often as required but it will always return the
        same value for one handle. The returned message digest is allocated within
        the message context and therefore valid until the handle is released or
        reseted (using gcry_md_close or gcry_md_reset. algo may be given as 0 to
        return the only enabled message digest or it may specify one of the enabled
        algorithms. The function does return NULL if the requested algorithm has not
        been enabled.
        """
        if not algo == 0:
            algo = self.isvalid(algo)
            dlen = lib.gcry_md_get_algo_dlen(algo)
        else:
            dlen = lib.gcry_md_get_algo_dlen(lib.gcry_md_get_algo(self.ctx))
        return ffi.buffer(lib.gcry_md_read(self.ctx, algo), dlen)[:]

    def __getattr__(self, attr):
        """
        Let's get some specific attributes 
        """
        if attr == 'algo':
            return ffi.string(lib.gcry_md_algo_name(lib.gcry_md_get_algo(self.ctx)))
        else:
            if attr == 'hashlen':
                return int(ffi.cast('int', lib.gcry_md_get_algo_dlen(lib.gcry_md_get_algo(self.ctx))))
            if attr == 'secure':
                valid = lib.gcry_md_is_secure(self.ctx)
                if valid == 0:
                    return False
                else:
                    return True