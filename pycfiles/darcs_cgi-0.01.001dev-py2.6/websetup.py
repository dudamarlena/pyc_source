# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/darcscgi/websetup.py
# Compiled at: 2009-09-11 13:58:44
"""Setup the darcs-cgi application"""
import logging
from darcscgi.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup darcscgi here"""
    load_environment(conf.global_conf, conf.local_conf)