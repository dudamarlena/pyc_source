# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/roadrunner/runner.py
# Compiled at: 2009-06-16 00:05:39
"""
roadrunner
"""
from roadrunner import testrunner
import os, sys, time, signal, shlex, roadrunner.platform
roadrunner
try:
    import readline
    HAVE_READLINE = True
except:
    HAVE_READLINE = False

def run_commandloop(args):
    while 1:
        cmdline = raw_input('rr> ').strip()
        if cmdline:
            try:
                cmdargs = shlex.split(cmdline)
            except ValueError:
                print 'Cmdline syntax error'
                continue
            else:
                if cmdargs[0] in ('quit', 'exit'):
                    sys.exit(0)
                if cmdargs[0] in ('help', '?'):
                    print HELP_MESSAGE
                    continue
                if cmdargs[0] == 'debug':
                    import pdb
                    pdb.set_trace()
                    continue
                if cmdargs[0] == 'python':
                    from code import InteractiveConsole
                    ic = InteractiveConsole(locals=locals())
                    ic.interact('Python Debug shell')
                    continue
                if cmdargs[0] == 'test':
                    args = cmdargs[1:]
                    break
                else:
                    print "Unknown command.  Type 'help' for help."
        else:
            print 'rr> test ' + shlex_join(args)
            break

    return args


def plone(zope_conf, preload_modules, packages_under_test, zope2_location, buildout_home, part_dir, args=sys.argv):
    software_home = zope2_location + '/lib/python'
    sys.argv = sys.argv[0:1]
    bootstrap_zope(zope_conf)
    args = args[1:]
    if HAVE_READLINE:
        readline.add_history('test ' + shlex_join(args))
    t1 = time.time()
    setup_layers = preload_plone(part_dir)
    t2 = time.time()
    preload_time = t2 - t1
    print 'Preloading took: %0.3f seconds.' % preload_time
    defaults = testrunner_defaults()
    defaults = setup_paths(defaults, software_home, buildout_home)
    saved_time = -preload_time
    ignore_signal_handlers()
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while 1:
        pid = os.fork()
        if not pid:
            t1 = time.time()
            rc = testrunner.run(defaults=defaults, args=[sys.argv[0]] + args, setup_layers=setup_layers)
            t2 = time.time()
            print 'Testrunner took: %0.3f seconds.  ' % (t2 - t1)
            sys.exit(rc)
        else:
            try:
                register_signal_handlers(pid)
                try:
                    status = os.wait()
                    saved_time += preload_time
                    if saved_time:
                        print 'Saved time so far: %0.3f seconds.' % saved_time
                except OSError:
                    pass

            finally:
                ignore_signal_handlers()
                os.system('stty echo')
            args = run_commandloop(args)


def bootstrap_zope(config_file):
    config_file = os.path.abspath(config_file)
    import Zope2
    Zope2.configure(config_file)


def filter_warnings():
    import warnings
    warnings.simplefilter('ignore', Warning, append=True)


filter_warnings()

def maybe_quote_args(arg):
    if ' ' in arg:
        return '"' + arg + '"'
    else:
        return arg


def shlex_join(args, char=' '):
    l = map(maybe_quote_args, args)
    return char.join(args)


HELP_MESSAGE = 'roadrunner help\n--------------\n\nexit\n    to quit\n\ntest <testrunner arguments>\n    run the testrunner\n\nhelp\n    this message\n    \nPress the <return> key to run the test again with the same arguments.\n\nIf you have readline you can use that to search your history.\n'

def setup_paths(defaults, software_home, buildout_home):
    """
    this code is from Zope's test.py
    """
    import Products
    products = []
    for path in Products.__path__:
        if not path.startswith(software_home):
            folders = [ f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)) if not f.startswith('.') if not f == 'CVS' ]
            if folders:
                for folder in folders:
                    package = os.path.join(path, folder)
                    if os.path.exists(os.path.join(package, '__init__.py')):
                        products.append(package)

    for product in products:
        defaults += ['--package-path', product, 'Products.%s' % os.path.split(product)[(-1)]]

    paths = sys.path
    for path in paths:
        if path != buildout_home:
            defaults += ['--test-path', path]

    return defaults


def preload_plone(conf):
    print 'Preloading Plone ...'
    from Products.PloneTestCase.layer import PloneSite
    from Products.PloneTestCase import PloneTestCase as ptc
    ptc.setupPloneSite()
    setup_layers = {}
    testrunner.setup_layer(PloneSite, setup_layers)
    del setup_layers[PloneSite]
    return setup_layers


def testrunner_defaults():
    defaults = ('--tests-pattern ^tests$ -v').split()
    defaults += ['-k']
    return defaults


original_signal_handler = None

def register_signal_handlers(pid):
    """propogate signals to child process"""

    def interrupt_handler(signum, frame, pid=pid):
        try:
            os.kill(pid, signal.SIGKILL)
            print
        except OSError, e:
            print str(e), pid

    signal.signal(signal.SIGINT, interrupt_handler)


def default_int_handler(signum, frame):
    print "\nInterrupt received. Type 'exit' to quit."


def ignore_signal_handlers():
    """restore signal handler"""
    signal.signal(signal.SIGINT, default_int_handler)