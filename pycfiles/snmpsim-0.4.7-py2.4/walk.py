# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim/record/walk.py
# Compiled at: 2018-12-30 10:46:50
from snmpsim.record import dump
from snmpsim.grammar import walk

class WalkRecord(dump.DumpRecord):
    __module__ = __name__
    grammar = walk.WalkGrammar()
    ext = 'snmpwalk'