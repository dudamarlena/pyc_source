# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/scene/subscene.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 552 bytes
from __future__ import division
from .node import Node

class SubScene(Node):
    __doc__ = 'A Node subclass that serves as a marker and parent node for certain\n    branches of the scenegraph.\n    \n    SubScene nodes are used as the top-level node for the internal scenes of\n    a canvas and a view box.\n    '

    def __init__(self, **kwargs):
        Node.__init__(self, **kwargs)
        self.document = self