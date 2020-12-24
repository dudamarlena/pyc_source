# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/toughcli/settings.py
# Compiled at: 2016-04-11 21:00:30
RUNDIR = '/home/toughrun'
DOCKER_OPS = ['', 'ps', 'config', 'pull', 'logs', 'start', 'stop', 'restart', 'kill', 'rm', 'down', 'pause', 'unpause']
MYSQL_OPS = DOCKER_OPS + ['status', 'backup', 'showdbs', 'makedb', 'upgrade']
REDIS_OPS = DOCKER_OPS + ['status']
RADIUS_OPS = DOCKER_OPS + ['status', 'upgrade']
WLAN_OPS = DOCKER_OPS + ['status', 'upgrade']