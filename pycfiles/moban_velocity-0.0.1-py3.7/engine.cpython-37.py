# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/moban_velocity/engine.py
# Compiled at: 2019-02-02 05:39:08
# Size of source mod 2**32: 710 bytes
import codecs
from airspeed import Template
import moban.utils as utils

class EngineVelocity(object):

    def __init__(self, template_dirs, extensions=None):
        self.template_dirs = template_dirs

    def get_template(self, template_file):
        actual_file = utils.get_template_path(self.template_dirs, template_file)
        with codecs.open(actual_file, 'r', encoding='utf-8') as (source):
            template = Template(source.read())
        return template

    def get_template_from_string(self, string):
        return Template(string)

    def apply_template(self, template, data, output):
        rendered_content = template.merge(data)
        return rendered_content