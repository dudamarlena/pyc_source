# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/lib/base.py
# Compiled at: 2010-08-08 03:18:44
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
import pysvnmanager.lib.helpers as h
from pylons.controllers.util import abort, etag_cache
from pylons import app_globals, cache, config, request, response, session
from pylons.i18n import _, ungettext, N_
from pylons.i18n import set_lang, add_fallback
from pylons import app_globals as g
from pylons import tmpl_context as c
from pylons import url
from pylons.controllers.util import redirect
from pysvnmanager.model.meta import Session
import sys
config_path = config['here'] + '/config'
if config_path not in sys.path:
    sys.path.insert(0, config_path)
from localconfig import LocalConfig as cfg

class BaseController(WSGIController):
    requires_auth = []

    def __before__(self, action=None):
        if 'lang' in session:
            set_lang(session['lang'])
        try:
            for lang in request.languages:
                if lang.lower() in ('zh-cn', 'zh'):
                    add_fallback('zh')
                elif lang in ('en', ):
                    add_fallback(lang)

        except:
            pass

        if getattr(g, 'catch_e', None):
            return redirect(url(controller='template', action='show_e'))
        else:
            g.catch_e = []
            if isinstance(self.requires_auth, bool) and not self.requires_auth:
                pass
            elif isinstance(self.requires_auth, (list, tuple)) and action not in self.requires_auth:
                pass
            elif 'user' not in session:
                session['path_before_login'] = request.path_info
                session.save()
                return redirect(url('login'))
            if hasattr(self, 'authz'):
                diff = self.authz.differ()
                if diff:
                    c.global_message = _('Some one maybe you, has modified the svn authz file by hands. Please %(begin)ssave once%(end)s to fix possible config error.') % {'begin': '<big><strong><a href="' + url(controller=self.__class__.__name__.lower()[0:-10], action='standardize') + '">', 
                       'end': '</a></strong></big>'}
                    c.global_message += '<blockquote>' + ('<br>').join(diff.splitlines()) + '</blockquote>'
            return

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def standardize(self):
        if hasattr(self, 'authz'):
            diff = self.authz.differ()
            if diff:
                self.authz.save(self.authz.version, comment=_('Modified external, save to avoid configuration error.'))
        if request.referer:
            redirect(request.referer)
        else:
            redirect(url(controller=self.__class__.__name__.lower()[0:-10], action='index'))