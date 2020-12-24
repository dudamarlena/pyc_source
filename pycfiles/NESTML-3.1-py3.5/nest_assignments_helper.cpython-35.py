# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/nest_assignments_helper.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5414 bytes
from pynestml.meta_model.ast_assignment import ASTAssignment
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import LoggingLevel, Logger

class NestAssignmentsHelper(object):
    __doc__ = '\n    This class contains several helper functions as used during printing of code.\n    '

    @classmethod
    def lhs_variable(cls, assignment):
        """
        Returns the corresponding symbol of the assignment.
        :param assignment: a single assignment.
        :type assignment: ASTAssignment.
        :return: a single variable symbol
        :rtype: variable_symbol
        """
        assert isinstance(assignment, ASTAssignment), '(PyNestML.CodeGeneration.Assignments) No or wrong type of assignment provided (%s)!' % type(assignment)
        symbol = assignment.get_scope().resolve_to_symbol(assignment.get_variable().get_complete_name(), SymbolKind.VARIABLE)
        if symbol is not None:
            return symbol
        else:
            Logger.log_message(message='No symbol could be resolved!', log_level=LoggingLevel.ERROR)
            return

    @classmethod
    def print_assignments_operation(cls, assignment):
        """
        Returns a nest processable format of the assignment operation.
        :param assignment: a single assignment
        :type assignment: ASTAssignment
        :return: the corresponding string representation
        :rtype: str
        """
        assert isinstance(assignment, ASTAssignment), '(PyNestML.CodeGeneration.Assignments) No or wrong type of assignment provided (%s)!' % type(assignment)
        if assignment.is_compound_sum:
            return '+='
        else:
            if assignment.is_compound_minus:
                return '-='
            if assignment.is_compound_product:
                return '*='
            if assignment.is_compound_quotient:
                return '/='
            return '='

    @classmethod
    def is_vectorized_assignment(cls, assignment):
        """
        Indicates whether the handed over assignment is vectorized, i.e., an assignment of vectors.
        :param assignment: a single assignment.
        :type assignment: ASTAssignment
        :return: True if vectorized, otherwise False.
        :rtype: bool
        """
        from pynestml.symbols.symbol import SymbolKind
        assert isinstance(assignment, ASTAssignment), '(PyNestML.CodeGeneration.Assignments) No or wrong type of assignment provided (%s)!' % type(assignment)
        symbol = assignment.get_scope().resolve_to_symbol(assignment.get_variable().get_complete_name(), SymbolKind.VARIABLE)
        if symbol is not None:
            if symbol.has_vector_parameter():
                return True
            else:
                for var in assignment.get_expression().get_variables():
                    symbol = var.get_scope().resolve_to_symbol(var.get_complete_name(), SymbolKind.VARIABLE)
                    if symbol is not None and symbol.has_vector_parameter():
                        return True

                return False
        else:
            Logger.log_message(message='No symbol could be resolved!', log_level=LoggingLevel.ERROR)
            return False

    @classmethod
    def print_size_parameter(cls, assignment):
        """
        Prints in a nest processable format the size parameter of the assignment.
        :param assignment: a single assignment
        :type assignment: ASTAssignment
        :return: the corresponding size parameter
        :rtype: str
        """
        from pynestml.symbols.symbol import SymbolKind
        assert assignment is not None and isinstance(assignment, ASTAssignment), '(PyNestML.CodeGeneration.Assignments) No or wrong type of assignment provided (%s)!' % type(assignment)
        vector_variable = None
        for variable in assignment.get_expression().get_variables():
            symbol = variable.get_scope().resolve_to_symbol(variable.get_complete_name(), SymbolKind.VARIABLE)
            if symbol is not None and symbol.has_vector_parameter():
                vector_variable = symbol
                break

        if vector_variable is None:
            vector_variable = assignment.get_scope().resolve_to_symbol(assignment.get_variable().get_complete_name(), SymbolKind.VARIABLE)
        return vector_variable.get_vector_parameter()