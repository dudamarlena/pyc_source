# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/data/value_restriction.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1909 bytes
from typing import Optional
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.symbol.sdv_structure import SymbolContainer
from exactly_lib.util.symbol_table import SymbolTable

class ErrorMessageWithFixTip(tuple):

    def __new__(cls, message: TextRenderer, how_to_fix: Optional[TextRenderer]=None):
        return tuple.__new__(cls, (message, how_to_fix))

    @property
    def message(self) -> TextRenderer:
        return self[0]

    @property
    def how_to_fix(self) -> Optional[TextRenderer]:
        return self[1]

    def __str__(self) -> str:
        from exactly_lib.util.simple_textstruct.file_printer_output import to_string
        return '%s{message=%s, how_to_fix=%s}' % (
         type(self),
         to_string.major_blocks(self.message.render_sequence()),
         '' if self.how_to_fix is None else to_string.major_blocks(self.how_to_fix.render()))


class ValueRestriction:
    __doc__ = '\n    A restriction on a resolved symbol value in the symbol table.\n\n    Since sometimes, the restriction on the resolved value can be checked\n    just by looking at the SDV - the checking method is given the SDV\n    instead of the resolved value.\n    '

    def is_satisfied_by(self, symbol_table: SymbolTable, symbol_name: str, container: SymbolContainer) -> Optional[ErrorMessageWithFixTip]:
        """
        :param symbol_table: A symbol table that contains all symbols that the checked value refer to.
        :param symbol_name: The name of the symbol that the restriction applies to
        :param container: The container of the value that the restriction applies to
        :rtype ErrorMessageWithFixTip
        :return: None if satisfied
        """
        raise NotImplementedError()