# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/type_caster.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3375 bytes
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.logging_helper import LoggingHelper
from pynestml.utils.messages import Messages

class TypeCaster(object):

    @staticmethod
    def do_magnitude_conversion_rhs_to_lhs(_rhs_type_symbol, _lhs_type_symbol, _containing_expression):
        """
        determine conversion factor from rhs to lhs, register it with the relevant expression, drop warning
        """
        _containing_expression.set_implicit_conversion_factor(UnitTypeSymbol.get_conversion_factor(_lhs_type_symbol.astropy_unit, _rhs_type_symbol.astropy_unit))
        _containing_expression.type = _lhs_type_symbol
        code, message = Messages.get_implicit_magnitude_conversion(_lhs_type_symbol, _rhs_type_symbol, _containing_expression.get_implicit_conversion_factor())
        Logger.log_message(code=code, message=message, error_position=_containing_expression.get_source_position(), log_level=LoggingLevel.WARNING)

    @staticmethod
    def try_to_recover_or_error(_lhs_type_symbol, _rhs_type_symbol, _containing_expression):
        if _rhs_type_symbol.is_castable_to(_lhs_type_symbol):
            if isinstance(_lhs_type_symbol, UnitTypeSymbol) and isinstance(_rhs_type_symbol, UnitTypeSymbol):
                conversion_factor = UnitTypeSymbol.get_conversion_factor(_lhs_type_symbol.astropy_unit, _rhs_type_symbol.astropy_unit)
                if not conversion_factor == 1.0:
                    TypeCaster.do_magnitude_conversion_rhs_to_lhs(_rhs_type_symbol, _lhs_type_symbol, _containing_expression)
                code, message = Messages.get_implicit_cast_rhs_to_lhs(_rhs_type_symbol.print_symbol(), _lhs_type_symbol.print_symbol())
                Logger.log_message(error_position=_containing_expression.get_source_position(), code=code, message=message, log_level=LoggingLevel.INFO)
        else:
            code, message = Messages.get_type_different_from_expected(_lhs_type_symbol, _rhs_type_symbol)
            Logger.log_message(error_position=_containing_expression.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)