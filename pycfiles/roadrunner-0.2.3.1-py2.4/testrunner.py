# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/roadrunner/testrunner.py
# Compiled at: 2009-06-16 00:05:39
"""Test runner

$Id: testrunner.py 69364 2006-08-07 15:56:38Z adamg $

PATCHED VERSION for roadrunner
"""
import gc, glob, logging, optparse, os, pdb, re, sys, tempfile, threading, time, trace, traceback, types, unittest
try:
    import hotshot, hotshot.stats
except ImportError:
    hotshot = None

real_pdb_set_trace = pdb.set_trace
osettrace = sys.settrace

def settrace(trace):
    if trace is None:
        return
    osettrace(trace)
    return


class TestIgnore:
    __module__ = __name__

    def __init__(self, options):
        self._test_dirs = [ self._filenameFormat(d[0]) + os.path.sep for d in test_dirs(options, {}) ]
        self._ignore = {}
        self._ignored = self._ignore.get

    def names(self, filename, modulename):
        if modulename == '<string>':
            return True
        filename = self._filenameFormat(filename)
        ignore = self._ignored(filename)
        if ignore is None:
            ignore = True
            if filename is not None:
                for d in self._test_dirs:
                    if filename.startswith(d):
                        ignore = False
                        break

            self._ignore[filename] = ignore
        return ignore

    def _filenameFormat(self, filename):
        return os.path.abspath(filename)


if sys.platform == 'win32':
    OldTestIgnore = TestIgnore

    class TestIgnore(OldTestIgnore):
        __module__ = __name__

        def _filenameFormat(self, filename):
            return os.path.normcase(os.path.abspath(filename))


class TestTrace(trace.Trace):
    """Simple tracer.

    >>> tracer = TestTrace(None, count=False, trace=False)

    Simple rules for use: you can't stop the tracer if it not started
    and you can't start the tracer if it already started:

    >>> tracer.stop()
    Traceback (most recent call last):
        File 'testrunner.py'
    AssertionError: can't stop if not started

    >>> tracer.start()
    >>> tracer.start()
    Traceback (most recent call last):
        File 'testrunner.py'
    AssertionError: can't start if already started

    >>> tracer.stop()
    >>> tracer.stop()
    Traceback (most recent call last):
        File 'testrunner.py'
    AssertionError: can't stop if not started
    """
    __module__ = __name__

    def __init__(self, options, **kw):
        trace.Trace.__init__(self, **kw)
        if options is not None:
            self.ignore = TestIgnore(options)
        self.started = False
        return

    def start(self):
        assert not self.started, "can't start if already started"
        if not self.donothing:
            sys.settrace = settrace
            sys.settrace(self.globaltrace)
            threading.settrace(self.globaltrace)
        self.started = True

    def stop(self):
        assert self.started, "can't stop if not started"
        if not self.donothing:
            sys.settrace = osettrace
            sys.settrace(None)
            threading.settrace(None)
        self.started = False
        return


class EndRun(Exception):
    """Indicate that the existing run call should stop

    Used to prevent additional test output after post-mortem debugging.
    """
    __module__ = __name__


def strip_py_ext(options, path):
    """Return path without its .py (or .pyc or .pyo) extension, or None.

    If options.usecompiled is false:
        If path ends with ".py", the path without the extension is returned.
        Else None is returned.

    If options.usecompiled is true:
        If Python is running with -O, a .pyo extension is also accepted.
        If Python is running without -O, a .pyc extension is also accepted.
    """
    if path.endswith('.py'):
        return path[:-3]
    if options.usecompiled:
        if __debug__:
            ext = '.pyc'
        else:
            ext = '.pyo'
        if path.endswith(ext):
            return path[:-len(ext)]
    return


def contains_init_py(options, fnamelist):
    """Return true iff fnamelist contains a suitable spelling of __init__.py.

    If options.usecompiled is false, this is so iff "__init__.py" is in
    the list.

    If options.usecompiled is true, then "__init__.pyo" is also acceptable
    if Python is running with -O, and "__init__.pyc" is also acceptable if
    Python is running without -O.
    """
    if '__init__.py' in fnamelist:
        return True
    if options.usecompiled:
        if __debug__:
            return '__init__.pyc' in fnamelist
        else:
            return '__init__.pyo' in fnamelist
    return False


def run(defaults=None, args=None, setup_layers={}):
    if args is None:
        args = sys.argv
    configure_logging()
    old_reporting_flags = doctest.set_unittest_reportflags(0)
    if len(args) > 1 and args[1] == '--resume-layer':
        args.pop(1)
        resume_layer = args.pop(1)
        resume_number = int(args.pop(1))
        defaults = []
        while len(args) > 1 and args[1] == '--default':
            args.pop(1)
            defaults.append(args.pop(1))

        sys.stdin = FakeInputContinueGenerator()
    else:
        resume_layer = resume_number = None
    options = get_options(args, defaults)
    if options.fail:
        return True
    options.testrunner_defaults = defaults
    options.resume_layer = resume_layer
    options.resume_number = resume_number
    pdb.set_trace = real_pdb_set_trace
    if hotshot is None and options.profile:
        print "The Python you're using doesn't seem to have the profiler so you can't use the --profile switch."
        sys.exit()
    if options.profile and sys.version_info[:3] <= (2, 4, 1) and __debug__:
        print 'Because of a bug in Python < 2.4.1, profiling during tests requires the -O option be passed to Python (not the test runner).'
        sys.exit()
    if options.coverage:
        tracer = TestTrace(options, trace=False, count=True)
        tracer.start()
    else:
        tracer = None
    if options.profile:
        prof_prefix = 'tests_profile.'
        prof_suffix = '.prof'
        prof_glob = prof_prefix + '*' + prof_suffix
        if not options.resume_layer:
            for file_name in glob.glob(prof_glob):
                os.unlink(file_name)

        (oshandle, file_path) = tempfile.mkstemp(prof_suffix, prof_prefix, '.')
        prof = hotshot.Profile(file_path)
        prof.start()
    try:
        try:
            failed = not run_with_options(options, setup_layers=setup_layers)
        except EndRun:
            failed = True

    finally:
        if tracer:
            tracer.stop()
        if options.profile:
            prof.stop()
            prof.close()
            os.close(oshandle)
    if options.profile and not options.resume_layer:
        stats = None
        for file_name in glob.glob(prof_glob):
            loaded = hotshot.stats.load(file_name)
            if stats is None:
                stats = loaded
            else:
                stats.add(loaded)

        stats.sort_stats('cumulative', 'calls')
        stats.print_stats(50)
    if tracer:
        coverdir = os.path.join(os.getcwd(), options.coverage)
        r = tracer.results()
        r.write_results(summary=True, coverdir=coverdir)
    doctest.set_unittest_reportflags(old_reporting_flags)
    return failed


