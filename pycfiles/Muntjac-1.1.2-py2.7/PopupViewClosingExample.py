# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/popupviews/PopupViewClosingExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label, PopupView
from muntjac.ui.popup_view import IPopupVisibilityListener

class PopupViewClosingExample(VerticalLayout, IPopupVisibilityListener):

    def __init__(self):
        super(PopupViewClosingExample, self).__init__()
        self.setSpacing(True)
        content = Label('This popup will close as soon as you move the mouse cursor outside of the popup area.')
        content.setWidth('300px')
        popup = PopupView('Default popup', content)
        popup.setHideOnMouseOut(True)
        popup.addListener(self, IPopupVisibilityListener)
        self.addComponent(popup)
        content = Label('This popup will only close if you click the mouse outside the popup area.')
        content.setWidth('300px')
        popup = PopupView("Popup that won't auto-close", content)
        popup.setHideOnMouseOut(False)
        popup.addListener(self, IPopupVisibilityListener)
        self.addComponent(popup)

    def popupVisibilityChange(self, event):
        if not event.isPopupVisible():
            self.getWindow().showNotification('Popup closed')