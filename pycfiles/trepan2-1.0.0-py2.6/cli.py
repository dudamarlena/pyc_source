# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/cli.py
# Compiled at: 2020-04-27 23:16:57
"""The command-line interface to the debugger.
"""
from __future__ import print_function
import pyficache, os, sys, tempfile, os.path as osp
from trepan import client as Mclient
from trepan import clifns as Mclifns
from trepan import debugger as Mdebugger
from trepan import exception as Mexcept
from trepan import options as Moptions
from trepan.interfaces import server as Mserver
from trepan.lib import file as Mfile
from trepan import misc as Mmisc
__title__ = 'trepan2'
from trepan.version import VERSION as __version__

def main(dbg=None, sys_argv=list(sys.argv)):
    """Routine which gets run if we were invoked directly"""
    orig_sys_argv = list(sys_argv)
    (opts, dbg_opts, sys_argv) = Moptions.process_options(__title__, __version__, sys_argv)
    if opts.server:
        connection_opts = {'IO': 'TCP', 'PORT': opts.port}
        intf = Mserver.ServerInterface(connection_opts=connection_opts)
        dbg_opts['interface'] = intf
        if 'FIFO' == intf.server_type:
            print('Starting FIFO server for process %s.' % os.getpid())
        elif 'TCP' == intf.server_type:
            print('Starting TCP server listening on port %s.' % intf.inout.PORT)
    elif opts.client:
        Mclient.main(opts, sys_argv)
        return
    dbg_opts['orig_sys_argv'] = orig_sys_argv
    if dbg is None:
        dbg = Mdebugger.Debugger(dbg_opts)
        dbg.core.add_ignore(main)
    Moptions._postprocess_options(dbg, opts)
    if len(sys_argv) == 0:
        mainpyfile = None
    else:
        mainpyfile = sys_argv[0]
        if not osp.isfile(mainpyfile):
            mainpyfile = Mclifns.whence_file(mainpyfile)
            is_readable = Mfile.readable(mainpyfile)
            if is_readable is None:
                print("%s: Python script file '%s' does not exist" % (
                 __title__, mainpyfile), file=sys.stderr)
                sys.exit(1)
            elif not is_readable:
                print("%s: Can't read Python script file '%s'" % (
                 __title__, mainpyfile), file=sys.stderr)
                sys.exit(1)
                return
        if Mfile.is_compiled_py(mainpyfile):
            try:
                from xdis import load_module, PYTHON_VERSION, IS_PYPY
                (python_version, timestamp, magic_int, co, is_pypy, source_size) = load_module(mainpyfile, code_objects=None, fast_load=True)
                assert is_pypy == IS_PYPY
                assert python_version == PYTHON_VERSION, 'bytecode is for version %s but we are version %s' % (
                 python_version, PYTHON_VERSION)
                py_file = co.co_filename
                if osp.isabs(py_file):
                    try_file = py_file
                else:
                    mainpydir = osp.dirname(mainpyfile)
                    dirnames = [mainpydir] + os.environ['PATH'].split(os.pathsep) + ['.']
                    try_file = Mclifns.whence_file(py_file, dirnames)
                if osp.isfile(try_file):
                    mainpyfile = try_file
                else:
                    raise IOError('Python file name embedded in code %s not found' % try_file)
            except:
                try:
                    from uncompyle6 import uncompyle_file
                except ImportError:
                    print("%s: Compiled python file '%s', but uncompyle6 not found" % (
                     __title__, mainpyfile), file=sys.stderr)
                    sys.exit(1)
                    return
                else:
                    short_name = osp.basename(mainpyfile).strip('.pyc')
                    fd = tempfile.NamedTemporaryFile(suffix='.py', prefix=short_name + '_', delete=False)
                    try:
                        uncompyle_file(mainpyfile, fd)
                        mainpyfile = fd.name
                        fd.close()
                    except:
                        print("%s: error uncompiling '%s'" % (
                         __title__, mainpyfile), file=sys.stderr)
                        fd.close()
                        os.unlink(fd.name)
                        sys.exit(1)

        mainpyfile_noopt = pyficache.pyc2py(mainpyfile)
        if mainpyfile != mainpyfile_noopt and Mfile.readable(mainpyfile_noopt):
            print("%s: Compiled Python script given and we can't use that." % __title__, file=sys.stderr)
            print('%s: Substituting non-compiled name: %s' % (
             __title__, mainpyfile_noopt), file=sys.stderr)
            mainpyfile = mainpyfile_noopt
        sys.path[0] = dbg.main_dirname = osp.dirname(mainpyfile)
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
        except:
            exception_name = str(sys.exc_info()[0])
            if exception_name == str(Mexcept.DebuggerQuit):
                break
            elif exception_name == str(Mexcept.DebuggerRestart):
                dbg.core.execution_status = 'Restart requested'
                if dbg.program_sys_argv:
                    sys.argv = list(dbg.program_sys_argv)
                    part1 = 'Restarting %s with arguments:' % dbg.core.filename(mainpyfile)
                    args = (' ').join(dbg.program_sys_argv[1:])
                    dbg.intf[(-1)].msg(Mmisc.wrapped_lines(part1, args, dbg.settings['width']))
            else:
                raise

    sys.argv = orig_sys_argv
    return


if __name__ == '__main__':
    main()