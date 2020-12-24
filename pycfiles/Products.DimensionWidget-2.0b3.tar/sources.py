# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/validators/sources.py
# Compiled at: 2009-04-26 22:17:24
import re
from Products.validation.interfaces.IValidator import IValidator

class AreaSourceValidator:
    """A validator for a sources in a 'AT Extensions' record filed.
    """
    __module__ = __name__
    __implements__ = IValidator

    def __init__(self, name, title='Source validator', description='Check the source item'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        if isinstance(value, str):
            source = value
        else:
            return 'Validation failed(%s): value is %s' % (self.name, repr(value))
        if re.match('[\\w ]+', source, re.UNICODE) is None:
            return 'Validation failed(%s): %s is not a valid source name' % (self.name, repr(source))
        return 1


class AreaKindsValidator:
    """A validator for a kind in a 'AT Extensions' record filed.
    """
    __module__ = __name__
    __implements__ = IValidator

    def __init__(self, name, title='Kind validator', description='Check the Kind item is not an empty list'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        if not isinstance(value, list):
            return 'Validation failed(%s): value is %s' % (self.name, repr(value))
        elif len(value) <= 0:
            return 'Validation failed(%s): kinds list is empty' % self.name
        return 1