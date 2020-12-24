# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tw\core\view.py
# Compiled at: 2011-07-14 12:05:16
import sys, logging, re, threading
from pkg_resources import iter_entry_points, load_entry_point
import tw
from tw.core.exceptions import WidgetException
from tw.core.util import LRUCache
__all__ = [
 'EngineManager', 'Renderable', 'EngineException', 'display', 'render']
log = logging.getLogger(__name__)

class EngineException(WidgetException):
    __module__ = __name__


def make_renderer(method, doc=None):

    def _renderer(self, renderable, **kw):
        template = kw.pop('template', renderable.template)
        if template is None:
            return
        origin = dynamic_best_engine(renderable, kw)
        destination = kw.get('displays_on', renderable.displays_on)
        if origin != 'cheetah':
            template = self.load_template(template, origin)
        renderer = self.get_render_method(origin, destination, method)
        output = renderer(info=kw, template=template)
        if method == 'display':
            output = self.adapt_output(output, destination)
        if isinstance(output, str):
            output = unicode(output, 'utf-8')
        return output

    _renderer.func_name = method
    _renderer.__doc__ = doc
    return _renderer


class EngineManager(dict):
    """
    Manages available templating engines.
    """
    __module__ = __name__
    default_view = 'toscawidgets'

    def __init__(self, extra_vars_func=None, options=None, load_all=False):
        self.extra_vars_func = extra_vars_func
        self.options = options
        self._cache = LRUCache(50)
        self._lock = threading.Lock()
        if load_all:
            self.load_all()

    def __repr__(self):
        return '< %s >' % self.__class__.__name__

    def load_engine(self, name, options=None, extra_vars_func=None, distribution=None):
        factory = None
        if distribution:
            factory = load_entry_point(distribution, 'python.templating.engines', name)
        else:
            for entrypoint in iter_entry_points('python.templating.engines'):
                if entrypoint.name == name:
                    factory = entrypoint.load()

        if factory is None:
            raise EngineException("No plugin available for engine '%s'" % name)
        options = options or self.options or {}
        options = options.copy()
        options.setdefault('mako.directories', []).extend(sys.path)
        options['mako.output_encoding'] = 'utf-8'
        extra_vars_func = extra_vars_func or self.extra_vars_func
        self._lock.acquire()
        try:
            self[name] = factory(extra_vars_func, options)
        finally:
            self._lock.release()
        return

    def __getitem__(self, name):
        """
        Return a Buffet plugin by name. If the plugin is not loaded it
        will try to load it with default arguments.
        """
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            self.load_engine(name)
            return dict.__getitem__(self, name)

    def load_all(self, engine_options=None, stdvars=None, raise_error=False):
        for ep in iter_entry_points('python.templating.engines'):
            try:
                self.load_engine(ep.name, engine_options, stdvars)
            except:
                log.warn("Failed to load '%s' template engine: %r", ep.name, sys.exc_info())
                if raise_error:
                    raise

    def load_template(self, template, engine_name):
        """Return's a compiled template and it's enginename"""
        output = None
        if isinstance(template, basestring) and _is_inline_template(template):
            key = (template, engine_name)
            try:
                output = self._cache[key]
            except KeyError:
                output = self._cache[key] = self[engine_name].load_template(None, template_string=template)

        elif isinstance(template, basestring):
            output = self[engine_name].load_template(template)
        else:
            output = template
        return output

    display = make_renderer('display', doc='\n        Displays the renderable. Returns appropriate output for target template\n        engine\n        ')
    render = make_renderer('render', doc='\n        Returns the serialized output in a string.\n        Useful for debugging or to return to the browser as-is.\n        ')

    def get_render_method(self, origin, destination, method):
        engine = self[origin]
        if method == 'display' and origin == destination and origin in ['kid', 'genshi']:
            return engine.transform

        def _render_xhtml(**kw):
            kw.update(format='xhtml')
            return engine.render(**kw)

        return _render_xhtml

    def adapt_output(self, output, destination):
        if isinstance(output, basestring) and destination == 'genshi':
            from genshi.input import HTML
            output = HTML(output)
        elif isinstance(output, basestring) and destination == 'kid':
            from kid import XML
            output = XML(output)
        return output


display = EngineManager.display.im_func
render = EngineManager.render.im_func

def choose_engine(obj, engine_name=None):
    tpl = obj.template
    if isinstance(tpl, basestring) and not _is_inline_template(tpl):
        colon = tpl.find(':')
        if colon > -1:
            engine_name = tpl[:colon]
            tpl = tpl[colon + 1:]
    return (
     engine_name, tpl)


def dynamic_best_engine(renderable, params):
    try:
        ideal_engine = params['displays_on']
    except KeyError:
        ideal_engine = renderable.displays_on

    if ideal_engine not in renderable.available_engines:
        try:
            best_engine = params['engine_name']
        except KeyError:
            best_engine = renderable.engine_name

    else:
        best_engine = ideal_engine
    assert best_engine is not None
    return best_engine


_is_inline_template = re.compile('(<|\\n|\\$)').search

class Renderable(object):
    """Base class for all objects that the EngineManager can render"""
    __module__ = __name__
    engine_name = 'toscawidgets'
    available_engines = []
    template = None

    def displays_on(self):
        return tw.framework.default_view

    displays_on = property(displays_on, doc='        Where the Renderable is being displayed on\n        ')

    def __new__(cls, *args, **kw):
        obj = object.__new__(cls)
        obj.template = kw.pop('template', obj.template)
        engine_name = kw.pop('engine_name', None)
        if obj.template is not None:
            (colon_based_engine_name, obj.template) = choose_engine(obj)
            if colon_based_engine_name:
                obj.available_engines = [
                 colon_based_engine_name]
            engine_name = colon_based_engine_name
        if engine_name:
            obj.engine_name = engine_name
        return obj

    def render(self, **kw):
        kw.setdefault('_', tw.framework.translator)
        return tw.framework.engines.render(self, **kw)

    def display(self, **kw):
        kw.setdefault('_', tw.framework.translator)
        return tw.framework.engines.display(self, **kw)