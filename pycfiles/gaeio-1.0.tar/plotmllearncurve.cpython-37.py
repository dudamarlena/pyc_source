# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\plotmllearncurve.py
# Compiled at: 2020-03-17 16:23:40
# Size of source mod 2**32: 22583 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.vis.font as vis_font
import cognitivegeo.src.gui.configlineplotting as gui_configlineplotting
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class plotmllearncurve(object):
    learnmat = []
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    lineplottingconfig = {}

    def setupGUI(self, PlotMlLearnCurve):
        PlotMlLearnCurve.setObjectName('PlotMlLearnCurve')
        PlotMlLearnCurve.setFixedSize(420, 270)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotcurve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PlotMlLearnCurve.setWindowIcon(icon)
        self.lblselect = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblselect.setObjectName('lblselect')
        self.lblselect.setGeometry(QtCore.QRect(10, 10, 60, 30))
        self.lblprocess = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblprocess.setObjectName('lblprocess')
        self.lblprocess.setGeometry(QtCore.QRect(10, 50, 60, 30))
        self.cbbprocess = QtWidgets.QComboBox(PlotMlLearnCurve)
        self.cbbprocess.setObjectName('cbbprocess')
        self.cbbprocess.setGeometry(QtCore.QRect(70, 50, 100, 30))
        self.lblcurve = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblcurve.setObjectName('lblcurve')
        self.lblcurve.setGeometry(QtCore.QRect(10, 90, 60, 30))
        self.cbbcurve = QtWidgets.QComboBox(PlotMlLearnCurve)
        self.cbbcurve.setObjectName('cbbcurve')
        self.cbbcurve.setGeometry(QtCore.QRect(70, 90, 100, 30))
        self.btnconfigline = QtWidgets.QPushButton(PlotMlLearnCurve)
        self.btnconfigline.setObjectName('btnconfigline')
        self.btnconfigline.setGeometry(QtCore.QRect(270, 10, 120, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigline.setIcon(icon)
        self.lblepoch = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblepoch.setObjectName('lblepoch')
        self.lblepoch.setGeometry(QtCore.QRect(210, 50, 60, 30))
        self.ldtepochmin = QtWidgets.QLineEdit(PlotMlLearnCurve)
        self.ldtepochmin.setObjectName('ldtepochmin')
        self.ldtepochmin.setGeometry(QtCore.QRect(270, 50, 50, 30))
        self.ldtepochmin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtepochmax = QtWidgets.QLineEdit(PlotMlLearnCurve)
        self.ldtepochmax.setObjectName('ldtepochmax')
        self.ldtepochmax.setGeometry(QtCore.QRect(340, 50, 50, 30))
        self.ldtepochmax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblepochrangeto = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblepochrangeto.setObjectName('lblepochrangeto')
        self.lblepochrangeto.setGeometry(QtCore.QRect(320, 50, 20, 30))
        self.lblepochrangeto.setAlignment(QtCore.Qt.AlignCenter)
        self.lblaccuracy = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblaccuracy.setObjectName('lblaccuracy')
        self.lblaccuracy.setGeometry(QtCore.QRect(210, 90, 60, 30))
        self.ldtaccuracymin = QtWidgets.QLineEdit(PlotMlLearnCurve)
        self.ldtaccuracymin.setObjectName('ldtaccuracymin')
        self.ldtaccuracymin.setGeometry(QtCore.QRect(270, 90, 50, 30))
        self.ldtaccuracymin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtaccuracymax = QtWidgets.QLineEdit(PlotMlLearnCurve)
        self.ldtaccuracymax.setObjectName('ldtaccuracymax')
        self.ldtaccuracymax.setGeometry(QtCore.QRect(340, 90, 50, 30))
        self.ldtaccuracymax.setAlignment(QtCore.Qt.AlignCenter)
        self.lblaccuracyrangeto = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblaccuracyrangeto.setObjectName('lblaccuracyrangeto')
        self.lblaccuracyrangeto.setGeometry(QtCore.QRect(320, 90, 20, 30))
        self.lblaccuracyrangeto.setAlignment(QtCore.Qt.AlignCenter)
        self.lblloss = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lblloss.setObjectName('lblloss')
        self.lblloss.setGeometry(QtCore.QRect(210, 130, 60, 30))
        self.ldtlossmin = QtWidgets.QLineEdit(PlotMlLearnCurve)
        self.ldtlossmin.setObjectName('ldtlossmin')
        self.ldtlossmin.setGeometry(QtCore.QRect(270, 130, 50, 30))
        self.ldtlossmin.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtlossmax = QtWidgets.QLineEdit(PlotMlLearnCurve)
        self.ldtlossmax.setObjectName('ldtlossmax')
        self.ldtlossmax.setGeometry(QtCore.QRect(340, 130, 50, 30))
        self.ldtlossmax.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllossrangeto = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lbllossrangeto.setObjectName('lbllossrangeto')
        self.lbllossrangeto.setGeometry(QtCore.QRect(320, 130, 20, 30))
        self.lbllossrangeto.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllegend = QtWidgets.QLabel(PlotMlLearnCurve)
        self.lbllegend.setObjectName('lbllegend')
        self.lbllegend.setGeometry(QtCore.QRect(210, 170, 60, 30))
        self.cbblegend = QtWidgets.QComboBox(PlotMlLearnCurve)
        self.cbblegend.setObjectName('cbblegend')
        self.cbblegend.setGeometry(QtCore.QRect(270, 170, 120, 30))
        self.btnapply = QtWidgets.QPushButton(PlotMlLearnCurve)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(130, 220, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/ok.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(PlotMlLearnCurve)
        self.msgbox.setObjectName('msgbox')
        _center_x = PlotMlLearnCurve.geometry().center().x()
        _center_y = PlotMlLearnCurve.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(PlotMlLearnCurve)
        QtCore.QMetaObject.connectSlotsByName(PlotMlLearnCurve)

    def retranslateGUI(self, PlotMlLearnCurve):
        self.dialog = PlotMlLearnCurve
        _translate = QtCore.QCoreApplication.translate
        PlotMlLearnCurve.setWindowTitle(_translate('PlotMlLearnCurve', 'Plot Learning Curve'))
        self.lblselect.setText(_translate('PlotMlLearnCurve', 'Select:'))
        self.lblprocess.setText(_translate('PlotMlLearnCurve', 'Process:'))
        self.cbbprocess.addItems(['Training', 'Validation', 'Both'])
        self.cbbprocess.currentIndexChanged.connect(self.changeCbbProcessCurve)
        self.lblcurve.setText(_translate('PlotMlLearnCurve', 'Curve:'))
        self.cbbcurve.addItems(['Accuracy', 'Loss', 'Both'])
        self.cbbcurve.currentIndexChanged.connect(self.changeCbbProcessCurve)
        self.btnconfigline.setText(_translate('PlotMlLearnCurve', 'Configuration'))
        self.btnconfigline.clicked.connect(self.clickBtnConfigLine)
        self.lblepoch.setText(_translate('PlotMlLearnCurve', 'Epoch:'))
        self.lblepochrangeto.setText(_translate('PlotMlLearnCurve', '~~'))
        self.lblaccuracy.setText(_translate('PlotMlLearnCurve', 'Accuracy:'))
        self.lblaccuracyrangeto.setText(_translate('PlotMlLearnCurve', '~~'))
        self.lblloss.setText(_translate('PlotMlLearnCurve', 'Loss:'))
        self.lbllossrangeto.setText(_translate('PlotMlLearnCurve', '~~'))
        self.lbllegend.setText(_translate('PlotMlLearnCurve', 'Legend:'))
        self.cbblegend.addItems(['On', 'Off'])
        self.btnapply.setText(_translate('PlotMlLearnCurve', 'Apply'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApply)
        self.lineplottingconfig['Training accuracy'] = core_set.Visual['Line']
        if np.ndim(self.learnmat) >= 2:
            if np.shape(self.learnmat)[1] >= 5:
                self.ldtepochmin.setText(_translate('PlotMlLearnCurve', str(np.min(self.learnmat[:, 0]))))
                self.ldtepochmax.setText(_translate('PlotMlLearnCurve', str(np.max(self.learnmat[:, 0]))))
                self.ldtaccuracymin.setText(_translate('PlotMlLearnCurve', str(np.min(self.learnmat[:, 1:3]))))
                self.ldtaccuracymax.setText(_translate('PlotMlLearnCurve', str(np.max(self.learnmat[:, 1:3]))))
                self.ldtlossmin.setText(_translate('PlotMlLearnCurve', str(np.min(self.learnmat[:, 3:5]))))
                self.ldtlossmax.setText(_translate('PlotMlLearnCurve', str(np.max(self.learnmat[:, 3:5]))))

    def changeCbbProcessCurve(self):
        _curvelist = []
        if self.cbbprocess.currentIndex() == 0:
            _curvelist = [
             'Training']
        if self.cbbprocess.currentIndex() == 1:
            _curvelist = [
             'Validation']
        if self.cbbprocess.currentIndex() == 2:
            _curvelist = [
             'Training', 'Validation']
        if self.cbbcurve.currentIndex() == 0:
            _curvelist = [_curve + ' accuracy' for _curve in _curvelist]
        if self.cbbcurve.currentIndex() == 1:
            _curvelist = [_curve + ' loss' for _curve in _curvelist]
        if self.cbbcurve.currentIndex() == 2:
            _curvelist = [_curve + ' accuracy' for _curve in _curvelist] + [_curve + ' loss' for _curve in _curvelist]
        _config = {}
        for _curve in _curvelist:
            if _curve in self.lineplottingconfig.keys():
                _config[_curve] = self.lineplottingconfig[_curve]
            else:
                _config[_curve] = core_set.Visual['Line']

        self.lineplottingconfig = _config

    def clickBtnConfigLine(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configlineplotting()
        _gui.lineplottingconfig = self.lineplottingconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.lineplottingconfig = _gui.lineplottingconfig
        _config.show()

    def clickBtnApply(self):
        self.refreshMsgBox()
        if np.ndim(self.learnmat) < 2 or np.shape(self.learnmat)[1] < 5:
            vis_msg.print('ERROR in PlotMlLearnCurve: Wrong learning matrix', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Plot Learning Curve', 'Wrong learning matrix')
            return
        if self.cbbprocess.currentIndex() == 0:
            processtype = 1
        if self.cbbprocess.currentIndex() == 1:
            processtype = -1
        if self.cbbprocess.currentIndex() == 2:
            processtype = 0
        if self.cbbcurve.currentIndex() == 0:
            curvetype = 1
        if self.cbbcurve.currentIndex() == 1:
            curvetype = -1
        if self.cbbcurve.currentIndex() == 2:
            curvetype = 0
        epochmin = basic_data.str2float(self.ldtepochmin.text())
        epochmax = basic_data.str2float(self.ldtepochmax.text())
        if epochmin is False or epochmax is False:
            print('PlotMlLearnCurve: Non-float epoch range')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Plot Learning Curve', 'Non-float epoch range')
            return
        accuracymin = basic_data.str2float(self.ldtaccuracymin.text())
        accuracymax = basic_data.str2float(self.ldtaccuracymax.text())
        if curvetype >= 0 and not accuracymin is False:
            if accuracymax is False:
                print('PlotMlLearnCurve: Non-float accuracy range')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Plot Learning Curve', 'Non-float accuracy range')
                return
            lossmin = basic_data.str2float(self.ldtlossmin.text())
            lossmax = basic_data.str2float(self.ldtlossmax.text())
            if curvetype <= 0 and not lossmin is False:
                if lossmax is False:
                    print('PlotMlLearnCurve: Non-float loss range')
                    QtWidgets.QMessageBox.critical(self.msgbox, 'Plot Learning Curve', 'Non-float loss range')
                    return
            if self.cbblegend.currentIndex() == 0:
                legendon = True
            if self.cbblegend.currentIndex() == 1:
                legendon = False
        self.plotLearningCurve(processtype=processtype, curvetype=curvetype, epochlim=[
         epochmin, epochmax],
          accuracylim=[
         accuracymin, accuracymax],
          losslim=[
         lossmin, lossmax],
          fontstyle=(self.fontstyle),
          legendon=legendon)

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def plotLearningCurve(self, processtype=0, curvetype=0, epochlim=[
 0, 10], accuracylim=[
 0, 1.0], losslim=[
 0, 10], fontstyle=None, legendon=True):
        vis_font.updatePltFont(fontstyle)
        fig, ax1 = plt.subplots()
        fig.patch.set_facecolor('white')
        ax1.set_xlabel('Epochs')
        ax1.set_xlim([min(self.learnmat[:, 0]), max(self.learnmat[:, 0])])
        if curvetype >= 0:
            ax1.set_ylabel('Accuracy')
        else:
            ax1.set_ylabel('Loss')
        if curvetype == 0:
            ax2 = ax1.twinx()
            ax2.set_ylabel('Loss')
        if processtype >= 0:
            if curvetype >= 0:
                k_line, = ax1.plot((self.learnmat[:, 0]), (self.learnmat[:, 1]), color=(self.lineplottingconfig['Training accuracy']['Color'].lower()),
                  linewidth=(self.lineplottingconfig['Training accuracy']['Width']),
                  linestyle=(self.lineplottingconfig['Training accuracy']['Style'].lower()),
                  marker=(self.lineplottingconfig['Training accuracy']['MarkerStyle']),
                  markersize=(self.lineplottingconfig['Training accuracy']['MarkerSize']),
                  label='Training accuracy')
                ax1.set_xlim(epochlim)
                ax1.set_ylim(accuracylim)
            else:
                b_line, = ax1.plot((self.learnmat[:, 0]), (self.learnmat[:, 3]), color=(self.lineplottingconfig['Training loss']['Color'].lower()),
                  linewidth=(self.lineplottingconfig['Training loss']['Width']),
                  linestyle=(self.lineplottingconfig['Training loss']['Style'].lower()),
                  marker=(self.lineplottingconfig['Training loss']['MarkerStyle']),
                  markersize=(self.lineplottingconfig['Training loss']['MarkerSize']),
                  label='Training loss')
                ax1.set_xlim(epochlim)
                ax1.set_ylim(losslim)
            if curvetype == 0:
                b_line, = ax2.plot((self.learnmat[:, 0]), (self.learnmat[:, 3]), color=(self.lineplottingconfig['Training loss']['Color'].lower()),
                  linewidth=(self.lineplottingconfig['Training loss']['Width']),
                  linestyle=(self.lineplottingconfig['Training loss']['Style'].lower()),
                  marker=(self.lineplottingconfig['Training loss']['MarkerStyle']),
                  markersize=(self.lineplottingconfig['Training loss']['MarkerSize']),
                  label='Training loss')
                ax2.set_xlim(epochlim)
                ax2.set_ylim(losslim)
            if processtype <= 0:
                if curvetype >= 0:
                    r_line, = ax1.plot((self.learnmat[:, 0]), (self.learnmat[:, 2]), color=(self.lineplottingconfig['Validation accuracy']['Color'].lower()),
                      linewidth=(self.lineplottingconfig['Validation accuracy']['Width']),
                      linestyle=(self.lineplottingconfig['Validation accuracy']['Style'].lower()),
                      marker=(self.lineplottingconfig['Validation accuracy']['MarkerStyle']),
                      markersize=(self.lineplottingconfig['Validation accuracy']['MarkerSize']),
                      label='Validation accuracy')
                    ax1.set_xlim(epochlim)
                    ax1.set_ylim(accuracylim)
        else:
            g_line, = ax1.plot((self.learnmat[:, 0]), (self.learnmat[:, 4]), color=(self.lineplottingconfig['Validation loss']['Color'].lower()),
              linewidth=(self.lineplottingconfig['Validation loss']['Width']),
              linestyle=(self.lineplottingconfig['Validation loss']['Style'].lower()),
              marker=(self.lineplottingconfig['Validation loss']['MarkerStyle']),
              markersize=(self.lineplottingconfig['Validation loss']['MarkerSize']),
              label='Validation loss')
            ax1.set_xlim(epochlim)
            ax1.set_ylim(losslim)
        if curvetype == 0:
            g_line, = ax2.plot((self.learnmat[:, 0]), (self.learnmat[:, 4]), color=(self.lineplottingconfig['Validation loss']['Color'].lower()),
              linewidth=(self.lineplottingconfig['Validation loss']['Width']),
              linestyle=(self.lineplottingconfig['Validation loss']['Style'].lower()),
              marker=(self.lineplottingconfig['Validation loss']['MarkerStyle']),
              markersize=(self.lineplottingconfig['Validation loss']['MarkerSize']),
              label='Validation loss')
            ax2.set_xlim(epochlim)
            ax2.set_ylim(losslim)
        if legendon:
            if processtype == 0:
                if curvetype == 0:
                    plt.legend([k_line, r_line, b_line, g_line], [
                     'Training accuracy', 'Validation accuracy', 'Training loss', 'Validation loss'],
                      loc='center right')
                if curvetype > 0:
                    plt.legend([k_line, r_line], [
                     'Training accuracy', 'Validation accuracy'],
                      loc='center right')
                if curvetype < 0:
                    plt.legend([b_line, g_line], [
                     'Training loss', 'Validation loss'],
                      loc='center right')
        if legendon:
            if processtype > 0:
                if curvetype == 0:
                    plt.legend([k_line, b_line], ['Training accuracy', 'Training loss'])
                if curvetype > 0:
                    plt.legend([k_line], ['Training accuracy'])
                if curvetype < 0:
                    plt.legend([b_line], ['Training loss'])
        if legendon:
            if processtype < 0:
                if curvetype == 0:
                    plt.legend([r_line, g_line], ['Validation accuracy', 'Validation loss'])
                if curvetype > 0:
                    plt.legend([r_line], ['Validation accuracy'])
                if curvetype < 0:
                    plt.legend([g_line], ['Validation loss'])
        fig.canvas.set_window_title('ML Learning Curve')
        plt.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PlotMlLearnCurve = QtWidgets.QWidget()
    gui = plotmllearncurve()
    gui.setupGUI(PlotMlLearnCurve)
    PlotMlLearnCurve.show()
    sys.exit(app.exec_())