def run_with_options(options, found_suites=None, setup_layers={}):
    """Find and run tests
    
    Passing a list of suites using the found_suites parameter will cause
    that list of suites to be used instead of attempting to load them from
    the filesystem. This is useful for unit testing the test runner.

    Returns True if all tests passed, or False if there were any failures
    of any kind.
    """
    global _layer_name_cache
    _layer_name_cache = {}
    if options.resume_layer:
        original_stderr = sys.stderr
        sys.stderr = sys.stdout
    elif options.verbose:
        if options.all:
            print 'Running tests at all levels'
        else:
            print 'Running tests at level %d' % options.at_level
    old_threshold = gc.get_threshold()
    if options.gc:
        if len(options.gc) > 3:
            print 'Too many --gc options'
            sys.exit(1)
        if options.gc[0]:
            print 'Cyclic garbage collection threshold set to: %s' % `(tuple(options.gc))`
        else:
            print 'Cyclic garbage collection is disabled.'
        gc.set_threshold(*options.gc)
    old_flags = gc.get_debug()
    if options.gc_option:
        new_flags = 0
        for op in options.gc_option:
            new_flags |= getattr(gc, op)

        gc.set_debug(new_flags)
    old_reporting_flags = doctest.set_unittest_reportflags(0)
    reporting_flags = 0
    if options.ndiff:
        reporting_flags = doctest.REPORT_NDIFF
    if options.udiff:
        if reporting_flags:
            print 'Can only give one of --ndiff, --udiff, or --cdiff'
            sys.exit(1)
        reporting_flags = doctest.REPORT_UDIFF
    if options.cdiff:
        if reporting_flags:
            print 'Can only give one of --ndiff, --udiff, or --cdiff'
            sys.exit(1)
        reporting_flags = doctest.REPORT_CDIFF
    if options.report_only_first_failure:
        reporting_flags |= doctest.REPORT_ONLY_FIRST_FAILURE
    if reporting_flags:
        doctest.set_unittest_reportflags(reporting_flags)
    else:
        doctest.set_unittest_reportflags(old_reporting_flags)
    for path in options.path:
        if path not in sys.path:
            sys.path.append(path)

    remove_stale_bytecode(options)
    tests_by_layer_name = find_tests(options, found_suites)
    ran = 0
    failures = []
    errors = []
    nlayers = 0
    import_errors = tests_by_layer_name.pop(None, None)
    if import_errors:
        print 'Test-module import failures:'
        for error in import_errors:
            (
             print_traceback('Module: %s\n' % error.module, error.exc_info),)

        print
    if 'unit' in tests_by_layer_name:
        tests = tests_by_layer_name.pop('unit')
        if not options.non_unit and not options.resume_layer:
            if options.layer:
                should_run = False
                for pat in options.layer:
                    if pat('unit'):
                        should_run = True
                        break

            else:
                should_run = True
            if should_run:
                print 'Running unit tests:'
                nlayers += 1
                ran += run_tests(options, tests, 'unit', failures, errors)
    layers_to_run = list(ordered_layers(tests_by_layer_name))
    if options.resume_layer is not None:
        layers_to_run = [ (layer_name, layer, tests) for (layer_name, layer, tests) in layers_to_run if layer_name == options.resume_layer ]
    elif options.layer:
        layers_to_run = [ (layer_name, layer, tests) for (layer_name, layer, tests) in layers_to_run if filter(None, [ pat(layer_name) for pat in options.layer ]) ]
    for (layer_name, layer, tests) in layers_to_run:
        nlayers += 1
        try:
            ran += run_layer(options, layer_name, layer, tests, setup_layers, failures, errors)
        except CanNotTearDown:
            setup_layers = None
            if not options.resume_layer:
                ran += resume_tests(options, layer_name, layers_to_run, failures, errors)
                break

    if setup_layers:
        if options.resume_layer == None:
            print 'Tearing down left over layers:'
        tear_down_unneeded((), setup_layers, True)
    if options.resume_layer:
        sys.stdout.close()
        print >> original_stderr, ran, len(failures), len(errors)
        for (test, exc_info) in failures:
            print >> original_stderr, (' ').join(str(test).strip().split('\n'))

        for (test, exc_info) in errors:
            print >> original_stderr, (' ').join(str(test).strip().split('\n'))

    else:
        if options.verbose > 1:
            if errors:
                print
                print 'Tests with errors:'
                for (test, exc_info) in errors:
                    print '  ', test

            if failures:
                print
                print 'Tests with failures:'
                for (test, exc_info) in failures:
                    print '  ', test

        if nlayers != 1:
            print 'Total: %s tests, %s failures, %s errors' % (ran, len(failures), len(errors))
        if import_errors:
            print
            print 'Test-modules with import problems:'
            for test in import_errors:
                print '  ' + test.module

    doctest.set_unittest_reportflags(old_reporting_flags)
    if options.gc_option:
        gc.set_debug(old_flags)
    if options.gc:
        gc.set_threshold(*old_threshold)
    return not bool(import_errors or failures or errors)


def run_tests(options, tests, name, failures, errors):
    repeat = options.repeat or 1
    repeat_range = iter(range(repeat))
    ran = 0
    gc.collect()
    lgarbage = len(gc.garbage)
    sumrc = 0
    if options.report_refcounts:
        if options.verbose:
            track = TrackRefs()
        rc = sys.gettotalrefcount()
    for i in repeat_range:
        if repeat > 1:
            print 'Iteration', i + 1
        if options.verbose > 0 or options.progress:
            print '  Running:'
        result = TestResult(options, tests, layer_name=name)
        t = time.time()
        if options.post_mortem:
            for test in tests:
                if result.shouldStop:
                    break
                result.startTest(test)
                state = test.__dict__.copy()
                try:
                    try:
                        test.debug()
                    except:
                        result.addError(test, sys.exc_info()[:2] + (sys.exc_info()[2].tb_next,))
                    else:
                        result.addSuccess(test)

                finally:
                    result.stopTest(test)
                test.__dict__.clear()
                test.__dict__.update(state)

        for test in tests:
            if result.shouldStop:
                break
            state = test.__dict__.copy()
            test(result)
            test.__dict__.clear()
            test.__dict__.update(state)

        t = time.time() - t
        if options.verbose == 1 or options.progress:
            result.stopTests()
            print
        failures.extend(result.failures)
        errors.extend(result.errors)
        print '  Ran %s tests with %s failures and %s errors in %.3f seconds.' % (result.testsRun, len(result.failures), len(result.errors), t)
        ran = result.testsRun
        gc.collect()
        if len(gc.garbage) > lgarbage:
            print 'Tests generated new (%d) garbage:' % (len(gc.garbage) - lgarbage)
            print gc.garbage[lgarbage:]
            lgarbage = len(gc.garbage)
        if options.report_refcounts:
            try:
                sys.stdout.getvalue()
            except AttributeError:
                pass
            else:
                prev = rc
                rc = sys.gettotalrefcount()
                if options.verbose:
                    track.update()
                    if i:
                        print '  sum detail refcount=%-8d sys refcount=%-8d change=%-6d' % (track.n, rc, rc - prev)
                        if options.verbose:
                            track.output()
                    else:
                        track.delta = None
                elif i:
                    print '  sys refcount=%-8d change=%-6d' % (rc, rc - prev)

    return ran


