# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/notification/describe_notification_center_user_posts.py
# Compiled at: 2016-10-02 15:05:47
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeNotificationCenterUserPostsAction(BaseAction):
    action = 'DescribeNotificationCenterUserPosts'
    command = 'describe-notification-center-user-posts'
    usage = '%(prog)s [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-t', '--post-type', dest='post_type', action='store', type=str, default='', help='the comma separated types of post you want to describe. ')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default=None, help='the comma separated status of post you want to describe. ')
        return

    @classmethod
    def build_directive(cls, options):
        return {'post_type': explode_array(options.post_type), 
           'status': explode_array(options.status)}