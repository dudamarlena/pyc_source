# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/optiongroup.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 15665 bytes
__doc__ = '\nRepresents an OptionGroup\n'
from boto.rds.dbsecuritygroup import DBSecurityGroup
from boto.resultset import ResultSet

class OptionGroup(object):
    """OptionGroup"""

    def __init__(self, connection=None, name=None, engine_name=None, major_engine_version=None, description=None, allow_both_vpc_and_nonvpc=False, vpc_id=None):
        self.name = name
        self.engine_name = engine_name
        self.major_engine_version = major_engine_version
        self.description = description
        self.allow_both_vpc_and_nonvpc = allow_both_vpc_and_nonvpc
        self.vpc_id = vpc_id
        self.options = []

    def __repr__(self):
        return 'OptionGroup:%s' % self.name

    def startElement(self, name, attrs, connection):
        if name == 'Options':
            self.options = ResultSet([
             (
              'Options', Option)])
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'OptionGroupName':
            self.name = value
        else:
            if name == 'EngineName':
                self.engine_name = value
            else:
                if name == 'MajorEngineVersion':
                    self.major_engine_version = value
                else:
                    if name == 'OptionGroupDescription':
                        self.description = value
                    else:
                        if name == 'AllowsVpcAndNonVpcInstanceMemberships':
                            if value.lower() == 'true':
                                self.allow_both_vpc_and_nonvpc = True
                            else:
                                self.allow_both_vpc_and_nonvpc = False
                        else:
                            if name == 'VpcId':
                                self.vpc_id = value
                            else:
                                setattr(self, name, value)

    def delete(self):
        return self.connection.delete_option_group(self.name)


class Option(object):
    """Option"""

    def __init__(self, name=None, description=None, permanent=False, persistent=False, port=None, settings=None, db_security_groups=None, vpc_security_groups=None):
        self.name = name
        self.description = description
        self.permanent = permanent
        self.persistent = persistent
        self.port = port
        self.settings = settings
        self.db_security_groups = db_security_groups
        self.vpc_security_groups = vpc_security_groups
        if self.settings is None:
            self.settings = []
        if self.db_security_groups is None:
            self.db_security_groups = []
        if self.vpc_security_groups is None:
            self.vpc_security_groups = []

    def __repr__(self):
        return 'Option:%s' % self.name

    def startElement(self, name, attrs, connection):
        if name == 'OptionSettings':
            self.settings = ResultSet([
             (
              'OptionSettings', OptionSetting)])
        else:
            if name == 'DBSecurityGroupMemberships':
                self.db_security_groups = ResultSet([
                 (
                  'DBSecurityGroupMemberships', DBSecurityGroup)])
            else:
                if name == 'VpcSecurityGroupMemberships':
                    self.vpc_security_groups = ResultSet([
                     (
                      'VpcSecurityGroupMemberships', VpcSecurityGroup)])
                else:
                    return

    def endElement(self, name, value, connection):
        if name == 'OptionName':
            self.name = value
        else:
            if name == 'OptionDescription':
                self.description = value
            else:
                if name == 'Permanent':
                    if value.lower() == 'true':
                        self.permenant = True
                    else:
                        self.permenant = False
                else:
                    if name == 'Persistent':
                        if value.lower() == 'true':
                            self.persistent = True
                        else:
                            self.persistent = False
                    else:
                        if name == 'Port':
                            self.port = int(value)
                        else:
                            setattr(self, name, value)


class OptionSetting(object):
    """OptionSetting"""

    def __init__(self, name=None, description=None, value=None, default_value=False, allowed_values=None, data_type=None, apply_type=None, is_modifiable=False, is_collection=False):
        self.name = name
        self.description = description
        self.value = value
        self.default_value = default_value
        self.allowed_values = allowed_values
        self.data_type = data_type
        self.apply_type = apply_type
        self.is_modifiable = is_modifiable
        self.is_collection = is_collection

    def __repr__(self):
        return 'OptionSetting:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Name':
            self.name = value
        else:
            if name == 'Description':
                self.description = value
            else:
                if name == 'Value':
                    self.value = value
                else:
                    if name == 'DefaultValue':
                        self.default_value = value
                    else:
                        if name == 'AllowedValues':
                            self.allowed_values = value
                        else:
                            if name == 'DataType':
                                self.data_type = value
                            else:
                                if name == 'ApplyType':
                                    self.apply_type = value
                                else:
                                    if name == 'IsModifiable':
                                        if value.lower() == 'true':
                                            self.is_modifiable = True
                                        else:
                                            self.is_modifiable = False
                                    else:
                                        if name == 'IsCollection':
                                            if value.lower() == 'true':
                                                self.is_collection = True
                                            else:
                                                self.is_collection = False
                                        else:
                                            setattr(self, name, value)


