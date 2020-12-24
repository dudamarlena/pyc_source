# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/websetup.py
# Compiled at: 2010-12-12 22:28:56
"""Setup the synthesis application"""
import logging, pylons.test
from config.environment import load_environment
from model.meta import Session, Base
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup synthesis here"""
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    Base.metadata.create_all(bind=Session.bind)