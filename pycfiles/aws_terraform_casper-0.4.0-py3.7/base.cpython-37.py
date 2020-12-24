# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/casper/services/base.py
# Compiled at: 2020-02-03 17:04:46
# Size of source mod 2**32: 1283 bytes
import boto3, importlib, logging
from abc import ABC, abstractmethod
SUPPORTED_SERVICES = {'ec2':'EC2Service', 
 'iam':'IAMService',  's3':'S3Service'}

class BaseService(ABC):

    def __init__(self, profile=None):
        self._resources_groups = {}
        self.session = boto3.Session()
        self.logger = logging.getLogger('casper')
        if profile:
            self.session = boto3.Session(profile_name=profile)

    @property
    def resources_groups(self):
        return self._resources_groups

    def get_cloud_resources(self, group):
        handler = getattr(self, f"_get_live_{group}", None)
        if handler:
            return handler()
        message = f"Service Handler for {group} is not currently supported"
        self.logger.debug(message)

    @abstractmethod
    def scan_service(self, ghosts):
        pass


class UnsupportedServiceException(Exception):
    pass


def get_service(service_name):
    if service_name not in SUPPORTED_SERVICES:
        raise UnsupportedServiceException()
    module = importlib.import_module(f"casper.services.{service_name}")
    service_class = SUPPORTED_SERVICES.get(service_name, None)
    service = getattr(module, service_class)
    return service