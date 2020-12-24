# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyWebFramework\tax_init\PageTaxInitFormBase.py
# Compiled at: 2019-07-24 04:40:52
# Size of source mod 2**32: 2748 bytes
import os
from pyWebFramework import PageBase

class PageTaxInitFormBase(PageBase):
    url = ''

    def __init__(self):
        super(PageTaxInitFormBase, self).__init__()

    def InitPage(self):
        if not super(PageTaxInitFormBase, self).InitPage():
            return False
        self.AddScript("\nfunction queryXPathAll(xpath_str) {\n    var xresult = document.evaluate(xpath_str, document, null, XPathResult.ANY_TYPE, null);\n    var xnodes = [];\n    var xres;\n    while (xres = xresult.iterateNext()) {\n        xnodes.push(xres);\n    }\n\n    return xnodes;\n}\n\nfunction queryXPath(xpath_str) {\n    var xresult = document.evaluate(xpath_str, document, null, XPathResult.ANY_TYPE, null);\n    var xnodes = [];\n    var xres;\n    while (xres = xresult.iterateNext()) {\n        return xres\n    }\n\n    return null;\n}\n\nfunction queryXPathText(xpath_str) {\n    var e = queryXPath(xpath_str);\n    \n    if (!e) {\n        throw 'xpath not found: ' + xpath_str;\n    }\n    \n    return e.innerText.trim();\n}\n\nfunction querySelectorText(selector_str) {\n    if (typeof document.querySelector !== 'undefined') {\n        var e = document.querySelector(selector_str);\n        if (!e) {\n            throw 'selector not found: ' + selector_str;\n        }\n        \n        return e.innerText.trim();\n    }\n    \n    if (typeof $ !== 'undefined') {\n        var $e = $(selector_str);\n        if ($e.length === 0) {\n            throw 'selector not found: ' + selector_str;\n        }\n        return $e.text();\n    }\n    \n    throw 'document.querySelector is undefined';\n}\n\nfunction isCellExistByXPath(xpath_str) {\n    return !!queryXPath(xpath_str);\n}\n\nfunction isCellExistBySelector(selector_str) {\n    if (typeof document.querySelector !== 'undefined') {\n        return !!document.querySelector(selector_str);\n    }\n    \n    if (typeof $ !== 'undefined') {\n        var $e = $(selector_str);\n        return $e.length !== 0;\n    }\n    \n    throw 'document.querySelector is undefined';\n}\n\nfunction test(xpath_str) {\n    r = queryXPathAll(xpath_str);\n    \n    LOG_INFO(r.length);\n}\n\n        ")
        return True

    def GetCellTextByXPath(self, xpath):
        return self.InvokeScriptString('queryXPathText', xpath)

    def IsCellExistByXPath(self, xpath):
        return self.InvokeScriptBool('isCellExistByXPath', xpath)

    def GetCellTextBySelector(self, selector):
        return self.InvokeScriptString('querySelectorText', selector)

    def IsCellExistBySelector(self, selector):
        return self.InvokeScriptBool('isCellExistBySelector', selector)

    def test(self, xpath):
        self.InvokeScript('test', xpath)