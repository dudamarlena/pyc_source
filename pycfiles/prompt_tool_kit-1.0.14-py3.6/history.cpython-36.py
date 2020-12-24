# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/history.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 2853 bytes
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
import datetime, os
__all__ = ('FileHistory', 'History', 'InMemoryHistory')

class History(with_metaclass(ABCMeta, object)):
    __doc__ = '\n    Base ``History`` interface.\n    '

    @abstractmethod
    def append(self, string):
        """ Append string to history. """
        pass

    @abstractmethod
    def __getitem__(self, key):
        """ Return one item of the history. It should be accessible like a `list`. """
        pass

    @abstractmethod
    def __iter__(self):
        """ Iterate through all the items of the history. Cronologically. """
        pass

    @abstractmethod
    def __len__(self):
        """ Return the length of the history.  """
        pass

    def __bool__(self):
        """
        Never evaluate to False, even when the history is empty.
        (Python calls __len__ if __bool__ is not implemented.)
        This is mainly to allow lazy evaluation::

            x = history or InMemoryHistory()
        """
        return True

    __nonzero__ = __bool__


class InMemoryHistory(History):
    __doc__ = '\n    :class:`.History` class that keeps a list of all strings in memory.\n    '

    def __init__(self):
        self.strings = []

    def append(self, string):
        self.strings.append(string)

    def __getitem__(self, key):
        return self.strings[key]

    def __iter__(self):
        return iter(self.strings)

    def __len__(self):
        return len(self.strings)


class FileHistory(History):
    __doc__ = '\n    :class:`.History` class that stores all strings in a file.\n    '

    def __init__(self, filename):
        self.strings = []
        self.filename = filename
        self._load()

    def _load(self):
        lines = []

        def add():
            if lines:
                string = ''.join(lines)[:-1]
                self.strings.append(string)

        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as (f):
                for line in f:
                    line = line.decode('utf-8')
                    if line.startswith('+'):
                        lines.append(line[1:])
                    else:
                        add()
                        lines = []

                add()

    def append(self, string):
        self.strings.append(string)
        with open(self.filename, 'ab') as (f):

            def write(t):
                f.write(t.encode('utf-8'))

            write('\n# %s\n' % datetime.datetime.now())
            for line in string.split('\n'):
                write('+%s\n' % line)

    def __getitem__(self, key):
        return self.strings[key]

    def __iter__(self):
        return iter(self.strings)

    def __len__(self):
        return len(self.strings)