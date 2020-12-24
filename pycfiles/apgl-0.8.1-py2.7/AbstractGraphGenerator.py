# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/AbstractGraphGenerator.py
# Compiled at: 2010-12-24 07:08:54
"""
Created on 3 Jul 2009

@author: charanpal

An abstract base class which represents a graph generator. The graph generator
takes an existing empty graph and produces edges over it. 
"""
from apgl.util.Util import Util

class AbstractGraphGenerator(object):

    def generate(self, graph):
        Util.abstract()