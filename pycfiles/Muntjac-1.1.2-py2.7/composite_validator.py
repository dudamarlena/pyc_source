# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/validators/composite_validator.py
# Compiled at: 2013-04-04 15:36:37
"""Allows you to chain (compose) many validators to validate one field."""
from muntjac.data.validators.abstract_validator import AbstractValidator
from muntjac.data.validator import InvalidValueException

class CompositeValidator(AbstractValidator):
    """The C{CompositeValidator} allows you to chain (compose) many
    validators to validate one field. The contained validators may be required
    to all validate the value to validate or it may be enough that one
    contained validator validates the value. This behaviour is controlled by
    the modes C{AND} and C{OR}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    MODE_AND = 0
    MODE_OR = 1
    MODE_DEFAULT = MODE_AND

    def __init__(self, mode=None, errorMessage=None):
        """Constructs a composite validator in given mode.
        """
        self._mode = self.MODE_DEFAULT
        self._validators = list()
        if mode is None:
            super(CompositeValidator, self).__init__('')
        else:
            super(CompositeValidator, self).__init__(errorMessage)
            self.setMode(mode)
        return

    def validate(self, value):
        """Validates the given value.

        The value is valid, if:
          - C{MODE_AND}: All of the sub-validators are valid
          - C{MODE_OR}: Any of the sub-validators are valid

        If the value is invalid, validation error is thrown. If the error
        message is set (non-null), it is used. If the error message has not
        been set, the first error occurred is thrown.

        @param value:
                   the value to check.
        @raise InvalidValueException:
                    if the value is not valid.
        """
        if self._mode == self.MODE_AND:
            for validator in self._validators:
                validator.validate(value)

            return
        if self._mode == self.MODE_OR:
            first = None
            for v in self._validators:
                try:
                    v.validate(value)
                    return
                except InvalidValueException as e:
                    if first is None:
                        first = e

            if first is None:
                return
            em = self.getErrorMessage()
            if em is not None:
                raise InvalidValueException(em)
            else:
                raise first
        raise ValueError, 'The validator is in unsupported operation mode'
        return

    def isValid(self, value):
        """Checks the validity of the the given value. The value is valid, if:
          - C{MODE_AND}: All of the sub-validators are valid
          - C{MODE_OR}: Any of the sub-validators are valid

        @param value:
                   the value to check.
        """
        if self._mode == self.MODE_AND:
            for v in self._validators:
                if not v.isValid(value):
                    return False

            return True
        if self._mode == self.MODE_OR:
            for v in self._validators:
                if v.isValid(value):
                    return True

            return False
        raise ValueError, 'The valitor is in unsupported operation mode'

    def getMode(self):
        """Gets the mode of the validator.

        @return: Operation mode of the validator: C{MODE_AND} or C{MODE_OR}.
        """
        return self._mode

    def setMode(self, mode):
        """Sets the mode of the validator. The valid modes are:
          - C{MODE_AND} (default)
          - C{MODE_OR}

        @param mode:
                   the mode to set.
        """
        if mode != self.MODE_AND and mode != self.MODE_OR:
            raise ValueError, 'Mode ' + mode + ' unsupported'
        self._mode = mode

    def getErrorMessage(self):
        """Gets the error message for the composite validator. If the error
        message is C{None}, original error messages of the sub-validators are
        used instead.
        """
        if super(CompositeValidator, self).getErrorMessage() is not None:
            return super(CompositeValidator, self).getErrorMessage()
        else:
            return

    def addValidator(self, validator):
        """Adds validator to the interface.

        @param validator:
                   the Validator object which performs validation checks on
                   this set of data field values.
        """
        if validator is None:
            return
        else:
            self._validators.append(validator)
            return

    def removeValidator(self, validator):
        """Removes a validator from the composite.

        @param validator:
                   the Validator object which performs validation checks on
                   this set of data field values.
        """
        self._validators.remove(validator)

    def getSubValidators(self, validatorType):
        """Gets sub-validators by class.

        If the component contains directly or recursively (it contains another
        composite containing the validator) validators compatible with given
        type they are returned. This only applies to C{AND} mode composite
        validators.

        If the validator is in C{OR} mode or does not contain any validators
        of given type null is returned.

        @return: iterable of validators compatible with given type
                that must apply or null if none found.
        """
        if self._mode != self.MODE_AND:
            return
        else:
            found = set()
            for v in self._validators:
                if issubclass(v.__class__, validatorType):
                    found.add(v)
                if isinstance(v, CompositeValidator) and v.getMode() == self.MODE_AND:
                    c = v.getSubValidators(validatorType)
                    if c is not None:
                        for cc in c:
                            found.add(cc)

            if len(found) == 0:
                return
            return found