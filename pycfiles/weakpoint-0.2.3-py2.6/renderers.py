# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/renderers.py
# Compiled at: 2012-11-21 04:46:57
from jinja2 import Environment, FileSystemLoader, PrefixLoader
from jinja2.exceptions import TemplateNotFound
from weakpoint.exceptions import RendererException
import os

class Renderer(object):

    def __init__(self, path):
        self.environment = Environment(loader=FileSystemLoader(path + os.sep + '_templates'))

    def render(self, template, vars_={}):
        try:
            template = self.environment.get_template(template)
        except TemplateNotFound:
            raise RendererException('Template not found')

        return template.render(**vars_)