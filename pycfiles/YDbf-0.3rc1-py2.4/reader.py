# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ydbf/reader.py
# Compiled at: 2009-07-14 03:19:12
"""
DBF reader
"""
__all__ = [
 'YDbfStrictReader', 'YDbfReader']
import datetime
from struct import calcsize, unpack
from itertools import izip
from ydbf import lib
try:
    from decimal import Decimal
    decimal_enabled = True
except ImportError:
    Decimal = lambda x: float(x)
    decimal_enabled = False

class YDbfReader(object):
    """
    Basic class for reading DBF
    
    Instance is an iterator over DBF records
    """
    __module__ = __name__

    def __init__(self, fh, fields=None, use_unicode=True, encoding=None):
        """
        Iterator over DBF records
        
        Args:
            `fh`:
                filehandler (should be opened for binary reading)
            
            `fields`:
                force to use your own DBF fields structure instead of builtin.
                Fields structure is defined as [(NAME, TYP, SIZE, DEC),]
            
            `use_unicode`:
                convert all char fields to unicode. Use builtin
                encoding (formerly lang code from DBF file) or
                implicitly defined encoding via `encoding` arg.
            
            `encoding`:
                force usage of implicitly defined encoding
                instead of builtin one. By default None.
        """
        self.fh = fh
        self.implicit_encoding = encoding
        if fields:
            self._fields = [
             ('_deletion_flag', 'C', 1, 0)] + list(fields)
            self.fields = list(fields)
            self.builtin_fields = []
            self.builtin__fields = []
        else:
            self._fields = []
            self.fields = []
            self.builtin_fields = []
            self.builtin__fields = []
        self.numrec = 0
        self.lenheader = 0
        self.numfields = 0
        self.fields = []
        self.field_names = ()
        self.start_from = 0
        self.stop_at = 0
        self.recfmt = ''
        self.recsize = 0
        self.dt = None
        self.dbf2date = lib.dbf2date
        self.encoding = None
        self.builtin_encoding = None
        self.converters = {}
        self.actions = {}
        self.action_resolvers = ()
        self.iterator = None
        self._readHeader()
        if use_unicode:
            self._defineEncoding()
        self._makeActions()
        self.postInit()
        return

    def postInit(self):
        pass

    def _makeActions(self):
        logic = {'Y': True, 'y': True, 'T': True, 't': True, 'N': False, 'n': False, 'F': False, 'f': False}
        self.actions = {'date': lambda val, size, dec: self.dbf2date(val.strip()), 
           'logic': lambda val, size, dec: logic.get(val.strip()), 
           'unicode': lambda val, size, dec: val.decode(self.encoding).rstrip(), 
           'string': lambda val, size, dec: val.rstrip(), 
           'integer': lambda val, size, dec: (val.strip() or 0) and int(val.strip()), 
           'decimal': lambda val, size, dec: Decimal('%%.%df' % dec % float(val.strip() or 0.0))}
        self.action_resolvers = (
         lambda typ, size, dec: typ == 'C' and self.encoding and 'unicode',
         lambda typ, size, dec: typ == 'C' and not self.encoding and 'string',
         lambda typ, size, dec: typ == 'N' and dec and 'decimal',
         lambda typ, size, dec: typ == 'N' and not dec and 'integer',
         lambda typ, size, dec: typ == 'D' and 'date',
         lambda typ, size, dec: typ == 'L' and 'logic')
        for (name, typ, size, dec) in self._fields:
            for resolver in self.action_resolvers:
                action = resolver(typ, size, dec)
                if action:
                    self.converters[name] = self.actions[action]
                    break

            if not action:
                raise ValueError('Cannot find dbf-to-python converter for field %s (type %s)' % (name, typ))

    def _readHeader(self):
        """
        Read DBF header
        """
        self.fh.seek(0)
        (sig, year, month, day, numrec, lenheader, recsize, lang) = unpack(lib.HEADER_FORMAT, self.fh.read(32))
        year = year + 1900
        if year < 1950:
            year = year + 100
        self.dt = datetime.date(year, month, day)
        self.sig = sig
        if sig not in lib.SUPPORTED_SIGNATURES:
            version = lib.SIGNATURES.get(sig, 'UNKNOWN')
            raise ValueError("DBF version '%s' (signature %s) not supported" % (version, hex(sig)))
        numfields = (lenheader - 33) // 32
        fields = []
        for fieldno in xrange(numfields):
            (name, typ, size, deci) = unpack(lib.FIELD_DESCRIPTION_FORMAT, self.fh.read(32))
            name = name.split('\x00', 1)[0]
            if typ not in ('N', 'D', 'L', 'C'):
                raise ValueError('Unknown type %r on field %s' % (typ, name))
            fields.append((name, typ, size, deci))

        terminator = self.fh.read(1)
        if terminator != '\r':
            raise ValueError("Terminator should be 0x0d. Terminator is a delimiter, which splits header and data sections in file. By specification it should be 0x0d, but it '%s'. This may be as result of corrupted file, non-DBF data or error in YDbf library." % hex(terminator))
        fields.insert(0, ('_deletion_flag', 'C', 1, 0))
        self.builtin__fields = fields
        self.builtin_fields = fields[1:]
        if not self.fields:
            self.fields = self.builtin_fields
            self._fields = self.builtin__fields
        self.raw_lang = lang
        self.recfmt = ('').join([ '%ds' % fld[2] for fld in self._fields ])
        self.recsize = calcsize(self.recfmt)
        self.numrec = numrec
        self.lenheader = lenheader
        self.numfields = numfields
        self.stop_at = numrec
        self.field_names = [ fld[0] for fld in self.fields ]

    def _defineEncoding(self):
        self.builtin_encoding = lib.ENCODINGS.get(self.raw_lang, (None, ))[0]
        if self.builtin_encoding is None and self.implicit_encoding is None:
            raise ValueError('Cannot resolve builtin lang code %s to encoding and no option `encoding` passed, but `use_unicode` are, so there is no info how we can decode chars to unicode. Please, set up option `encoding` or set `use_unicode` to False' % hex(self.raw_lang))
        if self.implicit_encoding:
            self.encoding = self.implicit_encoding
        else:
            self.encoding = self.builtin_encoding
        return

    def __iter__(self):
        if not self.iterator:
            self.iterator = self.records()
        return self.iterator

    def next(self):
        if not self.iterator:
            self.iterator = self.records()
        return self.iterator.next()

    def __len__(self):
        """
        Get number of records in DBF
        """
        return self.numrec

    def records(self, start_from=None, limit=None, show_deleted=False):
        """
        Iterate over DBF records
        
        Args:
            `start_from`:
                index of record start from (optional)
            `limit`:
                limits number of iterated records (optional)
            `show_deleted`:
                do not skip deleted records (optional)
                False by default
        """
        if start_from is not None:
            self.start_from = start_from
        offset = self.lenheader + self.recsize * self.start_from
        if self.fh.tell() != offset:
            self.fh.seek(offset)
        if limit is not None:
            self.stop_at = self.start_from + limit
        converters = tuple(((self.converters[name], name, size, dec) for (name, typ, size, dec) in self._fields))
        for i in xrange(self.start_from, self.stop_at):
            record = unpack(self.recfmt, self.fh.read(self.recsize))
            if not show_deleted and record[0] != ' ':
                continue
            try:
                yield dict(((name, conv(val, size, dec)) for ((conv, name, size, dec), val) in izip(converters, record) if name != '_deletion_flag' or show_deleted))
            except UnicodeDecodeError, err:
                args = list(err.args[:-1]) + ['Error occured while reading rec #%d. You are using YDbfReader with unicode-related options: actual encoding %s, builtin DBF encoding %s (raw lang code %s), manually set encoding is %s. Probably, data in DBF file is not encoded with %s encoding, so you should manually define encoding by setting up `encoding` option' % (i, self.encoding, self.builtin_encoding, hex(self.raw_lang), self.implicit_encoding, self.encoding)]
                raise UnicodeDecodeError(*args)
            except (IndexError, ValueError, TypeError, KeyError), err:
                raise RuntimeError('Error occured (%s: %s) while reading rec #%d' % (err.__class__.__name__, err, i))

        return

    def read(self):
        return self.records()

    def close(self):
        return self.fh.close()


