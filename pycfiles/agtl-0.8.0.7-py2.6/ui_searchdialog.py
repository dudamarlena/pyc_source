# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/qt/ui_searchdialog.py
# Compiled at: 2011-04-23 08:43:29
from PyQt4 import QtCore, QtGui

class Ui_SearchDialog(object):

    def setupUi(self, SearchDialog):
        SearchDialog.setObjectName('SearchDialog')
        SearchDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(SearchDialog)
        self.verticalLayout.setObjectName('verticalLayout')
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.lineEditSearch = QtGui.QLineEdit(SearchDialog)
        self.lineEditSearch.setObjectName('lineEditSearch')
        self.horizontalLayout.addWidget(self.lineEditSearch)
        self.pushButtonSearch = QtGui.QPushButton(SearchDialog)
        self.pushButtonSearch.setObjectName('pushButtonSearch')
        self.horizontalLayout.addWidget(self.pushButtonSearch)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidgetResults = QtGui.QListWidget(SearchDialog)
        self.listWidgetResults.setObjectName('listWidgetResults')
        self.verticalLayout.addWidget(self.listWidgetResults)
        self.retranslateUi(SearchDialog)
        QtCore.QMetaObject.connectSlotsByName(SearchDialog)

    def retranslateUi(self, SearchDialog):
        SearchDialog.setWindowTitle(QtGui.QApplication.translate('SearchDialog', 'Search Place', None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSearch.setText(QtGui.QApplication.translate('SearchDialog', 'Search', None, QtGui.QApplication.UnicodeUTF8))
        return