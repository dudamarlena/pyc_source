# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/create_notification_list.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateNotificationListAction(BaseAction):
    action = 'CreateNotificationList'
    command = 'create-notification-list'
    usage = '%(prog)s [-n --notification_list_name...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-n', '--notification-list-name', dest='notification_list_name', action='store', type=str, default='', help='the name of the notification list.')
        parser.add_argument('-i', '--notification-items', dest='notification_items', action='store', type=str, default='', help='an array including IDs of the notification items.')

    @classmethod
    def build_directive(cls, options):
        if options.notification_list_name == '':
            print 'error: notification_list_name should be specified.'
            return None
        else:
            notification_items = explode_array(options.notification_items)
            if not notification_items:
                print 'error: notification_items should be specified.'
                return None
            directive = {'notification_list_name': options.notification_list_name, 
               'notification_items': notification_items}
            return directive