# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/validatable.py
# Compiled at: 2013-04-04 15:36:37
"""Interface for validatable objects."""

class IValidatable(object):
    """Interface for validatable objects. Defines methods to verify if the
    object's value is valid or not, and to add, remove and list registered
    validators of the object.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    @see: L{IValidator}
    """

    def addValidator(self, validator):
        """Adds a new validator for this object. The validator's
        L{Validator.validate} method is activated every time the
        object's value needs to be verified, that is, when the L{isValid}
        method is called. This usually happens when the object's value changes.

        @param validator:
                   the new validator
        """
        raise NotImplementedError

    def removeValidator(self, validator):
        """Removes a previously registered validator from the object. The
        specified validator is removed from the object and its C{validate}
        method is no longer called in L{isValid}.

        @param validator:
                   the validator to remove
        """
        raise NotImplementedError

    def getValidators(self):
        """Lists all validators currently registered for the object. If no
        validators are registered, returns C{None}.

        @return: collection of validators or C{None}
        """
        raise NotImplementedError

    def isValid(self):
        """Tests the current value of the object against all registered
        validators. The registered validators are iterated and for each the
        L{Validator.validate} method is called. If any validator
        throws the L{InvalidValueException} this method returns
        C{False}.

        @return: C{True} if the registered validators concur that the
                value is valid, C{False} otherwise
        """
        raise NotImplementedError

    def validate(self):
        """Checks the validity of the validatable. If the validatable is valid
        this method should do nothing, and if it's not valid, it should throw
        C{InvalidValueException}

        @raise InvalidValueException:
                    if the value is not valid
        """
        raise NotImplementedError

    def isInvalidAllowed(self):
        """Checks the validabtable object accept invalid values.The default
        value is C{True}.
        """
        raise NotImplementedError

    def setInvalidAllowed(self, invalidValueAllowed):
        """Should the validabtable object accept invalid values. Supporting
        this configuration possibility is optional. By default invalid values
        are allowed.

        @raise NotImplementedError:
                    if the setInvalidAllowed is not supported.
        """
        raise NotImplementedError