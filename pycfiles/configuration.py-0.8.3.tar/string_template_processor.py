# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bogdan/projects/personal/configuration.py/configuration_py/parsers/string_template_processor.py
# Compiled at: 2017-03-29 09:29:43
from string import Template
import os
from configuration_py.parsers.base_parser import BaseConfigParser

class ConfigStringTemplateProcessor(BaseConfigParser):
    extensions = ('tmpl', 'strtmpl')

    def parse(self, file_content, context={}):
        context.update(os.environ)
        try:
            return Template(file_content).substitute(context)
        except KeyError as e:
            raise EnvironmentError(('Config try to use {e} variable which does not exists. Pass variable to load context or set it to the environment.').format(e=e))