# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/IncGraphSVGBase.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Provides basic functionality to take the #include graph of a preprocessed\nfile and plots it as a diagram in SVG.\n\nEvent handlers for onmouseover/onmouseout\n-----------------------------------------\n\nWe would like to have more detailed information available to the user when they\nmouseover an object on the SVG image. After a lot of experiment the most cross\nbrowser way this is done by providing an event handler to switch the opacity of\nan element between 0 and 1. See :py:meth:`IncGraphSVG.writeAltTextAndMouseOverRect`.\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import sys, inspect, pprint, cpip
from cpip.core import FileIncludeGraph
from cpip.util import XmlWrite
from cpip.plot import Coord
from cpip.plot import SVGWriter
from cpip.plot import TreePlotTransform
CANVAS_PADDING = Coord.Pad(Coord.Dim(4.0, 'mm'), Coord.Dim(4.0, 'mm'), Coord.Dim(4.0, 'mm'), Coord.Dim(4.0, 'mm'))

def processIncGraphToSvg(theLex, theFilePath, theClass, tptPos, tptSweep):
    """Convert a Include graph from a PpLexer to SVG in theFilePath."""
    myVis = FileIncludeGraph.FigVisitorTree(theClass)
    theLex.fileIncludeGraphRoot.acceptVisitor(myVis)
    myIgs = myVis.tree()
    myWidth = CANVAS_PADDING.prev + myIgs.plotCanvas.width + CANVAS_PADDING.next
    myDepth = CANVAS_PADDING.parent + myIgs.plotCanvas.depth + CANVAS_PADDING.child
    myWidth = Coord.Dim(int(myWidth.value + 0.5), myWidth.units)
    myDepth = Coord.Dim(int(myDepth.value + 0.5), myDepth.units)
    myCanvas = Coord.Box(myWidth, myDepth)
    myTpt = TreePlotTransform.TreePlotTransform(myCanvas, tptPos, tptSweep)
    myIgs.plotToFilePath(theFilePath, myTpt)


