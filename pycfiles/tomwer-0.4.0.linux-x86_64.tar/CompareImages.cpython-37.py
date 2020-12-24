# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/axis/CompareImages.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 24168 bytes
__authors__ = [
 'v. Valls', 'H. Payno']
__license__ = 'MIT'
__date__ = '26/02/2019'
from silx.gui import qt
import silx.gui.plot as _CompareImages
import silx.gui as silx_icons
import tomwer.gui as tomwer_icons
from silx.gui.plot import tools
import numpy
from silx.gui.colors import Colormap
import weakref, logging
_logger = logging.getLogger(__name__)
MODE_RAW_COMPARISON = 'Subtract in B&W mode'

class CompareImagesToolBar(qt.QToolBar):
    __doc__ = 'ToolBar containing specific tools to custom the configuration of a\n    :class:`CompareImages` widget\n\n    Use :meth:`setCompareWidget` to connect this toolbar to a specific\n    :class:`CompareImages` widget.\n\n    :param Union[qt.QWidget,None] parent: Parent of this widget.\n    '

    def __init__(self, parent=None):
        qt.QToolBar.__init__(self, parent)
        self._CompareImagesToolBar__compareWidget = None
        menu = qt.QMenu(self)
        self._CompareImagesToolBar__visualizationAction = qt.QAction(self)
        self._CompareImagesToolBar__visualizationAction.setMenu(menu)
        self._CompareImagesToolBar__visualizationAction.setCheckable(False)
        self.addAction(self._CompareImagesToolBar__visualizationAction)
        self._CompareImagesToolBar__visualizationGroup = qt.QActionGroup(self)
        self._CompareImagesToolBar__visualizationGroup.setExclusive(True)
        self._CompareImagesToolBar__visualizationGroup.triggered.connect(self._CompareImagesToolBar__visualizationModeChanged)
        icon = silx_icons.getQIcon('compare-mode-a')
        action = qt.QAction(icon, 'Display radio 1', self)
        action.setIconVisibleInMenu(True)
        action.setCheckable(True)
        action.setShortcut(qt.QKeySequence(qt.Qt.Key_A))
        action.setProperty('mode', CompareImages.VisualizationMode.ONLY_A)
        menu.addAction(action)
        self._CompareImagesToolBar__aModeAction = action
        self._CompareImagesToolBar__visualizationGroup.addAction(action)
        icon = silx_icons.getQIcon('compare-mode-b')
        action = qt.QAction(icon, 'Display radio 2', self)
        action.setIconVisibleInMenu(True)
        action.setCheckable(True)
        action.setShortcut(qt.QKeySequence(qt.Qt.Key_B))
        action.setProperty('mode', CompareImages.VisualizationMode.ONLY_B)
        menu.addAction(action)
        self._CompareImagesToolBar__bModeAction = action
        self._CompareImagesToolBar__visualizationGroup.addAction(action)
        icon = silx_icons.getQIcon('compare-mode-rbneg-channel')
        action = qt.QAction(icon, 'Subtract in color mode', self)
        action.setIconVisibleInMenu(True)
        action.setCheckable(True)
        action.setShortcut(qt.QKeySequence(qt.Qt.Key_C))
        action.setProperty('mode', _CompareImages.VisualizationMode.COMPOSITE_RED_BLUE_GRAY_NEG)
        menu.addAction(action)
        self._CompareImagesToolBar__ycChannelModeAction = action
        self._CompareImagesToolBar__visualizationGroup.addAction(action)
        icon = tomwer_icons.getQIcon('compare_mode_a_minus_b')
        action = qt.QAction(icon, 'Subtract in BW mode', self)
        action.setIconVisibleInMenu(True)
        action.setCheckable(True)
        action.setShortcut(qt.QKeySequence(qt.Qt.Key_S))
        action.setProperty('mode', MODE_RAW_COMPARISON)
        menu.addAction(action)
        self._CompareImagesToolBar__ycChannelModeAction = action
        self._CompareImagesToolBar__visualizationGroup.addAction(action)
        icon = tomwer_icons.getQIcon('switch')
        self._flip_action = qt.QAction(icon, 'flip radio 2', self)
        self._flip_action.setCheckable(True)
        self._flip_action.setChecked(True)
        self.addAction(self._flip_action)
        self.flipToggled = self._flip_action.toggled

    def setRadio2FlipVisible(self, visible):
        self._flip_action.setVisible(visible)

    def setRadio2Flip(self, checked):
        old = self.blockSignals(True)
        self._flip_action.setChecked(checked)
        self.blockSignals(old)

    def isRadio2Flip(self):
        """

        :return: return True if the user requires the image B to be flip or not
        :rtype: bool
        """
        return self._flip_action.isChecked()

    def setCompareWidget(self, widget):
        """
        Connect this tool bar to a specific :class:`CompareImages` widget.

        :param Union[None,CompareImages] widget: The widget to connect with.
        """
        compareWidget = self.getCompareWidget()
        if compareWidget is not None:
            compareWidget.sigConfigurationChanged.disconnect(self._CompareImagesToolBar__updateSelectedActions)
        else:
            compareWidget = widget
            if compareWidget is None:
                self._CompareImagesToolBar__compareWidget = None
            else:
                self._CompareImagesToolBar__compareWidget = weakref.ref(compareWidget)
        if compareWidget is not None:
            widget.sigConfigurationChanged.connect(self._CompareImagesToolBar__updateSelectedActions)
        self._CompareImagesToolBar__updateSelectedActions()

    def getCompareWidget(self):
        """Returns the connected widget.

        :rtype: CompareImages
        """
        if self._CompareImagesToolBar__compareWidget is None:
            return
        return self._CompareImagesToolBar__compareWidget()

    def __updateSelectedActions(self):
        """
        Update the state of this tool bar according to the state of the
        connected :class:`CompareImages` widget.
        """
        widget = self.getCompareWidget()
        if widget is None:
            return
        mode = widget.getVisualizationMode()
        action = None
        for a in self._CompareImagesToolBar__visualizationGroup.actions():
            actionMode = a.property('mode')
            if mode == actionMode:
                action = a
                break

        old = self._CompareImagesToolBar__visualizationGroup.blockSignals(True)
        if action is not None:
            action.setChecked(True)
        else:
            action = self._CompareImagesToolBar__visualizationGroup.checkedAction()
            if action is not None:
                action.setChecked(False)
        self._CompareImagesToolBar__updateVisualizationMenu()
        self._CompareImagesToolBar__visualizationGroup.blockSignals(old)

    def __visualizationModeChanged(self, selectedAction):
        """Called when user requesting changes of the visualization mode.
        """
        self._CompareImagesToolBar__updateVisualizationMenu()
        widget = self.getCompareWidget()
        if widget is not None:
            mode = selectedAction.property('mode')
            widget.setVisualizationMode(mode)

    def __updateVisualizationMenu(self):
        """Update the state of the action containing visualization menu.
        """
        selectedAction = self._CompareImagesToolBar__visualizationGroup.checkedAction()
        if selectedAction is not None:
            self._CompareImagesToolBar__visualizationAction.setText(selectedAction.text())
            self._CompareImagesToolBar__visualizationAction.setIcon(selectedAction.icon())
            self._CompareImagesToolBar__visualizationAction.setToolTip(selectedAction.toolTip())
        else:
            self._CompareImagesToolBar__visualizationAction.setText('')
            self._CompareImagesToolBar__visualizationAction.setIcon(qt.QIcon())
            self._CompareImagesToolBar__visualizationAction.setToolTip('')

    def __alignmentModeChanged(self, selectedAction):
        """Called when user requesting changes of the alignment mode.
        """
        self._CompareImagesToolBar__updateAlignmentMenu()
        widget = self.getCompareWidget()
        if widget is not None:
            mode = selectedAction.property('mode')
            widget.setAlignmentMode(mode)

    def __updateAlignmentMenu(self):
        """Update the state of the action containing alignment menu.
        """
        selectedAction = self._CompareImagesToolBar__alignmentGroup.checkedAction()
        if selectedAction is not None:
            self._CompareImagesToolBar__alignmentAction.setText(selectedAction.text())
            self._CompareImagesToolBar__alignmentAction.setIcon(selectedAction.icon())
            self._CompareImagesToolBar__alignmentAction.setToolTip(selectedAction.toolTip())
        else:
            self._CompareImagesToolBar__alignmentAction.setText('')
            self._CompareImagesToolBar__alignmentAction.setIcon(qt.QIcon())
            self._CompareImagesToolBar__alignmentAction.setToolTip('')

    def __keypointVisibilityChanged(self):
        """Called when action managing keypoints visibility changes"""
        widget = self.getCompareWidget()
        if widget is not None:
            keypointsVisible = self._CompareImagesToolBar__displayKeypoints.isChecked()
            widget.setKeypointsVisible(keypointsVisible)


