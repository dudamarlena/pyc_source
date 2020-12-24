# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/helpers/pycode.py
# Compiled at: 2018-06-04 12:38:26
# Size of source mod 2**32: 20222 bytes
import os, pandokia.lib, datetime, traceback

class reporter(object):
    report_view = False
    report_view_sep = '-' * 79
    report_view_verbose = False

    def __init__(self, source_file, setdefault=False, filename=None, test_run=None, project=None, host=None, context=None, location=None, test_runner=None, test_prefix=None):
        """pandokia log file object

        source_file
            The base name of the source file is added to the test prefix.
            May be None if you don't want that.

        setdefault = False
            If true, write a SETDEFAULT block; if pdkrun called you,
            you don't need this.  The default values come from the
            environment or gethostname().

        filename = None
            Name of the file to write the records to; if None, use
            PDK_LOG environment variable.

        test_run = None
        project = None
        host = None
        context = None
            Characteristics of this test run; if None, use related
            pandokia environment variable; if no environment variable,
            use "default"

        location = None
            Characteristics of this test run; if None, figure out
            the location of the tests from the current directory
            and PDK_FILE.  If you can't, don't report a location.

        test_runner = None
            if not None, report this string as the test runner used.

        test_prefix = None
            put this prefix on each test name; if None, use PDK_TESTPREFIX
            environment.  If not in environment, there is no prefix.

"""
        if filename is not None:
            self.filename = filename
            self.report_file = open(filename, 'a')
        else:
            if 'PDK_LOG' in os.environ:
                filename = os.environ['PDK_LOG']
                self.filename = filename
                self.report_file = open(filename, 'a')
            else:
                self.report_file = sys.stdout
                self.report_view = True
            if test_prefix is None:
                if 'PDK_TESTPREFIX' in os.environ:
                    self.test_prefix = os.environ['PDK_TESTPREFIX']
                else:
                    self.test_prefix = ''
            else:
                self.test_prefix = test_prefix
        if source_file is not None:
            if source_file.endswith('.py'):
                source_file = source_file[:-3]
            else:
                if source_file.endswith('.pyc') or source_file.endswith('.pyo'):
                    source_file = source_file[:-4]
            self.test_prefix = self.test_prefix + source_file
        if setdefault and not self.report_view:
            self.report_file.write('\n\nSTART\n')
            if test_run is None:
                if 'PDK_TESTRUN' in os.environ:
                    test_run = os.environ['PDK_TESTRUN']
                else:
                    test_run = 'default'
            self.write_field('test_run', test_run)
            if project is None:
                if 'PDK_PROJECT' in os.environ:
                    project = os.environ['PDK_PROJECT']
                else:
                    project = 'default'
            self.write_field('project', project)
            if host is None:
                if 'PDK_HOST' in list(os.environ.keys()):
                    host = os.environ['PDK_HOST']
                else:
                    host = pandokia.lib.gethostname()
            self.write_field('host', host)
            if location is None:
                if 'PDK_FILE' in os.environ:
                    location = os.getcwd() + '/' + os.environ['PDK_FILE']
                    self.write_field('location', location)
            else:
                self.write_field('location', location)
            if test_runner is not None:
                self.write_field('test_runner', test_runner)
            if context is None:
                if 'PDK_CONTEXT' in os.environ:
                    context = os.environ['PDK_CONTEXT']
            if context is not None:
                self.write_field('context', context)
            self.report_file.write('SETDEFAULT\n')
        self.status_count = {}

    def report(self, test_name, status, start_time=None, end_time=None, tra={}, tda={}, log=None, location=None):
        self.status_count[status] = self.status_count.get(status, 0) + 1
        if self.report_view:
            if status == 'P':
                if not self.report_view_verbose:
                    return
                self.report_file.write(self.report_view_sep)
                self.report_file.write('\n')
            else:
                if test_name is None:
                    test_name = self.test_prefix
                else:
                    if self.test_prefix != '':
                        if self.test_prefix.endswith('.') or self.test_prefix.endswith('/'):
                            test_name = self.test_prefix + test_name
                        else:
                            test_name = self.test_prefix + '.' + test_name
        else:
            if '\n' in test_name:
                test_name = test_name.replace('\n', '-')
            self.write_field('test_name', test_name)
            self.write_field('status', status)
            if not self.report_view:
                if location is not None:
                    self.write_field('location', str(location))
                else:
                    if start_time is not None:
                        self.write_field('start_time', str(start_time))
                    if end_time is not None:
                        self.write_field('end_time', str(end_time))
                    for name in tda:
                        self.write_field('tda_' + name, tda[name])

                    for name in tra:
                        self.write_field('tra_' + name, tra[name])

                    if log is not None:
                        self.write_field('log', log)
                self.report_file.write('END\n')
            else:
                self.report_file.write(log)
        self.report_file.flush()

    def start(self, test_name, tda={}):
        self.test_name = test_name
        self.tda = tda
        self.start_time = datetime.datetime.now()

    def finish(self, status, tra={}, log=None):
        self.report(test_name=(self.test_name),
          status=status,
          start_time=(self.start_time),
          end_time=(datetime.datetime.now()),
          tda=(self.tda),
          tra=tra,
          log=log)

    def write_field(self, name, value):
        value = str(value)
        if '\n' in value:
            if value.endswith('\n'):
                value = value[:-1]
            self.report_file.write('%s:\n' % name)
            for x in value.split('\n'):
                self.report_file.write('.%s\n' % x)

            self.report_file.write('\n')
        else:
            self.report_file.write('%s=%s\n' % (name, value))

    def close(self):
        self.report_file.close()
        self.report_file = None


