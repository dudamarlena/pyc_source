# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pytest_gui_status\utils.py
# Compiled at: 2016-01-13 15:25:21
import os
env_redis_port = os.environ.get('PYTEST_STATUS_PORT')
if env_redis_port:
    REDIS_PORT = int(env_redis_port)
else:
    REDIS_PORT = 5946
REDIS_PATH = os.environ.get('REDIS_PATH') or 'redis-server'
REDIS_ARGS = os.environ.get('REDIS_ARGS') or ''
command_redis_server_gen = '{REDIS_PATH} --port {REDIS_PORT} {REDIS_ARGS}'
command_redis_server = command_redis_server_gen.format(REDIS_PATH=REDIS_PATH, REDIS_ARGS=REDIS_ARGS, REDIS_PORT=REDIS_PORT)
command_status_gui_gen = 'pytest_gui_status "{norm_dir_name}"'

def s(input_):
    """ Convert str or uncode or bytes to str.
    If list, do it for all of them.
    If others, return as is. """
    import sys
    PY3 = sys.version_info > (3, )
    if isinstance(input_, list):
        return [ s(ele) for ele in input_ ]
    try:
        if PY3:
            assert type(input_) in [str, bytes]
        else:
            assert type(input_) in [str, unicode, bytes]
    except AssertionError:
        return input_

    if PY3:
        if type(input_) == bytes:
            str_ = bytes.decode(input_)
            return str_
    str_ = str(input_)
    return str_