def run_layer(options, layer_name, layer, tests, setup_layers, failures, errors):
    gathered = []
    gather_layers(layer, gathered)
    needed = dict([ (l, 1) for l in gathered ])
    if options.resume_number != 0:
        print 'Running %s tests:' % layer_name
    tear_down_unneeded(needed, setup_layers)
    if options.resume_layer != None:
        print '  Running in a subprocess.'
    setup_layer(layer, setup_layers)
    return run_tests(options, tests, layer_name, failures, errors)


def resume_tests(options, layer_name, layers, failures, errors):
    layers = [ l for (l, _, _) in layers ]
    layers = layers[layers.index(layer_name):]
    rantotal = 0
    resume_number = 0
    for layer_name in layers:
        args = [
         sys.executable, options.original_testrunner_args[0], '--resume-layer', layer_name, str(resume_number)]
        resume_number += 1
        for d in options.testrunner_defaults:
            args.extend(['--default', d])

        args.extend(options.original_testrunner_args[1:])
        if hotshot is not None and options.profile and sys.version_info[:3] <= (2,
                                                                                4,
                                                                                1):
            args.insert(1, '-O')
        if sys.platform.startswith('win'):
            args = args[0] + ' ' + (' ').join([ '"' + a.replace('\\', '\\\\').replace('"', '\\"') + '"' for a in args[1:] ])
        (subin, subout, suberr) = os.popen3(args)
        for l in subout:
            sys.stdout.write(l)

        line = suberr.readline()
        try:
            (ran, nfail, nerr) = map(int, line.strip().split())
        except:
            raise SubprocessError(line + suberr.read())

        while nfail > 0:
            nfail -= 1
            failures.append((suberr.readline().strip(), None))

        while nerr > 0:
            nerr -= 1
            errors.append((suberr.readline().strip(), None))

        rantotal += ran

    return rantotal


class SubprocessError(Exception):
    """An error occurred when running a subprocess
    """
    __module__ = __name__


class CanNotTearDown(Exception):
    """Couldn't tear down a test"""
    __module__ = __name__


def tear_down_unneeded(needed, setup_layers, optional=False):
    unneeded = [ l for l in setup_layers if l not in needed ]
    unneeded = order_by_bases(unneeded)
    unneeded.reverse()
    for l in unneeded:
        print '  Tear down %s' % name_from_layer(l),
        t = time.time()
        try:
            if hasattr(l, 'tearDown'):
                l.tearDown()
        except NotImplementedError:
            print '... not supported'
            if not optional:
                raise CanNotTearDown(l)
        else:
            print 'in %.3f seconds.' % (time.time() - t)

        del setup_layers[l]


def setup_layer(layer, setup_layers):
    assert layer is not object
    if layer not in setup_layers:
        for base in layer.__bases__:
            if base is not object:
                setup_layer(base, setup_layers)

        print '  Set up %s' % name_from_layer(layer),
        t = time.time()
        if hasattr(layer, 'setUp'):
            layer.setUp()
        print 'in %.3f seconds.' % (time.time() - t)
        setup_layers[layer] = 1


def dependencies(bases, result):
    for base in bases:
        result[base] = 1
        dependencies(base.__bases__, result)


