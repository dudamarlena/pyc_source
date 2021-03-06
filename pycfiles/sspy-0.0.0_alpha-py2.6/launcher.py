# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/sspy/launcher.py
# Compiled at: 2011-09-16 10:47:54
"""!
@package launcher
@file launcher.py

@brief This program starts the command line process for sspy
"""
import getopt, os, pdb, sys
try:
    import yaml
except ImportError:
    sys.exit('Need PyYaml http://pyyaml.org/\n')

from __cbi__ import PackageInfo
_package_info = PackageInfo()

def usage():
    print 'usage: %s [OPTIONS]' % sys.argv[0]
    print '\nStartup:'
    print ' -v, --version\t\tcurrent version number.'
    print ' -h, --help\t\tprint this help.'
    print ' --shell\t\tStarts the interactive shell.'
    print '\nScheduling:'
    print ' --builtins\t\tgive help about supported builtin simulation configurations.'
    print ' --optimize\t\tturn on the schedule optimizer.'
    print ' --emit-output\t\tfiles to write to stdout after the simulation finishes.'
    print ' --emit-schedules\tprint schedules to stdout instead of running them.'
    print ' --model-directory\tname of the directory where to look for non-std models.'
    print ' --model-filename\tfilename of the model description file (when using a builtin configuration).'
    print '\nProtocol Options:'
    print ' --perfectclamp\t\tset the command voltage for the perfect clamp protocol.'
    print ' --pulsegen-width1\tset the pulse width for the pulsegen protocol.'
    sys.exit(2)


from sspy import SSPy

def main(cwd=os.getcwd()):
    try:
        path = os.path.dirname(__file__)
        os.chdir(path)
    except:
        pass

    if len(sys.argv) < 2:
        usage()
    command_options = [
     'cell', 'model-name',
     'steps', 'time', 'time-step',
     'model-filename=', 'model-directory=',
     'version', 'help', 'background', 'builtins', 'optimize',
     'emit-schedules', 'emit-output',
     'perfectclamp',
     'pulsegen-width1=', 'pulsegen-width2=',
     'shell',
     'verbose', 'more-verbose', 'vv']
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], ':hvV', command_options)
    except getopt.GetoptError, err:
        print str(err)
        usage()

    os.chdir(cwd)
    shell = False
    stdout = False
    verbose = False
    more_verbose = False
    configuration = None
    model_directory = None
    model_filename = None
    model_name = None
    shell_batch_file = None
    for (opt, arg) in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt in '--model-directory':
            model_directory = arg
        elif opt in '--model-filename':
            model_filename = arg
        elif opt in '--model-name':
            model_name = arg
        elif opt in ('-V', '--version'):
            print 'version %s (%s)' % (_package_info.GetVersion(), _package_info.GetRevisionInfo())
            sys.exit(0)
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-vv', '--more-verbose'):
            verbose = True
        elif opt in ('--shell', ):
            shell = True
        else:
            assert False, 'unhandled option %s' % opt

    if len(args) > 0:
        for a in args:
            if os.path.isfile(a):
                configuration = a
                args.remove(a)

        if len(args) > 0:
            print 'Unprocessed arguments: ',
            for a in args:
                print '%s ' % a,

            print ''
    scheduler = SSPy(verbose=verbose)
    try:
        if configuration is not None:
            scheduler.Load(configuration)
    except Exception, e:
        print e
        sys.exit(1)

    if shell:
        from sspy.shell import SSPyShell
        sspy_shell = SSPyShell(scheduler=scheduler)
        sspy_shell.cmdloop()
    else:
        scheduler.Run()
    return