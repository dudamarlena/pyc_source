# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/qtgui/genaboutdialog.py
# Compiled at: 2006-01-31 15:27:30
import sys
from qt import *
image0_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x01\xacIDAT8\x8d\xc5\xd3?HU\x01\x14\xc7\xf1\xcf\xbd\xef\xbe\xe7C\t\x85G\x86\xa99\xbcA\x08j\x10\xcaj\x08lo\xb3\xdaBJ\xa4)\x82\xa0\x90\x96\xa0\xa5\xcd\x96\x96\x1a\x84\xa2\xa5\x16\x03\xe15\x84[B\xbaT\xd0\x1f\xb0\xa0L0^h/\xcb|\xff\xae\xb7\xa1@\x93\xb4\xc1\xa1\xb3\x9c\xdf\x19\xbe\x1c\xf8\x9d\xdf\t\x92$\xb1\x9d\n\xb7E#0\xa2S\xddG\xcb\xf8\x81\x15\xd4\x11!\x83\xf4:\x1d\xfd\x9e3\xf2\x99\x06gS)\xfb"\xb1\x87\xea\xae\xa0\xb0\xe5\xaa\x04\xabv\xe3\x8c\xba\xa1j]9\x88\x9c\x08\xc38\xac\xa5\xb3\xe9\xbbj\xfa6\x05\xabr\xb8\xdc\xd2\xd12\xd1\xd6\xd1v\xcd\x8aY\x15\xc7\xf0<L\x96\x92\xfb\xb9\xbd\xb9\\vO\xf6\x8e\xb2\xc3\x82up\xcd.\xb1sQ{\xf4\xa4\xfdx\xfb\xf5\xe6\xce\xe6\xee\xe2L\xb1\xa0\xe2\xa4\xc0\x1cDI)\x99^,/V\xc3\xfe\xb0\xc3\xa2{\xde\xeb\xc7+U\x03\xba\x0c\x04G\x82\xde\xcc\x81\x8c\xd2\xd3\x92\xe5\xc2\xf2\x03)C\xb2Jk&\x0ej\xd5\xa5\xe0\x82\x1eE\x8czg\xc5\x82\xa3\x0e:\x84\x9d\x18\xc3\xb8\x1b\x1a]\xb5\xc3W\x19d\t\x1a\x89\xac*zk\xcak=\xbaqJ^(\xaf\r5\xdcT7eD\x83a)\xf1F\x8bB\x15|7\xed\x85X\x11\rh\xc2\x07\xdc\xc2\x84a\x89K\x7f\x83!\xf2\r\xb1I\xcf,\xd8\xafU\x1as\x18S6\xe3\xbc&\xb7\xb7\x8a[$F\xec\x8d9/}\xd2\xaa\x8aq_\xcc\xba\xa8\xd1\xe8\xbf\xb2\x1a\xa9a\x15\x15\x13&\xf5\x99\xf7\xd9\xac\xd3"\x8f\xfe8\xe9&\x95\x92G\x80D\xd9\xbc^K\x06E\x1e\x0b\xacEwcO\xfd\xd2A\x9a\xe0\xbf\x7f\xe3O\xae\x03\x8b\xee\x04\xa5\xca\xcf\x00\x00\x00\x00IEND\xaeB`\x82'

class AboutDialog(QDialog):
    __module__ = __name__

    def __init__(self, parent=None, name=None, modal=0, fl=0):
        QDialog.__init__(self, parent, name, modal, fl)
        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data, 'PNG')
        if not name:
            self.setName('AboutDialog')
        self.setMinimumSize(QSize(300, 200))
        AboutDialogLayout = QVBoxLayout(self, 6, 6, 'AboutDialogLayout')
        AboutDialogLayout.setResizeMode(QLayout.Minimum)
        self.frame11 = QFrame(self, 'frame11')
        self.frame11.setFrameShape(QFrame.StyledPanel)
        self.frame11.setFrameShadow(QFrame.Raised)
        frame11Layout = QVBoxLayout(self.frame11, 6, 6, 'frame11Layout')
        self.title_label = QLabel(self.frame11, 'title_label')
        self.title_label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum, 0, 0, self.title_label.sizePolicy().hasHeightForWidth()))
        self.title_label.setTextFormat(QLabel.RichText)
        self.title_label.setAlignment(QLabel.AlignVCenter)
        frame11Layout.addWidget(self.title_label)
        self.text_label = QLabel(self.frame11, 'text_label')
        self.text_label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed, 0, 0, self.text_label.sizePolicy().hasHeightForWidth()))
        frame11Layout.addWidget(self.text_label)
        self.running_psyco_textLabel = QLabel(self.frame11, 'running_psyco_textLabel')
        self.running_psyco_textLabel.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum, 0, 0, self.running_psyco_textLabel.sizePolicy().hasHeightForWidth()))
        self.running_psyco_textLabel.setAlignment(QLabel.AlignCenter)
        frame11Layout.addWidget(self.running_psyco_textLabel)
        AboutDialogLayout.addWidget(self.frame11)
        self.about_ok_button = QPushButton(self, 'about_ok_button')
        self.about_ok_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed, 0, 0, self.about_ok_button.sizePolicy().hasHeightForWidth()))
        self.about_ok_button.setDefault(1)
        self.about_ok_button.setIconSet(QIconSet(self.image0))
        self.about_ok_button.setFlat(0)
        AboutDialogLayout.addWidget(self.about_ok_button)
        self.languageChange()
        self.resize(QSize(323, 200).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        self.connect(self.about_ok_button, SIGNAL('clicked()'), self.about_ok_button_clicked)

    def languageChange(self):
        self.setCaption(self.__tr('About ...'))
        self.title_label.setText(self.__tr('<p align="center"><font size="+3"><b>S<font size="+2">LOSL</font> Overlay Workbench V[VT]</b></font>\n<br />\n<br />\n<b>by Stefan Behnel</b>\n<br />\n<br />\nDesigning overlays in no-time!</p>'))
        self.text_label.setText(QString.null)
        self.running_psyco_textLabel.setText(self.__tr('- running psyco -'))
        self.about_ok_button.setText(self.__tr('&OK'))
        self.about_ok_button.setAccel(self.__tr('Alt+O'))

    def about_ok_button_clicked(self):
        print 'AboutDialog.about_ok_button_clicked(): Not implemented yet'

    def __tr(self, s, c=None):
        return qApp.translate('AboutDialog', s, c)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a, SIGNAL('lastWindowClosed()'), a, SLOT('quit()'))
    w = AboutDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()