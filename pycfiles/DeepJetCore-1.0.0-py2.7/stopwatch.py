# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/stopwatch.py
# Compiled at: 2018-07-12 08:05:01
"""
Created on 4 Mar 2017

@author: jkiesele
"""
import time as tm

class stopwatch(object):
    """
    classdocs
    """

    def __init__(self):
        """
        Constructor
        """
        self.start = tm.time()

    def getAndReset(self):
        nowT = tm.time()
        ret = nowT - self.start
        self.start = tm.time()
        return ret

    def getAndContinue(self):
        nowT = tm.time()
        return nowT - self.start