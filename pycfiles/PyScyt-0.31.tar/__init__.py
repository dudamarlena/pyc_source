# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/scxml/__init__.py
# Compiled at: 2011-02-26 13:09:55
import logging

class NullHandler(logging.Handler):

    def emit(self, record):
        pass


logger = logging.getLogger('pyscxml')
logger.addHandler(NullHandler())