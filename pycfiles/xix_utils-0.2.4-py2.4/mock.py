# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/mock.py
# Compiled at: 2006-04-15 16:24:49
"""Various things for mocking objects, data streams, etc.
"""
from warnings import warn
from StringIO import StringIO
__author__ = 'Drew Smathers'
__contact__ = 'drew.smathers@gmail.com'
__version__ = '$Revision$'[11:-2]

class File:
    r"""File mocker (only support some operations - do not
    expect this to be a full emulation of basic file type)

    Example Usage:

    >>> t = '''Hello
    ... World
    ... '''
    >>> fd = File(t)
    >>> for line in fd:
    ...    line
    ...
    'Hello\n'
    'World\n'
    ''
    """
    __module__ = __name__

    def __init__(self, text=None, mode='r'):
        warn('File implementation is not complete...')
        self.text = text or ''
        self.lines = []
        self.channel = StringIO()
        if mode == 'r':
            self.lines = [ line + '\n' for line in text.split('\n') ]
            self.lines[-1] = self.lines[(-1)][:-1]
        self.write = self.channel.write
        self.read = lambda : self.text
        self.readlines = lambda : self.lines
        self.__iter__ = lambda : iter(self.lines)