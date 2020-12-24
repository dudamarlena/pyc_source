# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_user_defined_function_correctly_defined.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 9625 bytes
from pynestml.meta_model.ast_compound_stmt import ASTCompoundStmt
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.meta_model.ast_small_stmt import ASTSmallStmt
from pynestml.meta_model.ast_stmt import ASTStmt
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.utils.type_caster import TypeCaster

class CoCoUserDefinedFunctionCorrectlyDefined(CoCo):
    __doc__ = '\n    This coco ensures that all user defined functions, which are defined with a type, have a return statement\n    and the type of the return statement is consistent with the declaration.\n    Allowed:\n        function foo(...) bool:\n            return True\n        end\n    Not allowed:\n        function foo(...) bool:\n            return\n        end\n    Attributes:\n        __processedFunction (ast_function): A reference to the currently processed function.\n    '
    processed_function = None

    @classmethod
    def check_co_co(cls, _neuron=None):
        """
        Checks the coco for the handed over neuron.
        :param _neuron: a single neuron instance.
        :type _neuron: ASTNeuron
        """
        assert _neuron is not None and isinstance(_neuron, ASTNeuron), '(PyNestML.CoCo.FunctionCallsConsistent) No or wrong type of neuron provided (%s)!' % type(_neuron)
        cls._CoCoUserDefinedFunctionCorrectlyDefined__neuronName = _neuron.get_name()
        for userDefinedFunction in _neuron.get_functions():
            cls.processed_function = userDefinedFunction
            symbol = userDefinedFunction.get_scope().resolve_to_symbol(userDefinedFunction.get_name(), SymbolKind.FUNCTION)
            if symbol is not None and len(userDefinedFunction.get_block().get_stmts()) > 0:
                cls._CoCoUserDefinedFunctionCorrectlyDefined__check_return_recursively(symbol.get_return_type(), userDefinedFunction.get_block().get_stmts(), False)
            elif symbol is not None and userDefinedFunction.has_return_type() and not symbol.get_return_type().equals(PredefinedTypes.get_void_type()):
                code, message = Messages.get_no_return()
                Logger.log_message(neuron=_neuron, code=code, message=message, error_position=userDefinedFunction.get_source_position(), log_level=LoggingLevel.ERROR)

    @classmethod
    def __check_return_recursively(cls, type_symbol=None, stmts=None, ret_defined=False):
        """
        For a handed over statement, it checks if the statement is a return statement and if it is typed according
        to the handed over type symbol.
        :param type_symbol: a single type symbol
        :type type_symbol: type_symbol
        :param stmts: a list of statements, either simple or compound
        :type stmts: list(ASTSmallStmt,ASTCompoundStmt)
        :param ret_defined: indicates whether a ret has already beef defined after this block of stmt, thus is not
                    necessary. Implies that the return has been defined in the higher level block
        :type ret_defined: bool
        """
        last_statement = stmts[(len(stmts) - 1)]
        ret_defined = False or ret_defined
        if len(stmts) > 0 and isinstance(last_statement, ASTStmt) and last_statement.is_small_stmt() and last_statement.small_stmt.is_return_stmt():
            ret_defined = True
        for c_stmt in stmts:
            if c_stmt.is_small_stmt():
                stmt = c_stmt.small_stmt
            else:
                stmt = c_stmt.compound_stmt
            if isinstance(stmt, ASTSmallStmt) and stmt.is_return_stmt():
                pass
            if stmts.index(c_stmt) != len(stmts) - 1:
                code, message = Messages.get_not_last_statement('Return')
                Logger.log_message(error_position=stmt.get_source_position(), code=code, message=message, log_level=LoggingLevel.WARNING)
            if stmt.get_return_stmt().has_expression() and type_symbol is PredefinedTypes.get_void_type():
                code, message = Messages.get_type_different_from_expected(PredefinedTypes.get_void_type(), stmt.get_return_stmt().get_expression().type)
                Logger.log_message(error_position=stmt.get_source_position(), message=message, code=code, log_level=LoggingLevel.ERROR)
            if not stmt.get_return_stmt().has_expression() and not type_symbol.equals(PredefinedTypes.get_void_type()):
                code, message = Messages.get_type_different_from_expected(PredefinedTypes.get_void_type(), type_symbol)
                Logger.log_message(error_position=stmt.get_source_position(), message=message, code=code, log_level=LoggingLevel.ERROR)
            if stmt.get_return_stmt().has_expression():
                type_of_return = stmt.get_return_stmt().get_expression().type
                if isinstance(type_of_return, ErrorTypeSymbol):
                    code, message = Messages.get_type_could_not_be_derived(cls.processed_function.get_name())
                    Logger.log_message(error_position=stmt.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)
                elif not type_of_return.equals(type_symbol):
                    TypeCaster.try_to_recover_or_error(type_symbol, type_of_return, stmt.get_return_stmt().get_expression())
            else:
                if isinstance(stmt, ASTCompoundStmt):
                    if stmt.is_if_stmt():
                        cls._CoCoUserDefinedFunctionCorrectlyDefined__check_return_recursively(type_symbol, stmt.get_if_stmt().get_if_clause().get_block().get_stmts(), ret_defined)
                        for else_ifs in stmt.get_if_stmt().get_elif_clauses():
                            cls._CoCoUserDefinedFunctionCorrectlyDefined__check_return_recursively(type_symbol, else_ifs.get_block().get_stmt(), ret_defined)

                        if stmt.get_if_stmt().has_else_clause():
                            cls._CoCoUserDefinedFunctionCorrectlyDefined__check_return_recursively(type_symbol, stmt.get_if_stmt().get_else_clause().get_block().get_stmts(), ret_defined)
                    else:
                        if stmt.is_while_stmt():
                            cls._CoCoUserDefinedFunctionCorrectlyDefined__check_return_recursively(type_symbol, stmt.get_while_stmt().get_block().get_stmts(), ret_defined)
                        elif stmt.is_for_stmt():
                            cls._CoCoUserDefinedFunctionCorrectlyDefined__check_return_recursively(type_symbol, stmt.get_for_stmt().get_block().get_stmts(), ret_defined)
                elif not ret_defined and stmts.index(c_stmt) == len(stmts) - 1:
                    if not (isinstance(stmt, ASTSmallStmt) and stmt.is_return_stmt()):
                        code, message = Messages.get_no_return()
                        Logger.log_message(error_position=stmt.get_source_position(), log_level=LoggingLevel.ERROR, code=code, message=message)