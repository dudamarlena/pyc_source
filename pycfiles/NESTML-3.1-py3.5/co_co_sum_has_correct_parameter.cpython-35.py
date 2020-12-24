# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_sum_has_correct_parameter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2534 bytes
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoSumHasCorrectParameter(CoCo):
    __doc__ = '\n    This coco ensures that cur_sum,cond_sum and convolve get only simple variable references as inputs.\n    Not allowed:\n     V mV = convolve(g_in+g_ex,Buffer)\n    '

    @classmethod
    def check_co_co(cls, neuron):
        """
        Ensures the coco for the handed over neuron.
        :param neuron: a single neuron instance.
        :type neuron: ast_neuron
        """
        cls.neuronName = neuron.get_name()
        visitor = SumIsCorrectVisitor()
        neuron.accept(visitor)


class SumIsCorrectVisitor(ASTVisitor):
    __doc__ = '\n    This visitor ensures that sums/convolve are provided with a correct rhs.\n    '

    def visit_function_call(self, node):
        """
        Checks the coco on the current function call.
        :param node: a single function call.
        :type node: ast_function_call
        """
        f_name = node.get_name()
        if f_name == PredefinedFunctions.CURR_SUM or f_name == PredefinedFunctions.COND_SUM or f_name == PredefinedFunctions.CONVOLVE:
            for arg in node.get_args():
                if not isinstance(arg, ASTSimpleExpression) or not arg.is_variable():
                    code, message = Messages.get_not_a_variable(str(arg))
                    Logger.log_message(code=code, message=message, error_position=arg.get_source_position(), log_level=LoggingLevel.ERROR)