# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/validators/double_validator.py
# Compiled at: 2013-04-04 15:36:37
"""String validator for a double precision floating point number."""
from muntjac.data.validators.abstract_string_validator import AbstractStringValidator

class DoubleValidator(AbstractStringValidator):
    """String validator for a double precision floating point number. See
    L{AbstractStringValidator} for more information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string can be parsed as an
        double.

        @param errorMessage:
                   the message to display in case the value does not validate.
        """
        super(DoubleValidator, self).__init__(errorMessage)

    def isValidString(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False