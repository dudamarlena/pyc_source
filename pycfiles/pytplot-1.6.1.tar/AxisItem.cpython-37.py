# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/PyTplot/PyTplot/pytplot/QtPlotter/CustomAxis/AxisItem.py
# Compiled at: 2020-04-24 00:12:01
# Size of source mod 2**32: 11743 bytes
import numpy as np, pyqtgraph as pg
import pyqtgraph.debug as debug
from pyqtgraph import Point
from pyqtgraph.Qt import QtCore
from pyqtgraph.python2_3 import asUnicode

class AxisItem(pg.AxisItem):
    __doc__ = '\n    GraphicsItem showing a single plot axis with ticks, values, and label.\n    Can be configured to fit on any side of a plot, and can automatically synchronize its displayed scale with ViewBox\n    items. Ticks can be extended to draw a grid.\n    If maxTickLength is negative, ticks point into the plot.\n    '

    def _updateWidth(self):
        if not self.isVisible():
            w = 0
        else:
            if self.fixedWidth is None:
                if not self.style['showValues']:
                    w = 0
                else:
                    if self.style['autoExpandTextSpace'] is True:
                        w = self.textWidth
                    else:
                        w = self.style['tickTextWidth']
                w += self.style['tickTextOffset'][0] if self.style['showValues'] else 0
                w += max(0, self.style['tickLength'])
                if self.label.isVisible():
                    w += self.label.boundingRect().height() * 1.4
            else:
                w = self.fixedWidth
        self.setMaximumWidth(w)
        self.setMinimumWidth(w)
        self.picture = None

    def generateDrawSpecs(self, p):
        """
        Calls tickValues() and tickStrings() to determine where and how ticks should
        be drawn, then generates from this a set of drawing commands to be
        interpreted by drawPicture().
        """
        profiler = debug.Profiler()
        bounds = self.mapRectFromParent(self.geometry())
        linkedView = self.linkedView()
        if linkedView is None or self.grid is False:
            tickBounds = bounds
        else:
            tickBounds = linkedView.mapRectToItem(self, linkedView.boundingRect())
        if self.orientation == 'left':
            span = (
             bounds.topRight(), bounds.bottomRight())
            tickStart = tickBounds.right()
            tickStop = bounds.right()
            tickDir = -1
            axis = 0
        else:
            if self.orientation == 'right':
                span = (
                 bounds.topLeft(), bounds.bottomLeft())
                tickStart = tickBounds.left()
                tickStop = bounds.left()
                tickDir = 1
                axis = 0
            else:
                if self.orientation == 'top':
                    span = (
                     bounds.bottomLeft(), bounds.bottomRight())
                    tickStart = tickBounds.bottom()
                    tickStop = bounds.bottom()
                    tickDir = -1
                    axis = 1
                else:
                    if self.orientation == 'bottom':
                        span = (
                         bounds.topLeft(), bounds.topRight())
                        tickStart = tickBounds.top()
                        tickStop = bounds.top()
                        tickDir = 1
                        axis = 1
                    else:
                        points = list(map(self.mapToDevice, span))
                        if None in points:
                            return
                        else:
                            lengthInPixels = Point(points[1] - points[0]).length()
                            if lengthInPixels == 0:
                                return
                                if self._tickLevels is None:
                                    tickLevels = self.tickValues(self.range[0], self.range[1], lengthInPixels)
                                    tickStrings = None
                            else:
                                tickLevels = []
                                tickStrings = []
                                for level in self._tickLevels:
                                    values = []
                                    strings = []
                                    tickLevels.append((None, values))
                                    tickStrings.append(strings)
                                    for val, strn in level:
                                        values.append(val)
                                        strings.append(strn)

                        dif = self.range[1] - self.range[0]
                        if dif == 0:
                            xScale = 1
                            offset = 0
                        else:
                            if axis == 0:
                                xScale = -bounds.height() / dif
                                offset = self.range[0] * xScale - bounds.height()
                            else:
                                xScale = bounds.width() / dif
                                offset = self.range[0] * xScale
                        xRange = [x * xScale - offset for x in self.range]
                        xMin = min(xRange)
                        xMax = max(xRange)
                        profiler('init')
                        tickPositions = []
                        tickSpecs = []
                        for i in range(len(tickLevels)):
                            tickPositions.append([])
                            ticks = tickLevels[i][1]
                            tickLength = self.style['tickLength'] / (i * 0.5 + 1.0)
                            lineAlpha = 255 / (i + 1)
                            if self.grid is not False:
                                lineAlpha *= self.grid / 255.0 * np.clip(0.05 * lengthInPixels / (len(ticks) + 1), 0.0, 1.0)
                            for v in ticks:
                                x = v * xScale - offset
                                if not x < xMin:
                                    if x > xMax:
                                        tickPositions[i].append(None)
                                        continue
                                    tickPositions[i].append(x)
                                    p1 = [
                                     x, x]
                                    p2 = [x, x]
                                    p1[axis] = tickStart
                                    p2[axis] = tickStop
                                    if self.grid is False:
                                        p2[axis] += tickLength * tickDir
                                    tickPen = self.pen()
                                    color = tickPen.color()
                                    color.setAlpha(lineAlpha)
                                    tickPen.setColor(color)
                                    tickSpecs.append((tickPen, Point(p1), Point(p2)))

                        profiler('compute ticks')
                        if self.style['stopAxisAtTick'][0] is True:
                            stop = max(span[0].y(), min(map(min, tickPositions)))
                            if axis == 0:
                                span[0].setY(stop)
                            else:
                                span[0].setX(stop)
                        if self.style['stopAxisAtTick'][1] is True:
                            stop = min(span[1].y(), max(map(max, tickPositions)))
                            if axis == 0:
                                span[1].setY(stop)
                            else:
                                span[1].setX(stop)
                        axisSpec = (
                         self.pen(), span[0], span[1])
                        textOffset = self.style['tickTextOffset'][axis]
                        textSize2 = 0
                        textRects = []
                        textSpecs = []
                        return self.style['showValues'] or (
                         axisSpec, tickSpecs, textSpecs)
                    for i in range(min(len(tickLevels), self.style['maxTextLevel'] + 1)):
                        if tickStrings is None:
                            spacing, values = tickLevels[i]
                            strings = self.tickStrings(values, self.autoSIPrefixScale * self.scale, spacing)
                        else:
                            strings = tickStrings[i]
                        if len(strings) == 0:
                            continue
                        else:
                            for j in range(len(strings)):
                                if tickPositions[i][j] is None:
                                    strings[j] = None

                            rects = []
                            for s in strings:
                                if s is None:
                                    rects.append(None)
                                else:
                                    br = p.boundingRect(QtCore.QRectF(0, 0, 100, 100), QtCore.Qt.AlignCenter, asUnicode(s))
                                    br.setHeight(br.height() * 1.4)
                                    rects.append(br)
                                    textRects.append(rects[(-1)])

                            if len(textRects) > 0:
                                if axis == 0:
                                    textSize = np.sum([r.height() for r in textRects])
                                    textSize2 = np.max([r.width() for r in textRects])
                                else:
                                    textSize = np.sum([r.width() for r in textRects])
                                    textSize2 = np.max([r.height() for r in textRects])
                            else:
                                textSize = 0
                            textSize2 = 0
                        if i > 0:
                            textFillRatio = float(textSize) / lengthInPixels
                            finished = False
                            for nTexts, limit in self.style['textFillLimits']:
                                if len(textSpecs) >= nTexts and textFillRatio >= limit:
                                    finished = True
                                    break

                            if finished:
                                break
                        for j in range(len(strings)):
                            vstr = strings[j]
                            if vstr is None:
                                continue
                            vstr = asUnicode(vstr)
                            x = tickPositions[i][j]
                            textRect = rects[j]
                            height = textRect.height()
                            width = textRect.width()
                            offset = max(0, self.style['tickLength']) + textOffset
                            if self.orientation == 'left':
                                textFlags = QtCore.Qt.TextDontClip | QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
                                rect = QtCore.QRectF(tickStop - offset - width, x - height / 2, width, height)
                            else:
                                if self.orientation == 'right':
                                    textFlags = QtCore.Qt.TextDontClip | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
                                    rect = QtCore.QRectF(tickStop + offset, x - height / 2, width, height)
                                else:
                                    if self.orientation == 'top':
                                        textFlags = QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom
                                        rect = QtCore.QRectF(x - width / 2.0, tickStop - offset - height, width, height)
                                    else:
                                        if self.orientation == 'bottom':
                                            textFlags = QtCore.Qt.TextDontClip | QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop
                                            rect = QtCore.QRectF(x - width / 2.0, tickStop + offset, width, height)
                                        textSpecs.append((rect, textFlags, vstr))

                    profiler('compute text')
                    self._updateMaxTextSize(textSize2)
                    return (
                     axisSpec, tickSpecs, textSpecs)