# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/CppCondGraphToHtml.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Writes out the Cpp Conditional processing graph as HTML.'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import os, cpip
from cpip.core import CppCond
from cpip.util import XmlWrite
from cpip.util import HtmlUtils
from cpip import TokenCss

def linkToIndex(theS, theIdxPath):
    with XmlWrite.Element(theS, 'p'):
        theS.characters('Return to ')
        with XmlWrite.Element(theS, 'a', {'href': theIdxPath}):
            theS.characters('Index')


class CcgVisitorToHtml(CppCond.CppCondGraphVisitorBase):
    """Writing CppCondGraph visitor object."""
    PAD_STR = '  '

    def __init__(self, theHtmlStream):
        """Constructor with an output XmlWrite.XhtmlStream and
        a a TuIndexer.TuIndexer object."""
        super(CcgVisitorToHtml, self).__init__()
        self._hs = theHtmlStream

    def visitPre(self, theCcgNode, theDepth):
        """Pre-traversal call with a CppCondGraphNode and the integer depth in
        the tree."""
        self._hs.characters(self.PAD_STR * theDepth)
        if theCcgNode.state:
            myCssClass = 'CcgNodeTrue'
        else:
            myCssClass = 'CcgNodeFalse'
        with XmlWrite.Element(self._hs, 'span', {'class': myCssClass}):
            self._hs.characters('#%s' % theCcgNode.cppDirective)
            if theCcgNode.constExpr is not None:
                self._hs.characters(' %s' % theCcgNode.constExpr)
        self._hs.characters(' ')
        self._hs.characters(' /* ')
        HtmlUtils.writeHtmlFileLink(self._hs, theCcgNode.fileId, theCcgNode.lineNum, os.path.basename(theCcgNode.fileId), theClass=None)
        self._hs.characters(' */')
        self._hs.characters('\n')
        return

    def visitPost(self, theCcgNode, theDepth):
        """Post-traversal call with a CppCondGraphNode and the integer depth in
        the tree."""
        pass


def processCppCondGrphToHtml(theLex, theHtmlPath, theTitle, theIdxPath):
    """Given the PpLexer write out the Cpp Cond Graph to the HTML file.
    theLex is a PpLexer.
    theHtmlPath is the file path of the output.
    theTitle is the page title.
    theIdxPath is the file name of the index page.
    theTuIndexer is a TuIndexer.TuIndexer object."""
    if not os.path.exists(os.path.dirname(theHtmlPath)):
        os.makedirs(os.path.dirname(theHtmlPath))
    with XmlWrite.XhtmlStream(theHtmlPath, mustIndent=cpip.INDENT_ML) as (myS):
        with XmlWrite.Element(myS, 'head'):
            with XmlWrite.Element(myS, 'link', {'href': TokenCss.TT_CSS_FILE, 
               'type': 'text/css', 
               'rel': 'stylesheet'}):
                pass
            with XmlWrite.Element(myS, 'title'):
                myS.characters(theTitle)
        with XmlWrite.Element(myS, 'body'):
            with XmlWrite.Element(myS, 'h1'):
                myS.characters('Preprocessing Conditional Compilation Graph: %s' % theLex.tuFileId)
            with XmlWrite.Element(myS, 'p'):
                myS.characters('The conditional compilation statements as green (i.e. evaluates as True)\nand red (evaluates as False). Each statement is linked to the source code it came from.\n')
            linkToIndex(myS, theIdxPath)
            with XmlWrite.Element(myS, 'pre'):
                myVisitor = CcgVisitorToHtml(myS)
                theLex.condCompGraph.visit(myVisitor)