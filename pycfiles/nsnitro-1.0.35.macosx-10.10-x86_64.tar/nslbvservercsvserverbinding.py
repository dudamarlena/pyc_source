# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nslbvservercsvserverbinding.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'Aleksandar Topuzovic'

class NSLBVServerCSVserverBinding(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSLBVServerCSVserverBinding, self).__init__()
        self.options = {'priority': '', 'policyname': '', 
           'name': '', 
           'cachevserver': '', 
           'cachetype': '', 
           'hits': ''}
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        self.resourcetype = NSLBVServerCSVserverBinding.get_resourcetype()
        return

    @staticmethod
    def get_resourcetype():
        """
        Binding object showing the csvserver that can be bound to lbvserver.
        """
        return 'lbvserver_csvserver_binding'

    def set_priority(self, priority):
        """
        Priority.
        """
        self.options['priority'] = priority

    def get_priority(self):
        """
        Priority.
        """
        return self.options['priority']

    def set_policyname(self, policyname):
        """
        Name of the policy bound to the LB vserver.
        """
        self.options['policyname'] = policyname

    def get_policyname(self):
        """
        Name of the policy bound to the LB vserver.
        """
        return self.options['policyname']

    def set_name(self, name):
        """
        The virtual server name to which the service is bound.
        Minimum length = 1
        """
        self.options['name'] = name

    def get_name(self):
        """
        The virtual server name to which the service is bound.
        Minimum length = 1
        """
        return self.options['name']

    def set_cachevserver(self, cachevserver):
        """
        Cache virtual server.
        """
        self.options['cachevserver'] = cachevserver

    def get_cachevserver(self):
        """
        Cache virtual server.
        """
        return self.options['cachevserver']

    def get_cachetype(self):
        """
        Cache type.
        """
        return self.options['cachetype']

    def get_hits(self):
        """
        Number of hits.
        """
        return self.options['hits']

    @staticmethod
    def get(nitro, lbvservercsvserverbinding):
        """
        Use this API to fetch lb vserver cs vserver binding resource of given name.
        """
        __url = nitro.get_url() + NSLBVServerCSVserverBinding.get_resourcetype() + '/' + lbvservercsvserverbinding.get_name()
        __json_csvservers = nitro.get(__url).get_response_field(NSLBVServerCSVserverBinding.get_resourcetype())
        __csvservers = []
        for json_csvserver in __json_csvservers:
            __csvservers.append(NSLBVServerCSVserverBinding(json_csvserver))

        return __csvservers