# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/xslt.py
# Compiled at: 2009-10-07 18:08:46
"""Apply an XSL transformation to XMLReporter's xml output"""
from xml import XMLReporter
import time

class XSLTReporter(XMLReporter):
    """This reporter uses an XSL transformation scheme to convert an XML output"""
    __module__ = __name__

    class IXSLTApplier:
        """An interface for XSLT libs"""
        __module__ = __name__

        def __init__(self, transform):
            """A constructor with the transformation to apply (string)"""
            pass

        def apply(self, input, params={}):
            """Apply the transformation to the input and return the result.
            Params is a dictionary of extra parameters for the XSLT convertion"""
            pass

    class FourSuiteXSLTApplier(IXSLTApplier):
        """XSLT applier that uses 4Suite"""
        __module__ = __name__

        def __init__(self, transform):
            from Ft.Xml.Xslt import Processor
            from Ft.Xml import InputSource
            self.processor = Processor.Processor()
            trans_source = InputSource.DefaultFactory.fromString(transform, 'CONVERTER')
            self.processor.appendStylesheet(trans_source)

        def apply(self, input, params={}):
            from Ft.Xml import InputSource
            input_source = InputSource.DefaultFactory.fromString(input, 'XML')
            return self.processor.run(input_source, topLevelParams=params)

    class WinCOMXSLTApplier(IXSLTApplier):
        """XSLT applier that uses window's COM interface to use a common windows XML library"""
        __module__ = __name__

        def __init__(self, transform):
            import win32com.client
            self.trans_obj = win32com.client.Dispatch('Microsoft.XMLDOM')
            self.trans_obj.loadXML(transform)

        def apply(self, input, params={}):
            import win32com.client
            input_obj = win32com.client.Dispatch('Microsoft.XMLDOM')
            input_obj.loadXML(input)
            return input_obj.transformNode(self.trans_obj)

    def __init__(self, filename, converter):
        XMLReporter.__init__(self)
        self.filename = filename
        self.converter = converter

    def done(self):
        XMLReporter.done(self)
        xslt_applier = self._create_xslt_applier()(self.converter)
        result = xslt_applier.apply(self.get_xml(), params={'date': unicode(time.asctime())})
        open(self.filename, 'wt').write(result)

    def _create_xslt_applier(self):
        try:
            import Ft.Xml
            return XSLTReporter.FourSuiteXSLTApplier
        except:
            pass

        try:
            import win32com.client
            win32com.client.Dispatch('Microsoft.XMLDOM')
            return XSLTReporter.WinCOMXSLTApplier
        except:
            pass

        raise Exception, 'Unable to find supported XSLT library (4Suite, MSXML)'