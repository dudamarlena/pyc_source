# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_shortcodes.py
# Compiled at: 2018-10-09 08:33:32
# Size of source mod 2**32: 1091 bytes
import ivy, sys, shortcodes
settings = ivy.site.config.get('shortcodes', {})
parser = (shortcodes.Parser)(**settings)

@ivy.hooks.register('node_text')
def render(text, node):
    try:
        return parser.parse(text, node)
    except shortcodes.ShortcodeError as err:
        try:
            msg = '-------------------\n'
            msg += '  Shortcode Error  \n'
            msg += '-------------------\n\n'
            msg += '  %s\n\n' % node
            msg += '  %s: %s' % (err.__class__.__name__, err)
            if err.__context__:
                cause = err.__context__
                msg += '\n\n  The following cause was reported:\n\n'
                msg += '  %s: %s' % (cause.__class__.__name__, cause)
            sys.exit(msg)
        finally:
            err = None
            del err