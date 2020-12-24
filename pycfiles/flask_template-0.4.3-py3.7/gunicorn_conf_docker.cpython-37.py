# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flask_template/templates/mongo/gunicorn_conf_docker.py
# Compiled at: 2020-04-01 02:43:02
# Size of source mod 2**32: 301 bytes
import logging
LOG_PATH = '/data/logs/proj'
PID_FILE = 'proj.pid'
bind = '%s:%s' % ('0.0.0.0', 80)
workers = 4
worker_connections = 100
preload_app = True
timeout = 600
deamon = False
debug = False
loglevel = 'info'
pidfile = '%s/%s' % (LOG_PATH, PID_FILE)
accesslog = '-'