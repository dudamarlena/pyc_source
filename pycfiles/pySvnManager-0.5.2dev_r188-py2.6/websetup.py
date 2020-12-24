# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/websetup.py
# Compiled at: 2010-08-08 03:18:44
"""Setup the pySvnManager application"""
import logging, pylons.test
from pysvnmanager.config.environment import load_environment
from paste.deploy import appconfig
from shutil import copyfile
import os
from pkg_resources import resource_filename
from pysvnmanager.config.environment import load_environment
from pysvnmanager.model.meta import Session, metadata, Base
from pysvnmanager import model
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup pysvnmanager here"""
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    else:
        from pylons import config
        wsgiapp = pylons.test.pylonsapp
        config['here'] = wsgiapp.config.get('here')
    here = conf['here']
    if not os.path.exists(here + '/config'):
        os.mkdir(here + '/config')
    if not os.path.exists(here + '/config/RCS'):
        os.mkdir(here + '/config/RCS')
    if not os.path.exists(here + '/svnroot'):
        os.mkdir(here + '/svnroot')
    filelist = [
     'svn.access', 'svn.passwd', 'localconfig.py']
    for f in filelist:
        src = resource_filename('pysvnmanager', 'config/' + f + '.in')
        dest = here + '/config/' + f
        if os.path.exists(dest):
            log.warning('Warning: %s already exist, ignored.' % f)
        else:
            copyfile(src, dest)

    log.info('Creating tables...')
    Base.metadata.create_all(bind=Session.bind)
    log.info('Successfully set up.')