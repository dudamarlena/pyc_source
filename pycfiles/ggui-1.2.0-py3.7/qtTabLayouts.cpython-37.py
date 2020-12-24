# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ggui\qtTabLayouts.py
# Compiled at: 2019-12-22 01:36:00
# Size of source mod 2**32: 15999 bytes
"""
.. module:: qtTabLayouts
    :synopsis: Defines the gGui overview tab and associated tools
.. moduleauthor:: Duy Nguyen <dnguyen@nrao.edu>
"""
from configparser import ConfigParser
from PyQt5 import QtWidgets
from glue.app.qt.application import GlueApplication
import glue.core.session
from glue.config import qt_fixed_layout_tab, viewer_tool
from glue.viewers.common.qt.tool import Tool
from glue.viewers.matplotlib.qt.data_viewer import MatplotlibDataViewer
from glue.viewers.scatter.qt import ScatterViewer
from glue.viewers.image.qt import ImageViewer
from pkg_resources import resource_filename

class gGuiOverviewBaseViewer(MatplotlibDataViewer):
    __doc__ = 'Base class for gGui data viewers\n    Implements basic data import logic, band organizing, and UI methods\n    Adds FUV/NUV band support and associated band toggle tools\n    '
    tools = ['fuv_toggle', 'nuv_toggle']

    def __init__(self, glue_session, data):
        """Initializes base gGui data viewer

        :param session: Corresponding Glue parent's 'session' object that stores
        information about the current environment of glue. Needed for superclass constructor
        :param data: Band separated dict of data to load
        """
        super().__init__(glue_session)
        self.figure.canvas.mpl_connect('button_press_event', self.mousePressEvent)
        self.data_cache = {}
        for band, band_data in data.items():
            self.add_data(band_data)
            for index, layerData in enumerate([layers.layer for layers in self.state.layers]):
                if layerData == band_data:
                    self.data_cache[band] = {'data':band_data, 
                     'layer':self.state.layers[index]}
                    break

        if 'FUV' in self.data_cache:
            self.data_cache['FUV']['layer'].color = 'blue'
        if 'NUV' in self.data_cache:
            self.data_cache['NUV']['layer'].color = 'red'

    def toggle_band_visibility(self, band: str, value: str=None):
        """Toggles visibility of a dataset by band

        :param band: Band to toggle (i.e. 'NUV' or 'FUV')
        :param value: Optional parameter to explicitly set the band's visibility to a specific value.
            Absence will toggle the exising visibility
        """
        if self.data_cache.get(band).get('layer'):
            if not value:
                value = not self.data_cache[band]['layer'].visible
            self.data_cache[band]['layer'].visible = value

    def mousePressEvent(self, event):
        self._session.application._viewer_in_focus = self
        self._session.application._update_focus_decoration()
        self._session.application._update_plot_dashboard()


class ggui_lightcurve_viewer(gGuiOverviewBaseViewer, ScatterViewer):
    __doc__ = 'Data Viewer class that handles gPhoton lightcurve events'

    def __init__(self, session, lightcurve_data, x_att=None, y_att=None):
        """Initializes an instance of the gPhoton lightcurve viewer

        :param session: Corresponding Glue parent's 'session' object that stores
        information about the current environment of glue. Needed for superclass constructor
        :param lightcurve_data: Dict containing lightcurve data identified via respective frequency band
        :param x_att: Label of attribute to assign to the x-axis
        :param y_att: Label of attribute to assign to the y-axis
        """
        super().__init__(session, lightcurve_data)
        band_data = list(self.data_cache.values())[0]['data']
        try:
            if x_att:
                self.state.x_att = band_data.id[x_att]
        except KeyError as error:
            try:
                print('WARNING: gGui cannot assign lightcurve x axis: ' + str(error))
            finally:
                error = None
                del error

        try:
            if y_att:
                self.state.y_att = band_data.id[y_att]
        except KeyError as error:
            try:
                print('WARNING: gGui cannot assign lightcurve y axis: ' + str(error))
            finally:
                error = None
                del error

        for datalayer in self.data_cache.values():
            datalayer['layer'].linestyle = 'solid'
            datalayer['layer'].line_visible = True
            datalayer['layer'].yerr_att = datalayer['data'].id['flux_bgsub_err']
            datalayer['layer'].yerr_visible = True


