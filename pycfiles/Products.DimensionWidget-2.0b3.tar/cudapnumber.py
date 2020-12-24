# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/validators/cudapnumber.py
# Compiled at: 2009-04-26 22:17:24
import re
from Products.validation.interfaces.IValidator import IValidator

class CUDAPNumberValidator:
    """A validator for a CUDAP number.
    """
    __module__ = __name__
    __implements__ = IValidator

    def __init__(self, name, title='CUDAP Number validator', description='Check that CUDAP field is a valid CUDAP number'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, *args, **kwargs):
        type_doc = ('RESO', 'RESOREC', 'RESODEC', 'RESOHCD', 'RESOHCS', 'RESOSEC',
                    'ORDEHCD', 'ORDEHCS')
        if isinstance(value, str):
            cudap = value
        else:
            return 'Validation failed(%s): value is %s' % (self.name, repr(value))
        cudap_re = re.compile('^[A-Z]+-[A-Z]{3}:\\d{7}/\\d{4}$')
        if cudap_re.match(cudap) is None:
            return 'Validation failed(%s): %s is not a valid CUDAP: It should be of the form TypeDoc-server:number/year where TypeDoc is one of %s, server is a 3 character string, number is a 7 digit number and year is a 4 digit number' % (self.name, repr(cudap), str(type_doc))
        dash_index = cudap.find('-')
        if cudap[:dash_index] not in type_doc:
            return 'Validation failed(%s): %s is not a valid CUDAP: TypeDoc should be one of the following: %s' % (self.name, repr(cudap), str(type_doc))
        return 1