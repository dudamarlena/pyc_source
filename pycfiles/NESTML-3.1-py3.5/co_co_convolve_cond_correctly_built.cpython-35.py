# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_convolve_cond_correctly_built.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3111 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoConvolveCondCorrectlyBuilt(CoCo):
    __doc__ = '\n    This coco ensures that convolve and cond/curr sum are correctly build, i.e.,\n    that the first argument is the variable from the initial block and the second argument an input buffer.\n    Allowed:\n        function I_syn_exc pA =   convolve(g_ex, spikesExc) * ( V_bounded - E_ex )\n    Not allowed:\n        function I_syn_exc pA =   convolve(g_ex, g_ex) * ( V_bounded - E_ex )\n\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(ConvolveCheckerVisitor())


class ConvolveCheckerVisitor(ASTVisitor):
    __doc__ = '\n    Visits a function call and checks that if the function call is a cond_sum,cur_sum or convolve, the parameters\n    are correct.\n    '

    def visit_function_call(self, node):
        func_name = node.get_name()
        if func_name == 'convolve' or func_name == 'cond_sum' or func_name == 'curr_sum':
            symbol_var = node.get_scope().resolve_to_symbol(str(node.get_args()[0]), SymbolKind.VARIABLE)
            symbol_buffer = node.get_scope().resolve_to_symbol(str(node.get_args()[1]), SymbolKind.VARIABLE)
            if symbol_var is not None and not symbol_var.is_shape() and not symbol_var.is_init_values():
                code, message = Messages.get_first_arg_not_shape_or_equation(func_name)
                Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
            if symbol_buffer is not None and not symbol_buffer.is_input_buffer_spike():
                code, message = Messages.get_second_arg_not_a_buffer(func_name)
                Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)
            return