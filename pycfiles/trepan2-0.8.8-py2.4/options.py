# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/options.py
# Compiled at: 2018-10-27 14:00:27
import os, sys, codecs
from optparse import OptionParser
from trepan import debugger as Mdebugger, api as Mapi, clifns as Mclifns
from trepan.lib import file as Mfile
from trepan.inout import output as Moutput

def add_startup_file(dbg_initfiles):
    """ Read debugger startup file(s): both python code and
    debugger profile to dbg_initfiles."""
    startup_python_file = default_configfile('profile.py')
    if Mfile.readable(startup_python_file):
        fp = codecs.open(startup_python_file, 'r', encoding='utf8')
        try:
            exec fp.read()
        finally:
            fp.close()
    startup_trepan_file = default_configfile('profile')
    if Mfile.readable(startup_trepan_file):
        dbg_initfiles.append(startup_trepan_file)


def default_configfile(base_filename):
    """Return fully expanded configuration filename location for
    base_filename. python2 and  python3 debuggers share the smae
    directory: ~/.config/trepan.py
    """
    file_dir = os.path.join(os.environ.get('HOME', '~'), '.config', 'trepanpy')
    file_dir = Mclifns.path_expanduser_abs(file_dir)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir, mode=493)
    return os.path.join(file_dir, base_filename)


def process_options(debugger_name, pkg_version, sys_argv, option_list=None):
    """Handle debugger options. Set `option_list' if you are writing
    another main program and want to extend the existing set of debugger
    options.

    The options dicionary from optparser is returned. sys_argv is
    also updated."""
    usage_str = '%prog [debugger-options] [python-script [script-options...]]\n\n    Runs the extended python debugger'
    optparser = OptionParser(usage=usage_str, option_list=option_list, version='%%prog version %s' % pkg_version)
    optparser.add_option('-X', '--trace', dest='linetrace', action='store_true', default=False, help='Show lines before executing them.This option also sets --batch')
    optparser.add_option('-F', '--fntrace', dest='fntrace', action='store_true', default=False, help='Show functions before executing them.This option also sets --batch')
    optparser.add_option('--basename', dest='basename', action='store_true', default=False, help='Filenames strip off basename, (e.g. for regression tests)')
    optparser.add_option('--client', dest='client', action='store_true', help='Connect to an existing debugger process started with the --server option. See options for client.')
    optparser.add_option('-x', '--command', dest='command', action='store', type='string', metavar='FILE', help='Execute commands from FILE.')
    optparser.add_option('--cd', dest='cd', action='store', type='string', metavar='DIR', help='Change current directory to DIR.')
    optparser.add_option('--confirm', dest='confirm', action='store_true', default=True, help='Confirm potentially dangerous operations')
    optparser.add_option('--dbg_trepan', dest='dbg_trepan', action='store_true', default=False, help='Debug the debugger')
    optparser.add_option('--different', dest='different', action='store_true', default=True, help='Consecutive stops should have different positions')
    optparser.add_option('-e', '--exec', dest='execute', type='string', help='list of debugger commands to ' + 'execute. Separate the commands with ;;')
    optparser.add_option('-H', '--host', dest='host', default='127.0.0.1', action='store', type='string', metavar='IP-OR-HOST', help='connect IP or host name. Only valid if --client option given.')
    optparser.add_option('--highlight', dest='highlight', action='store', type='string', metavar='{light|dark|plain}', default='light', help="Use syntax and terminal highlight output. 'plain' is no highlight")
    optparser.add_option('--private', dest='private', action='store_true', default=False, help="Don't register this as a global debugger")
    optparser.add_option('--post-mortem', dest='post_mortem', action='store_true', default=True, help='Enter debugger on an uncaught (fatal) exception')
    optparser.add_option('--no-post-mortem', dest='post_mortem', action='store_false', default=True, help="Don't enter debugger on an uncaught (fatal) exception")
    optparser.add_option('-n', '--nx', dest='noexecute', action='store_true', default=False, help="Don't execute commands found in any initialization files")
    optparser.add_option('-o', '--output', dest='output', metavar='FILE', action='store', type='string', help="Write debugger's output (stdout) to FILE")
    optparser.add_option('-P', '--port', dest='port', default=1027, action='store', type='int', help='Use TCP port number NUMBER for out-of-process connections.')
    optparser.add_option('--server', dest='server', action='store_true', help='Out-of-process server connection mode')
    optparser.add_option('--sigcheck', dest='sigcheck', action='store_true', default=False, help='Set to watch for signal handler changes')
    (
     optparser.add_option('-t', '--target', dest='target', help="Specify a target to connect to. Arguments should be of form, 'protocol address'."),)
    optparser.add_option('--from_ipython', dest='from_ipython', action='store_true', default=False, help='Called from inside ipython')
    optparser.add_option('--annotate', default=0, type='int', help='Use annotations to work inside emacs')
    optparser.disable_interspersed_args()
    sys.argv = list(sys_argv)
    (opts, sys.argv) = optparser.parse_args()
    dbg_opts = {'from_ipython': opts.from_ipython}
    dbg_initfiles = []
    if not opts.noexecute:
        add_startup_file(dbg_initfiles)
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

    return (opts, dbg_opts, sys.argv)


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
    dbg.settings['style'] = None
    if not opts.private:
        Mdebugger.debugger_obj = dbg
    if opts.post_mortem:
        Mapi.debugger_on_post_mortem()
    return


if __name__ == '__main__':
    import pprint

    def doit(prog, version, arg_str):
        print "options '%s'" % arg_str
        args = arg_str.split()
        (opts, dbg_opts, sys_argv) = process_options('testing', version, args)
        pp.pprint(vars(opts))
        print ''


    pp = pprint.PrettyPrinter(indent=4)
    doit('testing', '1.1', '')
    doit('testing', '1.2', 'foo bar')
    doit('testing', '1.3', '--server')
    doit('testing', '1.3', '--command %s bar baz' % __file__)
    doit('testing', '1.4', '--server --client')
    doit('testing', '1.5', '--style=emacs')
    doit('testing', '1.6', '--help')