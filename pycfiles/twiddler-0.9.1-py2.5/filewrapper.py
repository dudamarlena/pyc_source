# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/input/filewrapper.py
# Compiled at: 2008-07-24 14:48:01
import os
from twiddler.input.default import Default
from twiddler.interfaces import IInput
from zope.interface import implements

class FileWrapper:
    implements(IInput)

    def __init__(self, input=Default, prefix=None, encoding=None):
        self.input = input
        self.encoding = encoding
        if prefix is None:
            self.prefix = os.getcwd()
        elif os.path.isfile(prefix):
            self.prefix = os.path.split(prefix)[0]
        else:
            self.prefix = prefix
        return

    def __call__(self, source, indexes):
        source = open(os.path.abspath(os.path.join(self.prefix, source))).read()
        if self.encoding is not None:
            source = source.decode(self.encoding)
        return self.input(source, indexes)