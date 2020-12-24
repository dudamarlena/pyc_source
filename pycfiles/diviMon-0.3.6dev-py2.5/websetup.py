# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/websetup.py
# Compiled at: 2008-08-07 05:50:38
"""Setup the diviMon application"""
import logging, paste.deploy
from paste.deploy import appconfig
from pylons import config
from divimon.config.environment import load_environment
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup divimon here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    paste.deploy.CONFIG.push_process_config({'app_conf': conf.local_conf, 'global_conf': conf.global_conf})
    from divimon import model
    engine = config['pylons.g'].sa_engine
    print 'Creating database tables'
    model.meta.create_all(bind=engine)
    print 'Creating default entries'
    role = model.Role(name='admin')
    model.Session.save(role)
    role = model.Role(name='sales')
    model.Session.save(role)
    role = model.Role(name='warehouse')
    model.Session.save(role)
    try:
        from crypt import crypt
        password = unicode(crypt('admin', 'AA'))
    except ImportError:
        password = 'admin'

    user = model.User(name='admin', password=password, role=1)
    model.Session.save(user)
    model.Session.commit()
    for t in ('Delivery Order', 'Delivery Receipt', 'Delivery Receipt Confirmed'):
        entry = model.TransType(name=unicode(t))
        model.Session.save(entry)

    for p in ('COD', 'Credit', 'Cheque'):
        entry = model.PayType(name=unicode(p))
        model.Session.save(entry)

    for ps in ('Unpaid', 'Paid'):
        entry = model.PayStatus(name=unicode(ps))
        model.Session.save(entry)

    for cnt in range(1, 4):
        entry = model.Area(name='Area %s' % cnt)
        model.Session.save(entry)
        agent = model.Agent(name='Agent %s' % cnt, area=cnt)
        model.Session.save(agent)
        customer = model.Customer(name='Customer %s' % cnt, area=cnt)
        model.Session.save(customer)

    for cheque_status in ('Unclaimed', 'Claimed', 'For Return', 'Returned'):
        entry = model.Cheque_status(name=unicode(cheque_status))
        model.Session.save(entry)

    model.Session.commit()