# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/ecurve.py
# Compiled at: 2017-03-12 11:23:15
# Size of source mod 2**32: 5568 bytes
from ctypes.util import find_library
from ._gcrypt import ffi
from . import errors
from .gctypes.sexpression import SExpression
from .gctypes.ec_point import Point
from .gctypes.mpi import MPIint
from .gctypes.key import Key
lib = ffi.dlopen(find_library('gcrypt'))

class ECurve(object):
    __doc__ = '\n    This object describes an elliptic curve. It provides methods to access points\n    and mpi associated to it.\n\n    It provides dictionnary like method to access to its member.\n    '

    def __init__(self, keyparam=None, curve=None):
        """
        Let's create the context needed for the Elliptic curve calculation.
        It needs a keyparam formed like an ecc_keyparam S-Expression as a
        parameters and an optional curve-name to fill in the blank of the
        parameter.
        """
        if keyparam is not None:
            if not isinstance(keyparam, SExpression):
                raise TypeError('keyparam must be a SExpression. Got {} instead.'.format(type(keyparam)))
            if keyparam is None:
                if curve is None:
                    raise TypeError('at least one of keyparam and curve must be passed to __init__')
            ec_curve = ffi.new('gcry_ctx_t *', ffi.NULL)
            error = ffi.cast('gpg_error_t', 0)
            if keyparam is None:
                keyparam_t = ffi.NULL
            else:
                keyparam_t = keyparam.sexp
        else:
            if curve == None:
                curve = ''
            error = lib.gcry_mpi_ec_new(ec_curve, keyparam_t, curve.encode())
            if error != 0:
                raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)
        self.curve = ec_curve[0]
        self.name = curve

    def __del__(self):
        """
        We need to release the the context associated to ourself.
        """
        lib.gcry_ctx_release(self.curve)

    def __setitem__(self, key, item):
        """
        We want to add either a Point or a MPI to our elliptic curve
        context.
        """
        error = ffi.cast('gcry_error_t', 0)
        if isinstance(item, Point):
            error = lib.gcry_mpi_ec_set_point(key.encode(), item.point, self.curve)
        else:
            if isinstance(item, MPIint):
                error = lib.gcry_mpi_ec_set_mpi(key.encode(), item.mpi, self.curve)
            else:
                raise TypeError('Item must be Point or MPI. Got {} instead.'.format(type(item)))
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)

    def __getitem__(self, key):
        """
        Let's retrieve an item from the Elliptic Curve. Item to be retrieved can only be
        in keys defined by the ecc-private key params.

        p, a, b, n and d are mpi
        g and q are points.
        """
        if key in ('p', 'a', 'b', 'n', 'd'):
            mpi = MPIint()
            pointer = lib.gcry_mpi_ec_get_mpi(key.encode(), self.curve, 1)
            if pointer == ffi.NULL:
                return
            else:
                mpi.mpi = pointer
                return mpi
        if key in ('q', 'g'):
            point = Point(self.curve)
            pointer = lib.gcry_mpi_ec_get_point(key.encode(), self.curve, 1)
            if pointer == ffi.NULL:
                return
            else:
                point.point = pointer
                return point
        raise KeyError

    def __repr__(self):
        """
        We want to print the current EC. For that we will create the S-Expression
        corresponding to the current state of the curve, and returns it in a tuple with the
        name of the curve.
        """
        return '(keyparam \n    (ecc \n        (p {})\n        (a {})\n        (b {})\n        (n {})\n        (d {})\n        (q {})\n        (g {})\n    )\n)'.format(self['p'], self['a'], self['b'], self['n'], self['d'], self['q'], self['g'])

    def key(self, mode=0):
        """
        Return an S-expression representing the context curve. Depending on the
        state of that context, the S-expression may either be a public key, a
        private key or any other object used with public key operations. On
        success 0 is returned and a new S-expression is stored at r_sexp; on
        error an error code is returned and NULL is stored at r_sexp. mode must be
        one of:
            0
                Decide what to return depending on the context. For example if the
                private key parameter is available a private key is returned, if
                not a public key is returned.
            GCRY_PK_GET_PUBKEY
                Return the public key even if the context has the private key
                parameter.
            GCRY_PK_GET_SECKEY
                Return the private key or the error GPG_ERR_NO_SECKEY if it is not
                possible.

        As of now this function supports only certain ECC operations because a
        context object is right now only defined for ECC. Over time this function
        will be extended to cover more algorithms.
        """
        if mode == 'PUBKEY':
            mode = 1
        else:
            if mode == 'SECKEY':
                mode = 2
        error = ffi.cast('gcry_error_t', 0)
        r_sexp = ffi.new('gcry_sexp_t *')
        error = lib.gcry_pubkey_get_sexp(r_sexp, mode, self.curve)
        if error > 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)), error)
        return Key(SExpression(r_sexp))