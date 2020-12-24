# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/guispinbox.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 8939 bytes
"""
General-purpose :mod:`QAbstractSpinBox` widget subclasses.
"""
from PySide2.QtGui import QValidator
from PySide2.QtWidgets import QDoubleSpinBox
from betse.util.type.numeric import floats
from betse.util.type.text import regexes
from betse.util.type.types import type_check
from betsee.util.widget.mixin.guiwdgeditmixin import QBetseeEditWidgetMixin

class QBetseeDoubleSpinBox(QBetseeEditWidgetMixin, QDoubleSpinBox):
    __doc__ = '\n    General-purpose :mod:`QDoubleSpinBox` widget optimized for contextual\n    display and validation of floating point numbers.\n\n    This application-specific widget augments the stock :class:`QDoubleSpinBox`\n    widget with additional support for scientific notation, permitting *only*\n    characters permissible in both:\n\n    * Decimal notation (e.g., digits, signs, and the radix point).\n    * Scientific notation (e.g., digits, signs, the radix point, and the letter\n      "e" in both capitalized and uncapitalized variants).\n\n    Attributes\n    ----------\n    _validator : QBetseeDoubleValidator\n        Application-specific validator validating floating point numbers in\n        both decimal and scientific notation.\n\n    See Also\n    ----------\n    https://jdreaver.com/posts/2014-07-28-scientific-notation-spin-box-pyside.html\n        Blog post partially inspiring this implementation.\n    '
    SINGLE_STEP_DEFAULT = 1.0

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._validator = QBetseeDoubleValidator()
        self.setMaximum(floats.FLOAT_MAX)

    def validate(self, text: str, char_index: int) -> QValidator.State:
        return self._validator.validate(text, char_index)

    def fixup(self, text: str) -> str:
        return self._validator.fixup(text)

    def valueFromText(self, text: str) -> float:
        """
        Floating point number converted from the passed human-readable string.
        """
        return float(text)

    def textFromValue(self, number: float) -> str:
        """
        Human-readable string converted from the passed floating point number.
        """
        return floats.to_str(number)


class QBetseeDoubleValidator(QValidator):
    __doc__ = '\n    Validator enabling the :mod:`QBetseeDoubleSpinBox` widget to input and\n    display floating point numbers in both decimal and scientific notation.\n\n    This application-specific widget augments the stock\n    :class:`QDoubleValidator` validator with additional support for scientific\n    notation.\n\n    Attributes\n    ----------\n    _float_regex : RegexCompiledType\n        Compiled regular expression matching a floating point number.\n\n    See Also\n    ----------\n    https://jdreaver.com/posts/2014-07-28-scientific-notation-spin-box-pyside.html\n        Blog post partially inspiring this implementation.\n    '
    _CHARS_NONDIGIT = {
     'e', 'E', '.', '-', '+'}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._float_regex = floats.get_float_regex()

    @type_check
    def validate(self, text: str, char_index: int) -> QValidator.State:
        """
        Validate the passed input text at the passed character index of this
        text to be a valid floating point number or not.

        Specifically, this method returns:

        * :attr:`State.Acceptable` if this text is guaranteed to be an valid
          floating point number.
        * :attr:`State.Intermediate` if this text is currently an invalid
          floating point number but could conceivably be transformed into a
          valid floating point number by subsequent input of one or more
          printable characters.
        * :attr:`State.Invalid` if this text is guaranteed to be an invalid
          floating point number regardless of subsequently input printable
          characters.

        Parameters
        ----------
        text : str
            Input text to be validated.
        char_index : int
            0-based character index of the input cursor in this text.

        Returns
        ----------
        State
            Whether this text is a valid floating point number or not.
        """
        if floats.is_float_str(text):
            return QValidator.State.Acceptable
        else:
            if text == '' or text[(char_index - 1)] in self._CHARS_NONDIGIT:
                return QValidator.State.Intermediate
            return QValidator.State.Invalid

    @type_check
    def fixup(self, text: str) -> str:
        """
        Input guaranteed to be in either the :attr:`State.Intermediate` or
        :attr:`State.Valid` states, sanitized from the passed input guaranteed
        to be in the :attr:`State.Invalid` state.

        Specifically, this function returns:

        * The first substring in this invalid input matching a floating point
          number in either decimal or scientific notation if this input
          contains such a substring. In this case, the returned string is
          guaranteeably valid.
        * The empty string otherwise. In this case, the returned string is
          *not* guaranteeably valid and hence is merely intermediate.

        In either case, the returned string is guaranteed *not* to be invalid.
        Of course, this does *not* guarantee this string to be valid.

        Parameters
        ----------
        text : str
            Invalid input text to be munged.

        Returns
        ----------
        str
            Intermediate or valid input munged from this invalid input.
        """
        return regexes.get_match_full_first_if_any(text=text,
          regex=(self._float_regex)) or ''