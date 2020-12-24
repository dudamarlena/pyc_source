# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/graphite/axis.py
# Compiled at: 2007-10-30 16:55:44
"""Implements axis for graphite."""
import math
from property import *
import constants as C
from constants import LINEAR, AUTO, X, Y, Z
from primitive import Text, LineStyle, TextStyle, Line
from copy import copy, deepcopy
import pid as PID, Num, types
try:
    math.log(2.0, 3.0)
    log = math.log
except TypeError, x:
    assert '1' in str(x) and '2' in str(x)

    def log(num, base=math.e):
        return math.log(num) / math.log(base)


class TickMarks(PropHolder):
    """Class TickMarks
        Purpose: keeps information about a set of tick marks -- how big
                         they are, the labels, etc.
        Notes: we may have to deal better with overlapping tickmarks later.
        """
    _properties = {'inextent': FloatProperty(0.02, 'length (towards center) of marks, in view coordinates', minval=0, maxval=1), 
       'outextent': FloatProperty(0, 'length (away from center) of marks, in view coordinates', minval=0, maxval=1), 
       'spacing': FloatProperty(0, 'distance between marks, in dataset coordinates (0=auto)', minval=0), 
       'labeldist': FloatProperty(-0.04, 'distance from axis in view coordinates where labels should be placed', minval=-1, maxval=1), 
       'offset': FloatProperty(0, 'distance from the origin (in data coordinates) before the tick marks start', minval=0), 
       'lineStyle': ClassProperty(LineStyle, LineStyle(), 'style of the tickmark lines'), 
       'labelStyle': ClassProperty(TextStyle, TextStyle(), 'text style of tickmark labels'), 
       'labels': Property(None, 'tickmark labels: None, AUTO, a format string, list of strings, or function')}

    def __init__(self, inextent=0.02, outextent=0, offset=0, spacing=0, lineStyle=None, labels=None, labelStyle=None):
        PropHolder.__init__(self)
        self.inextent, self.outextent = inextent, outextent
        self.offset = offset
        self.spacing = spacing
        if lineStyle is not None:
            self.lineStyle = lineStyle
        else:
            self.lineStyle = LineStyle()
        if labelStyle is not None:
            self.labelStyle = labelStyle
        else:
            self.labelStyle = TextStyle(font=PID.Font(size=10))
        self.labels = labels
        return

    def __repr__(self):
        return 'TickMarks()'

    def exportString(self, selfname):
        """Returns a string with all field assignments."""
        retval = self.exportStringFunc(selfname, proplist=('inextent', 'outextent',
                                                           'offset', 'lineStyle',
                                                           'labelStyle', 'labels'))
        return retval

    def submitLabel(self, primitives, ticknum, value, pos):
        """submit a label for the 'ticknum'-th tick mark, having data value 'value', at view coordinates 'pos'"""
        if callable(self.labels):
            primitives.append(Text(self.labels(ticknum, value), pos, style=self.labelStyle))
        elif type(self.labels) == types.StringType:
            primitives.append(Text(self.labels % value, pos, style=self.labelStyle))
        else:
            primitives.append(Text(self.labels[(ticknum % len(self.labels))], pos, style=self.labelStyle))