class TestResult(unittest.TestResult):
    __module__ = __name__
    max_width = 80

    def __init__(self, options, tests, layer_name=None):
        unittest.TestResult.__init__(self)
        self.options = options
        if layer_name != 'unit':
            layers = []
            gather_layers(layer_from_name(layer_name), layers)
            self.layers = order_by_bases(layers)
        else:
            self.layers = []
        if options.progress:
            count = 0
            for test in tests:
                count += test.countTestCases()

            self.count = count
        self.last_width = 0
        if options.progress:
            try:
                import curses
            except ImportError:
                sys.modules['curses'] = None
            else:
                try:
                    curses.setupterm()
                except TypeError:
                    pass
                else:
                    self.max_width = curses.tigetnum('cols')
        return

    def getShortDescription(self, test, room):
        room -= 1
        s = str(test)
        if len(s) > room:
            pos = s.find(' (')
            if pos >= 0:
                w = room - (pos + 5)
                if w < 1:
                    s = s[:room - 3] + '...'
                else:
                    pre = s[:pos + 2]
                    post = s[-w:]
                    s = '%s...%s' % (pre, post)
            else:
                w = room - 4
                s = '... ' + s[-w:]
        return ' ' + s[:room]

    def testSetUp(self):
        """A layer may define a setup method to be called before each
        individual test.
        """
        for layer in self.layers:
            if hasattr(layer, 'testSetUp'):
                layer.testSetUp()

    def testTearDown(self):
        """A layer may define a teardown method to be called after each
           individual test.
           
           This is useful for clearing the state of global
           resources or resetting external systems such as relational
           databases or daemons.
        """
        for layer in self.layers[-1::-1]:
            if hasattr(layer, 'testTearDown'):
                layer.testTearDown()

    def startTest(self, test):
        self.testSetUp()
        unittest.TestResult.startTest(self, test)
        testsRun = self.testsRun - 1
        count = test.countTestCases()
        self.testsRun = testsRun + count
        options = self.options
        self.test_width = 0
        if options.progress:
            if self.last_width:
                sys.stdout.write('\r' + ' ' * self.last_width + '\r')
            s = '    %d/%d (%.1f%%)' % (self.testsRun, self.count, self.testsRun * 100.0 / self.count)
            sys.stdout.write(s)
            self.test_width += len(s)
            if options.verbose == 1:
                room = self.max_width - self.test_width - 1
                s = self.getShortDescription(test, room)
                sys.stdout.write(s)
                self.test_width += len(s)
        elif options.verbose == 1:
            for i in range(count):
                sys.stdout.write('.')
                testsRun += 1

        if options.verbose > 1:
            s = str(test)
            sys.stdout.write(' ')
            sys.stdout.write(s)
            self.test_width += len(s) + 1
        sys.stdout.flush()
        self._threads = threading.enumerate()
        self._start_time = time.time()

    def addSuccess(self, test):
        if self.options.verbose > 2:
            t = max(time.time() - self._start_time, 0.0)
            s = ' (%.3f ms)' % t
            sys.stdout.write(s)
            self.test_width += len(s) + 1

    def addError(self, test, exc_info):
        if self.options.verbose > 2:
            print ' (%.3f ms)' % (time.time() - self._start_time)
        unittest.TestResult.addError(self, test, exc_info)
        print
        self._print_traceback('Error in test %s' % test, exc_info)
        if self.options.post_mortem:
            if self.options.resume_layer:
                print
                print '*' * 70
                print "Can't post-mortem debug when running a layer as a subprocess!"
                print '*' * 70
                print
            else:
                post_mortem(exc_info)
        self.test_width = self.last_width = 0

    def addFailure(self, test, exc_info):
        if self.options.verbose > 2:
            print ' (%.3f ms)' % (time.time() - self._start_time)
        unittest.TestResult.addFailure(self, test, exc_info)
        print
        self._print_traceback('Failure in test %s' % test, exc_info)
        if self.options.post_mortem:
            post_mortem(exc_info)
        self.test_width = self.last_width = 0

    def stopTests(self):
        if self.options.progress and self.last_width:
            sys.stdout.write('\r' + ' ' * self.last_width + '\r')

    def stopTest(self, test):
        self.testTearDown()
        if self.options.progress:
            self.last_width = self.test_width
        elif self.options.verbose > 1:
            print
        if gc.garbage:
            print 'The following test left garbage:'
            print test
            print gc.garbage
        new_threads = [ t for t in threading.enumerate() if t.isAlive() if t not in self._threads ]
        if new_threads:
            print 'The following test left new threads behind:'
            print test
            print 'New thread(s):', new_threads
        sys.stdout.flush()

    def _print_traceback(self, msg, exc_info):
        print_traceback(msg, exc_info)


doctest_template = '\nFile "%s", line %s, in %s\n\n%s\nWant:\n%s\nGot:\n%s\n'

class FakeInputContinueGenerator:
    __module__ = __name__

    def readline(self):
        print 'c\n'
        print '*' * 70
        print "Can't use pdb.set_trace when running a layer as a subprocess!"
        print '*' * 70
        print
        return 'c\n'


def print_traceback(msg, exc_info):
    print
    print msg
    v = exc_info[1]
    if isinstance(v, doctest.DocTestFailureException):
        tb = v.args[0]
    elif isinstance(v, doctest.DocTestFailure):
        tb = doctest_template % (v.test.filename, v.test.lineno + v.example.lineno + 1, v.test.name, v.example.source, v.example.want, v.got)
    else:
        tb = ('').join(traceback.format_exception(*exc_info))
    print tb


def post_mortem(exc_info):
    err = exc_info[1]
    if isinstance(err, (doctest.UnexpectedException, doctest.DocTestFailure)):
        if isinstance(err, doctest.UnexpectedException):
            exc_info = err.exc_info
            if exc_info[2].tb_frame.f_code.co_filename == '<string>':
                print_doctest_location(err)
        else:
            print_doctest_location(err)
            try:
                exec 'raise ValueError("Expected and actual output are different")' in err.test.globs
            except:
                exc_info = sys.exc_info()

    print '%s:' % (exc_info[0],)
    print exc_info[1]
    pdb.post_mortem(exc_info[2])
    raise EndRun


def print_doctest_location(err):
    filename = err.test.filename
    if filename.endswith('.pyc'):
        filename = filename[:-1]
    print '> %s(%s)_()' % (filename, err.test.lineno + err.example.lineno + 1)


def ordered_layers(tests_by_layer_name):
    layer_names = dict([ (layer_from_name(layer_name), layer_name) for layer_name in tests_by_layer_name ])
    for layer in order_by_bases(layer_names):
        layer_name = layer_names[layer]
        yield (layer_name, layer, tests_by_layer_name[layer_name])


def gather_layers(layer, result):
    if layer is not object:
        result.append(layer)
    for b in layer.__bases__:
        gather_layers(b, result)


def layer_from_name(layer_name):
    """Return the layer for the corresponding layer_name by discovering
       and importing the necessary module if necessary.

       Note that a name -> layer cache is maintained by name_from_layer
       to allow locating layers in cases where it would otherwise be
       impossible.
    """
    if _layer_name_cache.has_key(layer_name):
        return _layer_name_cache[layer_name]
    layer_names = layer_name.split('.')
    layer_module, module_layer_name = layer_names[:-1], layer_names[(-1)]
    return getattr(import_name(('.').join(layer_module)), module_layer_name)


def order_by_bases(layers):
    """Order the layers from least to most specific (bottom to top)
    """
    named_layers = [ (name_from_layer(layer), layer) for layer in layers ]
    named_layers.sort()
    named_layers.reverse()
    gathered = []
    for (name, layer) in named_layers:
        gather_layers(layer, gathered)

    gathered.reverse()
    seen = {}
    result = []
    for layer in gathered:
        if layer not in seen:
            seen[layer] = 1
            if layer in layers:
                result.append(layer)

    return result


_layer_name_cache = {}

def name_from_layer(layer):
    """Determine a name for the Layer using the namespace to avoid conflicts.

    We also cache a name -> layer mapping to enable layer_from_name to work
    in cases where the layer cannot be imported (such as layers defined
    in doctests)
    """
    if layer.__module__ == '__builtin__':
        name = layer.__name__
    else:
        name = layer.__module__ + '.' + layer.__name__
    _layer_name_cache[name] = layer
    return name


def find_tests(options, found_suites=None):
    """Creates a dictionary mapping layer name to a suite of tests to be run
    in that layer.

    Passing a list of suites using the found_suites parameter will cause
    that list of suites to be used instead of attempting to load them from
    the filesystem. This is useful for unit testing the test runner.
    """
    suites = {}
    if found_suites is None:
        found_suites = find_suites(options)
    for suite in found_suites:
        for (test, layer_name) in tests_from_suite(suite, options):
            suite = suites.get(layer_name)
            if not suite:
                suite = suites[layer_name] = unittest.TestSuite()
            suite.addTest(test)

    return suites


