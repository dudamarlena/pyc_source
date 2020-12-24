# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sy85\sysex.py
# Compiled at: 2010-02-26 15:56:35
"""Classes and functions for representing and handling SY85 sysex bulk dumps."""
import logging, struct
from itertools import chain
import bulktypes
from constants import *
from binutils import bin, read_midi_short

class SysexParseError(Exception):
    pass


class UnsupportedSysexType(SysexParseError):
    pass


class UnsupportedBulkType(SysexParseError):
    pass


class ChecksumError(SysexParseError):
    pass


def is_yamaha_sysex(data):
    """Return True if given data looks like a Yamaha Sysex bulk dump."""
    return len(data) >= 8 and data.startswith(SOX + MANUFACTURER_ID)


class SY85SysexContainer(dict):
    bulk_types = [
     'voices',
     'drumvoices',
     'performances',
     'multis',
     'songs',
     'rhythms',
     'seq_dumps',
     'synth_setups',
     'seq_setups',
     'samples']

    def __init__(self, strict=False):
        super(SY85SysexContainer, self).__init__()
        for type_ in self.bulk_types:
            self[type_] = []

        self.strict = strict

    @classmethod
    def fromfile(cls, fn, strict=False):
        if isinstance(fn, basestring):
            fn = open(fn, 'rb')
        inst = cls(strict)
        inst.parse_sysex_data(fn.read())
        return inst

    def parse_sysex_data(self, data):
        chunks = data.split(SOX)[1:]
        for (i, chunk) in enumerate(chunks):
            try:
                (typecode, data, checksum) = self.parse_sysex_chunk(SOX + chunk)
            except SysexParseError, exc:
                if self.strict:
                    raise
                else:
                    logging.warning('Parse error chunk %i: %s', i, exc)

        if not chunks:
            raise SysexParseError('No valid sysex chunks found.')

    def parse_sysex_chunk(self, data):
        if not is_yamaha_sysex(data):
            raise SysexParseError('Unrecognized data format.')
        data = data.rstrip(EOX)
        header, data, checksum = data[:6], data[6:-1], ord(data[(-1)])
        (sox, man_id, dev_id, msg_fmt_id, bc_msb, bc_lsb) = struct.unpack('6B', header)
        typecode = data[4:10]
        bc = read_midi_short(bc_msb, bc_lsb)
        if chr(msg_fmt_id) not in (MSG_ID_BULK_DUMP, MSG_ID_NSEQ_DUMP):
            raise UnsupportedSysexType('Only sysex bulk dump messages are supported.')
        if len(data) != bc:
            if typecode not in ('0065RY', '0065SQ') or bc != 538:
                raise SysexParseError('Bogus data length, chunk type %s. Read: %i, actual: %i' % (
                 typecode, bc, len(data)))
        self._check_checksum(data, checksum)
        logging.debug('Adding chunk of type %s' % typecode)
        self.add_chunk(typecode, data)
        return (typecode, data, checksum)

    def add_chunk(self, typecode, data):
        try:
            typename = BULKDATATYPES[typecode]['name']
        except KeyError:
            raise UnsupportedBulkType('Bulk message type not supported: %s' % typecode)

        container_name = typename.lower().replace(' ', '_') + 's'
        container = self.get(container_name)
        bulkclass = getattr(bulktypes, BULKDATATYPES[typecode]['classname'])
        container.append(bulkclass(typecode, data))

    def _check_checksum(self, data, checksum):
        checkbyte = sum([ ord(c) for c in data ]) + checksum & 127
        if checkbyte:
            raise ChecksumError('Checksum error: %s (%i), result: %s' % (
             bin(checksum), checksum, bin(checkbyte)))

    @property
    def chunks(self):
        return chain(*[ self[type_] for type_ in self.bulk_types ])

    def dump(self, output=None):
        """Dump all chunks to given file or return them as a string if no file is given."""
        data = [ chunk.dump() for chunk in self.chunks ]
        if output:
            if isinstance(output, file):
                fo = output
            else:
                fo = open(output, 'wb')
            fo.write(('').join(data))
            if not isinstance(output, file):
                fo.close()
        else:
            return ('').join(data)