# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/toolbox/command.py
# Compiled at: 2009-10-08 00:25:03
from toolbox import toolbox

def run_script():
    parser = OptionParser()
    parser.add_option('-v', action='store_true', dest='verbose', default=True)
    parser.add_option('-q', action='store_false', dest='verbose')
    parser.add_option('-l', '--list', action='store_const', dest='action', const='list', default='switch')
    (options, args) = parser.parse_args()
    tbx = toolbox(options.toolbox_dir)
    try:
        method = getattr(tbx, options.action, None)
        if not method(args):
            options.print_help()
    except:
        options.print_help()

    return