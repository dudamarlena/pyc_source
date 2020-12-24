# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/graphicsItems/AxisItem.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 43745 bytes
from ..Qt import QtGui, QtCore
from ..python2_3 import asUnicode
import numpy as np
from ..Point import Point
from .. import debug
import weakref
from .. import functions as fn
from .. import getConfigOption
from .GraphicsWidget import GraphicsWidget
__all__ = ['AxisItem']

class AxisItem(GraphicsWidget):
    __doc__ = '\n    GraphicsItem showing a single plot axis with ticks, values, and label.\n    Can be configured to fit on any side of a plot, and can automatically synchronize its displayed scale with ViewBox items.\n    Ticks can be extended to draw a grid.\n    If maxTickLength is negative, ticks point into the plot. \n    '

    def __init__(self, orientation, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        """
        ==============  ===============================================================
        **Arguments:**
        orientation     one of 'left', 'right', 'top', or 'bottom'
        maxTickLength   (px) maximum length of ticks to draw. Negative values draw
                        into the plot, positive values draw outward.
        linkView        (ViewBox) causes the range of values displayed in the axis
                        to be linked to the visible range of a ViewBox.
        showValues      (bool) Whether to display values adjacent to ticks 
        pen             (QPen) Pen used when drawing ticks.
        ==============  ===============================================================
        """
        GraphicsWidget.__init__(self, parent)
        self.label = QtGui.QGraphicsTextItem(self)
        self.picture = None
        self.orientation = orientation
        if orientation not in ('left', 'right', 'top', 'bottom'):
            raise Exception("Orientation argument must be one of 'left', 'right', 'top', or 'bottom'.")
        else:
            if orientation in ('left', 'right'):
                self.label.rotate(-90)
            self.style = {'tickTextOffset':[
              5, 2], 
             'tickTextWidth':30, 
             'tickTextHeight':18, 
             'autoExpandTextSpace':True, 
             'tickFont':None, 
             'stopAxisAtTick':(False, False), 
             'textFillLimits':[
              (0, 0.8),
              (2, 0.6),
              (4, 0.4),
              (6, 0.2)], 
             'showValues':showValues, 
             'tickLength':maxTickLength, 
             'maxTickLevel':2, 
             'maxTextLevel':2}
            self.textWidth = 30
            self.textHeight = 18
            self.fixedWidth = None
            self.fixedHeight = None
            self.labelText = ''
            self.labelUnits = ''
            self.labelUnitPrefix = ''
            self.labelStyle = {}
            self.logMode = False
            self.tickFont = None
            self._tickLevels = None
            self._tickSpacing = None
            self.scale = 1.0
            self.autoSIPrefix = True
            self.autoSIPrefixScale = 1.0
            self.setRange(0, 1)
            if pen is None:
                self.setPen()
            else:
                self.setPen(pen)
        self._linkedView = None
        if linkView is not None:
            self.linkToView(linkView)
        self.showLabel(False)
        self.grid = False

    def setStyle(self, **kwds):
        """
        Set various style options.
        
        =================== =======================================================
        Keyword Arguments:
        tickLength          (int) The maximum length of ticks in pixels. 
                            Positive values point toward the text; negative 
                            values point away.
        tickTextOffset      (int) reserved spacing between text and axis in px
        tickTextWidth       (int) Horizontal space reserved for tick text in px
        tickTextHeight      (int) Vertical space reserved for tick text in px
        autoExpandTextSpace (bool) Automatically expand text space if the tick
                            strings become too long.
        tickFont            (QFont or None) Determines the font used for tick 
                            values. Use None for the default font.
        stopAxisAtTick      (tuple: (bool min, bool max)) If True, the axis 
                            line is drawn only as far as the last tick. 
                            Otherwise, the line is drawn to the edge of the 
                            AxisItem boundary.
        textFillLimits      (list of (tick #, % fill) tuples). This structure
                            determines how the AxisItem decides how many ticks 
                            should have text appear next to them. Each tuple in
                            the list specifies what fraction of the axis length
                            may be occupied by text, given the number of ticks
                            that already have text displayed. For example::
                            
                                [(0, 0.8), # Never fill more than 80% of the axis
                                 (2, 0.6), # If we already have 2 ticks with text, 
                                           # fill no more than 60% of the axis
                                 (4, 0.4), # If we already have 4 ticks with text, 
                                           # fill no more than 40% of the axis
                                 (6, 0.2)] # If we already have 6 ticks with text, 
                                           # fill no more than 20% of the axis
                                
        showValues          (bool) indicates whether text is displayed adjacent
                            to ticks.
        =================== =======================================================
        
        Added in version 0.9.9
        """
        for kwd, value in kwds.items():
            if kwd not in self.style:
                raise NameError('%s is not a valid style argument.' % kwd)
            if kwd in ('tickLength', 'tickTextOffset', 'tickTextWidth', 'tickTextHeight'):
                if not isinstance(value, int):
                    raise ValueError("Argument '%s' must be int" % kwd)
            if kwd == 'tickTextOffset':
                if self.orientation in ('left', 'right'):
                    self.style['tickTextOffset'][0] = value
                else:
                    self.style['tickTextOffset'][1] = value
            elif kwd == 'stopAxisAtTick':
                try:
                    if not (len(value) == 2 and isinstance(value[0], bool) and isinstance(value[1], bool)):
                        raise AssertionError
                except:
                    raise ValueError("Argument 'stopAxisAtTick' must have type (bool, bool)")

                self.style[kwd] = value
            else:
                self.style[kwd] = value

        self.picture = None
        self._adjustSize()
        self.update()

    def close(self):
        self.scene().removeItem(self.label)
        self.label = None
        self.scene().removeItem(self)

    def setGrid(self, grid):
        """Set the alpha value (0-255) for the grid, or False to disable.
        
        When grid lines are enabled, the axis tick lines are extended to cover
        the extent of the linked ViewBox, if any.
        """
        self.grid = grid
        self.picture = None
        self.prepareGeometryChange()
        self.update()

    def setLogMode(self, log):
        """
        If *log* is True, then ticks are displayed on a logarithmic scale and values
        are adjusted accordingly. (This is usually accessed by changing the log mode 
        of a :func:`PlotItem <pyqtgraph.PlotItem.setLogMode>`)
        """
        self.logMode = log
        self.picture = None
        self.update()

    def setTickFont(self, font):
        self.tickFont = font
        self.picture = None
        self.prepareGeometryChange()
        self.update()

    def resizeEvent(self, ev=None):
        nudge = 5
        br = self.label.boundingRect()
        p = QtCore.QPointF(0, 0)
        if self.orientation == 'left':
            p.setY(int(self.size().height() / 2 + br.width() / 2))
            p.setX(-nudge)
        else:
            if self.orientation == 'right':
                p.setY(int(self.size().height() / 2 + br.width() / 2))
                p.setX(int(self.size().width() - br.height() + nudge))
            else:
                if self.orientation == 'top':
                    p.setY(-nudge)
                    p.setX(int(self.size().width() / 2.0 - br.width() / 2.0))
                else:
                    if self.orientation == 'bottom':
                        p.setX(int(self.size().width() / 2.0 - br.width() / 2.0))
                        p.setY(int(self.size().height() - br.height() + nudge))
                    self.label.setPos(p)
                    self.picture = None

    def showLabel(self, show=True):
        """Show/hide the label text for this axis."""
        self.label.setVisible(show)
        if self.orientation in ('left', 'right'):
            self._updateWidth()
        else:
            self._updateHeight()
        if self.autoSIPrefix:
            self.updateAutoSIPrefix()

    def setLabel(self, text=None, units=None, unitPrefix=None, **args):
        """Set the text displayed adjacent to the axis.
        
        ==============  =============================================================
        **Arguments:**
        text            The text (excluding units) to display on the label for this
                        axis.
        units           The units for this axis. Units should generally be given
                        without any scaling prefix (eg, 'V' instead of 'mV'). The
                        scaling prefix will be automatically prepended based on the
                        range of data displayed.
        **args          All extra keyword arguments become CSS style options for
                        the <span> tag which will surround the axis label and units.
        ==============  =============================================================
        
        The final text generated for the label will look like::
        
            <span style="...options...">{text} (prefix{units})</span>
            
        Each extra keyword argument will become a CSS option in the above template. 
        For example, you can set the font size and color of the label::
        
            labelStyle = {'color': '#FFF', 'font-size': '14pt'}
            axis.setLabel('label text', units='V', **labelStyle)
        
        """
        if text is not None:
            self.labelText = text
            self.showLabel()
        if units is not None:
            self.labelUnits = units
            self.showLabel()
        if unitPrefix is not None:
            self.labelUnitPrefix = unitPrefix
        if len(args) > 0:
            self.labelStyle = args
        self.label.setHtml(self.labelString())
        self._adjustSize()
        self.picture = None
        self.update()

    def labelString(self):
        if self.labelUnits == '':
            if not self.autoSIPrefix or self.autoSIPrefixScale == 1.0:
                units = ''
            else:
                units = asUnicode('(x%g)') % (1.0 / self.autoSIPrefixScale)
        else:
            units = asUnicode('(%s%s)') % (asUnicode(self.labelUnitPrefix), asUnicode(self.labelUnits))
        s = asUnicode('%s %s') % (asUnicode(self.labelText), asUnicode(units))
        style = ';'.join(['%s: %s' % (k, self.labelStyle[k]) for k in self.labelStyle])
        return asUnicode("<span style='%s'>%s</span>") % (style, asUnicode(s))

    def _updateMaxTextSize(self, x):
        if self.orientation in ('left', 'right'):
            mx = max(self.textWidth, x)
            if mx > self.textWidth or mx < self.textWidth - 10:
                self.textWidth = mx
                if self.style['autoExpandTextSpace'] is True:
                    self._updateWidth()
        else:
            mx = max(self.textHeight, x)
            if mx > self.textHeight or mx < self.textHeight - 10:
                self.textHeight = mx
                if self.style['autoExpandTextSpace'] is True:
                    self._updateHeight()

    def _adjustSize(self):
        if self.orientation in ('left', 'right'):
            self._updateWidth()
        else:
            self._updateHeight()

    def setHeight(self, h=None):
        """Set the height of this axis reserved for ticks and tick labels.
        The height of the axis label is automatically added.
        
        If *height* is None, then the value will be determined automatically
        based on the size of the tick text."""
        self.fixedHeight = h
        self._updateHeight()

    def _updateHeight(self):
        if not self.isVisible():
            h = 0
        else:
            if self.fixedHeight is None:
                if not self.style['showValues']:
                    h = 0
                else:
                    if self.style['autoExpandTextSpace'] is True:
                        h = self.textHeight
                    else:
                        h = self.style['tickTextHeight']
                h += self.style['tickTextOffset'][1] if self.style['showValues'] else 0
                h += max(0, self.style['tickLength'])
                if self.label.isVisible():
                    h += self.label.boundingRect().height() * 0.8
            else:
                h = self.fixedHeight
        self.setMaximumHeight(h)
        self.setMinimumHeight(h)
        self.picture = None

    def setWidth(self, w=None):
        """Set the width of this axis reserved for ticks and tick labels.
        The width of the axis label is automatically added.
        
        If *width* is None, then the value will be determined automatically
        based on the size of the tick text."""
        self.fixedWidth = w
        self._updateWidth()

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
                    w += self.label.boundingRect().height() * 0.8
            else:
                w = self.fixedWidth
        self.setMaximumWidth(w)
        self.setMinimumWidth(w)
        self.picture = None

    def pen(self):
        if self._pen is None:
            return fn.mkPen(getConfigOption('foreground'))
        return fn.mkPen(self._pen)

    def setPen(self, *args, **kwargs):
        """
        Set the pen used for drawing text, axes, ticks, and grid lines.
        If no arguments are given, the default foreground color will be used 
        (see :func:`setConfigOption <pyqtgraph.setConfigOption>`).
        """
        self.picture = None
        if args or kwargs:
            self._pen = (fn.mkPen)(*args, **kwargs)
        else:
            self._pen = fn.mkPen(getConfigOption('foreground'))
        self.labelStyle['color'] = '#' + fn.colorStr(self._pen.color())[:6]
        self.setLabel()
        self.update()

    def setScale(self, scale=None):
        """
        Set the value scaling for this axis. 
        
        Setting this value causes the axis to draw ticks and tick labels as if
        the view coordinate system were scaled. By default, the axis scaling is 
        1.0.
        """
        if scale is None:
            scale = 1.0
            self.enableAutoSIPrefix(True)
        if scale != self.scale:
            self.scale = scale
            self.setLabel()
            self.picture = None
            self.update()

    def enableAutoSIPrefix(self, enable=True):
        """
        Enable (or disable) automatic SI prefix scaling on this axis. 
        
        When enabled, this feature automatically determines the best SI prefix 
        to prepend to the label units, while ensuring that axis values are scaled
        accordingly. 
        
        For example, if the axis spans values from -0.1 to 0.1 and has units set 
        to 'V' then the axis would display values -100 to 100
        and the units would appear as 'mV'
        
        This feature is enabled by default, and is only available when a suffix
        (unit string) is provided to display on the label.
        """
        self.autoSIPrefix = enable
        self.updateAutoSIPrefix()

    def updateAutoSIPrefix(self):
        if self.label.isVisible():
            scale, prefix = fn.siScale(max(abs(self.range[0] * self.scale), abs(self.range[1] * self.scale)))
            if self.labelUnits == '':
                if prefix in ('k', 'm'):
                    scale = 1.0
                    prefix = ''
            self.setLabel(unitPrefix=prefix)
        else:
            scale = 1.0
        self.autoSIPrefixScale = scale
        self.picture = None
        self.update()

    def setRange(self, mn, mx):
        """Set the range of values displayed by the axis.
        Usually this is handled automatically by linking the axis to a ViewBox with :func:`linkToView <pyqtgraph.AxisItem.linkToView>`"""
        if any(np.isinf((mn, mx))) or any(np.isnan((mn, mx))):
            raise Exception('Not setting range to [%s, %s]' % (str(mn), str(mx)))
        self.range = [
         mn, mx]
        if self.autoSIPrefix:
            self.updateAutoSIPrefix()
        self.picture = None
        self.update()

    def linkedView(self):
        """Return the ViewBox this axis is linked to"""
        if self._linkedView is None:
            return
        return self._linkedView()

    def linkToView(self, view):
        """Link this axis to a ViewBox, causing its displayed range to match the visible range of the view."""
        oldView = self.linkedView()
        self._linkedView = weakref.ref(view)
        if self.orientation in ('right', 'left'):
            if oldView is not None:
                oldView.sigYRangeChanged.disconnect(self.linkedViewChanged)
            view.sigYRangeChanged.connect(self.linkedViewChanged)
        else:
            if oldView is not None:
                oldView.sigXRangeChanged.disconnect(self.linkedViewChanged)
            view.sigXRangeChanged.connect(self.linkedViewChanged)
        if oldView is not None:
            oldView.sigResized.disconnect(self.linkedViewChanged)
        view.sigResized.connect(self.linkedViewChanged)

    def linkedViewChanged(self, view, newRange=None):
        if self.orientation in ('right', 'left'):
            if newRange is None:
                newRange = view.viewRange()[1]
            if view.yInverted():
                (self.setRange)(*newRange[::-1])
            else:
                (self.setRange)(*newRange)
        elif newRange is None:
            newRange = view.viewRange()[0]
        elif view.xInverted():
            (self.setRange)(*newRange[::-1])
        else:
            (self.setRange)(*newRange)

    def boundingRect(self):
        linkedView = self.linkedView()
        if linkedView is None or self.grid is False:
            rect = self.mapRectFromParent(self.geometry())
            tl = self.style['tickLength']
            if self.orientation == 'left':
                rect = rect.adjusted(0, -15, -min(0, tl), 15)
            else:
                if self.orientation == 'right':
                    rect = rect.adjusted(min(0, tl), -15, 0, 15)
                else:
                    if self.orientation == 'top':
                        rect = rect.adjusted(-15, 0, 15, -min(0, tl))
                    else:
                        if self.orientation == 'bottom':
                            rect = rect.adjusted(-15, min(0, tl), 15, 0)
            return rect
        return self.mapRectFromParent(self.geometry()) | linkedView.mapRectToItem(self, linkedView.boundingRect())

    def paint(self, p, opt, widget):
        profiler = debug.Profiler()
        if self.picture is None:
            try:
                picture = QtGui.QPicture()
                painter = QtGui.QPainter(picture)
                specs = self.generateDrawSpecs(painter)
                profiler('generate specs')
                if specs is not None:
                    (self.drawPicture)(painter, *specs)
                    profiler('draw picture')
            finally:
                painter.end()

            self.picture = picture
        self.picture.play(p)

    def setTicks(self, ticks):
        """Explicitly determine which ticks to display.
        This overrides the behavior specified by tickSpacing(), tickValues(), and tickStrings()
        The format for *ticks* looks like::

            [
                [ (majorTickValue1, majorTickString1), (majorTickValue2, majorTickString2), ... ],
                [ (minorTickValue1, minorTickString1), (minorTickValue2, minorTickString2), ... ],
                ...
            ]
        
        If *ticks* is None, then the default tick system will be used instead.
        """
        self._tickLevels = ticks
        self.picture = None
        self.update()

    def setTickSpacing(self, major=None, minor=None, levels=None):
        """
        Explicitly determine the spacing of major and minor ticks. This 
        overrides the default behavior of the tickSpacing method, and disables
        the effect of setTicks(). Arguments may be either *major* and *minor*, 
        or *levels* which is a list of (spacing, offset) tuples for each 
        tick level desired.
        
        If no arguments are given, then the default behavior of tickSpacing
        is enabled.
        
        Examples::
        
            # two levels, all offsets = 0
            axis.setTickSpacing(5, 1)
            # three levels, all offsets = 0
            axis.setTickSpacing([(3, 0), (1, 0), (0.25, 0)])
            # reset to default
            axis.setTickSpacing()
        """
        if levels is None:
            if major is None:
                levels = None
            else:
                levels = [
                 (
                  major, 0), (minor, 0)]
        self._tickSpacing = levels
        self.picture = None
        self.update()

    def tickSpacing(self, minVal, maxVal, size):
        """Return values describing the desired spacing and offset of ticks.
        
        This method is called whenever the axis needs to be redrawn and is a 
        good method to override in subclasses that require control over tick locations.
        
        The return value must be a list of tuples, one for each set of ticks::
        
            [
                (major tick spacing, offset),
                (minor tick spacing, offset),
                (sub-minor tick spacing, offset),
                ...
            ]
        """
        if self._tickSpacing is not None:
            return self._tickSpacing
        dif = abs(maxVal - minVal)
        if dif == 0:
            return []
        optimalTickCount = max(2.0, np.log(size))
        optimalSpacing = dif / optimalTickCount
        p10unit = 10 ** np.floor(np.log10(optimalSpacing))
        intervals = np.array([1.0, 2.0, 10.0, 20.0, 100.0]) * p10unit
        minorIndex = 0
        while intervals[(minorIndex + 1)] <= optimalSpacing:
            minorIndex += 1

        levels = [
         (
          intervals[(minorIndex + 2)], 0),
         (
          intervals[(minorIndex + 1)], 0)]
        if self.style['maxTickLevel'] >= 2:
            minSpacing = min(size / 20.0, 30.0)
            maxTickCount = size / minSpacing
            if dif / intervals[minorIndex] <= maxTickCount:
                levels.append((intervals[minorIndex], 0))
            return levels

    def tickValues(self, minVal, maxVal, size):
        """
        Return the values and spacing of ticks to draw::
        
            [  
                (spacing, [major ticks]), 
                (spacing, [minor ticks]), 
                ... 
            ]
        
        By default, this method calls tickSpacing to determine the correct tick locations.
        This is a good method to override in subclasses.
        """
        minVal, maxVal = sorted((minVal, maxVal))
        minVal *= self.scale
        maxVal *= self.scale
        ticks = []
        tickLevels = self.tickSpacing(minVal, maxVal, size)
        allValues = np.array([])
        for i in range(len(tickLevels)):
            spacing, offset = tickLevels[i]
            start = np.ceil((minVal - offset) / spacing) * spacing + offset
            num = int((maxVal - start) / spacing) + 1
            values = (np.arange(num) * spacing + start) / self.scale
            values = list(filter(lambda x: all(np.abs(allValues - x) > spacing * 0.01), values))
            allValues = np.concatenate([allValues, values])
            ticks.append((spacing / self.scale, values))

        if self.logMode:
            return self.logTickValues(minVal, maxVal, size, ticks)
        return ticks

    def logTickValues(self, minVal, maxVal, size, stdTicks):
        ticks = []
        for spacing, t in stdTicks:
            if spacing >= 1.0:
                ticks.append((spacing, t))

        if len(ticks) < 3:
            v1 = int(np.floor(minVal))
            v2 = int(np.ceil(maxVal))
            minor = []
            for v in range(v1, v2):
                minor.extend(v + np.log10(np.arange(1, 10)))

            minor = [x for x in minor if x > minVal if x < maxVal]
            ticks.append((None, minor))
        return ticks

    def tickStrings(self, values, scale, spacing):
        """Return the strings that should be placed next to ticks. This method is called 
        when redrawing the axis and is a good method to override in subclasses.
        The method is called with a list of tick values, a scaling factor (see below), and the 
        spacing between ticks (this is required since, in some instances, there may be only 
        one tick and thus no other way to determine the tick spacing)
        
        The scale argument is used when the axis label is displaying units which may have an SI scaling prefix.
        When determining the text to display, use value*scale to correctly account for this prefix.
        For example, if the axis label's units are set to 'V', then a tick value of 0.001 might
        be accompanied by a scale value of 1000. This indicates that the label is displaying 'mV', and 
        thus the tick should display 0.001 * 1000 = 1.
        """
        if self.logMode:
            return self.logTickStrings(values, scale, spacing)
        places = max(0, np.ceil(-np.log10(spacing * scale)))
        strings = []
        for v in values:
            vs = v * scale
            if abs(vs) < 0.001 or abs(vs) >= 10000:
                vstr = '%g' % vs
            else:
                vstr = '%%0.%df' % places % vs
            strings.append(vstr)

        return strings

    def logTickStrings(self, values, scale, spacing):
        return ['%0.1g' % x for x in 10 ** np.array(values).astype(float)]

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
                                    br.setHeight(br.height() * 0.8)
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

    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs):
        profiler = debug.Profiler()
        p.setRenderHint(p.Antialiasing, False)
        p.setRenderHint(p.TextAntialiasing, True)
        pen, p1, p2 = axisSpec
        p.setPen(pen)
        p.drawLine(p1, p2)
        p.translate(0.5, 0)
        for pen, p1, p2 in tickSpecs:
            p.setPen(pen)
            p.drawLine(p1, p2)

        profiler('draw ticks')
        if self.tickFont is not None:
            p.setFont(self.tickFont)
        p.setPen(self.pen())
        for rect, flags, text in textSpecs:
            p.drawText(rect, flags, text)

        profiler('draw text')

    def show(self):
        GraphicsWidget.show(self)
        if self.orientation in ('left', 'right'):
            self._updateWidth()
        else:
            self._updateHeight()

    def hide(self):
        GraphicsWidget.hide(self)
        if self.orientation in ('left', 'right'):
            self._updateWidth()
        else:
            self._updateHeight()

    def wheelEvent(self, ev):
        if self.linkedView() is None:
            return
        elif self.orientation in ('left', 'right'):
            self.linkedView().wheelEvent(ev, axis=1)
        else:
            self.linkedView().wheelEvent(ev, axis=0)
        ev.accept()

    def mouseDragEvent(self, event):
        if self.linkedView() is None:
            return
        if self.orientation in ('left', 'right'):
            return self.linkedView().mouseDragEvent(event, axis=1)
        return self.linkedView().mouseDragEvent(event, axis=0)

    def mouseClickEvent(self, event):
        if self.linkedView() is None:
            return
        return self.linkedView().mouseClickEvent(event)