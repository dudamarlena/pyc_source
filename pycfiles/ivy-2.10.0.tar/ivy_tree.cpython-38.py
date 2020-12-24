# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_tree.py
# Compiled at: 2019-06-13 04:26:43
# Size of source mod 2**32: 1389 bytes
import ivy, sys, os
helptext = "\nUsage: %s tree [FLAGS]\n\n  Print the site's node tree.\n\nFlags:\n  -h, --help            Print this command's help text and exit.\n\n" % os.path.basename(sys.argv[0])

@ivy.hooks.register('cli')
def register_command(parser):
    parser.new_cmd('tree', helptext, callback)


def callback(parser):

    @ivy.hooks.register('main')
    def tree_callback():
        if not ivy.site.home():
            sys.exit("Error: cannot locate the site's home directory.")
        ivy.utils.termline()
        ivy.utils.safeprint('Site: %s' % ivy.site.home())
        ivy.utils.termline()
        ivy.utils.safeprint(ivy.nodes.root().str())
        ivy.utils.termline()