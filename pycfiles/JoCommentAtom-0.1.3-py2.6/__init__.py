# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jocommentatom/__init__.py
# Compiled at: 2010-12-27 16:35:31
from pyramid.configuration import Configurator
from pyramid.settings import asbool
from pyramid.exceptions import NotFound
from jocommentatom.models import initialize_db
from jocommentatom.views import atom_feed, notfound_view

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['site_url'] = settings.get('site_url').rstrip('/')
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    db_echo = settings.get('db_echo', 'false')
    initialize_db(db_string, asbool(db_echo))
    config = Configurator(settings=settings)
    config.add_route('home', '/', view=atom_feed, view_renderer='templates/atom_feed.pt')
    config.add_view(notfound_view, context=NotFound)
    return config.make_wsgi_app()