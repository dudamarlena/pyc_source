# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/history.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 2853 bytes
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from six import with_metaclass
import datetime, os
__all__ = ('FileHistory', 'History', 'InMemoryHistory')

class History(with_metaclass(ABCMeta, object)):
    """History"""

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
    """InMemoryHistory"""

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
    """FileHistory"""

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