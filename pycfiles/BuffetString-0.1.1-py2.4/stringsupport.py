# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\buffetstring\stringsupport.py
# Compiled at: 2006-01-07 15:27:52
"""
BuffetString is more of a proof-of-concept and example
'python.templating.engines' plugin than anything else.  If it is useful
to you, great.  Otherwise, just read over the source for a simple example
of making a plugin.
"""
import string, os

class StringTemplatePlugin(object):
    __module__ = __name__
    extension = 'tmpl'

    def __init__(self, extra_vars_func=None, config=None):
        """extra_vars_func == optional callable() that returns a dict
        config == optional dict() of configuration settings
        """
        self.get_extra_vars = extra_vars_func
        if config:
            self.config = config
        else:
            self.config = dict()

    def load_template(self, template_name):
        """template_name == dotted.path.to.template (without .ext)
        
        The dotted notation is present because many template engines
        allow templates to be compiled down to Python modules.  TurboGears
        uses that feature to its adavantage, and for ease of integration
        the python.templating.engines plugin format requires the path to
        the template to be supplied as a dotted.path.to.template regardless
        of whether is is a module or not.

        In the case of string.Template templates, they are just simple text
        files, so we deal with the dotted notation and translate it into a
        standard file path to open the text file.
        """
        parts = template_name.split('.')
        template_filename = '%s.%s' % (parts.pop(), self.extension)
        template_path = os.path.join(*parts)
        template_file_path = os.path.join(template_path, template_filename)
        template_file = open(template_file_path)
        template_obj = string.Template(template_file.read())
        template_file.close()
        return template_obj

    def render(self, info, format='html', fragment=False, template=None):
        """info == dict() of variables to stick into the template namespace
        format == output format if applicable
        fragment == special rules about rendering part of a page
        template == dotted.path.to.template (without .ext)

        You might not need all of these arguments.  info and template are the
        only ones used in this simple example.
        """
        vars = info
        if callable(self.get_extra_vars):
            vars.update(self.get_extra_vars())
        template_obj = self.load_template(template)
        return template_obj.safe_substitute(**vars)