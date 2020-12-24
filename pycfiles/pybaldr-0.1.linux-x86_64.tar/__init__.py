# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/pybaldr/venv/lib/python2.7/site-packages/pybaldr/__init__.py
# Compiled at: 2015-03-23 01:06:08
import struct
RECORD_LENGTH_BUFFER_SIZE = 8
CHUNK_LENGTH_BYTES = 1024

class BaldrRecord(object):
    """
    A container for the header and body of a Baldr record.
    """

    def __init__(self, header, body):
        self.header = header
        self.body = body

    def __len__(self):
        return struct.unpack('>Q', self.header)[0]

    def __unicode__(self):
        return '%s byte body: %s' % (len(self), unicode(self.body))


def full_read(bytes):
    """
    Returns a list of BaldrRecord objects. This method is not optimized for
    performance.
    """
    results = []
    cursor = 0
    while cursor < len(bytes) - 1:
        start_header = cursor
        end_header = cursor + RECORD_LENGTH_BUFFER_SIZE
        header = bytes[start_header:end_header]
        start_body = end_header
        end_body = start_body + struct.unpack('>Q', header)[0]
        body = bytes[start_body:end_body]
        results.append(BaldrRecord(header, body))
        cursor = end_body

    return results