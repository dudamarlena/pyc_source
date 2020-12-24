# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_yaml.py
# Compiled at: 2019-10-28 14:59:23
# Size of source mod 2**32: 788 bytes
import ivy, re, sys
try:
    import yaml
except ImportError:
    pass
else:

    @ivy.hooks.register('file_text')
    def parse_yaml(text, meta):
        if text.startswith('---\n'):
            match = re.match('^---\\n(.*?\\n)---\\n+', text, re.DOTALL)
            if match:
                text = text[match.end(0):]
                data = yaml.safe_load(match.group(1))
                if isinstance(data, dict):
                    meta.update(data)
        return text