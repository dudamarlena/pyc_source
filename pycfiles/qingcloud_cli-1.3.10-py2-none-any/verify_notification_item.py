# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/verify_notification_item.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class VerifyNotificationItemAction(BaseAction):
    action = 'VerifyNotificationItem'
    command = 'verify-notification-item'
    usage = '%(prog)s [-c --notification_item_content...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-c', '--notification-item-content', dest='notification_item_content', action='store', type=str, default='', help='The content of notification item which will be verified.')
        parser.add_argument('-v', '--verification-code', dest='verification_code', action='store', type=str, default='', help='The verification code.')

    @classmethod
    def build_directive(cls, options):
        if options.notification_item_content == '':
            print 'error: notification_item_content should be specified.'
            return None
        else:
            if options.verification_code == '':
                print 'error: verification_code should be specified.'
                return None
            directive = {'notification_item_content': options.notification_item_content, 
               'verification_code': options.verification_code}
            return directive