# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/nose_html/__init__.py
# Compiled at: 2013-08-14 08:52:24
"""
A nose plugin which generates a HTML report to show the result at a glance.

------------------------------------------------------------------------
Copyright (c) 2004-2006, Wai Yip Tung
Copyright (c) 2009-2012, The SIO2 Project Team
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
__author__ = 'Wai Yip Tung'
__version__ = '0.8.1'
import datetime, StringIO, os.path, sys, time, logging, traceback, operator
from xml.sax import saxutils
from nose.plugins.base import Plugin
import codecs

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """
    STATUS = {0: 'pass', 
       1: 'fail', 
       2: 'error'}
    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''
    HTML_TMPL = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n    <title>%(title)s</title>\n    <meta name="generator" content="%(generator)s"/>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>\n    %(stylesheet)s\n</head>\n<body>\n<script language="javascript" type="text/javascript"><!--\noutput_list = Array();\n\n/* level - 0:Summary; 1:Failed; 2:All */\nfunction showCase(level) {\n    trs = document.getElementsByTagName("tr");\n    for (var i = 0; i < trs.length; i++) {\n        tr = trs[i];\n        id = tr.id;\n        if (id.substr(0,2) == \'ft\') {\n            if (level < 1) {\n                tr.className = \'hiddenRow\';\n            }\n            else {\n                tr.className = \'\';\n            }\n        }\n        if (id.substr(0,2) == \'pt\') {\n            if (level > 1) {\n                tr.className = \'\';\n            }\n            else {\n                tr.className = \'hiddenRow\';\n            }\n        }\n    }\n}\n\nfunction showClassDetail(cid, count) {\n    var id_list = Array(count);\n    var toHide = 1;\n    for (var i = 0; i < count; i++) {\n        tid0 = \'t\' + cid.substr(1) + \'.\' + (i+1);\n        tid = \'f\' + tid0;\n        tr = document.getElementById(tid);\n        if (!tr) {\n            tid = \'p\' + tid0;\n            tr = document.getElementById(tid);\n        }\n        id_list[i] = tid;\n        if (tr.className) {\n            toHide = 0;\n        }\n    }\n    for (var i = 0; i < count; i++) {\n        tid = id_list[i];\n        if (toHide) {\n            document.getElementById(tid).className = \'hiddenRow\';\n        }\n        else {\n            document.getElementById(tid).className = \'\';\n        }\n    }\n}\n\nfunction html_escape(s) {\n    s = s.replace(/&/g,\'&amp;\');\n    s = s.replace(/</g,\'&lt;\');\n    s = s.replace(/>/g,\'&gt;\');\n    return s;\n}\n\nfunction showOutput(id, name) {\n    var w = window.open("", //url\n                    name,\n                    "resizable,scrollbars,status,width=800,height=450");\n    d = w.document;\n    d.write("<pre>");\n    d.write(html_escape(output_list[id]));\n    d.write("\\n");\n    d.write("<a href=\'javascript:window.close()\'>close</a>\\n");\n    d.write("</pre>\\n");\n    d.close();\n}\n--></script>\n\n%(heading)s\n%(report)s\n%(ending)s\n\n</body>\n</html>\n'
    STYLESHEET_TMPL = '\n<style type="text/css" media="screen">\nbody        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }\ntable       { font-size: 100%; }\npre         { }\n\n/* -- heading ---------------------------------------------------------------------- */\nh1 {\n}\n.heading {\n    margin-top: 0ex;\n    margin-bottom: 1ex;\n}\n\n.heading .attribute {\n    margin-top: 1ex;\n    margin-bottom: 0;\n}\n\n.heading .description {\n    margin-top: 4ex;\n    margin-bottom: 6ex;\n}\n\n/* -- report ------------------------------------------------------------------------ */\n#show_detail_line {\n    margin-top: 3ex;\n    margin-bottom: 1ex;\n}\n#result_table {\n    width: 80%;\n    border-collapse: collapse;\n    border: medium solid #777;\n}\n#header_row {\n    font-weight: bold;\n    color: white;\n    background-color: #777;\n}\n#result_table td {\n    border: thin solid #777;\n    padding: 2px;\n}\n#total_row  { font-weight: bold; }\n.passClass  { background-color: #6c6; }\n.failClass  { background-color: #c60; }\n.errorClass { background-color: #c00; }\n.passCase   { color: #6c6; }\n.failCase   { color: #c60; font-weight: bold; }\n.errorCase  { color: #c00; font-weight: bold; }\n.hiddenRow  { display: none; }\n.testcase   { margin-left: 2em; }\n\n\n/* -- ending ---------------------------------------------------------------------- */\n#ending {\n}\n\n</style>\n'
    HEADING_TMPL = "<div class='heading'>\n<h1>%(title)s</h1>\n%(parameters)s\n<p class='description'>%(description)s</p>\n</div>\n\n"
    HEADING_ATTRIBUTE_TMPL = "<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>\n"
    REPORT_TMPL = "\n<p id='show_detail_line'>Show\n<a href='javascript:showCase(0)'>Summary</a>\n<a href='javascript:showCase(1)'>Failed</a>\n<a href='javascript:showCase(2)'>All</a>\n</p>\n<table id='result_table'>\n<colgroup>\n<col align='left' />\n<col align='right' />\n<col align='right' />\n<col align='right' />\n<col align='right' />\n<col align='right' />\n<col align='right' />\n</colgroup>\n<tr id='header_row'>\n    <td>Test Group/Test case</td>\n    <td>Time</td>\n    <td>Count</td>\n    <td>Pass</td>\n    <td>Fail</td>\n    <td>Error</td>\n    <td>View</td>\n</tr>\n%(test_list)s\n<tr id='total_row'>\n    <td>Total</td>\n    <td>%(time)s</td>\n    <td>%(count)s</td>\n    <td>%(Pass)s</td>\n    <td>%(fail)s</td>\n    <td>%(error)s</td>\n    <td>&nbsp;</td>\n</tr>\n</table>\n"
    REPORT_CLASS_TMPL = '\n<tr class=\'%(style)s\'>\n    <td>%(desc)s</td>\n    <td>%(time)s</td>\n    <td>%(count)s</td>\n    <td>%(Pass)s</td>\n    <td>%(fail)s</td>\n    <td>%(error)s</td>\n    <td><a href="javascript:showClassDetail(\'%(cid)s\',%(count)s)">Detail</a></td>\n</tr>\n'
    REPORT_TEST_WITH_OUTPUT_TMPL = '\n<tr id=\'%(tid)s\' class=\'%(Class)s\'>\n    <td class=\'%(style)s\'><div class=\'testcase\'>%(desc)s</div></td>\n    <td>%(time)s</td>\n    <td colspan=\'5\' align=\'center\'><a href="javascript:showOutput(\'%(tid)s\', \'%(desc)s\')">%(status)s</a>%(script)s</td>\n</tr>\n'
    REPORT_TEST_NO_OUTPUT_TMPL = "\n<tr id='%(tid)s' class='%(Class)s'>\n    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>\n    <td>%(time)s</td>\n    <td colspan='5' align='center'>%(status)s</td>\n</tr>\n"
    REPORT_TEST_OUTPUT_TMPL = '\n<script language="javascript" type="text/javascript">output_list[\'%(id)s\'] = \'%(output)s\';</script>\n'
    ENDING_TMPL = "<div id='ending'>&nbsp;</div>"


def jsEscapeString(s):
    """ Escape s for use as a Javascript String """
    return s.replace('\\', '\\\\').replace('\r', '\\r').replace('\n', '\\n').replace('"', '\\"').replace("'", "\\'").replace('&', '\\x26').replace('<', '\\x3C').replace('>', '\\x3E')


def formatTimeDelta(time):
    if time > datetime.timedelta(seconds=60):
        return '%d:%02d.%02d' % (time.seconds / 60,
         time.seconds % 60,
         time.microseconds / 100000)
    return '%d.%02d' % (time.seconds,
     time.microseconds / 100000)


class _TestResult(object):

    def __init__(self, verbosity=1):
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.result = []

    def testTime(self, test):
        if hasattr(test, 'testStartTime'):
            return datetime.datetime.now() - test.testStartTime
        else:
            return datetime.timedelta()

    def addSuccess(self, test, capt=''):
        self.success_count += 1
        self.result.append((0, test, capt, '', self.testTime(test)))

    def addError(self, test, err, capt=''):
        self.error_count += 1
        self.result.append((2, test, capt,
         ('').join(traceback.format_exception(*err)),
         self.testTime(test)))

    def addFailure(self, test, err, capt=''):
        self.failure_count += 1
        self.result.append((1, test, capt,
         ('').join(traceback.format_exception(*err)),
         self.testTime(test)))


class HTMLGenerator_mixin(Template_mixin):
    """
    """

    def __init__(self, stream=sys.stdout, verbosity=1, title=None, description=None):
        self.title = self.DEFAULT_TITLE
        self.description = self.DEFAULT_DESCRIPTION
        self.startTime = datetime.datetime.now()

    def sortResult(self, result_list):
        rmap = {}
        class_time = {}
        classes = []
        for n, t, o, e, time in result_list:
            cls = t.__class__
            if not rmap.has_key(cls):
                rmap[cls] = []
                class_time[cls] = datetime.timedelta(0)
                classes.append(cls)
            rmap[cls].append((n, t, o, e, time))
            class_time[cls] += time

        r = [ (cls, rmap[cls]) for cls, time in sorted(class_time.items(), key=operator.itemgetter(1), reverse=True)
            ]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        self.stopTime = datetime.datetime.now()
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result.success_count:
            status.append('Pass %s' % result.success_count)
        if result.failure_count:
            status.append('Failure %s' % result.failure_count)
        if result.error_count:
            status.append('Error %s' % result.error_count)
        if status:
            status = (' ').join(status)
        else:
            status = 'none'
        return [('Start Time', startTime),
         (
          'Duration', duration),
         (
          'Status', status)]

    def generateReport(self, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(title=saxutils.escape(self.title), generator=generator, stylesheet=stylesheet, heading=heading, report=report, ending=ending)
        return output

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(name=saxutils.escape(name), value=saxutils.escape(value))
            a_lines.append(line)

        heading = self.HEADING_TMPL % dict(title=saxutils.escape(self.title), parameters=('').join(a_lines), description=saxutils.escape(self.description))
        return heading

    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        total_time = datetime.timedelta(0)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            np = nf = ne = 0
            class_time = datetime.timedelta(0)
            for n, t, o, e, time in cls_results:
                class_time += time
                total_time += time
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                else:
                    ne += 1

            if cls.__module__ == '__main__':
                name = cls.__name__
            else:
                name = '%s:%s' % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split('\n')[0] or ''
            desc = doc and '%s: %s' % (name, doc) or name
            row = self.REPORT_CLASS_TMPL % dict(style=ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass', desc=desc, time=formatTimeDelta(class_time), count=np + nf + ne, Pass=np, fail=nf, error=ne, cid='c%s' % (cid + 1))
            rows.append(row)
            for tid, (n, t, o, e, time) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e, time)

        report = self.REPORT_TMPL % dict(test_list=('').join(rows), time=formatTimeDelta(total_time), count=str(result.success_count + result.failure_count + result.error_count), Pass=str(result.success_count), fail=str(result.failure_count), error=str(result.error_count))
        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e, time):
        o = o or ''
        e = e or ''
        has_output = bool(o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        name = t.id().split('.')[(-1)]
        doc = t.shortDescription() or ''
        desc = doc and '%s: %s' % (name, doc) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL
        if isinstance(o, str):
            uo = o.decode('latin-1')
        else:
            uo = o
        if isinstance(e, str):
            ue = e.decode('latin-1')
        else:
            ue = e
        script = self.REPORT_TEST_OUTPUT_TMPL % dict(id=tid, output=jsEscapeString(uo + ue))
        row = tmpl % dict(tid=tid, Class=n == 0 and 'hiddenRow' or 'none', style=n == 2 and 'errorCase' or n == 1 and 'failCase' or 'none', desc=desc.replace("'", "\\'"), script=script, time=formatTimeDelta(time), status=self.STATUS[n])
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL


log = logging.getLogger('nose.plugins')

class HTML(HTMLGenerator_mixin, Plugin):
    """Use this plugin to get HTML output for unit tests."""

    def __init__(self, *args, **kw):
        Plugin.__init__(self, *args, **kw)
        HTMLGenerator_mixin.__init__(self)

    def options(self, parser, env):
        Plugin.options(self, parser, env)
        parser.add_option('--html-file', action='store', dest='html_file', default=env.get('NOSE_HTML_FILE', 'test_report.html'), metavar='FILE', help='HTML log file name')

    def begin(self):
        self.result = _TestResult()

    def startTest(self, test):
        test.testStartTime = datetime.datetime.now()

    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        self.html_file = os.path.abspath(options.html_file)

    def addSuccess(self, test, capt=''):
        self.result.addSuccess(test, capt)

    def addError(self, test, err, capt=''):
        self.result.addError(test, err, capt)

    def addFailure(self, test, err, capt='', tbinfo=None):
        self.result.addFailure(test, err, capt)

    def report(self, stream):
        output = self.generateReport(self.result)
        f = codecs.open(self.html_file, encoding='utf-8', mode='w')
        f.write(output)
        f.close()