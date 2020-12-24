# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/refaction/websetup.py
# Compiled at: 2008-09-15 10:45:09
"""Setup the Refaction application"""
import logging, paste.deploy
from paste.deploy import appconfig
from pylons import config
from refaction.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup refaction here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    paste.deploy.CONFIG.push_process_config({'app_conf': conf.local_conf, 'global_conf': conf.global_conf})
    from refaction import model
    engine = config['pylons.g'].sa_engine
    print 'Creating database tables'
    model.meta.create_all(bind=engine)
    print 'Creating default entries'
    role = model.Role(name='admin')
    role.save()
    role = model.Role(name='manager')
    role.save()
    role = model.Role(name='subscriber')
    role.save()
    role = model.Role(name='member')
    role.save()
    try:
        from crypt import crypt
        password = unicode(crypt('admin', 'AA'))
    except ImportError:
        password = 'admin'

    user = model.User(name='admin', password=password, role=1)
    user.save()
    model.Session.commit()