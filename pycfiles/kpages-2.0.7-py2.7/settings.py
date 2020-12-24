# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kpages/settings.py
# Compiled at: 2019-01-22 20:27:35
"""
    系统配置文件

    不建议修改本文件，应用设置应该保存在 /settings.py 应用配置文件中。
    应用配置会覆盖同名的系统配置。

"""
PORT = 8088
BIND_IP = None
SOCK_TIMEOUT = 10
SOCK_TIMEOUT_MS = None
CPU_MULTIPLE = 5
SESSION_EXPIRE = 2592000
DEBUG = True
GZIP = True
ACTION_DIR = ('action', )
JOB_DIR = 'logic'
UTEST_DIR = 'utest'
STATIC_DIR_NAME = 'static'
TEMPLATE_DIR_NAME = 'template'
COOKIE_SECRET = '61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo='
XSRF_COOKIES = False
PERSISTENT_DB_CONNECTION = False
CACHE_HOST = 'localhost'
DB_HOST = 'localhost'
DB_NAME = 'test'
GFS_NAME = DB_NAME
SERVICE_CHANNEL = 'channel1'
SERVICE_LISTKEY = 'kpages_cmd_list'
max_buffer_size = 1048576000
RPC_PORT = 8080
RPC_DIR = ('rpc', )