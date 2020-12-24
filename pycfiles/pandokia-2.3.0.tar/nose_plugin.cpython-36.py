# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/helpers/nose_plugin.py
# Compiled at: 2018-06-11 15:04:27
# Size of source mod 2**32: 14698 bytes
"""
This plugin provides a --pdk option to generate a log file for the
Pandokia test management system. Additional optional arguments determine
the logfile name, project name, and test run name.

Exception and stdout handling for inclusion in log file were copied
from the pinocchio output_save plugin by Titus Brown."""
import os, time, datetime, sys, re, nose.plugins.base, nose.case, unittest, traceback, platform, pandokia.helpers.pycode
p_StringO = None
c_StringO = None
try:
    from StringIO import StringIO as p_StringO
    from cStringIO import OutputType as c_StringO
except ImportError:
    from io import StringIO as p_StringO
    c_StringO = p_StringO

def get_stdout():
    if isinstance(sys.stdout, c_StringO) or isinstance(sys.stdout, p_StringO):
        return sys.stdout.getvalue()


def pdktimestamp(tt):
    """Formats the time in the format PDK wants.
    Input is a timestamp from time.time()"""
    x = datetime.datetime.fromtimestamp(tt)
    ans = '%s.%03d' % (x.strftime('%Y-%m-%d %H:%M:%S'),
     x.microsecond / 1000)
    return ans


def cleanname(name):
    """Removes any object id strings from the test name. These
    can occur in the case of a generated test."""
    pat = re.compile('.at.0x\\w*>')
    newname = re.sub(pat, '>', name)
    return newname


