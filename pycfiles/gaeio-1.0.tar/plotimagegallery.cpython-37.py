# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\plotimagegallery.py
# Compiled at: 2019-12-16 00:14:23
# Size of source mod 2**32: 7300 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.vis.colormap as vis_cmap
import cognitivegeo.src.vis.image as vis_image
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class plotimagegallery(object):
    title = 'Plot Image Gallery'
    icon = 'image.png'
    imagelist = []
    imagestyle = core_set.Visual['Image']
    imagestyle['Flipped'] = False
    imageidx = 0
    ncol = 1
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, PlotImageGallery):
        PlotImageGallery.setObjectName('PlotImageGallery')
        PlotImageGallery.setFixedSize(500, 210)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/' + self.icon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PlotImageGallery.setWindowIcon(icon)
        self.lbltype = QtWidgets.QLabel(PlotImageGallery)
        self.lbltype.setObjectName('lbltype')
        self.lbltype.setGeometry(QtCore.QRect(10, 10, 80, 30))
        self.cbbtype = QtWidgets.QComboBox(PlotImageGallery)
        self.cbbtype.setObjectName('cbbtype')
        self.cbbtype.setGeometry(QtCore.QRect(90, 10, 400, 30))
        self.lblcmap = QtWidgets.QLabel(PlotImageGallery)
        self.lblcmap.setObjectName('lblcmap')
        self.lblcmap.setGeometry(QtCore.QRect(10, 60, 80, 30))
        self.cbbcmap = QtWidgets.QComboBox(PlotImageGallery)
        self.cbbcmap.setObjectName('cbbcmap')
        self.cbbcmap.setGeometry(QtCore.QRect(90, 60, 100, 30))
        self.cbxflip = QtWidgets.QCheckBox(PlotImageGallery)
        self.cbxflip.setObjectName('cbxflip')
        self.cbxflip.setGeometry(QtCore.QRect(200, 60, 40, 30))
        self.lblinterp = QtWidgets.QLabel(PlotImageGallery)
        self.lblinterp.setObjectName('lblinterp')
        self.lblinterp.setGeometry(QtCore.QRect(260, 60, 80, 30))
        self.cbbinterp = QtWidgets.QComboBox(PlotImageGallery)
        self.cbbinterp.setObjectName('cbbinterp')
        self.cbbinterp.setGeometry(QtCore.QRect(340, 60, 150, 30))
        self.lblncol = QtWidgets.QLabel(PlotImageGallery)
        self.lblncol.setObjectName('lblncol')
        self.lblncol.setGeometry(QtCore.QRect(10, 110, 80, 30))
        self.cbbncol = QtWidgets.QComboBox(PlotImageGallery)
        self.cbbncol.setObjectName('cbbncol')
        self.cbbncol.setGeometry(QtCore.QRect(90, 110, 150, 30))
        self.btnapply = QtWidgets.QPushButton(PlotImageGallery)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(170, 160, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/ok.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(PlotImageGallery)
        self.msgbox.setObjectName('msgbox')
        _center_x = PlotImageGallery.geometry().center().x()
        _center_y = PlotImageGallery.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(PlotImageGallery)
        QtCore.QMetaObject.connectSlotsByName(PlotImageGallery)

    def retranslateGUI(self, PlotImageGallery):
        self.dialog = PlotImageGallery
        _translate = QtCore.QCoreApplication.translate
        PlotImageGallery.setWindowTitle(_translate('PlotImageGallery', self.title))
        self.lbltype.setText(_translate('PlotImageGallery', 'Select:'))
        self.cbbtype.addItems(self.imagelist)
        self.lblcmap.setText(_translate('PlotImageGallery', 'Color map:'))
        self.cbbcmap.addItems(vis_cmap.ColorMapList)
        for _i in range(len(vis_cmap.ColorMapList)):
            self.cbbcmap.setItemIcon(_i, QtGui.QIcon(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/cmap_' + vis_cmap.ColorMapList[_i] + '.png')).scaled(80, 30)))

        self.cbbcmap.setCurrentIndex(list.index(vis_cmap.ColorMapList, self.imagestyle['Colormap']))
        self.cbxflip.setText(_translate('PlotImageGallery', ''))
        self.cbxflip.setIcon(QtGui.QIcon(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/flip.png')).scaled(80, 80)))
        self.cbxflip.setChecked(self.imagestyle['Flipped'])
        self.lblinterp.setText(_translate('PlotImageGallery', 'Interpolation:'))
        self.cbbinterp.addItems(vis_image.InterpolationList)
        for _i in range(len(vis_image.InterpolationList)):
            self.cbbinterp.setItemIcon(_i, QtGui.QIcon(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/interp_' + vis_image.InterpolationList[_i] + '.png')).scaled(80, 40)))

        self.cbbinterp.setCurrentIndex(list.index(vis_image.InterpolationList, self.imagestyle['Interpolation']))
        self.lblncol.setText(_translate('PlotImageGallery', 'Image per row:'))
        self.cbbncol.addItems([str(i + 1) for i in range(20)])
        self.btnapply.setText(_translate('PlotImageGallery', 'Apply'))
        self.btnapply.clicked.connect(self.clickBtnApply)

    def clickBtnApply(self):
        self.imageidx = self.cbbtype.currentIndex()
        self.imagestyle['Colormap'] = vis_cmap.ColorMapList[self.cbbcmap.currentIndex()]
        self.imagestyle['Interpolation'] = vis_image.InterpolationList[self.cbbinterp.currentIndex()]
        self.imagestyle['Flipped'] = self.cbxflip.isChecked()
        self.ncol = int(self.cbbncol.currentIndex()) + 1
        self.dialog.close()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PlotImageGallery = QtWidgets.QWidget()
    gui = plotimagegallery()
    gui.setupGUI(PlotImageGallery)
    PlotImageGallery.show()
    sys.exit(app.exec_())