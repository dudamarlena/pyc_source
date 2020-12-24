# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/runner.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 16852 bytes
""" basic collect and runtest protocol implementations """
import bdb, sys
from time import time
import py, pytest
from py._code.code import TerminalRepr

def pytest_namespace():
    return {'fail':fail, 
     'skip':skip, 
     'importorskip':importorskip, 
     'exit':exit}


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting', 'reporting', after='general')
    (
     group.addoption('--durations', action='store',
       type=int,
       default=None,
       metavar='N',
       help='show N slowest setup/test durations (N=0 for all).'),)


def pytest_terminal_summary(terminalreporter):
    durations = terminalreporter.config.option.durations
    if durations is None:
        return
    else:
        tr = terminalreporter
        dlist = []
        for replist in tr.stats.values():
            for rep in replist:
                if hasattr(rep, 'duration'):
                    dlist.append(rep)

        if not dlist:
            return
        dlist.sort(key=(lambda x: x.duration))
        dlist.reverse()
        if not durations:
            tr.write_sep('=', 'slowest test durations')
        else:
            tr.write_sep('=', 'slowest %s test durations' % durations)
        dlist = dlist[:durations]
    for rep in dlist:
        nodeid = rep.nodeid.replace('::()::', '::')
        tr.write_line('%02.2fs %-8s %s' % (
         rep.duration, rep.when, nodeid))


def pytest_sessionstart(session):
    session._setupstate = SetupState()


def pytest_sessionfinish(session):
    session._setupstate.teardown_all()


class NodeInfo:

    def __init__(self, location):
        self.location = location


def pytest_runtest_protocol(item, nextitem):
    item.ihook.pytest_runtest_logstart(nodeid=(item.nodeid),
      location=(item.location))
    runtestprotocol(item, nextitem=nextitem)
    return True


def runtestprotocol(item, log=True, nextitem=None):
    hasrequest = hasattr(item, '_request')
    if hasrequest:
        if not item._request:
            item._initrequest()
    rep = call_and_report(item, 'setup', log)
    reports = [rep]
    if rep.passed:
        reports.append(call_and_report(item, 'call', log))
    reports.append(call_and_report(item, 'teardown', log, nextitem=nextitem))
    if hasrequest:
        item._request = False
        item.funcargs = None
    return reports


def pytest_runtest_setup(item):
    item.session._setupstate.prepare(item)


def pytest_runtest_call(item):
    try:
        item.runtest()
    except Exception:
        type, value, tb = sys.exc_info()
        tb = tb.tb_next
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        del tb
        raise


def pytest_runtest_teardown(item, nextitem):
    item.session._setupstate.teardown_exact(item, nextitem)


def pytest_report_teststatus(report):
    if report.when in ('setup', 'teardown'):
        if report.failed:
            return ('error', 'E', 'ERROR')
        else:
            if report.skipped:
                return ('skipped', 's', 'SKIPPED')
            return ('', '', '')


def call_and_report(item, when, log=True, **kwds):
    call = call_runtest_hook(item, when, **kwds)
    hook = item.ihook
    report = hook.pytest_runtest_makereport(item=item, call=call)
    if log:
        hook.pytest_runtest_logreport(report=report)
    if check_interactive_exception(call, report):
        hook.pytest_exception_interact(node=item, call=call, report=report)
    return report


def check_interactive_exception(call, report):
    return call.excinfo and not (hasattr(report, 'wasxfail') or call.excinfo.errisinstance(skip.Exception) or call.excinfo.errisinstance(bdb.BdbQuit))


def call_runtest_hook(item, when, **kwds):
    hookname = 'pytest_runtest_' + when
    ihook = getattr(item.ihook, hookname)
    return CallInfo((lambda : ihook(item=item, **kwds)), when=when)


class CallInfo:
    __doc__ = ' Result/Exception info a function invocation. '
    excinfo = None

    def __init__(self, func, when):
        self.when = when
        self.start = time()
        try:
            self.result = func()
        except KeyboardInterrupt:
            self.stop = time()
            raise
        except:
            self.excinfo = py.code.ExceptionInfo()

        self.stop = time()

    def __repr__(self):
        if self.excinfo:
            status = 'exception: %s' % str(self.excinfo.value)
        else:
            status = 'result: %r' % (self.result,)
        return '<CallInfo when=%r %s>' % (self.when, status)


def getslaveinfoline(node):
    try:
        return node._slaveinfocache
    except AttributeError:
        d = node.slaveinfo
        ver = '%s.%s.%s' % d['version_info'][:3]
        node._slaveinfocache = s = '[%s] %s -- Python %s %s' % (
         d['id'], d['sysplatform'], ver, d['executable'])
        return s


