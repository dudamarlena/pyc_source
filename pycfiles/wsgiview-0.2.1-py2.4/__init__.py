# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiview\__init__.py
# Compiled at: 2007-01-01 18:51:51
"""Use TurboGears Template Plug-ins Anywhere."""
__author__ = 'L. C. Rees <lcrees-at-gmail.com>'
__revision__ = '0.2'
import pkg_resources
__all__ = [
 'WsgiView', 'view']
_engines = dict(((_engine.name, _engine) for _engine in pkg_resources.iter_entry_points('python.templating.engines')))

def view(template=None, **kw):
    """Decorator for WsgiView.

    @param template A template name
    """

    def decorator(application):
        return WsgiView(application, template, **kw)

    return decorator


class WsgiView(object):
    """TurboGears/Buffet Template Plug-in WSGI Middleware."""
    __module__ = __name__
    engine = None

    def __init__(self, application, template=None, **kw):
        if template is not None:
            (engine_name, template) = template.split(':')
            extra_vars_func = kw.get('extra_vars')
            options = kw.get('options', dict())
            engine = _engines[engine_name].load()
            self.engine = engine(extra_vars_func, options)
        self.format = kw.get('format', 'html')
        self.fragment = kw.get('fragment', False)
        self.application, self.template = application, template
        return

    def __call__(self, environ, start_response):
        info = self.application(environ, start_response)
        engine_name = environ.get('wsgiview.engine')
        if engine_name is not None:
            extra_vars_func = environ.get('wsgiview.extra_vars_func')
            options = environ.get('wsgiview.options')
            engine = _engines[engine_name].load()
            engine = engine(extra_vars_func, options)
        else:
            engine = self.engine
        template = environ.get('wsgiview.template', self.template)
        format = environ.get('wsgiview.format', self.format)
        fragment = environ.get('wsgiview.fragment', self.fragment)
        return [
         str(engine.render(info, format, fragment, template))]