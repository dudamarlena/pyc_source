# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/plotter/regex.py
# Compiled at: 2012-06-28 06:14:39
import os, re
from mole.plotter import Plotter

class PlotterRegexError(Exception):
    """Error plottering with a regular expression."""
    pass


class PlotterRegex(Plotter):
    """The plotter split a stream into lines, using a regular expression."""
    BREAK_BEFORE = 0
    BREAK_AFTER = 1

    def __init__(self, regex, break_condition=BREAK_BEFORE, bufsize=1024):
        """Create a new :class:`PlotterBasic` object, which split lines when
        find a regular expression in the stream.

        :param `regex`: the regular expression to find into.
        :param `break_condition`: a keyword 'before' or 'after', which means
            where the line is break relative to the expression found.
        :param `bufsize`: the buffer chunk size in bytes, buy default
            1024.
        """
        self.regex = re.compile(regex, re.MULTILINE)
        self.BUFSIZE = bufsize
        if break_condition == 'before':
            self.break_condition = self.BREAK_BEFORE
        elif break_condition == 'after':
            self.break_condition = self.BREAK_AFTER
        else:
            self.break_condition = break_condition

    def __call__(self, stream):
        """Plotter processor.

        :param:`stream` a stream which a read method is available.
        """
        spool = ''
        chunk = ''
        chunk = stream.read(self.BUFSIZE)
        while chunk:
            spool += chunk
            if self.break_condition == self.BREAK_BEFORE:
                items = map(lambda x: x.start(), [ x for x in self.regex.finditer(spool) ])
            if self.break_condition == self.BREAK_AFTER:
                items = map(lambda x: x.end(), [ x for x in self.regex.finditer(spool) ])
            pos = 0
            for index in items[:-1]:
                if index == pos:
                    continue
                yield spool[pos:index].rstrip(os.linesep)
                pos = index

            spool = spool[pos:]
            chunk = stream.read(self.BUFSIZE)

        if spool:
            if self.break_condition == self.BREAK_BEFORE:
                items = map(lambda x: x.start(), [ x for x in self.regex.finditer(spool) ])
            if self.break_condition == self.BREAK_AFTER:
                items = map(lambda x: x.end(), [ x for x in self.regex.finditer(spool) ])
            pos = 0
            for index in items:
                if index == pos:
                    continue
                yield spool[pos:index].rstrip(os.linesep)
                pos = index

            spool = spool[pos:]
        if spool:
            yield spool.rstrip(os.linesep)