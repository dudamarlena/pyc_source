# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nssystemcmdpolicy.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'zojoncj'

class NSSystemCMDPolicy(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSSystemCMDPolicy, self).__init__()
        self.options = {'policyname': '', 
           'action': '', 
           'cmdspec': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options:
                    self.options[key] = json_data[key]

        self.resourcetype = NSSystemCMDPolicy.get_resourcetype()
        return

    @staticmethod
    def get_resourcetype():
        return 'systemcmdpolicy'

    def set_policyname(self, policyname):
        self.options['policyname'] = policyname

    def get_policyname(self):
        return self.options['policyname']

    def set_action(self, action):
        self.options['action'] = action

    def get_action(self):
        return self.options['action']

    def set_cmdspec(self, cmdspec):
        self.options['cmdspec'] = cmdspec

    def get_cmdspec(self):
        return self.options['cmdspec']

    @staticmethod
    def add(nitro, systemcmdpolicy):
        __systemcmdpolicy = NSSystemCMDPolicy()
        __systemcmdpolicy.set_policyname(systemcmdpolicy.get_policyname())
        __systemcmdpolicy.set_action(systemcmdpolicy.get_action())
        __systemcmdpolicy.set_cmdspec(systemcmdpolicy.get_cmdspec())
        return __systemcmdpolicy.add_resource(nitro)

    @staticmethod
    def update(nitro, systemcmdpolicy):
        __systemcmdpolicy = NSSystemCMDPolicy()
        __systemcmdpolicy.set_policyname(systemcmdpolicy.get_policyname())
        __systemcmdpolicy.set_action(systemcmdpolicy.get_action())
        __systemcmdpolicy.set_cmdspec(systemcmdpolicy.get_cmdspec())
        return __systemcmdpolicy.update_resource(nitro)

    @staticmethod
    def delete(nitro, systemcmdpolicy):
        __systemcmdpolicy = NSSystemCMDPolicy()
        __systemcmdpolicy.set_policyname(systemcmdpolicy.get_policyname())
        nsresponse = __systemcmdpolicy.delete_resource(nitro, object_name=__systemcmdpolicy.get_policyname())
        return nsresponse

    @staticmethod
    def get_all(nitro):
        """
        Use this API to fetch all cmdpolicy resources that are configured on netscaler.
        """
        __url = nitro.get_url() + NSSystemCMDPolicy.get_resourcetype()
        __json_systemcmdpolicies = nitro.get(__url).get_response_field(NSSystemCMDPolicy.get_resourcetype())
        __systemcmdpolicies = []
        for json_systemcmdpolicy in __json_systemcmdpolicies:
            __systemcmdpolicies.append(NSSystemCMDPolicy(json_systemcmdpolicy))

        return __systemcmdpolicies