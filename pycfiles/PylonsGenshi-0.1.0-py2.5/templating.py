# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylonsgenshi/templating.py
# Compiled at: 2008-01-03 15:16:04
import os, pylons
from genshi.filters import Translator
from genshi.template import TemplateLoader, Context
import logging
log = logging.getLogger(__name__)

def template_loaded(template):
    template.filters.insert(0, Translator(pylons.i18n.ugettext))


loader = TemplateLoader(search_path=pylons.config['pylons.paths']['templates'], auto_reload=True, callback=template_loaded)

def _update_names(ns):
    """Return a dict of Pylons vars and their respective objects updated
    with the ``ns`` dict."""
    d = dict(c=pylons.c._current_obj(), g=pylons.g._current_obj(), h=pylons.config.get('pylons.h') or pylons.h._current_obj(), render=render, request=pylons.request._current_obj(), translator=pylons.translator._current_obj(), ungettext=pylons.i18n.ungettext, _=pylons.i18n._, N_=pylons.i18n.N_)
    if pylons.config['pylons.environ_config'].get('session', True):
        d['session'] = pylons.session._current_obj()
    d.update(ns)
    log.debug('Updated render namespace with pylons vars: %s', d)
    return Context(**d)


def render(filename, method='xhtml', encoding='utf-8', **options):
    template = loader.load(filename.replace('.', os.sep) + '.html', encoding=encoding)
    if not options:
        options = {}
    engine_dict = Context()
    return template.generate(engine_dict)