class VpcSecurityGroup(object):
    """VpcSecurityGroup"""

    def __init__(self, vpc_id=None, status=None):
        self.vpc_id = vpc_id
        self.status = status

    def __repr__(self):
        return 'VpcSecurityGroup:%s' % self.vpc_id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'VpcSecurityGroupId':
            self.vpc_id = value
        else:
            if name == 'Status':
                self.status = value
            else:
                setattr(self, name, value)


class OptionGroupOption(object):
    """OptionGroupOption"""

    def __init__(self, name=None, description=None, engine_name=None, major_engine_version=None, min_minor_engine_version=None, permanent=False, persistent=False, port_required=False, default_port=None, settings=None, depends_on=None):
        self.name = name
        self.description = description
        self.engine_name = engine_name
        self.major_engine_version = major_engine_version
        self.min_minor_engine_version = min_minor_engine_version
        self.permanent = permanent
        self.persistent = persistent
        self.port_required = port_required
        self.default_port = default_port
        self.settings = settings
        self.depends_on = depends_on
        if self.settings is None:
            self.settings = []
        if self.depends_on is None:
            self.depends_on = []

    def __repr__(self):
        return 'OptionGroupOption:%s' % self.name

    def startElement(self, name, attrs, connection):
        if name == 'OptionGroupOptionSettings':
            self.settings = ResultSet([
             (
              'OptionGroupOptionSettings', OptionGroupOptionSetting)])
        else:
            if name == 'OptionsDependedOn':
                self.depends_on = []
            else:
                return

    def endElement(self, name, value, connection):
        if name == 'Name':
            self.name = value
        else:
            if name == 'Description':
                self.description = value
            else:
                if name == 'EngineName':
                    self.engine_name = value
                else:
                    if name == 'MajorEngineVersion':
                        self.major_engine_version = value
                    else:
                        if name == 'MinimumRequiredMinorEngineVersion':
                            self.min_minor_engine_version = value
                        else:
                            if name == 'Permanent':
                                if value.lower() == 'true':
                                    self.permenant = True
                                else:
                                    self.permenant = False
                            else:
                                if name == 'Persistent':
                                    if value.lower() == 'true':
                                        self.persistent = True
                                    else:
                                        self.persistent = False
                                else:
                                    if name == 'PortRequired':
                                        if value.lower() == 'true':
                                            self.port_required = True
                                        else:
                                            self.port_required = False
                                    else:
                                        if name == 'DefaultPort':
                                            self.default_port = int(value)
                                        else:
                                            setattr(self, name, value)


class OptionGroupOptionSetting(object):
    """OptionGroupOptionSetting"""

    def __init__(self, name=None, description=None, default_value=False, allowed_values=None, apply_type=None, is_modifiable=False):
        self.name = name
        self.description = description
        self.default_value = default_value
        self.allowed_values = allowed_values
        self.apply_type = apply_type
        self.is_modifiable = is_modifiable

    def __repr__(self):
        return 'OptionGroupOptionSetting:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'SettingName':
            self.name = value
        else:
            if name == 'SettingDescription':
                self.description = value
            else:
                if name == 'DefaultValue':
                    self.default_value = value
                else:
                    if name == 'AllowedValues':
                        self.allowed_values = value
                    else:
                        if name == 'ApplyType':
                            self.apply_type = value
                        else:
                            if name == 'IsModifiable':
                                if value.lower() == 'true':
                                    self.is_modifiable = True
                                else:
                                    self.is_modifiable = False
                            else:
                                setattr(self, name, value)