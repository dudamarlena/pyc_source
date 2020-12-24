# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/library/Operators.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2332 bytes
from ..Node import Node

class UniOpNode(Node):
    __doc__ = 'Generic node for performing any operation like Out = In.fn()'

    def __init__(self, name, fn):
        self.fn = fn
        Node.__init__(self, name, terminals={'In':{'io': 'in'}, 
         'Out':{'io':'out', 
          'bypass':'In'}})

    def process(self, **args):
        return {'Out': getattr(args['In'], self.fn)()}


class BinOpNode(Node):
    __doc__ = 'Generic node for performing any operation like A.fn(B)'

    def __init__(self, name, fn):
        self.fn = fn
        Node.__init__(self, name, terminals={'A':{'io': 'in'}, 
         'B':{'io': 'in'}, 
         'Out':{'io':'out', 
          'bypass':'A'}})

    def process(self, **args):
        if isinstance(self.fn, tuple):
            for name in self.fn:
                try:
                    fn = getattr(args['A'], name)
                    break
                except AttributeError:
                    pass

        else:
            fn = getattr(args['A'], self.fn)
        out = fn(args['B'])
        if out is NotImplemented:
            raise Exception('Operation %s not implemented between %s and %s' % (fn, str(type(args['A'])), str(type(args['B']))))
        return {'Out': out}


class AbsNode(UniOpNode):
    __doc__ = 'Returns abs(Inp). Does not check input types.'
    nodeName = 'Abs'

    def __init__(self, name):
        UniOpNode.__init__(self, name, '__abs__')


class AddNode(BinOpNode):
    __doc__ = 'Returns A + B. Does not check input types.'
    nodeName = 'Add'

    def __init__(self, name):
        BinOpNode.__init__(self, name, '__add__')


class SubtractNode(BinOpNode):
    __doc__ = 'Returns A - B. Does not check input types.'
    nodeName = 'Subtract'

    def __init__(self, name):
        BinOpNode.__init__(self, name, '__sub__')


class MultiplyNode(BinOpNode):
    __doc__ = 'Returns A * B. Does not check input types.'
    nodeName = 'Multiply'

    def __init__(self, name):
        BinOpNode.__init__(self, name, '__mul__')


class DivideNode(BinOpNode):
    __doc__ = 'Returns A / B. Does not check input types.'
    nodeName = 'Divide'

    def __init__(self, name):
        BinOpNode.__init__(self, name, ('__truediv__', '__div__'))