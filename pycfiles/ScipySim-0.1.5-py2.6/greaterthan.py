# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/logic/greaterthan.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on Feb 2, 2010

@author: Brian Thorne
"""
from scipysim.actors.logic import Compare

class GreaterThan(Compare):
    """
    This actor takes a source and passes on the value if it is equal or over 
    a specified threshold. Or boolean output is available (@see Compare).
    """

    def compare(self, obj):
        """Return true if value is above preset threshold"""
        return obj['value'] >= self.threshold