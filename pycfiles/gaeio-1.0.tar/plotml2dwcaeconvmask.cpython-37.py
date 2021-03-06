# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\plotml2dwcaeconvmask.py
# Compiled at: 2019-12-16 00:14:22
# Size of source mod 2**32: 4688 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, numpy as np
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.vis.colormap as vis_cmap
import cognitivegeo.src.vis.image as vis_image
import cognitivegeo.src.gui.plotimagegallery as gui_core
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.wcaereconstructor as ml_wcae
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class plotml2dwcaeconvmask(gui_core):
    modelpath = ''
    modelname = ''
    maskstyle = core_set.Visual['Image']
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, PlotMl2DWcaeConvMask):
        gui_core.title = 'Plot 2D-WCAE Conv. Mask'
        gui_core.icon = 'mask.png'
        gui_core.imagestyle = self.maskstyle
        gui_core.imagelist = self.getConvMaskList()
        gui_core.setupGUI(self, PlotMl2DWcaeConvMask)

    def clickBtnApply(self):
        self.refreshMsgBox()
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in PlotMl2DWcaeConvMask: No WCAE network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Plot 2D-WCAE Conv. Mask', 'No CAE network found')
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

        ml_wcae.plotWCAEConvMask(wcaepath=(self.modelpath), wcaename=(self.modelname), blockidx=_blockidx,
          layeridx=_layeridx,
          ncol=_ncol,
          cmapname=_colormap,
          flipcmap=_flipped,
          interpolation=_interpolation,
          qicon=(QtGui.QIcon(os.path.join(self.iconpath, 'icons/logo.png'))))

    def getConvMaskList(self):
        _imagelist = []
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is True:
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
    PlotMl2DWcaeConvMask = QtWidgets.QWidget()
    gui = plotml2dwcaeconvmask()
    gui.setupGUI(PlotMl2DWcaeConvMask)
    PlotMl2DWcaeConvMask.show()
    sys.exit(app.exec_())