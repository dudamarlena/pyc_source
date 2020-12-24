# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/websetup.py
# Compiled at: 2008-03-10 19:54:16
"""Setup the SalvationFocus application"""
import logging
from paste.deploy import appconfig
from pylons import config
from salvationfocus.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup salvationfocus here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    import salvationfocus.model as model
    from model import Administrator
    import hashlib
    log.info('Setting up database connectivity...')
    engine = config['pylons.g'].sa_engine
    log.info('Creating tables...')
    model.metadata.create_all(bind=engine)
    log.info('Successfully set up.')
    log.info('Adding initial Administrator...')
    password = 'password'
    pass_hash = hashlib.sha256(password).hexdigest()
    admin = Administrator()
    admin.login_name = 'admin'
    admin.password_hash = pass_hash
    admin.email = 'your_email@your_domain.com'
    model.Session.save(admin)
    model.Session.commit()
    log.info('Successfully set up.')