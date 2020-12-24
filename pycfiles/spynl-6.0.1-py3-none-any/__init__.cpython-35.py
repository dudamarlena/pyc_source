# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/__init__.py
# Compiled at: 2017-01-30 10:34:06
# Size of source mod 2**32: 3476 bytes
"""The main package of Spynl."""
import os.path
from pyramid.config import Configurator
from pyramid.settings import asbool
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.viewderivers import INGRESS
from spynl.main import plugins, serial, about, routing, events, endpoints, session
from spynl.main.utils import renderer_factory, check_origin, handle_pre_flight_request
from spynl.main.exceptions import SpynlException
from spynl.main.error_views import spynl_error, error400, error500
from spynl.main.validation import validate_json_schema
from spynl.main.docs.documentation import make_docs
from spynl.main.docs.settings import check_required_settings
from spynl.main.dateutils import now
from spynl.main.locale import TemplateTranslations

def main(global_config, test_settings=None, **settings):
    """
    Return a Pyramid WSGI application.

    Before that, we tell plugins how to add a view and tell views which
    renderer to use. And we take care of test settings. Then, we initialise the
    main plugins and the external plugins (which are not in this repository).
    """
    config = Configurator(settings=settings)
    config.add_settings({'spynl.ops.start_time': now()})
    if test_settings:
        for key, value in test_settings.items():
            config.add_settings({key: value})

    config.add_view_deriver(validate_json_schema)
    config.add_view_deriver(handle_pre_flight_request, under=INGRESS)
    config.add_view_deriver(check_origin)
    routing.main(config)
    events.main(config)
    serial.main(config)
    endpoints.main(config)
    about.main(config)
    plugins.main(config)
    session.main(config)
    check_required_settings(config)
    config.add_renderer('spynls-renderer', renderer_factory)
    config.add_translation_dirs('spynl.main:locale/')
    config.add_view(error400, context='pyramid.httpexceptions.HTTPError', renderer='spynls-renderer', permission=NO_PERMISSION_REQUIRED, is_error_view=True)
    config.add_view(spynl_error, context=SpynlException, renderer='spynls-renderer', permission=NO_PERMISSION_REQUIRED, is_error_view=True)
    config.add_view(error500, context=Exception, renderer='spynls-renderer', permission=NO_PERMISSION_REQUIRED, is_error_view=True)
    make_docs(config)
    config.include('pyramid_jinja2')
    config.add_settings({'jinja2.filters': {'static_url': 'pyramid_jinja2.filters:static_url_filter'}, 
     'jinja2.i18n.gettext': TemplateTranslations})
    if test_settings:
        config.include('pyramid_mailer.testing')
    else:
        config.include('pyramid_mailer')
    config.commit()
    config.registry.notify(plugins.PluginsLoaded(config))
    return config.make_wsgi_app()