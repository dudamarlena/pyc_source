# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/describe_notification_items.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeNotificationItemsAction(BaseAction):
    action = 'DescribeNotificationItems'
    command = 'describe-notification-items'
    usage = '%(prog)s [-i --notification_items...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--notification-items', dest='notification_items', action='store', type=str, default=None, help='An array including IDs of notification items.')
        parser.add_argument('-l', '--notification-list', dest='notification_list', action='store', type=str, default=None, help='The ID of notification list.')
        parser.add_argument('-t', '--notification-item-type', dest='notification_item_type', action='store', type=str, default=None, help='The type of notification item, including email, phone and webhook.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'notification_items': options.notification_items, 
           'notification_list': options.notification_list, 
           'notification_item_type': options.notification_item_type}
        return directive