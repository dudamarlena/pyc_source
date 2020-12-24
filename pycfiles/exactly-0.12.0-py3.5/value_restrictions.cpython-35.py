# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/restrictions/value_restrictions.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 3917 bytes
from typing import Optional
from exactly_lib.common.report_rendering import text_docs
from exactly_lib.definitions import type_system
from exactly_lib.symbol.data.path_sdv import PathSdv
from exactly_lib.symbol.data.restrictions import error_messages
from exactly_lib.symbol.data.value_restriction import ErrorMessageWithFixTip, ValueRestriction
from exactly_lib.symbol.err_msg import error_messages as err_msg_for_any_type
from exactly_lib.symbol.sdv_structure import SymbolContainer
from exactly_lib.test_case_file_structure.path_relativity import PathRelativityVariants
from exactly_lib.test_case_file_structure.relativity_validation import is_satisfied_by
from exactly_lib.type_system.value_type import ValueType, TypeCategory
from exactly_lib.util.symbol_table import SymbolTable

class AnyDataTypeRestriction(ValueRestriction):
    __doc__ = '\n    A restriction that any data symbol value satisfies.\n    '

    def is_satisfied_by(self, symbol_table: SymbolTable, symbol_name: str, container: SymbolContainer) -> Optional[ErrorMessageWithFixTip]:
        if container.sdv.type_category is not TypeCategory.DATA:
            return err_msg_for_any_type.invalid_type_msg([type_system.DATA_TYPE_2_VALUE_TYPE[symbol_type] for symbol_type in type_system.DATA_TYPE_LIST_ORDER], symbol_name, container)


class StringRestriction(ValueRestriction):
    __doc__ = '\n    Restriction to string values.\n    '

    def is_satisfied_by(self, symbol_table: SymbolTable, symbol_name: str, container: SymbolContainer) -> Optional[ErrorMessageWithFixTip]:
        if container.sdv.value_type is not ValueType.STRING:
            return err_msg_for_any_type.invalid_type_msg([ValueType.STRING], symbol_name, container)


class PathRelativityRestriction(ValueRestriction):
    __doc__ = '\n    Restricts to `PathDdv` and `PathRelativityVariants`\n    '

    def __init__(self, accepted: PathRelativityVariants):
        self._accepted = accepted

    def is_satisfied_by(self, symbol_table: SymbolTable, symbol_name: str, container: SymbolContainer) -> Optional[ErrorMessageWithFixTip]:
        sdv = container.sdv
        if not isinstance(sdv, PathSdv):
            return err_msg_for_any_type.invalid_type_msg([ValueType.PATH], symbol_name, container)
        else:
            path = sdv.resolve(symbol_table)
            actual_relativity = path.relativity()
            satisfaction = is_satisfied_by(actual_relativity, self._accepted)
            if satisfaction:
                return
            msg = error_messages.unsatisfied_path_relativity(symbol_name, container, self._accepted, actual_relativity)
            return ErrorMessageWithFixTip(text_docs.single_pre_formatted_line_object(msg))

    @property
    def accepted(self) -> PathRelativityVariants:
        return self._accepted


class ValueRestrictionVisitor:

    def visit(self, x: ValueRestriction):
        if isinstance(x, AnyDataTypeRestriction):
            return self.visit_none(x)
        if isinstance(x, StringRestriction):
            return self.visit_string(x)
        if isinstance(x, PathRelativityRestriction):
            return self.visit_path_relativity(x)
        raise TypeError('%s is not an instance of %s' % (str(x), str(ValueRestriction)))

    def visit_none(self, x: AnyDataTypeRestriction):
        raise NotImplementedError()

    def visit_string(self, x: StringRestriction):
        raise NotImplementedError()

    def visit_path_relativity(self, x: PathRelativityRestriction):
        raise NotImplementedError()