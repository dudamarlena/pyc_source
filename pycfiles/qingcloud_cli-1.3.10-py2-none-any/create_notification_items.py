# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/create_notification_items.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction
import json

class CreateNotificationItemsAction(BaseAction):
    action = 'CreateNotificationItems'
    command = 'create-notification-items'
    usage = '%(prog)s [-i --notification-items...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--notification-items', dest='notification_items', action='store', type=str, default='', help="A list of JSON Objects which contains 'content',                                 'notification_item_type' and 'remarks'.                                  'For Example:'                                  '[{'content':'xxxxxx@yunify.com','notification_item_type':'email','remarks':'qem'}]'.")

    @classmethod
    def build_directive(cls, options):
        if options.notification_items == '':
            print 'error: notification_items should be specified.'
            return None
        else:
            directive = {'notification_items': json.loads(options.notification_items)}
            return directive