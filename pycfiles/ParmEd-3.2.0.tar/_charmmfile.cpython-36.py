# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/charmm/_charmmfile.py
# Compiled at: 2018-07-20 20:34:11
# Size of source mod 2**32: 5917 bytes
"""
Provides a class for reading CHARMM-style files. The key component to these
files is that the ! character is a comment character and everything after ! is
ignored.
"""
from parmed.utils.io import genopen

class CharmmFile(object):
    __doc__ = '\n    A CHARMM file that recognizes the "!" character as a \'comment\' token. It\n    can be iterated over and generally treated like a file object, but only\n    spits out strings that have been truncated at its first comment character.\n    \n    There is currently no way to recognize a ! as a _non_ comment character,\n    since allowing an escape character does not seem to be common practice and\n    would likely introduce negative performance implications.\n    '

    def __init__(self, fname, mode='r'):
        if mode not in ('r', 'w'):
            raise ValueError('Cannot open CharmmFile with mode "%s"' % mode)
        else:
            if mode == 'r':
                self.status = 'OLD'
            else:
                self.status = 'NEW'
        self._handle = genopen(fname, mode)
        self.closed = False
        self.line_number = 0
        self.comment = ''

    def __enter__(self):
        self._handle.__enter__()
        return self

    def __exit__(self, *args):
        if not self.closed:
            self.close()

    def tell(self):
        return self._handle.tell()

    def seek(self, value):
        return self._handle.seek(value)

    def write(self, *args, **kwargs):
        return (self._handle.write)(*args, **kwargs)

    def __iter__(self):
        parts = []
        for line in self._handle:
            try:
                idx = line.index('!')
            except ValueError:
                idx = None
                end = ''
                self.comment = ''
                if line.rstrip('\r\n').endswith('-'):
                    parts.append(line.rstrip('\r\n')[:-1])
                    continue
            else:
                end = '\n'
                self.comment = line[idx:].rstrip()
            parts.append(line[:idx] + end)
            yield ' '.join(parts)
            parts = []

    def readline(self):
        self.line_number += 1
        line = self._handle.readline()
        parts = []
        while line:
            if line.rstrip('\r\n').endswith('-'):
                parts.append(line.rstrip('\r\n')[:-1])
                line = self._handle.readline()
                self.line_number += 1
            else:
                parts.append(line)
                break

        line = ' '.join(parts)
        try:
            idx = line.index('!')
            self.comment = line[idx:].rstrip()
            end = '\n'
        except ValueError:
            idx = None
            end = ''
            self.comment = ''

        return line[:idx] + end

    def readlines(self):
        return [line for line in self]

    def read(self):
        return ''.join(self.readlines())

    def close(self):
        self._handle.close()
        self.closed = True

    def rewind(self):
        """ Return to the beginning of the file """
        self._handle.seek(0)

    def __del__(self):
        try:
            self.closed or self._handle.close()
        except AttributeError:
            pass


class CharmmStreamFile(object):
    __doc__ = '\n    The stream file is broken down into sections of commands delimited by the\n    strings:\n        read <section> <options>\n        ....\n        ....\n        end\n    This object provides iterators over those sections and a file-like API for\n    dealing with the text.\n\n    '

    def __init__(self, fname):
        self.lines = []
        self.comments = []
        with CharmmFile(fname, 'r') as (f):
            for line in f:
                self.lines.append(line)
                self.comments.append(f.comment)

        self.line_number = 0

    def __iter__(self):
        return iter(self.lines)

    def rewind(self):
        """ Return to the beginning of the file """
        self.line_number = 0

    def next_section(self):
        """
        Fast-forwards the file to the next CHARMM command section

        Returns
        -------
        name, data, comments : str, list of str, list of str
            name is the line defining the section that's being returned, whereas
            data is a list of all lines in the section, and comments is a list
            of all comments (same size as data) for all those lines

        Notes
        -----
        The line pointer will be set to the line defining the section
        """
        lines = []
        comments = []
        while self.line_number < len(self.lines):
            line = self.lines[self.line_number].strip()
            comment = self.comments[self.line_number].strip()
            if line[:4].lower() == 'read':
                title = line.strip()
                self.line_number += 1
                line = self.lines[self.line_number]
                while line and not line.strip().lower().startswith('end'):
                    lines.append(line)
                    comments.append(comment)
                    self.line_number += 1
                    line = self.lines[self.line_number]
                    comment = self.comments[self.line_number]

                if line[:3].upper() == 'END':
                    lines.append(line)
                    comments.append(comment)
                return (
                 title, lines, comments)
            self.line_number += 1

        return (None, None, None)

    def __del__(self):
        pass