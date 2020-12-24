# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_correct_numerator_of_unit.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2181 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoCorrectNumeratorOfUnit(CoCo):
    __doc__ = '\n    This coco ensures that all units which consist of a dividend and divisor, where the numerator is a numeric\n    value, have 1 as the numerator. \n    Allowed:\n        V_m 1/mV = ...\n    Not allowed:\n        V_m 2/mV = ...\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(NumericNumeratorVisitor())


class NumericNumeratorVisitor(ASTVisitor):
    __doc__ = '\n    Visits a numeric numerator and checks if the value is 1.\n    '

    def visit_unit_type(self, node):
        """
        Check if the coco applies,
        :param node: a single unit type object.
        :type node: ast_unit_type
        """
        if node.is_div and isinstance(node.lhs, int) and node.lhs != 1:
            from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
            node.set_type_symbol(ErrorTypeSymbol())
            code, message = Messages.get_wrong_numerator(str(node))
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)