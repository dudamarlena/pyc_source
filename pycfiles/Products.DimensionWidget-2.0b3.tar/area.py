# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/validators/area.py
# Compiled at: 2009-04-26 22:17:24
from Products.validation.interfaces.IValidator import IValidator

class AreaRecordValidator:
    """A validator for the area record.
    """
    __module__ = __name__
    __implements__ = IValidator

    def __init__(self, name, title='Area record validator', description='Check that every item in the Area Record is valid'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        return 1