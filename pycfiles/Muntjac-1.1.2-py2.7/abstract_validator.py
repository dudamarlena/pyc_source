# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/validators/abstract_validator.py
# Compiled at: 2013-04-04 15:36:37
"""Abstract IValidator implementation that provides a basic IValidator
implementation except the isValid method."""
from muntjac.data.validator import InvalidValueException, IValidator

class AbstractValidator(IValidator):
    """Abstract L{IValidator} implementation that provides a basic IValidator
    implementation except the L{isValid} method. Sub-classes need to implement
    the L{isValid} method.

    To include the value that failed validation in the exception message you
    can use "{0}" in the error message. This will be replaced with the failed
    value (converted to string using L{__str__}) or "null" if the value is
    None.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, errorMessage):
        """Constructs a validator with the given error message.

        @param errorMessage:
                   the message to be included in an L{InvalidValueException}
                   (with "{0}" replaced by the value that failed validation).
        """
        self._errorMessage = errorMessage

    def validate(self, value):
        if not self.isValid(value):
            message = self._errorMessage.replace('{0}', str(value))
            raise InvalidValueException(message)

    def getErrorMessage(self):
        """Returns the message to be included in the exception in case the
        value does not validate.

        @return: the error message provided in the constructor or using
                L{setErrorMessage}.
        """
        return self._errorMessage

    def setErrorMessage(self, errorMessage):
        """Sets the message to be included in the exception in case the value
        does not validate. The exception message is typically shown to the end
        user.

        @param errorMessage:
                   the error message. "{0}" is automatically replaced by the
                   value that did not validate.
        """
        self._errorMessage = errorMessage