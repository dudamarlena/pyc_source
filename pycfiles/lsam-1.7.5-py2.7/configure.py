# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsam/configure.py
# Compiled at: 2019-05-24 02:34:45
from .sam_api import API, XMLBase, XMLRequest, ResultFilter
__all__ = ('Config', 'LocalUserDhcpHostConfig', 'Configure', 'ConfigureChild')

class Config(XMLBase):

    def __init__(self, className, actions, *subconfig):
        self.xml = getattr(API, className)()
        self.actionMask(actions)
        self.childSet = None
        for subconf in subconfig:
            self.child(subconf)

        return

    def child(self, subconf):
        if self.childSet is None:
            self.childSet = getattr(API, 'children-Set')()
            self.xml.append(self.childSet)
        self.childSet.append(subconf.xml)
        return


class LocalUserDhcpHostConfig(Config):

    def __init__(self, actions, **kw):
        Config.__init__(self, 'localuserdb.DhcpHost', actions)
        for k, v in sorted(kw.items()):
            self.tag(k, v)

    def set_custom_option(self, option_number, option_value, option_type='hex'):
        config = Config('localuserdb.LocalUserDbDhcpCustomOption', 'create|modify')
        config.tag('option', 'customOption')
        config.tag('optionNumber', option_number)
        config.tag('optionType', option_type)
        config.tag('optionValue', option_value)
        self.child(config)


class Configure(XMLRequest):
    METHOD = 'generic.GenericObject.configureInstanceWithResult'

    def __init__(self, distinguishedName, config, deployer='immediate', synchronousDeploy=True, includeChildren=False):
        XMLRequest.__init__(self)
        self.tag('deployer', deployer)
        self.tag('includeChildren', includeChildren)
        self.tag('distinguishedName', distinguishedName)
        self.tag('synchronousDeploy', synchronousDeploy)
        self.xml.configInfo = API.configInfo(config.xml)

    def result_fields(self, className=None):
        result_filter = ResultFilter(className)
        self.xml.append(result_filter.xml)
        return result_filter


class ConfigureChild(XMLRequest):
    METHOD = 'generic.GenericObject.configureChildInstanceWithResult'

    def __init__(self, distinguishedName, config, deployer='immediate', synchronousDeploy=True):
        XMLRequest.__init__(self)
        self.tag('deployer', deployer)
        self.tag('distinguishedName', distinguishedName)
        self.tag('synchronousDeploy', synchronousDeploy)
        self.xml.childConfigInfo = API.childConfigInfo(config.xml)

    def result_fields(self, className=None):
        result_filter = ResultFilter(className)
        self.xml.append(result_filter.xml)
        return result_filter