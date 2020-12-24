# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/loggrok/log.py
# Compiled at: 2006-11-22 13:16:22
"""Log file containers.

$Id: log.py 391 2006-11-22 18:16:26Z djfroofy $
"""
from loggrok.parse import parserFactory, LogParseException
from xix.utils.xio import AggregateFileInput
from UserString import UserString
from cStringIO import StringIO
import glob, os.path, sys
__author__ = 'Drew Smathers'
__copyright__ = 'Copyright 2005, Drew Smathers'
__revision__ = '$Revision: 391 $'

class LogStreamException(Exception):
    """LogStream errors.
    """
    __module__ = __name__


class LogHeader(UserString):
    """Contains the header portion of a log entry.
    """
    __module__ = __name__

    def __init__(self, header=None, parser=None, meta=None):
        UserString.__init__(self, '')
        if meta is None:
            header_parser = parser or parserFactory('log.header')
            (self.data, meta) = header_parser.parse(header)
        else:
            self.data = header
        for (key, value) in meta.items():
            if hasattr(self, key):
                raise ValueError, 'Cannot set attribute %s of LogHeader' % key
            setattr(self, key, value)

        return


class LogEntry:
    """Contains a logical log entry - header, message
    """
    __module__ = __name__

    def __init__(self, header, message, parser=None):
        self.header = header
        message_parser = parser or parserFactory('log.message')
        (message, meta) = message_parser.parse(message)
        self.message = UserString(message)
        self.message.category = meta.category
        for (key, value) in meta.items():
            if hasattr(self.message, key):
                raise ValueError, 'Cannot set attribute %s of string' % key
            setattr(self.message, key, value)

    def __str__(self):
        return str(self.message)


class MalformedLogEntry(LogEntry):
    """Temporary container for header and message that could not parsed
    """
    __module__ = __name__

    def __init__(self, header, message):
        self.header = header
        self.message = message


class LogStream:
    """LogStream instances are created by passing a file descriptor
    or valid pathname to file to initializer.

    Using file descriptor:

    >>> from xix.utils.config import configFactory
    >>> fname = configFactory('loggrok-unittest.cfg').files.basicTest
    >>> fd = open(fname)
    >>> log = LogStream(fd)

    Using filename

    >>> log = LogStream(fname)

    """
    __module__ = __name__

    def __init__(self, logfile):
        if hasattr(logfile, 'readlines'):
            self.fd = logfile
        else:
            self.fd = open(logfile)
        self.messageParser = parserFactory('log.message')
        self.headerParser = parserFactory('log.header')
        self.__lastheader = None
        self.action = self.__donothing
        self.header = None
        self.message_buffer = StringIO()
        return

    def __donothing(self, entry):
        pass

    def __recvline(self, line):
        try:
            (header, meta) = self.headerParser.parse(line)
            if header:
                try:
                    entry = None
                    if self.header:
                        entry = self.__process_entry()
                    self.header = LogHeader(header, meta=meta)
                    self.message_buffer.write(line[len(self.header):])
                    return entry
                except LogParseException, lpe:
                    self.header = LogHeader(header)
                    self.message_buffer.truncate(0)
                    self.message_buffer.seek(0)
                    self.message_buffer.write(line[len(self.header):])
                    return

            else:
                self.message_buffer.write(line)
        except:
            self.message_buffer.write(line)

        return

    def __process_entry(self):
        message = self.message_buffer.getvalue()
        entry = LogEntry(self.header, message, parser=self.messageParser)
        self.action(entry)
        self.message_buffer.truncate(0)
        self.message_buffer.seek(0)
        return entry

    def readentries(self):
        """readentry iterator

        @todo unit testing
        """
        for line in self.fd:
            entry = self.__recvline(line)
            if entry:
                yield entry

        try:
            entry = self.__process_entry()
            if entry:
                yield entry
        except LogParseException:
            pass

    def __iter__(self):
        return self.readentries()

    def close(self):
        """
        >>> from xix.utils.config import configFactory
        >>> fname = configFactory('loggrok-unittest.cfg').files.basicTest
        >>> log = LogStream(fname)
        >>> log.close()
        """
        self.fd.close()


class RollingLogStream(LogStream):
    """Abstract RollingLog type.  Rolling logs effectively stitch 
    together a sequence of logs into one log object.
    """
    __module__ = __name__

    def __init__(self, files):
        LogStream.__init__(self, AggregateFileInput(files))


def _sortmatched(matched, pos):
    sortlist = []
    default = None
    for match in matched:
        try:
            index = int(match.split('.')[pos])
            sortlist.append((index, match))
        except Exception, e:
            default = match

    sortlist.sort()
    results = [ tup[1] for tup in sortlist ]
    if default:
        results = [
         default] + results
    results.reverse()
    return results


class RollingIndexLogStream(RollingLogStream):
    """Given a directory with rolled over logs, create a logstream based on these
    file.

    @todo unit testing 
    """
    __module__ = __name__

    def __init__(self, directory, basename, ext='log'):
        """
        @param directory: name of directory containing logs
        @param basename: basename of log files
        @param ext: ext of logfiles (default is 'log')
        """
        matched = glob.glob(os.path.join(directory, basename + '*.' + ext))
        matched = _sortmatched(matched, -2)
        RollingLogStream.__init__(self, matched)


class RollingIndexLogStream2(RollingLogStream):
    """For directories containing logs of the form (from newest to oldest):
    
    <basename>.log <basename>.log.1 <basename>.log.2
    """
    __module__ = __name__

    def __init__(self, directory, basename, ext='log'):
        matched = glob.glob(os.path.join(directory, basename + '.' + ext + '*'))
        matched = _sortmatched(matched, -1)
        RollingLogStream.__init__(self, matched)


class RollingDateLogStream(RollingLogStream):
    __module__ = __name__

    def __init__(self):
        raise NotImplementedError, 'RollingDateLog has not been implemented'


if __name__ == '__main__':
    pass