class Axis(PropHolder):
    """Class: Axis
        Purpose: defines the extent, type, and appearance of an axis
        """
    _properties = {'range': Property([AUTO, AUTO], 'data range of the axis; [AUTO,AUTO] means auto range'), 
       'drawPos': Property([((0, 0, 0), (1, 0, 0))], 'locations in view coordinates where the axis should be drawn'), 
       'label': ClassProperty(Text, None, 'axis label'), 
       'visible': BoolProperty(True, 'whether or not the axis should be drawn at all'), 
       'tickMarks': ListProperty(ClassProperty(TickMarks, None, ''), None, 'list of TickMarks objects attached to this axis')}

    def __init__(self, whichAxis='X', logbase=LINEAR):
        """Constructor -- initializes member variables with sensible defaults for the given axis type (X, Y, or Z)."""
        PropHolder.__init__(self)
        self.range = copy(self.range)
        startpos = (0, 0, 0)
        if whichAxis == 'X' or whichAxis == X:
            endpos = (1, 0, 0)
            self.label = 'X Axis'
            self.label.points[0] = (0, -0.2, 0)
        elif whichAxis == 'Y' or whichAxis == Y:
            endpos = (0, 1, 0)
            self.label = 'Y Axis'
            self.label.points[0] = (-0.15, 0, 0)
            self.label.angle = 90
        if self.label:
            pass
        elif whichAxis == 'Z' or whichAxis == Z:
            endpos = (0, 0, 1)
        else:
            raise TypeError, "Axis constructor did not receive one of 'X', 'Y', 'Z'"
        self.drawPos = [
         (
          startpos, endpos)]
        self.tickMarks = [
         TickMarks()]

    def __repr__(self):
        return 'Axis()'

    def exportString(self, selfname):
        """Returns a string with all field assignments."""
        retval = self.exportStringFunc(selfname, proplist=('range', 'drawPos', 'label',
                                                           'visible', 'tickMarks'), compProplist=[
         'tickMarks'])
        return retval

    def scale(self):
        """return the scale factor needed to map our range into 0-1"""
        return 1.0 / (self.actualRange()[1] - self.actualRange()[0])

    def origin(self):
        """return the start of our range"""
        return self.actualRange()[0]

    def viewScale(self, whichAxis):
        """Return the extent of this graph axis in *view* space, along the given coordinate axis (X, Y, or Z) -- normally, this extent is 1.  Note that only the first drawPos of the axis is considered."""
        drawPos = self.drawPos[0]
        return drawPos[1][whichAxis] - drawPos[0][whichAxis]

    def viewOrigin(self, whichAxis):
        """Return the origin of this graph axis in *view* space, along the given coordinate axis (X, Y, or Z) -- normally, this origin is 0.  Note that only the first drawPos of the axis is considered."""
        return self.drawPos[0][0][whichAxis]

    def setActualRange(self, datarange):
        """Placeholder: Do nothing for now"""
        (rangestart, rangeend) = self.range[:2]

    def submit(self, primitives):
        """append any drawing primitives for this axis onto the given list"""
        pass

    def _submitLabel(self, primitives):
        """Submit the axis label (if any).
                It adds primitives to the list of primitives that is passed in."""
        if self.label:
            adjustedText = deepcopy(self.label)
            adjustedPos = [0, 0, 0]
            for axis in (X, Y, Z):
                dwp = [ pos[0][axis] for pos in self.drawPos ] + [ pos[1][axis] for pos in self.drawPos ]
                bmin = min(dwp)
                bmax = max(dwp)
                center = float(bmin + bmax) / 2.0
                adjustedPos[axis] = self.label.points[0][axis] + center

            adjustedText.points[0] = adjustedPos
            primitives.append(adjustedText)


