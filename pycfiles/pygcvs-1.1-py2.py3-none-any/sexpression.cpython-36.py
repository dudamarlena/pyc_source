# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/gctypes/sexpression.py
# Compiled at: 2017-04-09 08:14:05
# Size of source mod 2**32: 17007 bytes
import re
from collections.abc import MutableMapping
from ctypes.util import find_library
from .._gcrypt import ffi
from .. import errors
from .mpi import MPIint, MPIopaque, MPI
lib = ffi.dlopen(find_library('gcrypt'))

class SExpression(object):
    """SExpression"""

    def __init__(self, *args, **kwargs):
        """
        Let's build a new S-Expression. We're going to use sscan to allow
        for detection of parsing errors.

        kwargs might contains various st of args, used to determine which
        function will be called to build the s-expr
        """
        error = ffi.cast('gcry_error_t', 0)
        erroffset = 0
        sexp = ffi.new('gcry_sexp_t *')
        self.fmt = 'DEFAULT'
        if len(args) == 0:
            raise TypeError('SExpression must be created with at least 1 parameters, none given')
        elif len(args) == 1 and isinstance(args[0], bytes):
            error = lib.gcry_sexp_sscan(sexp, ffi.cast('size_t *', erroffset), args[0], ffi.cast('size_t', len(args[0])))
        else:
            if len(args) == 1:
                if ffi.typeof(args[0]) is ffi.typeof('gcry_sexp_t *') or ffi.typeof(args[0]) is ffi.typeof('gcry_sexp_t'):
                    self._SExpression__sexp = args[0]
                    self.fmt = 'ADVANCED'
                    return
            items = re.findall('%([mMsdubS])', args[0].decode())
            i = 1
            vargs = []
            for item in items:
                if item in ('m', 'M'):
                    if not isinstance(args[i], MPI):
                        raise TypeError('Item {} (%{}) should be of type MPI, got {} instead'.format(i, item, type(args[i])))
                    vargs.append(args[i].mpi)
                    i += 1
                    continue
                if item == 's':
                    data = args[i]
                    if isinstance(data, str):
                        data = data.encode()
                    if not isinstance(data, bytes):
                        raise TypeError('Item {} (%{}) should be of type bytes or str, got {} instead'.format(i, item, type(data)))
                    vargs.append(ffi.new('char []', data))
                    i += 1
                    continue
                if item in ('d', 'u'):
                    if not isinstance(args[i], int):
                        raise TypeError('Item {} (%{}) should be of type int, got {} instead'.format(i, item, type(args[i])))
                    else:
                        if item == 'u':
                            if args[i] < 0:
                                raise TypeError('Item {} (%{}) should be of type unsigned int, got a negative number'.format(i, item))
                        if item == 'u':
                            vargs.append(ffi.cast('unsigned int', args[i]))
                        else:
                            vargs.append(ffi.cast('int', args[i]))
                    i += 1
                else:
                    if item == 'b':
                        try:
                            if not isinstance(args[i], int):
                                raise TypeError('Item {} (%{}) should be preceded by an int which value is the length of the string'.format(i, item))
                            else:
                                data = args[(i + 1)]
                                if isinstance(data, str):
                                    data = data.encode()
                                raise isinstance(data, bytes) or TypeError('Item {} (%{}) should be of type bytes or str, got {} instead'.format(i, item, type(data)))
                            vargs.append(ffi.cast('int', args[i]))
                            vargs.append(ffi.new('char []', data))
                            i += 2
                            continue
                        except IndexError:
                            raise TypeError('Item {} (%{}) should be made of two parts.'.format(i, item))

                    if item == 'S':
                        if not isinstance(args[i], SExpression):
                            raise TypeError('Item {} (%{}) should be a S-Expression, got a {} instead'.format(i, item, type(args[i])))
                        if not repr(args[i]).startswith("SExpression(b'("):
                            raise ValueError("Item {} (%{}) must be an SExpression starting by a '('".format(i, item))
                        vargs.append(args[i].sexp)
                        i += 1
                        continue

            error = (lib.gcry_sexp_build)(sexp, ffi.cast('size_t *', erroffset), args[0], *vargs)
        if error > 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)
        self._SExpression__sexp = sexp[0]
        self.fmt = 'ADVANCED'

    def __iter__(self):
        """
        We will iterate through the S-expression, retruning each item as a SExpression.
        """
        i = 0
        while i < len(self):
            yield self[i]
            i += 1

    def __getattr__(self, attr):
        if attr == 'sexp':
            if ffi.typeof(self._SExpression__sexp) == ffi.typeof('gcry_sexp_t *'):
                return self._SExpression__sexp[0]
            if ffi.typeof(self._SExpression__sexp) == ffi.typeof('gcry_sexp_t'):
                return self._SExpression__sexp
            raise Exception
        else:
            if attr == 'car':
                return SExpression(lib.gcry_sexp_car(self.sexp))
            if attr == 'cdr':
                return self[1:len(self)]

    def __setattr__(self, attr, value):
        if attr == 'sexp':
            self._SExpression__sexp = value
        super(SExpression, self).__setattr__(attr, value)

    def __size__(self):
        """
        Return the actual size in bytes of the sexpression
        """
        fmt = getattr(lib, 'GCRYSEXP_FMT_' + self.fmt)
        return lib.gcry_sexp_sprint(self.sexp, fmt, ffi.NULL, 0)

    def __len__(self):
        """
        Returns the len of the S-expression.
        """
        return lib.gcry_sexp_length(self.sexp)

    def __contains__(self, item):
        """
        Let's check if an item is present in the SExpression
        """
        if isinstance(item, str):
            item = item.encode()
        if not isinstance(item, bytes):
            raise TypeError('item should be of type bytes or str, got {} instead'.format(type(item)))
        exist = lib.gcry_sexp_find_token(self.sexp, item, len(item))
        if exist == ffi.NULL:
            return False
        else:
            return True

    def __repr__(self):
        """
        We need to print the S-expression in a format that can be used to be parsed
        into another S-expression. It means that we should be able to eval the result
        of this command to create a new S-Expression, so the returned result should
        be something like that: "SExpression(b'(item (list 1 2 3))')"
        """
        fmt = getattr(lib, 'GCRYSEXP_FMT_' + self.fmt)
        bytes_out = ffi.new('char [{}]'.format(self.__size__()))
        size = lib.gcry_sexp_sprint(self.sexp, fmt, bytes_out, self.__size__())
        bytes_repr = ffi.buffer(bytes_out, size)[:]
        return 'SExpression({})'.format(repr(bytes_repr))

    @classmethod
    def dict_constructor(cls, expression, constructor=''):
        for key in expression:
            if isinstance(expression[key], MPI):
                constructor += '(%s #%s#)' % (key.encode(), expression[key].to_bytes().hex().encode())
            elif isinstance(expression[key], str):
                constructor += '(%s "%s")' % (key.encode(), expression[key].encode())
            elif isinstance(expression[key], bytes):
                constructor += '(%s "%s")' % (key.encode(), expression[key])
            else:
                if isinstance(expression[key], int):
                    constructor += '(%s "%s")' % (key.encode(), repr(expression[key]).encode())
                else:
                    if isinstance(expression[key], dict):
                        constructor += cls.dict_constructor(expression[key], constructor)
                        constructor = '(%s %s)' % (key.encode(), constructor)
                    else:
                        raise Exception('Unsupported data type {}'.format(expression[key]))

        return constructor

    @classmethod
    def from_dict(cls, expression):
        """
        Let's try to create a SExpression from a dict. The function will parse the (key, value) pair
        of the expression given as a dict, and try to assemble a string suitable to be given as a
        SExpression constructor, usually a bytes of the form b'(key value)'

        The function will then return a SExpression.
        """
        return cls(cls.dict_constructor(expression))

    def dump(self):
        """
        Dump the S-expression in a format suitable for libgcrypt debug mode
        """
        lib.gcry_sexp_dump(self.sexp)

    def __delitem__(self, key):
        """
        Let's delete an item. Item must be in the cdr
        """
        if isinstance(key, str):
            key = key.encode()
        if key not in self.cdr:
            raise KeyError
        new_cdr = [item for item in self.cdr if item.getstring(0) != key]
        print(new_cdr)
        sexp = ' %S' * len(new_cdr)
        new_sexp = SExpression('(%s' + sexp + ')', self.car.getstring(0), *new_cdr)
        self.sexp = new_sexp.sexp

    def __setitem__(self, key, value):
        """
        This is used to set an item. It will be appended to the cdr of the S-expression.
        """
        if key in self:
            raise Exception('Item {} already set')
        else:
            if isinstance(value, str):
                value = value.encode()
            else:
                if isinstance(value, bytes):
                    queue = SExpression('({} %s)'.format(key).encode(), value)
                if isinstance(value, SExpression):
                    queue = SExpression('({} %S)'.format(key).encode(), value)
                if isinstance(value, MPI):
                    queue = SExpression('({} %m)'.format(key).encode(), value)
            if isinstance(value, int):
                queue = SExpression('({} %d)'.format(key).encode(), value)
        i = 0
        cdr = []
        queue_sexp = ''
        for item in self.cdr:
            i += 1
            queue_sexp += '%S'
            cdr.append(item)

        sexp = ('(%S {} %S)', format(queue_sexp))
        new_sexp = SExpression('(%s ({} %S))'.format(queue_sexp).encode(), self.car.getstring(0), *cdr, *(queue,))
        self.sexp = new_sexp.sexp

    def __getitem__(self, key):
        """
        This is used to navigate through a S-expression, using token, slice or indexes.
        """
        if isinstance(key, str):
            key = key.encode()
            sexp_match = lib.gcry_sexp_find_token(self.sexp, key, 0)
            if sexp_match != ffi.NULL:
                return SExpression(sexp_match).cdr
            raise KeyError
        else:
            if isinstance(key, bytes):
                sexp_match = lib.gcry_sexp_find_token(self.sexp, key, 0)
                if sexp_match != ffi.NULL:
                    return SExpression(sexp_match).cdr
                raise KeyError
            if isinstance(key, int):
                sexp_match = lib.gcry_sexp_nth(self.sexp, key)
                if sexp_match != ffi.NULL:
                    return SExpression(sexp_match)
                raise IndexError
            if isinstance(key, slice):
                start = key.start
                stop = key.stop
                if not (key.step == 1 or key.step == None):
                    raise IndexError
                if stop > len(self) or start > len(self):
                    raise IndexError
                fmt = '%S ' * (stop - start)
                if stop - start > 1:
                    fmt = '({})'.format(fmt)
                fmt = fmt.encode()
                args = [SExpression(lib.gcry_sexp_nth(self.sexp, i)) for i in range(start, stop)]
                return SExpression(fmt, *args)

    def __eq__(self, other):
        """
        Try to test if two SExpression are equals
        """
        if not isinstance(other, SExpression):
            if not TypeError('Cannot test equality with something else than a SExpression, got {}'.format(type(other))):
                raise AssertionError
        return repr(self) == repr(other)

    def keys(self):
        _SExpression__keys = []
        for item in self:
            try:
                self[item.car.getstring(0)]
                _SExpression__keys.append(item.car.getstring(0))
            except KeyError:
                continue

        return _SExpression__keys

    def getstring(self, index):
        """
        This is used to get the string stored at index value in a SExpression.

        If the value can't be converted to a string or self[index] is another list, then
        we will return None
        """
        value = lib.gcry_sexp_nth_string(self.sexp, index)
        if value == ffi.NULL:
            return
        else:
            return ffi.string(value)

    def getdata(self, index):
        """
        This is isued ti get the bytes stored at index value in e SExpression.

        If the value can't be converted to a bytes or self[index] is another list, then
        we will return None
        """
        len = ffi.new('size_t *')
        value = lib.gcry_sexp_nth_data(self.sexp, index, len)
        if value == ffi.NULL:
            return
        else:
            return ffi.buffer(value, len[0])[:]

    def getmpi(self, index, fmt='USG'):
        """
        This is used to get the mpi stored at index value in a SExpression

        If the value can't be converted to a MPI or self[index]  is another list, then
        we will return None
        """
        mpi = lib.gcry_sexp_nth_mpi(self.sexp, index, lib.GCRYMPI_FMT_USG)
        if mpi == ffi.NULL:
            return
        else:
            opaque = lib.gcry_mpi_get_flag(mpi, lib.GCRYMPI_FLAG_OPAQUE)
            if opaque == 1:
                result = MPIopaque()
            else:
                result = MPIint()
            result.mpi = mpi
            return result

    def extract(self, params, path=None):
        """
        Extract parameters from an S-expression using a list of parameters name. It works in a simialr way to getopts.
        We must first parse the params string, in order to allocate enough mpi to hold the data.
        The result will be a dict of MPI mapped to their param name.

        If path is precised we will search for parameters inside a sub S-epression
        """
        match = re.compile("([+-/&]?(\\w{1}|'\\w+'))")
        results = match.findall(params)
        result = {}
        pointers = []
        for item in results:
            if item[0].startswith('-'):
                result[item[1]] = MPIint()
            else:
                if item[0].startswith('/'):
                    result[item[1]] = MPIopaque()
                else:
                    result[item[1]] = MPIint()
                    result[item[1]].fmt = 'USG'
            pointers.append(ffi.new('gcry_mpi_t *'))

        pointers += [ffi.NULL]
        if path == None:
            path = ffi.NULL
        error = ffi.cast('gcry_error_t', 0)
        error = (lib.gcry_sexp_extract_param)(self.sexp, path, params.encode(), *pointers)
        if error != 0:
            raise errors.GcryptException(ffi.string(lib.gcry_strerror(error)).decode(), error)
        i = 0
        for mpi in result:
            result[mpi].mpi = pointers[i][0]
            i += 1

        return result