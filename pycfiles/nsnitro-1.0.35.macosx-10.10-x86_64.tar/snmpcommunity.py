# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/snmpcommunity.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'ivanxx@gmail.com'

class SNMPCommunity(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(SNMPCommunity, self).__init__()
        self.options = {'communityname': '', 'permissions': ''}
        self.resourcetype = SNMPCommunity.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'snmpcommunity'

    def set_communityname(self, communityname):
        self.options['communityname'] = communityname

    def set_permissions(self, permissions):
        self.options['permissions'] = permissions

    def get_communityname(self):
        return self.options['communityname']

    def get_permissions(self):
        return self.options['permissions']

    @staticmethod
    def add(nitro, snmpcommunity):
        __snmpcommunity = SNMPCommunity()
        __snmpcommunity.set_communityname(snmpcommunity.get_communityname())
        __snmpcommunity.set_permissions(snmpcommunity.get_permissions())
        return __snmpcommunity.add_resource(nitro)

    @staticmethod
    def delete(nitro, snmpcommunity):
        __snmpcommunity = SNMPCommunity()
        __snmpcommunity.set_communityname(snmpcommunity.get_communityname())
        return __snmpcommunity.delete_resource(nitro)

    @staticmethod
    def get(nitro, snmpcommunity):
        __snmpcommunity = SNMPCommunity()
        __snmpcommunity.set_communityname(snmpcommunity)
        __snmpcommunity.get_resource(nitro, object_name=__snmpcommunity.get_communityname())
        return __snmpcommunity

    @staticmethod
    def get_all(nitro):
        __url = nitro.get_url() + SNMPCommunity.get_resourcetype()
        __json_snmpcommunities = nitro.get(__url).get_response_field(SNMPCommunity.get_resourcetype())
        __snmpcommunities = []
        for json_snmpcommunity in __json_snmpcommunities:
            __snmpcommunities.append(SNMPCommunity(json_snmpcommunity))

        return __snmpcommunities