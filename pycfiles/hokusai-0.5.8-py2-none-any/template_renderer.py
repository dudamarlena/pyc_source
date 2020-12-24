# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/lib/template_renderer.py
# Compiled at: 2020-04-09 11:50:23
import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from hokusai.lib.exceptions import HokusaiError

class TemplateRenderer(object):

    def __init__(self, template_path, template_config):
        self.template_path = template_path
        self.template_config = template_config

    def load_template(self):
        try:
            env = Environment(loader=FileSystemLoader(os.path.split(self.template_path)[0]), undefined=StrictUndefined)
            return env.get_template(os.path.split(self.template_path)[1])
        except IOError:
            raise HokusaiError('Template not found.')

    def render(self):
        template = self.load_template()
        try:
            return template.render(**self.template_config)
        except Exception as e:
            raise HokusaiError('Rendering template raised error %s' % repr(e))