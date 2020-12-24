# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/user_translatable_label.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from camelot.core.utils import ugettext_lazy
from camelot.core.utils import ugettext as _
from camelot.view.art import Icon

class TranslateLabelAction(QtGui.QAction):
    translate_icon = Icon('tango/16x16/apps/preferences-desktop-locale.png')

    def __init__(self, parent):
        super(TranslateLabelAction, self).__init__(_('Change translation'), parent)
        self.setIcon(self.translate_icon.getQIcon())


class UserTranslatableLabel(QtGui.QLabel):
    """A QLabel that allows the user to translate the text contained 
within by right clicking on it and selecting the appropriate submenu.
"""

    def __init__(self, text, parent=None):
        """:param text: the text to be displayed within the label, this can
        be either a normal string or a ugettext_lazy string, only in the last
        case, the label will be translatable"""
        super(UserTranslatableLabel, self).__init__(unicode(text), parent)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        if isinstance(text, ugettext_lazy):
            self._text = text
            translate_action = TranslateLabelAction(self)
            translate_action.triggered.connect(self.change_translation)
            self.addAction(translate_action)
        else:
            self._text = None
        return

    @QtCore.pyqtSlot()
    def change_translation(self):
        if self._text:
            new_translation, ok = QtGui.QInputDialog.getText(self, _('Change translation'), _('Translation'), QtGui.QLineEdit.Normal, unicode(self._text))
            new_translation = unicode(new_translation).strip()
            if ok and new_translation:
                from camelot.core.utils import set_translation
                self.setText(new_translation)
                set_translation(self._text._string_to_translate, new_translation)
                from camelot.view.model_thread import post
                post(self.create_update_translation_table(self._text._string_to_translate, unicode(QtCore.QLocale().name()), unicode(new_translation)))

    def create_update_translation_table(self, source, language, value):

        def update_translation_table():
            from camelot.model.i18n import Translation
            from sqlalchemy.orm.session import Session
            t = Translation.get_by(source=source, language=language)
            if not t:
                t = Translation(source=source, language=language)
            t.value = value
            Session.object_session(t).flush([t])

        return update_translation_table