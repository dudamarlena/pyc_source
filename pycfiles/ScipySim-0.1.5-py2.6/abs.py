# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/math/abs.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 9/12/2009

@author: brian
"""
from scipysim.actors import Siso

class Abs(Siso):
    """
    This actor takes a source and passes on the absolute value. 
    """

    def __init__(self, input_channel, output_channel):
        """
        Constructor for the absolute actor. 
        """
        super(Abs, self).__init__(input_channel=input_channel, output_channel=output_channel)

    def siso_process(self, obj):
        tag, value = obj['tag'], obj['value']
        if value < 0:
            value *= -1
        return {'tag': tag, 'value': value}