class LinearAxis(Axis):

    def logorigin(self):
        """return the start of our range, transformed by the log base"""
        return self.actualRange()[0]

    def logscale(self):
        """return the scale factor needed to map our range into 0-1, after a log transformation"""
        return self.scale()

    def transform(self, x):
        return lambda x: x

    def dfltLabelFormat(self):
        rel = math.log10((abs(self._rangestart) + abs(self._rangeend)) / abs(self._tickspacing))
        a = int(math.floor(math.log10(abs(self._tickspacing))))
        if a < 0 and a > -5 and rel + 2 > abs(a):
            fmtstring = '%%.%df' % -a
            return fmtstring
        if a >= 0 and a < 5 and rel + 2 > a:
            return '%.0f'
        b = int(math.floor(math.log10(abs(self._rangestart) + abs(self._rangeend))))
        b10 = math.pow(10.0, -b)
        if rel > 0:
            fmts = '%%.%dfe%d' % (int(math.ceil(rel)), b)
        else:
            fmts = '%%.0fe%d' % b
        return lambda tn, x, bb=b10, fs=fmts: fs % (x * b10)

    def setActualRange(self, datarange):
        """Depending upon AUTO settings set the actual bounds and
                tickmark spacing for this axis"""
        (rangestart, rangeend) = self.range[:2]
        if self.range[0] == AUTO:
            rangestart = datarange[0]
        if self.range[1] == AUTO:
            rangeend = datarange[1]
        if rangestart == rangeend:
            rangeend = rangestart + 1
        magnitude = math.floor(math.log10(abs(rangeend - rangestart)))
        magnitude = magnitude - 1
        powmag = math.pow(10.0, magnitude)
        if powmag * 50 < abs(rangeend - rangestart):
            powmag = powmag * 10
        elif powmag * 20 < abs(rangeend - rangestart):
            powmag = powmag * 5
        elif powmag * 10 < abs(rangeend - rangestart):
            powmag = powmag * 2
        delta = 0.01 * powmag
        if rangestart > rangeend:
            delta = -delta
        if self.range[0] == AUTO:
            rangestart = math.floor((rangestart - delta) / powmag) * powmag
        if self.range[1] == AUTO:
            rangeend = math.ceil((rangeend + delta) / powmag) * powmag
        self._tickspacing = powmag
        self._rangestart = rangestart
        self._rangeend = rangeend

    def actualRange(self):
        if self._rangestart > self._rangeend:
            return (
             self._rangeend, self._rangestart)
        return (
         self._rangestart, self._rangeend)

    def submit(self, primitives):
        """append any drawing primitives for this axis onto the given list"""
        if not self.visible:
            return
        for t in self.tickMarks:
            if t.labels == AUTO:
                t.labels = self.dfltLabelFormat()

        for positions in self.drawPos:
            startpos = Num.array(positions[0], Num.Float)
            endpos = Num.array(positions[1], Num.Float)
            primitives.append(Line(startpos, endpos))
            for marks in self.tickMarks:
                labelStyle = deepcopy(marks.labelStyle)
                if startpos[1] == endpos[1]:
                    labelStyle.vjust = C.TOP
                    labelStyle.hjust = C.CENTER
                else:
                    labelStyle.vjust = C.CENTER
                    labelStyle.hjust = C.RIGHT
                if marks.offset:
                    raise NotImplementedError, 'TickMarks.offset'
                style = marks.lineStyle
                pos = self.actualRange()[0] + marks.offset
                rangestart = self.actualRange()[0]
                rangeend = self.actualRange()[1]
                innies = [
                 marks.inextent] * 3
                outies = [marks.outextent] * 3
                labeldist = marks.labeldist
                for axis in range(0, 3):
                    if startpos[axis] > 0.5:
                        innies[axis] = innies[axis] * -1
                        outies[axis] = outies[axis] * -1
                        if startpos[axis] == endpos[axis]:
                            labeldist = labeldist * -1
                            if labelStyle.hjust == C.RIGHT:
                                labelStyle.hjust = C.LEFT
                            if labelStyle.vjust == C.TOP:
                                labelStyle.vjust = C.BOTTOM

                tickcount = 0
                tickspacing = marks.spacing
                if tickspacing <= 0:
                    tickspacing = self._tickspacing
                while pos <= self.actualRange()[1]:
                    fpos = (pos - rangestart) * self.scale()
                    v = (endpos - startpos) * fpos + startpos
                    if startpos[X] == endpos[X]:
                        primitives.append(Line((
                         v[X] + innies[X], v[Y], v[Z]), (
                         v[X] - outies[X], v[Y], v[Z]), style))
                    if startpos[Y] == endpos[Y]:
                        primitives.append(Line((
                         v[X], v[Y] + innies[Y], v[Z]), (
                         v[X], v[Y] - outies[Y], v[Z]), style))
                    if startpos[Z] == endpos[Z]:
                        primitives.append(Line((
                         v[X], v[Y], v[Z] + innies[Z]), (
                         v[X], v[Y], v[Z] - outies[Z]), style))
                    if marks.labels != None:
                        labelpos = (v[X] + (startpos[X] == endpos[X]) * labeldist,
                         v[Y] + (startpos[Y] == endpos[Y]) * labeldist,
                         v[Z] + (startpos[Z] == endpos[Z]) * labeldist)
                        marks.submitLabel(primitives, tickcount, pos, labelpos)
                    pos += tickspacing
                    tickcount += 1

        self._submitLabel(primitives)
        return


