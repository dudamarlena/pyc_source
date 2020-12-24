# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/IncGraphSVG.py
# Compiled at: 2017-10-03 13:07:16
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import os, inspect
from cpip.core import PpTokenCount
from cpip.util import XmlWrite
from cpip.plot import Coord
from cpip.plot import PlotNode
from cpip.plot import SVGWriter
from cpip import IncGraphSVGBase

class SVGTreeNodeMain(IncGraphSVGBase.SVGTreeNodeBase):
    """This does most of the heavy lifting of plotting the include graph SVG.
    The challenges are plotting things in the 'right' order and with the 'right'
    JavaScript so that the DHTML does not look too hideous.
    
    Basic principle here is that :py:meth:`plotInitialise` writes static data. In
    our case just the pretty histogram pop-up (Ed. is this right???).
    
    Then :py:meth:`.SVGTreeNodeBase.plotToSVGStream` is called -
    this is implemented in the base class.
    
    Finally :py:meth:`plotFinalise` is called - this overlays the DHTML text. This is
    a little tricky as our way of DHTML is to switch opacity on underlying
    objects the switching boundary being the overlying object (e.g. '?').
    So _all_ the underlying objects need to be written first so that the
    overlying objects are always 'visible' to trigger onmouseover/onmouseout on
    the underlying object."""
    COMMON_UNITS = 'mm'
    WIDTH_PER_TOKEN = Coord.Dim(1.0 / 1000.0, COMMON_UNITS)
    WIDTH_MINIMUM = Coord.Dim(5, COMMON_UNITS)
    FILE_DEPTH = Coord.Dim(32.0, COMMON_UNITS)
    SPACE_PARENT_CHILD = Coord.Dim(16.0, COMMON_UNITS)
    FILE_PADDING = Coord.Pad(Coord.Dim(4.0, COMMON_UNITS), Coord.Dim(2.0, COMMON_UNITS), Coord.Dim(16.0, COMMON_UNITS), Coord.Dim(16.0, COMMON_UNITS))
    ATTRS_LINE_ROOT_CHILDREN_JOIN = {'stroke-width': '8', 
       'stroke': 'lightgrey'}
    ATTRS_NODE_NORMAL = {'fill': 'mistyrose', 
       'stroke': 'black', 
       'stroke-width': '1'}
    ATTRS_NODE_MT = {'fill': 'aqua', 
       'stroke': 'black', 
       'stroke-width': '1'}
    ATTRS_NODE_CONDITIONAL = {'fill': 'salmon', 
       'stroke': 'black', 
       'stroke-width': '1'}
    ATTRS_LINE_NORMAL_TO = {'stroke-width': '2', 
       'stroke': 'black'}
    ATTRS_LINE_NORMAL_FROM = {'stroke-width': '0.5', 
       'stroke': 'black'}
    ATTRS_LINE_MT_TO = {'stroke-width': '2', 
       'stroke': 'aqua', 
       'stroke-dasharray': '8,8'}
    ATTRS_LINE_MT_FROM = {'stroke-width': '0.5', 
       'stroke': 'aqua', 
       'stroke-dasharray': '8,8'}
    ATTRS_LINE_CONDITIONAL_TO = {'stroke-width': '0.5', 
       'stroke': 'black', 
       'stroke-dasharray': '8,2,2,2'}
    ATTRS_LINE_CONDITIONAL_FROM = {'stroke-width': '0.25', 
       'stroke': 'black', 
       'stroke-dasharray': '8,2,2,2'}
    STYLE_VERDANA_12 = 'text.V12'
    CLASS_VERDANA_12 = 'V12'
    ATTRS_VERDANA_12 = {'dominant-baseline': 'middle', 
       'font-family': 'Verdana', 
       'font-size': '12', 
       'text-anchor': 'middle', 
       'text-decoration': 'underline'}
    STYLE_VERDANA_9 = 'text.V9'
    CLASS_VERDANA_9 = 'V9'
    ATTRS_VERDANA_9 = {'dominant-baseline': 'middle', 
       'font-family': 'Verdana', 
       'font-size': '9'}
    STYLE_TEXT_SCALE = 'text.scale'
    CLASS_TEXT_SCALE = 'scale'
    ATTRS_TEXT_SCALE = {'dominant-baseline': 'middle', 
       'font-family': 'Verdana', 
       'font-size': '12', 
       'text-anchor': 'left'}
    STYLE_COURIER_10 = 'text.C10'
    CLASS_COURIER_10 = 'C10'
    ATTRS_COURIER_10 = {'font-family': 'Courier', 
       'font-size': '10', 
       'font-weight': '10'}
    STYLE_RECT_INVIS = 'rect.invis'
    CLASS_RECT_INVIS = 'invis'
    ATTRS_RECT_INVIS = {'fill': 'red', 
       'opacity': '0', 
       'stroke': 'black', 
       'stroke-width': '1'}
    CHEVRON_COLOUR_FILL = 'palegreen'
    CHEVRON_COLOUR_STROKE = 'black'
    CHEVRON_STROKE_WIDTH = '.5'
    HIST_DEPTH = Coord.Dim(4.0, COMMON_UNITS)
    HIST_PP_TOKEN_TYPES_COLOURS = (
     ('header-name', 'orange'),
     ('identifier', 'blue'),
     ('string-literal', 'cyan'),
     ('pp-number', 'green'),
     ('character-literal', 'magenta'),
     ('preprocessing-op-or-punc', 'red'),
     ('non-whitespace', 'black'),
     ('concat', 'yellow'),
     ('whitespace', 'white'))
    HIST_RECT_COLOUR_STROKE = 'black'
    HIST_RECT_STROKE_WIDTH = '.5'
    HIST_LEGEND_ID = 'HistogramLegend'
    POPUP_TEXT = ' ? '

    def __init__(self, theFig, theLineNum):
        super(SVGTreeNodeMain, self).__init__(theFig, theLineNum)
        self._tokenCounterChildren = PpTokenCount.PpTokenCount()
        self._numChildSigTokens = 0
        self._bb = PlotNode.PlotNodeBboxBoxy()
        if theFig is None:
            self._dataMap = None
        else:
            self._dataMap = {}
            self._dataMap['numToks'] = theFig.numTokens
            self._dataMap['condComp'] = theFig.condComp
            self._dataMap['tokenCntr'] = theFig.tokenCounter
            self._dataMap['findLogic'] = theFig.findLogic
        self._triggerS = []
        self._numPassesToPlotSelf = 2
        return

    @property
    def tokenCounter(self):
        """This is the PpTokenCount.PpTokenCount() for me only."""
        if self.isRoot:
            return PpTokenCount.PpTokenCount()
        return self._dataMap['tokenCntr']

    @property
    def tokenCounterChildren(self):
        """This is the computed PpTokenCount.PpTokenCount() for all my descendents."""
        return self._tokenCounterChildren

    @property
    def tokenCounterTotal(self):
        """This is the computed PpTokenCount.PpTokenCount() me plus my descendents."""
        retVal = PpTokenCount.PpTokenCount()
        retVal += self.tokenCounter
        retVal += self.tokenCounterChildren
        return retVal

    @property
    def condComp(self):
        """A string of conditional tests."""
        assert not self.isRoot
        return self._dataMap['condComp']

    @property
    def findLogic(self):
        """The find logic as a string."""
        assert not self.isRoot
        return self._dataMap['findLogic']

    def finalise(self):
        """Finalisation this sets up all the bounding boxes of me and my children."""
        for aChild in self._children:
            aChild.finalise()

        self._tokenCounterChildren = PpTokenCount.PpTokenCount()
        self._numChildSigTokens = 0
        for aChild in self._children:
            self._bb.extendChildBbox(aChild.bb.bbSigma)
            self._tokenCounterChildren += aChild.tokenCounterTotal
            self._numChildSigTokens += aChild.tokenCounterTotal.tokenCountNonWs(isAll=False)

        if not self.isRoot:
            self._bb.width = self.WIDTH_MINIMUM + self.WIDTH_PER_TOKEN.scale(self.tokenCounterTotal.tokenCountNonWs(isAll=False))
            self._bb.depth = self.FILE_DEPTH
            self._bb.bbSelfPadding = self.FILE_PADDING
            if len(self._children) > 0:
                self._bb.bbSpaceChildren = self.SPACE_PARENT_CHILD

    def writePreamble(self, theS):
        """Write any preamble such as CSS or JavaScript.
        To be implemented by child classes."""
        cssDict = {'tspan': {'white-space': 'pre'}, self.STYLE_VERDANA_12: self.ATTRS_VERDANA_12, 
           self.STYLE_VERDANA_9: self.ATTRS_VERDANA_9, 
           self.STYLE_COURIER_10: self.ATTRS_COURIER_10, 
           self.STYLE_TEXT_SCALE: self.ATTRS_TEXT_SCALE, 
           self.STYLE_RECT_INVIS: self.ATTRS_RECT_INVIS}
        with XmlWrite.Element(theS, 'defs', {}):
            theS.writeCSS(cssDict)
        self._writeECMAScript(theS)
        self._writeScaleControls(theS)

    def _writeScaleControls(self, theSvg):
        """Write the text elements that control re-scaling."""
        myAttrs = {'class': self.CLASS_TEXT_SCALE}
        myPointP = Coord.Pt(Coord.Dim(8.0, self.COMMON_UNITS), Coord.Dim(4.0, self.COMMON_UNITS))
        with SVGWriter.SVGGroup(theSvg, {'id': 'scaleGroup'}):
            with SVGWriter.SVGText(theSvg, myPointP, None, None, myAttrs):
                theSvg.characters('Select scale (bold selected):')
            myAttrs['text-decoration'] = 'underline'
            myPointP = Coord.newPt(myPointP, incX=Coord.Dim(64, 'mm'), incY=None)
            for scale in self.SCALE_FACTORS:
                myAttrs['onclick'] = "scaleGraphic(%s, '%s')" % (scale, scale)
                myAttrs['id'] = str(scale)
                if scale == self._scale:
                    myAttrs['font-weight'] = 'bold'
                else:
                    myAttrs['font-weight'] = 'normal'
                text = '%d%%' % int(scale * 100)
                with SVGWriter.SVGText(theSvg, myPointP, None, None, myAttrs):
                    theSvg.characters(text)
                myPointP = Coord.newPt(myPointP, incX=Coord.Dim(5 * len(text), 'mm'), incY=None)

        return

    def plotInitialise(self, theSvg, theDatumL, theTpt):
        """Plot the histogram legend once only."""
        self.commentFunctionBegin(theSvg)
        self.commentFunctionEnd(theSvg)

    def plotFinalise(self, theSvg, theDatumL, theTpt):
        """Finish the plot. In this case we write the text overlays."""
        self.commentFunctionBegin(theSvg, File=self._fileName)
        self._writeTriggers(theSvg)
        self.commentFunctionEnd(theSvg, File=self._fileName)

    def _writeTriggers(self, theSvg):
        """Write the rectangles that trigger pop-up text last so that they are on top."""
        for aChild in self._children:
            aChild._writeTriggers(theSvg)

        for _pt, _box, _attrs in self._triggerS:
            with SVGWriter.SVGRect(theSvg, _pt, _box, _attrs):
                pass

    def _plotSelf(self, theSvg, theDatumL, theTpt, thePassNum, idStack):
        """Plot me to a stream at the logical datum point"""
        assert not self.isRoot
        if thePassNum == 0:
            self.commentFunctionBegin(theSvg, File=self._fileName, Node=self.nodeName, Pass=thePassNum)
            if self.condCompState:
                if self.numTokens > 0:
                    myAttrs = self.ATTRS_NODE_NORMAL
                else:
                    myAttrs = self.ATTRS_NODE_MT
            else:
                myAttrs = self.ATTRS_NODE_CONDITIONAL
            if self._bb.hasSetArea:
                myBoxDatumP = theTpt.boxDatumP(self._bb.plotPointSelf(theDatumL), self._bb.box)
                with SVGWriter.SVGRect(theSvg, myBoxDatumP, theTpt.boxP(self._bb.box), myAttrs):
                    pass
            self._plotSelfInternals(theSvg, theDatumL, theTpt)
        elif thePassNum == 1:
            self._plotTextOverlay(theSvg, theDatumL, theTpt, idStack)
        self.commentFunctionEnd(theSvg, File=self._fileName, Node=self.nodeName, Pass=thePassNum)

    def plotRoot(self, theSvg, theDatumL, theTpt, passNum):
        if passNum == 1:
            self._plotHistogramLegend(theSvg, theTpt)

    def _plotSelfToChildren(self, theSvg, theDatumL, theTpt):
        """Plot links from me to my children to a stream at the
        (self) logical datum point."""
        assert len(self._children) > 0
        assert not self.isRoot
        myDatumL = self._bb.plotPointSelf(theDatumL)
        for i, datumChildL in self._enumerateChildren(theDatumL, theTpt):
            if self._children[i].condCompState:
                if self._children[i].numTokens > 0:
                    myAttrsTo = self.ATTRS_LINE_NORMAL_TO
                    myAttrsFrom = self.ATTRS_LINE_NORMAL_FROM
                else:
                    myAttrsTo = self.ATTRS_LINE_MT_TO
                    myAttrsFrom = self.ATTRS_LINE_MT_FROM
            else:
                myAttrsTo = self.ATTRS_LINE_CONDITIONAL_TO
                myAttrsFrom = self.ATTRS_LINE_CONDITIONAL_FROM
            if theTpt.positiveSweepDir:
                childOrd = len(self._children) - i - 1
            else:
                childOrd = i
            linePtsFirst = [ theTpt.pt(l) for l in (
             self._bb.pcRoll(myDatumL, childOrd),
             self._bb.pcTo(myDatumL, childOrd),
             self._children[i].bb.pcLand(datumChildL),
             self._children[i].bb.pcStop(datumChildL))
                           ]
            linePtsSecond = [ theTpt.pt(l) for l in (
             self._children[i].bb.cpRoll(datumChildL),
             self._children[i].bb.cpTo(datumChildL),
             self._bb.cpLand(myDatumL, childOrd),
             self._bb.cpStop(myDatumL, childOrd))
                            ]
            if theTpt.positiveSweepDir:
                linePtsSecond, linePtsFirst = linePtsFirst, linePtsSecond
            j = 1
            while j < len(linePtsFirst):
                with SVGWriter.SVGLine(theSvg, linePtsFirst[(j - 1)], linePtsFirst[j], myAttrsTo):
                    pass
                j += 1

            j = 1
            while j < len(linePtsSecond):
                with SVGWriter.SVGLine(theSvg, linePtsSecond[(j - 1)], linePtsSecond[j], myAttrsFrom):
                    pass
                j += 1

    def _plotRootChildToChild(self, theSvg, theDatumL, theTpt):
        """Join up children of root node with vertical lines."""
        assert len(self._children) > 0
        assert self.isRoot
        self.commentFunctionBegin(theSvg)
        ptNextL = None
        for i, datumChildL in self._enumerateChildren(theDatumL, theTpt):
            if i > 0:
                ptPrevL = theTpt.prevdcL(self._children[i].bb.plotPointSelf(datumChildL), self._children[i].bb.box)
                with SVGWriter.SVGLine(theSvg, theTpt.pt(ptNextL), theTpt.pt(ptPrevL), self.ATTRS_LINE_ROOT_CHILDREN_JOIN):
                    pass
            ptNextL = theTpt.nextdcL(self._children[i].bb.plotPointSelf(datumChildL), self._children[i].bb.box)

        self.commentFunctionEnd(theSvg)
        return

    def _plotSelfInternals(self, theSvg, theDl, theTpt):
        """Plot structures inside the box and the static text that is
        the file name."""
        if self.__mustPlotSelfHistogram():
            myHistDl = self._bb.plotPointSelf(theDl)
            self._plotHistogram(theSvg, myHistDl, theTpt, self.tokenCounter)
            if self.__mustPlotChildHistogram():
                myHistDl = Coord.newPt(myHistDl, None, self.HIST_DEPTH)
                self._plotHistogram(theSvg, myHistDl, theTpt, self._tokenCounterChildren)
        self._plotChevron(theSvg, theDl, theTpt)
        if not self.isRoot:
            self._plotFileName(theSvg, theDl, theTpt)
        return

    def _plotTextOverlay(self, theSvg, theDatumL, theTpt, idStack):
        """Plots all the text associated with the parent and child.
        We write the hidden objects first then the visible objects. This is
        because the hidden objects are controlled onmouseover/onmouseout on
        the visible objects and they have to be later in the SVG file for this
        to work."""
        self.commentFunctionBegin(theSvg, File=self._fileName, Node=self.nodeName)
        if len(self._children) > 0 and not self.isRoot:
            self._plotTextOverlayChildren(theSvg, theDatumL, theTpt)
        if self.__mustPlotSelfHistogram():
            myHistDl = self._bb.plotPointSelf(theDatumL)
            self._plotTextOverlayHistogram(theSvg, myHistDl, theTpt)
            if self.__mustPlotChildHistogram():
                myHistDl = Coord.newPt(myHistDl, None, self.HIST_DEPTH)
                self._plotTextOverlayHistogram(theSvg, myHistDl, theTpt)
        if not self.isRoot:
            self._plotTextOverlayTokenCountTable(theSvg, theDatumL, theTpt)
            self._plotFileNameStackPopup(theSvg, theDatumL, theTpt, idStack)
        self.commentFunctionEnd(theSvg, File=self._fileName, Node=self.nodeName)
        return

    def _plotTextOverlayChildren(self, theSvg, theDatumL, theTpt):
        """Plot text associated with my children to a stream at the
        (self) logical datum point."""
        assert len(self._children) > 0
        assert not self.isRoot
        self.commentFunctionBegin(theSvg, File=self._fileName)
        for i, datumChildL in self._enumerateChildren(theDatumL, theTpt):
            self._plotWhereWhyHow(theSvg, i, datumChildL, theTpt)

        self.commentFunctionEnd(theSvg, File=self._fileName)

    def _plotWhereWhyHow(self, theSvg, iChild, theDatumL, theTpt):
        """Plot description of Where/Why/How inclusion of a single child to a
        stream at the (self) logical datum point."""
        assert not self.isRoot
        assert len(self._children) > 0
        assert iChild >= 0 and iChild < len(self._children)
        self.commentFunctionBegin(theSvg, File=self._fileName)
        myDatumL = self._children[iChild].bb.plotPointSelf(theDatumL)
        myAltTxtPointP = theTpt.pt(Coord.newPt(myDatumL, incX=self._children[iChild].bb.width.scale(0.5), incY=self.FILE_PADDING.parent.scale(-0.5)))
        altTextS = []
        altTextS.append('Where: %s#%d ' % (
         self.nodeName, self._children[iChild].lineNum))
        if len(self._children[iChild].condComp) > 0:
            assert self._children[iChild].condCompState
            altTextS.append('  Why: %s ' % self._children[iChild].condComp)
        else:
            altTextS.append('  Why: %s ' % str(self._children[iChild].condCompState))
        altTextS.append('  How: #include %s' % (', ').join(self._children[iChild].findLogic))
        triggerBoxP = theTpt.boxP(Coord.Box(self._children[iChild].bb.width, self.FILE_PADDING.parent))
        triggerPointP = theTpt.pt(Coord.newPt(myDatumL, incX=self._children[iChild].bb.width, incY=self.FILE_PADDING.parent.scale(-1.0)))
        self.writeAltTextAndMouseOverRect(theSvg, theSvg.id, myAltTxtPointP, altTextS, triggerPointP, triggerBoxP)
        self.commentFunctionEnd(theSvg, File=self._fileName)

    def _plotTextOverlayHistogram(self, theSvg, theHistDl, theTpt):
        """Plot the text associated with a histogram."""
        myCentreL = Coord.newPt(theHistDl, self._bb.width.scale(0.5), self.HIST_DEPTH.scale(0.5))
        myPointP = theTpt.pt(myCentreL)
        myAttrs = {'class': self.CLASS_RECT_INVIS, 
           'onmouseover': 'showHistogram(%s, %s)' % (
                         myPointP.x.value + 3, myPointP.y.value + 2), 
           'onmouseout': 'hideHistogram()'}
        myWidth = self._bb.width
        myBox = Coord.Box(myWidth, self.HIST_DEPTH)
        with SVGWriter.SVGRect(theSvg, theTpt.boxDatumP(theHistDl, myBox), theTpt.boxP(myBox), myAttrs):
            pass

    def _fileNamePoint(self, theDatumL, theTpt):
        """Returns the point to plot the file name or None."""
        if self._bb.hasSetArea:
            myDatumL = self._bb.plotPointSelf(theDatumL)
            textPointL = theTpt.tdcL(myDatumL, self._bb.box)
            textPointL = Coord.newPt(textPointL, incX=self.FILE_PADDING.prev.scale(0.5), incY=None)
            return theTpt.pt(textPointL)
        else:
            return

    def _fileIdStackToListOfStr(self, theIdStack):
        """Given a list of alternating file names and line numbers such as:
        ['root', 3, foo.h, 7, bar.h] this returns a list of strings thus:
        ['root#3, 'foo.h#7, 'bar.h']"""
        myAltS = []
        i = 0
        while i < len(theIdStack):
            if i + 1 < len(theIdStack):
                myAltS.append('%s#%d' % (theIdStack[i], theIdStack[(i + 1)]))
            else:
                myAltS.append(theIdStack[i])
            i += 2

        return myAltS

    def _plotFileName(self, theSvg, theDatumL, theTpt):
        """Writes out the file name adjacent to the file box as static text."""
        self.commentFunctionBegin(theSvg, File=self._fileName)
        if self._bb.hasSetArea:
            textPointP = self._fileNamePoint(theDatumL, theTpt)
            assert textPointP is not None
            myAttrs = {'class': self.CLASS_VERDANA_12, 
               'opacity': '1.0'}
            with SVGWriter.SVGText(theSvg, textPointP, None, None, myAttrs):
                theSvg.characters(os.path.basename(self.nodeName))
        self.commentFunctionEnd(theSvg, File=self._fileName)
        return

    def _plotFileNameStackPopup(self, theSvg, theDatumL, theTpt, idStack):
        """Writes out the file name at the top with a pop-up with the
        absolute path."""
        self.commentFunctionBegin(theSvg, File=self._fileName)
        if self._bb.hasSetArea:
            textPointP = self._fileNamePoint(theDatumL, theTpt)
            assert textPointP is not None
            triggerBoxP = Coord.Box(Coord.baseUnitsDim(12 * len(os.path.basename(self.nodeName))), Coord.baseUnitsDim(14))
            triggerPointP = Coord.newPt(textPointP, triggerBoxP.width.scale(-0.5), triggerBoxP.depth.scale(-0.5))
            self.writeAltTextAndMouseOverRect(theSvg, theSvg.id, textPointP, self._fileIdStackToListOfStr(idStack), triggerPointP, triggerBoxP)
        self.commentFunctionEnd(theSvg, File=self._fileName)
        return

    def _plotTextOverlayTokenCountTable(self, theSvg, theDatumL, theTpt):
        """Plots the token count table as text+alternate text."""
        assert not self.isRoot
        self.commentFunctionBegin(theSvg, File=self._fileName)
        myDatumL = self._bb.plotPointSelf(theDatumL)
        myDatumL = Coord.newPt(myDatumL, incX=self._bb.width, incY=None)
        triggerBoxL = self._bb.box
        if self.__mustPlotSelfHistogram():
            myDatumL = Coord.newPt(myDatumL, None, self.HIST_DEPTH)
            triggerBoxL = Coord.Box(triggerBoxL.width, triggerBoxL.depth - self.HIST_DEPTH)
            if self.__mustPlotChildHistogram():
                myDatumL = Coord.newPt(myDatumL, None, self.HIST_DEPTH)
                triggerBoxL = Coord.Box(triggerBoxL.width, triggerBoxL.depth - self.HIST_DEPTH)
        myDatumP = theTpt.pt(myDatumL)
        altTextS = self._altTextsForTokenCount()
        self.writeAltTextAndMouseOverRect(theSvg, theSvg.id, myDatumP, altTextS, myDatumP, theTpt.boxP(triggerBoxL))
        self.commentFunctionEnd(theSvg, File=self._fileName)
        return

    def _altTextsForTokenCount(self):
        """Returns a list of strings that are the alternate text for token counts."""
        assert not self.isRoot
        if len(self._children) > 0:
            myCounterTotal = PpTokenCount.PpTokenCount()
            myCounterTotal += self.tokenCounter
            myCounterTotal += self.tokenCounterChildren
        FIELD_WIDTH = 7
        myTokTypeS = [ t[0] for t in self.HIST_PP_TOKEN_TYPES_COLOURS ]
        typeLen = max([ len(t) for t in myTokTypeS ])
        altTextS = []
        if len(self._children) > 0:
            altTextS.append('%*s %*s [%*s] %*s [%*s] %*s [%*s]' % (
             typeLen,
             'Type',
             FIELD_WIDTH,
             'Me',
             FIELD_WIDTH,
             'Me',
             FIELD_WIDTH,
             'Child',
             FIELD_WIDTH,
             'Child',
             FIELD_WIDTH,
             'All',
             FIELD_WIDTH,
             'All'))
        else:
            altTextS.append('%*s %*s [%*s]' % (
             typeLen,
             'Type',
             FIELD_WIDTH,
             'Me',
             FIELD_WIDTH,
             'Me'))
        cntrTotalS = [
         0] * 6
        for t in myTokTypeS:
            cntrTotalS[0] += self.tokenCounter.tokenCount(t, isAll=True)
            cntrTotalS[1] += self.tokenCounter.tokenCount(t, isAll=False)
            line = '%*s %*d [%*d]' % (
             typeLen,
             t,
             FIELD_WIDTH,
             self.tokenCounter.tokenCount(t, isAll=True),
             FIELD_WIDTH,
             self.tokenCounter.tokenCount(t, isAll=False))
            if len(self._children) > 0:
                line += ' %*d [%*d] %*d [%*d]' % (
                 FIELD_WIDTH,
                 self.tokenCounterChildren.tokenCount(t, isAll=True),
                 FIELD_WIDTH,
                 self.tokenCounterChildren.tokenCount(t, isAll=False),
                 FIELD_WIDTH,
                 myCounterTotal.tokenCount(t, isAll=True),
                 FIELD_WIDTH,
                 myCounterTotal.tokenCount(t, isAll=False))
                cntrTotalS[2] += self.tokenCounterChildren.tokenCount(t, isAll=True)
                cntrTotalS[3] += self.tokenCounterChildren.tokenCount(t, isAll=False)
                cntrTotalS[4] += myCounterTotal.tokenCount(t, isAll=True)
                cntrTotalS[5] += myCounterTotal.tokenCount(t, isAll=False)
            altTextS.append(line)

        line = '%*s %*d [%*d]' % (
         typeLen,
         'Total',
         FIELD_WIDTH,
         cntrTotalS[0],
         FIELD_WIDTH,
         cntrTotalS[1])
        if len(self._children) > 0:
            line += ' %*d [%*d] %*d [%*d]' % (
             FIELD_WIDTH,
             cntrTotalS[2],
             FIELD_WIDTH,
             cntrTotalS[3],
             FIELD_WIDTH,
             cntrTotalS[4],
             FIELD_WIDTH,
             cntrTotalS[5])
        altTextS.append(line)
        return altTextS

    def __mustPlotSelfHistogram(self):
        return self.tokenCounter.tokenCountNonWs(isAll=False) > 0

    def __mustPlotChildHistogram(self):
        return self.__mustPlotSelfHistogram() and len(self._children) > 0 and self._numChildSigTokens > 0

    def _plotHistogram(self, theSvg, theHistDl, theTpt, theTokCounter):
        myTokCountTotal = theTokCounter.totalAllUnconditional
        assert theTokCounter.tokenCountNonWs(isAll=False) > 0
        assert myTokCountTotal > 0
        myHistDl = theHistDl
        for k, myFill in self.HIST_PP_TOKEN_TYPES_COLOURS:
            tCount = theTokCounter.tokenCount(k, isAll=False)
            if tCount > 0:
                myWidth = self._bb.width.scale(tCount / (1.0 * myTokCountTotal))
                myBox = Coord.Box(myWidth, self.HIST_DEPTH)
                with SVGWriter.SVGRect(theSvg, theTpt.boxDatumP(myHistDl, myBox), theTpt.boxP(myBox), {'fill': myFill, 
                   'stroke': self.HIST_RECT_COLOUR_STROKE, 
                   'stroke-width': self.HIST_RECT_STROKE_WIDTH}):
                    pass
                myHistDl = Coord.newPt(myHistDl, incX=myWidth, incY=None)

        return

    def _plotHistogramLegend(self, theSvg, theTpt):
        """Plot a standardised legend. This is plotted as a group within a defs."""
        myDatumP = Coord.Pt(Coord.Dim(0.0, self.COMMON_UNITS), Coord.Dim(0.0, self.COMMON_UNITS))
        with SVGWriter.SVGGroup(theSvg, {'id': self.HIST_LEGEND_ID, 'opacity': '0.0'}):
            idVal = 0
            with SVGWriter.SVGRect(theSvg, myDatumP, Coord.Box(Coord.Dim(48.0, self.COMMON_UNITS), Coord.Dim(40.0, self.COMMON_UNITS)), {'fill': self.ALT_RECT_FILL, 
               'id': '%d' % idVal}):
                idVal += 2
            myDatumP = Coord.newPt(myDatumP, incX=Coord.Dim(2.0, self.COMMON_UNITS), incY=Coord.Dim(2.0, self.COMMON_UNITS))
            myTokIdxS = list(range(len(self.HIST_PP_TOKEN_TYPES_COLOURS)))
            if theTpt.positiveSweepDir:
                myTokIdxS.reverse()
            for iC in myTokIdxS:
                myBox = Coord.Box(self.HIST_DEPTH, self.HIST_DEPTH)
                with SVGWriter.SVGRect(theSvg, myDatumP, myBox, {'fill': self.HIST_PP_TOKEN_TYPES_COLOURS[iC][1], 
                   'stroke': self.HIST_RECT_COLOUR_STROKE, 
                   'stroke-width': self.HIST_RECT_STROKE_WIDTH, 
                   'id': '%d' % idVal}):
                    idVal += 2
                myTextDatumP = Coord.newPt(myDatumP, incX=self.HIST_DEPTH + Coord.Dim(2.0, self.COMMON_UNITS), incY=self.HIST_DEPTH.scale(0.5))
                with SVGWriter.SVGText(theSvg, myTextDatumP, None, None, {'font-family': 'Verdana', 
                   'font-size': '10', 
                   'dominant-baseline': 'middle', 
                   'id': '%d' % idVal}):
                    theSvg.characters(self.HIST_PP_TOKEN_TYPES_COLOURS[iC][0])
                    idVal += 2
                myDatumP = Coord.newPt(myDatumP, incX=None, incY=self.HIST_DEPTH)

        return

    def _plotChevron(self, theSvg, theDl, theTpt):
        r"""Plots a wedge to represent the relative number of tokens in me and
        my children.
        D------------------.------------------|
        |                                     |
        |------------------.------------------|
        |                                     |
        A-----------B------.------D-----------|
        |            \     .     /            |
        |             \    .    /             |
        |              \   .   /              |
        |               \  .  /               |
        |                \ . /                |
        ------------------\C/------------------
        We plot in the order D moveto A moveto B lineto C lineto D lineto B
        """
        mySelfTokCount = self.tokenCounter.tokenCountNonWs(isAll=False)
        if mySelfTokCount == 0 and self._numChildSigTokens == 0:
            return
        else:
            myDl = self._bb.plotPointSelf(theDl)
            myPtC = Coord.newPt(myDl, self._bb.width.scale(0.5), self._bb.depth)
            if self.__mustPlotSelfHistogram():
                myDl = Coord.newPt(myDl, None, self.HIST_DEPTH)
            if self.__mustPlotChildHistogram():
                myDl = Coord.newPt(myDl, None, self.HIST_DEPTH)
            if self._numChildSigTokens == 0:
                polyLogicalPtS = [
                 myDl,
                 myPtC,
                 Coord.newPt(myDl, self._bb.width, None)]
            else:
                ratioChevron = 1.0 * mySelfTokCount / (self._numChildSigTokens + mySelfTokCount)
                myChevronOffset = self._bb.width.scale(0.5 * ratioChevron)
                myDl = Coord.newPt(myDl, self._bb.width.scale(0.5) - myChevronOffset, None)
                polyLogicalPtS = [
                 myDl,
                 myPtC,
                 Coord.newPt(myDl, myChevronOffset.scale(2.0), None)]
            polyPhysicalPtS = [ theTpt.pt(p) for p in polyLogicalPtS ]
            j = 1
            while j < len(polyPhysicalPtS):
                with SVGWriter.SVGLine(theSvg, polyPhysicalPtS[(j - 1)], polyPhysicalPtS[j], {'stroke-width': '2', 
                   'stroke': 'black'}):
                    pass
                j += 1

            return

    def writeAltTextAndMouseOverRect(self, theSvg, theId, theAltPt, theAltS, theTrigPt, theTrigRect):
        """Composes and writes the (pop-up) alternate text.
        Also writes a trigger rectangle."""
        with SVGWriter.SVGGroup(theSvg, {'id': 't%s%s' % (theId, self.ALT_ID_SUFFIX), 'opacity': '0.0'}):
            altFontSize = self.ALT_FONT_PROPERTIES[self.ALT_FONT_FAMILY]['size']
            altFontLenFactor = self.ALT_FONT_PROPERTIES[self.ALT_FONT_FAMILY]['lenFactor']
            altFontHeightFactor = self.ALT_FONT_PROPERTIES[self.ALT_FONT_FAMILY]['heightFactor']
            maxChars = max([ len(s) for s in theAltS ])
            boxWidth = Coord.Dim(altFontSize * maxChars * altFontLenFactor, 'pt')
            if len(theAltS) < 2:
                boxHeight = Coord.Dim(altFontSize * 2, 'pt')
            else:
                boxHeight = Coord.Dim(altFontSize * len(theAltS) * altFontHeightFactor, 'pt')
            boxAttrs = {'fill': self.ALT_RECT_FILL}
            with SVGWriter.SVGRect(theSvg, theAltPt, Coord.Box(boxWidth, boxHeight), boxAttrs):
                pass
            myAltTextPt = Coord.newPt(theAltPt, incX=Coord.Dim(1 * altFontSize * 3 * altFontLenFactor / 2.0, 'pt'), incY=Coord.Dim(12, 'pt'))
            with SVGWriter.SVGText(theSvg, myAltTextPt, 'Courier', altFontSize, {'font-weight': 'normal'}):
                self._writeStringListToTspan(theSvg, myAltTextPt, theAltS)
        boxAttrs = {'class': self.CLASS_RECT_INVIS, 'id': 't%s' % theId, 
           'onmouseover': "swapOpacity('t%s', 't%s')" % (
                         theId, theId + self.ALT_ID_SUFFIX), 
           'onmouseout': "swapOpacity('t%s', 't%s')" % (
                        theId, theId + self.ALT_ID_SUFFIX)}
        self._triggerS.append((theTrigPt, theTrigRect, boxAttrs))