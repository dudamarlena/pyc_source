# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/generator/AbstractGraphGenerator.py
# Compiled at: 2010-12-24 07:08:54
__doc__ = '\nCreated on 3 Jul 2009\n\n@author: charanpal\n\nAn abstract base class which represents a graph generator. The graph generator\ntakes an existing empty graph and produces edges over it. \n'
from apgl.util.Util import Util

class AbstractGraphGenerator(object):

    def generate(self, graph):
        Util.abstract()