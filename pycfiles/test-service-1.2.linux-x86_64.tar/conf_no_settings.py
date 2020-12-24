# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kylin/pyenvs/kylins-flask/lib/python2.7/site-packages/test_service/conf_no_settings.py
# Compiled at: 2015-02-14 10:29:21
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/14'
import os
from os.path import join, dirname
project_path = os.path.dirname(os.path.abspath(__file__))
service_debug = True
post_data_print = True
post_data_saved = True
exec_time_print = True
save_rows_queue = 5
LOGIN_API = ('/user/login/', '/user/join/')
LOGOUT_API = ('/user/logout/', )
time_report = join(dirname(project_path), 'report', 'report_time.md')
curl_report = join(dirname(project_path), 'report', 'report_curl.md')
converge_conf = {'output_file_name': 'convert.py', 
   'is_distinct_sort': True, 
   'data_format_string': 'echo "    (%s, u\'%s\'), " >> %s'}
converge_file = [
 'views.py']
converge_list = [ os.path.join(os.path.join(project_path, 'demo'), uni_file) for uni_file in converge_file ]