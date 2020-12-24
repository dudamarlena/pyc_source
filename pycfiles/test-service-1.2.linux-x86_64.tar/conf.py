# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kylin/pyenvs/kylins-flask/lib/python2.7/site-packages/test_service/conf.py
# Compiled at: 2015-02-14 10:28:07
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'
import os
from os.path import join, dirname
from django.conf import settings
from django.utils.importlib import import_module

def project_path():
    u"""获取项目目录."""
    setting_module = os.environ.get('DJANGO_SETTINGS_MODULE')
    project_catalog = os.path.dirname(import_module(setting_module).__file__)
    return project_catalog


project_path = project_path()
service_debug = settings.DEBUG
post_data_print = getattr(settings, 'POST_DATA_PRINT', True)
post_data_saved = getattr(settings, 'POST_DATA_SAVED', True)
exec_time_print = getattr(settings, 'EXEC_TIME_PRINT', True)
save_rows_queue = getattr(settings, 'SAVE_ROWS_QUEUE', 5)
login_api = getattr(settings, 'LOGIN_API', None)
logout_api = getattr(settings, 'LOGOUT_API', None)
time_report = getattr(settings, 'TIME_REPORT', join(dirname(project_path), 'report', 'report_time.md'))
curl_report = getattr(settings, 'CURL_REPORT', join(dirname(project_path), 'report', 'report_curl.md'))
converge_conf = {'output_file_name': 'convert.py', 
   'is_distinct_sort': True, 
   'data_format_string': 'echo "    (%s, u\'%s\'), " >> %s'}
converge_list = getattr(settings, 'CONVERGE_LIST', None)