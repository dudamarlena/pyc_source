# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramusus/workspace/manufacture/env/src/django-vkontakte-groups-migration/vkontakte_groups_migration/tasks.py
# Compiled at: 2014-10-22 12:47:09
from celery.task import Task
from vkontakte_groups_migration.models import GroupMigration, update_group_users

class VkontakteGroupUpdateUsersM2M(Task):

    def run(self, stat_id, **kwargs):
        stat = GroupMigration.objects.get(pk=stat_id)
        logger = self.get_logger(**kwargs)
        logger.info('VK group "%s" users m2m relations updating started' % stat.group)
        update_group_users(stat.group)
        logger.info('VK group "%s" users m2m relations succesfully updated' % stat.group)
        return True