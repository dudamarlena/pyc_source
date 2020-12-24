# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_shortcodes.py
# Compiled at: 2020-05-13 04:52:49
# Size of source mod 2**32: 1095 bytes
import ivy, sys
try:
    import shortcodes
except ImportError:
    shortcodes = None
else:
    settings = ivy.site.config.get('shortcodes', {})
    if shortcodes:
        parser = (shortcodes.Parser)(**settings)

        @ivy.hooks.register('node_text')
        def render(text, node):
            try:
                return parser.parse(text, node)
                    except shortcodes.ShortcodeError as err:
                try:
                    msg = 'Shortcode Error\n'
                    msg += f"  Node: {node}\n"
                    msg += f"  Error: {err.__class__.__name__}: {err}"
                    if (cause := err.__context__):
                        msg += '\n  Cause: {cause.__class__.__name__}: {cause}'
                    sys.exit(msg)
                finally:
                    err = None
                    del err