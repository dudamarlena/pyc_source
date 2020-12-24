# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_function_have_rhs.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1940 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoFunctionHaveRhs(CoCo):
    __doc__ = '\n    This coco ensures that all function declarations, e.g., function V_rest mV = V_m - 55mV, have a rhs.\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(FunctionRhsVisitor())


class FunctionRhsVisitor(ASTVisitor):
    __doc__ = '\n    This visitor ensures that everything declared as function has a rhs.\n    '

    def visit_declaration(self, node):
        """
        Checks if the coco applies.
        :param node: a single declaration.
        :type node: ASTDeclaration.
        """
        if node.is_function and not node.has_expression():
            code, message = Messages.get_no_rhs(node.get_variables()[0].get_name())
            Logger.log_message(error_position=node.get_source_position(), log_level=LoggingLevel.ERROR, code=code, message=message)