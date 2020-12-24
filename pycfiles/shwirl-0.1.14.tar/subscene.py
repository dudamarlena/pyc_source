# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/scene/subscene.py
# Compiled at: 2016-11-03 01:40:19
from __future__ import division
from .node import Node

class SubScene(Node):
    """A Node subclass that serves as a marker and parent node for certain
    branches of the scenegraph.
    
    SubScene nodes are used as the top-level node for the internal scenes of
    a canvas and a view box.
    """

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)
        self.document = self