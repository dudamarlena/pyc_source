# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_correct_order_in_equation.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2113 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoCorrectOrderInEquation(CoCo):
    __doc__ = "\n    This coco ensures that whenever a ode-equation is assigned to a variable, it have a differential order \n    of at leas one.\n    Allowed:\n        equations:\n            V_m' = ...\n        end\n    Not allowed:\n        equations:\n            V_m = ...\n        end  \n    "

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(OrderOfEquationVisitor())


class OrderOfEquationVisitor(ASTVisitor):
    __doc__ = '\n    This visitor checks that all differential equations have a differential order.\n    '

    def visit_ode_equation(self, node):
        """
        Checks the coco.
        :param node: A single ode equation.
        :type node: ast_ode_equation
        """
        if node.get_lhs().get_differential_order() == 0:
            code, message = Messages.get_order_not_declared(node.get_lhs().get_name())
            Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)