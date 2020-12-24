# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/loggrok/parse.py
# Compiled at: 2006-01-04 21:01:57
"""Log file entry parsers
"""
from UserDict import UserDict
import sys, re
__author__ = 'Drew Smathers'
__copyright__ = 'Copyright 2005, Drew Smathers'
__revision__ = '$Revision: 179 $'
LOG_PATTERN_DEFAULT = re.compile('^(\\d\\d\\d\\d-\\d\\d-\\d\\d \\d\\d:\\d\\d:\\d\\d,\\d\\d\\d) ([A-Z]{4,5}) *')

class LogParseException(Exception):
    __module__ = __name__


class LogParser:
    __module__ = __name__

    def parse(self, data):
        pass


class MessageParser(LogParser):
    __module__ = __name__

    def __init__(self, pattern_lookup=(), meta_keys_lookup=()):
        if pattern_lookup and meta_keys_lookup:
            repatts = []
            for patt in pattern_lookup:
                repatts.append(re.compile(patt, re.M))

            self.lookup = zip(repatts, meta_keys_lookup)
        else:
            self.lookup = None
        return

    def parse(self, data):
        """@todo unit testing
        """
        cat = 0
        if self.lookup is None:
            meta = UserDict()
            meta.category = 0
            return (data, meta)
        for (pattern, meta_keys) in self.lookup:
            match = pattern.match(data)
            if match:
                meta = UserDict()
                for (index, key) in enumerate(meta_keys):
                    meta[key] = match.groups()[index]

                meta.category = cat
                return (match.group(), meta)
            cat += 1

        raise LogParseException, 'Failed parsing message: %s' % data
        return


class HeaderParser(LogParser):
    __module__ = __name__

    def __init__(self, pattern=None, meta_keys=None):
        if pattern:
            self.pattern = re.compile(pattern)
        else:
            self.pattern = LOG_PATTERN_DEFAULT
        self.meta_keys = meta_keys or ('timestamp', 'level')

    def parse(self, line):
        """@todo unit testing
        """
        match = self.pattern.match(line)
        if match is None:
            raise LogParseException, 'Failed parsing header: %s' % line
        meta = {}
        for (index, key) in enumerate(self.meta_keys):
            meta[key] = match.groups()[index]

        return (
         match.group(), meta)


class ParserFactory(UserDict):
    __module__ = __name__

    def __call__(self, name):
        return self[name]


parserFactory = ParserFactory()
parserFactory['log.message'] = MessageParser()
parserFactory['log.header'] = HeaderParser()