# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/profpy/apis/utils/Api.py
# Compiled at: 2020-01-07 15:07:46
# Size of source mod 2**32: 734 bytes
import abc

class Api(abc.ABC):

    def __init__(self, in_public_key, in_private_key, in_url, in_ip_restriction=None):
        self.url = in_url
        self.public_key = in_public_key
        self.private_key = in_private_key
        self.ip_restriction = in_ip_restriction
        self.endpoints = []
        self.endpoint_to_args = {}
        self.uuid = None
        self.time = None
        self.hash = None
        self.token = None

    @abc.abstractmethod
    def _set_args_mapping(self):
        pass

    @abc.abstractmethod
    def _set_endpoints(self):
        pass

    @abc.abstractmethod
    def _hit_endpoint(self, valid_args, endpoint_name, get_one=False, request_type='GET', **kwargs):
        pass