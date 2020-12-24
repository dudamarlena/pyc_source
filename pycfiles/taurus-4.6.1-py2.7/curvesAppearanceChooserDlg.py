# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/qwt5/curvesAppearanceChooserDlg.py
# Compiled at: 2019-08-19 15:09:30
"""
curvesAppearanceChooserDlg.py:
    A Qt dialog for choosing plot appearance (symbols and lines)
    for a QwtPlot-derived widget (like Taurusplot)
"""
from __future__ import print_function
from builtins import object
import copy
from taurus.external.qt import Qt, Qwt5, compat
from taurus.core.util.containers import CaselessDict
from taurus.qt.qtgui.util.ui import UILoadable
NamedLineStyles = {None: '', Qt.Qt.NoPen: 'No line', 
   Qt.Qt.SolidLine: '_____', 
   Qt.Qt.DashLine: '_ _ _', 
   Qt.Qt.DotLine: '.....', 
   Qt.Qt.DashDotLine: '_._._', 
   Qt.Qt.DashDotDotLine: '.._..'}
ReverseNamedLineStyles = {}
for k, v in NamedLineStyles.items():
    ReverseNamedLineStyles[v] = k

NamedCurveStyles = {None: '', Qwt5.QwtPlotCurve.NoCurve: 'No curve', 
   Qwt5.QwtPlotCurve.Lines: 'Lines', 
   Qwt5.QwtPlotCurve.Sticks: 'Sticks', 
   Qwt5.QwtPlotCurve.Steps: 'Steps', 
   Qwt5.QwtPlotCurve.Dots: 'Dots'}
ReverseNamedCurveStyles = {}
for k, v in NamedCurveStyles.items():
    ReverseNamedCurveStyles[v] = k

NamedSymbolStyles = {None: '', 
   Qwt5.QwtSymbol.NoSymbol: 'No symbol', 
   Qwt5.QwtSymbol.Ellipse: 'Circle', 
   Qwt5.QwtSymbol.Rect: 'Square', 
   Qwt5.QwtSymbol.Diamond: 'Diamond', 
   Qwt5.QwtSymbol.Triangle: 'Triangle', 
   Qwt5.QwtSymbol.DTriangle: 'Down Triangle', 
   Qwt5.QwtSymbol.UTriangle: 'Up triangle', 
   Qwt5.QwtSymbol.LTriangle: 'Left Triangle', 
   Qwt5.QwtSymbol.RTriangle: 'Right Triangle', 
   Qwt5.QwtSymbol.Cross: 'Cross', 
   Qwt5.QwtSymbol.XCross: 'XCross', 
   Qwt5.QwtSymbol.HLine: 'Horizontal line', 
   Qwt5.QwtSymbol.VLine: 'Vertical line', 
   Qwt5.QwtSymbol.Star1: 'Star1', 
   Qwt5.QwtSymbol.Star2: 'Star2', 
   Qwt5.QwtSymbol.Hexagon: 'Hexagon'}
ReverseNamedSymbolStyles = {}
for k, v in NamedSymbolStyles.items():
    ReverseNamedSymbolStyles[v] = k

NamedColors = ['Black', 'Red', 'Blue', 'Magenta',
 'Green', 'Cyan', 'Yellow', 'Gray', 'White']

