# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\ext\turbogears.py
# Compiled at: 2007-01-03 20:15:06
"""webstring plugin for TurboGears and Buffet"""
from webstring import Template

def _get_mod_func(callback):
    """Breaks a callable name out from a module name.

    @param callback Name of a callback        
    """
    dot = callback.rindex('.')
    return (callback[:dot], callback[dot + 1:])


def _get_callback(callback):
    """Loads a callable based on its name

    callback A callback's name"""
    (mod_name, func_name) = _get_mod_func(callback)
    try:
        return getattr(__import__(mod_name, '', '', ['']), func_name)
    except ImportError, error:
        raise ImportError('Could not import %s. Error was: %s' % (mod_name, str(error)))
    except AttributeError, error:
        raise AttributeError('Tried %s in module %s. Error was: %s' % (func_name, mod_name, str(error)))


class TurboWebstring(object):
    """webstring support for TurboGears and Buffet."""
    __module__ = __name__

    def __init__(self, extra_vars_func=None, options=None):
        """
        @param extra_vars_func Not used
        @param options Extra settings for webstring Template
        """
        if options is None:
            options = dict()
        self.options = options
        self.engine = options.get('webstring.engine', 'etree')
        self.encoding = options.get('webstring.encoding', 'utf-8')
        self.templates = options.get('webstring.templates')
        self.format = options.get('webstring.format', 'html')
        self.auto = options.get('webstring.auto', False)
        self.max = options.get('webstring.max', 25)
        self.template = options.get('webstring.template')
        if self.template is not None:
            self.template = Template(self.template, self.auto, self.max, templates=self.templates, engine=self.engine, format=self.format)
        else:
            self.callable = options.get('webstring.callable')
        return

    def load_template(self, classname):
        """Loads a callable function that accepts a single argument for info.
    
        @param classname The name of the function
        @param loadingSite Not used
        """
        self.callable = _get_callback(classname)

    def render(self, info, format='html', fragment=False, template=None):
        """Renders data in the desired format.
    
        @param info The data
        @param format Format to render data to (default: 'html') 
        @param fragment Not used
        @param template Name of a template (default: None)
        """
        if template is not None:
            template = Template(template, self.auto, self.max, templates=self.templates, engine=self.engine, format=self.format)
        else:
            template = self.template
        if self.callable is not None:
            return self.callable(info)
        return template.render(info, format, self.encoding)

    def transform(self, info, template):
        """Stub for compatibility."""
        pass