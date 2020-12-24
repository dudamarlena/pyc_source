# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/neurospaces/launcher.py
# Compiled at: 2011-08-29 14:45:23
"""!
@package launcher
@file launcher.py

@brief This program starts the command line process for the devloper package
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
    sys.exit(2)


def main(cwd=os.getcwd()):
    try:
        path = os.path.dirname(__file__)
        os.chdir(path)
    except:
        pass

    if len(sys.argv) < 2:
        usage()
    command_options = [
     'vv', 'version',
     'shell', 'help', 'verbose', 'more-verbose']
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
    from neurospaces.packages import PackageManager
    package_manager = PackageManager(verbose=verbose)
    if shell:
        from shell import PackageShell
        package_shell = PackageShell(package_manager=package_manager)
        package_shell.cmdloop()
    return