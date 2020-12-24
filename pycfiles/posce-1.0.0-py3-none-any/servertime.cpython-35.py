# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\procode\tools\servertime.py
# Compiled at: 2019-07-08 01:51:24
# Size of source mod 2**32: 1251 bytes
import datetime, threading, time

class ServerTime:
    is_request_system_flug = False
    close_flug = False
    server_time = datetime.datetime.now()


def updatetime():
    if ServerTime.is_request_system_flug:
        ServerTime.server_time = ServerTime.server_time + datetime.timedelta(seconds=1)
        timer = threading.Timer(1, updatetime)
        timer.start()


def get_time():
    if ServerTime.is_request_system_flug:
        return datetime.datetime.strftime(ServerTime.server_time, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


def get_date():
    if ServerTime.is_request_system_flug:
        return datetime.datetime.strftime(ServerTime.server_time, '%Y-%m-%d')
    else:
        return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')


def get_timestamp():
    if ServerTime.is_request_system_flug:
        return int(time.mktime(ServerTime.server_time.timetuple()) * 1000)
    else:
        return int(time.time() * 1000)


if __name__ == '__main__':
    ServerTime.server_time = datetime.datetime.strptime('2019-05-13 15:28:00', '%Y-%m-%d %H:%M:%S')
    get_time()