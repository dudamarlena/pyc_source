# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/websetup.py
# Compiled at: 2008-06-20 03:41:00
__doc__ = 'Setup the PyCRUD application'
import logging, paste.deploy
from paste.deploy import appconfig
from pylons import config
from pycrud.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup pycrud here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    paste.deploy.CONFIG.push_process_config({'app_conf': conf.local_conf, 'global_conf': conf.global_conf})
    from pycrud import model
    engine = config['pylons.g'].sa_engine
    print 'Creating tables'
    model.meta.create_all(bind=engine)
    print 'Adding default folders'
    for f in ('Inbox', 'Archive', 'Outbox', 'Sent'):
        folder = model.Folder(name=f, commend=f)
        model.Session.save(folder)
        model.Session.commit()

    print 'Successfully setup.'