@UILoadable
class CurvesAppearanceChooser(Qt.QWidget):
    """
    A widget for choosing plot appearance for one or more curves.
    The current curves properties are passed using the setCurves() method using
    a dictionary with the following structure::

        curvePropDict={name1:prop1, name2:prop2,...}

    where propX is an instance of :class:`CurveAppearanceProperties`
    When applying, a signal is emitted and the chosen properties are made
    available in a similar dictionary. """
    NAME_ROLE = Qt.Qt.UserRole
    controlChanged = Qt.pyqtSignal()
    curveAppearanceChanged = Qt.pyqtSignal(compat.PY_OBJECT, list)
    CurveTitleEdited = Qt.pyqtSignal('QString', 'QString')

    def __init__(self, parent=None, curvePropDict={}, showButtons=False, autoApply=False, designMode=False):
        super(CurvesAppearanceChooser, self).__init__(parent)
        self.loadUi()
        self.autoApply = autoApply
        self.sStyleCB.insertItems(0, sorted(NamedSymbolStyles.values()))
        self.lStyleCB.insertItems(0, list(NamedLineStyles.values()))
        self.cStyleCB.insertItems(0, list(NamedCurveStyles.values()))
        self.sColorCB.addItem('')
        self.lColorCB.addItem('')
        if not showButtons:
            self.applyBT.hide()
            self.resetBT.hide()
        for color in NamedColors:
            icon = self._colorIcon(color)
            self.sColorCB.addItem(icon, '', Qt.QColor(color))
            self.lColorCB.addItem(icon, '', Qt.QColor(color))

        self.__itemsDict = CaselessDict()
        self.setCurves(curvePropDict)
        self.bckgndBT.setIcon(Qt.QIcon(':color-fill.svg'))
        self.curvesLW.itemSelectionChanged.connect(self.onSelectedCurveChanged)
        self.curvesLW.itemChanged.connect(self.onItemChanged)
        self.applyBT.clicked.connect(self.onApply)
        self.resetBT.clicked.connect(self.onReset)
        self.sStyleCB.currentIndexChanged.connect(self._onSymbolStyleChanged)
        self.sStyleCB.currentIndexChanged.connect(self.onControlChanged)
        self.lStyleCB.currentIndexChanged.connect(self.onControlChanged)
        self.sColorCB.currentIndexChanged.connect(self.onControlChanged)
        self.lColorCB.currentIndexChanged.connect(self.onControlChanged)
        self.cStyleCB.currentIndexChanged.connect(self.onControlChanged)
        self.sSizeSB.valueChanged.connect(self.onControlChanged)
        self.lWidthSB.valueChanged.connect(self.onControlChanged)
        self.sFillCB.stateChanged.connect(self.onControlChanged)
        self.cFillCB.stateChanged.connect(self.onControlChanged)

    def setCurves(self, curvePropDict):
        """Populates the list of curves from the properties dictionary. It uses
        the curve title for display, and stores the curve name as the item data
        (with role=CurvesAppearanceChooser.NAME_ROLE)

        :param curvePropDict:   (dict) a dictionary whith keys=curvenames and
                                values= :class:`CurveAppearanceProperties` object
        """
        self.curvePropDict = curvePropDict
        self._curvePropDictOrig = copy.deepcopy(curvePropDict)
        self.curvesLW.clear()
        self.__itemsDict = CaselessDict()
        for name, prop in self.curvePropDict.items():
            item = Qt.QListWidgetItem(str(prop.title), self.curvesLW)
            self.__itemsDict[name] = item
            item.setData(self.NAME_ROLE, str(name))
            item.setToolTip('<b>Curve Name:</b> %s' % name)
            item.setFlags(Qt.Qt.ItemIsEnabled | Qt.Qt.ItemIsSelectable | Qt.Qt.ItemIsUserCheckable | Qt.Qt.ItemIsDragEnabled | Qt.Qt.ItemIsEditable)

        self.curvesLW.setCurrentRow(0)

    def onItemChanged(self, item):
        """slot used when an item data has changed"""
        name = item.data(self.NAME_ROLE)
        previousTitle = self.curvePropDict[name].title
        currentTitle = item.text()
        if previousTitle != currentTitle:
            self.curvePropDict[name].title = currentTitle
            self.CurveTitleEdited.emit(name, currentTitle)

    def updateTitles(self, newTitlesDict=None):
        """
        Updates the titles of the curves that are displayed in the curves list.

        :param newTitlesDict: (dict<str,str>) dictionary with key=curve_name and
                              value=title
        """
        if newTitlesDict is None:
            return
        else:
            for name, title in newTitlesDict.items():
                self.curvePropDict[name].title = title
                self.__itemsDict[name].setText(title)

            return

    def getSelectedCurveNames(self):
        """Returns the curve names for the curves selected at the curves list.

        *Note*: The names may differ from the displayed text, which
        corresponds to the curve titles (this method is what you likely need if
        you want to get keys to use in curves or curveProp dicts).

        :return: (string_list) the names of the selected curves
        """
        return [ item.data(self.NAME_ROLE) for item in self.curvesLW.selectedItems() ]

    def showProperties(self, prop=None):
        """Updates the dialog to show the given properties.

        :param prop: (CurveAppearanceProperties) the properties object
                     containing what should be shown. If a given property is set
                     to None, the corresponding widget will show a "neutral"
                     display
        """
        if prop is None:
            prop = self._shownProp
        self.sStyleCB.setCurrentIndex(self.sStyleCB.findText(NamedSymbolStyles[prop.sStyle]))
        self.lStyleCB.setCurrentIndex(self.lStyleCB.findText(NamedLineStyles[prop.lStyle]))
        self.cStyleCB.setCurrentIndex(self.cStyleCB.findText(NamedCurveStyles[prop.cStyle]))
        self.sSizeSB.setValue(max(prop.sSize, -1))
        self.lWidthSB.setValue(max(prop.lWidth, -1))
        if prop.sColor is None:
            index = 0
        else:
            index = self.sColorCB.findData(Qt.QColor(prop.sColor))
        if index == -1:
            index = self.sColorCB.count()
            self.sColorCB.addItem(self._colorIcon(Qt.QColor(prop.sColor)), '', Qt.QColor(prop.sColor))
        self.sColorCB.setCurrentIndex(index)
        if prop.lColor is None:
            index = 0
        else:
            index = self.lColorCB.findData(Qt.QColor(prop.lColor))
        if index == -1:
            index = self.lColorCB.count()
            self.lColorCB.addItem(self._colorIcon(Qt.QColor(prop.lColor)), '', Qt.QColor(prop.lColor))
        self.lColorCB.setCurrentIndex(index)
        if prop.sFill is None:
            checkState = Qt.Qt.PartiallyChecked
        elif prop.sFill:
            checkState = Qt.Qt.Checked
        else:
            checkState = Qt.Qt.Unchecked
        if prop.cFill is None:
            checkState = Qt.Qt.PartiallyChecked
        elif prop.cFill:
            checkState = Qt.Qt.Checked
        else:
            checkState = Qt.Qt.Unchecked
        self.cFillCB.setCheckState(checkState)
        return

    def onControlChanged(self, *args):
        """slot to be called whenever a control widget is changed. It emmits a
        'controlChanged signal and applies the change if in autoapply mode.
        It ignores any arguments passed"""
        self.controlChanged.emit()
        if self.autoApply:
            self.onApply()

    def onSelectedCurveChanged(self):
        """Updates the shown properties when the curve selection changes"""
        plist = [ self.curvePropDict[name] for name in self.getSelectedCurveNames()
                ]
        if len(plist) == 0:
            plist = [
             CurveAppearanceProperties()]
        self._shownProp = CurveAppearanceProperties.merge(plist)
        self.showProperties(self._shownProp)

    def _onSymbolStyleChanged(self, text):
        """Slot called when the Symbol style is changed, to ensure that symbols
        are visible if you choose them

        :param text: (str) the new symbol style label
        """
        text = str(text)
        if self.sSizeSB.value() < 2 and text not in ('', 'No symbol'):
            self.sSizeSB.setValue(3)

    def getShownProperties(self):
        """Returns a copy of the currently shown properties and updates
        self._shownProp

        :return: (CurveAppearanceProperties)
        """
        prop = CurveAppearanceProperties()
        prop.sStyle = ReverseNamedSymbolStyles[str(self.sStyleCB.currentText())]
        prop.lStyle = ReverseNamedLineStyles[str(self.lStyleCB.currentText())]
        prop.cStyle = ReverseNamedCurveStyles[str(self.cStyleCB.currentText())]
        prop.sSize = self.sSizeSB.value()
        prop.lWidth = self.lWidthSB.value()
        if prop.sSize < 0:
            prop.sSize = None
        if prop.lWidth < 0:
            prop.lWidth = None
        index = self.sColorCB.currentIndex()
        if index == 0:
            prop.sColor = None
        else:
            prop.sColor = Qt.QColor(self.sColorCB.itemData(index))
        index = self.lColorCB.currentIndex()
        if index == 0:
            prop.lColor = None
        else:
            prop.lColor = Qt.QColor(self.lColorCB.itemData(index))
        checkState = self.sFillCB.checkState()
        if checkState == Qt.Qt.PartiallyChecked:
            prop.sFill = None
        else:
            prop.sFill = bool(checkState)
        checkState = self.cFillCB.checkState()
        if checkState == Qt.Qt.PartiallyChecked:
            prop.cFill = None
        else:
            prop.cFill = bool(checkState)
        self._shownProp = copy.deepcopy(prop)
        return copy.deepcopy(prop)

    def onApply(self):
        """Apply does 2 things:

            - It updates `self.curvePropDict` using the current values
              choosen in the dialog
            - It emits a curveAppearanceChanged signal that indicates the names
              of the curves that changed and the new properties. (The names and
              the properties are returned by the function as well)

        :return: (tuple<CurveAppearanceProperties,list>) a tuple containing the
                 curve properties and a list of the selected curve names (as a
                 list<str>)
        """
        names = self.getSelectedCurveNames()
        prop = self.getShownProperties()
        for n in names:
            self.curvePropDict[n] = CurveAppearanceProperties.merge([self.curvePropDict[n], prop], conflict=CurveAppearanceProperties.inConflict_update_a)

        self.curveAppearanceChanged.emit(prop, names)
        return (
         prop, names)

    def onReset(self):
        """slot to be called when the reset action is triggered. It reverts to
        the original situation"""
        self.setCurves(self._curvePropDictOrig)
        self.curvesLW.clearSelection()

    def _colorIcon(self, color, w=10, h=10):
        pixmap = Qt.QPixmap(w, h)
        pixmap.fill(Qt.QColor(color))
        return Qt.QIcon(pixmap)


