# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/efs/filesystems.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 864 bytes
from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources

class FileSystems(AWSResources):

    def __init__(self, facade, region):
        super(FileSystems, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_file_systems = await self.facade.efs.get_file_systems(self.region)
        for raw_file_system in raw_file_systems:
            name, resource = self._parse_file_system(raw_file_system)
            self[name] = resource

    def _parse_file_system(self, raw_file_system):
        fs_id = raw_file_system.pop('FileSystemId')
        raw_file_system['name'] = raw_file_system.pop('Name') if 'Name' in raw_file_system else None
        raw_file_system['tags'] = raw_file_system.pop('Tags')
        return (
         fs_id, raw_file_system)