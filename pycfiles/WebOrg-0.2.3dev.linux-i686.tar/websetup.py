# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/websetup.py
# Compiled at: 2011-07-12 22:16:02
"""Setup the WebOrg application"""
import logging, pylons.test
from weborg.config.environment import load_environment
from weborg.model.meta import Session, Base
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup weborg here"""
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    Base.metadata.create_all(bind=Session.bind)