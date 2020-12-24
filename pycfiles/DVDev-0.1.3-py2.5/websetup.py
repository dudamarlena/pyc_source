# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/dvdev/websetup.py
# Compiled at: 2009-04-17 21:05:49
"""Setup the DVDev application"""
import logging
from dvdev.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup dvdev here"""
    load_environment(conf.global_conf, conf.local_conf)