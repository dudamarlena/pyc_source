# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_shortcodes.py
# Compiled at: 2016-09-06 05:15:53
# Size of source mod 2**32: 1361 bytes
import ark, sys
try:
    import shortcodes
except ImportError:
    shortcodes = None

if shortcodes:
    settings = ark.site.config.get('shortcodes', {})
    parser = shortcodes.Parser(**settings)

    @ark.hooks.register('record_text')
    def render(text, node):
        try:
            return parser.parse(text, node)
        except shortcodes.ShortcodeError as err:
            msg = '-------------------\n'
            msg += '  Shortcode Error  \n'
            msg += '-------------------\n\n'
            msg += '  Node: %s\n\n' % node.path()
            msg += '  %s: %s' % (err.__class__.__name__, err)
            if err.__context__:
                cause = err.__context__
                msg += '\n\nThe following cause was reported:\n\n'
                msg += '%s: %s' % (cause.__class__.__name__, cause)
            sys.exit(msg)