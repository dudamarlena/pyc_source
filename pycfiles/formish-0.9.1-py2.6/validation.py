# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/formish/validation.py
# Compiled at: 2009-06-17 11:37:51
"""
The validation module converts data to and from request format (or at least
calls the converters that do so) and also converts dotted numeric formats into
sequences (e.g. a.0 and a.1 onto a[0] and a[1]). It also includes some
validation exceptions.
"""

class FormishError(Exception):
    """
    Base class for all Forms errors. A single string, message, is accepted and
    stored as an attribute.
    
    The message is not passed on to the Exception base class because it doesn't
    seem to be able to handle unicode at all.
    """

    def __init__(self, message, *args):
        Exception.__init__(self, message, *args)
        self.message = message

    def __str__(self):
        return self.message

    __unicode__ = __str__

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)


class FormError(FormishError):
    """
    Form validation error. Raise this, typically from a submit callback, to
    signal that the form (not an individual field) failed to validate.
    """
    pass


class NoActionError(FormishError):
    """
    Form validation error. Raise this, typically from a submit callback, to
    signal that the form (not an individual field) failed to validate.
    """
    pass