# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/git/lib/python2.5/site-packages/hive/websetup.py
# Compiled at: 2011-07-08 01:47:53
"""Setup the hive application"""
import logging, pylons.test
from hive.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup hive here"""
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)