# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/popupviews/PopupViewContentsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label, PopupView, TextField
from muntjac.ui import popup_view

class PopupViewContentsExample(VerticalLayout):

    def __init__(self):
        super(PopupViewContentsExample, self).__init__()
        self.setSpacing(True)
        content = Label('This is a simple Label component inside the popup. You can place any Muntjac components here.')
        content.setWidth('300px')
        popup = PopupView('Static HTML content', content)
        self.addComponent(popup)
        popup = PopupView(PopupTextField())
        popup.setDescription('Click to edit')
        popup.setHideOnMouseOut(False)
        self.addComponent(popup)


class PopupTextField(popup_view.IContent):

    def __init__(self):
        self._root = VerticalLayout()
        self._tf = TextField('Edit me')
        self._root.setSizeUndefined()
        self._root.setSpacing(True)
        self._root.setMargin(True)
        self._root.addComponent(Label('The changes made to any components inside the popup are reflected automatically when the popup is closed, but you might want to provide explicit action buttons for the user, like "Save" or "Close".'))
        self._root.addComponent(self._tf)
        self._tf.setValue('Initial dynamic content')
        self._tf.setWidth('300px')

    def getMinimizedValueAsHTML(self):
        return str(self._tf.getValue())

    def getPopupComponent(self):
        return self._root