try:
    import StringIO
except ImportError:
    import io as StringIO

import sys
save_stdout = []
save_stderr = []
save_tagname = []

def snarf_stdout(tagname=None):
    global save_stderr
    global save_stdout
    save_stdout.append(sys.stdout)
    save_stderr.append(sys.stderr)
    save_tagname.append(tagname)
    sys.stdout = sys.stderr = StringIO.StringIO()


def end_snarf_stdout(tagname=None):
    s = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = save_stdout.pop()
    sys.stderr = save_stderr.pop()
    old_tagname = save_tagname.pop()
    if old_tagname != tagname:
        f = open('/dev/tty', 'w')
        f.write('Mismatched snarf_stdout/end_snarf_stdout - expected %s got %s' % (
         tagname, old_tagname))
        f.close()
        raise ValueError('Mismatched snarf_stdout/end_snarf_stdout')
    return s


def peek_snarfed_stdout():
    """returns current text of snarfed stdout, non-destructively"""
    if isinstance(sys.stdout, StringIO.StringIO):
        return sys.stdout.getvalue()
    else:
        return


cached_rpt = None
with_counter = 0
with_counter_stack = []
with_seq = 0

class _pycode_with(object):
    __doc__ = '\n    with test( name, rpt, tda= {}, tra = {} ) as t :\n        t.tra[\'name\'] = some_value\n        t.tda[\'name\'] = some_value\n        print "stuff"\n        assert some_expression\n        raise some_error()\n\n    name is the name of the test.\n\n    rpt is the pycode object to report to\n\n    tda and tra are optional initial values of the tda/tra\n    dicts.  A COPY of each will be attached to the context\n    manager object.\n\n\n    '

    def __init__(self, *l, **kw):
        raise Exception('Do not instantiate me directly.  Use pycode.test or pycode.setup')

    def fmt(self, name, rpt, tda, tra, location):
        global cached_rpt
        global runner_minipyt
        global with_counter
        try:
            runner_minipyt
        except NameError:
            from . import runner_minipyt as m
            runner_minipyt = m

        if with_seq:
            self.name = '%0*d-%s' % (with_seq, with_counter, name)
        else:
            self.name = name
        if rpt is None:
            if not cached_rpt:
                cached_rpt = reporter(None)
            self.rpt = cached_rpt
        else:
            self.rpt = rpt
        self.tda = tda.copy()
        self.tra = tra.copy()
        self.expired = False
        self.location = location
        if location is None:
            import inspect
            l = inspect.stack()
            this_file = l[0][1]
            for x in l:
                if x[1] != this_file or x[3] == 'package_test':
                    self.location = x[1]
                    break

            if '__init__' in self.location:
                open('/dev/tty', 'w').write(str(l))

    def __enter__(self):
        global with_counter
        if self.expired:
            raise Exception('Object not reusable')
        self.expired = True
        with_counter_stack.append(with_counter + 1)
        with_counter = 0
        runner_minipyt.currently_running_test_name.append(self.name)
        self.full_name = '.'.join([x for x in runner_minipyt.currently_running_test_name if x])
        self.start_time = datetime.datetime.now()
        snarf_stdout()
        return self

    def __exit__(self, extype, exvalue, extraceback):
        global with_counter
        if runner_minipyt.currently_running_test_name.pop() != self.name:
            raise Exception('Internal inconsistency in pycode context manager - name stack is messed up')
        else:
            with_counter = with_counter_stack.pop()
            if extype is None:
                status = self.pass_status
            else:
                if isinstance(exvalue, AssertionError):
                    status = 'F'
                else:
                    status = 'E'
            if 'exception' not in self.tra:
                self.tra['exception'] = str(exvalue)
                self.tra['exception_type'] = str(extype)
            if status != 'P':
                print(str(exvalue))
                traceback.print_tb(extraceback)
            log = end_snarf_stdout()
            if runner_minipyt.dots_mode:
                runner_minipyt.show_dot(status, self.full_name, log)
        self.rpt.report(test_name=(self.full_name), status=status,
          start_time=(self.start_time),
          end_time=(datetime.datetime.now()),
          tra=(self.tra),
          tda=(self.tda),
          log=log,
          location=(self.location))
        return True


class test(_pycode_with):
    pass_status = 'P'

    def __init__(self, name, rpt=None, tda={}, tra={}, location=None):
        self.fmt(name, rpt, tda, tra, location)


class setup(_pycode_with):
    pass_status = 'P'

    def __init__(self, name, rpt=None, tda={}, tra={}, location=None):
        self.fmt(name, rpt, tda, tra, location)


def package_test(parent, test_package, test_modules, verbose=False, silent=False):
    global cached_rpt
    if silent:
        verbose = False
    else:
        import pandokia.helpers.runner_minipyt as runner_minipyt
        runner_minipyt.dots_mode = ''
        cached_rpt = reporter(None)
        cached_rpt.report_view_verbose = verbose
        for x in test_modules:
            x = parent + '.' + test_package + '.' + x
            with test(x) as (t):
                exec('import %s' % x)

        passed = cached_rpt.status_count.get('P', 0)
        failed = cached_rpt.status_count.get('F', 0)
        error = cached_rpt.status_count.get('E', 0)
        if not silent:
            print(cached_rpt.report_view_sep)
            print('Pass: %d  Fail: %d  Error: %d' % (passed, failed, error))
        if failed == 0:
            if error == 0:
                return 0
    return 1