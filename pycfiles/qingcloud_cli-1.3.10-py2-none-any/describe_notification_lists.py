# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/describe_notification_lists.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction
from qingcloud.cli.misc.utils import explode_array

class DescribeNotificationListsAction(BaseAction):
    action = 'DescribeNotificationLists'
    command = 'describe-notification-lists'
    usage = '%(prog)s [-l --notification_lists...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-l', '--notification-lists', dest='notification_lists', action='store', type=str, default=None, help='an array including the IDs of the notification lists.')
        parser.add_argument('-s', '--search-word', dest='search_word', action='store', type=str, default=None, help=' the search word of notification list name.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'notification_lists': explode_array(options.notification_lists), 
           'search_word': options.search_word, 
           'offset': options.offset, 
           'limit': options.limit}
        return directive