# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\drewtils\parsers.py
# Compiled at: 2017-12-04 22:05:21
# Size of source mod 2**32: 4482 bytes
"""Classes for simple file processing"""
import re
__all__ = [
 'KeywordParser', 'PatternReader']

class _TextProcessor(object):
    __doc__ = 'Parent class for text processors.'

    def __init__(self, path):
        self.path = path
        self._stream = None
        self.line = ''

    def __enter__(self):
        self._stream = open(self.path, 'r')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stream.close()
        self._stream = None

    def _step(self):
        self.line = self._stream.readline()
        return self.line

    def _match(self, regexp):
        return re.match(regexp, self.line)

    def _search(self, regexp):
        return re.search(regexp, self.line)

    def _checkOpen(self):
        if self._stream is None:
            raise IOError('Parse must be used in a with <> as <>: block')

    def seekToTop(self):
        """Reset the file pointer to the start of the file."""
        self._stream.seek(0)


class KeywordParser(_TextProcessor):
    __doc__ = "\n    Class for parsing a file for chunks separated by various keywords.\n\n    Parameters\n    ----------\n    filePath: str\n        Object to be read. Any object with ``read`` and ``close`` methods\n    keys: Iterable\n        List of keywords/phrases that will indicate the start of a chunk\n    separators: Iterable or None\n        List of additional phrases that can separate two chunks.\n        If not given, will default to empty line ``'\\n'``.\n    eof: str\n        String to indicate the end of the file\n\n    Attributes\n    ----------\n    line: str\n        Most recently read line\n    "

    def __init__(self, filePath, keys, separators=None, eof=''):
        _TextProcessor.__init__(self, filePath)
        self._startMatch = self._makeMatchFromIterable(keys)
        separators = set(keys).union(set(separators) if separators else set(['\n']))
        self._endMatch = self._makeMatchFromIterable(separators)
        self._end = eof

    def yieldChunks(self):
        """
        Return each chunk of text as a generator.

        Yields
        ------
        list
            The next chunk in the file.
        """
        self._checkOpen()
        chunk = []
        while self._step() != self._end:
            if self._match(self._endMatch):
                if chunk:
                    yield chunk
                chunk = [self.line] if self._match(self._startMatch) else []
            elif chunk:
                chunk.append(self.line)

        if chunk:
            yield chunk

    def parse(self):
        """
        Parse the file and return a list of keyword blocks.

        Returns
        -------
        list
            List of key word argument chunks.

        """
        return list(self.yieldChunks())

    @staticmethod
    def _makeMatchFromIterable(args):
        return re.compile('|'.join([str(arg) for arg in args]))


class PatternReader(_TextProcessor):
    __doc__ = '\n    Class that can read over a file looking for patterns.\n\n    Parameters\n    ----------\n    filePath: str\n        path to the file that is to be read\n\n    Attributes\n    ----------\n    line: str\n        Most recently read line\n    match: regular expression match or None\n        Match from the most recently read line\n    '

    def __init__(self, filePath):
        _TextProcessor.__init__(self, filePath)
        self.match = None

    def searchFor(self, pattern):
        """
        Return true if the pattern is found.

        Parameters
        ----------
        pattern: str or compiled regular expression

        Returns
        -------
        bool: True if the pattern was found

        """
        self._checkOpen()
        regexp = re.compile(pattern) if isinstance(pattern, str) else pattern
        while self._step():
            self.match = self._search(regexp)
            if self.match:
                return True

        return False

    def yieldMatches(self, pattern):
        """
        Generator that returns all match groups that match pattern.

        Parameters
        ----------
        pattern: str or compiled regular expression
            Seek through the file and yield all match groups for lines that
            contain this patten.

        Yields
        ------
        sequential match groups

        """
        while self.searchFor(pattern):
            yield self.match