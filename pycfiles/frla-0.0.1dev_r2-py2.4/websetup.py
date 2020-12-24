# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/websetup.py
# Compiled at: 2008-09-22 06:43:33
"""Setup the frla application"""
import logging
from paste.deploy import appconfig
from pylons import config
from frla.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup frla here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)