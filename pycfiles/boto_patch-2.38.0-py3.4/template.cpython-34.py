# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudformation/template.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1686 bytes
from boto.resultset import ResultSet
from boto.cloudformation.stack import Capability

class Template(object):

    def __init__(self, connection=None):
        self.connection = connection
        self.description = None
        self.template_parameters = None
        self.capabilities_reason = None
        self.capabilities = None

    def startElement(self, name, attrs, connection):
        if name == 'Parameters':
            self.template_parameters = ResultSet([('member', TemplateParameter)])
            return self.template_parameters
        else:
            if name == 'Capabilities':
                self.capabilities = ResultSet([('member', Capability)])
                return self.capabilities
            return

    def endElement(self, name, value, connection):
        if name == 'Description':
            self.description = value
        else:
            if name == 'CapabilitiesReason':
                self.capabilities_reason = value
            else:
                setattr(self, name, value)


class TemplateParameter(object):

    def __init__(self, parent):
        self.parent = parent
        self.default_value = None
        self.description = None
        self.no_echo = None
        self.parameter_key = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'DefaultValue':
            self.default_value = value
        else:
            if name == 'Description':
                self.description = value
            else:
                if name == 'NoEcho':
                    self.no_echo = bool(value)
                else:
                    if name == 'ParameterKey':
                        self.parameter_key = value
                    else:
                        setattr(self, name, value)