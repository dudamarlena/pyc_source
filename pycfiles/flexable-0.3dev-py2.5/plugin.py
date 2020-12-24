# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/flexable/plugin.py
# Compiled at: 2007-07-17 10:02:43
"""
WSGI Template Plugin
http://docs.turbogears.org/1.0/TemplatePlugins
"""
import sys, os
from template import Template

class FlexablePlugin(object):
    """
    Template Plugin for flexable.
    options

     - flexable.path separated by ":" or seaquence of template directory paths. default value is sys.path .
     - flexable.output_encoding output encoding. default value is 'utf-8'
     - flexable.output_format 'xhtml', 'xml' or 'html'not yet implemented.
     - flexable.suffix suffix of template filename.default value is '.html'
    """

    def __init__(self, extra_vars_func=None, options=None):
        self.extra_vars_func = extra_vars_func
        self.options = options
        paths = options.get('flexable.paths', sys.path)
        if isinstance(paths, str) or isinstance(paths, unicode):
            paths = paths.split[':']
        self.paths = paths
        self.suffix = options.get('flexable.suffix', '.html')

    def load_template(self, templatename):
        path = templatename.split('.')
        path[-1] = '%s%s' % (path[(-1)], self.suffix)
        path = os.path.join(*path)
        for dir in self.paths:
            fullpath = os.path.join(dir, path)
            if os.path.exists(fullpath) and os.path.isfile(fullpath):
                return Template(fullpath)

        msgprm = (
         path, (':').join(self.paths))
        msg = 'template "%s" is not found in paths "%s"' % msgprm
        raise Exception, msg

    def render(self, info, format='html', fragment=False, template=None):
        """Renders the template to a string using the provided info."""
        if template is None:
            return str(info)
        t = self.load_template(template)
        t.merge(info)
        return str(t)

    def transform(self, info, template):
        """Render the output to Elements"""
        pass