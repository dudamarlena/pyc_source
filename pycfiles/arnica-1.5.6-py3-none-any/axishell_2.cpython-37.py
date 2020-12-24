# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duranton/Documents/CERFACS/CODES/arnica/src/arnica/utils/axishell_2.py
# Compiled at: 2020-03-30 05:30:51
# Size of source mod 2**32: 6025 bytes
""" axishell module
to create x-axisymmetric shells for scientific computations
"""
import numpy as np
from arnica.utils.shell import Shell

class AxiShell(Shell):
    __doc__ = "\\\n    *Base class for x-axisymmetric computationnal shells*\n\n    AxiShell class is based on Shell class, inheriting of Shell methods.\n    At initialization, the shell is builded an an x-axisymmetric shell.\n\n    Some attributes are based on **u** and **v**, defined as the curvilinear\\\n    longitudinal (x/r) abscissa and curvilinear azimutal (theta) abscissa\\\n    respectively.\n\n    ::\n                      (x_n, r_n)\n                _____X_____\n         ___----     |     ----___     Cylindrical system\n        \\            |            /    Example longi/u <=> r\n         \\           |           /\n          \\          |          /      r - longi/u\n           \\         |         /       ^\n            \\        | (x_0, r_0)      |\n             \\      _X_      /         |\n              \\__---   ---__/          X-----> theta - azi/v\n                                      x\n\n              ................\n          ...                 ..       Cylindrical system\n        ..                     .       Example longi/u <=> x/r\n        .                      .\n        .      ................         r\n        .     .                         ^\n         .     ...................      |\n         ..                             |\n            ......................      X-----> x\n                          <--      theta - azi/v\n                     x/r - longi/u\n\n    :param n_azi: Number of azimuthal shell points\n    :type n_azi: int\n    :param n_longi: Number of longitudinal shell points\n    :type n_longi: int\n    :param angle: Range angle of the axicylindrical geometry\n    :type angle: float\n    :param ctrl_pts_x: Array of dim (n,) of x-coordinates of the points defining the spline\n    :param ctrl_pts_r: Array of dim (n,) of r-coordinates of the points defining the spline\n\n    Optionals arguments :\n    :param angle_min: Minimum angle of the shell\n    :type angle_min: float\n\n    Public attributes :\n\n        - **shape** - Shape of the shell : (n_azi, n_longi)\n        - **width_matrix** - Dict containing thickness matrices of shape 'shape'\n        - **matrix** - Dict containing fields of shape 'shape' - To deprecate\n\n    Private attributes :\n\n        - **_xyz**\n        - **_rad**\n        - **_theta**\n        - **_n_x**\n        - **_n_r**\n        - **_n_y**\n        - **_n_z**\n        - **_du**\n        - **_dv**\n        - **_abs_curv**\n        - **_du**\n        - **_dv**\n        - **_abs_curv**\n        - **_dwu**\n        - **_dwv**\n        - **_surf**\n\n    "

    def __init__(self, n_azi, n_longi, angle, ctrl_pts_x, ctrl_pts_r, angle_min=None):
        """
        *Initialize an AxiShell object*
        """
        Shell.__init__(self, n_azi, n_longi)
        self.ctrl_pts_x = ctrl_pts_x
        self.ctrl_pts_r = ctrl_pts_r
        self.angle = angle
        self.angle_min = angle_min
        self._build_shell()

    def _build_shell(self):
        """
        *Build shell from geometric features*

            - Construct a spline used as base for extrusion              from control points : tck
            - Discretise the spline : shell_crest
            - Compute normal vectors for the 1D shell_crest
            - Compute r,n_x,n_r-components for 2D shell
            - Compute theta-components for 2D shell
            - Compute xyz,n_y,n_z-components for 2D shell
        """
        shell_crest = self._compute_shell_crest(self.ctrl_pts_x, self.ctrl_pts_r)
        self._rad = np.tile(shell_crest[1], (self.shape[0], 1))
        rot_angle = 0
        if self.angle_min is not None:
            rot_angle = 0.5 * self.angle + self.angle_min
        min_theta = (rot_angle - 0.5 * self.angle) * np.pi / 180
        max_theta = (rot_angle + 0.5 * self.angle) * np.pi / 180
        self._theta = np.transpose(np.tile(np.linspace(min_theta, max_theta,
          num=(self.shape[0])), (
         self.shape[1], 1)))
        tmp_x = np.tile(shell_crest[0], (self.shape[0], 1))
        tmp_y = self._rad * np.cos(self._theta)
        tmp_z = self._rad * np.sin(self._theta)
        self._xyz = np.stack((tmp_x, tmp_y, tmp_z), axis=(-1))
        xr_nml_1d = self._compute_shellcrest_nml(shell_crest)
        self._n_r = np.tile(xr_nml_1d[1], (self.shape[0], 1))
        self._n_x = np.tile(xr_nml_1d[0], (self.shape[0], 1))
        self._n_y = self._n_r * np.cos(self._theta)
        self._n_z = self._n_r * np.sin(self._theta)
        self._du = np.pad(np.sqrt(np.diff((self._xyz[:, :, 0]), axis=1) ** 2 + np.diff((self._rad), axis=1) ** 2), ((0, 0),
                                                                                                                    (1, 0)), 'edge')
        self._dv = self._rad * np.pad(np.diff((self._theta), axis=0), ((1, 0), (0, 0)), 'edge')
        self._abs_curv = np.cumsum(np.take(self._du, 0, 0)) - self._du[(0, 0)]
        self._dwu = self._du.copy()
        self._dwu[:, (0, -1)] /= 2
        self._dwv = self._dv.copy()
        self._dwv[(0, -1), :] /= 2
        self._surf = np.multiply(self._dwu, self._dwv)