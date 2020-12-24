# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/delete_notification_lists.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteNotificationListsAction(BaseAction):
    action = 'DeleteNotificationLists'
    command = 'delete-notification-lists'
    usage = '%(prog)s [-l --notification_lists...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-l', '--notification-lists', dest='notification_lists', action='store', type=str, default='', help='An array including IDs of the notification lists which you want to delete.')

    @classmethod
    def build_directive(cls, options):
        notification_lists = explode_array(options.notification_lists)
        if not notification_lists:
            print 'error: notification_lists should be specified.'
            return None
        else:
            directive = {'notification_lists': notification_lists}
            return directive