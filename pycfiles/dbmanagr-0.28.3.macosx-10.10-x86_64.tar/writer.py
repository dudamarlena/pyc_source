# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/writer.py
# Compiled at: 2015-10-11 07:17:06
import logging, codecs, sys
from dbmanagr.logger import LogWith
from dbmanagr.formatter import Formatter, TestFormatter, DefaultFormatter
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
logger = logging.getLogger(__name__)

class DefaultWriter(object):

    def write(self, items):
        return self.str(items)

    def str(self, items):
        return map(self.itemtostring, items)

    def itemtostring(self, item):
        return unicode(item)


class StdoutWriter(DefaultWriter):

    def __init__(self, items_format='Title\tSubtitle\tAutocomplete\n{0}\n', item_format='{title}\t{subtitle}\t{autocomplete}', item_separator='\n', format_error_format='{0}'):
        self.items_format = items_format
        self.item_format = item_format
        self.item_separator = item_separator
        self.format_error_format = format_error_format
        Formatter.set(DefaultFormatter())

    def filter_(self, items):
        return items

    def str(self, items):
        items = self.prepare(items)
        items = self.filter_(items)
        s = self.item_separator.join(map(self.itemtostring, items))
        return self.items_format.format(s)

    def prepare(self, items):
        if not items:
            return []
        return items

    def itemtostring(self, item):
        return self.item_format.format(item=unicode(item), **item.__dict__)


class FormatWriter(StdoutWriter):

    def __init__(self, items_format='Title\tSubtitle\tAutocomplete\n{0}\n', item_format='{title}\t{subtitle}\t{autocomplete}', item_separator='\n', format_error_format='{0}'):
        StdoutWriter.__init__(self, items_format, item_format, item_separator, format_error_format)

    def itemtostring(self, item):
        return item.format()


class TestWriter(FormatWriter):

    def __init__(self, items_format='Title\tAutocomplete\n{0}', item_format='{title}\t{autocomplete}'):
        FormatWriter.__init__(self, items_format, item_format)
        Formatter.set(TestFormatter())


class Writer(object):
    writer = StdoutWriter()

    @staticmethod
    def set(arg):
        Writer.writer = arg

    @staticmethod
    @LogWith(logger, log_args=False, log_result=False)
    def write(items):
        return Writer.writer.write(items)

    @staticmethod
    @LogWith(logger, log_args=False, log_result=False)
    def itemtostring(item):
        return Writer.writer.itemtostring(item)