# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/visual/canvas.py
# Compiled at: 2018-10-01 15:21:18
# Size of source mod 2**32: 28003 bytes
import numpy as np
from .render_volume import RenderVolume
from vispy import app, scene
from vispy.gloo import gl

class Canvas3D(scene.SceneCanvas):
    __doc__ = 'Class describing the 3D canvas where the visualisation is plotted'

    def __init__(self, resolution):
        """Initialise the vispy canvas3D

        Parameters
        ----------
        resolution : appQt.desktop().screenGeometry()
            Width and height of the canvas.
        """
        self._configured = False
        self._fg = (0.5, 0.5, 0.5, 1)
        scene.SceneCanvas.__init__(self, keys='interactive',
          size=(
         resolution.width(), resolution.height()),
          show=True)
        self.unfreeze()
        self.window_resolution = resolution
        self._configure_canvas()
        self._configure_3d()
        self.freeze()

    def _configure_canvas(self):
        """Configure the vispy canvas

        Sets the background color, add and configure the grid to define where the colorbar and
        the main visualisation will be.
        """
        self.central_widget.bgcolor = '#404040'
        self.grid = self.central_widget.add_grid(spacing=0, margin=0)

    def _configure_3d(self):
        """Configure the vispy canvas grid.
        """
        if self._configured:
            return
        self.cbar_left = self.grid.add_widget(None, row=0, col=0, border_color='#404040', bgcolor='#404040')
        self.cbar_left.width_max = 0
        self.view = self.grid.add_view(row=0, col=1, border_color='#404040',
          bgcolor='#404040')
        self.view.camera = 'turntable'
        self.camera = self.view.camera
        self._configured = True

    def colorbar(self, cmap, position='left', label='', clim=('', ''), border_width=0.0, border_color='#404040', **kwargs):
        """Show a ColorBar

        Parameters
        ----------
        cmap : str | vispy.color.ColorMap
            Either the name of the ColorMap to be used from the standard
            set of names (refer to `vispy.color.get_colormap`),
            or a custom ColorMap object.
            The ColorMap is used to apply a gradient on the colorbar.
        position : {'left', 'right', 'top', 'bottom'}
            The position of the colorbar with respect to the plot.
            'top' and 'bottom' are placed horizontally, while
            'left' and 'right' are placed vertically
        label : str
            The label that is to be drawn with the colorbar
            that provides information about the colorbar.
        clim : tuple (min, max)
            the minimum and maximum values of the data that
            is given to the colorbar. This is used to draw the scale
            on the side of the colorbar.
        border_width : float (in px)
            The width of the border the colormap should have. This measurement
            is given in pixels
        border_color : str | vispy.color.Color
            The color of the border of the colormap. This can either be a
            str as the color's name or an actual instace of a vipy.color.Color

        Returns
        -------
        colorbar : instance of ColorBarWidget

        See also
        --------
        ColorBarWidget
        """
        self.cbar = (scene.ColorBarWidget)(orientation=position, label=label, 
         cmap=cmap, 
         clim=clim, 
         border_width=border_width, 
         border_color=border_color, **kwargs)
        if self.window_resolution.width() <= 3000:
            CBAR_LONG_DIM = 150
            self.cbar.label.font_size = 15
            self.cbar.label.color = 'white'
            self.cbar.ticks[0].font_size = 12
            self.cbar.ticks[1].font_size = 12
            self.cbar.ticks[0].color = 'white'
            self.cbar.ticks[1].color = 'white'
        else:
            CBAR_LONG_DIM = 300
            self.cbar.label.font_size = 60
            self.cbar.label.color = 'white'
            self.cbar.ticks[0].font_size = 45
            self.cbar.ticks[1].font_size = 45
            self.cbar.ticks[0].color = 'white'
            self.cbar.ticks[1].color = 'white'
        if self.cbar.orientation == 'bottom':
            self.grid.remove_widget(self.cbar_bottom)
            self.cbar_bottom = self.grid.add_widget((self.cbar), row=2, col=1)
            self.cbar_bottom.height_max = self.cbar_bottom.height_max = CBAR_LONG_DIM
        else:
            if self.cbar.orientation == 'top':
                self.grid.remove_widget(self.cbar_top)
                self.cbar_top = self.grid.add_widget((self.cbar), row=0, col=1)
                self.cbar_top.height_max = self.cbar_top.height_max = CBAR_LONG_DIM
            else:
                if self.cbar.orientation == 'left':
                    self.grid.remove_widget(self.cbar)
                    self.cbar_left = self.grid.add_widget((self.cbar), row=0, col=0)
                    self.cbar_left.width_max = self.cbar_left.width_min = CBAR_LONG_DIM
                else:
                    self.grid.remove_widget(self.cbar_right)
                    self.cbar_right = self.grid.add_widget((self.cbar), row=2, col=2)
                    self.cbar_right.width_max = self.cbar_right.width_min = CBAR_LONG_DIM

    def histogram(self, data, bins=100, color='w', orientation='h'):
        """Calculate and show a histogram of data

        Parameters
        ----------
        data : array-like
            Data to histogram. Currently only 1D data is supported.
        bins : int | array-like
            Number of bins, or bin edges.
        color : instance of Color
            Color of the histogram.
        orientation : {'h', 'v'}
            Orientation of the histogram.
        """
        self.view_histogram = self.grid.add_view(row=1, col=0, border_color='#404040', bgcolor='#404040')
        self.view_histogram.camera = 'panzoom'
        self.hist = scene.Histogram(data, bins, color, orientation)
        self.view_histogram.add(self.hist)
        self.view_histogram.camera.set_range()

    def set_volume_scene(self, cube):
        """Set volume scene

        Configures the vispy canvas to display the 3D visualisation.

        Parameters
        ----------
        cube : astropy.io.fits
            FITS file opened with astropy.io.fits containing the volumetric data (e.g. spectral cube).

        TO DO
        -----
        Move some of the code from this function to atomic functions (e.g. header information for cmap).

        """
        if self.view:
            canvas = self.central_widget.remove_widget(self.grid)
            self._configure_canvas()
        self.unfreeze()
        self.view = self.grid.add_view(row=0, col=1, border_color='#404040',
          bgcolor='#404040')
        try:
            if len(cube[0].data.shape) == 4:
                data = cube[0].data[0][:2048, :2048, :2048]
                self.vel_axis = cube[0].data[0].shape[0]
            else:
                data = cube[0].data[:2048, :2048, :2048]
                self.vel_axis = cube[0].data.shape[0]
            try:
                self.bunit = cube[0].header['BUNIT']
            except:
                self.bunit = 'unknown'

            try:
                self.vel_type = cube[0].header['CTYPE3']
            except:
                self.vel_type = 'Epoch'

            try:
                self.vel_val = cube[0].header['CRVAL3']
                lim_is_set = False
                try:
                    self.vel_delt = cube[0].header['CDELT3']
                    set_lim = True
                except:
                    set_lim = False

                if self.vel_type == 'VELO-HEL' or self.vel_type == 'FELO-HEL':
                    self.vel_type += ' (km/s)'
                    if set_lim:
                        self.clim_vel = (
                         np.int(np.round(float(self.vel_val) / 1000)),
                         np.int(np.round((float(self.vel_val) + float(self.vel_delt) * self.vel_axis) / 1000)))
                        lim_is_set = True
                    else:
                        if self.vel_type == 'FREQ':
                            if cube[0].header['CUNIT3'] == 'Hz':
                                self.vel_type += ' (T' + cube[0].header['CUNIT3'] + ')'
                                self.clim_vel = (float(self.vel_val) / 1000000000,
                                 (float(self.vel_val) + float(self.vel_delt) * self.vel_axis) / 1000000000)
                                lim_is_set = True
                        else:
                            self.vel_type += ' (' + cube[0].header['CUNIT3'] + ')'
                            self.clim_vel = (np.int(np.round(float(self.vel_val))),
                             np.int(np.round(float(self.vel_val) + float(self.vel_delt) * self.vel_axis)))
                            lim_is_set = True
                else:
                    pass
                if self.vel_type == 'WAVE':
                    self.vel_type += ' (' + cube[0].header['CUNIT3'] + ')'
                if set_lim == True:
                    if lim_is_set == False:
                        self.clim_vel = (
                         np.int(np.round(float(self.vel_val))),
                         np.int(np.round(float(self.vel_val) + float(self.vel_delt) * self.vel_axis)))
                        lim_is_set = True
                if set_lim == False:
                    try:
                        self.vel_delt = cube[0].header['STEP']
                        self.clim_vel = (np.int(np.round(float(self.vel_val))),
                         np.int(np.round(float(self.vel_val) + float(self.vel_delt) * self.vel_axis)))
                    except:
                        self.clim_vel = (
                         0, self.vel_axis)

            except:
                self.vel_val = 'Undefined'

            data = np.flipud(np.rollaxis(data, 1))
            self.volume = RenderVolume(data, parent=(self.view.scene),
              threshold=0.225,
              emulate_texture=False)
            vertices, filled_indices, outline_indices = self.create_cube(data.shape)
            self.axis = scene.visuals.Mesh((vertices['position']), outline_indices,
              color='white',
              parent=(self.view.scene),
              mode='lines')
            gl.glLineWidth(1.5)
            self.view.add(self.axis)
            self.colorbar(label=(str(self.vel_type)), clim=(self.volume.clim),
              cmap='hsl',
              border_width=0,
              border_color='#404040')
            self.rotation = scene.MatrixTransform()
            self.timer = app.Timer(connect=(self.rotate))
            self.angle = 0.0
            self.freeze()
        except ValueError as e:
            try:
                t = e
                print(t)
            finally:
                e = None
                del e

    def create_cube(self, shape):
        """ Generate vertices & indices for a filled and outlined cube

        Parameters
        ----------
        shape : list
            List representing the shape of the numpy array.

        Returns
        -------
        vertices : array
            Array of vertices suitable for use as a VertexBuffer.
        filled : array
            Indices to use to produce a filled cube.
        outline : array
            Indices to use to produce an outline of the cube.
        """
        vtype = [
         (
          'position', np.float32, 3),
         (
          'texcoord', np.float32, 2),
         (
          'normal', np.float32, 3),
         (
          'color', np.float32, 4)]
        itype = np.uint32
        x0, x1 = -0.5, shape[2] - 0.5
        y0, y1 = -0.5, shape[1] - 0.5
        z0, z1 = -0.5, shape[0] - 0.5
        p = np.array([[x0, y0, z0],
         [
          x1, y0, z0],
         [
          x0, y1, z0],
         [
          x1, y1, z0],
         [
          x0, y0, z1],
         [
          x1, y0, z1],
         [
          x0, y1, z1],
         [
          x1, y1, z1]])
        n = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0],
         [
          -1, 0, 1], [0, -1, 0], [0, 0, -1]])
        c = np.array([[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [1, 0, 1, 1],
         [
          1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 0, 1], [0, 0, 0, 1]])
        t = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
        faces_p = [
         0, 1, 2, 3,
         0, 3, 4, 5,
         0, 5, 6, 1,
         1, 6, 7, 2,
         7, 4, 3, 2,
         4, 7, 6, 5]
        faces_c = [0, 1, 2, 3,
         0, 3, 4, 5,
         0, 5, 6, 1,
         1, 6, 7, 2,
         7, 4, 3, 2,
         4, 7, 6, 5]
        faces_n = [0, 0, 0, 0,
         1, 1, 1, 1,
         2, 2, 2, 2,
         3, 3, 3, 3,
         4, 4, 4, 4,
         5, 5, 5, 5]
        faces_t = [0, 1, 2, 3,
         0, 1, 2, 3,
         0, 1, 2, 3,
         3, 2, 1, 0,
         0, 1, 2, 3,
         0, 1, 2, 3]
        vertices = np.zeros(24, vtype)
        vertices['position'] = p[faces_p]
        vertices['normal'] = n[faces_n]
        vertices['color'] = c[faces_c]
        vertices['texcoord'] = t[faces_t]
        filled = np.resize(np.array([0, 1, 2, 0, 2, 3], dtype=itype), 36)
        filled += np.repeat(4 * np.arange(6, dtype=itype), 6)
        filled = filled.reshape((len(filled) // 3, 3))
        outline = np.resize(np.array([0, 1, 1, 3, 3, 2, 2, 0], dtype=itype), 48)
        outline = np.array([0, 1, 0, 2, 2, 3, 1, 3,
         0, 6, 1, 7, 2, 10, 3, 14,
         6, 7, 6, 10, 10, 14, 7, 14])
        return (
         vertices, filled, outline)

    def set_rendering_params(self, tf_method, cmap, combo_color_method, interpolation_method):
        """Set rendering parameters for the visualised volume.

        Parameters
        ----------
        tf_method : str
            Transfer function method
        cmap : str
            Color map (e.g. hot, RbBl...)
        combo_color_method : str
            Color method (e.g. mom0, mom1, rgb)
        interpolation_method : str
            Interpolation method
        """
        self.volume.method = tf_method
        self.volume.cmap = cmap
        self.volume.color_method = combo_color_method
        self.volume.interpolation = interpolation_method
        if self.volume.color_method == 0:
            label = str(self.bunit)
            clim = self.volume.clim
        else:
            label = str(self.vel_type)
            clim = self.clim_vel

    def set_threshold(self, threshold):
        """Set threshold value for the visualised volume.

        Parameters
        ----------
        threshold : int, float
        """
        try:
            threshold = float(threshold)
        except:
            print('Threshold: needs to be a float')

        try:
            threshold -= self.volume.clim[0]
            threshold /= self.volume.clim[1] - self.volume.clim[0]
            self.volume.threshold = threshold
        except:
            print('Invalid threshold')

    def set_color_scale(self, color_scale):
        """Set color scale value for the visualised volume.

        Parameters
        ----------
        color_scale: str
            Scaling function (e.g. linear, log, exp)
        """
        self.volume.color_scale = color_scale

    def set_box_filter_size(self, filter_size):
        """Set box filter kernel size value for the visualised volume.

        Parameters
        ----------
        filter_size: int
            Filter kernel size. Number of neighbours considered during the convolution.
        """
        self.volume.filter_size = filter_size

    def set_filter_type(self, filter_type):
        """Set box filter type for the visualised volume.

        The two filter methods currently available are `filter out`, or `rescale`.

        Parameters
        ----------
        filter_type : int
            Type of filter
        """
        self.volume.filter_type = filter_type

    def set_gaussian_filter(self, use_gaussian_filter, gaussian_filter_size):
        """Set gaussian filter parameters.

        Parameters
        ----------
        use_gaussian_filter : int
            0 or 1, compute the gaussian filter (1) or not (0).
        gaussian_filter_size : int
            Size of the kernel. Number of neighbours considered during the convolution.
        """
        self.volume.use_gaussian_filter = use_gaussian_filter
        self.volume.gaussian_filter_size = gaussian_filter_size

    def set_high_discard_filter(self, high_discard_filter_value, scaled_value, filter_type):
        """Set high discard filter value (values higher than this will be discarded).

        Parameters
        ----------
        high_discard_filter_value : int, float
            Upper limit.
        scaled_value : int, float
            High discard value scaled to data range
        filter_type : str
            Filter type
        """
        self.volume.high_discard_filter_value = high_discard_filter_value
        self.update_clim('high', scaled_value, filter_type)

    def set_low_discard_filter(self, low_discard_filter_value, scaled_value, filter_type):
        """Set low discard value (values lower than this will be discarded).

        Parameters
        ----------
        low_discard_filter_value : int, float
            Lower limit
        scaled_value : int, float
            Scaled value
        filter_type : str
            Filter type
        """
        self.volume.low_discard_filter_value = low_discard_filter_value
        self.update_clim('low', scaled_value, filter_type)

    def update_clim(self, type, value, filter_type):
        """Update color limit (clim)

        Parameters
        ----------
        type : str
            bound type (low or high)
        value : int, float
            New value to be set
        filter_type : str
            Filter type
        """
        if self.volume.color_method == 0:
            if filter_type == 'Rescale':
                if type == 'low':
                    self.cbar.clim = [
                     value, self.cbar.clim[1]]
                if type == 'high':
                    self.cbar.clim = [
                     self.cbar.clim[0], value]

    def set_density_factor(self, density_factor):
        """Set density factor

        Parameters
        ----------
        density_factor : int, float
            Factor used with AVIP to set the transparency level
        """
        self.volume.density_factor = density_factor

    def set_fov(self, fov):
        """Set the field of view of the camera.

        Parameters
        ----------
        fov : int, float
            Field of view
        """
        self.view.camera.fov = fov

    def set_camera(self, cam, fov):
        """Set camera type.

        Parameters
        ----------
        cam : str
            Camera type (based on vispy's cameras)
        fov : int, float
            Camera's field of view
        """
        if cam == 'Perspectivecamera':
            self.view.camera = scene.cameras.PerspectiveCamera(parent=(self.view.scene), fov=(float(fov)),
              name='Perspectivecamera',
              center=(0.5, 0.5, 0.5))
        if cam == 'Turntable':
            self.view.camera = scene.cameras.TurntableCamera(parent=(self.view.scene), elevation=0.0,
              azimuth=0.0,
              fov=(float(fov)),
              name='Turntable')
        if cam == 'Fly':
            self.view.camera = scene.cameras.FlyCamera(parent=(self.view.scene), fov=(float(fov)),
              name='Fly')
        if cam == 'Arcball':
            self.view.camera = scene.cameras.ArcballCamera(parent=(self.view.scene), fov=(float(fov)),
              name='Arcball')

    def set_autorotate(self, flag):
        """Set autorotate value.

        Parameters
        ----------
        flag : bool
            Should it autorotate or not. True: autorotate. False: will not autorotate
        """
        if flag == True:
            self.timer.start(0.01)
        else:
            self.timer.stop()

    def rotate(self, event):
        """Perform a rotation of the visualisation.

        Function to which a timer connects to.
        """
        self.angle = 3.6
        self.view.camera.orbit(self.angle, 0)

    def set_log_scale(self, flag):
        """Set the log scaling.

        Parameters
        ----------
        flag : bool
            Log scale or not.

        Note
        ----
        Not currently being used.
        """
        self.volume.log_scale = flag

    def set_scaling(self, scalex, scaley, scalez):
        """Set x, y, or z scaling (transform).

        Parameters
        ----------
        scalex : int, float
            scaling factor for the x axis
        scaley: int, float
            scaling factor for the y axis
        scalez: int, float
            scaling factor for the z axis
        """
        self.axis.transform = self.volume.transform = scene.STTransform(scale=(scalex, scalez, scaley), translate=(
         -scalex ** 2, -scalez ** 2, -scaley ** 2))

    def set_transform(self, x, y, z):
        """Set the transform.

        Deprecated.
        """
        self.unfreeze()
        self.axis.transform = self.volume.transform = scene.STTransform(translate=(x, y, z))
        self.freeze()