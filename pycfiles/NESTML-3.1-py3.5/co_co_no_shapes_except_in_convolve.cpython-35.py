# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_no_shapes_except_in_convolve.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4899 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_ode_shape import ASTOdeShape
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoNoShapesExceptInConvolve(CoCo):
    __doc__ = '\n    This CoCo ensures that shape variables do not occur on the right hand side except in convolve/curr_sum and\n    cond_sum.\n    Allowed:\n        shape g_ex ...\n        function I_syn_exc pA = cond_sum(g_ex, spikeExc) * ( V_m - E_ex )\n\n    Not allowed\n        shape g_ex ...\n        function I_syn_exc pA = g_ex * ( V_m - E_ex )\n\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        shape_collector_visitor = ShapeCollectingVisitor()
        shape_names = shape_collector_visitor.collect_shapes(neuron=node)
        shape_usage_visitor = ShapeUsageVisitor(_shapes=shape_names)
        shape_usage_visitor.work_on(node)


class ShapeUsageVisitor(ASTVisitor):

    def __init__(self, _shapes=None):
        """
        Standard constructor.
        :param _shapes: a list of shapes.
        :type _shapes: list(ASTOdeShape)
        """
        super(ShapeUsageVisitor, self).__init__()
        self._ShapeUsageVisitor__shapes = _shapes
        self._ShapeUsageVisitor__neuron_node = None

    def work_on(self, neuron):
        self._ShapeUsageVisitor__neuron_node = neuron
        neuron.accept(self)

    def visit_variable(self, node):
        """
        Visits each shape and checks if it is used correctly.
        :param node: a single node.
        :type node: AST_
        """
        for shapeName in self._ShapeUsageVisitor__shapes:
            symbol = node.get_scope().resolve_to_symbol(shapeName, SymbolKind.VARIABLE)
            if symbol is None:
                code, message = Messages.get_no_variable_found(shapeName)
                Logger.log_message(neuron=self._ShapeUsageVisitor__neuron_node, code=code, message=message, log_level=LoggingLevel.ERROR)
                continue
                if not symbol.is_shape():
                    pass
            elif node.get_complete_name() == shapeName:
                pass
            parent = self._ShapeUsageVisitor__neuron_node.get_parent(node)
            if parent is not None:
                if isinstance(parent, ASTOdeShape):
                    pass
            else:
                grandparent = self._ShapeUsageVisitor__neuron_node.get_parent(parent)
                if grandparent is not None and isinstance(grandparent, ASTFunctionCall):
                    grandparent_func_name = grandparent.get_name()
                    if not grandparent_func_name == 'curr_sum':
                        if not grandparent_func_name == 'cond_sum':
                            if grandparent_func_name == 'convolve':
                                pass
                            continue
                            code, message = Messages.get_shape_outside_convolve(shapeName)
                            Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)


class ShapeCollectingVisitor(ASTVisitor):

    def __init__(self):
        super(ShapeCollectingVisitor, self).__init__()
        self.shape_names = None

    def collect_shapes(self, neuron):
        """
        Collects all shapes in the model.
        :param neuron: a single neuron instance
        :type neuron: ast_neuron
        :return: a list of shapes.
        :rtype: list(str)
        """
        self.shape_names = list()
        neuron.accept(self)
        return self.shape_names

    def visit_ode_shape(self, node):
        """
        Collects the shape.
        :param node: a single shape node.
        :type node: ASTOdeShape
        """
        self.shape_names.append(node.get_variable().get_name_of_lhs())