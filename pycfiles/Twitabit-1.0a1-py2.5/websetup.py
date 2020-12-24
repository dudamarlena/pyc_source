# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twitabit/websetup.py
# Compiled at: 2008-01-19 12:54:36
"""Setup the Twitabit application"""
import logging
from paste.deploy import appconfig
from pylons import config
from twitabit.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup twitabit here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)