class ggui_image_viewer(gGuiOverviewBaseViewer, ImageViewer):
    __doc__ = 'Data Viewer class that handles gPhoton FITS images'

    def __init__(self, session, image_data, x_att, y_att):
        super().__init__(session, image_data)


@viewer_tool
class FuvToggleTool(Tool):
    __doc__ = 'Glue data viewer tool that calls the FUV band visibility toggle method to corresponding ggui data viewer'
    icon = resource_filename('ggui.icons', 'FUV_transparent.png')
    tool_id = 'fuv_toggle'
    tool_tip = 'Toggle the FUV Dataset'

    def __init__(self, viewer):
        super().__init__(viewer)

    def activate(self):
        """Calls the ggui data viewer's data visibility toggle with the 'FUV' band"""
        self.viewer.toggle_band_visibility('FUV')


@viewer_tool
class NuvToggleTool(Tool):
    __doc__ = 'Glue data viewer tool that calls the NUV band visibility toggle method to corresponding ggui data viewer'
    icon = resource_filename('ggui.icons', 'NUV_transparent.png')
    tool_id = 'nuv_toggle'
    tool_tip = 'Toggle the NUV Dataset'

    def __init__(self, viewer):
        super().__init__(viewer)

    def activate(self):
        """Calls the ggui data viewer's data visibility toggle with the 'FUV' band"""
        self.viewer.toggle_band_visibility('NUV')


