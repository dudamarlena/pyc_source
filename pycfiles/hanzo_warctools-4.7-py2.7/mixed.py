# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hanzo/warctools/mixed.py
# Compiled at: 2013-01-14 05:25:26
from hanzo.warctools.record import ArchiveRecord, ArchiveParser
from hanzo.warctools.warc import WarcParser
from hanzo.warctools.arc import ArcParser

class MixedRecord(ArchiveRecord):

    @classmethod
    def make_parser(self):
        return MixedParser()


class MixedParser(ArchiveParser):

    def __init__(self):
        self.arc = ArcParser()
        self.warc = WarcParser()

    def parse(self, stream, offset=None):
        line = stream.readline()
        while line:
            if line.startswith('WARC'):
                return self.warc.parse(stream, offset, line=line)
            if line not in ('\n', '\r\n', '\r'):
                return self.arc.parse(stream, offset, line=line)
            line = stream.readline()

        return (
         None, (), offset)