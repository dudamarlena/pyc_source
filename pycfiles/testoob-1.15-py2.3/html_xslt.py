# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/html_xslt.py
# Compiled at: 2009-10-07 18:08:46
"""Report results in HTML, using an XSL transformation"""
from xslt import XSLTReporter

class HTMLReporter(XSLTReporter):
    __module__ = __name__

    def __init__(self, filename):
        import xslconverters
        XSLTReporter.__init__(self, filename, xslconverters.BASIC_CONVERTER)