class BaseReport(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def toterminal(self, out):
        longrepr = self.longrepr
        if hasattr(self, 'node'):
            out.line(getslaveinfoline(self.node))
        else:
            if hasattr(longrepr, 'toterminal'):
                longrepr.toterminal(out)
            else:
                try:
                    out.line(longrepr)
                except UnicodeEncodeError:
                    out.line('<unprintable longrepr>')

    def get_sections(self, prefix):
        for name, content in self.sections:
            if name.startswith(prefix):
                yield (
                 prefix, content)

    passed = property(lambda x: x.outcome == 'passed')
    failed = property(lambda x: x.outcome == 'failed')
    skipped = property(lambda x: x.outcome == 'skipped')

    @property
    def fspath(self):
        return self.nodeid.split('::')[0]


def pytest_runtest_makereport(item, call):
    when = call.when
    duration = call.stop - call.start
    keywords = dict([(x, 1) for x in item.keywords])
    excinfo = call.excinfo
    sections = []
    if not call.excinfo:
        outcome = 'passed'
        longrepr = None
    else:
        if not isinstance(excinfo, py.code.ExceptionInfo):
            outcome = 'failed'
            longrepr = excinfo
        else:
            if excinfo.errisinstance(pytest.skip.Exception):
                outcome = 'skipped'
                r = excinfo._getreprcrash()
                longrepr = (str(r.path), r.lineno, r.message)
            else:
                outcome = 'failed'
                if call.when == 'call':
                    longrepr = item.repr_failure(excinfo)
                else:
                    longrepr = item._repr_failure_py(excinfo, style=(item.config.option.tbstyle))
    for rwhen, key, content in item._report_sections:
        sections.append(('Captured std%s %s' % (key, rwhen), content))

    return TestReport(item.nodeid, item.location, keywords, outcome, longrepr, when, sections, duration)


class TestReport(BaseReport):
    __doc__ = ' Basic test report object (also used for setup and teardown calls if\n    they fail).\n    '

    def __init__(self, nodeid, location, keywords, outcome, longrepr, when, sections=(), duration=0, **extra):
        self.nodeid = nodeid
        self.location = location
        self.keywords = keywords
        self.outcome = outcome
        self.longrepr = longrepr
        self.when = when
        self.sections = list(sections)
        self.duration = duration
        self.__dict__.update(extra)

    def __repr__(self):
        return '<TestReport %r when=%r outcome=%r>' % (
         self.nodeid, self.when, self.outcome)


class TeardownErrorReport(BaseReport):
    outcome = 'failed'
    when = 'teardown'

    def __init__(self, longrepr, **extra):
        self.longrepr = longrepr
        self.sections = []
        self.__dict__.update(extra)


def pytest_make_collect_report(collector):
    call = CallInfo(collector._memocollect, 'memocollect')
    longrepr = None
    if not call.excinfo:
        outcome = 'passed'
    else:
        from _pytest import nose
        skip_exceptions = (
         Skipped,) + nose.get_skip_exceptions()
    if call.excinfo.errisinstance(skip_exceptions):
        outcome = 'skipped'
        r = collector._repr_failure_py(call.excinfo, 'line').reprcrash
        longrepr = (str(r.path), r.lineno, r.message)
    else:
        outcome = 'failed'
        errorinfo = collector.repr_failure(call.excinfo)
        if not hasattr(errorinfo, 'toterminal'):
            errorinfo = CollectErrorRepr(errorinfo)
        longrepr = errorinfo
    rep = CollectReport(collector.nodeid, outcome, longrepr, getattr(call, 'result', None))
    rep.call = call
    return rep


class CollectReport(BaseReport):

    def __init__(self, nodeid, outcome, longrepr, result, sections=(), **extra):
        self.nodeid = nodeid
        self.outcome = outcome
        self.longrepr = longrepr
        self.result = result or []
        self.sections = list(sections)
        self.__dict__.update(extra)

    @property
    def location(self):
        return (self.fspath, None, self.fspath)

    def __repr__(self):
        return '<CollectReport %r lenresult=%s outcome=%r>' % (
         self.nodeid, len(self.result), self.outcome)


class CollectErrorRepr(TerminalRepr):

    def __init__(self, msg):
        self.longrepr = msg

    def toterminal(self, out):
        out.line((self.longrepr), red=True)


class SetupState(object):
    __doc__ = ' shared state for setting up/tearing down test items or collectors. '

    def __init__(self):
        self.stack = []
        self._finalizers = {}

    def addfinalizer(self, finalizer, colitem):
        """ attach a finalizer to the given colitem.
        if colitem is None, this will add a finalizer that
        is called at the end of teardown_all().
        """
        if not (colitem and not isinstance(colitem, tuple)):
            raise AssertionError
        elif not py.builtin.callable(finalizer):
            raise AssertionError
        self._finalizers.setdefault(colitem, []).append(finalizer)

    def _pop_and_teardown(self):
        colitem = self.stack.pop()
        self._teardown_with_finalization(colitem)

    def _callfinalizers(self, colitem):
        finalizers = self._finalizers.pop(colitem, None)
        exc = None
        while finalizers:
            fin = finalizers.pop()
            try:
                fin()
            except Exception:
                if exc is None:
                    exc = sys.exc_info()

        if exc:
            (py.builtin._reraise)(*exc)

    def _teardown_with_finalization(self, colitem):
        self._callfinalizers(colitem)
        if hasattr(colitem, 'teardown'):
            colitem.teardown()
        for colitem in self._finalizers:
            if not colitem is None:
                if not colitem in self.stack:
                    assert isinstance(colitem, tuple)

    def teardown_all(self):
        while self.stack:
            self._pop_and_teardown()

        for key in list(self._finalizers):
            self._teardown_with_finalization(key)

        assert not self._finalizers

    def teardown_exact(self, item, nextitem):
        needed_collectors = nextitem and nextitem.listchain() or []
        self._teardown_towards(needed_collectors)

    def _teardown_towards(self, needed_collectors):
        while self.stack:
            if self.stack == needed_collectors[:len(self.stack)]:
                break
            self._pop_and_teardown()

    def prepare(self, colitem):
        """ setup objects along the collector chain to the test-method
            and teardown previously setup objects."""
        needed_collectors = colitem.listchain()
        self._teardown_towards(needed_collectors)
        for col in self.stack:
            if hasattr(col, '_prepare_exc'):
                (py.builtin._reraise)(*col._prepare_exc)

        for col in needed_collectors[len(self.stack):]:
            self.stack.append(col)
            try:
                col.setup()
            except Exception:
                col._prepare_exc = sys.exc_info()
                raise


def collect_one_node(collector):
    ihook = collector.ihook
    ihook.pytest_collectstart(collector=collector)
    rep = ihook.pytest_make_collect_report(collector=collector)
    call = rep.__dict__.pop('call', None)
    if call:
        if check_interactive_exception(call, rep):
            ihook.pytest_exception_interact(node=collector, call=call, report=rep)
    return rep


class OutcomeException(Exception):
    __doc__ = ' OutcomeException and its subclass instances indicate and\n        contain info about test and collection outcomes.\n    '

    def __init__(self, msg=None, pytrace=True):
        Exception.__init__(self, msg)
        self.msg = msg
        self.pytrace = pytrace

    def __repr__(self):
        if self.msg:
            return str(self.msg)
        else:
            return '<%s instance>' % (self.__class__.__name__,)

    __str__ = __repr__


class Skipped(OutcomeException):
    __module__ = 'builtins'


class Failed(OutcomeException):
    __doc__ = ' raised from an explicit call to pytest.fail() '
    __module__ = 'builtins'


class Exit(KeyboardInterrupt):
    __doc__ = ' raised for immediate program exits (no tracebacks/summaries)'

    def __init__(self, msg='unknown reason'):
        self.msg = msg
        KeyboardInterrupt.__init__(self, msg)


def exit(msg):
    """ exit testing process as if KeyboardInterrupt was triggered. """
    __tracebackhide__ = True
    raise Exit(msg)


exit.Exception = Exit

def skip(msg=''):
    """ skip an executing test with the given message.  Note: it's usually
    better to use the pytest.mark.skipif marker to declare a test to be
    skipped under certain conditions like mismatching platforms or
    dependencies.  See the pytest_skipping plugin for details.
    """
    __tracebackhide__ = True
    raise Skipped(msg=msg)


skip.Exception = Skipped

def fail(msg='', pytrace=True):
    """ explicitely fail an currently-executing test with the given Message.

    :arg pytrace: if false the msg represents the full failure information
                  and no python traceback will be reported.
    """
    __tracebackhide__ = True
    raise Failed(msg=msg, pytrace=pytrace)


fail.Exception = Failed

def importorskip(modname, minversion=None):
    """ return imported module if it has at least "minversion" as its
    __version__ attribute.  If no minversion is specified the a skip
    is only triggered if the module can not be imported.
    Note that version comparison only works with simple version strings
    like "1.2.3" but not "1.2.3.dev1" or others.
    """
    __tracebackhide__ = True
    compile(modname, '', 'eval')
    try:
        __import__(modname)
    except ImportError:
        skip('could not import %r' % (modname,))

    mod = sys.modules[modname]
    if minversion is None:
        return mod
    else:
        verattr = getattr(mod, '__version__', None)

        def intver(verstring):
            return [int(x) for x in verstring.split('.')]

        if verattr is None or intver(verattr) < intver(minversion):
            skip('module %r has __version__ %r, required is: %r' % (
             modname, verattr, minversion))
        return mod