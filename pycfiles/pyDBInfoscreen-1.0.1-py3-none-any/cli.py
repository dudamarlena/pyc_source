# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/cli.py
# Compiled at: 2013-03-23 13:27:25
__doc__ = ' The hairy command-line interface to the debugger.\n'
import os, os.path, sys
package = 'pydbgr'
if package not in sys.modules:
    __import__('pkg_resources').declare_namespace(package)
from optparse import OptionParser
from import_relative import import_relative, get_srcdir
Minterface = import_relative('interface', '.', package)
Mapi = import_relative('api', top_name=package)
Mclifns = import_relative('clifns', top_name=package)
Mdebugger = import_relative('debugger', top_name=package)
Mexcept = import_relative('exception', top_name=package)
Moutput = import_relative('output', '.io', package)
Mserver = import_relative('server', '.interfaces', package)
Mfile = import_relative('file', '.lib', package)
Mmisc = import_relative('misc', '.', package)
__title__ = package
exec compile(open(os.path.join(get_srcdir(), 'VERSION.py')).read(), os.path.join(get_srcdir(), 'VERSION.py'), 'exec')
__version__ = VERSION

def process_options(debugger_name, pkg_version, sys_argv, option_list=None):
    """Handle debugger options. Set `option_list' if you are writing
    another main program and want to extend the existing set of debugger
    options.

    The options dicionary from opt_parser is return. sys_argv is
    also updated."""
    usage_str = '%prog [debugger-options] [python-script [script-options...]]\n\n       Runs the extended python debugger'
    optparser = OptionParser(usage=usage_str, option_list=option_list, version='%%prog version %s' % pkg_version)
    optparser.add_option('-X', '--trace', dest='linetrace', action='store_true', default=False, help='Show lines before executing them. ' + 'This option also sets --batch')
    optparser.add_option('-F', '--fntrace', dest='fntrace', action='store_true', default=False, help='Show functions before executing them. ' + 'This option also sets --batch')
    optparser.add_option('--basename', dest='basename', action='store_true', default=False, help='Filenames strip off basename, (e.g. for regression tests)')
    optparser.add_option('-x', '--command', dest='command', action='store', type='string', metavar='FILE', help='Execute commands from FILE.')
    optparser.add_option('--cd', dest='cd', action='store', type='string', metavar='DIR', help='Change current directory to DIR.')
    optparser.add_option('--confirm', dest='confirm', action='store_true', default=True, help='Confirm potentially dangerous operations')
    optparser.add_option('--dbg_pydbgr', dest='dbg_pydbgr', action='store_true', default=False, help='Debug the debugger')
    optparser.add_option('--different', dest='different', action='store_true', default=True, help='Consecutive stops should have different positions')
    optparser.add_option('-e', '--exec', dest='execute', type='string', help='list of debugger commands to ' + 'execute. Separate the commands with ;;')
    optparser.add_option('--highlight', dest='highlight', action='store', type='string', metavar='{light|dark|plain}', default='light', help="Use syntax and terminal highlight output. 'plain' is no highlight")
    optparser.add_option('--private', dest='private', action='store_true', default=False, help="Don't register this as a global debugger")
    optparser.add_option('--post-mortem', dest='post_mortem', action='store_true', default=True, help='Enter debugger on an uncaught (fatal) exception')
    optparser.add_option('--no-post-mortem', dest='post_mortem', action='store_false', default=True, help="Don't enter debugger on an uncaught (fatal) exception")
    optparser.add_option('-n', '--nx', dest='noexecute', action='store_true', default=False, help="Don't execute commands found in any " + 'initialization files')
    optparser.add_option('-o', '--output', dest='output', metavar='FILE', action='store', type='string', help="Write debugger's output (stdout) " + 'to FILE')
    optparser.add_option('--server', dest='server', action='store_true', help='Out-of-process server connection mode')
    optparser.add_option('--sigcheck', dest='sigcheck', action='store_true', default=False, help='Set to watch for signal handler changes')
    (
     optparser.add_option('-t', '--target', dest='target', help='Specify a target to connect to. Arguments' + " should be of form, 'protocol address'."),)
    optparser.add_option('--annotate', default=0, type='int', help='Use annotations to work inside emacs')
    optparser.disable_interspersed_args()
    sys.argv = list(sys_argv)
    (opts, sys.argv) = optparser.parse_args()
    dbg_opts = {}
    dbg_initfiles = []
    if not opts.noexecute:
        startup_file = '.%src' % debugger_name
        if 'HOME' in os.environ:
            startup_home_file = os.path.join(os.environ['HOME'], startup_file)
            expanded_startup_home = Mclifns.path_expanduser_abs(startup_home_file)
            if Mfile.readable(expanded_startup_home):
                dbg_initfiles.append(startup_home_file)
    if opts.command:
        dbg_initfiles.append(opts.command)
    dbg_opts['proc_opts'] = {'initfile_list': dbg_initfiles}
    if opts.cd:
        os.chdir(opts.cd)
    if opts.output:
        try:
            dbg_opts['output'] = Moutput.DebuggerUserOutput(opts.output)
        except IOError:
            (_, xxx_todo_changeme, _) = sys.exc_info()
            (errno, strerror) = xxx_todo_changeme.args
            print 'I/O in opening debugger output file %s' % opts.output
            print 'error(%s): %s' % (errno, strerror)
        except:
            print 'Unexpected error in opening debugger output file %s' % opts.output
            print sys.exc_info()[0]
            sys.exit(2)

    if opts.server:
        intf = Mserver.ServerInterface()
        dbg_opts['interface'] = intf
        if 'FIFO' == intf.server_type:
            print 'Starting FIFO server for process %s.' % os.getpid()
        elif 'TCP' == intf.server_type:
            print 'Starting TCP server listening on port %s.' % intf.inout.PORT
    return (
     opts, dbg_opts, sys.argv)


def _postprocess_options(dbg, opts):
    """ Handle options (`opts') that feed into the debugger (`dbg')"""
    print_events = []
    if opts.fntrace:
        print_events = ['c_call', 'c_return', 'call', 'return']
    if opts.linetrace:
        print_events += ['line']
    if len(print_events):
        dbg.settings['printset'] = frozenset(print_events)
    for setting in ('annotate', 'basename', 'different'):
        dbg.settings[setting] = getattr(opts, setting)

    if getattr(opts, 'highlight'):
        dbg.settings['highlight'] = opts.highlight
    else:
        dbg.settings['highlight'] = 'plain'
    if not opts.private:
        Mdebugger.debugger_obj = dbg
    if opts.post_mortem:
        Mapi.debugger_on_post_mortem()


def main(dbg=None, sys_argv=list(sys.argv)):
    """Routine which gets run if we were invoked directly"""
    global __title__
    orig_sys_argv = list(sys_argv)
    (opts, dbg_opts, sys_argv) = process_options(__title__, __version__, sys_argv)
    dbg_opts['orig_sys_argv'] = orig_sys_argv
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
        mainpyfile_noopt = Mfile.file_pyc2py(mainpyfile)
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