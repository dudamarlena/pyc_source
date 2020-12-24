# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsgslbvserverdomainbinding.py
# Compiled at: 2015-12-01 16:20:42
from nsbaseresource import NSBaseResource

class NSGSLBVServerDomainBinding(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSGSLBVServerDomainBinding, self).__init__()
        self.options = {'name': '', 
           'backupipflag': '', 
           'cookietimeout': '', 
           'backupip': '', 
           'ttl': '', 
           'domainname': '', 
           'sitedomainttl': '', 
           'cookie_domainflag': '', 
           'cookie_domain': '', 
           '__count': ''}
        self.resourcetype = NSGSLBVServerDomainBinding.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'gslbvserver_domain_binding'

    def set_name(self, name):
        """
        """
        self.options['name'] = name

    def get_name(self):
        """
        """
        return self.options['name']

    def get_backupipflag(self):
        """
        """
        return self.options['backupipflag']

    def get_cookietimeout(self):
        """
        """
        return self.options['cookietimeout']

    def get_backupip(self):
        """
        """
        return self.options['backupip']

    def get_domainname(self):
        """
        """
        return self.options['domainname']

    def get_count(self):
        """
        """
        return self.options['__count']

    @staticmethod
    def get(nitro, domain_binding):
        """
        Use this API to fetch csvserver resource of given name.
        """
        __domain_binding = NSGSLBVServerDomainBinding()
        __domain_binding.set_name(domain_binding.get_name())
        __domain_binding.get_resource(nitro)
        return __domain_binding