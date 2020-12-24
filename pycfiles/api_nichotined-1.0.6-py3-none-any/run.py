# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/api_metadata/run.py
# Compiled at: 2017-11-27 05:10:38
__doc__ = ' Entry points for API metadata application. '
from ocs.api import app
from . import __version__, views
APPLICATION_INFO = app.ApplicationInfo(name='api_metadata', version=__version__, fluent_tag='ocs.api_metadata')

def app_factory(global_config, **local_conf):
    """ PasteDeploy entry point. """
    return wsgi


def debug():
    """ Development standalone server. """
    app_ = app.DebugApplication(APPLICATION_INFO)
    app_.register_views(views)
    app_.print_url_map()
    return app_.run(host='0.0.0.0', port=2222)


def wsgi(environ, start_response):
    """ PasteDeploy entry point. """
    app_ = getattr(wsgi, '_app', None)
    if not app_:
        app_ = app.WSGIApplication(APPLICATION_INFO)
        app_.register_views(views)
        setattr(wsgi, '_app', app_)
    return app_.run(environ, start_response)