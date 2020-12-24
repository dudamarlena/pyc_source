# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\batch.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 4560 bytes
__doc__ = 'Batch\n\nBatches\n=======\n\nBatches allow you to optimize the number of gl calls using pyglets batch\n\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import pyglet
from pyglet import gl
from cocos.cocosnode import CocosNode
__all__ = [
 'BatchNode', 'BatchableNode']

def ensure_batcheable(node):
    if not isinstance(node, BatchableNode):
        raise Exception('Children node of a batch must be of class BatchableNode')
    for c in node.get_children():
        ensure_batcheable(c)


class BatchNode(CocosNode):

    def __init__(self):
        super(BatchNode, self).__init__()
        self.batch = pyglet.graphics.Batch()
        self.groups = {}

    def add(self, child, z=0, name=None):
        ensure_batcheable(child)
        child.set_batch(self.batch, self.groups, z)
        super(BatchNode, self).add(child, z, name)

    def visit(self):
        """ All children are placed in to self.batch, so nothing to visit """
        if not self.visible:
            return
        gl.glPushMatrix()
        self.transform()
        self.batch.draw()
        gl.glPopMatrix()

    def remove(self, child):
        if isinstance(child, str):
            child_node = self.get(child)
        else:
            child_node = child
        child_node.set_batch(None)
        super(BatchNode, self).remove(child)

    def draw(self):
        pass


class BatchableNode(CocosNode):

    def add(self, child, z=0, name=None):
        batchnode = self.get_ancestor(BatchNode)
        if not batchnode:
            super(BatchableNode, self).add(child, z, name)
            return
        ensure_batcheable(child)
        super(BatchableNode, self).add(child, z, name)
        child.set_batch(self.batch, batchnode.groups, z)

    def remove(self, child):
        if isinstance(child, str):
            child_node = self.get(child)
        else:
            child_node = child
        child_node.set_batch(None)
        super(BatchableNode, self).remove(child)

    def set_batch(self, batch, groups=None, z=0):
        self.batch = batch
        if batch is None:
            self.group = None
        else:
            group = groups.get(z)
            if group is None:
                group = pyglet.graphics.OrderedGroup(z)
                groups[z] = group
            self.group = group
        for childZ, child in self.children:
            child.set_batch(self.batch, groups, z + childZ)