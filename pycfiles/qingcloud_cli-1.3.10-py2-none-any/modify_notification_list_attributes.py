# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/modify_notification_list_attributes.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyNotificationListAttributesAction(BaseAction):
    action = 'ModifyNotificationListAttributes'
    command = 'modify-notification-list-attributes'
    usage = '%(prog)s [-l --notification_list] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-l', '--notification-list', dest='notification_list', action='store', type=str, default='', help='The ID of notification list which attributes you want to modify.')
        parser.add_argument('-n', '--notification-list-name', dest='notification_list_name', action='store', type=str, default=None, help='The new name of the notification list which will be modified.')
        parser.add_argument('-i', '--notification-items', dest='notification_items', action='store', type=str, default=None, help=' An array including IDs of notification items.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.notification_list == '':
            print 'error: notification_list_id should be specified.'
            return None
        else:
            directive = {'notification_list': options.notification_list, 
               'notification_list_name': options.notification_list_name, 
               'notification_items': explode_array(options.notification_items)}
            return directive