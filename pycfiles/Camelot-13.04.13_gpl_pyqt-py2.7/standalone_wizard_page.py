# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/standalone_wizard_page.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget
from camelot.view.model_thread import object_thread
from camelot.core.utils import ugettext_lazy as _

class HSeparator(QFrame):

    def __init__(self, parent=None):
        super(HSeparator, self).__init__(parent)
        self.setFrameStyle(QFrame.HLine | QFrame.Sunken)


class StandaloneWizardPage(QDialog):
    """A Standalone Wizard Page Dialog for quick configuration windows"""

    def __init__(self, window_title=None, parent=None, flags=Qt.Dialog):
        super(StandaloneWizardPage, self).__init__(parent, flags)
        self.setWindowTitle(unicode(window_title or ' '))
        self.set_layouts()

    def set_layouts(self):
        assert object_thread(self)
        self._vlayout = QVBoxLayout()
        self._vlayout.setSpacing(0)
        self._vlayout.setContentsMargins(0, 0, 0, 0)
        banner_layout = QGridLayout()
        banner_layout.setColumnStretch(0, 1)
        banner_layout.addWidget(QLabel(), 0, 1, Qt.AlignRight)
        banner_layout.addLayout(QVBoxLayout(), 0, 0)
        banner_widget = QWidget()
        banner_widget.setLayout(banner_layout)
        self._vlayout.addWidget(banner_widget)
        self._vlayout.addWidget(HSeparator())
        self._vlayout.addWidget(QFrame(), 1)
        self._vlayout.addWidget(HSeparator())
        self._vlayout.addWidget(QWidget())
        self.setLayout(self._vlayout)

    def banner_widget(self):
        return self._vlayout.itemAt(0).widget()

    def main_widget(self):
        return self._vlayout.itemAt(2).widget()

    def buttons_widget(self):
        return self._vlayout.itemAt(4).widget()

    def banner_layout(self):
        return self.banner_widget().layout()

    def banner_logo_holder(self):
        return self.banner_layout().itemAtPosition(0, 1).widget()

    def banner_text_layout(self):
        return self.banner_layout().itemAtPosition(0, 0).layout()

    def set_banner_logo_pixmap(self, pixmap):
        self.banner_logo_holder().setPixmap(pixmap)

    def set_banner_title(self, title):
        title_widget = QLabel('<dt><b>%s</b></dt>' % title)
        self.banner_text_layout().insertWidget(0, title_widget)

    def set_banner_subtitle(self, subtitle):
        subtitle_widget = QLabel('<dd>%s</dd>' % subtitle)
        self.banner_text_layout().insertWidget(1, subtitle_widget)

    def set_default_buttons(self, accept=_('OK'), reject=_('Cancel'), done=None):
        """add an :guilabel:`ok` and a :guilabel:`cancel` button.
        """
        layout = QtGui.QHBoxLayout()
        layout.setDirection(QtGui.QBoxLayout.RightToLeft)
        if accept != None:
            ok_button = QtGui.QPushButton(unicode(accept), self)
            ok_button.setObjectName('accept')
            ok_button.pressed.connect(self.accept)
            layout.addWidget(ok_button)
        if reject != None:
            cancel_button = QtGui.QPushButton(unicode(reject), self)
            cancel_button.setObjectName('reject')
            cancel_button.pressed.connect(self.reject)
            layout.addWidget(cancel_button)
        layout.addStretch()
        self.buttons_widget().setLayout(layout)
        return