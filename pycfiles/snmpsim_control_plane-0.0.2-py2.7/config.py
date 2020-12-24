# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim_control_plane/metrics/config.py
# Compiled at: 2020-01-14 13:16:07


class DefaultConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    SQLALCHEMY_ECHO = False
    DEBUG = False
    SNMPSIM_METRICS_LISTEN_IP = '127.0.0.1'
    SNMPSIM_METRICS_LISTEN_PORT = 5001
    SNMPSIM_METRICS_SSL_CERT = None
    SNMPSIM_METRICS_SSL_KEY = None