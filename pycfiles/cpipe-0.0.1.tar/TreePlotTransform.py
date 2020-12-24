# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/plot/TreePlotTransform.py
# Compiled at: 2017-10-03 13:07:16
__doc__ = 'Provides a means of re-interpreting the coordinate system when plotting\ntrees so that the the tree root can be top/left/bottom/right and the child\norder plotted anti-clockwise or clockwise.\n\nThis can convert \'logical\' positions into \'physical\' positions. Where a\n\'logical\' position is one with the root of the tree at the top and the\nchild nodes below in left-to-right (i.e. anti-clockwise) order.\nA \'physical\' position is a plot-able position where the root of the tree is\ntop/left/bottom or right and the child nodes are in anti-clockwise or\nclockwise order.\n\nTransforming sizes and positions\n--------------------------------\n\nIf the first suffix is \'l\' this is the "logical" coordinate system.                                \nIf the first suffix is \'p\' this is the "physical" coordinate system.                                \n  \nThen:\n                              \n* ``C`` - The canvas dimension, Cpw is "Canvas physical width"                            \n* ``W`` - Width dimension, physical and logical.                            \n* ``D`` - Depth dimension, physical and logical.                            \n* ``B`` - Box datum position ("top-left"), physical and logical, x and y.                            \n* ``P`` - Arbitrary point, physical and logical, x and y.                            \n                                \nSo this "logical view" of the tree graph (\'top\' and \'-\'):\ni.e. Root(s) is a top and children are written in an anti-clockwise. ::\n\n     ---> x\n     |\n     \\/\n     y\n    \n    <------------------------ Clw ------------------------>\n    |                                  To Parent\n    |                                     |\n    |             Blx, Bly -->*************************\n    |                         *                  |    *\n    Cld                       *                 Dl    *\n    |                         *<-------- Wl -----|--->*\n    |                         *                  |    *\n    |       Plx, Ply ->.      *                  |    *\n    |                         *************************\n    |                             |        |       |\n    |                        To C[0]  To C[c]   To C[C-1]\n\nOr:\n                        \n====== ===    ===    ==    ==    ============== ============== ========== =========\nOrigin Cpw    Cpd    Wp    Dp    Bpx            Bpy            Ppx        Ppy\n====== ===    ===    ==    ==    ============== ============== ========== =========\ntop    Clw    Cld    Wl    Dl    Blx            Bly            Plx        Ply\nleft   Cld    Clw    Dl    Wl    Bly            (Clw-Plx-Wl)   Ply        Clw-Plx\nbottom Clw    Cld    Wl    Dl    (Clw-Plx-Wl)   (Cld-Ply-Dl)   Clw-Plx    Cld-Ply\nright  Cld    Clw    Dl    Wl    (Cld-Ply-Dl)   Blx            Cld-Ply    Plx\n====== ===    ===    ==    ==    ============== ============== ========== =========\n\nNote the diagonal top-right to bottom-left transference between each pair of\ncolumns. That is because with each successive line we are doing a 90 degree\nrotation (anti-clockwise) plus a +ve y translation by Clw (top->left or \nbottom->right) or Cld (left->bottom or right->top).\n\nIncrementing child positions\n----------------------------\n\nMoving from one child to another is done in the following combinations:\n\n========= ====== ======\nOrigin    \'-\'    \'+\'\n========= ====== ======\ntop       right  left\nleft      up     down\nbottom    left   right\nright     down   up\n========= ====== ======\n'
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
from cpip import ExceptionCpip
from . import Coord

class ExceptionTreePlotTransform(ExceptionCpip):
    """Exception class for TreePlotTransform."""


class ExceptionTreePlotTransformRangeCtor(ExceptionTreePlotTransform):
    """Exception class for out of range input on construction."""


