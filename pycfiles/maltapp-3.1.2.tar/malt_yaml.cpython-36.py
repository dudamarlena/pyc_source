# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sysadmin/src/malt/malt/ext/malt_yaml.py
# Compiled at: 2017-05-12 18:32:27
# Size of source mod 2**32: 1136 bytes
import malt, re
try:
    import yaml
except ImportError:
    yaml = None

if yaml:

    @malt.hooks.register('file_text')
    def parse_yaml(text, meta):
        if text.startswith('---\n'):
            match = re.match('^---\\n(.*?\\n)---\\n+', text, re.DOTALL)
            if match:
                text = text[match.end(0):]
                data = yaml.load(match.group(1))
                if isinstance(data, dict):
                    meta.update(data)
        return text