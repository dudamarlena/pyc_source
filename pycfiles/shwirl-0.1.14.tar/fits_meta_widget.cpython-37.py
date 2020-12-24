# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/interface/widgets/fits_meta_widget.py
# Compiled at: 2018-10-01 15:07:29
# Size of source mod 2**32: 1683 bytes
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QColor

class FitsMetaWidget(QWidget):
    __doc__ = 'Widget to render the FITS HDU information'

    def __init__(self, parent=None):
        """Initialise the layout, including QTextEdit widget.
        """
        super(FitsMetaWidget, self).__init__(parent)
        l_title = QLabel('Fits Primary Header')
        self.l_header = QTextEdit('No fits loaded ')
        self.l_header.setReadOnly(True)
        font = self.l_header.font()
        font.setFamily('Avenir')
        font.setPointSize(12)
        gbox = QGridLayout()
        gbox.addWidget(l_title, 0, 1)
        gbox.addWidget(self.l_header, 1, 1)
        vbox = QVBoxLayout()
        vbox.addLayout(gbox)
        vbox.addStretch(1.0)
        self.setLayout(vbox)

    def print_header(self, header):
        """Print the Primary HDU information of the fits file

        Parameters
        ----------
            header : astropy.io.fits.header, dict
                HDU taken from a fits file.
        """
        self.l_header.clear()
        self.l_header.insertPlainText('card\tvalue\tcomment\n')
        for card in header.cards:
            self.l_header.setTextColor(QColor('blue'))
            self.l_header.insertPlainText(str(card[0]) + '\t')
            self.l_header.setTextColor(QColor('black'))
            self.l_header.insertPlainText(str(card[1]) + '\t')
            self.l_header.setTextColor(QColor('red'))
            self.l_header.insertPlainText(str(card[2]) + '\n')

        sb = self.l_header.verticalScrollBar()
        sb.setValue(sb.maximum())