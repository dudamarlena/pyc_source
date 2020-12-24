# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\jep_py\content.py
# Compiled at: 2016-01-01 11:01:34
# Size of source mod 2**32: 3752 bytes
"""Content tracking in response to ContentSync messages."""
import enum, logging, collections
_logger = logging.getLogger(__name__)

@enum.unique
class SynchronizationResult(enum.Enum):
    OutOfSync = 1
    Updated = 2


class NewlineMode:
    __doc__ = 'Representation of newlines in string as bit mask.'
    Unknown = 0
    N = 1
    R = 2
    RN = 4
    All = N | R | RN

    @classmethod
    def detect(cls, text):
        mode = cls.Unknown
        if text:
            chariter = iter(text)
            rpending = False
            try:
                while mode < cls.All:
                    c = next(chariter)
                    if c == '\n':
                        mode |= cls.N
                    elif c == '\r':
                        rpending = True
                        c = next(chariter)
                        rpending = False
                        if c == '\n':
                            mode |= cls.RN
                        else:
                            mode |= cls.R

            except StopIteration:
                if rpending:
                    mode |= cls.R

        return mode

    @classmethod
    def open_newline_mode(cls, mode):
        """Returns the open() newline mode that best corresponds to the given mode."""
        if mode == cls.N or mode == cls.Unknown:
            return
        if mode == cls.R:
            return '\r'
        if mode == cls.RN:
            return '\r\n'
        return ''


class ContentMonitor:
    __doc__ = 'Monitors the file contents based on synchronization requests from a frontend.\n\n    Current implementation uses straight forward Python strings, which involves multiple copies on insert:\n\n        * Copy to first slice\n        * Copy to second slice\n        * Copy of all slices and inserted text to destination string\n\n    If this becomes too much of a performance hit, it may be optimized, e.g. in form of an extension in C or\n    a data structure that directly represents string edit operations (btree, ...).\n    '

    def __init__(self):
        self._content_by_path = {}

    def __getitem__(self, filepath):
        """Returns the bytes know for file with given path."""
        return self._content_by_path.get(filepath, None)

    def synchronize(self, filepath, data, start, end=None):
        """Synchronizes content of given file."""
        content = self._content_by_path.get(filepath, '')
        length = len(content)
        end = end if end is not None else length
        if start < 0 or start > length or end < 0 or end > length or start > end:
            _logger.warning('Received content sync for %s, with current length %d. Start index %d or end index %d inconsistent.' % (filepath, length, start, end))
            return SynchronizationResult.OutOfSync
        if start < 0:
            start = 0
        if end < 0:
            end = 0
        _logger.debug('Updating file %s from index %d to %d with "%s".' % (filepath, start, end, data))
        before = content[0:start]
        after = content[end:]
        self._content_by_path[filepath] = ''.join([before, data, after])
        return SynchronizationResult.Updated