# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/subicpos/websetup.py
# Compiled at: 2008-05-21 22:43:52
"""Setup the SubicPOS application"""
import logging, paste.deploy
from paste.deploy import appconfig
from pylons import config
from subicpos.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup subicpos here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    paste.deploy.CONFIG.push_process_config({'app_conf': conf.local_conf, 'global_conf': conf.global_conf})
    from subicpos import model
    engine = config['pylons.g'].sa_engine
    print 'Creating database tables'
    model.meta.create_all(bind=engine)
    print 'Creating default entries'
    for t in ('Fuel', 'Service', 'Treats', 'Delivered', 'Returns', 'Waste', 'Consumed'):
        entry = model.TransType(name=unicode(t))
        model.Session.save(entry)

    for c in ('Fuel', 'Service', 'Treats'):
        entry = model.Classification(name=unicode(c))
        model.Session.save(entry)

    for p in ('Cash', 'Card', 'Cheque', 'Fleet'):
        entry = model.PayType(name=unicode(p))
        model.Session.save(entry)

    entry = model.Branch(name='Branch 1')
    model.Session.save(entry)
    model.Session.commit()