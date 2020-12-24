# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/final_vertex.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 148 bytes
from .vertex import Vertex, VertexCategory

class FinalVertex(Vertex):

    def __init__(self):
        Vertex.__init__(self, VertexCategory.FINAL)