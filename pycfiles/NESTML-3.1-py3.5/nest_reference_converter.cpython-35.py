# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/codegeneration/nest_reference_converter.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 13987 bytes
from pynestml.codegeneration.gsl_names_converter import GSLNamesConverter
from pynestml.codegeneration.i_reference_converter import IReferenceConverter
from pynestml.codegeneration.nest_names_converter import NestNamesConverter
from pynestml.codegeneration.unit_converter import UnitConverter
from pynestml.meta_model.ast_arithmetic_operator import ASTArithmeticOperator
from pynestml.meta_model.ast_bit_operator import ASTBitOperator
from pynestml.meta_model.ast_comparison_operator import ASTComparisonOperator
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_logical_operator import ASTLogicalOperator
from pynestml.meta_model.ast_unary_operator import ASTUnaryOperator
from pynestml.meta_model.ast_variable import ASTVariable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.utils.ast_utils import ASTUtils
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages

class NESTReferenceConverter(IReferenceConverter):
    __doc__ = '\n    This concrete reference converter is used to transfer internal names to counter-pieces in NEST.\n    '

    def __init__(self, uses_gsl=False):
        """
        Standard constructor.
        :param uses_gsl: indicates whether GSL is used.
        :type uses_gsl: bool
        """
        self.uses_gsl = uses_gsl

    @classmethod
    def convert_binary_op(cls, binary_operator):
        """
        Converts a single binary operator to nest processable format.
        :param binary_operator: a single binary operator string.
        :type binary_operator: AST_
        :return: the corresponding nest representation
        :rtype: str
        """
        if isinstance(binary_operator, ASTArithmeticOperator):
            return cls.convert_arithmetic_operator(binary_operator)
        if isinstance(binary_operator, ASTBitOperator):
            return cls.convert_bit_operator(binary_operator)
        if isinstance(binary_operator, ASTComparisonOperator):
            return cls.convert_comparison_operator(binary_operator)
        if isinstance(binary_operator, ASTLogicalOperator):
            return cls.convert_logical_operator(binary_operator)
        raise RuntimeError('Cannot determine binary operator!')

    @classmethod
    def convert_function_call(cls, function_call, prefix=''):
        """
        Converts a single handed over function call to C++ NEST API syntax.

        Parameters
        ----------
        function_call : ASTFunctionCall
            The function call node to convert.
        prefix : str
            Optional string that will be prefixed to the function call. For example, to refer to a function call in the class "node", use a prefix equal to "node." or "node->".

            Predefined functions will not be prefixed.

        Returns
        -------
        s : str
            The function call string in C++ syntax.
        """
        function_name = function_call.get_name()
        if function_name == 'and':
            return '&&'
        if function_name == 'or':
            return '||'
        if function_name == PredefinedFunctions.TIME_RESOLUTION:
            return 'nest::Time::get_resolution().get_ms()'
        if function_name == PredefinedFunctions.TIME_STEPS:
            return 'nest::Time(nest::Time::ms((double) ({!s}))).get_steps()'
        if function_name == PredefinedFunctions.CLIP:
            return 'std::min({2!s}, std::max({1!s}, {0!s}))'
        if function_name == PredefinedFunctions.MAX:
            return 'std::max({!s}, {!s})'
        if function_name == PredefinedFunctions.MIN:
            return 'std::min({!s}, {!s})'
        if function_name == PredefinedFunctions.EXP:
            return 'std::exp({!s})'
        if function_name == PredefinedFunctions.LN:
            return 'std::log({!s})'
        if function_name == PredefinedFunctions.LOG10:
            return 'std::log10({!s})'
        if function_name == PredefinedFunctions.COSH:
            return 'std::cosh({!s})'
        if function_name == PredefinedFunctions.SINH:
            return 'std::sinh({!s})'
        if function_name == PredefinedFunctions.TANH:
            return 'std::tanh({!s})'
        if function_name == PredefinedFunctions.EXPM1:
            return 'numerics::expm1({!s})'
        if function_name == PredefinedFunctions.RANDOM_NORMAL:
            return '(({!s}) + ({!s}) * ' + prefix + 'normal_dev_( nest::kernel().rng_manager.get_rng( ' + prefix + 'get_thread() ) ))'
        if function_name == PredefinedFunctions.RANDOM_UNIFORM:
            return '(({!s}) + ({!s}) * nest::kernel().rng_manager.get_rng( ' + prefix + 'get_thread() )->drand())'
        if function_name == PredefinedFunctions.EMIT_SPIKE:
            return 'set_spiketime(nest::Time::step(origin.get_steps()+lag+1));\nnest::SpikeEvent se;\nnest::kernel().event_delivery_manager.send(*this, se, lag)'
        function_is_predefined = PredefinedFunctions.get_function(function_name)
        if function_is_predefined:
            prefix = ''
        if ASTUtils.needs_arguments(function_call):
            n_args = len(function_call.get_args())
            return prefix + function_name + '(' + ', '.join(['{!s}' for _ in range(n_args)]) + ')'
        return prefix + function_name + '()'

    def convert_name_reference(self, variable):
        """
        Converts a single variable to nest processable format.
        :param variable: a single variable.
        :type variable: ASTVariable
        :return: a nest processable format.
        :rtype: str
        """
        from pynestml.codegeneration.nest_printer import NestPrinter
        assert variable is not None and isinstance(variable, ASTVariable), '(PyNestML.CodeGeneration.NestReferenceConverter) No or wrong type of uses-gsl provided (%s)!' % type(variable)
        variable_name = NestNamesConverter.convert_to_cpp_name(variable.get_complete_name())
        if variable_name == PredefinedVariables.E_CONSTANT:
            return 'numerics::e'
        symbol = variable.get_scope().resolve_to_symbol(variable_name, SymbolKind.VARIABLE)
        if symbol is None:
            if PredefinedUnits.is_unit(variable.get_complete_name()):
                return str(UnitConverter.get_factor(PredefinedUnits.get_unit(variable.get_complete_name()).get_unit()))
            code, message = Messages.get_could_not_resolve(variable_name)
            Logger.log_message(log_level=LoggingLevel.ERROR, code=code, message=message, error_position=variable.get_source_position())
            return ''
        if symbol.is_local():
            return variable_name + ('[i]' if symbol.has_vector_parameter() else '')
        if symbol.is_buffer():
            if isinstance(symbol.get_type_symbol(), UnitTypeSymbol):
                units_conversion_factor = UnitConverter.get_factor(symbol.get_type_symbol().unit.unit)
            else:
                units_conversion_factor = 1
            s = ''
            if not units_conversion_factor == 1:
                s += '(' + str(units_conversion_factor) + ' * '
            s += NestPrinter.print_origin(symbol) + NestNamesConverter.buffer_value(symbol)
            if symbol.has_vector_parameter():
                s += '[i]'
            if not units_conversion_factor == 1:
                s += ')'
            return s
        if symbol.is_function:
            return 'get_' + variable_name + '()' + ('[i]' if symbol.has_vector_parameter() else '')
        if symbol.is_init_values():
            temp = NestPrinter.print_origin(symbol)
            if self.uses_gsl:
                temp += GSLNamesConverter.name(symbol)
            else:
                temp += NestNamesConverter.name(symbol)
            temp += '[i]' if symbol.has_vector_parameter() else ''
            return temp
        return NestPrinter.print_origin(symbol) + NestNamesConverter.name(symbol) + ('[i]' if symbol.has_vector_parameter() else '')

    @classmethod
    def convert_constant(cls, constant_name):
        """
        Converts a single handed over constant.
        :param constant_name: a constant as string.
        :type constant_name: str
        :return: the corresponding nest representation
        :rtype: str
        """
        if constant_name == 'inf':
            return 'std::numeric_limits<double_t>::infinity()'
        else:
            return constant_name

    @classmethod
    def convert_unary_op(cls, unary_operator):
        """
        Depending on the concretely used operator, a string is returned.
        :param unary_operator: a single operator.
        :type unary_operator:  ASTUnaryOperator
        :return: the same operator
        :rtype: str
        """
        if unary_operator.is_unary_plus:
            return '(+%s)'
        if unary_operator.is_unary_minus:
            return '(-%s)'
        if unary_operator.is_unary_tilde:
            return '(~%s)'
        raise RuntimeError('Cannot determine unary operator!', LoggingLevel.ERROR)

    @classmethod
    def convert_encapsulated(cls):
        """
        Converts the encapsulating parenthesis to NEST style.
        :return: a set of parenthesis
        :rtype: str
        """
        return '(%s)'

    @classmethod
    def convert_logical_not(cls):
        """
        Returns a representation of the logical not in NEST.
        :return: a string representation
        :rtype: str
        """
        return '(!%s)'

    @classmethod
    def convert_logical_operator(cls, op):
        """
        Prints a logical operator in NEST syntax.
        :param op: a logical operator object
        :type op: ASTLogicalOperator
        :return: a string representation
        :rtype: str
        """
        if op.is_logical_and:
            return '%s&&%s'
        if op.is_logical_or:
            return '%s||%s'
        raise RuntimeError('Cannot determine logical operator!', LoggingLevel.ERROR)

    @classmethod
    def convert_comparison_operator(cls, op):
        """
        Prints a logical operator in NEST syntax.
        :param op: a logical operator object
        :type op: ASTComparisonOperator
        :return: a string representation
        :rtype: str
        """
        if op.is_lt:
            return '%s<%s'
        if op.is_le:
            return '%s<=%s'
        if op.is_eq:
            return '%s==%s'
        if op.is_ne or op.is_ne2:
            return '%s!=%s'
        if op.is_ge:
            return '%s>=%s'
        if op.is_gt:
            return '%s>%s'
        raise RuntimeError('Cannot determine comparison operator!')

    @classmethod
    def convert_bit_operator(cls, op):
        """
        Prints a logical operator in NEST syntax.
        :param op: a logical operator object
        :type op: ASTBitOperator
        :return: a string representation
        :rtype: str
        """
        if op.is_bit_shift_left:
            return '%s<<%s'
        if op.is_bit_shift_right:
            return '%s>>%s'
        if op.is_bit_and:
            return '%s&%s'
        if op.is_bit_or:
            return '%s|%s'
        if op.is_bit_xor:
            return '%s^%s'
        raise RuntimeError('Cannot determine bit operator!')

    @classmethod
    def convert_arithmetic_operator(cls, op):
        """
        Prints a logical operator in NEST syntax.
        :param op: a logical operator object
        :type op: ASTArithmeticOperator
        :return: a string representation
        :rtype: str
        """
        if op.is_plus_op:
            return '%s + %s'
        if op.is_minus_op:
            return '%s - %s'
        if op.is_times_op:
            return '%s * %s'
        if op.is_div_op:
            return '%s / %s'
        if op.is_modulo_op:
            return '%s % %s'
        if op.is_pow_op:
            return 'pow(%s, %s)'
        raise RuntimeError('Cannot determine arithmetic operator!')

    @classmethod
    def convert_ternary_operator(cls):
        """
        Prints a ternary operator in NEST syntax.
        :return: a string representation
        :rtype: str
        """
        return '(%s) ? (%s) : (%s)'