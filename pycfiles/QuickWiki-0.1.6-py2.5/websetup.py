# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/quickwiki/websetup.py
# Compiled at: 2009-02-23 12:50:50
"""Setup the QuickWiki application"""
import logging
from quickwiki import model
from quickwiki.config.environment import load_environment
from quickwiki.model import meta
log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup quickwiki here"""
    load_environment(conf.global_conf, conf.local_conf)
    log.info('Creating tables...')
    meta.metadata.create_all(bind=meta.engine)
    log.info('Successfully set up.')
    log.info('Adding front page data...')
    page = model.Page(title='FrontPage', content='**Welcome** to the QuickWiki front page!')
    meta.Session.add(page)
    meta.Session.commit()
    log.info('Successfully set up.')