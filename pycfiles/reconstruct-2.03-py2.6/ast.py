# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\text\ast.py
# Compiled at: 2010-05-01 15:45:14
from construct import *

class AstNode(Container):

    def __init__(self, nodetype, **kw):
        Container.__init__(self)
        self.nodetype = nodetype
        for (k, v) in sorted(kw.iteritems()):
            setattr(self, k, v)

    def accept(self, visitor):
        return getattr(visitor, 'visit_%s' % (self.nodetype,))(self)


class AstTransformator(Adapter):

    def _decode(self, obj, context):
        return self.to_ast(obj, context)

    def _encode(self, obj, context):
        return self.to_cst(obj, context)