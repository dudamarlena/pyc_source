# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_no_semantics_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1946 bytes
"""
Placeholder for rhs productions that are not implemented
"""
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.utils.error_strings import ErrorStrings
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import MessageCode
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTNoSemanticsVisitor(ASTVisitor):
    __doc__ = '\n    A visitor which indicates that there a no semantics for the given node.\n    '

    def visit_expression(self, node):
        """
        Visits a single rhs but does not execute any steps besides printing a message. This
        visitor indicates that no functionality has been implemented for this type of nodes.
        :param node: a single rhs
        :type node: ast_expression or ast_simple_expression
        """
        error_msg = ErrorStrings.message_no_semantics(self, str(node), node.get_source_position())
        node.type = ErrorTypeSymbol()
        Logger.log_message(message=error_msg, code=MessageCode.NO_SEMANTICS, error_position=node.get_source_position(), log_level=LoggingLevel.WARNING)