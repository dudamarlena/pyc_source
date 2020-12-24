# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudsearch2/optionstatus.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 8121 bytes
from boto.compat import json

class OptionStatus(dict):
    __doc__ = "\n    Presents a combination of status field (defined below) which are\n    accessed as attributes and option values which are stored in the\n    native Python dictionary.  In this class, the option values are\n    merged from a JSON object that is stored as the Option part of\n    the object.\n\n    :ivar domain_name: The name of the domain this option is associated with.\n    :ivar create_date: A timestamp for when this option was created.\n    :ivar state: The state of processing a change to an option.\n        Possible values:\n\n        * RequiresIndexDocuments: the option's latest value will not\n          be visible in searches until IndexDocuments has been called\n          and indexing is complete.\n        * Processing: the option's latest value is not yet visible in\n          all searches but is in the process of being activated.\n        * Active: the option's latest value is completely visible.\n\n    :ivar update_date: A timestamp for when this option was updated.\n    :ivar update_version: A unique integer that indicates when this\n        option was last updated.\n    "

    def __init__(self, domain, data=None, refresh_fn=None, refresh_key=None, save_fn=None):
        self.domain = domain
        self.refresh_fn = refresh_fn
        self.refresh_key = refresh_key
        self.save_fn = save_fn
        self.refresh(data)

    def _update_status(self, status):
        self.creation_date = status['CreationDate']
        self.status = status['State']
        self.update_date = status['UpdateDate']
        self.update_version = int(status['UpdateVersion'])

    def _update_options(self, options):
        if options:
            self.update(options)

    def refresh(self, data=None):
        """
        Refresh the local state of the object.  You can either pass
        new state data in as the parameter ``data`` or, if that parameter
        is omitted, the state data will be retrieved from CloudSearch.
        """
        if not data:
            if self.refresh_fn:
                data = self.refresh_fn(self.domain.name)
                if data:
                    if self.refresh_key:
                        for key in self.refresh_key:
                            data = data[key]

            if data:
                self._update_status(data['Status'])
                self._update_options(data['Options'])

    def to_json(self):
        """
        Return the JSON representation of the options as a string.
        """
        return json.dumps(self)

    def save(self):
        """
        Write the current state of the local object back to the
        CloudSearch service.
        """
        if self.save_fn:
            data = self.save_fn(self.domain.name, self.to_json())
            self.refresh(data)


class IndexFieldStatus(OptionStatus):

    def save(self):
        pass


class AvailabilityOptionsStatus(OptionStatus):

    def save(self):
        pass


class ScalingParametersStatus(IndexFieldStatus):
    pass


class ExpressionStatus(IndexFieldStatus):
    pass


class ServicePoliciesStatus(OptionStatus):

    def new_statement(self, arn, ip):
        """
        Returns a new policy statement that will allow
        access to the service described by ``arn`` by the
        ip specified in ``ip``.

        :type arn: string
        :param arn: The Amazon Resource Notation identifier for the
            service you wish to provide access to.  This would be
            either the search service or the document service.

        :type ip: string
        :param ip: An IP address or CIDR block you wish to grant access
            to.
        """
        return {'Effect': 'Allow', 
         'Action': '*', 
         'Resource': arn, 
         'Condition': {'IpAddress': {'aws:SourceIp': [
                                                      ip]}}}

    def _allow_ip(self, arn, ip):
        if 'Statement' not in self:
            s = self.new_statement(arn, ip)
            self['Statement'] = [s]
            self.save()
        else:
            add_statement = True
            for statement in self['Statement']:
                if statement['Resource'] == arn:
                    for condition_name in statement['Condition']:
                        if condition_name == 'IpAddress':
                            add_statement = False
                            condition = statement['Condition'][condition_name]
                            if ip not in condition['aws:SourceIp']:
                                condition['aws:SourceIp'].append(ip)
                            else:
                                continue

                    continue

            if add_statement:
                s = self.new_statement(arn, ip)
                self['Statement'].append(s)
            self.save()

    def allow_search_ip(self, ip):
        """
        Add the provided ip address or CIDR block to the list of
        allowable address for the search service.

        :type ip: string
        :param ip: An IP address or CIDR block you wish to grant access
            to.
        """
        arn = self.domain.service_arn
        self._allow_ip(arn, ip)

    def allow_doc_ip(self, ip):
        """
        Add the provided ip address or CIDR block to the list of
        allowable address for the document service.

        :type ip: string
        :param ip: An IP address or CIDR block you wish to grant access
            to.
        """
        arn = self.domain.service_arn
        self._allow_ip(arn, ip)

    def _disallow_ip(self, arn, ip):
        if 'Statement' not in self:
            return
        need_update = False
        for statement in self['Statement']:
            if statement['Resource'] == arn:
                for condition_name in statement['Condition']:
                    if condition_name == 'IpAddress':
                        condition = statement['Condition'][condition_name]
                        if ip in condition['aws:SourceIp']:
                            condition['aws:SourceIp'].remove(ip)
                            need_update = True
                        else:
                            continue

                continue

        if need_update:
            self.save()

    def disallow_search_ip(self, ip):
        """
        Remove the provided ip address or CIDR block from the list of
        allowable address for the search service.

        :type ip: string
        :param ip: An IP address or CIDR block you wish to grant access
            to.
        """
        arn = self.domain.service_arn
        self._disallow_ip(arn, ip)

    def disallow_doc_ip(self, ip):
        """
        Remove the provided ip address or CIDR block from the list of
        allowable address for the document service.

        :type ip: string
        :param ip: An IP address or CIDR block you wish to grant access
            to.
        """
        arn = self.domain.service_arn
        self._disallow_ip(arn, ip)