def tests_from_suite(suite, options, dlevel=1, dlayer='unit'):
    """Returns a sequence of (test, layer_name)

    The tree of suites is recursively visited, with the most specific
    layer taking precidence. So if a TestCase with a layer of 'foo' is
    contained in a TestSuite with a layer of 'bar', the test case would be
    returned with 'foo' as the layer.

    Tests are also filtered out based on the test level and test selection
    filters stored in the options.
    """
    level = getattr(suite, 'level', dlevel)
    layer = getattr(suite, 'layer', dlayer)
    if not isinstance(layer, basestring):
        layer = name_from_layer(layer)
    if isinstance(suite, unittest.TestSuite):
        for possible_suite in suite:
            for r in tests_from_suite(possible_suite, options, level, layer):
                yield r

    if isinstance(suite, StartUpFailure):
        yield (
         suite, None)
    elif level <= options.at_level:
        for pat in options.test:
            if pat(str(suite)):
                yield (
                 suite, layer)
                break

    return


def find_suites(options):
    for (fpath, package) in find_test_files(options):
        for (prefix, prefix_package) in options.prefix:
            if fpath.startswith(prefix) and package == prefix_package:
                noprefix = fpath[len(prefix):]
                noext = strip_py_ext(options, noprefix)
                assert noext is not None
                module_name = noext.replace(os.path.sep, '.')
                if package:
                    module_name = package + '.' + module_name
                for filter in options.module:
                    if filter(module_name):
                        break
                else:
                    continue

                try:
                    module = import_name(module_name)
                except:
                    suite = StartUpFailure(options, module_name, sys.exc_info()[:2] + (sys.exc_info()[2].tb_next.tb_next,))
                else:
                    try:
                        suite = getattr(module, options.suite_name)()
                        if isinstance(suite, unittest.TestSuite):
                            check_suite(suite, module_name)
                        else:
                            raise TypeError('Invalid test_suite, %r, in %s' % (suite, module_name))
                    except:
                        suite = StartUpFailure(options, module_name, sys.exc_info()[:2] + (None, ))

                    yield suite
                    break

    return


def check_suite(suite, module_name):
    for x in suite:
        if isinstance(x, unittest.TestSuite):
            check_suite(x, module_name)
        elif not isinstance(x, unittest.TestCase):
            raise TypeError('Invalid test, %r,\nin test_suite from %s' % (x, module_name))


class StartUpFailure:
    __module__ = __name__

    def __init__(self, options, module, exc_info):
        if options.post_mortem:
            post_mortem(exc_info)
        self.module = module
        self.exc_info = exc_info


def find_test_files(options):
    found = {}
    for (f, package) in find_test_files_(options):
        if f not in found:
            found[f] = 1
            yield (f, package)


identifier = re.compile('[_a-zA-Z]\\w*$').match

def find_test_files_(options):
    tests_pattern = options.tests_pattern
    test_file_pattern = options.test_file_pattern

    def update_root2ext(dirname, noext, withext):
        key = os.path.join(dirname, noext)
        new = os.path.join(dirname, withext)
        if key in root2ext:
            root2ext[key] = min(root2ext[key], new)
        else:
            root2ext[key] = new

    for (p, package) in test_dirs(options, {}):
        for (dirname, dirs, files) in walk_with_symlinks(options, p):
            if dirname != p and not contains_init_py(options, files):
                continue
            root2ext = {}
            dirs[:] = filter(identifier, dirs)
            d = os.path.split(dirname)[1]
            if tests_pattern(d) and contains_init_py(options, files):
                for file in files:
                    noext = strip_py_ext(options, file)
                    if noext and test_file_pattern(noext):
                        update_root2ext(dirname, noext, file)

            for file in files:
                noext = strip_py_ext(options, file)
                if noext and tests_pattern(noext):
                    update_root2ext(dirname, noext, file)

            winners = root2ext.values()
            winners.sort()
            for file in winners:
                yield (
                 file, package)


def walk_with_symlinks(options, dir):
    for (dirpath, dirs, files) in os.walk(dir):
        dirs.sort()
        files.sort()
        dirs[:] = [ d for d in dirs if d not in options.ignore_dir ]
        yield (dirpath, dirs, files)
        for d in dirs:
            p = os.path.join(dirpath, d)
            if os.path.islink(p):
                for (sdirpath, sdirs, sfiles) in walk_with_symlinks(options, p):
                    yield (
                     sdirpath, sdirs, sfiles)


compiled_sufixes = ('.pyc', '.pyo')

def remove_stale_bytecode(options):
    if options.keepbytecode:
        return
    for (p, _) in options.test_path:
        for (dirname, dirs, files) in walk_with_symlinks(options, p):
            for file in files:
                if file[-4:] in compiled_sufixes and file[:-1] not in files:
                    fullname = os.path.join(dirname, file)
                    print 'Removing stale bytecode file', fullname
                    os.unlink(fullname)


def test_dirs(options, seen):
    if options.package:
        for p in options.package:
            p = import_name(p)
            for p in p.__path__:
                p = os.path.abspath(p)
                if p in seen:
                    continue
                for (prefix, package) in options.prefix:
                    if p.startswith(prefix) or p == prefix[:-1]:
                        seen[p] = 1
                        yield (p, package)
                        break

    for dpath in options.test_path:
        yield dpath


def import_name(name):
    __import__(name)
    return sys.modules[name]


def configure_logging():
    """Initialize the logging module."""
    import logging.config
    logini = os.path.abspath('log.ini')
    if os.path.exists(logini):
        logging.config.fileConfig(logini)
    else:
        root = logging.getLogger()
        root.addHandler(NullHandler())
        logging.basicConfig()
    if os.environ.has_key('LOGGING'):
        level = int(os.environ['LOGGING'])
        logging.getLogger().setLevel(level)


class NullHandler(logging.Handler):
    """Logging handler that drops everything on the floor.

    We require silence in the test environment.  Hush.
    """
    __module__ = __name__

    def emit(self, record):
        pass


