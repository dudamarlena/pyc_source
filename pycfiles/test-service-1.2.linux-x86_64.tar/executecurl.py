# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kylin/pyenvs/kylins-flask/lib/python2.7/site-packages/test_service/management/commands/executecurl.py
# Compiled at: 2015-02-14 10:30:19
"""读取存放测试脚本的文件, 以命令行的形式执行指定的行脚本, 指定范围的行脚本.
"""
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'
from django.core.management.base import BaseCommand
from test_service.curl_reader import curl_script
import six

class Command(BaseCommand):
    help = 'execute curl command script in saved file.'

    def handle(self, *args, **options):
        arg_len = len(args)
        arg_start, arg_count = (None, None)
        if arg_len == 2:
            try:
                arg_count = abs(int(args[1]))
            except (TypeError, ValueError):
                six.print_('Requires effective positive integer input.')
                return

        if arg_len > 0:
            try:
                arg_start = int(args[0])
            except (TypeError, ValueError):
                six.print_('Requires effective positive integer input.')
                return

        if arg_count:
            curl_script.run_script_lines(arg_start, arg_count)
        elif arg_start:
            curl_script.run_script_line(arg_start)
        else:
            curl_script.run_script_line()
        return