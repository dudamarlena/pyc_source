# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/bwcli.py
# Compiled at: 2016-11-12 22:08:17
""" The hairy command-line interface to the debugger.
"""
import pyficache, os, os.path, sys
from optparse import OptionParser
from trepan import clifns as Mclifns
from trepan import debugger as Mdebugger, exception as Mexcept, misc as Mmisc
from trepan import file as Mfile
from trepan.interfaces import bullwinkle as Mbullwinkle
__title__ = 'trepan'
from trepan.VERSION import VERSION as __version__

def process_options(debugger_name, pkg_version, sys_argv, option_list=None):
    """Handle debugger options. Set `option_list' if you are writing
    another main program and want to extend the existing set of debugger
    options.

    The options dicionary from opt_parser is return. sys_argv is
    also updated."""
    usage_str = '%prog [debugger-options] [python-script [script-options...]]\n\n       Runs the extended python debugger'
    optparser = OptionParser(usage=usage_str, option_list=option_list, version='%%prog version %s' % pkg_version)
    optparser.add_option('-F', '--fntrace', dest='fntrace', action='store_true', default=False, help='Show functions before executing them. ' + 'This option also sets --batch')
    optparser.add_option('--basename', dest='basename', action='store_true', default=False, help='Filenames strip off basename, (e.g. for regression tests)')
    optparser.add_option('--different', dest='different', action='store_true', default=True, help='Consecutive stops should have different positions')
    optparser.disable_interspersed_args()
    sys.argv = list(sys_argv)
    (opts, sys.argv) = optparser.parse_args()
    dbg_opts = {}
    return (
     opts, dbg_opts, sys.argv)


def _postprocess_options(dbg, opts):
    """ Handle options (`opts') that feed into the debugger (`dbg')"""
    print_events = []
    if opts.fntrace:
        print_events = ['c_call', 'c_return', 'call', 'return']
    if len(print_events):
        dbg.settings['printset'] = frozenset(print_events)
    for setting in ('basename', 'different'):
        dbg.settings[setting] = getattr(opts, setting)

    dbg.settings['highlight'] = 'plain'
    Mdebugger.debugger_obj = dbg


def main(dbg=None, sys_argv=list(sys.argv)):
    """Routine which gets run if we were invoked directly"""
    global __title__
    orig_sys_argv = list(sys_argv)
    (opts, dbg_opts, sys_argv) = process_options(__title__, __version__, sys_argv)
    dbg_opts['orig_sys_argv'] = sys_argv
    dbg_opts['interface'] = Mbullwinkle.BWInterface()
    dbg_opts['processor'] = 'bullwinkle'
    if dbg is None:
        dbg = Mdebugger.Debugger(dbg_opts)
        dbg.core.add_ignore(main)
    _postprocess_options(dbg, opts)
    if len(sys_argv) == 0:
        mainpyfile = None
    else:
        mainpyfile = sys_argv[0]
        if not os.path.isfile(mainpyfile):
            mainpyfile = Mclifns.whence_file(mainpyfile)
            is_readable = Mfile.readable(mainpyfile)
            if is_readable is None:
                print "%s: Python script file '%s' does not exist" % (__title__, mainpyfile)
                sys.exit(1)
            elif not is_readable:
                print "%s: Can't read Python script file '%s'" % (__title__, mainpyfile)
                sys.exit(1)
                return
        mainpyfile_noopt = pyficache.pyc2py(mainpyfile)
        if mainpyfile != mainpyfile_noopt and Mfile.readable(mainpyfile_noopt):
            print "%s: Compiled Python script given and we can't use that." % __title__
            print '%s: Substituting non-compiled name: %s' % (__title__, mainpyfile_noopt)
            mainpyfile = mainpyfile_noopt
        sys.path[0] = dbg.main_dirname = os.path.dirname(mainpyfile)
    dbg.sig_received = False
    while True:
        try:
            if dbg.program_sys_argv and mainpyfile:
                normal_termination = dbg.run_script(mainpyfile)
                if not normal_termination:
                    break
            else:
                dbg.core.execution_status = 'No program'
                dbg.core.processor.process_commands()
            dbg.core.execution_status = 'Terminated'
            dbg.intf[(-1)].msg('The program finished - quit or restart')
            dbg.core.processor.process_commands()
        except Mexcept.DebuggerQuit:
            break
        except Mexcept.DebuggerRestart:
            dbg.core.execution_status = 'Restart requested'
            if dbg.program_sys_argv:
                sys.argv = list(dbg.program_sys_argv)
                part1 = 'Restarting %s with arguments:' % dbg.core.filename(mainpyfile)
                args = (' ').join(dbg.program_sys_argv[1:])
                dbg.intf[(-1)].msg(Mmisc.wrapped_lines(part1, args, dbg.settings['width']))
            else:
                break
        except SystemExit:
            break

    sys.argv = orig_sys_argv
    return


if __name__ == '__main__':
    main()