class TrackRefs(object):
    """Object to track reference counts across test runs."""
    __module__ = __name__

    def __init__(self):
        self.type2count = {}
        self.type2all = {}
        self.delta = None
        self.n = 0
        self.update()
        self.delta = None
        return

    def update(self):
        gc.collect()
        obs = sys.getobjects(0)
        type2count = {}
        type2all = {}
        n = 0
        for o in obs:
            if type(o) is str and o == '<dummy key>':
                continue
            all = sys.getrefcount(o) - 3
            n += all
            t = type(o)
            if t is types.InstanceType:
                t = o.__class__
            if t in type2count:
                type2count[t] += 1
                type2all[t] += all
            else:
                type2count[t] = 1
                type2all[t] = all

        ct = [ (type_or_class_title(t), type2count[t] - self.type2count.get(t, 0), type2all[t] - self.type2all.get(t, 0)) for t in type2count.iterkeys() ]
        ct += [ (type_or_class_title(t), -self.type2count[t], -self.type2all[t]) for t in self.type2count.iterkeys() if t not in type2count ]
        ct.sort()
        self.delta = ct
        self.type2count = type2count
        self.type2all = type2all
        self.n = n

    def output(self):
        printed = False
        s1 = s2 = 0
        for (t, delta1, delta2) in self.delta:
            if delta1 or delta2:
                if not printed:
                    print '    Leak details, changes in instances and refcounts by type/class:'
                    print '    %-55s %6s %6s' % ('type/class', 'insts', 'refs')
                    print '    %-55s %6s %6s' % ('-' * 55, '-----', '----')
                    printed = True
                print '    %-55s %6d %6d' % (t, delta1, delta2)
                s1 += delta1
                s2 += delta2

        if printed:
            print '    %-55s %6s %6s' % ('-' * 55, '-----', '----')
            print '    %-55s %6s %6s' % ('total', s1, s2)
        self.delta = None
        return


def type_or_class_title(t):
    module = getattr(t, '__module__', '__builtin__')
    if module == '__builtin__':
        return t.__name__
    return '%s.%s' % (module, t.__name__)


parser = optparse.OptionParser('Usage: %prog [options] [MODULE] [TEST]')
searching = optparse.OptionGroup(parser, 'Searching and filtering', 'Options in this group are used to define which tests to run.\n')
searching.add_option('--package', '--dir', '-s', action='append', dest='package', help="Search the given package's directories for tests.  This can be\nspecified more than once to run tests in multiple parts of the source\ntree.  For example, if refactoring interfaces, you don't want to see\nthe way you have broken setups for tests in other packages. You *just*\nwant to run the interface tests.\n\nPackages are supplied as dotted names.  For compatibility with the old\ntest runner, forward and backward slashed in package names are\nconverted to dots.\n\n(In the special case of packages spread over multiple directories,\nonly directories within the test search path are searched. See the\n--path option.)\n\n")
searching.add_option('--module', '-m', action='append', dest='module', help='Specify a test-module filter as a regular expression.  This is a\ncase-sensitive regular expression, used in search (not match) mode, to\nlimit which test modules are searched for tests.  The regular\nexpressions are checked against dotted module names.  In an extension\nof Python regexp notation, a leading "!" is stripped and causes the\nsense of the remaining regexp to be negated (so "!bc" matches any\nstring that does not match "bc", and vice versa).  The option can be\nspecified multiple test-module filters.  Test modules matching any of\nthe test filters are searched.  If no test-module filter is specified,\nthen all test moduless are used.\n')
searching.add_option('--test', '-t', action='append', dest='test', help='Specify a test filter as a regular expression.  This is a\ncase-sensitive regular expression, used in search (not match) mode, to\nlimit which tests are run.  In an extension of Python regexp notation,\na leading "!" is stripped and causes the sense of the remaining regexp\nto be negated (so "!bc" matches any string that does not match "bc",\nand vice versa).  The option can be specified multiple test filters.\nTests matching any of the test filters are included.  If no test\nfilter is specified, then all tests are run.\n')
searching.add_option('--unit', '-u', action='store_true', dest='unit', help='Run only unit tests, ignoring any layer options.\n')
searching.add_option('--non-unit', '-f', action='store_true', dest='non_unit', help='Run tests other than unit tests.\n')
searching.add_option('--layer', action='append', dest='layer', help='Specify a test layer to run.  The option can be given multiple times\nto specify more than one layer.  If not specified, all layers are run.\nIt is common for the running script to provide default values for this\noption.  Layers are specified regular expressions, used in search\nmode, for dotted names of objects that define a layer.  In an\nextension of Python regexp notation, a leading "!" is stripped and\ncauses the sense of the remaining regexp to be negated (so "!bc"\nmatches any string that does not match "bc", and vice versa).  The\nlayer named \'unit\' is reserved for unit tests, however, take note of\nthe --unit and non-unit options.\n')
searching.add_option('-a', '--at-level', type='int', dest='at_level', help='Run the tests at the given level.  Any test at a level at or below\nthis is run, any test at a level above this is not run.  Level 0\nruns all tests.\n')
searching.add_option('--all', action='store_true', dest='all', help='Run tests at all levels.')
parser.add_option_group(searching)
reporting = optparse.OptionGroup(parser, 'Reporting', 'Reporting options control basic aspects of test-runner output\n')
reporting.add_option('--verbose', '-v', action='count', dest='verbose', help='Make output more verbose.\nIncrement the verbosity level.\n')
reporting.add_option('--quiet', '-q', action='store_true', dest='quiet', help='Make the output minimal, overriding any verbosity options.\n')
reporting.add_option('--progress', '-p', action='store_true', dest='progress', help='Output progress status\n')
reporting.add_option('-1', action='store_true', dest='report_only_first_failure', help='Report only the first failure in a doctest. (Examples after the\nfailure are still executed, in case they do any cleanup.)\n')
reporting.add_option('--ndiff', action='store_true', dest='ndiff', help='When there is a doctest failure, show it as a diff using the ndiff.py utility.\n')
reporting.add_option('--udiff', action='store_true', dest='udiff', help='When there is a doctest failure, show it as a unified diff.\n')
reporting.add_option('--cdiff', action='store_true', dest='cdiff', help='When there is a doctest failure, show it as a context diff.\n')
parser.add_option_group(reporting)
analysis = optparse.OptionGroup(parser, 'Analysis', 'Analysis options provide tools for analysing test output.\n')
analysis.add_option('--post-mortem', '-D', action='store_true', dest='post_mortem', help='Enable post-mortem debugging of test failures')
analysis.add_option('--gc', '-g', action='append', dest='gc', type='int', help='Set the garbage collector generation threshold.  This can be used\nto stress memory and gc correctness.  Some crashes are only\nreproducible when the threshold is set to 1 (agressive garbage\ncollection).  Do "--gc 0" to disable garbage collection altogether.\n\nThe --gc option can be used up to 3 times to specify up to 3 of the 3\nPython gc_threshold settings.\n\n')
analysis.add_option('--gc-option', '-G', action='append', dest='gc_option', type='choice', choices=['DEBUG_STATS', 'DEBUG_COLLECTABLE', 'DEBUG_UNCOLLECTABLE', 'DEBUG_INSTANCES', 'DEBUG_OBJECTS', 'DEBUG_SAVEALL', 'DEBUG_LEAK'], help='Set a Python gc-module debug flag.  This option can be used more than\nonce to set multiple flags.\n')
analysis.add_option('--repeat', '-N', action='store', type='int', dest='repeat', help='Repeat the testst the given number of times.  This option is used to\nmake sure that tests leave thier environment in the state they found\nit and, with the --report-refcounts option to look for memory leaks.\n')
analysis.add_option('--report-refcounts', '-r', action='store_true', dest='report_refcounts', help='After each run of the tests, output a report summarizing changes in\nrefcounts by object type.  This option that requires that Python was\nbuilt with the --with-pydebug option to configure.\n')
analysis.add_option('--coverage', action='store', type='string', dest='coverage', help='Perform code-coverage analysis, saving trace data to the directory\nwith the given name.  A code coverage summary is printed to standard\nout.\n')
analysis.add_option('--profile', action='store_true', dest='profile', help='Run the tests under hotshot and display the top 50 stats, sorted by\ncumulative time and number of calls.\n')