class TreePlotTransform(object):
    """Provides a means of re-interpreting the coordinate system when plotting trees.
    
    rootPosition = frozenset(['top', 'bottom', 'left', 'right'])
    default: 'top'

    sweepDirection = frozenset(['+', '-'])
    default: '-'

    Has functionality for interpreting width/depth to actual postions
    given rootPostion.
    """
    RANGE_ROOTPOS = [
     'top', 'left', 'bottom', 'right']
    RANGE_ROOTPOS_INT = range(len(RANGE_ROOTPOS))
    RANGE_SWEEPDIR = [
     '-', '+']
    RANGE_SWEEPDIR_INT = range(len(RANGE_SWEEPDIR))

    def __init__(self, theLogicalCanvas, rootPos='top', sweepDir='-'):
        """Constructor, takes a 'logical' Canvas as a Coord.Box and the orientation."""
        self._clw = theLogicalCanvas.width
        self._cld = theLogicalCanvas.depth
        try:
            self._rootPos = self.RANGE_ROOTPOS.index(rootPos)
        except ValueError:
            raise ExceptionTreePlotTransformRangeCtor('"%s" not in: %s' % (rootPos, self.RANGE_ROOTPOS))

        try:
            self._sweepDir = self.RANGE_SWEEPDIR.index(sweepDir)
        except ValueError:
            raise ExceptionTreePlotTransformRangeCtor('"%s" not in: %s' % (sweepDir, self.RANGE_SWEEPDIR))

    @property
    def rootPos(self):
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        return self.RANGE_ROOTPOS[self._rootPos]

    @property
    def sweepDir(self):
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        return self.RANGE_SWEEPDIR[self._sweepDir]

    @property
    def positiveSweepDir(self):
        """True if positive sweep, false otherwise."""
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        return self.RANGE_SWEEPDIR[self._sweepDir] == '+'

    def genRootPos(self):
        """Yield all possible root positions."""
        for aPos in self.RANGE_ROOTPOS:
            yield aPos

    def genSweepDir(self):
        """Yield all possible root positions."""
        for aDir in self.RANGE_SWEEPDIR:
            yield aDir

    def canvasP(self):
        """Returns a Coord.Box that describes the physical canvass."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        if self._rootPos == 0:
            return Coord.Box(self._clw, self._cld)
        if self._rootPos == 1:
            return Coord.Box(self._cld, self._clw)
        if self._rootPos == 2:
            return Coord.Box(self._clw, self._cld)
        return Coord.Box(self._cld, self._clw)

    def boxP(self, theBl):
        """Given a logical box this returns a Coord.Box that describes the physical box."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        if self._rootPos == 0:
            return Coord.Box(theBl.width, theBl.depth)
        if self._rootPos == 1:
            return Coord.Box(theBl.depth, theBl.width)
        if self._rootPos == 2:
            return Coord.Box(theBl.width, theBl.depth)
        return Coord.Box(theBl.depth, theBl.width)

    def boxDatumP(self, theBlxy, theBl):
        """Given a logical point and logical box this returns a physical
        point that is the box datum ("upper left")."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        if self._rootPos == 0:
            return Coord.Pt(theBlxy.x, theBlxy.y)
        if self._rootPos == 1:
            return Coord.Pt(theBlxy.y, self._clw - theBlxy.x - theBl.width)
        if self._rootPos == 2:
            return Coord.Pt(self._clw - theBlxy.x - theBl.width, self._cld - theBlxy.y - theBl.depth)
        return Coord.Pt(self._cld - theBlxy.y - theBl.depth, theBlxy.x)

    def tdcL(self, theBlxy, theBl):
        """Given a logical datum (logical top left) and a logical box this
        returns logical top dead centre of a box."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        if self._rootPos == 0:
            return Coord.Pt(theBlxy.x + theBl.width.scale(0.5), theBlxy.y)
        if self._rootPos == 1:
            return Coord.Pt(theBlxy.x + theBl.width, theBlxy.y + theBl.depth.scale(0.5))
        if self._rootPos == 2:
            return Coord.Pt(theBlxy.x + theBl.width.scale(0.5), theBlxy.y + theBl.depth)
        return Coord.Pt(theBlxy.x, theBlxy.y + theBl.depth.scale(0.5))

    def bdcL(self, theBlxy, theBl):
        """Given a logical datum (logical top left) and a logical box this
        returns logical bottom dead centre of a box."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        if self._rootPos == 0:
            return Coord.Pt(theBlxy.x + theBl.width.scale(0.5), theBlxy.y + theBl.depth)
        if self._rootPos == 1:
            return Coord.Pt(theBlxy.x, theBlxy.y + theBl.depth.scale(0.5))
        if self._rootPos == 2:
            return Coord.Pt(theBlxy.x + theBl.width.scale(0.5), theBlxy.y)
        return Coord.Pt(theBlxy.x + theBl.width, theBlxy.y + theBl.depth.scale(0.5))

    def prevdcL(self, theBlxy, theBl):
        """Given a logical datum (logical top left) and a logical box this
        returns logical 'previous' dead centre of a box."""
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        if self._sweepDir == 0:
            return Coord.Pt(theBlxy.x, theBlxy.y + theBl.depth.scale(0.5))
        return Coord.Pt(theBlxy.x + theBl.width, theBlxy.y + theBl.depth.scale(0.5))

    def nextdcL(self, theBlxy, theBl):
        """Given a logical datum (logical top left) and a logical box this
        returns logical 'next' dead centre of a box."""
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        if self._sweepDir == 0:
            return Coord.Pt(theBlxy.x + theBl.width, theBlxy.y + theBl.depth.scale(0.5))
        return Coord.Pt(theBlxy.x, theBlxy.y + theBl.depth.scale(0.5))

    def tdcP(self, theBlxy, theBl):
        """Given a logical datum (logical top left) and a logical box this
        returns physical top dead centre of a box."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        return self.pt(self.tdcL(theBlxy, theBl))

    def bdcP(self, theBlxy, theBl):
        """Given a logical datum (logical top left) and a logical box this
        returns physical bottom dead centre of a box."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        return self.pt(self.bdcL(theBlxy, theBl))

    def pt(self, thePt, units=None):
        """Given an arbitrary logical point as a Coord.Pt(), this returns the
        physical point as a Coord.Pt().
        If units is supplied then the return value will be in those units."""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        if self._rootPos == 0:
            retVal = Coord.Pt(thePt.x, thePt.y)
        elif self._rootPos == 1:
            retVal = Coord.Pt(thePt.y, self._clw - thePt.x)
        elif self._rootPos == 2:
            retVal = Coord.Pt(self._clw - thePt.x, self._cld - thePt.y)
        else:
            retVal = Coord.Pt(self._cld - thePt.y, thePt.x)
        if units is not None:
            return retVal.convert(units)
        else:
            return retVal

    def startChildrenLogicalPos(self, thePt, theBox):
        """Returns the starting child logical datum point ('top-left') given
        the children logical datum point and the children.bbSigma.
        Returns a Coord.Pt().
        This takes into account the sweep direction."""
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        if self._sweepDir == 0:
            return thePt
        return Coord.Pt(thePt.x + theBox.width, thePt.y)

    def preIncChildLogicalPos(self, thePt, theBox):
        """Pre-incrempents the child logical datum point ('top-left') given
        the child logical datum point and the child.bbSigma.
        Returns a Coord.Pt().
        This takes into account the sweep direction."""
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        if self._sweepDir == 0:
            return thePt
        return Coord.Pt(thePt.x - theBox.width, thePt.y)

    def postIncChildLogicalPos(self, thePt, theBox):
        """Post-incrempents the child logical datum point ('top-left') given
        the child logical datum point and the child.bbSigma.
        Returns a Coord.Pt().
        This takes into account the sweep direction."""
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        if self._sweepDir == 0:
            return Coord.Pt(thePt.x + theBox.width, thePt.y)
        return thePt

    def incPhysicalChildPos(self, thePt, theDim):
        """Given a child physical datum point and a distance to next child this
        returns the next childs physical datum point.
        TODO: Remove this as redundant?"""
        assert self._rootPos in self.RANGE_ROOTPOS_INT
        assert self._sweepDir in self.RANGE_SWEEPDIR_INT
        if self._rootPos == 0:
            if self._sweepDir == 0:
                return Coord.Pt(thePt.x + theDim, thePt.y)
            return Coord.Pt(thePt.x - theDim, thePt.y)
        if self._rootPos == 1:
            if self._sweepDir == 0:
                return Coord.Pt(thePt.x, thePt.y - theDim)
            return Coord.Pt(thePt.x, thePt.y + theDim)
        if self._rootPos == 2:
            if self._sweepDir == 0:
                return Coord.Pt(thePt.x - theDim, thePt.y)
            return Coord.Pt(thePt.x + theDim, thePt.y)
        if self._sweepDir == 0:
            return Coord.Pt(thePt.x, thePt.y + theDim)
        return Coord.Pt(thePt.x, thePt.y - theDim)