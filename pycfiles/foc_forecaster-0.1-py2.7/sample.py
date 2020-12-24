# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/forecaster/ai/sample.py
# Compiled at: 2012-02-08 04:49:36
"""
Created on 20. 12. 2011.

@author: kermit
"""
CRISIS_CLASS = 'crisis'
NORMAL_CLASS = 'normal'

class Sample(object):
    """
    A single pattern recognition sample
    """

    def __init__(self, features=None, classification=None, description=None):
        """
        Constructor
        """
        self.features = features
        self.classification = classification
        self.description = description