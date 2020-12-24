# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbojinja\widgets.py
# Compiled at: 2007-02-26 02:01:49
"""Template support for jinja"""
try:
    import os
    from jinja import Template, Context, StringLoader, FileSystemLoader
except:
    print 'jinja not found. You should install jinja first to use jinja template'
    raise

import pkg_resources

class TurboJinja:
    __module__ = __name__
    extension = 'html'

    def __init__(self, extra_vars_func=None, options=None):
        self.get_extra_vars = extra_vars_func
        if options:
            self.options = options
        else:
            self.options = dict()

    def load_template(self, template_name):
        """template_name == dotted.path.to.template (without .ext)

        Searches for a template along the Python path.

        Template files must end in ".html" and be in legitimate packages.
        """
        divider = template_name.rfind('.')
        if divider > -1:
            package = template_name[0:divider]
            basename = template_name[divider + 1:]
        else:
            raise ValueError, 'All templates must be in a package'
        templates_path = package.replace('.', os.sep)
        template_obj = Template(basename, FileSystemLoader(templates_path))
        return template_obj

    def render(self, info, format='html', fragment=False, template=None):
        vars = info
        if callable(self.get_extra_vars):
            vars.update(self.get_extra_vars())
        tclass = self.load_template(template)
        return tclass.render(Context(vars))