# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/nsnitro/nsresources/nsresponderaction.py
# Compiled at: 2014-04-24 09:01:10
from nsbaseresource import NSBaseResource
__author__ = 'timl'

class NSResponderAction(NSBaseResource):

    def __init__(self, json_data=None):
        """
        Supplied with json_data the object can be pre-filled
        """
        super(NSResponderAction, self).__init__()
        self.options = {'name': '', 
           'newname': '', 
           'type': '', 
           'target': '', 
           'bypasssafetycheck': '', 
           'hits': '', 
           'referencecount': '', 
           'undefhits': ''}
        self.resourcetype = NSResponderAction.get_resourcetype()
        if json_data is not None:
            for key in json_data.keys():
                if key in self.options.keys():
                    self.options[key] = json_data[key]

        return

    @staticmethod
    def get_resourcetype():
        return 'responderaction'

    def set_name(self, name):
        """
        Name of the responder action.

        Default value: 0
        """
        self.options['name'] = name

    def get_name(self):
        """
        Name of the responder action.

        Default value: 0
        """
        return self.options['name']

    def set_type(self, action_type):
        """
        Type (respondwith, redirect) of responder action.

        Default value: 0
        """
        self.options['type'] = action_type

    def get_type(self):
        """
        Type (respondwith, redirect) of responder action.

        Default value: 0
        """
        return self.options['type']

    def set_target(self, target):
        """
        Target of responder action.

        Default value: 0
        """
        self.options['target'] = target

    def get_target(self):
        """
        Target of responder action.

        Default value: 0
        """
        return self.options['target']

    def set_newname(self, newname):
        """
        The new name of the responder action.

        Default value: 0
        Minimum length =  1.
        """
        self.options['newname'] = newname

    def get_newname(self):
        """
        The new name of the responder action.

        Default value: 0
        Minimum length =  1.
        """
        return self.options['newname']

    def get_hits(self):
        """
        Number of hits.

        Default value: 0
        """
        return self.options['hits']

    def get_undefhits(self):
        """
        Number of undef hits.

        Default value: 0
        """
        return self.options['undefhits']

    def get_referencecount(self):
        """
        Number of references to this action.

        Default value: 0
        """
        return self.options['referencecount']

    def set_bypasssafetycheck(self, bypasssafetycheck):
        """
        Bypass the safety check

        Default value: NO
        """
        valid = ('YES', 'NO')
        if bypasssafetycheck and bypasssafetycheck not in valid:
            raise ValueError('bypasssafetycheck must be one of %s' % (',').join(valid))
        self.options['bypasssafetycheck'] = bypasssafetycheck

    def get_bypasssafetycheck(self):
        """
        Bypass the safety check

        Default value: NO
        """
        return self.options['bypasssafetycheck']

    @staticmethod
    def get(nitro, responderaction):
        """
        Use this API to fetch responderaction resource of given name.
        """
        __responderaction = NSResponderAction()
        __responderaction.set_name(responderaction.get_name())
        __responderaction.get_resource(nitro)
        return __responderaction

    @staticmethod
    def get_all(nitro):
        """
        Use this API to fetch all configured responderaction resources.
        """
        __url = nitro.get_url() + NSResponderAction.get_resourcetype()
        __json_cspolicies = nitro.get(__url).get_response_field(NSResponderAction.get_resourcetype())
        __responderpolicies = []
        for json_responderaction in __json_cspolicies:
            __responderpolicies.append(NSResponderAction(json_responderaction))

        return __responderpolicies

    @staticmethod
    def add(nitro, responderaction):
        """
        Use this API to add responderaction.
        """
        __responderaction = NSResponderAction()
        __responderaction.set_name(responderaction.get_name())
        __responderaction.set_type(responderaction.get_type())
        __responderaction.set_target(responderaction.get_target())
        __responderaction.set_bypasssafetycheck(responderaction.get_bypasssafetycheck())
        return __responderaction.add_resource(nitro)

    @staticmethod
    def delete(nitro, responderaction):
        """
        Use this API to delete responderaction of a given name.
        """
        __responderaction = NSResponderAction()
        __responderaction.set_name(responderaction.get_name())
        nsresponse = __responderaction.delete_resource(nitro)
        return nsresponse

    @staticmethod
    def update(nitro, responderaction):
        """
        Use this API to update a responderaction of a given name.
        """
        __responderaction = NSResponderAction()
        __responderaction.set_name(responderaction.get_name())
        __responderaction.set_target(responderaction.get_target())
        __responderaction.set_bypasssafetycheck(responderaction.get_bypasssafetycheck())
        return __responderaction.update_resource(nitro)

    @staticmethod
    def rename(nitro, responderaction):
        """
        Use this API to rename responderaction.
        """
        __responderaction = NSResponderAction()
        __responderaction.set_name(responderaction.get_name())
        __responderaction.set_newname(responderaction.get_newname())
        return __responderaction.perform_operation(nitro, 'rename')