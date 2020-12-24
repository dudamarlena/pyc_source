# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/scripts/base.py
# Compiled at: 2008-06-20 03:40:59
"""base.py - base module for various utilities
"""
from sys import argv
import paste.deploy
from paste.deploy import appconfig
from pylons import config
from sqlchemistry import Config, Environment
from pycrud.config.environment import load_environment
(INBOX, ARCHIVE, OUTBOX) = range(1, 4)
NUMBER = '09283205839'
SERVER_CONF = '/etc/pycrud/server.ini'
CUSTOM_CONF = '/etc/pycrud/custom.ini'
custom_env = Environment(Config(CUSTOM_CONF))
space_sub = '_'

def setup(filename=SERVER_CONF):
    global model
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    paste.deploy.CONFIG.push_process_config({'app_conf': conf.local_conf, 'global_conf': conf.global_conf})
    from pycrud import model
    return model