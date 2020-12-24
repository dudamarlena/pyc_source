# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/languageeditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from customeditor import AbstractCustomEditor

class LanguageEditor(QtGui.QComboBox, AbstractCustomEditor):
    """A ComboBox that shows a list of languages, the editor takes
    as its value the ISO code of the language"""
    editingFinished = QtCore.pyqtSignal()
    language_choices = []

    def __init__(self, parent=None, languages=[], field_name='language', **kwargs):
        """
        :param languages: a list of ISO codes with languages
        that are allowed in the combo box, if the list is empty, all languages
        are allowed (the default)
        """
        QtGui.QComboBox.__init__(self, parent)
        AbstractCustomEditor.__init__(self)
        self.setObjectName(field_name)
        self.index_by_language = dict()
        languages = [ QtCore.QLocale(lang).language() for lang in languages ]
        if not self.language_choices:
            for language in range(QtCore.QLocale.C, QtCore.QLocale.Chewa + 1):
                if languages and language not in languages:
                    continue
                language_name = unicode(QtCore.QLocale.languageToString(language))
                self.language_choices.append((language, language_name))

            self.language_choices.sort(key=lambda x: x[1])
        for i, (language, language_name) in enumerate(self.language_choices):
            self.addItem(language_name, QtCore.QVariant(language))
            self.index_by_language[language] = i

        self.activated.connect(self._activated)

    @QtCore.pyqtSlot(int)
    def _activated(self, _index):
        self.editingFinished.emit()

    def set_value(self, value):
        value = AbstractCustomEditor.set_value(self, value)
        if value:
            locale = QtCore.QLocale(value)
            self.setCurrentIndex(self.index_by_language[locale.language()])

    def get_value(self):
        from camelot.core.utils import variant_to_pyobject
        current_index = self.currentIndex()
        if current_index >= 0:
            language = variant_to_pyobject(self.itemData(self.currentIndex()))
            locale = QtCore.QLocale(language)
            value = unicode(locale.name())
        else:
            value = None
        return AbstractCustomEditor.get_value(self) or value