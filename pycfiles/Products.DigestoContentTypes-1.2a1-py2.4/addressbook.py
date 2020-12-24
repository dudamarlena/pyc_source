# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/validators/addressbook.py
# Compiled at: 2009-04-26 22:17:24
import re
from Products.validation.interfaces.IValidator import IValidator
from Products.validation.validators.BaseValidators import EMAIL_RE

class AddressBookValidator:
    """A validator for a tuple of email addresses.
    """
    __module__ = __name__
    __implements__ = IValidator

    def __init__(self, name, title='Address book validator', description='Check that every item in a tuple is a valid email address'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        if isinstance(value, str):
            addresses = (
             value,)
        elif hasattr(value, '__iter__'):
            addresses = value
        else:
            return 'Validation failed(%s): value is %s' % (self.name, repr(value))
        regex = '^' + EMAIL_RE
        compiled_re = re.compile(regex)
        for address in addresses:
            m = compiled_re.match(address)
            if m is None:
                return 'Validation failed(%s): %s is not a valid email address' % (self.name, repr(address))

        return 1