class SVGTreeNodeBase(FileIncludeGraph.FigVisitorTreeNodeBase):
    COMMON_UNITS = 'mm'
    UNNAMED_UNITS = 'px'
    VIEWBOX_SCALE = 8.0
    ALT_RECT_FILL = 'khaki'
    ALT_ID_SUFFIX = '.alt'
    ALT_FONT_FAMILY = 'monospace'
    ALT_FONT_PROPERTIES = {'Courier': {'size': 10, 
                   'lenFactor': 0.5, 
                   'heightFactor': 1.2}, 
       'monospace': {'size': 10, 
                     'lenFactor': 0.5, 
                     'heightFactor': 1.2}}
    NAMESPACE_XLINK = 'http://www.w3.org/1999/xlink'
    SCALE_FACTORS = (0.05, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0)
    SCALE_MAX_Y = Coord.Dim(1000, 'mm')

    def __init__(self, theFig, theLineNum):
        super(SVGTreeNodeBase, self).__init__(theLineNum)
        self._isRoot = theFig is None
        if theFig is None:
            self._fileName = None
            self._numTokens = -1
            self._condCompState = None
        else:
            self._fileName = theFig.fileName
            self._numTokens = theFig.numTokensSig
            self._condCompState = theFig.condCompState
        self._bb = None
        self.TRACE = cpip.SVG_COMMENT_FUNCTIONS
        self._numPassesToPlotSelf = 0
        return

    def dumpToStream(self, theS=sys.stdout, p=''):
        """Debug/trace."""
        theS.write('%sFile: %s\n' % (p, self.nodeName))
        for aLine in str(self.bb).splitlines():
            theS.write('%s%s\n' % (p, aLine))

        for aChild in self._children:
            aChild.dumpToStream(theS, p + '  ')

    def commentFunctionBegin(self, theSvg, **kwargs):
        """Injects a comment into the SVG with the start of the
        executing function name."""
        if self.TRACE:
            theSvg.comment(' %s(): %s %s' % (
             inspect.stack()[1][3], 'BEGIN',
             pprint.pformat(kwargs)), newLine=True)

    def commentFunctionEnd(self, theSvg, **kwargs):
        """Injects a comment into the SVG with the completion of the
        executing function name."""
        if self.TRACE:
            theSvg.comment(' %s(): %s %s' % (
             inspect.stack()[1][3], 'END',
             pprint.pformat(kwargs)), newLine=True)

    @property
    def isRoot(self):
        return self._isRoot

    @property
    def numTokens(self):
        """The number of significant tokens for me only (not including children)."""
        return self._numTokens

    @property
    def nodeName(self):
        """This is the file name or 'Root'."""
        if self.isRoot:
            return 'Root'
        return self._fileName

    @property
    def condCompState(self):
        """True/False if conditionally compiled node."""
        assert not self.isRoot
        return self._condCompState

    @property
    def bb(self):
        """Returns a PlotNode.PlotNodeBboxBoxy() object for this node."""
        assert self._bb is not None
        return self._bb

    @property
    def plotCanvas(self):
        """The logical size of the plot canvas as a Coord.Box()."""
        return self.bb.bbSigma

    def finalise(self):
        """This will be called on finalisation.
        For depth first finalisation the child class should call finalise
        on each child first."""
        raise NotImplementedError('finalise() not implemented')

    def plotToFilePath(self, theFileName, theTpt):
        """Root level call to plot to a SVG file, theTpt is an
        TreePlotTransform object and is used to transform the internal logical
        coordinates to physical plot positions."""
        self.plotToFileObj(open(theFileName, 'w'), theTpt)

    def plotToFileObj(self, theFileObj, theTpt):
        """Root level call to plot to a file object. The SVG stream is
        created here."""
        if self._numPassesToPlotSelf < 1:
            raise ValueError('No self._numPassesToPlotSelf set!')
        myRootAttrs = {'xmlns:xlink': self.NAMESPACE_XLINK}
        canvasY = theTpt.canvasP().depth + Coord.Dim(60, 'mm') + Coord.Dim(8, 'mm')
        myCanvas = Coord.Box(theTpt.canvasP().width + Coord.Dim(60, 'mm'), canvasY)
        yOffsetForScalingText = Coord.Dim(10, 'mm')
        scaleIdx = self.SCALE_FACTORS.index(1)
        assert scaleIdx >= 0
        while scaleIdx > 0 and canvasY > self.SCALE_MAX_Y:
            canvasY = canvasY.scale(0.5)
            scaleIdx -= 1

        self._scale = self.SCALE_FACTORS[scaleIdx]
        with SVGWriter.SVGWriter(theFileObj, myCanvas, myRootAttrs, mustIndent=cpip.INDENT_ML) as (myS):
            myDatum = Coord.Pt(CANVAS_PADDING.prev - yOffsetForScalingText, CANVAS_PADDING.parent)
            self.writePreamble(myS)
            myS.comment(' Root position: %s, Sweep direction: %s canvas=%s datum=%s' % (
             theTpt.rootPos, theTpt.sweepDir, theTpt.canvasP(), myDatum), newLine=True)
            with SVGWriter.SVGGroup(myS, {'transform': 'translate(0, 24)'}):
                with SVGWriter.SVGGroup(myS, {'id': 'graphic', 
                   'transform': 'scale(%s)' % self.SCALE_FACTORS[scaleIdx]}):
                    with SVGWriter.SVGRect(myS, Coord.newPt(Coord.zeroBaseUnitsPt(), incX=None, incY=yOffsetForScalingText), theTpt.canvasP(), {'fill': 'none', 
                       'stroke': 'grey', 
                       'stroke-width': '2'}):
                        pass
                    self.plotInitialise(myS, myDatum, theTpt)
                    for p in range(self._numPassesToPlotSelf):
                        self.plotToSVGStream(myS, myDatum, theTpt, p, [])

                    self.plotFinalise(myS, myDatum, theTpt)
        return

    def writePreamble(self, theS):
        """Write any preamble such as CSS or JavaScript.
        To be implemented by child classes."""
        raise NotImplementedError

    def plotInitialise(self, theSvg, theDatumL, theTpt):
        """Called once immediately before the recursive plotToSVGStream().
        Can be overridden in child classes for specific use."""
        pass

    def plotFinalise(self, theSvg, theDatumL, theTpt):
        """Called once immediately before the plot is closed.
        Can be overridden in child classes for specific use."""
        pass

    def plotToSVGStream(self, theSvg, theDatumL, theTpt, passNum, idStack):
        """Plot me to a stream and my children at the logical datum point,
        this is a recursive call."""
        self.commentFunctionBegin(theSvg, File=self._fileName, Pass=passNum)
        if not self.isRoot:
            if self.lineNum != -1:
                idStack.append(self.lineNum)
            idStack.append(self.nodeName)
        if len(self._children) > 0:
            if passNum == 0:
                if self.isRoot:
                    self._plotRootChildToChild(theSvg, theDatumL, theTpt)
                else:
                    self._plotSelfToChildren(theSvg, theDatumL, theTpt)
            for i, datumChildL in reversed(list(self._enumerateChildren(theDatumL, theTpt))):
                self._children[i].plotToSVGStream(theSvg, datumChildL, theTpt, passNum, idStack)

        if not self.isRoot:
            self._plotSelf(theSvg, theDatumL, theTpt, passNum, idStack)
        else:
            self.plotRoot(theSvg, theDatumL, theTpt, passNum)
        if not self.isRoot:
            if self.lineNum != -1:
                idStack.pop()
            idStack.pop()
        self.commentFunctionEnd(theSvg, File=self._fileName, Pass=passNum)

    def plotRoot(self, theSvg, theDatumL, theTpt, passNum):
        """Call to plot any root node, for example our child class uses this
        to plot the histogram legend before starting on the text."""
        pass

    def _plotSelf(self, theSvg, theDatumL, theTpt, idStack):
        """Plot me to a stream at the logical datum point.
        Must be provided by child classes."""
        raise NotImplementedError('_plotSelf() not implemented')

    def _plotRootChildToChild(self, theSvg, theDatumL, theTpt):
        """In the case of me being root this plots child to child."""
        assert self.isRoot
        raise NotImplementedError('_plotRootChildToChild() not implemented')

    def _plotSelfToChildren(self, theSvg, theDatumL, theTpt):
        """In the case of me being not root this plots me to my children."""
        assert self.isRoot
        raise NotImplementedError('_plotSelfToChildren() not implemented')

    def _enumerateChildren(self, theDatumL, theTpt):
        """Generates a tuple of (index, logical_datum_point) for my children."""
        assert len(self._children) > 0
        datumChildL = theTpt.startChildrenLogicalPos(self._bb.childBboxDatum(theDatumL), self._bb.bbChildren)
        for i, aChild in enumerate(self._children):
            datumChildL = theTpt.preIncChildLogicalPos(datumChildL, aChild.bb.bbSigma)
            yield (i, datumChildL)
            datumChildL = theTpt.postIncChildLogicalPos(datumChildL, aChild.bb.bbSigma)

    def _writeECMAScript(self, theSvg):
        """Writes the ECMA script for pop-up text switching."""
        myScriptS = []
        myScriptS.append('\nfunction swapOpacity(idFrom, idTo) {\n    var svgFrom = document.getElementById(idFrom);\n    var svgTo = document.getElementById(idTo);\n    var attrFrom = svgFrom.getAttribute("opacity");\n    var attrTo = svgTo.getAttribute("opacity");\n    svgTo.setAttributeNS(null, "opacity", attrFrom);\n    svgFrom.setAttributeNS(null, "opacity", attrTo);\n}\n\nfunction setOpacity(id, value) {\n    var svgElem = document.getElementById(id);\n    svgElem.setAttributeNS(null, "opacity", value);\n}\n\n')
        myScriptS.append('\nfunction showHistogram(x, y) {\n    var histElem = document.getElementById("HistogramLegend");\n    // Use the ID to compute the y offset. The x offset is 8.0mm for text,\n    // 2.0mm or 0mm for rect\n    for (var i = 0; i < 38; i += 2) {\n        var elem = histElem.children[i / 2]\n        if (i == 0) {\n            var xOffset = 0;\n        } else if (elem.nodeName == "text") {\n            var xOffset = 8;\n        } else {\n            var xOffset = 2;\n        }\n        elem.setAttributeNS(null, "x", x + xOffset + "mm");\n        elem.setAttributeNS(null, "y", y + i + "mm");\n    }\n    histElem.setAttributeNS(null, "opacity", 1.0);\n}\n \nfunction hideHistogram() {\n    setOpacity("HistogramLegend", 0.0)\n}\n \n')
        myScriptS.append('\nfunction scaleGraphic(scale, theId) {\n    var graphicGroup = document.getElementById("graphic");\n    graphicGroup.setAttributeNS(null, "transform", "scale(" + scale + ")");\n    // Un-bold all then bold the txtId.\n    var scaleGroup = document.getElementById("scaleGroup");\n    for (var i = 0; i < scaleGroup.children.length; ++i) {\n        var elem = scaleGroup.children[i];\n        if (elem.id == theId) {\n            elem.setAttributeNS(null, "font-weight", "bold");\n        } else {\n            elem.setAttributeNS(null, "font-weight", "normal");\n        }\n    }\n}\n')
        theSvg.writeECMAScript(('').join(myScriptS))

    def _writeAlternateText(self, theSvg, thePoint, theId, theText, theAltS, yOffs=Coord.Dim(0, 'pt')):
        """Composes and writes the (pop-up) alternate text.
        thePoint is the physical point to locate both texts."""
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
            with SVGWriter.SVGRect(theSvg, Coord.newPt(thePoint, incX=Coord.Dim(-1 * altFontSize * (1 + len(theText) * altFontLenFactor / 2.0), 'pt'), incY=Coord.Dim(-1 * altFontHeightFactor * altFontSize, 'pt') + yOffs), Coord.Box(boxWidth, boxHeight), boxAttrs):
                pass
            myAltTextPt = Coord.newPt(thePoint, incX=Coord.Dim(-1 * altFontSize * len(theText) * altFontLenFactor / 2.0, 'pt'), incY=yOffs)
            with SVGWriter.SVGText(theSvg, myAltTextPt, 'Courier', altFontSize, {'font-weight': 'normal'}):
                self._writeStringListToTspan(theSvg, myAltTextPt, theAltS)

    def _writeStringListToTspan(self, theSvg, thePointX, theList):
        """Converts a multi-line string to tspan elements in monospaced format.
        theSvg is the SVG stream.
        theAttrs is the attributes of the enclosing <text> element.
        theStr is the string to write.
        
        This writes the tspan elements within an existing text element, thus:
        <text id="original.alt" font-family="Courier" font-size="12" text-anchor="middle" x="250" y="250">
            <tspan xml:space="preserve"> One</tspan>
            <tspan x="250" dy="1em" xml:space="preserve"> Two</tspan>
            <tspan x="250" dy="1em" xml:space="preserve">Three</tspan>
        </text>
        """
        for i, aLine in enumerate(theList):
            elemAttrs = {}
            if i > 0:
                elemAttrs['x'] = SVGWriter.dimToTxt(thePointX.x)
                elemAttrs['dy'] = '1.5em'
            with XmlWrite.Element(theSvg, 'tspan', elemAttrs):
                theSvg.characters(aLine)
                theSvg.characters(' ')