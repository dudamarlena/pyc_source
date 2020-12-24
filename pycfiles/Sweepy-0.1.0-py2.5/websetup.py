# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sweepy/websetup.py
# Compiled at: 2009-10-21 07:41:19
"""Setup the Sweepy application"""
import logging
from sweepy.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup sweepy here"""
    load_environment(conf.global_conf, conf.local_conf)