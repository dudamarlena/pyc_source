# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/error.py
# Compiled at: 2010-03-24 05:43:08


class ElementError(object):
    error_type = 'ERROR'
    tag = ''
    msg_id = ''
    description = ''
    line = None
    msg_origin = ''

    def __init__(self, node, description=None):
        self.tag = node.tag
        self.line = node.sourceline
        if description:
            self.description = description

    def get_message(self):
        fmt = '<unknown>:%(sourceline)s:%(type)s:%(msg_origin)s:%(element)s:%(message)s: %(description)s'
        return fmt % {'type': self.error_type, 'sourceline': self.line, 
           'element': self.tag, 
           'message': self.msg_id, 
           'description': self.description}


class Warning(ElementError):
    error_type = 'WARNING'


class VersionWarning(Warning):
    msg_id = 'INCOMPATIBLE_FINVOICE_VERSION'

    def __init__(self, description):
        self.description = description


class ElementMissingError(ElementError):
    error_type = 'ERROR'
    msg_id = 'ELEMENT_MISSING'

    def __init__(self, node, msg_extra=''):
        self.line = node.sourceline
        self.node = node
        self.description = msg_extra


class UnknownAttributeWarning(Warning):
    msg_id = 'UNKNOWN_ATTRIBUTE'


class UnknownElementWarning(Warning):
    msg_id = 'UNKNOWN_ELEMENT'


class InvalidValue(ElementError):
    msg_id = 'INVALID_VALUE'


class LxmlErrorWrapper(ElementError):

    def __init__(self, msg):
        msg_parts = str(msg).split(':')
        self.line = msg_parts[1]
        self.msg_id = 'DTD_VALIDATION'
        self.description = msg_parts[(-1)]

    def get_message(self):
        return self.description


class ValueMismatchError(ElementError):
    error_type = 'ERROR'
    msg_id = 'VALUE_MISMATCH'
    line = -1
    node = ''

    def __init__(self, description=''):
        self.description = description