# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\plotml2dasfeconvmask.py
# Compiled at: 2019-12-16 00:14:22
# Size of source mod 2**32: 4667 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, numpy as np
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.vis.colormap import colormap as vis_cmap
from cognitivegeo.src.vis.image import image as vis_image
from cognitivegeo.src.gui.plotimagegallery import plotimagegallery as gui_core
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.cnnclassifier import cnnclassifier as ml_cnn
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class plotml2dasfeconvmask(gui_core):
    modelpath = ''
    modelname = ''
    maskstyle = core_set.Visual['Image']
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, PlotMl2DAsfeConvMask):
        gui_core.title = 'Plot 2D-ASFE Conv. Mask'
        gui_core.icon = 'mask.png'
        gui_core.imagestyle = self.maskstyle
        gui_core.imagelist = self.getConvMaskList()
        gui_core.setupGUI(self, PlotMl2DAsfeConvMask)

    def clickBtnApply(self):
        self.refreshMsgBox()
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in PlotMl2DAsfeConvMask: No ASFE network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Plot 2D-ASFE Conv. Mask', 'No ASFE network found')
            return
        _modelinfo = ml_tfm.getModelInfo(self.modelpath, self.modelname)
        _nblock = _modelinfo['number_conv_block']
        _nlayer = _modelinfo['number_conv_layer']
        _imageidx = self.cbbtype.currentIndex()
        _colormap = vis_cmap.ColorMapList[self.cbbcmap.currentIndex()]
        _flipped = self.cbxflip.isChecked()
        _interpolation = vis_image.InterpolationList[self.cbbinterp.currentIndex()].lower()
        _ncol = int(self.cbbncol.currentIndex()) + 1
        _blockidx = 0
        _layeridx = 0
        for i in range(_nblock):
            if sum(_nlayer[0:i + 1]) >= _imageidx + 1:
                _blockidx = i
                _layeridx = _imageidx - sum(_nlayer[0:i])
                break

        ml_cnn.plotCNNConvMask(cnnpath=(self.modelpath), cnnname=(self.modelname), blockidx=_blockidx,
          layeridx=_layeridx,
          ncol=_ncol,
          cmapname=_colormap,
          flipcmap=_flipped,
          interpolation=_interpolation,
          qicon=(QtGui.QIcon(os.path.join(self.iconpath, 'icons/logo.png'))))

    def getConvMaskList(self):
        _imagelist = []
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(self.modelpath, self.modelname)
            _nblock = _modelinfo['number_conv_block']
            _nlayer = _modelinfo['number_conv_layer']
            _nfeature = _modelinfo['number_conv_feature']
            _imagelist = []
            for i in range(_nblock):
                for j in range(_nlayer[i]):
                    _imagelist.append('Convolution block No. ' + str(i + 1) + ', layer No. ' + str(j + 1) + ' ----- ' + str(_nfeature[i]) + ' masks')

        return _imagelist


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PlotMl2DAsfeConvMask = QtWidgets.QWidget()
    gui = plotml2dasfeconvmask()
    gui.setupGUI(PlotMl2DAsfeConvMask)
    PlotMl2DAsfeConvMask.show()
    sys.exit(app.exec_())