# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kylin/pyenvs/kylins-flask/lib/python2.7/site-packages/test_service/curl_builder.py
# Compiled at: 2015-02-14 06:55:16
from __future__ import unicode_literals
__author__ = b'kylinfish@126.com'
__date__ = b'2014/11/08'
import os
from datetime import datetime
import six
from .conf import curl_report, login_api, logout_api, save_rows_queue
if six.PY3:
    from queue import Queue
else:
    from Queue import Queue

class DataStore(object):
    """数据行存储类.
    """

    def __init__(self, report_file, maxsize=5):
        super(DataStore, self).__init__()
        self._report_file = report_file
        self._lines_store = Queue(maxsize=maxsize)
        dir_path = os.path.dirname(self._report_file)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def get_report_file(self):
        return self._report_file

    def open_file_data(self):
        u"""读取报告文件
        """
        if os.path.exists(self._report_file):
            read_file = open(self._report_file, b'rb')
            return read_file.readlines()
        else:
            return

    def save_line_data(self, line):
        u"""保存行数据.

            :param line
        """
        if not self._lines_store.full():
            self._lines_store.put(line)
        if self._lines_store.full():
            self.save_file_data()

    def save_file_data(self):
        u"""存储数据到文件.
        """
        with open(self._report_file, b'ab') as (f):
            if not self._lines_store.empty():
                log_time = b'#### %s\n' % str(datetime.now())
                f.write(log_time)
            while not self._lines_store.empty():
                one = self._lines_store.get()
                f.write(b'\t%s' % one)


class RequireStore(DataStore):
    """拦截request, 构建curl脚本, 并存储类.
    """
    _LOGIN_API = login_api
    _LOGOUT_API = logout_api

    def __init__(self, report_file, maxsize=0, cookie=None):
        super(RequireStore, self).__init__(report_file, maxsize)
        self.cookie = cookie

    def hold_data_require(self, request, request_url=None, data=None):
        u"""构建脚本, 生成curl 命令行.

            :param request
            :param request_url
            :param data

            仅支持:
            method: GET/POST 其它如有需要待扩展
            protocol: http/https 其它不考虑
        """
        line = b'curl '
        if self.cookie:
            if request.get_full_path() in self._LOGIN_API + self._LOGOUT_API:
                line = (b'').join((line, b'-D %s ' % self.cookie))
            else:
                line = (b'').join((line, b'-b %s ' % self.cookie))
        if request.method == b'POST' and data:
            line = (b'').join((line, b'-d "%s" ' % data))
        elif request.method == b'GET' and data:
            line = (b'').join((line, b'-G "%s" ' % data))
        if not request_url:
            protocol = b'http://' if not request.is_secure() else b'https://'
            request_url = b'%s%s%s' % (protocol, request.get_host(), request.get_full_path())
        line = (b'').join((line, request_url))
        return line


def sole_file_data(instance, orig_sign, sole_sign):
    u"""对拦截curl记录保存文件, 做处理去掉重复行.

        :param instance: DataStore实例
        :param orig_sign: 老文件标识
        :param sole_sign: 新文件标识
    """
    lines = instance.open_file_data()
    if lines:
        sole_file = instance.get_report_file().replace(orig_sign, sole_sign)
        if os.path.exists(sole_file):
            os.remove(sole_file)
        six.print_(b'Original: %s' % len(lines))
        sole_data = set(lines)
        num_date = 0
        with open(sole_file, b'ab') as (rf):
            for _line_ in sole_data:
                if _line_.startswith(b'####'):
                    num_date += 1
                    continue
                rf.write(_line_)

        six.print_(b'Nowadays: %s' % (len(sole_data) - num_date))
        six.print_(b'All is Ok')
    else:
        six.print_(b'Data is None')


cur_instance = RequireStore(report_file=curl_report, maxsize=save_rows_queue, cookie=b'./log/cookie.txt')