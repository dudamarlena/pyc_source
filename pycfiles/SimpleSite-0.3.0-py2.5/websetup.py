# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesite/websetup.py
# Compiled at: 2008-11-08 16:42:54
"""Setup the SimpleSite application"""
import logging, os.path
from simplesite import model
from simplesite.config.environment import load_environment
from authkit.users.sqlalchemy_driver import UsersFromDatabase
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup simplesite here"""
    load_environment(conf.global_conf, conf.local_conf)
    from simplesite.model import meta
    meta.metadata.bind = meta.engine
    log.info('Adding the AuthKit model...')
    users = UsersFromDatabase(model)
    filename = os.path.split(conf.filename)[(-1)]
    if filename == 'test.ini':
        log.info('Dropping existing tables...')
        meta.metadata.drop_all(checkfirst=True)
    meta.metadata.create_all(checkfirst=True)
    log.info('Adding roles and uses...')
    users.role_create('delete')
    users.user_create('foo', password='bar')
    users.user_create('admin', password='opensesame')
    users.user_add_role('admin', role='delete')
    log.info('Adding tags...')
    tag1 = model.Tag()
    tag1.name = 'Pylons'
    meta.Session.add(tag1)
    tag2 = model.Tag()
    tag2.name = 'Paste'
    meta.Session.add(tag2)
    tag3 = model.Tag()
    tag3.name = 'Tutorial'
    meta.Session.add(tag3)
    tag4 = model.Tag()
    tag4.name = 'Database'
    meta.Session.add(tag4)
    tag5 = model.Tag()
    tag5.name = 'Recipe'
    meta.Session.add(tag5)
    log.info('Adding homepage...')
    section_home = model.Section()
    section_home.path = ''
    section_home.name = 'Home Section'
    meta.Session.add(section_home)
    meta.Session.flush()
    page_contact = model.Page()
    page_contact.title = 'Contact Us'
    page_contact.path = 'contact'
    page_contact.name = 'Contact Us Page'
    page_contact.content = 'Contact us page'
    page_contact.section = section_home.id
    meta.Session.add(page_contact)
    meta.Session.flush()
    section_dev = model.Section()
    section_dev.path = 'dev'
    section_dev.name = 'Development Section'
    section_dev.section = section_home.id
    section_dev.before = page_contact.id
    meta.Session.add(section_dev)
    meta.Session.flush()
    page_svn = model.Page()
    page_svn.title = 'SVN Page'
    page_svn.path = 'svn'
    page_svn.name = 'SVN Page'
    page_svn.content = 'This is the SVN page.'
    page_svn.section = section_dev.id
    meta.Session.add(page_svn)
    meta.Session.flush()
    page_dev = model.Page()
    page_dev.title = 'Development Home'
    page_dev.path = 'index'
    page_dev.name = 'Development Page'
    page_dev.content = 'This is the development home page.'
    page_dev.section = section_dev.id
    page_dev.before = page_svn.id
    meta.Session.add(page_dev)
    meta.Session.flush()
    page_home = model.Page()
    page_home.title = 'Home'
    page_home.path = 'index'
    page_home.name = 'Home'
    page_home.content = 'Welcome to the SimpleSite home page.'
    page_home.section = section_home.id
    page_home.before = section_dev.id
    meta.Session.add(page_home)
    meta.Session.flush()
    meta.Session.commit()
    log.info('Successfully set up.')