def do_pychecker(*args):
    if not os.environ.get('PYCHECKER'):
        os.environ['PYCHECKER'] = '-q'
    import pychecker.checker


analysis.add_option('--pychecker', action='callback', callback=do_pychecker, help='Run the tests under pychecker\n')
parser.add_option_group(analysis)
setup = optparse.OptionGroup(parser, 'Setup', 'Setup options are normally supplied by the testrunner script, although\nthey can be overridden by users.\n')
setup.add_option('--path', action='append', dest='path', help="Specify a path to be added to Python's search path.  This option can\nbe used multiple times to specify multiple search paths.  The path is\nusually specified by the test-runner script itself, rather than by\nusers of the script, although it can be overridden by users.  Only\ntests found in the path will be run.\n\nThis option also specifies directories to be searched for tests.\nSee the search_directory.\n")
setup.add_option('--test-path', action='append', dest='test_path', help='Specify a path to be searched for tests, but not added to the Python\nsearch path.  This option can be used multiple times to specify\nmultiple search paths.  The path is usually specified by the\ntest-runner script itself, rather than by users of the script,\nalthough it can be overridden by users.  Only tests found in the path\nwill be run.\n')
setup.add_option('--package-path', action='append', dest='package_path', nargs=2, help='Specify a path to be searched for tests, but not added to the Python\nsearch path.  Also specify a package for files found in this path.\nThis is used to deal with directories that are stiched into packages\nthat are not otherwise searched for tests.\n\nThis option takes 2 arguments.  The first is a path name. The second is\nthe package name.\n\nThis option can be used multiple times to specify\nmultiple search paths.  The path is usually specified by the\ntest-runner script itself, rather than by users of the script,\nalthough it can be overridden by users.  Only tests found in the path\nwill be run.\n')
setup.add_option('--tests-pattern', action='store', dest='tests_pattern', help='The test runner looks for modules containing tests.  It uses this\npattern to identify these modules.  The modules may be either packages\nor python files.\n\nIf a test module is a package, it uses the value given by the\ntest-file-pattern to identify python files within the package\ncontaining tests.\n')
setup.add_option('--suite-name', action='store', dest='suite_name', help="Specify the name of the object in each test_module that contains the\nmodule's test suite.\n")
setup.add_option('--test-file-pattern', action='store', dest='test_file_pattern', help='Specify a pattern for identifying python files within a tests package.\nSee the documentation for the --tests-pattern option.\n')
setup.add_option('--ignore_dir', action='append', dest='ignore_dir', help='Specifies the name of a directory to ignore when looking for tests.\n')
parser.add_option_group(setup)
other = optparse.OptionGroup(parser, 'Other', 'Other options')
other.add_option('--keepbytecode', '-k', action='store_true', dest='keepbytecode', help="Normally, the test runner scans the test paths and the test\ndirectories looking for and deleting pyc or pyo files without\ncorresponding py files.  This is to prevent spurious test failures due\nto finding compiled modules where source modules have been deleted.\nThis scan can be time consuming.  Using this option disables this\nscan.  If you know you haven't removed any modules since last running\nthe tests, can make the test run go much faster.\n")
other.add_option('--usecompiled', action='store_true', dest='usecompiled', help='Normally, a package must contain an __init__.py file, and only .py files\ncan contain test code.  When this option is specified, compiled Python\nfiles (.pyc and .pyo) can be used instead:  a directory containing\n__init__.pyc or __init__.pyo is also considered to be a package, and if\nfile XYZ.py contains tests but is absent while XYZ.pyc or XYZ.pyo exists\nthen the compiled files will be used.  This is necessary when running\ntests against a tree where the .py files have been removed after\ncompilation to .pyc/.pyo.  Use of this option implies --keepbytecode.\n')
parser.add_option_group(other)

def compile_filter(pattern):
    if pattern.startswith('!'):
        pattern = re.compile(pattern[1:]).search
        return lambda s: not pattern(s)
    return re.compile(pattern).search


def merge_options(options, defaults):
    odict = options.__dict__
    for (name, value) in defaults.__dict__.items():
        if value is not None and odict[name] is None:
            odict[name] = value

    return


default_setup_args = [
 '--tests-pattern', '^tests$', '--at-level', '1', '--ignore', '.svn', '--ignore', 'CVS', '--ignore', '{arch}', '--ignore', '.arch-ids', '--ignore', '_darcs', '--test-file-pattern', '^test', '--suite-name', 'test_suite']

