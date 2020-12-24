# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hamtools/adif.py
# Compiled at: 2016-09-28 21:35:13
"""
Python API for reading the Amateur Data Interchange Format, aka ADIF.

ADIF version 1.0 is supported.
"""
from collections import namedtuple, OrderedDict
from decimal import Decimal
from datetime import datetime
BLOCKSIZE = 1024

class ParseError(Exception):
    pass


class Field(object):
    __slots__ = [
     'name', 'type', 'body']

    def __init__(self, name='', type='', body=''):
        self.name = name
        self.type = type
        self.body = body

    def __repr__(self):
        return (' ').join(('<Field', self.name, self.type, self.body, '>'))

    def __eq__(self, s2):
        if self.name == s2.name and self.type == s2.type and s2.body == self.body:
            return True
        return False

    def __ne__(self, s2):
        if self.name == s2.name or self.type == s2.type or s2.body == self.body:
            return False
        return True


class Reader(object):

    def __init__(self, flo):
        self.adif_ver = None
        self.flo = flo
        flo.seek(0)
        c = flo.read(1)
        if c == '<':
            self.header_present = False
            flo.seek(0)
        else:
            self.header_present = True
            for field in self._lex(blocksize=1):
                if field.name == 'adif_ver':
                    self.adif_ver = field.body
                elif field.name == 'eoh':
                    break

        self.bookmark = flo.tell()
        return

    def _lex(self, blocksize=BLOCKSIZE):
        """Given a file like object, yield named tuple for each record."""
        flo = self.flo
        state = 'comment'
        pos = 0
        field = Field()
        while True:
            buf = flo.read(blocksize)
            for c in buf:
                if state == 'comment':
                    if c == '<':
                        state = 'name'
                        field = Field()
                elif state == 'name':
                    if c == ':':
                        state = 'len'
                        field_len = ''
                    elif c == '>':
                        state = 'comment'
                        field.name = field.name.lower()
                        field.type = field.type.lower()
                        yield field
                    else:
                        field.name = field.name + c
                elif state == 'len':
                    if c == ':':
                        state = 'type'
                        field_len = int(field_len)
                    elif c == '>':
                        state = 'body'
                        field_len = int(field_len)
                    else:
                        field_len = field_len + c
                elif state == 'type':
                    if c == ':':
                        raise ParseError()
                    elif c == '>':
                        state = 'body'
                    else:
                        field.type = field.type + c
                elif state == 'body':
                    if field_len > 0:
                        field.body = field.body + c
                        field_len -= 1
                    if field_len == 0:
                        state = 'comment'
                        field.name = field.name.lower()
                        field.type = field.type.lower()
                        yield field
                else:
                    raise Exception('Invalid state at %d' % pos)
                pos += 1

            if len(buf) < blocksize:
                break

    def __iter__(self):
        """Iterate over records in file"""
        self.flo.seek(self.bookmark)
        rec = OrderedDict()
        for field in self._lex():
            if field.name == 'eor':
                if 'qso_date' in rec and 'time_on' in rec:
                    rec['app_datetime_on'] = datetime(int(rec['qso_date'][:4]), int(rec['qso_date'][4:6]), int(rec['qso_date'][6:8]), int(rec['time_on'][:2]), int(rec['time_on'][2:4]))
                if 'qso_date' in rec and 'time_off' in rec:
                    rec['app_datetime_off'] = datetime(int(rec['qso_date'][:4]), int(rec['qso_date'][4:6]), int(rec['qso_date'][6:8]), int(rec['time_off'][:2]), int(rec['time_off'][2:4]))
                yield rec
                rec = OrderedDict()
            else:
                rec[field.name] = field.body


def format_header(header_text=' ', adif_ver=None):
    assert header_text != ''
    if adif_ver is None:
        return '%s<eoh>' % header_text
    else:
        return '%s<adif_ver:%d>%s<eoh>' % (
         header_text, len(adif_ver), adif_ver)


def format_record(record):
    fields = []
    for k, v in record.iteritems():
        if k == 'app_datetime_on':
            continue
        fields.append('<%s:%d>%s' % (k, len(v), v))

    fields.append('<eor>')
    return ('').join(fields)