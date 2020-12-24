# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mathml/pmathml/mspace.py
# Compiled at: 2005-02-13 12:26:06
from element import Element, xml_mapping
import warnings

class MSpace(Element):

    def __init__(self, plotter, children):
        Element.__init__(self, plotter)
        assert len(children) == 0

    def update(self):
        self.width = self.getAttribute('width', recursive=0, default='0').asLength()
        height = self.getAttribute('height', recursive=0, default='0').asLength()
        depth = self.getAttribute('depth', recursive=0, default='0').asLength()
        self.height = height + depth
        self.axis = depth

    def draw(self):
        pass

    def embellished_p(self):
        return


xml_mapping['mspace'] = MSpace