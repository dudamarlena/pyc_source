# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/yamlargs.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 705 bytes
from dexy.filter import DexyFilter
from dexy.utils import parse_yaml
import re

class YamlargsFilter(DexyFilter):
    __doc__ = '\n    Specify attributes in YAML at top of file.\n    '
    aliases = ['yamlargs']

    def process_text(self, input_text):
        regex = '\r?\n---\r?\n'
        if re.search(regex, input_text):
            self.log_debug('Found yaml content.')
            raw_yamlargs, content = re.split(regex, input_text)
            yamlargs = parse_yaml(raw_yamlargs)
            self.log_debug('Adding yaml: %s' % yamlargs)
            self.add_runtime_args(yamlargs)
            return content
        self.log_debug('No yaml content found.')
        return input_text