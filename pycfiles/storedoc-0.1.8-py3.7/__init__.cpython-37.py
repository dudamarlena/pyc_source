# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/storedoc/__init__.py
# Compiled at: 2019-08-12 00:59:01
# Size of source mod 2**32: 1061 bytes
from storedoc.services import SUPPORTED_SERVICES
from storedoc.local import LocalStorage

class Service(object):

    def __init__(self, service_name):
        if service_name in SUPPORTED_SERVICES:
            self.service_name = service_name
        else:
            raise Exception('Service not found.')

    def available_services(self):
        return dict(SUPPORTED_SERVICES.keys())

    def describe_all_services(self):
        print('Services: ')
        for service_name in SUPPORTED_SERVICES:
            description = SUPPORTED_SERVICES[service_name]['description']
            print('{} - {} '.format(service_name, description))

    def get_conn(self):
        return getattr(self, 'service', 'Service not connected.')

    def describe(self):
        return SUPPORTED_SERVICES[self.service_name]['description']

    def connect(self, **credentials):
        self.service = (SUPPORTED_SERVICES[self.service_name]['service'])(**credentials)

    def upload_file(self, file, **kwargs):
        return (self.service.upload_file)(file, **kwargs)