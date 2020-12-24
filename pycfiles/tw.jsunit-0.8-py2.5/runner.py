# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/laureano/desarrollo/eggs/tw/twtools/projects/tw.jsunit/trunk/tw/jsunit/runner.py
# Compiled at: 2008-04-25 20:27:53
from tw.api import Widget, JSLink, CSSLink, JSSource
from tw.core.resources import Resource
from tw.jsunit.base import *
from tw.jsunit import jsunit_css
__all__ = [
 'Runner', 'RunnerJS', 'RunnerSetupJS']

class RunnerSetupJS(JSSource):
    __module__ = __name__
    resources = []
    source_vars = [
     'testpage']
    src = "\n    function jsUnitParseParms(string) {\n        var i;\n        var searchString = unescape(string);\n        var parameterHash = new Object();\n\n        if (!searchString) {\n            return parameterHash;\n        }\n\n        i = searchString.indexOf('?');\n        if (i != -1) {\n            searchString = searchString.substring(i + 1);\n        }\n\n        var parmList = searchString.split('&');\n        var a;\n        for (i = 0; i < parmList.length; i++) {\n            a = parmList[i].split('=');\n            a[0] = a[0].toLowerCase();\n            if (a.length > 1) {\n                parameterHash[a[0]] = a[1];\n            }\n            else {\n                parameterHash[a[0]] = true;\n            }\n        }\n        return parameterHash;\n    }\n\n    function jsUnitConstructTestParms() {\n        var p;\n        var parms = '';\n\n        for (p in jsUnitParmHash) {\n            var value = jsUnitParmHash[p];\n\n            if (!value ||\n                p == 'testpage' ||\n                p == 'autorun' ||\n                p == 'submitresults' ||\n                p == 'showtestframe' ||\n                p == 'resultid') {\n                continue;\n            }\n\n            if (parms) {\n                parms += '&';\n            }\n\n            parms += p;\n\n            if (typeof(value) != 'boolean') {\n                parms += '=' + value;\n            }\n        }\n        return escape(parms);\n    }\n\n    // var jsUnitParmHash = jsUnitParseParms(document.location.search);\n    var jsUnitParmHash = jsUnitParseParms('testpage=$testpage');\n\n    // set to true to turn debugging code on, false to turn it off.\n    xbDEBUG.on = jsUnitGetParm('debug') ? true : false;\n    "
    template_engine = 'genshi'
    javascript = [jsunit_js]

    def update_params(self, d):
        for param in self.source_vars:
            value = getattr(self, param)

        super(RunnerSetupJS, self).update_params(d)

    def post_init(self, *args, **kw):
        pass

    location = Resource.valid_locations.head


class RunnerJS(JSSource):
    __module__ = __name__
    resources = []
    source_vars = []
    src = '\n    var testManager;\n    var utility;\n    var tracer;\n\n\n    if (!Array.prototype.push) {\n        Array.prototype.push = function (anObject) {\n            this[this.length] = anObject;\n        }\n    }\n\n    if (!Array.prototype.pop) {\n        Array.prototype.pop = function () {\n            if (this.length > 0) {\n                delete this[this.length - 1];\n                this.length--;\n            }\n        }\n    }\n\n    function shouldKickOffTestsAutomatically() {\n        return jsUnitGetParm(\'autorun\') == "true";\n    }\n\n    function shouldShowTestFrame() {\n        return jsUnitGetParm(\'showtestframe\');\n    }\n\n    function shouldSubmitResults() {\n        return jsUnitGetParm(\'submitresults\');\n    }\n\n    function getResultId() {\n        if (jsUnitGetParm(\'resultid\'))\n            return jsUnitGetParm(\'resultid\');\n        return "";\n    }\n\n    function submitResults() {\n        window.mainFrame.mainData.document.testRunnerForm.runButton.disabled = true;\n        window.mainFrame.mainResults.populateHeaderFields(getResultId(), navigator.userAgent, JSUNIT_VERSION, testManager.resolveUserEnteredTestFileName());\n        window.mainFrame.mainResults.submitResults();\n    }\n\n    function wasResultUrlSpecified() {\n        return shouldSubmitResults() && jsUnitGetParm(\'submitresults\') != \'true\';\n    }\n\n    function getSpecifiedResultUrl() {\n        return jsUnitGetParm(\'submitresults\');\n    }\n\n    function init() {\n        var testRunnerFrameset = document.getElementById(\'testRunnerFrameset\');\n        if (shouldShowTestFrame() && testRunnerFrameset) {\n            var testFrameHeight;\n            if (jsUnitGetParm(\'showtestframe\') == \'true\')\n                testFrameHeight = DEFAULT_TEST_FRAME_HEIGHT;\n            else\n                testFrameHeight = jsUnitGetParm(\'showtestframe\');\n            testRunnerFrameset.rows = \'*,0,\' + testFrameHeight;\n        }\n        testManager = new jsUnitTestManager();\n        tracer = new JsUnitTracer(testManager);\n        if (shouldKickOffTestsAutomatically()) {\n            window.mainFrame.mainData.kickOffTests();\n        }\n    }\n    '
    template_engine = 'genshi'
    javascript = [jsunit_js]

    def update_params(self, d):
        for param in self.source_vars:
            value = getattr(self, param)

        super(RunnerJS, self).update_params(d)

    def post_init(self, *args, **kw):
        pass

    location = Resource.valid_locations.head


class Runner(Widget):
    __module__ = __name__
    runner_setup_js_obj = RunnerSetupJS
    runner_js_obj = RunnerJS
    params = js_params = ['testpage']
    testpage = '/runpage'
    template = '\n<frameset id="testRunnerFrameset" rows="*,0,0" border="0" onload="init()">\n\n    <frame frameborder="0" name="mainFrame" src="toscawidgets/resources/tw.jsunit.base/static/app/main-frame.html">\n    <frame frameborder="0" name="documentLoader" src="toscawidgets/resources/tw.jsunit.base/static/app/main-loader.html">\n    <frame frameborder="0" name="testContainer" src="toscawidgets/resources/tw.jsunit.base/static/app/testContainer.html">\n\n    <noframes>\n        <body>\n        <p>Sorry, JsUnit requires support for frames.</p>\n        </body>\n    </noframes>\n</frameset>\n    '

    def __init__(self, *args, **kw):
        super(Runner, self).__init__(*args, **kw)
        d = {}
        for param in self.js_params:
            value = getattr(self, param)
            if value is not None:
                d[param] = getattr(self, param)

        runner_setup_js = self.runner_setup_js_obj(**d)
        runner_js = self.runner_js_obj(**d)
        self.javascript = [jsunit_js, jsunit_xbdebug_js, jsunit_test_manager_js, jsunit_tracer_js, jsunit_test_suite_js, runner_setup_js, runner_js]
        self.css = [jsunit_css]
        return

    def update_params(self, d):
        super(Runner, self).update_params(d)