# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/facade/efs.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2677 bytes
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.aws.facade.basefacade import AWSBaseFacade
from ScoutSuite.providers.aws.facade.utils import AWSFacadeUtils
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently

class EFSFacade(AWSBaseFacade):

    async def get_file_systems(self, region: str):
        try:
            try:
                file_systems = await AWSFacadeUtils.get_all_pages('efs', region, self.session, 'describe_file_systems', 'FileSystems')
            except Exception as e:
                try:
                    print_exception('Failed to get EFS file systems: {}'.format(e))
                    file_systems = []
                finally:
                    e = None
                    del e

            else:
                await get_and_set_concurrently([
                 self._get_and_set_tags, self._get_and_set_mount_targets],
                  file_systems, region=region)
        finally:
            return

        return file_systems

    async def _get_and_set_tags(self, file_system: {}, region: str):
        client = AWSFacadeUtils.get_client('efs', self.session, region)
        try:
            file_system['Tags'] = await run_concurrently(lambda : client.describe_tags(FileSystemId=(file_system['FileSystemId']))['Tags'])
        except Exception as e:
            try:
                print_exception('Failed to describe EFS tags: {}'.format(e))
            finally:
                e = None
                del e

    async def _get_and_set_mount_targets(self, file_system: {}, region: str):
        try:
            file_system['MountTargets'] = {}
            mount_targets = await AWSFacadeUtils.get_all_pages('efs',
              region, (self.session), 'describe_mount_targets', 'MountTargets', FileSystemId=(file_system['FileSystemId']))
        except Exception as e:
            try:
                print_exception('Failed to get and set EFS mount targets: {}'.format(e))
            finally:
                e = None
                del e

        else:
            if len(mount_targets) == 0:
                return
            for mount_target in mount_targets:
                mount_target_id = mount_target['MountTargetId']
                file_system['MountTargets'][mount_target_id] = mount_target

            await get_and_set_concurrently([
             self._get_and_set_mount_target_security_groups],
              mount_targets, region=region)

    async def _get_and_set_mount_target_security_groups(self, mount_target: {}, region: str):
        client = AWSFacadeUtils.get_client('efs', self.session, region)
        try:
            mount_target['SecurityGroups'] = await run_concurrently(lambda : client.describe_mount_target_security_groups(MountTargetId=(mount_target['MountTargetId']))['SecurityGroups'])
        except Exception as e:
            try:
                print_exception('Failed to describe EFS mount target security groups: {}'.format(e))
            finally:
                e = None
                del e