class YDbfStrictReader(YDbfReader):
    """
    DBF-reader with additional logical checks
    """
    __module__ = __name__

    def postInit(self):
        super(YDbfStrictReader, self).postInit()
        self.checkConsistency()

    def checkConsistency(self):
        """
        Some logical checks of DBF structure.
        If some check failed, AssertionError is raised.
        """
        assert self.recsize > 1, 'Length of record must be >1'
        if self.sig in (3, 4):
            assert self.recsize < 4000, 'Length of record must be <4000 B for dBASE III and IV'
        assert self.recsize < 32 * 1024, 'Length of record must be <32KB'
        assert self.numrec >= 0, 'Number of records must be non-negative'
        assert self.numfields > 0, 'The dbf file must have at least one field'
        if self.sig == 3:
            assert self.numfields < 128, 'Number of fields in dBASE III must be <128'
        if self.sig == 4:
            assert self.numfields < 256, 'Number of fields in dBASE IV must be <256'
        for (f_name, f_type, f_size, f_decimal) in self.fields:
            if f_type == 'N':
                assert f_size < 20, "Size of numeral field must be <20 (field '%s', size %d)" % (f_name, f_size)
            if f_type == 'C':
                assert f_size < 255, "Size of numeral field must be <255 (field '%s', size %d)" % (f_name, f_size)
            if f_type == 'L':
                assert f_size == 1, "Size of logical field must be 1 (field '%s', size %d)" % (f_name, f_size)

        file_name = getattr(self.fh, 'name', None)
        if file_name is not None:
            import os
            try:
                os_size = os.stat(file_name)[6]
            except OSError, msg:
                return
            else:
                dbf_size = long(self.lenheader + 1 + self.numrec * self.recsize)
                assert os_size == dbf_size
        return