# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/gotrace.py
# Compiled at: 2014-02-02 09:23:12
"""gotrace: Graphical otrace launcher
"""
import logging, os, signal, sys, threading, time, traceback, gtermhost

def main(args=None):
    global Gterm_host
    global Host_secret
    global Trace_shell
    import imp
    if args is None:
        args = sys.argv[1:]
    funcname = ''
    server = 'localhost'
    hostname = ''
    j = 0
    while j < len(args) - 1:
        if args[j] == '-f':
            funcname = args[(j + 1)]
        elif args[j] == '-n':
            hostname = args[(j + 1)]
        elif args[j] == '-s':
            server = args[(j + 1)]
        else:
            break
        j += 2

    if j >= len(args):
        print >> sys.stderr, 'Usage: gotrace [-f function_name] [-n hostname] [-s server_addr[:port] (default: localhost:%d)] program_file [arg1 arg2 ...]' % gtermhost.DEFAULT_HOST_PORT
        sys.exit(1)
    filepath = args[j]
    args = args[j + 1:]
    if not os.path.isfile(filepath) or not os.access(filepath, os.R_OK):
        print >> sys.stderr, 'gotrace: Unable to read file %s' % filepath
        sys.exit(1)
    abspath = os.path.abspath(filepath)
    filedir, basename = os.path.split(abspath)
    modname, extension = os.path.splitext(basename)
    if not hostname:
        hostname = modname
    if ':' in server:
        server, sep, port = server.partition(':')
        port = int(port)
    else:
        port = gtermhost.DEFAULT_HOST_PORT
    modfile, modpath, moddesc = imp.find_module(modname, [filedir])
    modobj = imp.load_module(modname, modfile, modpath, moddesc)
    orig_funcobj = getattr(modobj, funcname, None) if funcname else None
    if funcname and not callable(orig_funcobj):
        print >> sys.stderr, "gotrace: Program %s does not have function named '%s'" % (filepath, funcname)
        sys.exit(1)
    oshell_globals = modobj.__dict__
    Gterm_host, Host_secret, Trace_shell = gtermhost.gterm_connect(hostname, server, server_port=port, connect_kw={}, oshell_globals=oshell_globals, oshell_thread=True, oshell_unsafe=True, oshell_init=modname + '.trc')

    def host_shutdown():
        print >> sys.stderr, 'Shutting down'
        gtermhost.gterm_shutdown(Trace_shell)

    def sigterm(signal, frame):
        logging.warning('SIGTERM signal received')
        host_shutdown()

    signal.signal(signal.SIGTERM, sigterm)
    try:
        try:
            if funcname:
                time.sleep(1)
                funcobj = getattr(modobj, funcname)
                if args:
                    funcobj(args)
                else:
                    funcobj()
            else:
                Trace_shell.loop(wait_to_run=True)
        except Exception as excp:
            traceback.print_exc()
            print >> sys.stderr, '\nType ^C to abort'
            Trace_shell.execute('cd ~~')
            while not Trace_shell.shutting_down:
                time.sleep(1)

    finally:
        host_shutdown()

    return


if __name__ == '__main__':
    main(args=sys.argv[1:])