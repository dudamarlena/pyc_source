# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/video/mpeg_ts.py
# Compiled at: 2009-09-07 17:44:28
"""
MPEG-2 Transport Stream parser.

Documentation:
- MPEG-2 Transmission
  http://erg.abdn.ac.uk/research/future-net/digital-video/mpeg2-trans.html

Author: Victor Stinner
Creation date: 13 january 2007
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, ParserError, MissingField, UInt8, Enum, Bit, Bits, RawBytes
from hachoir_core.endian import BIG_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal

class Packet(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        if self['has_error'].value:
            self._size = 204 * 8
        else:
            self._size = 188 * 8

    PID = {0: 'Program Association Table (PAT)', 1: 'Conditional Access Table (CAT)', 8191: 'Null packet'}

    def createFields(self):
        yield textHandler(UInt8(self, 'sync', 8), hexadecimal)
        if self['sync'].value != 71:
            raise ParserError('MPEG-2 TS: Invalid synchronization byte')
        yield Bit(self, 'has_error')
        yield Bit(self, 'payload_unit_start')
        yield Bit(self, 'priority')
        yield Enum(textHandler(Bits(self, 'pid', 13, 'Program identifier'), hexadecimal), self.PID)
        yield Bits(self, 'scrambling_control', 2)
        yield Bit(self, 'has_adaptation')
        yield Bit(self, 'has_payload')
        yield Bits(self, 'counter', 4)
        yield RawBytes(self, 'payload', 184)
        if self['has_error'].value:
            yield RawBytes(self, 'error_correction', 16)

    def createDescription(self):
        text = 'Packet: PID %s' % self['pid'].display
        if self['payload_unit_start'].value:
            text += ', start of payload'
        return text

    def isValid(self):
        if not self['has_payload'].value and not self['has_adaptation'].value:
            return 'No payload and no adaptation'
        pid = self['pid'].value
        if 2 <= pid <= 15 or 8192 <= pid:
            return 'Invalid program identifier (%s)' % self['pid'].display
        return ''


class MPEG_TS(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': 'mpeg_ts', 'category': 'video', 'file_ext': ('ts', ), 'min_size': 188 * 8, 'description': 'MPEG-2 Transport Stream'}
    endian = BIG_ENDIAN

    def validate(self):
        sync = self.stream.searchBytes('G', 0, 204 * 8)
        if sync is None:
            return 'Unable to find synchronization byte'
        for index in xrange(5):
            try:
                packet = self[('packet[%u]' % index)]
            except (ParserError, MissingField):
                if index and self.eof:
                    return True
                else:
                    return 'Unable to get packet #%u' % index

            err = packet.isValid()
            if err:
                return 'Packet #%u is invalid: %s' % (index, err)

        return True

    def createFields(self):
        sync = self.stream.searchBytes('G', 0, 204 * 8)
        if sync is None:
            raise ParserError('Unable to find synchronization byte')
        elif sync:
            yield RawBytes(self, 'incomplete_packet', sync // 8)
        while not self.eof:
            yield Packet(self, 'packet[]')

        return