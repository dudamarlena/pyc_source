# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/plugins/Jinja2Templating.py
# Compiled at: 2013-03-05 21:43:25
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader
from jinja2 import TemplateNotFound
from thot.utils import datetimeformat, ordinal_suffix
from thot.template import TemplateException
__all__ = [
 'Jinja2Template']

class Jinja2Template(object):
    default_template = 'default.html'

    def __init__(self, settings):
        self.settings = settings
        self.env = Environment(loader=ChoiceLoader([
         FileSystemLoader(self.settings['template_dir']),
         PackageLoader('thot')]))
        self.env.filters['datetimeformat'] = datetimeformat
        self.env.filters['ordinalsuffix'] = ordinal_suffix

    def render_string(self, template_str, **kwargs):
        """Use `template_str` as a template"""
        template = self.env.from_string(template_str)
        try:
            return template.render(**kwargs)
        except TemplateNotFound as err:
            raise TemplateException("Template '%s' not found" % err)

    def render_file(self, template_name, **kwargs):
        """Use `template_name` as a template"""
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateException

        try:
            return template.render(**kwargs)
        except TemplateNotFound as err:
            raise TemplateException("Template '%s' not found" % err)