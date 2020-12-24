# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/systemgroupsystemuserbinding.py
# Compiled at: 2015-10-01 09:23:35
from nsbaseresource import NSBaseResource
__author__ = 'md2k@md2k.net'

class SystemGroupSystemUserBinding(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(SystemGroupSystemUserBinding, self).__init__()
        self.options = {'groupname': '', 'username': ''}
        self.resourcetype = SystemGroupSystemUserBinding.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'systemgroup_systemuser_binding'

    def set_username(self, username):
        """The name of command policy.
        """
        self.options['username'] = username

    def get_username(self):
        """The name of command policy.
        """
        return self.options['username']

    def set_groupname(self, groupname):
        """Name of the system group.<br/>Minimum length =  1.
        """
        self.options['groupname'] = groupname

    def get_groupname(self):
        """Name of the system group.<br/>Minimum length =  1.
        """
        return self.options['groupname']

    @staticmethod
    def add(nitro, systemgroup):
        __systemgroup = SystemGroupSystemUserBinding()
        __systemgroup.set_username(systemgroup.get_username())
        __systemgroup.set_groupname(systemgroup.get_groupname())
        return __systemgroup.add_resource(nitro)

    @staticmethod
    def update(nitro, systemgroup):
        __systemgroup = SystemGroupSystemUserBinding()
        __systemgroup.set_username(systemgroup.get_username())
        __systemgroup.set_groupname(systemgroup.get_groupname())
        return __systemgroup.update_resource(nitro)

    @staticmethod
    def delete(nitro, systemgroup):
        __systemgroup = SystemGroupSystemUserBinding()
        __systemgroup.set_groupname(systemgroup.get_groupname())
        return __systemgroup.delete_resource(nitro)

    @staticmethod
    def get(nitro, systemgroup):
        __systemgroup = SystemGroupSystemUserBinding()
        __systemgroup.set_groupname(systemgroup.get_groupname())
        return __systemgroup.get_resource(nitro)

    @staticmethod
    def get_all(nitro):
        __url = nitro.get_url() + SystemGroupSystemUserBinding.get_resourcetype()
        __json_systemgroup = nitro.get(__url).get_response_field(SystemGroupSystemUserBinding.get_resourcetype())
        __systemgroup = []
        for json_systemgroup in __json_systemgroup:
            __systemgroup.append(SystemGroupSystemUserBinding(json_systemgroup))

        return __systemgroup