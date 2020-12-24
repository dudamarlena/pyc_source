# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/junitxml.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 8189 bytes
""" report test results in JUnit-XML format, for use with Hudson and build integration servers.

Based on initial code from Ross Lawley.
"""
import py, os, re, sys, time
if sys.version_info[0] < 3:
    from codecs import open
else:
    unichr = chr
    unicode = str
    long = int

class Junit(py.xml.Namespace):
    pass


_legal_chars = (9, 10, 13)
_legal_ranges = ((32, 126), (128, 55295), (57344, 65533), (65536, 1114111))
_legal_xml_re = [unicode('%s-%s') % (unichr(low), unichr(high)) for low, high in _legal_ranges if low < sys.maxunicode]
_legal_xml_re = [unichr(x) for x in _legal_chars] + _legal_xml_re
illegal_xml_re = re.compile(unicode('[^%s]') % unicode('').join(_legal_xml_re))
del _legal_chars
del _legal_ranges
del _legal_xml_re

def bin_xml_escape(arg):

    def repl(matchobj):
        i = ord(matchobj.group())
        if i <= 255:
            return unicode('#x%02X') % i
        else:
            return unicode('#x%04X') % i

    return py.xml.raw(illegal_xml_re.sub(repl, py.xml.escape(arg)))


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption('--junitxml', '--junit-xml', action='store', dest='xmlpath',
      metavar='path',
      default=None,
      help='create junit-xml style report file at given path.')
    group.addoption('--junitprefix', '--junit-prefix', action='store', metavar='str',
      default=None,
      help='prepend prefix to classnames in junit-xml output')


def pytest_configure(config):
    xmlpath = config.option.xmlpath
    if xmlpath:
        if not hasattr(config, 'slaveinput'):
            config._xml = LogXML(xmlpath, config.option.junitprefix)
            config.pluginmanager.register(config._xml)


def pytest_unconfigure(config):
    xml = getattr(config, '_xml', None)
    if xml:
        del config._xml
        config.pluginmanager.unregister(xml)


def mangle_testnames(names):
    names = [x.replace('.py', '') for x in names if x != '()']
    names[0] = names[0].replace('/', '.')
    return names


class LogXML(object):

    def __init__(self, logfile, prefix):
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.normpath(os.path.abspath(logfile))
        self.prefix = prefix
        self.tests = []
        self.passed = self.skipped = 0
        self.failed = self.errors = 0

    def _opentestcase(self, report):
        names = mangle_testnames(report.nodeid.split('::'))
        classnames = names[:-1]
        if self.prefix:
            classnames.insert(0, self.prefix)
        self.tests.append(Junit.testcase(classname=('.'.join(classnames)),
          name=(bin_xml_escape(names[(-1)])),
          time=(getattr(report, 'duration', 0))))

    def _write_captured_output(self, report):
        for capname in ('out', 'err'):
            allcontent = ''
            for name, content in report.get_sections('Captured std%s' % capname):
                allcontent += content

            if allcontent:
                tag = getattr(Junit, 'system-' + capname)
                self.append(tag(bin_xml_escape(allcontent)))

    def append(self, obj):
        self.tests[(-1)].append(obj)

    def append_pass(self, report):
        self.passed += 1
        self._write_captured_output(report)

    def append_failure(self, report):
        if hasattr(report, 'wasxfail'):
            self.append(Junit.skipped(message='xfail-marked test passes unexpectedly'))
            self.skipped += 1
        else:
            if hasattr(report.longrepr, 'reprcrash'):
                message = report.longrepr.reprcrash.message
            else:
                if isinstance(report.longrepr, (unicode, str)):
                    message = report.longrepr
                else:
                    message = str(report.longrepr)
                message = bin_xml_escape(message)
                fail = Junit.failure(message=message)
                fail.append(bin_xml_escape(report.longrepr))
                self.append(fail)
                self.failed += 1
        self._write_captured_output(report)

    def append_collect_error(self, report):
        self.append(Junit.error((bin_xml_escape(report.longrepr)), message='collection failure'))
        self.errors += 1

    def append_collect_skipped(self, report):
        self.append(Junit.skipped((bin_xml_escape(report.longrepr)), message='collection skipped'))
        self.skipped += 1

    def append_error(self, report):
        self.append(Junit.error((bin_xml_escape(report.longrepr)), message='test setup failure'))
        self.errors += 1

    def append_skipped(self, report):
        if hasattr(report, 'wasxfail'):
            self.append(Junit.skipped((bin_xml_escape(report.wasxfail)), message='expected test failure'))
        else:
            filename, lineno, skipreason = report.longrepr
            if skipreason.startswith('Skipped: '):
                skipreason = bin_xml_escape(skipreason[9:])
            self.append(Junit.skipped(('%s:%s: %s' % (filename, lineno, skipreason)), type='pytest.skip',
              message=skipreason))
        self.skipped += 1
        self._write_captured_output(report)

    def pytest_runtest_logreport(self, report):
        if report.passed:
            if report.when == 'call':
                self._opentestcase(report)
                self.append_pass(report)
        else:
            if report.failed:
                self._opentestcase(report)
                if report.when != 'call':
                    self.append_error(report)
                else:
                    self.append_failure(report)
            elif report.skipped:
                self._opentestcase(report)
                self.append_skipped(report)

    def pytest_collectreport(self, report):
        if not report.passed:
            self._opentestcase(report)
            if report.failed:
                self.append_collect_error(report)
            else:
                self.append_collect_skipped(report)

    def pytest_internalerror(self, excrepr):
        self.errors += 1
        data = bin_xml_escape(excrepr)
        self.tests.append(Junit.testcase(Junit.error(data, message='internal error'),
          classname='pytest',
          name='internal'))

    def pytest_sessionstart(self):
        self.suite_start_time = time.time()

    def pytest_sessionfinish(self):
        dirname = os.path.dirname(os.path.abspath(self.logfile))
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        logfile = open((self.logfile), 'w', encoding='utf-8')
        suite_stop_time = time.time()
        suite_time_delta = suite_stop_time - self.suite_start_time
        numtests = self.passed + self.failed
        logfile.write('<?xml version="1.0" encoding="utf-8"?>')
        logfile.write(Junit.testsuite((self.tests),
          name='pytest',
          errors=(self.errors),
          failures=(self.failed),
          skips=(self.skipped),
          tests=numtests,
          time=('%.3f' % suite_time_delta)).unicode(indent=0))
        logfile.close()

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep('-', 'generated xml file: %s' % self.logfile)