# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blobs/websetup.py
# Compiled at: 2008-02-19 12:19:12
"""Setup the Houdini File Server application"""
import logging
from paste.deploy import appconfig
from pylons import config
from blobs.wsgiapp import load_environment
from blobs import model
log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    print 'Creating database in', config['sqlalchemy.url']
    model.meta.create_all()