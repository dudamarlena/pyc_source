# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/template.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 6514 bytes
import six, jinja2
from jinja2.ext import Extension
from jinja2.nodes import Include, Const
from babel.localedata import exists
from werkzeug.urls import url_quote_plus
from mediagoblin import mg_globals
from mediagoblin import messages
from mediagoblin import _version
from mediagoblin.tools import common
from mediagoblin.tools.translate import is_rtl
from mediagoblin.tools.translate import set_thread_locale
from mediagoblin.tools.pluginapi import get_hook_templates, hook_transform
from mediagoblin.tools.timesince import timesince
from mediagoblin.meddleware.csrf import render_csrf_form_token
SETUP_JINJA_ENVS = {}

def get_jinja_env(app, template_loader, locale):
    """
    Set up the Jinja environment,

    (In the future we may have another system for providing theming;
    for now this is good enough.)
    """
    set_thread_locale(locale)
    if locale in SETUP_JINJA_ENVS:
        return SETUP_JINJA_ENVS[locale]
    jinja2_config = app.global_config.get('jinja2', {})
    local_exts = jinja2_config.get('extensions', [])
    template_env = jinja2.Environment(loader=template_loader, autoescape=True, undefined=jinja2.StrictUndefined, extensions=[
     'jinja2.ext.i18n', 'jinja2.ext.autoescape',
     TemplateHookExtension] + local_exts)
    if six.PY2:
        template_env.install_gettext_callables(mg_globals.thread_scope.translations.ugettext, mg_globals.thread_scope.translations.ungettext)
    else:
        template_env.install_gettext_callables(mg_globals.thread_scope.translations.gettext, mg_globals.thread_scope.translations.ngettext)
    template_env.globals['fetch_messages'] = messages.fetch_messages
    template_env.globals['app_config'] = app.app_config
    template_env.globals['global_config'] = app.global_config
    template_env.globals['version'] = _version.__version__
    template_env.globals['auth'] = app.auth
    template_env.globals['is_rtl'] = is_rtl(locale)
    template_env.filters['urlencode'] = url_quote_plus
    template_env.globals['timesince'] = timesince
    template_env.globals['get_hook_templates'] = get_hook_templates
    template_env.globals = hook_transform('template_global_context', template_env.globals)
    from mediagoblin import notifications
    template_env.globals['get_notifications'] = notifications.get_notifications
    template_env.globals['get_notification_count'] = notifications.get_notification_count
    template_env.globals['get_comment_subscription'] = notifications.get_comment_subscription
    if exists(locale):
        SETUP_JINJA_ENVS[locale] = template_env
    return template_env


TEMPLATE_TEST_CONTEXT = {}

def render_template(request, template_path, context):
    """
    Render a template with context.

    Always inserts the request into the context, so you don't have to.
    Also stores the context if we're doing unit tests.  Helpful!
    """
    global TEMPLATE_TEST_CONTEXT
    template = request.template_env.get_template(template_path)
    context['request'] = request
    rendered_csrf_token = render_csrf_form_token(request)
    if rendered_csrf_token is not None:
        context['csrf_token'] = render_csrf_form_token(request)
    if request.controller_name:
        context = hook_transform((
         request.controller_name, template_path), context)
    context = hook_transform('template_context_prerender', context)
    rendered = template.render(context)
    if common.TESTS_ENABLED:
        TEMPLATE_TEST_CONTEXT[template_path] = context
    return rendered


def clear_test_template_context():
    global TEMPLATE_TEST_CONTEXT
    TEMPLATE_TEST_CONTEXT = {}


class TemplateHookExtension(Extension):
    __doc__ = '\n    Easily loop through a bunch of templates from a template hook.\n\n    Use:\n      {% template_hook("comment_extras") %}\n\n    ... will include all templates hooked into the comment_extras section.\n    '
    tags = set(['template_hook'])

    def parse(self, parser):
        includes = []
        expr = parser.parse_expression()
        lineno = expr.lineno
        hook_name = expr.args[0].value
        for template_name in get_hook_templates(hook_name):
            includes.append(parser.parse_import_context(Include(Const(template_name), True, False, lineno=lineno), True))

        return includes