@qt_fixed_layout_tab
class ggui_overview_tab(QtWidgets.QMdiArea):
    __doc__ = 'Displays an overview of all gPhoton data products supplied to ggui'

    def __init__(self, session=None, target_name='Target', target_data=None):
        """Initializes the ggui overview tab with given data

        :param session: Corresponding Glue parent's 'session' object that stores 
        information about the current environment of glue
        :param target_name: The name of the target we are "overviewing"
        :param target_data: The gPhoton data (lighcurves, coadds, cubes) we are "overviewing"
        """
        super().__init__()
        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self._initialized_viewers = {}
        if target_data:
            self.load_data(session, target_name, target_data)

    def load_data(self, session: glue.core.session, target_name: str, target_data: dict):
        """Constructs the appropriate data viewer for any gPhoton data products provided

        :param session: Corresponding Glue parent's 'session' object that stores 
            information about the current environment of glue.
        :param target_name: The name of the target we are "overviewing"
        :param target_data: The gPhoton data (lighcurves, coadds, cubes) we are "overviewing"
        """
        config = ConfigParser()
        config.read(resource_filename('ggui', 'ggui.conf'))
        viewer_setters = {'lightcurve':self.loadLightcurve, 
         'coadd':self.loadCoadd, 
         'cube':self.loadCube}
        data_product_in_focus = None
        for data_product, viewer in self._initialized_viewers.items():
            if viewer is session.application._viewer_in_focus:
                data_product_in_focus = data_product
                continue

        self._initialized_viewers = {}
        for widgetIndex in reversed(range(0, self.layout.count())):
            self.layout.takeAt(widgetIndex).widget().deleteLater()

        for dataType, data in target_data.items():
            try:
                if data:
                    self._initialized_viewers[dataType] = viewer_setters[dataType](session, target_name, data, config.get('Mandatory Fields', (dataType + '_x'), fallback=None), config.get('Mandatory Fields', (dataType + '_y'), fallback=None))
            except ValueError as error:
                try:
                    print('WARNING: ' + str(error))
                    continue
                finally:
                    error = None
                    del error

        if data_product_in_focus in self._initialized_viewers:
            session.application._viewer_in_focus = self._initialized_viewers[data_product_in_focus]
        else:
            session.application._viewer_in_focus = None
        session.application._update_focus_decoration()
        session.application._update_plot_dashboard()

    def loadLightcurve(self, session: glue.core.session, target_name: str, lightcurve_data: dict, x_att: str, y_att: str):
        """Constructs a lightcurve viewer for gPhoton Lightcurve data

        :param session: Corresponding Glue parent's 'session' object that stores 
            information about the current environment of glue.
        :param target_name: The name of the target we are "overviewing"
        :param lightcurve_data: The gPhoton lightcurve to plot
        :param x_att: Label of attribute to assign to the x-axis
        :param y_att: Label of attribute to assign to the y-axis
        :returns: Initialized lightcurve viewer
        """
        for band, band_data in lightcurve_data.items():
            if isinstance(band_data, list):
                raise ValueError(str(target_name) + ' band ' + str(band) + ' has more than one (' + str(len(band_data)) + ') associated dataset. Cannot plot lightcurve data for this band due to ambiguity.')

        lightCurveViewer = ggui_lightcurve_viewer(session, lightcurve_data, x_att, y_att)
        lightCurveViewer.toolbar.actions['fuv_toggle'].setEnabled('FUV' in list(lightcurve_data.keys()))
        lightCurveViewer.toolbar.actions['nuv_toggle'].setEnabled('NUV' in list(lightcurve_data.keys()))
        lightCurveViewer.axes.set_title('Full Lightcurve of ' + target_name)
        lightCurveViewer.axes.set_autoscaley_on(True)
        self.layout.addWidget(lightCurveViewer, 0, 0, 1, 2)
        self.lightCurveViewer = lightCurveViewer
        lightCurveViewer.redraw()
        return lightCurveViewer

    def loadCoadd(self, session: glue.core.session, target_name: str, coadd_data: dict, x_att: str, y_att: str):
        """Constructs an image viewer for gPhoton Coadd FITS data

        :param session: Corresponding Glue parent's 'session' object that stores 
            information about the current environment of glue.
        :param target_name: The name of the target we are "overviewing"
        :param coadd_data: The gPhoton Coadd to plot
        :param x_att: Label of attribute to assign to the x-axis
        :param y_att: Label of attribute to assign to the y-axis
        :returns: Initialized coadd viewer
        """
        for band, band_data in coadd_data.items():
            if isinstance(band_data, list):
                raise ValueError(str(target_name) + ' band ' + str(band) + ' has more than one (' + str(len(band_data)) + ') associated dataset. Cannot plot coadd data for this band due to ambiguity.')

        coaddViewer = ggui_image_viewer(session, coadd_data, x_att, y_att)
        coaddViewer.toolbar.actions['fuv_toggle'].setEnabled('FUV' in list(coadd_data.keys()))
        coaddViewer.toolbar.actions['nuv_toggle'].setEnabled('NUV' in list(coadd_data.keys()))
        coaddViewer.axes.set_title('CoAdd of ' + target_name)
        self.layout.addWidget(coaddViewer, 1, 0)
        self.coaddViewer = coaddViewer
        return coaddViewer

    def loadCube(self, session: glue.core.session, target_name: str, cube_data: dict, x_att: str, y_att: str):
        """Constructs an image viewer for gPhoton Cube FITS data

        :param session: Corresponding Glue parent's 'session' object that stores 
            information about the current environment of glue.
        :param target_name: The name of the target we are "overviewing"
        :param cube_data: The gPhoton Cube to plot
        :param x_att: Label of attribute to assign to the x-axis
        :param y_att: Label of attribute to assign to the y-axis
        :returns: Initialized cube viewer
        """
        for band, band_data in cube_data.items():
            if isinstance(band_data, list):
                raise ValueError(str(target_name) + ' band ' + str(band) + ' has more than one (' + str(len(band_data)) + ') associated dataset. Cannot plot cube data for this band due to ambiguity.')

        cubeViewer = ggui_image_viewer(session, cube_data, x_att, y_att)
        cubeViewer.toolbar.actions['fuv_toggle'].setEnabled('FUV' in list(cube_data.keys()))
        cubeViewer.toolbar.actions['nuv_toggle'].setEnabled('NUV' in list(cube_data.keys()))
        cubeViewer.axes.set_title('Cube of ' + target_name)
        self.layout.addWidget(cubeViewer, 1, 1)
        self.cubeViewer = cubeViewer
        return cubeViewer