# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/SplitPanelPositioningExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.terminal.sizeable import ISizeable
from muntjac.data.property import IValueChangeListener
from muntjac.api import VerticalLayout, HorizontalLayout, VerticalSplitPanel, Label, HorizontalSplitPanel, OptionGroup, Alignment

class SplitPanelPositioningExample(VerticalLayout):

    def __init__(self):
        super(SplitPanelPositioningExample, self).__init__()
        self.setStyleName('split-panel-positioning-example')
        self.setSpacing(True)
        controls = HorizontalLayout()
        controls.setSpacing(True)
        self.addComponent(controls)
        self._verticalSplitPanel = VerticalSplitPanel()
        self._verticalSplitPanel.setSplitPosition(100, ISizeable.UNITS_PIXELS)
        self._verticalSplitPanel.setLocked(True)
        self._verticalSplitPanel.setHeight('450px')
        self._verticalSplitPanel.setWidth('100%')
        self.addComponent(self._verticalSplitPanel)
        topArea = Label()
        topArea.setStyleName('top-area')
        topArea.addStyleName('measured-from-top')
        topArea.setSizeFull()
        self._verticalSplitPanel.addComponent(topArea)
        self._horizontalSplitPanel = HorizontalSplitPanel()
        self._horizontalSplitPanel.setSplitPosition(30, ISizeable.UNITS_PERCENTAGE)
        self._horizontalSplitPanel.setSizeFull()
        self._horizontalSplitPanel.setLocked(True)
        self._verticalSplitPanel.addComponent(self._horizontalSplitPanel)
        leftArea = Label()
        leftArea.setStyleName('left-area')
        leftArea.addStyleName('measured-from-left')
        leftArea.setSizeFull()
        self._horizontalSplitPanel.addComponent(leftArea)
        rightArea = Label()
        rightArea.setStyleName('right-area')
        rightArea.setSizeFull()
        self._horizontalSplitPanel.addComponent(rightArea)
        self._measurePositionFromLeft = OptionGroup('Horizontal split position', [
         '30% from left', '30% from right'])
        self._measurePositionFromLeft.setValue('30% from left')
        self._measurePositionFromLeft.setImmediate(True)
        l = LeftRightListener(self, leftArea, rightArea)
        self._measurePositionFromLeft.addListener(l, IValueChangeListener)
        controls.addComponent(self._measurePositionFromLeft)
        controls.setComponentAlignment(self._measurePositionFromLeft, Alignment.MIDDLE_CENTER)
        self._measurePositionFromTop = OptionGroup('Vertical split position', [
         '100px from top', '100px from bottom'])
        self._measurePositionFromTop.setValue('100px from top')
        self._measurePositionFromTop.setImmediate(True)
        l = TopBottomListener(self, leftArea, rightArea, topArea)
        self._measurePositionFromTop.addListener(l, IValueChangeListener)
        controls.addComponent(self._measurePositionFromTop)
        controls.setComponentAlignment(self._measurePositionFromTop, Alignment.MIDDLE_CENTER)


class LeftRightListener(IValueChangeListener):

    def __init__(self, c, leftArea, rightArea):
        self._c = c
        self._leftArea = leftArea
        self._rightArea = rightArea

    def valueChange(self, event):
        if event.getProperty().getValue() == '30% from right':
            self._leftArea.removeStyleName('measured-from-left')
            self._rightArea.removeStyleName('measured-from-bottom')
            self._rightArea.addStyleName('measured-from-right')
            self._c._horizontalSplitPanel.setSplitPosition(30, ISizeable.UNITS_PERCENTAGE, True)
        else:
            self._rightArea.removeStyleName('measured-from-right')
            self._leftArea.removeStyleName('measured-from-bottom')
            self._leftArea.addStyleName('measured-from-left')
            self._c._horizontalSplitPanel.setSplitPosition(30, ISizeable.UNITS_PERCENTAGE, False)


class TopBottomListener(IValueChangeListener):

    def __init__(self, c, leftArea, rightArea, topArea):
        self._c = c
        self._leftArea = leftArea
        self._rightArea = rightArea
        self._topArea = topArea

    def valueChange(self, event):
        if event.getProperty().getValue() == '100px from bottom':
            self._topArea.removeStyleName('measured-from-top')
            if self._c._measurePositionFromLeft.getValue() == '30% from left':
                self._rightArea.addStyleName('measured-from-bottom')
            else:
                self._leftArea.addStyleName('measured-from-bottom')
            self._c._verticalSplitPanel.setSplitPosition(100, ISizeable.UNITS_PIXELS, True)
        else:
            if self._c._measurePositionFromLeft.getValue() == '30% from left':
                self._rightArea.removeStyleName('measured-from-bottom')
            else:
                self._leftArea.removeStyleName('measured-from-bottom')
            self._topArea.addStyleName('measured-from-top')
            self._c._verticalSplitPanel.setSplitPosition(100, ISizeable.UNITS_PIXELS, False)