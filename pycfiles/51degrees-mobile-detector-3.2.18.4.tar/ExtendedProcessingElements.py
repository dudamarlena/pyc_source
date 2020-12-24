# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\ExtendedProcessingElements.py
# Compiled at: 2005-09-29 16:53:48
__doc__ = '\nExtended versions of XSLT elements for debugging and execution tracing\n\nThese subclasses typically just override the .instantiate method of the\noriginal class, doing something before calling the original method, like\nwriting debug or trace output and maintaining whatever state info is\nnecessary in the process.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import sys, time

class BaseElement:
    """
    An XSLT element superclass that supports debugging and execution tracing.

    An existing XSLT element can be extended by subclassing this and the
    original element class. In order to make use of the extended class, it
    should be referenced in Ft.Xml.Xslt.StylesheetHandler._ELEMENT_MAPPING,
    and additional instance variables necessary should be set as desired.
    """
    __module__ = __name__
    _ft_debugger_saveResults = 0
    _ft_debugger_record = -1

    def doAll(self, processor, method, args, argNames, name, _timer=time.time):
        """
        This method, specific to extended processign elements, attempts to
        perform all extended processing. By default, it looks at the given
        processor's instance variables to determine what to do; e.g.,
        processor._4xslt_debug can trigger debug handling.

        processor is the active Processor instance.

        method is the instantiate method of the original element class.

        args are a sequence of arguments (besides self) for the method.
        argNames are the names of these arguments, for display purposes
        (the names from the method signature, usually). keyword args are
        not supported.

        name is the display name of the original element.
        """
        if processor._4xslt_trace:
            argStr = ''
            for ctr in xrange(len(args)):
                if argNames[ctr]:
                    argStr = argStr + '%s = %s ' % (argNames[ctr], args[ctr])

            if hasattr(self, 'baseUri'):
                name = name + ' Uri: %s' % self.baseUri
            if hasattr(self, 'lineNumber') and self.lineNumber != '??':
                name = name + ' Line: %s Col %s' % (self.lineNumber, self.columnNumber)
            processor._4xslt_traceStream.write('%s Begin %s %s\n' % (processor._4xslt_traceIndent * '  ', name, argStr))
            processor._4xslt_traceIndent += 1
            start = _timer()
            rt = method(self, *args)
            end = _timer()
            processor._4xslt_traceIndent -= 1
            processor._4xslt_traceStream.write('%s End %s %s in %0.5fs\n' % (processor._4xslt_traceIndent * '  ', name, argStr, end - start))
        elif processor._4xslt_debug:
            if self._ft_debugger_record:
                res = processor._ft_debug_controller.startCall(self, args[0])
            record = self._ft_debugger_record
            if self._ft_debugger_record > 0:
                self._ft_debugger_record = self._ft_debugger_record - 1
            rt = method(self, *args)
            if record:
                processor._ft_debug_controller.endCall(self, args[0], res, self._ft_debugger_saveResults and rt or None)
        else:
            rt = method(self, *args)
        return rt
        return


from Ft.Xml.Xslt import Processor

class ExtendedProcessor(BaseElement, Processor.Processor):
    """
    A version of the Processor class that supports debugging and tracing.
    """
    __module__ = __name__
    _4xslt_trace = True
    _4xslt_traceIndent = 0
    _4xslt_traceStream = sys.stderr
    _ft_debugger_record = 1

    def applyTemplates(self, context, params=None):
        return self.doAll(self, Processor.Processor.applyTemplates, (
         context, params), (
         'context', 'params'), 'Processor.ApplyTemplates')


from Ft.Xml.Xslt import TemplateElement

class ExtendedTemplateElement(BaseElement, TemplateElement.TemplateElement):
    __module__ = __name__

    def instantiate(self, context, processor, params=None):
        name = 'TemplateElement'
        if self._match:
            name = name + " match='%s'" % repr(self._match)
        if self._mode:
            name = name + " mode='%s'" % str(self._mode)
        if self._name:
            name = name + " name='%s'" % str(self._name)
        return self.doAll(processor, TemplateElement.TemplateElement.instantiate, (
         context, processor, params), (
         'context', None, 'params'), name)
        return


