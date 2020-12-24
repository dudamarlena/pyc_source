# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Users\zhuojiamin\Desktop\dabao\aotutest\lib\HTMLTestRunner.py
# Compiled at: 2018-08-17 04:51:20
# Size of source mod 2**32: 25876 bytes
"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.

The simplest way to use this is to invoke its main method. E.g.

    import unittest
    import HTMLTestRunner

    ... define your tests ...

    if __name__ == '__main__':
        HTMLTestRunner.main()

For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'

    # run the test
    runner.run(my_test_suite)

------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
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
__version__ = '0.8.2'
import datetime, io, sys, time, unittest
from xml.sax import saxutils

class OutputRedirector(object):
    __doc__ = ' Wrapper to redirect stdout or stderr '

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

class Template_mixin(object):
    __doc__ = '\n    Define a HTML template for report customerization and generation.\n\n    Overall structure of an HTML report\n\n    HTML\n    +------------------------+\n    |<html>                  |\n    |  <head>                |\n    |                        |\n    |   STYLESHEET           |\n    |   +----------------+   |\n    |   |                |   |\n    |   +----------------+   |\n    |                        |\n    |  </head>               |\n    |                        |\n    |  <body>                |\n    |                        |\n    |   HEADING              |\n    |   +----------------+   |\n    |   |                |   |\n    |   +----------------+   |\n    |                        |\n    |   REPORT               |\n    |   +----------------+   |\n    |   |                |   |\n    |   +----------------+   |\n    |                        |\n    |   ENDING               |\n    |   +----------------+   |\n    |   |                |   |\n    |   +----------------+   |\n    |                        |\n    |  </body>               |\n    |</html>                 |\n    +------------------------+\n    '
    STATUS = {0:'pass', 
     1:'fail', 
     2:'error'}
    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''
    HTML_TMPL = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n    <title>%(title)s</title>\n    <meta name="generator" content="%(generator)s"/>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>\n    %(stylesheet)s\n</head>\n<body>\n<script language="javascript" type="text/javascript"><!--\noutput_list = Array();\n\n/* level - 0:Summary; 1:Failed; 2:All */\nfunction showCase(level) {\n    trs = document.getElementsByTagName("tr");\n    for (var i = 0; i < trs.length; i++) {\n        tr = trs[i];\n        id = tr.id;\n        if (id.substr(0,2) == \'ft\') {\n            if (level < 1) {\n                tr.className = \'hiddenRow\';\n            }\n            else {\n                tr.className = \'\';\n            }\n        }\n        if (id.substr(0,2) == \'pt\') {\n            if (level > 1) {\n                tr.className = \'\';\n            }\n            else {\n                tr.className = \'hiddenRow\';\n            }\n        }\n    }\n}\n\n\nfunction showClassDetail(cid, count) {\n    var id_list = Array(count);\n    var toHide = 1;\n    for (var i = 0; i < count; i++) {\n        tid0 = \'t\' + cid.substr(1) + \'.\' + (i+1);\n        tid = \'f\' + tid0;\n        tr = document.getElementById(tid);\n        if (!tr) {\n            tid = \'p\' + tid0;\n            tr = document.getElementById(tid);\n        }\n        id_list[i] = tid;\n        if (tr.className) {\n            toHide = 0;\n        }\n    }\n    for (var i = 0; i < count; i++) {\n        tid = id_list[i];\n        if (toHide) {\n            document.getElementById(\'div_\'+tid).style.display = \'hiddenRow\'\n            document.getElementById(tid).className = \'hiddenRow\';\n        }\n        else {\n            document.getElementById(tid).className = \'\';\n        }\n    }\n}\n\n\nfunction showTestDetail(div_id){\n    var details_div = document.getElementById(div_id)\n    var displayState = details_div.style.display\n    if (displayState != \'block\' ) {\n        displayState = \'block\'\n        details_div.style.display = \'block\'\n    }\n    else {\n        details_div.style.display = \'none\'\n    }\n}\n\n\nfunction html_escape(s) {\n    s = s.replace(/&/g,\'&amp;\');\n    s = s.replace(/</g,\'&lt;\');\n    s = s.replace(/>/g,\'&gt;\');\n    return s;\n}\n\n/* obsoleted by detail in <div>\nfunction showOutput(id, name) {\n    var w = window.open("", //url\n                    name,\n                    "resizable,scrollbars,status,width=800,height=450");\n    d = w.document;\n    d.write("<pre>");\n    d.write(html_escape(output_list[id]));\n    d.write("\\n");\n    d.write("<a href=\'javascript:window.close()\'>close</a>\\n");\n    d.write("</pre>\\n");\n    d.close();\n}\n*/\n--></script>\n\n%(heading)s\n%(report)s\n%(ending)s\n\n</body>\n</html>\n'
    STYLESHEET_TMPL = '\n<style type="text/css" media="screen">\nbody        { font-family: verdana, arial, helvetica, sans-serif; font-size: 14px; max-width: 900px; margin: 0 auto; margin-top:2%; }\ntable       { font-size: 100%; }\npre         { width: 500px; white-space: pre-wrap; }\n\n/* -- heading ---------------------------------------------------------------------- */ \nh1 {\n\tfont-size: 16pt;\n}\n.heading {\n    margin-top: 0ex;\n    margin-bottom: 1ex;\n    text-align: center;\n}\n\n.heading .attribute {\n    margin-top: 1ex;\n    margin-bottom: 0;\n}\n.items{\n    width: 50%;\n    margin-bottom: 5px;\n}\n\n.heading .description {\n    margin-top: 4ex;\n    margin-bottom: 6ex;\n}\n\n/* -- css div popup ------------------------------------------------------------------------ */\na.popup_link {\n}\n\na.popup_link:hover {\n    color: red;\n}\n\n.popup_window {\n    margin-top: 10px;\n    display: none;\n    position: relative;\n    left: 0px;\n    top: 0px;\n    /*border: solid #627173 1px; */\n    padding: 10px;\n    background-color: #F4F4F4;\n    font-family: "Lucida Console", "Courier New", Courier, monospace;\n    text-align: left;\n    font-size: 8pt;\n    width: 500px;\n}\n\n}\n/* -- report ------------------------------------------------------------------------ */\n#show_detail_line {\n    margin-top: 3ex;\n    margin-bottom: 1ex;\n}\n#result_table {\n    width: 100%;\n    border-collapse: collapse;\n}\n#header_row {\n    font-weight: bold;\n    color: white;\n    background-color: #08c3b4;\n}\n\n#result_table td {\n    border: 1px solid #eee;\n    padding: 10px;\n}\n#header_row td, .failClass td{\n    border: 0\n}\n#total_row  { font-weight: bold; }\n.passClass  { background-color: #f3f5f5; color: #08c3b4; }\n.failClass  { background-color: #f3f5f5; color: #948989; }\n.errorClass { background-color: #f3f5f5; color: #c00; }\n.passCase   { color: #6c6; }\n.failCase   { color: #c60; font-weight: bold; }\n.errorCase  { color: #c00; font-weight: bold; }\n.hiddenRow  { display: none; }\n.hide       { display: none; }\n.testcase   { margin-left: 2em; }\n\n\n/* -- ending ---------------------------------------------------------------------- */\n#ending {\n}\n\n</style>\n'
    HEADING_TMPL = "<div class='heading'>\n<h1>%(title)s</h1>\n</div>\n<div style='border: 1px solid #eee;'>\n<div>\n\n%(parameters)s\n<p class='description'>%(description)s</p>\n\n\n"
    HEADING_ATTRIBUTE_TMPL = "<ul style='list-style: none;'><li class='attribute items' style='float: left;'><strong>%(name)s:</strong> %(value)s</li></ul>\n"
    REPORT_TMPL = '\n<p id=\'show_detail_line\'>报告详情：\n<a href=\'javascript:showCase(0)\'>Summary</a>\n<a href=\'javascript:showCase(1)\'>Failed</a>\n<a href=\'javascript:showCase(2)\'>All</a>\n</p>\n</div>\n<table id=\'result_table\' style=\'text-align:center; margin:0 auto;\'>\n<colgroup>\n<col align=\'left\' />\n<col align=\'right\' />\n<col align=\'right\' />\n<col align=\'right\' />\n<col align=\'right\' />\n<col align=\'right\' />\n</colgroup>\n<tr id=\'header_row\'>\n    <td>用例集/测试用例</td>\n    <td>总计</td>\n    <td>通过</td>\n    <td>失败</td>\n    <td>错误</td>\n    <td>详情</td>\n</tr>\n%(test_list)s\n<tr id=\'total_row\'>\n    <td>总计</td>\n    <td>%(count)s</td>\n    <td>%(Pass)s</td>\n    <td>%(fail)s</td>\n    <td>%(error)s</td>\n    <td>&nbsp;</td>\n</tr>\n</table>\n</div>\n<div style="position: fixed; bottom: 100px; right: 50px; width: 20px; background-color: #08c3b4; text-align: center;"><a href="#topAnchor" style="color: #fff">回到顶部</a></div>\n'
    REPORT_CLASS_TMPL = '\n<tr class=\'%(style)s\'>\n    <td>%(desc)s</td>\n    <td>%(count)s</td>\n    <td>%(Pass)s</td>\n    <td>%(fail)s</td>\n    <td>%(error)s</td>\n    <td><a href="javascript:showClassDetail(\'%(cid)s\',%(count)s)">详情</a></td>\n</tr>\n'
    REPORT_TEST_WITH_OUTPUT_TMPL = '\n<tr id=\'%(tid)s\' class=\'%(Class)s hide\'>\n    <td class=\'%(style)s\'><div class=\'testcase\'>%(desc)s</div></td>\n    <td colspan=\'5\' align=\'center\'>\n\n    <!--css div popup start-->\n    <a class="popup_link" onfocus=\'this.blur();\' href="javascript:showTestDetail(\'div_%(tid)s\')" >\n        %(status)s</a>\n\n    <div id=\'div_%(tid)s\' class="popup_window">\n        <div style=\'text-align: right; color:red;cursor:pointer\'>\n        <a onfocus=\'this.blur();\' onclick="document.getElementById(\'div_%(tid)s\').style.display = \'none\' " >\n           [x]</a>\n        </div>\n        <pre>\n        %(script)s\n        </pre>\n    </div>\n    <!--css div popup end-->\n\n    </td>\n</tr>\n'
    REPORT_TEST_NO_OUTPUT_TMPL = "\n<tr id='%(tid)s' class='%(Class)s'>\n    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>\n    <td colspan='5' align='center'>%(status)s</td>\n</tr>\n"
    REPORT_TEST_OUTPUT_TMPL = '\n%(id)s: %(output)s\n'
    ENDING_TMPL = "<div id='ending'>&nbsp;</div>"


TestResult = unittest.TestResult

class _TestResult(TestResult):

    def __init__(self, verbosity=2):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity
        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)
        self.outputBuffer = io.StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('Pass: ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[(-1)]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('Error:  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('Error')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[(-1)]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('Failure:  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('Failure')


class HTMLTestRunner(Template_mixin):
    __doc__ = '\n    '

    def __init__(self, stream=sys.stdout, verbosity=2, title=None, description=None):
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        self.startTime = datetime.datetime.now()

    def run(self, test):
        """Run the given test case or test suite."""
        result = _TestResult(self.verbosity)
        test(result)
        self.stopTime = datetime.datetime.now()
        self.generateReport(test, result)
        return result

    def sortResult(self, result_list):
        rmap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e))

        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result.success_count:
            status.append('通过： %s' % result.success_count)
        else:
            if result.failure_count:
                status.append('失败： %s' % result.failure_count)
            if result.error_count:
                status.append('错误： %s' % result.error_count)
            if status:
                status = ' '.join(status)
            else:
                status = 'none'
        return [
         (
          'Start Time', startTime),
         (
          'Duration', duration),
         (
          'Status', status)]

    def generateReport(self, test, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(title=(saxutils.escape(self.title)),
          generator=generator,
          stylesheet=stylesheet,
          heading=heading,
          report=report,
          ending=ending)
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(name=(saxutils.escape(name)),
              value=(saxutils.escape(value)))
            a_lines.append(line)

        heading = self.HEADING_TMPL % dict(title=(saxutils.escape(self.title)),
          parameters=(''.join(a_lines)),
          description=(saxutils.escape(self.description)))
        return heading

    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                else:
                    if n == 1:
                        nf += 1
                    else:
                        ne += 1

            if cls.__module__ == '__main__':
                name = cls.__name__
            else:
                name = '%s.%s' % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split('\n')[0] or ''
            desc = doc and '%s: %s' % (name, doc) or name
            row = self.REPORT_CLASS_TMPL % dict(style=(ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass'),
              desc=desc,
              count=(np + nf + ne),
              Pass=np,
              fail=nf,
              error=ne,
              cid=('c%s' % (cid + 1)))
            rows.append(row)
            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)

        report = self.REPORT_TMPL % dict(test_list=(''.join(rows)),
          count=(str(result.success_count + result.failure_count + result.error_count)),
          Pass=(str(result.success_count)),
          fail=(str(result.failure_count)),
          error=(str(result.error_count)))
        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        has_output = bool(o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        name = t.id().split('.')[(-1)]
        doc = t.shortDescription() or ''
        desc = doc and '%s: %s' % (name, doc) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL
        uo = o
        if isinstance(e, str):
            ue = e
        else:
            ue = e
        script = self.REPORT_TEST_OUTPUT_TMPL % dict(id=tid,
          output=(saxutils.escape(uo + ue)))
        row = tmpl % dict(tid=tid,
          Class=(n == 0 and 'hiddenRow' or 'none'),
          style=(n == 2 and 'errorCase' or n == 1 and 'failCase' or 'none'),
          desc=desc,
          script=script,
          status=(self.STATUS[n]))
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL


class TestProgram(unittest.TestProgram):
    __doc__ = '\n    A variation of the unittest.TestProgram. Please refer to the base\n    class for command line parameters.\n    '

    def runTests(self):
        if self.testRunner is None:
            self.testRunner = HTMLTestRunner(verbosity=(self.verbosity))
        unittest.TestProgram.runTests(self)


main = TestProgram
if __name__ == '__main__':
    main(module=None)