class LogAxis(Axis):
    _properties = Axis._properties.copy()
    _properties['logbase'] = FloatProperty(LINEAR, 'LINEAR, or a log base (e.g., 10 or math.e)', minval=1.0)
    _properties['logsteps'] = IntProperty(9, 'number of sub-steps within one base cycle on a log axis, or 0 for default', minval=0)

    def logorigin(self):
        """return the start of our range, transformed by the log base"""
        return log(self.actualRange()[0], self.logbase)

    def logscale(self):
        """return the scale factor needed to map our range into 0-1, after a log transformation"""
        return 1.0 / (log(self.actualRange()[1], self.logbase) - log(self.actualRange()[0], self.logbase))

    def exportString(self, selfname):
        """Returns a string with all field assignments."""
        retval = self.formatFunc('logbase', selfname, self.logbase)
        retval += Axis.exportStringFunc(self, selfname, proplist=['logbase'])
        retval += Axis.exportString(self, selfname)
        return retval

    def transform(self, x):
        return lambda x, b=self.logbase: log(x, b)

    def setActualRange(self, datarange):
        """Placeholder: Do nothing for now"""
        (rangestart, rangeend) = self.range[:2]

    def submit(self, primitives):
        """append any drawing primitives for this axis onto the given list"""
        if not self.visible:
            return
        for positions in self.drawPos:
            startpos = Num.array(positions[0], Num.Float)
            endpos = Num.array(positions[1], Num.Float)
            primitives.append(Line(startpos, endpos))
            for marks in self.tickMarks:
                labelStyle = deepcopy(marks.labelStyle)
                if startpos[1] == endpos[1]:
                    labelStyle.vjust = C.TOP
                    labelStyle.hjust = C.CENTER
                else:
                    labelStyle.vjust = C.CENTER
                    labelStyle.hjust = C.RIGHT
                if marks.offset:
                    raise NotImplementedError, 'TickMarks.offset'
                style = marks.lineStyle
                pos = self.actualRange()[0] + marks.offset
                if marks.logsteps < 1:
                    raise NotImplementedError, "Can't agree on defaults!"
                assert pos > 0
                a = log(pos, self.logbase)
                substep = (math.pow(self.logbase, a) - math.pow(self.logbase, a - 1)) / marks.logsteps
                rangestart = log(self.actualRange()[0], self.logbase)
                rangeend = log(self.actualRange()[1], self.logbase)
                innies = [
                 marks.inextent] * 3
                outies = [marks.outextent] * 3
                labeldist = marks.labeldist
                for axis in range(0, 3):
                    if startpos[axis] > 0.5:
                        innies[axis] = innies[axis] * -1
                        outies[axis] = outies[axis] * -1
                        if startpos[axis] == endpos[axis]:
                            labeldist = labeldist * -1
                            if labelStyle.hjust == C.RIGHT:
                                labelStyle.hjust = C.LEFT
                            if labelStyle.vjust == C.TOP:
                                labelStyle.vjust = C.BOTTOM

                tickcount = 0
                while pos <= self.actualRange()[1]:
                    fpos = (log(pos, self.logbase) - rangestart) * self.logscale()
                    v = (endpos - startpos) * fpos + startpos
                    if startpos[X] == endpos[X]:
                        primitives.append(Line((
                         v[X] + innies[X], v[Y], v[Z]), (
                         v[X] - outies[X], v[Y], v[Z]), style))
                    if startpos[Y] == endpos[Y]:
                        primitives.append(Line((
                         v[X], v[Y] + innies[Y], v[Z]), (
                         v[X], v[Y] - outies[Y], v[Z]), style))
                    if startpos[Z] == endpos[Z]:
                        primitives.append(Line((
                         v[X], v[Y], v[Z] + innies[Z]), (
                         v[X], v[Y], v[Z] - outies[Z]), style))
                    if marks.labels != None:
                        labelpos = (v[X] + (startpos[X] == endpos[X]) * labeldist,
                         v[Y] + (startpos[Y] == endpos[Y]) * labeldist,
                         v[Z] + (startpos[Z] == endpos[Z]) * labeldist)
                        marks.submitLabel(primitives, tickcount, pos, labelpos)
                    if tickcount % marks.logsteps == 0:
                        substep = substep * self.logbase
                    pos = pos + substep
                    tickcount = tickcount + 1

        self._submitLabel(primitives)
        return