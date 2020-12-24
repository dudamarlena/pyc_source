# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/net/www/util.py
# Compiled at: 2016-07-25 12:05:26
"""Common WWW/CGI utilities"""
from __future__ import print_function
import sys, os

def exception(str=''):
    if sys.exc_type == SystemExit:
        return
    print('Content-Type: text/html\n')
    import html
    print(html.exception())
    if str:
        print(str)
    sys.exit(1)


def error(err_str):
    if not err_str:
        err_str = 'Unknown error'
    print('Content-Type: text/html\n')
    print(str(err_str))
    sys.exit(1)


def get_redirect(_str=''):
    server_name = os.environ['SERVER_NAME']
    server_port = os.environ['SERVER_PORT']
    if server_port == '80':
        server_port = ''
    else:
        server_port = ':' + server_port
    return 'http://' + server_name + server_port + _str


def convert_empty(estr):
    if estr:
        _str = str(estr)
    else:
        _str = '&nbsp;'
    return _str


def gen_html(title, body):
    print('\n   <HTML>\n      <HEAD>\n         <TITLE>\n            %s\n         </TITLE>\n      </HEAD>\n\n      <BODY>\n         %s\n      </BODY>\n   </HTML>\n   ' % (title, body))


def mkexpires(hours=1, minutes=0, seconds=0):
    from datetime import datetime, timedelta
    expire = datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return 'Expires: %s' % expire.strftime('%a, %d %b %Y %H:%M:%S GMT')


def parse_time(t):
    import time
    for format in ('%a, %d %b %Y %H:%M:%S GMT', '%A, %d-%b-%y %H:%M:%S GMT', '%A, %d-%b-%Y %H:%M:%S GMT'):
        try:
            return time.mktime(time.strptime(t, format)) - time.timezone
        except (ValueError, OverflowError):
            pass

    return