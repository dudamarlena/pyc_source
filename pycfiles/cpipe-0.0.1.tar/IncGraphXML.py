# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/IncGraphXML.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Generates an XML file from an include graph.\n\nThis is implemented as a hierarchical visitor pattern. This could have be\nimplemented as a non-hierarchical visitor pattern using less memory\nat the expense of more code.\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from cpip.core import FileIncludeGraph
from cpip.core import PpToken
from cpip.core import PpTokenCount
from cpip.util import XmlWrite

def processIncGraphToXml(theLex, theFilePath):
    """Convert a Include graph from a PpLexer to SVG in theFilePath."""
    myVis = FileIncludeGraph.FigVisitorTree(IncGraphXML)
    theLex.fileIncludeGraphRoot.acceptVisitor(myVis)
    myIgs = myVis.tree()
    myIgs.writeToFilePath(theFilePath)


class IncGraphXML(FileIncludeGraph.FigVisitorTreeNodeBase):

    def __init__(self, theFig, theLineNum):
        super(IncGraphXML, self).__init__(theLineNum)
        self._isRoot = theFig is None
        self._tokenCounterChildren = PpTokenCount.PpTokenCount()
        if self._isRoot:
            self._dataMap = None
        else:
            self._dataMap = {}
            self._dataMap['fileName'] = theFig.fileName
            self._dataMap['numToks'] = theFig.numTokens
            self._dataMap['condComp'] = theFig.condComp
            self._dataMap['condCompState'] = theFig.condCompState
            self._dataMap['tokenCntr'] = theFig.tokenCounter
            self._dataMap['findLogic'] = theFig.findLogic
        return

    @property
    def tokenCounter(self):
        """This is the computed PpTokenCount.PpTokenCount() me only."""
        return self._dataMap['tokenCntr']

    @property
    def tokenCounterChildren(self):
        """This is the computed PpTokenCount.PpTokenCount() for all my children but not me."""
        return self._tokenCounterChildren

    def finalise(self):
        """This will be called on finalisation. This just accumulates the
        child token counter."""
        self._tokenCounterChildren = PpTokenCount.PpTokenCount()
        for aChild in self._children:
            aChild.finalise()

        for aChild in self._children:
            self._tokenCounterChildren += aChild.tokenCounter
            self._tokenCounterChildren += aChild.tokenCounterChildren

    def writeToFilePath(self, theFileName):
        """Root level call to plot to a SVG file, theTpt is an
        TreePlotTransform object and is used to transform the internal logical
        coordinates to physical plot positions."""
        self.writeToFileObj(open(theFileName, 'w'))

    def writeToFileObj(self, theFileObj):
        """Root level call to plot to a file object. The SVG stream is
        created here."""
        with XmlWrite.XmlStream(theFileObj) as (myS):
            self.writeToSVGStream(myS)

    def writeToSVGStream(self, theS):
        """Write me to a stream and my children at the logical datum point,
        this is a recursive call."""
        if not self._isRoot:
            self._writeSelf(theS)
        if len(self._children) > 0:
            for c in self._children:
                c.writeToSVGStream(theS)

    def _writeSelf(self, theS):
        """Plot me to a stream at the logical datum point.
        Must be provided by child classes."""
        assert not self._isRoot
        myAtrtrs = {'name': self._dataMap['fileName'], 
           'bool': str(self._dataMap['condComp'])}
        with XmlWrite.Element(theS, 'File', myAtrtrs):
            pass

    def _writeTokenCounters(self, theS, theCntr):
        with XmlWrite.Element(theS, 'TokenCounts'):
            with XmlWrite.Element('TokenCountAll'):
                self._writeTokenCounter(theS, theCntr, True)
            with XmlWrite.Element(theS, 'TokenCountUnconditional'):
                self._writeTokenCounter(theS, theCntr, True)

    def _writeTokenCounter(self, theS, theCntr, isAll):
        for aType in PpToken.LEX_PPTOKEN_TYPES:
            myAttrs = {'type': aType, 
               'count': '%d' % theCntr.tokenCount(aType, isAll)}
            with XmlWrite.Element(theS, 'Tokens', myAttrs):
                pass