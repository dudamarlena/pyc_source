# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/processor.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 197 bytes


class Processor(object):

    def process(self, vertex, path):
        pass

    def undo(self, vertex, path):
        pass


class ProcessingResult:
    CONTINUE = 0
    GO_BACK = 1
    STOP = 2