from Ft.Xml.Xslt import IfElement

class ExtendedIfElement(BaseElement, IfElement.IfElement):
    __module__ = __name__

    def instantiate(self, context, processor):
        name = "xsl:if test='%s'" % repr(self._test)
        return self.doAll(processor, IfElement.IfElement.instantiate, (
         context, processor), (
         'context', None), name)
        return


from Ft.Xml.Xslt import ChooseElement

class ExtendedChooseElement(BaseElement, ChooseElement.ChooseElement):
    __module__ = __name__

    def instantiate(self, context, processor):
        name = 'xsl:choose'
        return self.doAll(processor, ChooseElement.ChooseElement.instantiate, (
         context, processor), (
         'context', None), name)
        return


class ExtendedSimpleElement(BaseElement):
    __module__ = __name__

    def instantiate(self, context, processor):
        name = self.getName()
        return self.doAll(processor, self._ft_actualClass.instantiate, (
         context, processor), (
         'context', None), name)
        return


from Ft.Xml.Xslt import LiteralElement

class ExtendedLiteralElement(ExtendedSimpleElement, LiteralElement.LiteralElement):
    __module__ = __name__
    _ft_actualClass = LiteralElement.LiteralElement

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return 'LiteralElement: %s' % self.nodeName


from Ft.Xml.Xslt import ValueOfElement

class ExtendedValueOfElement(ExtendedSimpleElement, ValueOfElement.ValueOfElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return "xsl:value-of select='%s'" % repr(self._select)


from Ft.Xml.Xslt import AttributeElement

class ExtendedAttributeElement(ExtendedSimpleElement, AttributeElement.AttributeElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return "xsl:attribute name='%s'" % str(self._name)


from Ft.Xml.Xslt import CommentElement

class ExtendedCommentElement(ExtendedSimpleElement, CommentElement.CommentElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return 'xsl:comment'


from Ft.Xml.Xslt import CopyElement

class ExtendedCopyElement(ExtendedSimpleElement, CopyElement.CopyElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return 'xsl:copy'


from Ft.Xml.Xslt import CopyOfElement

class ExtendedCopyOfElement(ExtendedSimpleElement, CopyOfElement.CopyOfElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return "xsl:copy-of select='%s'" % repr(self._select)


from Ft.Xml.Xslt import ElementElement

class ExtendedElementElement(ExtendedSimpleElement, ElementElement.ElementElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return "xsl:element name='%s'" % str(self._name)


from Ft.Xml.Xslt import ForEachElement

class ExtendedForEachElement(ExtendedSimpleElement, ForEachElement.ForEachElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return "xsl:for-each select='%s'" % repr(self._select)


from Ft.Xml.Xslt import ProcessingInstructionElement

class ExtendedProcessingInstructionElement(ExtendedSimpleElement, ProcessingInstructionElement.ProcessingInstructionElement):
    __module__ = __name__

    def getName(self):
        self._ft_actualClass = self.__class__.__bases__[1]
        return 'xsl:processing-instruction'


newMappings = {'template': 'ExtendedProcessingElements.ExtendedTemplateElement', 'if': 'ExtendedProcessingElements.ExtendedIfElement', 'value-of': 'ExtendedProcessingElements.ExtendedValueOfElement', 'choose': 'ExtendedProcessingElements.ExtendedChooseElement', 'attribute': 'ExtendedProcessingElements.ExtendedAttributeElement', 'comment': 'ExtendedProcessingElements.ExtendedCommentElement', 'copy': 'ExtendedProcessingElements.ExtendedCopyElement', 'copy-of': 'ExtendedProcessingElements.ExtendedCopyOfElement', 'element': 'ExtendedProcessingElements.ExtendedElementElement', 'for-each': 'ExtendedProcessingElements.ExtendedForEachElement', 'processing-instruction': 'ExtendedProcessingElements.ExtendedProcessingInstructionElement'}

def GetMappings():
    import StylesheetHandler
    g_traceMappings = StylesheetHandler._ELEMENT_MAPPING.copy()
    g_traceMappings.update(newMappings)
    StylesheetHandler.LiteralElement = ExtendedLiteralElement
    return g_traceMappings