def get_options(args=None, defaults=None):
    (default_setup, _) = parser.parse_args(default_setup_args)
    assert not _
    if defaults:
        (defaults, _) = parser.parse_args(defaults)
        assert not _
        merge_options(defaults, default_setup)
    else:
        defaults = default_setup
    if args is None:
        args = sys.argv
    original_testrunner_args = args
    args = args[1:]
    (options, positional) = parser.parse_args(args)
    merge_options(options, defaults)
    options.original_testrunner_args = original_testrunner_args
    options.fail = False
    if positional:
        module_filter = positional.pop(0)
        if module_filter != '.':
            if options.module:
                options.module.append(module_filter)
            else:
                options.module = [
                 module_filter]
        if positional:
            test_filter = positional.pop(0)
            if options.test:
                options.test.append(test_filter)
            else:
                options.test = [
                 test_filter]
            if positional:
                parser.error('Too mant positional arguments')
    options.ignore_dir = dict([ (d, 1) for d in options.ignore_dir ])
    options.test_file_pattern = re.compile(options.test_file_pattern).search
    options.tests_pattern = re.compile(options.tests_pattern).search
    options.test = map(compile_filter, options.test or '.')
    options.module = map(compile_filter, options.module or '.')
    if options.package:
        options.package = [ p.replace('/', '.').replace('\\', '.') for p in options.package ]
        options.package = [ re.sub('\\.$', '', p) for p in options.package ]
    options.path = map(os.path.abspath, options.path or ())
    options.test_path = map(os.path.abspath, options.test_path or ())
    options.test_path += options.path
    options.test_path = [ (path, '') for path in options.test_path ] + [ (os.path.abspath(path), package) for (path, package) in options.package_path or () ]
    options.prefix = [ (path + os.path.sep, package) for (path, package) in options.test_path ]
    if options.all:
        options.at_level = sys.maxint
    if options.unit:
        options.layer = [
         'unit']
    if options.layer:
        options.layer = map(compile_filter, options.layer)
    options.layer = options.layer and dict([ (l, 1) for l in options.layer ])
    if options.usecompiled:
        options.keepbytecode = options.usecompiled
    if options.quiet:
        options.verbose = 0
    if options.report_refcounts and options.repeat < 2:
        print '        You must use the --repeat (-N) option to specify a repeat\n        count greater than 1 when using the --report_refcounts (-r)\n        option.\n        '
        options.fail = True
        return options
    if options.report_refcounts and not hasattr(sys, 'gettotalrefcount'):
        print '        The Python you are running was not configured\n        with --with-pydebug. This is required to use\n        the --report-refcounts option.\n        '
        options.fail = True
        return options
    return options


if sys.version_info < (2, 4):

    def __iter__(suite):
        return iter(suite._tests)


    unittest.TestSuite.__iter__ = __iter__
    del __iter__

def test_suite():
    import renormalizing
    checker = renormalizing.RENormalizing([(re.compile("<class 'exceptions.(\\w+)Error'>:"), 'exceptions.\\1Error:'), (re.compile('^> [^\n]+->None$', re.M), '> ...->None'), (re.compile("'[A-Za-z]:\\\\"), "'"), (re.compile('\\\\\\\\'), '/'), (re.compile('\\\\'), '/'), (re.compile('/r'), '\\\\r'), (re.compile('\\r'), '\\\\r\n'), (re.compile('\\d+[.]\\d\\d\\d seconds'), 'N.NNN seconds'), (re.compile('\\d+[.]\\d\\d\\d ms'), 'N.NNN ms'), (re.compile('( |")[^\n]+testrunner-ex'), '\\1testrunner-ex'), (re.compile('( |")[^\n]+testrunner.py'), '\\1testrunner.py'), (re.compile('> [^\\n]*(doc|unit)test[.]py\\(\\d+\\)'), '\\1doctest.py(NNN)'), (re.compile('[.]py\\(\\d+\\)'), '.py(NNN)'), (re.compile('[.]py:\\d+'), '.py:NNN'), (re.compile(' line \\d+,', re.IGNORECASE), ' Line NNN,'),
     (
      re.compile('^ +File "[^\\n]+(doc|unit)test.py", [^\\n]+\\n[^\\n]+\\n', re.MULTILINE), ''), (re.compile('^> [^\n]+->None$', re.M), '> ...->None'), (re.compile('import pdb; pdb'), 'Pdb()')])

    def setUp(test):
        test.globs['saved-sys-info'] = (
         sys.path[:], sys.argv[:], sys.modules.copy(), gc.get_threshold())
        test.globs['this_directory'] = os.path.split(__file__)[0]
        test.globs['testrunner_script'] = __file__

    def tearDown(test):
        (sys.path[:], sys.argv[:]) = test.globs['saved-sys-info'][:2]
        gc.set_threshold(*test.globs['saved-sys-info'][3])
        sys.modules.clear()
        sys.modules.update(test.globs['saved-sys-info'][2])

    suites = [
     doctest.DocFileSuite('testrunner-arguments.txt', 'testrunner-coverage.txt', 'testrunner-debugging.txt', 'testrunner-edge-cases.txt', 'testrunner-errors.txt', 'testrunner-layers-ntd.txt', 'testrunner-layers.txt', 'testrunner-layers-api.txt', 'testrunner-progress.txt', 'testrunner-simple.txt', 'testrunner-test-selection.txt', 'testrunner-verbose.txt', 'testrunner-wo-source.txt', 'testrunner-repeat.txt', 'testrunner-gc.txt', 'testrunner-knit.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE, checker=checker), doctest.DocTestSuite()]
    if sys.platform == 'win32':
        suites.append(doctest.DocFileSuite('testrunner-coverage-win32.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE, checker=checker))
    if sys.version_info[:3] > (2, 4, 1) or not __debug__:
        try:
            import hotshot.stats
        except ImportError:
            pass
        else:
            suites.append(doctest.DocFileSuite('testrunner-profiling.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE, checker=renormalizing.RENormalizing([(re.compile('tests_profile[.]\\S*[.]prof'), 'tests_profile.*.prof')])))

    if hasattr(sys, 'gettotalrefcount'):
        suites.append(doctest.DocFileSuite('testrunner-leaks.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE, checker=renormalizing.RENormalizing([(re.compile('\\d+[.]\\d\\d\\d seconds'), 'N.NNN seconds'), (re.compile('sys refcount=\\d+ +change=\\d+'), 'sys refcount=NNNNNN change=NN'), (re.compile('sum detail refcount=\\d+ +'), 'sum detail refcount=NNNNNN '), (re.compile('total +\\d+ +\\d+'), 'total               NNNN    NNNN'), (re.compile('^ +(int|type) +-?\\d+ +-?\\d+ *\\n', re.M), '')])))
    else:
        suites.append(doctest.DocFileSuite('testrunner-leaks-err.txt', setUp=setUp, tearDown=tearDown, optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE, checker=checker))
    return unittest.TestSuite(suites)


def main():
    default = [
     '--path', os.path.split(sys.argv[0])[0], '--tests-pattern', '^testrunner$']
    run(default)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--resume-layer':
        sys.path.insert(0, os.path.split(os.path.split(os.path.split(os.path.abspath(sys.argv[0]))[0])[0])[0])
    import zope.testing.testrunner
    from zope.testing import doctest
    main()
from zope.testing import doctest