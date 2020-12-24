# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\helloworld\websetup.py
# Compiled at: 2010-11-24 19:43:46
"""Setup the helloworld application"""
import logging, pylons.test
from helloworld.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup helloworld here"""
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)