# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/casper/casper.py
# Compiled at: 2020-02-03 17:04:46
# Size of source mod 2**32: 2497 bytes
from casper.state import CasperState
from casper.services.base import get_service
import os, logging

class Casper(object):

    def __init__(self, start_directory: str=None, bucket_name: str=None, state_file: str=None, profile: str=None, exclude_resources: set=None):
        if start_directory is None or start_directory == '.':
            start_directory = os.getcwd()
        if exclude_resources is None:
            exclude_resources = set()
        self.exclude_resources = exclude_resources
        self.start_dir = start_directory
        self.profile = profile
        self.state_file = state_file
        self.bucket = bucket_name
        self.casper_state = CasperState(profile=(self.profile),
          bucket=(self.bucket),
          state_file=(self.state_file))
        self.logger = logging.getLogger('casper')

    def build(self, exclude_directories: set=None, exclude_state_res: set=None):
        self.logger.info('Building states...')
        state_info = self.casper_state.build_state_resources(start_dir=(self.start_dir),
          exclude_directories=exclude_directories,
          exclude_state_res=exclude_state_res)
        return state_info

    def scan(self, service_name, detailed=False):
        if self.casper_state.state_resources is None:
            self.casper_state.load_state()
        self.logger.info(f"Scanning {service_name.upper()} service...")
        service = get_service(service_name)
        cloud_service = service(profile=(self.profile))
        terraformed_resources = self.casper_state.state_resources
        ghosts = {}
        for resource_group in cloud_service.resources_groups:
            resources = cloud_service.get_cloud_resources(resource_group)
            diff = set(resources.keys()).difference(set(terraformed_resources.get(resource_group, [])))
            ghosts[resource_group] = {}
            ghosts[resource_group]['ids'] = [d for d in diff if d not in self.exclude_resources]
            ghosts[resource_group]['count'] = len(ghosts[resource_group]['ids'])
            if detailed:
                ghosts[resource_group]['resources'] = [resources[d] for d in diff if d not in self.exclude_resources]

        cloud_service.scan_service(ghosts)
        return ghosts