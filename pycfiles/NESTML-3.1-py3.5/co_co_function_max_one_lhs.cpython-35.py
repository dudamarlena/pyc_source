# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_function_max_one_lhs.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2106 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoFunctionMaxOneLhs(CoCo):
    __doc__ = '\n    This coco ensures that whenever a function (aka alias) is declared, only one left-hand side is present.\n    Allowed:\n        function V_rest mV = V_m - 55mV\n    Not allowed:\n        function V_reset,V_rest mV = V_m - 55mV\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(FunctionMaxOneLhs())


class FunctionMaxOneLhs(ASTVisitor):
    __doc__ = '\n    This visitor ensures that every function has exactly one lhs.\n    '

    def visit_declaration(self, node):
        """
        Checks the coco.
        :param node: a single declaration.
        :type node: ast_declaration
        """
        if node.is_function and len(node.get_variables()) > 1:
            code, message = Messages.get_several_lhs(list(var.get_name() for var in node.get_variables()))
            Logger.log_message(error_position=node.get_source_position(), log_level=LoggingLevel.ERROR, code=code, message=message)