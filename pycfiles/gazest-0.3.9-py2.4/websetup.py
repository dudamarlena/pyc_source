# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/websetup.py
# Compiled at: 2007-10-25 12:41:27
"""Setup the gazest application"""
import logging
from paste.deploy import appconfig
from pylons import config
from gazest.config.environment import load_environment
import extra_data
from pkg_resources import resource_string
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup gazest here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    from gazest import model
    model.meta.create_all(bind=config['pylons.g'].sa_engine)
    stub_rev = model.RevNode()
    resource_string(extra_data.__name__, 'default_not_found_page.txt')
    stub_rev.body = resource_string(extra_data.__name__, 'default_stub_page.txt')
    not_found_rev = model.RevNode()
    not_found_rev.body = resource_string(extra_data.__name__, 'default_not_found_page.txt')
    ns = model.Namespace(stub_rev=stub_rev, not_found_rev=not_found_rev, slug='', wikiprefix='def', name='default namespace')
    model.db_sess.commit()