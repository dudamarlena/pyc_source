# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/utils/tools.py
# Compiled at: 2018-11-28 04:21:54
import time, socket

def parse_time(timestamp):
    try:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    except Exception:
        return '0000-00-00 00:00:00'


def get_time():
    return parse_time(time.time())


flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) or isinstance(L, tuple) else [L]

def get_hostname():
    try:
        return (';').join(flat(socket.gethostbyname_ex(socket.gethostname())))
    except Exception:
        return socket.gethostname()


if __name__ == '__main__':
    print get_time()