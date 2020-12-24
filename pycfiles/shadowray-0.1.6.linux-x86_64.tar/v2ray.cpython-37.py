# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mt/PycharmProjects/Shadowray/venv/lib/python3.7/site-packages/shadowray/config/v2ray.py
# Compiled at: 2019-06-22 10:10:48
# Size of source mod 2**32: 891 bytes
import os
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
USER_HOME = os.path.expanduser('~')
SHADOWRAY_CONFIG_FOLDER = os.path.join(PROJECT_PATH, '.shadowray')
V2RAY_FOLDER = os.path.join(SHADOWRAY_CONFIG_FOLDER, 'v2ray')
V2RAY_BINARY = os.path.join(V2RAY_FOLDER, 'v2ray')
V2CTL_BINARY = os.path.join(V2RAY_FOLDER, 'v2ctl')
EXECUTE_ARGS = '-config=stdin:'
RESOURCES_FOLDER = os.path.join(SHADOWRAY_CONFIG_FOLDER, 'resources')
SUBSCRIBE_FILE = os.path.join(RESOURCES_FOLDER, 'subscribes.json')
SERVER_FILE = os.path.join(RESOURCES_FOLDER, 'servers.json')
PROJECT_CONFIG_FILE = os.path.join(SHADOWRAY_CONFIG_FOLDER, 'config.json')
SERVER_KEY_FROM_ORIGINAL = 'servers_original'
SERVER_KEY_FROM_SUBSCRIBE = 'servers_subscribe'
V2RAY_PID_FILE = os.path.join(SHADOWRAY_CONFIG_FOLDER, 'pid')
CONFIG_STREAM_FILE = os.path.join(SHADOWRAY_CONFIG_FOLDER, 'stdin')