class CurveAppearanceProperties(object):
    """An object describing the appearance of a TaurusCurve"""

    def __init__(self, sStyle=None, sSize=None, sColor=None, sFill=None, lStyle=None, lWidth=None, lColor=None, cStyle=None, yAxis=None, cFill=None, title=None, visible=None):
        """
        Creator of :class:`CurveAppearanceProperties`
        Possible keyword arguments are:
            - sStyle= symbolstyle
            - sSize= int
            - sColor= color
            - sFill= bool
            - lStyle= linestyle
            - lWidth= int
            - lColor= color
            - cStyle= curvestyle
            - cFill= bool
            - yAxis= axis
            - visible = bool
            - title= title

        Where:
            - color is a color that QColor() understands (i.e. a
              Qt.Qt.GlobalColor, a color name, or a Qt.Qcolor)
            - symbolstyle is one of Qwt5.QwtSymbol.Style
            - linestyle is one of Qt.Qt.PenStyle
            - curvestyle is one of Qwt5.QwtPlotCurve.CurveStyle
            - axis is one of Qwt5.QwtPlot.Axis
            - title is something that Qwt5.QwtText() accepts in its constructor
              (i.e. a QwtText or a string type)
        """
        self.sStyle = sStyle
        self.sSize = sSize
        self.sColor = sColor
        self.sFill = sFill
        self.lStyle = lStyle
        self.lWidth = lWidth
        self.lColor = lColor
        self.cStyle = cStyle
        self.cFill = cFill
        self.yAxis = yAxis
        self.title = title
        self.visible = visible
        self.propertyList = ['sStyle', 'sSize', 'sColor', 'sFill', 'lStyle', 'lWidth',
         'lColor', 'cStyle', 'cFill', 'yAxis', 'title', 'visible']

    def _print(self):
        """Just for debug"""
        print('-' * 77)
        for k in self.propertyList:
            print(k + '= ', self.__getattribute__(k))

        print('-' * 77)

    @staticmethod
    def inConflict_update_a(a, b):
        """This  function can be passed to CurvesAppearance.merge()
        if one wants to update prop1 with prop2 except for those
        attributes of prop2 that are set to None"""
        if b is None:
            return a
        else:
            return b
            return

    @staticmethod
    def inConflict_none(a, b):
        """In case of conflict, returns None"""
        return

    def conflictsWith(self, other, strict=True):
        """returns a list of attribute names that are in conflict between this self and other"""
        result = []
        for aname in self.propertyList:
            vself = getattr(self, aname)
            vother = getattr(other, aname)
            if vself != vother and (strict or not (vself is None or vother is None)):
                result.append(aname)

        return result

    @classmethod
    def merge(self, plist, attributes=None, conflict=None):
        """returns a CurveAppearanceProperties object formed by merging a list
        of other CurveAppearanceProperties objects

        **Note:** This is a class method, so it can be called without previously
        instantiating an object

        :param plist: (sequence<CurveAppearanceProperties>) objects to be merged
        :param attributes: (sequence<str>) the name of the attributes to
                           consider for the merge. If None, all the attributes
                           will be merged
        :param conflict: (callable) a function that takes 2 objects (having a
                         different attribute)and returns a value that solves the
                         conflict. If None is given, any conflicting attribute
                         will be set to None.

        :return: (CurveAppearanceProperties) merged properties
        """
        n = len(plist)
        if n < 1:
            raise ValueError('plist must contain at least 1 member')
        plist = copy.deepcopy(plist)
        if n == 1:
            return plist[0]
        else:
            if attributes is None:
                attributes = [
                 'sStyle', 'sSize', 'sColor', 'sFill', 'lStyle',
                 'lWidth', 'lColor', 'cStyle', 'cFill', 'yAxis', 'title']
            if conflict is None:
                conflict = CurveAppearanceProperties.inConflict_none
            p = CurveAppearanceProperties()
            for a in attributes:
                alist = [ p.__getattribute__(a) for p in plist ]
                p.__setattr__(a, alist[0])
                for ai in alist[1:]:
                    if alist[0] != ai:
                        p.__setattr__(a, conflict(alist[0], ai))
                        break

            return p

    def applyToCurve(self, curve):
        """applies the current properties to a given curve
        If a property is set to None, it is not applied to the curve"""
        raise DeprecationWarning('CurveAppearanceProperties.applyToCurve() is deprecated. Use TaurusCurve.setAppearanceProperties() instead')
        curve.setAppearanceProperties(self)