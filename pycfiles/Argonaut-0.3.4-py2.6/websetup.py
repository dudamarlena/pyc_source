# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/websetup.py
# Compiled at: 2011-02-20 13:54:21
"""Setup the argonaut application"""
import logging, pylons.test
from argonaut.config.environment import load_environment
from argonaut.model.meta import Session, Base
from argonaut.model.initial_data import config_data, page_data, auth_data, box_data, boxes_data, page_type_data, media_data, social_data
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """
    
    To set up the application, you need to use the command:
    paster setup-app <config_file>:#arg
    
    This is due to a bug in pastedeploy (http://www.mail-archive.com/pylons-discuss@googlegroups.com/msg08524.html)
    
    """
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    Base.metadata.create_all(bind=Session.bind)
    config_data.init_data()
    page_type_data.init_data()
    page_data.init_data()
    auth_data.init_data()
    box_data.init_data()
    boxes_data.init_data()
    media_data.init_data()
    social_data.init_data()