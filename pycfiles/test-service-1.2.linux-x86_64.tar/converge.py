# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kylin/pyenvs/kylins-flask/lib/python2.7/site-packages/test_service/management/commands/converge.py
# Compiled at: 2015-02-14 10:30:19
"""从源码文件中生成 消息码/消息文本配置信息.
"""
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'
from django.core.management.base import NoArgsCommand
from test_service.conf import converge_list
from test_service.converge import ConvergeSRC

class Command(NoArgsCommand):
    help = '从源码文件中生成 消息码/消息文本配置信息.'

    def handle_noargs(self, **options):
        ConvergeSRC(converge_list).exec_script_line()