# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_yaml.py
# Compiled at: 2016-09-05 18:24:48
# Size of source mod 2**32: 1134 bytes
import ark, re
try:
    import yaml
except ImportError:
    yaml = None

if yaml:

    @ark.hooks.register('file_text')
    def parse_yaml(text, meta):
        if text.startswith('---\n'):
            match = re.match('^---\\n(.*?\\n)---\\n+', text, re.DOTALL)
            if match:
                text = text[match.end(0):]
                data = yaml.load(match.group(1))
                if isinstance(data, dict):
                    meta.update(data)
                return text