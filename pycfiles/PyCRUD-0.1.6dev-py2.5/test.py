# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/config/test.py
# Compiled at: 2008-06-20 03:40:59
import paste.deploy
from sqlalchemy import clear_mapper, create_engine, create_session
from sqlalchemy.ext.assignmapper import assign_mapper
from sqlalchemy.ext.sessioncontext import SessionContext
import pylons.database, quickwiki.models as model

def setup_config(command, filename, section, vars):
    """
    Place any commands to setup quickwiki here.
    """
    conf = paste.deploy.appconfig('config:' + filename)
    paste.deploy.CONFIG.push_process_config({'app_conf': conf.local_conf, 'global_conf': conf.global_conf})
    uri = conf['sqlalchemy.dburi']
    engine = create_engine(uri)
    print 'Connecting to database %s' % uri
    model.meta.connect(engine)
    print 'Creating tables'
    model.meta.create_all()
    clear_mapper(model.page_mapper)
    assign_mapper(SessionContext(lambda : create_session(bind_to=engine)), model.Page, model.pages_table)
    print 'Adding front page data'
    page = model.Page()
    page.title = 'FrontPage'
    page.content = 'Welcome to the QuickWiki front page.'
    page.flush()
    print 'Successfully setup.'