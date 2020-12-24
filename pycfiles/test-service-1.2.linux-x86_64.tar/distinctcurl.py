# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kylin/pyenvs/kylins-flask/lib/python2.7/site-packages/test_service/management/commands/distinctcurl.py
# Compiled at: 2015-02-14 10:30:19
"""对拦截curl记录保存文件, 做处理去掉重复行.
"""
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'
from django.core.management.base import NoArgsCommand
from test_service.curl_builder import sole_file_data, cur_instance

class Command(NoArgsCommand):
    help = '对拦截curl记录保存文件, 做处理去掉重复行.'

    def handle_noargs(self, **options):
        sole_file_data(cur_instance, '_curl.md', '_sole.md')