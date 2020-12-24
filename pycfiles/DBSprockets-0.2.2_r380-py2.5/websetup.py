# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/dbmechanic/frameworks/tg2/test/TG2TestApp/tg2testapp/websetup.py
# Compiled at: 2008-06-30 11:43:47
"""Setup the TG2TestApp application"""
import logging
from paste.deploy import appconfig
from pylons import config
from tg2testapp.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup tg2testapp here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    from tg2testapp import model
    print 'Creating tables'
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)
    model.DBSession.commit()
    print 'Successfully setup'