import silx
if silx._version.MINOR > 10 and silx._version.MAJOR == 0:

    class CompareImages(_CompareImages.CompareImages):

        def _createToolBars(self, plot):
            """Create tool bars displayed by the widget"""
            self._interactiveModeToolBar = tools.InteractiveModeToolBar(parent=self, plot=plot)
            self._imageToolBar = tools.ImageToolBar(parent=self, plot=plot)
            toolBar = CompareImagesToolBar(self)
            toolBar.setCompareWidget(self)
            self._compareToolBar = toolBar
            self.flipToggled = self._compareToolBar.flipToggled
            self.setRadio2FlipVisible = self._compareToolBar.setRadio2FlipVisible
            self.setRadio2Flip = self._compareToolBar.setRadio2Flip
            self.isRadio2Flip = self._compareToolBar.isRadio2Flip

        def _createStatusBar(self, plot):
            self._statusBar = CompareImagesStatusBar(self)
            self._statusBar.setCompareWidget(self)

        def getCompareToolBar(self):
            return self._compareToolBar


else:

    class CompareImages(_CompareImages.CompareImages):

        def _createToolBars(self, plot):
            """Create tool bars displayed by the widget"""
            toolBar = tools.InteractiveModeToolBar(parent=self, plot=plot)
            self._interactiveModeToolBar = toolBar
            toolBar = tools.ImageToolBar(parent=self, plot=plot)
            self._imageToolBar = toolBar
            toolBar = CompareImagesToolBar(self)
            toolBar.setCompareWidget(self)
            self._compareToolBar = toolBar
            self.flipToggled = self._compareToolBar.flipToggled
            self.setRadio2FlipVisible = self._compareToolBar.setRadio2FlipVisible
            self.setRadio2Flip = self._compareToolBar.setRadio2Flip
            self.isRadio2Flip = self._compareToolBar.isRadio2Flip

        def getCompareToolBar(self):
            return self._compareToolBar

        def __updateData(self):
            """Compute aligned image when the alignement mode changes.

            This function cache input images which are used when
            vertical/horizontal separators moves.
            """
            raw1, raw2 = self._CompareImages__raw1, self._CompareImages__raw2
            if raw1 is None or raw2 is None:
                return
            alignmentMode = self.getAlignmentMode()
            self._CompareImages__transformation = None
            if alignmentMode == _CompareImages.AlignmentMode.ORIGIN:
                yy = max(raw1.shape[0], raw2.shape[0])
                xx = max(raw1.shape[1], raw2.shape[1])
                size = (yy, xx)
                data1 = self._CompareImages__createMarginImage(raw1, size, transparent=True)
                data2 = self._CompareImages__createMarginImage(raw2, size, transparent=True)
                self._CompareImages__matching_keypoints = ([0.0], [0.0], [1.0])
            else:
                if alignmentMode == _CompareImages.AlignmentMode.CENTER:
                    yy = max(raw1.shape[0], raw2.shape[0])
                    xx = max(raw1.shape[1], raw2.shape[1])
                    size = (yy, xx)
                    data1 = self._CompareImages__createMarginImage(raw1, size, transparent=True, center=True)
                    data2 = self._CompareImages__createMarginImage(raw2, size, transparent=True, center=True)
                    self._CompareImages__matching_keypoints = ([data1.shape[1] // 2],
                     [
                      data1.shape[0] // 2],
                     [
                      1.0])
                else:
                    if alignmentMode == _CompareImages.AlignmentMode.STRETCH:
                        data1 = raw1
                        data2 = self._CompareImages__rescaleImage(raw2, data1.shape)
                        self._CompareImages__matching_keypoints = ([0, data1.shape[1], data1.shape[1], 0],
                         [
                          0, 0, data1.shape[0], data1.shape[0]],
                         [
                          1.0, 1.0, 1.0, 1.0])
                    else:
                        if alignmentMode == _CompareImages.AlignmentMode.AUTO:
                            yy = max(raw1.shape[0], raw2.shape[0])
                            xx = max(raw1.shape[1], raw2.shape[1])
                            size = (yy, xx)
                            data1 = self._CompareImages__createMarginImage(raw1, size)
                            data2 = self._CompareImages__createMarginImage(raw2, size)
                            self._CompareImages__matching_keypoints = ([0.0], [0.0], [1.0])
                            try:
                                data1, data2 = self._CompareImages__createSiftData(data1, data2)
                                if data2 is None:
                                    raise ValueError('Unexpected None value')
                            except Exception as e:
                                try:
                                    _logger.error(e)
                                    self._CompareImages__setDefaultAlignmentMode()
                                    return
                                finally:
                                    e = None
                                    del e

                        else:
                            assert False
                            mode = self.getVisualizationMode()
            if mode in _CompareImages.VisualizationMode.COMPOSITE_RED_BLUE_GRAY_NEG:
                data1 = self._CompareImages__composeImage(data1, data2, mode)
                data2 = numpy.empty((0, 0))
            else:
                if mode == _CompareImages.VisualizationMode.COMPOSITE_RED_BLUE_GRAY:
                    data1 = self._CompareImages__composeImage(data1, data2, mode)
                    data2 = numpy.empty((0, 0))
                else:
                    if mode == _CompareImages.VisualizationMode.ONLY_A:
                        data2 = numpy.empty((0, 0))
                    else:
                        if mode == _CompareImages.VisualizationMode.ONLY_B:
                            data1 = numpy.empty((0, 0))
                        else:
                            if mode == MODE_RAW_COMPARISON:
                                data1 = data1.astype(numpy.float64) - data2.astype(numpy.float64)
                                data1 = data1.astype(data1.dtype)
                                data2 = numpy.empty((0, 0))
                            else:
                                self._CompareImages__data1, self._CompareImages__data2 = data1, data2
                                self._CompareImages__plot.addImage(data1, z=0, legend='image1', resetzoom=False)
                                self._CompareImages__plot.addImage(data2, z=0, legend='image2', resetzoom=False)
                                self._CompareImages__image1 = self._CompareImages__plot.getImage('image1')
                                self._CompareImages__image2 = self._CompareImages__plot.getImage('image2')
                                self._CompareImages__updateKeyPoints()
                                if self._CompareImages__previousSeparatorPosition is None:
                                    value = self._CompareImages__data1.shape[1] // 2
                                    self._CompareImages__vline.setPosition(value, 0)
                                    value = self._CompareImages__data1.shape[0] // 2
                                    self._CompareImages__hline.setPosition(0, value)
                                self._CompareImages__updateSeparators()
                                mode1 = self._CompareImages__getImageMode(data1)
                                mode2 = self._CompareImages__getImageMode(data2)
                                if mode1 == 'intensity' and mode1 == mode2:
                                    if self._CompareImages__data1.size == 0:
                                        vmin = self._CompareImages__data2.min()
                                        vmax = self._CompareImages__data2.max()
                                    else:
                                        if self._CompareImages__data2.size == 0:
                                            vmin = self._CompareImages__data1.min()
                                            vmax = self._CompareImages__data1.max()
                                        else:
                                            vmin = min(self._CompareImages__data1.min(), self._CompareImages__data2.min())
                                            vmax = max(self._CompareImages__data1.max(), self._CompareImages__data2.max())
                                    colormap = Colormap(vmin=vmin, vmax=vmax)
                                    self._CompareImages__image1.setColormap(colormap)
                                    self._CompareImages__image2.setColormap(colormap)

        def _createStatusBar(self, plot):
            self._statusBar = CompareImagesStatusBar(self)
            self._statusBar.setCompareWidget(self)


class CompareImagesStatusBar(qt.QStatusBar):
    __doc__ = 'StatusBar containing specific information contained in a\n    :class:`CompareImages` widget\n\n    Use :meth:`setCompareWidget` to connect this toolbar to a specific\n    :class:`CompareImages` widget.\n\n    :param Union[qt.QWidget,None] parent: Parent of this widget.\n    '

    def __init__(self, parent=None):
        qt.QStatusBar.__init__(self, parent)
        self.setSizeGripEnabled(False)
        self.layout().setSpacing(0)
        self._CompareImagesStatusBar__compareWidget = None
        self._label1 = qt.QLabel(self)
        self._label1.setFrameShape(qt.QFrame.WinPanel)
        self._label1.setFrameShadow(qt.QFrame.Sunken)
        self._label2 = qt.QLabel(self)
        self._label2.setFrameShape(qt.QFrame.WinPanel)
        self._label2.setFrameShadow(qt.QFrame.Sunken)
        self._transform = qt.QLabel(self)
        self._transform.setFrameShape(qt.QFrame.WinPanel)
        self._transform.setFrameShadow(qt.QFrame.Sunken)
        self.addWidget(self._label1)
        self.addWidget(self._label2)
        self.addWidget(self._transform)
        self._pos = None
        self._updateStatusBar()

    def setCompareWidget(self, widget):
        """
        Connect this tool bar to a specific :class:`CompareImages` widget.

        :param Union[None,CompareImages] widget: The widget to connect with.
        """
        compareWidget = self.getCompareWidget()
        if compareWidget is not None:
            compareWidget.getPlot().sigPlotSignal.disconnect(self._CompareImagesStatusBar__plotSignalReceived)
            compareWidget.sigConfigurationChanged.disconnect(self._CompareImagesStatusBar__dataChanged)
        else:
            compareWidget = widget
            if compareWidget is None:
                self._CompareImagesStatusBar__compareWidget = None
            else:
                self._CompareImagesStatusBar__compareWidget = weakref.ref(compareWidget)
        if compareWidget is not None:
            compareWidget.getPlot().sigPlotSignal.connect(self._CompareImagesStatusBar__plotSignalReceived)
            compareWidget.sigConfigurationChanged.connect(self._CompareImagesStatusBar__dataChanged)

    def getCompareWidget(self):
        """Returns the connected widget.

        :rtype: CompareImages
        """
        if self._CompareImagesStatusBar__compareWidget is None:
            return
        return self._CompareImagesStatusBar__compareWidget()

    def __plotSignalReceived(self, event):
        """Called when old style signals at emmited from the plot."""
        if event['event'] == 'mouseMoved':
            x, y = event['x'], event['y']
            self._CompareImagesStatusBar__mouseMoved(x, y)

    def __mouseMoved(self, x, y):
        """Called when mouse move over the plot."""
        self._pos = (
         x, y)
        self._updateStatusBar()

    def __dataChanged(self):
        """Called when internal data from the connected widget changes."""
        self._updateStatusBar()

    def _formatData(self, data):
        """Format pixel of an image.

        It supports intensity, RGB, and RGBA.

        :param Union[int,float,numpy.ndarray,str]: Value of a pixel
        :rtype: str
        """
        if data is None:
            return '-'
        else:
            if isinstance(data, (int, numpy.integer)):
                return '%d' % data
            if isinstance(data, (float, numpy.floating)):
                return '%f' % data
            if isinstance(data, numpy.ndarray):
                if data.shape == (3, ):
                    return 'R:%d G:%d B:%d' % (data[0], data[1], data[2])
                if data.shape == (4, ):
                    return 'R:%d G:%d B:%d A:%d' % (data[0], data[1], data[2], data[3])
        _logger.debug('Unsupported data format %s. Cast it to string.', type(data))
        return str(data)

    def _updateStatusBar(self):
        """Update the content of the status bar"""
        widget = self.getCompareWidget()
        if widget is None:
            self._label1.setText('Radio1: -')
            self._label2.setText('Radio2: -')
            self._transform.setVisible(False)
        else:
            transform = widget.getTransformation()
            self._transform.setVisible(transform is not None)
            if transform is not None:
                has_notable_translation = not numpy.isclose((transform.tx), 0.0, atol=0.01) or not numpy.isclose((transform.ty), 0.0, atol=0.01)
                has_notable_scale = not numpy.isclose((transform.sx), 1.0, atol=0.01) or not numpy.isclose((transform.sy), 1.0, atol=0.01)
                has_notable_rotation = not numpy.isclose((transform.rot), 0.0, atol=0.01)
                strings = []
                if has_notable_translation:
                    strings.append('Translation')
                else:
                    if has_notable_scale:
                        strings.append('Scale')
                    if has_notable_rotation:
                        strings.append('Rotation')
                    if strings == []:
                        has_translation = not numpy.isclose(transform.tx, 0.0) or not numpy.isclose(transform.ty, 0.0)
                        has_scale = not numpy.isclose(transform.sx, 1.0) or not numpy.isclose(transform.sy, 1.0)
                        has_rotation = not numpy.isclose(transform.rot, 0.0)
                        if not has_translation:
                            if has_scale or has_rotation:
                                text = 'No big changes'
                        else:
                            text = 'No changes'
                    else:
                        text = '+'.join(strings)
                self._transform.setText('Align: ' + text)
                strings = []
                if not numpy.isclose(transform.ty, 0.0):
                    strings.append('Translation x: %0.3fpx' % transform.tx)
                if not numpy.isclose(transform.ty, 0.0):
                    strings.append('Translation y: %0.3fpx' % transform.ty)
                if not numpy.isclose(transform.sx, 1.0):
                    strings.append('Scale x: %0.3f' % transform.sx)
                if not numpy.isclose(transform.sy, 1.0):
                    strings.append('Scale y: %0.3f' % transform.sy)
                else:
                    if not numpy.isclose(transform.rot, 0.0):
                        strings.append('Rotation: %0.3fdeg' % (transform.rot * 180 / numpy.pi))
                    if strings == []:
                        text = 'No transformation'
                    else:
                        text = '\n'.join(strings)
                self._transform.setToolTip(text)
            elif self._pos is None:
                self._label1.setText('Radio1: -')
                self._label2.setText('Radio2: -')
            else:
                data1, data2 = widget.getRawPixelData(self._pos[0], self._pos[1])
                if isinstance(data1, str):
                    self._label1.setToolTip(data1)
                    text1 = '-'
                else:
                    self._label1.setToolTip('')
                    text1 = self._formatData(data1)
                if isinstance(data2, str):
                    self._label2.setToolTip(data2)
                    text2 = '-'
                else:
                    self._label2.setToolTip('')
                    text2 = self._formatData(data2)
                self._label1.setText('Radio1: %s' % text1)
                self._label2.setText('Radio2: %s' % text2)