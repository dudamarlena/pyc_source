# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/logic/lessthan.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on Feb 2, 2010

@author: Brian Thorne
"""
from scipysim.actors.logic import Compare

class LessThan(Compare):

    def compare(self, obj):
        return obj['value'] < self.threshold