class Pdk(nose.plugins.base.Plugin):
    __doc__ = '\n    Provides --pdk option that causes each test to generate a PDK-\n    compatible log file.\n    '
    enabled = False
    pdkroot = None
    score = 500
    name = 'pdk'

    def options(self, parser, env=os.environ):
        parser.add_option('--pdk',
          action='store_true', dest='pdk_enabled', default=(env.get('PDK', False)),
          help='Generate PDK-compatible log file')
        parser.add_option('--pdklog',
          action='store', dest='pdklog', default=(env.get('PDK_LOG', None)),
          help='Path for PDK-compatible log file [PDK_LOG]')
        parser.add_option('--pdkproject',
          action='store', dest='pdkproject', default=(env.get('PDK_PROJECT', 'default')),
          help='Project name to write to PDK-compatible log file [PDK_PROJECT]')
        parser.add_option('--pdktestrun',
          action='store', dest='pdktestrun', default=(env.get('PDK_TESTRUN', time.asctime())),
          help='Test run name to write to PDK-compatible log file [PDK_TESTRUN]')
        parser.add_option('--pdktestprefix',
          action='store', dest='pdktestprefix', default=(env.get('PDK_TESTPREFIX', '')),
          help='Prefix to attach to test names in PDK-compatible log file [PDK_TESTPREFIX]')
        parser.add_option('--pdkcontext',
          action='store', dest='pdkcontext', default=(env.get('PDK_CONTEXT', 'default')),
          help='Context name to write to PDK-compatible log file [PDK_CONTEXT]')

    def configure(self, options, conf):
        self.conf = conf
        self.enabled = options.pdk_enabled
        if options.pdklog is not None:
            self.enabled = True
            self.pdklogfile = options.pdklog
        else:
            if 'PDK_LOG' in os.environ:
                self.enabled = True
                self.pdklogfile = os.environ['PDK_LOG']
            else:
                self.pdklogfile = os.path.join(os.path.abspath(os.path.curdir), 'PDK_DEFAULT.LOG')
        self.pdkproject = options.pdkproject.replace(' ', '-')
        self.pdktestrun = options.pdktestrun.replace(' ', '-')
        self.pdktestprefix = options.pdktestprefix
        self.pdkcontext = options.pdkcontext.replace(' ', '-')

    def begin(self):
        """Figure out the name of the logfile, open it, &
        initialize it for this test run."""
        self.rpt = None
        fname = self.pdklogfile
        hostname = platform.node()
        if '.' in hostname:
            hostname = hostname.split('.', 1)[0]
        if 'PDK_HOST' in list(os.environ.keys()):
            hostname = os.environ['PDK_HOST']
        try:
            if 'PDK_FILE' in os.environ:
                if 'PDK_DIRECTORY' in os.environ:
                    d = os.environ['PDK_DIRECTORY']
                else:
                    d = os.path.abspath(os.path.curdir)
                default_location = os.path.join(d, os.environ['PDK_FILE'])
            else:
                default_location = os.path.abspath(os.path.curdir)
            self.rpt = pandokia.helpers.pycode.reporter(source_file=None,
              setdefault=True,
              filename=(self.pdklogfile),
              test_run=(self.pdktestrun),
              project=(self.pdkproject),
              host=hostname,
              context=(self.pdkcontext),
              location=default_location,
              test_runner='nose',
              test_prefix='')
        except IOError as e:
            sys.stderr.write('Error opening log file %s: %s\n' % (
             fname, e.strerror))
            sys.stderr.write('***No Logging Performed***\n')
            return

    def startTest(self, test):
        self.pdk_starttime = time.time()

    def stopTest(self, test):
        pass

    def addError(self, test, err):
        self.write_report(test, 'E', err)

    def addFailure(self, test, err):
        self.write_report(test, 'F', err)

    def addSuccess(self, test):
        self.write_report(test, 'P')

    def write_report(self, test, status, err=None):
        from nose.inspector import inspect_traceback
        truncate_output_mark = '-------------------- >> begin captured stdout'
        truncate_output_len = len(truncate_output_mark)
        self.pdk_endtime = time.time()
        tbinfo = None
        exc = None
        exc_tra = None
        capture = get_stdout()
        if err is not None:
            ec, ev, tb = err
            str_ec = ec.__name__.lstrip()
            str_ev = str(ev)
            if not str_ev:
                str_ev = '(No message)'
            if tb:
                tbinfo = inspect_traceback(tb)
                str_rv = '\n'.join([tbinfo])
                str_tb = ''.join(traceback.format_tb(tb))
            str_ev_mark = str_ev.find(truncate_output_mark)
            if str_ev_mark >= 0:
                str_ev_truncated = str_ev[0:str_ev_mark]
            else:
                str_ev_truncated = str_ev
            exc_tra = '{}: {}'.format(str_ec, str_ev_truncated)
            exc = 'Type: {}\nMessage: {}\nTrigger: {}\n'.format(str_ec, str_ev_truncated, str_tb.splitlines()[(-1)].lstrip())
            final_tb = str_tb + '\n' + 'EXCEPTION\n' + exc
            if capture is None:
                capture = final_tb
            else:
                capture += final_tb
            if status == 'F':
                exc_tra = None
        self.pdklog((test.test), status, log=capture, exc=exc_tra)

    def find_txa(self, test):
        """Find the TDA and TRA dictionaries, which will be in different
        places depending on what kind of a test this is.
        """
        if isinstance(test, nose.case.MethodTestCase):
            try:
                tda = test.test.__self__.tda
            except AttributeError:
                tda = dict()

            try:
                tra = test.test.__self__.tra
            except AttributeError:
                tra = dict()

        elif isinstance(test, nose.case.FunctionTestCase):
            try:
                tda = test.test.__globals__['tda']
            except KeyError:
                tda = dict()

            try:
                tra = test.test.__globals__['tra']
            except KeyError:
                tra = dict()

        else:
            if isinstance(test, unittest.TestCase):
                try:
                    tda = test.tda
                except AttributeError:
                    tda = dict()

                try:
                    tra = test.tra
                except AttributeError:
                    tra = dict()

            else:
                tda = dict()
                tra = {'warning': 'Unknown test type: tda/tra not found'}
                raise TypeError('Unknown test type, %s' % type(test.test))
            return (
             tda, tra)

    def pdklog(self, test, status, log=None, exc=None):
        """Write a record of a single test result to the PDK log file.
        This includes everything that we know how to report about this particular
        test.  (Information common to all tests was written as a SETDEFAULT
        block when we opened the log file.)
        """
        name = None
        if name is None:
            try:
                name = cleanname(test.name)
            except AttributeError:
                try:
                    name = cleanname(test.test.name)
                except AttributeError:
                    name = cleanname(test.id().replace(' ', '_'))

            if self.pdktestprefix != '':
                name = self.pdktestprefix.endswith('/') or '%s/%s' % (self.pdktestprefix, name)
            else:
                name = '%s%s' % (self.pdktestprefix, name)
        tda, tra = self.find_txa(test)
        tda = isinstance(tda, dict) or {}
        tda['testtype'] = str(type(test))
        if hasattr(test, 'arg'):
            count = 0
            for k in test.arg:
                count += 1
                try:
                    tda['tda_arg%ds' % count] = str(k)
                except:
                    pass

        elif exc is not None:
            tra['exception'] = exc
        else:
            if name == 'nose.failure.Failure.runTest':
                pass
            else:
                if name.endswith('/nose.failure.Failure.runTest'):
                    pass
                elif self.rpt:
                    self.rpt.report(test_name=name,
                      status=status,
                      start_time=(pdktimestamp(self.pdk_starttime)),
                      end_time=(pdktimestamp(self.pdk_endtime)),
                      tda=tda,
                      tra=tra,
                      log=log)

    def finalize(self, result):
        if self.rpt:
            self.rpt.close()