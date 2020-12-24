# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/proxiedssl/__init__.py
# Compiled at: 2011-04-18 13:03:28
import logging

class NullHandler(logging.Handler):

    def emit(self, record):
        pass


logging.getLogger('proxiedssl').addHandler(NullHandler())