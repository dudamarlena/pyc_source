# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\geometry\airfoil.py
# Compiled at: 2020-04-22 20:05:44
# Size of source mod 2**32: 47795 bytes
from aerosandbox.geometry.common import *

class Airfoil:

    def __init__(self, name=None, coordinates=None, CL_function=lambda alpha, Re, mach, deflection: alpha * np.pi / 180 * (2 * np.pi), CDp_function=lambda alpha, Re, mach, deflection: (1 + (alpha / 5) ** 2) * 2 * (0.074 / Re ** 0.2), Cm_function=lambda alpha, Re, mach, deflection: 0):
        """
        Creates an Airfoil object.
        :param name: Name of the airfoil [string]
        :param coordinates: Either:
            a) None if "name" is a 4-digit NACA airfoil (e.g. "naca2412"),
            a) None if "name" is the name of an airfoil in the UIUC airfoil database (must be the name of the .dat file, e.g. "s1223"),
            b) a filepath to a .dat file (including the .dat) [string], or
            c) an array of coordinates [Nx2 ndarray].
        :param CL_function:
        :param CDp_function:
        :param Cm_function:
        """
        self.name = name if name is not None else 'Untitled'
        self.coordinates = None
        if coordinates is not None:
            if type(coordinates) is str:
                try:
                    self.populate_coordinates_from_filepath(filepath=coordinates)
                except Exception as e:
                    try:
                        print(e)
                        print("Couldn't populate coordinates from filepath!")
                    finally:
                        e = None
                        del e

            else:
                self.coordinates = coordinates
        else:
            try:
                self.populate_coordinates_from_naca()
            except:
                try:
                    self.populate_coordinates_from_UIUC_database()
                except:
                    pass

        self.CL_function = CL_function
        self.CDp_function = CDp_function
        self.Cm_function = Cm_function

    def __repr__(self):
        return 'Airfoil %s (%i points)' % (
         self.name,
         self.coordinates.shape[0] if self.coordinates is not None else 0)

    def populate_coordinates_from_naca(self, n_points_per_side=100):
        """
        Populates a variable called self.coordinates with the coordinates of the airfoil.
        :param n_points_per_side: Number of points per side of the airfoil (top/bottom).
        :return: None (in-place)
        """
        name = self.name.lower().strip()
        assert 'naca' in name, 'Not a NACA airfoil!'
        nacanumber = name.split('naca')[1]
        assert nacanumber.isdigit(), "Couldn't parse the number of the NACA airfoil!"
        assert len(nacanumber) == 4, 'Can only parse 4-digit NACA airfoils at the moment!'
        max_camber = int(nacanumber[0]) * 0.01
        camber_loc = int(nacanumber[1]) * 0.1
        thickness = int(nacanumber[2:]) * 0.01
        x_t = cosspace(0, 1, n_points_per_side)
        y_t = 5 * thickness * (0.2969 * x_t ** 0.5 - 0.126 * x_t - 0.3516 * x_t ** 2 + 0.2843 * x_t ** 3 - 0.1015 * x_t ** 4)
        if camber_loc == 0:
            camber_loc = 0.5
        y_c = cas.if_else(x_t <= camber_loc, max_camber / camber_loc ** 2 * (2 * camber_loc * x_t - x_t ** 2), max_camber / (1 - camber_loc) ** 2 * (1 - 2 * camber_loc + 2 * camber_loc * x_t - x_t ** 2))
        dycdx = cas.if_else(x_t <= camber_loc, 2 * max_camber / camber_loc ** 2 * (camber_loc - x_t), 2 * max_camber / (1 - camber_loc) ** 2 * (camber_loc - x_t))
        theta = cas.atan(dycdx)
        x_U = x_t - y_t * cas.sin(theta)
        x_L = x_t + y_t * cas.sin(theta)
        y_U = y_c + y_t * cas.cos(theta)
        y_L = y_c - y_t * cas.cos(theta)
        x_U, y_U = x_U[::-1, :], y_U[::-1, :]
        x_L, y_L = x_L[1:], y_L[1:]
        x = cas.vertcat(x_U, x_L)
        y = cas.vertcat(y_U, y_L)
        self.coordinates = np.array(cas.horzcat(x, y))

    def populate_coordinates_from_UIUC_database(self):
        """
        Populates a variable called self.coordinates with the coordinates of the airfoil.
        :return: None (in-place)
        """
        name = self.name.lower().strip()
        import importlib.resources
        from aerosandbox import airfoil_database
        try:
            with importlib.resources.open_text(airfoil_database, name) as (f):
                raw_text = f.readlines()
        except:
            with importlib.resources.open_text(airfoil_database, name + '.dat') as (f):
                raw_text = f.readlines()

        trimmed_text = []
        for line in raw_text:
            try:
                line_np = np.fromstring(line, sep=' ')
                if line_np.shape[0] == 2:
                    trimmed_text.append(line_np)
            except:
                pass

        coordinates = np.hstack(trimmed_text).reshape((-1, 2))
        self.coordinates = coordinates

    def populate_coordinates_from_filepath(self, filepath):
        """
        Populates a variable called self.coordinates with the coordinates of the airfoil.
        :param filepath: A DAT file to pull the airfoil coordinates from. (includes the ".dat") [string]
        :return: None (in-place)
        """
        try:
            with open(filepath, 'r') as (f):
                raw_text = f.readlines()
        except:
            with open(filepath + '.dat', 'r') as (f):
                raw_text = f.readlines()

        trimmed_text = []
        for line in raw_text:
            try:
                line_np = np.fromstring(line, sep=' ')
                if line_np.shape[0] == 2:
                    trimmed_text.append(line_np)
            except:
                pass

        coordinates = np.hstack(trimmed_text).reshape((-1, 2))
        self.coordinates = coordinates

    def local_camber(self, x_over_c=np.linspace(0, 1, 101)):
        """
        Returns the local camber of the airfoil.
        :param x_over_c: The x/c locations to calculate the camber at [1D array, more generally, an iterable of floats]
        :return: Local camber of the airfoil (y/c) [1D array].
        """
        upper = self.upper_coordinates()[::-1]
        lower = self.lower_coordinates()
        upper_interpolated = np.interp(x_over_c, upper[:, 0], upper[:, 1])
        lower_interpolated = np.interp(x_over_c, lower[:, 0], lower[:, 1])
        return (upper_interpolated + lower_interpolated) / 2

    def local_thickness(self, x_over_c=np.linspace(0, 1, 101)):
        """
        Returns the local thickness of the airfoil.
        :param x_over_c: The x/c locations to calculate the thickness at [1D array, more generally, an iterable of floats]
        :return: Local thickness of the airfoil (y/c) [1D array].
        """
        upper = self.upper_coordinates()[::-1]
        lower = self.lower_coordinates()
        upper_interpolated = np.interp(x_over_c, upper[:, 0], upper[:, 1])
        lower_interpolated = np.interp(x_over_c, lower[:, 0], lower[:, 1])
        return upper_interpolated - lower_interpolated

    def draw(self, draw_mcl=True, backend='plotly'):
        """
        Draw the airfoil object.
        :param draw_mcl: Should we draw the mean camber line (MCL)? [boolean]
        :param backend: Which backend should we use? "plotly" or "matplotlib" [boolean]
        :return: None
        """
        x = np.array(self.coordinates[:, 0]).reshape(-1)
        y = np.array(self.coordinates[:, 1]).reshape(-1)
        if backend == 'plotly':
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x,
              y=y,
              mode='lines+markers',
              name='Airfoil'))
            if draw_mcl:
                x_mcl = np.linspace(np.min(x), np.max(x), len(x))
                y_mcl = self.local_camber(x_mcl)
                fig.add_trace(go.Scatter(x=x_mcl,
                  y=y_mcl,
                  mode='lines+markers',
                  name='Mean Camber Line (MCL)'))
            fig.update_layout(xaxis_title='x/c',
              yaxis_title='y/c',
              yaxis=dict(scaleanchor='x', scaleratio=1),
              title=('%s Airfoil' % self.name))
            fig.show()
        else:
            if backend == 'matplotlib':
                fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.8), dpi=200)
                plt.plot(x, y, '.-', zorder=11, color='#280887')
                if draw_mcl:
                    x_mcl = np.linspace(np.min(x), np.max(x), len(x))
                    y_mcl = self.local_camber(x_mcl)
                    plt.plot(x_mcl, y_mcl, '-', zorder=4, color='#28088744')
                plt.axis('equal')
                plt.xlabel('$x/c$')
                plt.ylabel('$y/c$')
                plt.title('%s Airfoil' % self.name)
                plt.tight_layout()
                plt.show()

    def LE_index(self):
        return np.argmin(self.coordinates[:, 0])

    def lower_coordinates(self):
        return self.coordinates[self.LE_index():, :]

    def upper_coordinates(self):
        return self.coordinates[:self.LE_index() + 1, :]

    def TE_thickness(self):
        return self.local_thickness(x_over_c=1)

    def TE_angle(self):
        upper_TE_vec = self.coordinates[0, :] - self.coordinates[1, :]
        lower_TE_vec = self.coordinates[-1, :] - self.coordinates[-2, :]
        return 180 / np.pi * np.arctan2(upper_TE_vec[0] * lower_TE_vec[1] - upper_TE_vec[1] * lower_TE_vec[0], upper_TE_vec[0] * lower_TE_vec[0] + upper_TE_vec[1] * upper_TE_vec[1])

    def area(self):
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        x_n = np.roll(x, -1)
        y_n = np.roll(y, -1)
        a = x * y_n - x_n * y
        A = 0.5 * np.sum(a)
        return A

    def centroid(self):
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        x_n = np.roll(x, -1)
        y_n = np.roll(y, -1)
        a = x * y_n - x_n * y
        A = 0.5 * np.sum(a)
        x_c = 1 / (6 * A) * np.sum(a * (x + x_n))
        y_c = 1 / (6 * A) * np.sum(a * (y + y_n))
        centroid = np.array([x_c, y_c])
        return centroid

    def Ixx(self):
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        x_n = np.roll(x, -1)
        y_n = np.roll(y, -1)
        a = x * y_n - x_n * y
        A = 0.5 * np.sum(a)
        x_c = 1 / (6 * A) * cas.sum1(a * (x + x_n))
        y_c = 1 / (6 * A) * cas.sum1(a * (y + y_n))
        centroid = np.array([x_c, y_c])
        Ixx = 0.08333333333333333 * np.sum(a * (y ** 2 + y * y_n + y_n ** 2))
        Iuu = Ixx - A * centroid[1] ** 2
        return Iuu

    def Iyy(self):
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        x_n = np.roll(x, -1)
        y_n = np.roll(y, -1)
        a = x * y_n - x_n * y
        A = 0.5 * np.sum(a)
        x_c = 1 / (6 * A) * np.sum(a * (x + x_n))
        y_c = 1 / (6 * A) * np.sum(a * (y + y_n))
        centroid = np.array([x_c, y_c])
        Iyy = 0.08333333333333333 * np.sum(a * (x ** 2 + x * x_n + x_n ** 2))
        Ivv = Iyy - A * centroid[0] ** 2
        return Ivv

    def Ixy(self):
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        x_n = np.roll(x, -1)
        y_n = np.roll(y, -1)
        a = x * y_n - x_n * y
        A = 0.5 * np.sum(a)
        x_c = 1 / (6 * A) * np.sum(a * (x + x_n))
        y_c = 1 / (6 * A) * np.sum(a * (y + y_n))
        centroid = np.array([x_c, y_c])
        Ixy = 0.041666666666666664 * np.sum(a * (x * y_n + 2 * x * y + 2 * x_n * y_n + x_n * y))
        Iuv = Ixy - A * centroid[0] * centroid[1]
        return Iuv

    def J(self):
        x = self.coordinates[:, 0]
        y = self.coordinates[:, 1]
        x_n = np.roll(x, -1)
        y_n = np.roll(y, -1)
        a = x * y_n - x_n * y
        A = 0.5 * np.sum(a)
        x_c = 1 / (6 * A) * np.sum(a * (x + x_n))
        y_c = 1 / (6 * A) * np.sum(a * (y + y_n))
        centroid = np.array([x_c, y_c])
        Ixx = 0.08333333333333333 * np.sum(a * (y ** 2 + y * y_n + y_n ** 2))
        Iyy = 0.08333333333333333 * np.sum(a * (x ** 2 + x * x_n + x_n ** 2))
        J = Ixx + Iyy
        return J

    def repanel(self, n_points_per_side=100, inplace=False):
        """
        Returns a repaneled version of the airfoil with cosine-spaced coordinates on the upper and lower surfaces.
        :param n_points_per_side: Number of points per side (upper and lower) of the airfoil [int]
            Notes: The number of points defining the final airfoil will be n_points_per_side*2-1,
            since one point (the leading edge point) is shared by both the upper and lower surfaces.
        :param inplace: Whether to perform this as an in-place operation or return the new airfoil as a newly instantiated object [boolean]
        :return: If inplace is True, None. If inplace is False, the new airfoil [Airfoil].
        """
        upper_original_coors = self.upper_coordinates()
        lower_original_coors = self.lower_coordinates()
        upper_distances_between_points = ((upper_original_coors[:-1, 0] - upper_original_coors[1:, 0]) ** 2 + (upper_original_coors[:-1, 1] - upper_original_coors[1:, 1]) ** 2) ** 0.5
        lower_distances_between_points = ((lower_original_coors[:-1, 0] - lower_original_coors[1:, 0]) ** 2 + (lower_original_coors[:-1, 1] - lower_original_coors[1:, 1]) ** 2) ** 0.5
        upper_distances_from_TE = np.hstack((0, np.cumsum(upper_distances_between_points)))
        lower_distances_from_LE = np.hstack((0, np.cumsum(lower_distances_between_points)))
        upper_distances_from_TE_normalized = upper_distances_from_TE / upper_distances_from_TE[(-1)]
        lower_distances_from_LE_normalized = lower_distances_from_LE / lower_distances_from_LE[(-1)]
        s = np_cosspace(0, 1, n_points_per_side)
        x_upper = np.interp(s, upper_distances_from_TE_normalized, upper_original_coors[:, 0])
        y_upper = np.interp(s, upper_distances_from_TE_normalized, upper_original_coors[:, 1])
        x_lower = np.interp(s, lower_distances_from_LE_normalized, lower_original_coors[:, 0])
        y_lower = np.interp(s, lower_distances_from_LE_normalized, lower_original_coors[:, 1])
        x_coors = np.hstack((x_upper, x_lower[1:]))
        y_coors = np.hstack((y_upper, y_lower[1:]))
        coordinates = np.vstack((x_coors, y_coors)).T
        airfoil = self if inplace else copy.deepcopy(self)
        if 'Repaneled' not in airfoil.name:
            airfoil.name += ' (Repaneled)'
        airfoil.coordinates = coordinates
        return airfoil

    def add_control_surface(self, deflection=0.0, hinge_point_x=0.75, inplace=False):
        """
        Returns a version of the airfoil with a control surface added at a given point. Implicitly repanels the airfoil as part of this operation.
        :param deflection: deflection angle [degrees]. Downwards-positive.
        :param hinge_point_x: location of the hinge, as a fraction of chord [float].
        :param inplace: Whether to perform this as an in-place operation or return the new airfoil as a newly instantiated object [boolean]
        :return: If inplace is True, None. If inplace is False, the new airfoil [Airfoil].
        """
        sintheta = np.sin(-cas.pi / 180 * deflection)
        costheta = np.cos(-cas.pi / 180 * deflection)
        rotation_matrix = np.array([
         [
          costheta, sintheta],
         [
          -sintheta, costheta]])
        hinge_point_y = self.local_camber(hinge_point_x)
        hinge_point = np.hstack((hinge_point_x, hinge_point_y))
        c = np.copy(self.coordinates)
        c[c[:, 0] > hinge_point_x] = (rotation_matrix.T @ (c[(c[:, 0] > hinge_point_x)] - hinge_point).T).T + hinge_point
        coordinates = c
        airfoil = self if inplace else copy.deepcopy(self)
        if 'Flapped' not in airfoil.name:
            airfoil.name += ' (Flapped)'
        airfoil.coordinates = coordinates
        return airfoil

    def write_dat(self, filepath):
        """
        Writes a .dat file corresponding to this airfoil to a filepath.
        :param filepath: filepath (including the filename and .dat extension) [string]
        :return: None
        """
        with open(filepath, 'w+') as (f):
            f.writelines([
             self.name + '\n'] + ['     %.12f    %.12f\n' % tuple(coordinate) for coordinate in self.coordinates])

    def xfoil_a(self, alpha, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=20, verbose=False):
        """
        Interface to XFoil, provided through the open-source xfoil Python library by DARcorporation.
        Point analysis at a given alpha.
        :param alpha: angle of attack [deg]
        :param Re: Reynolds number
        :param M: Mach number
        :param n_crit: Critical Tollmien-Schlichting wave amplification factor
        :param xtr_bot: Bottom trip location [x/c]
        :param xtr_top: Top trip location [x/c]
        :param reset_bls: Reset boundary layer parameters upon initialization?
        :param repanel: Repanel airfoil within XFoil?
        :param max_iter: Maximum number of global Newton iterations
        :param verbose: Choose whether you want to suppress output from xfoil [boolean]
        :return: A dict of {alpha, Cl, Cd, Cm, Cp_min}
        """
        try:
            xf = XFoil()
        except NameError:
            raise NameError('It appears that the XFoil-Python interface is not installed, so unfortunately you can\'t use this function!\nTo install it, run "pip install xfoil" in your terminal, or manually install it from: https://github.com/DARcorporation/xfoil-python .\nNote: users on UNIX systems have reported errors with installing this (Windows seems fine).')

        def run():
            xf.airfoil = xfoil_model.Airfoil(x=(np.array(self.coordinates[:, 0]).reshape(-1)),
              y=(np.array(self.coordinates[:, 1]).reshape(-1)))
            xf.Re = Re
            xf.M = M
            xf.n_crit = n_crit
            xf.xtr = (xtr_top, xtr_bot)
            if reset_bls:
                xf.reset_bls()
            if repanel:
                xf.repanel()
            xf.max_iter = max_iter
            return xf.a(alpha)

        if verbose:
            cl, cd, cm, Cp_min = run()
        else:
            with stdout_redirected():
                cl, cd, cm, Cp_min = run()
        a = alpha
        return {'alpha':a, 
         'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}

    def xfoil_cl(self, cl, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=20, verbose=False):
        """
        Interface to XFoil, provided through the open-source xfoil Python library by DARcorporation.
        Point analysis at a given lift coefficient.
        :param cl: Lift coefficient
        :param Re: Reynolds number
        :param M: Mach number
        :param n_crit: Critical Tollmien-Schlichting wave amplification factor
        :param xtr_bot: Bottom trip location [x/c]
        :param xtr_top: Top trip location [x/c]
        :param reset_bls: Reset boundary layer parameters upon initialization?
        :param repanel: Repanel airfoil within XFoil?
        :param max_iter: Maximum number of global Newton iterations
        :param verbose: Choose whether you want to suppress output from xfoil [boolean]
        :return: A dict of {alpha, Cl, Cd, Cm, Cp_min}
        """
        try:
            xf = XFoil()
        except NameError:
            raise NameError('It appears that the XFoil-Python interface is not installed, so unfortunately you can\'t use this function!\nTo install it, run "pip install xfoil" in your terminal, or manually install it from: https://github.com/DARcorporation/xfoil-python .\nNote: users on UNIX systems have reported errors with installing this (Windows seems fine).')

        def run():
            xf.airfoil = xfoil_model.Airfoil(x=(np.array(self.coordinates[:, 0]).reshape(-1)),
              y=(np.array(self.coordinates[:, 1]).reshape(-1)))
            xf.Re = Re
            xf.M = M
            xf.n_crit = n_crit
            xf.xtr = (xtr_top, xtr_bot)
            if reset_bls:
                xf.reset_bls()
            if repanel:
                xf.repanel()
            xf.max_iter = max_iter
            return xf.cl(cl)

        if verbose:
            a, cd, cm, Cp_min = run()
        else:
            with stdout_redirected():
                a, cd, cm, Cp_min = run()
        cl = cl
        return {'alpha':a, 
         'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}

    def xfoil_aseq(self, a_start, a_end, a_step, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=20, verbose=False):
        """
        Interface to XFoil, provided through the open-source xfoil Python library by DARcorporation.
        Alpha sweep analysis.
        :param a_start: First angle of attack [deg]
        :param a_end: Last angle of attack [deg]
        :param a_step: Amount to increment angle of attack by [deg]
        :param Re: Reynolds number
        :param M: Mach number
        :param n_crit: Critical Tollmien-Schlichting wave amplification factor
        :param xtr_bot: Bottom trip location [x/c]
        :param xtr_top: Top trip location [x/c]
        :param reset_bls: Reset boundary layer parameters upon initialization?
        :param repanel: Repanel airfoil within XFoil?
        :param max_iter: Maximum number of global Newton iterations
        :param verbose: Choose whether you want to suppress output from xfoil [boolean]
        :return: A dict of {alpha, Cl, Cd, Cm, Cp_min}
        """
        try:
            xf = XFoil()
        except NameError:
            raise NameError('It appears that the XFoil-Python interface is not installed, so unfortunately you can\'t use this function!\nTo install it, run "pip install xfoil" in your terminal, or manually install it from: https://github.com/DARcorporation/xfoil-python .\nNote: users on UNIX systems have reported errors with installing this (Windows seems fine).')

        def run():
            xf.airfoil = xfoil_model.Airfoil(x=(np.array(self.coordinates[:, 0]).reshape(-1)),
              y=(np.array(self.coordinates[:, 1]).reshape(-1)))
            xf.Re = Re
            xf.M = M
            xf.n_crit = n_crit
            xf.xtr = (xtr_top, xtr_bot)
            if reset_bls:
                xf.reset_bls()
            if repanel:
                xf.repanel()
            xf.max_iter = max_iter
            return xf.aseq(a_start, a_end, a_step)

        if verbose:
            a, cl, cd, cm, Cp_min = run()
        else:
            with stdout_redirected():
                a, cl, cd, cm, Cp_min = run()
        return {'alpha':a,  'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}

    def xfoil_cseq(self, cl_start, cl_end, cl_step, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=20, verbose=False):
        """
        Interface to XFoil, provided through the open-source xfoil Python library by DARcorporation.
        Lift coefficient sweep analysis.
        :param cl_start: First lift coefficient [unitless]
        :param cl_end: Last lift coefficient [unitless]
        :param cl_step: Amount to increment lift coefficient by [unitless]
        :param Re: Reynolds number
        :param M: Mach number
        :param n_crit: Critical Tollmien-Schlichting wave amplification factor
        :param xtr_bot: Bottom trip location [x/c]
        :param xtr_top: Top trip location [x/c]
        :param reset_bls: Reset boundary layer parameters upon initialization?
        :param repanel: Repanel airfoil within XFoil?
        :param max_iter: Maximum number of global Newton iterations
        :param verbose: Choose whether you want to suppress output from xfoil [boolean]
        :return: A dict of {alpha, Cl, Cd, Cm, Cp_min}
        """
        try:
            xf = XFoil()
        except NameError:
            raise NameError('It appears that the XFoil-Python interface is not installed, so unfortunately you can\'t use this function!\nTo install it, run "pip install xfoil" in your terminal, or manually install it from: https://github.com/DARcorporation/xfoil-python .\nNote: users on UNIX systems have reported errors with installing this (Windows seems fine).')

        def run():
            xf.airfoil = xfoil_model.Airfoil(x=(np.array(self.coordinates[:, 0]).reshape(-1)),
              y=(np.array(self.coordinates[:, 1]).reshape(-1)))
            xf.Re = Re
            xf.M = M
            xf.n_crit = n_crit
            xf.xtr = (xtr_top, xtr_bot)
            if reset_bls:
                xf.reset_bls()
            if repanel:
                xf.repanel()
            xf.max_iter = max_iter
            return xf.cseq(cl_start, cl_end, cl_step)

        if verbose:
            a, cl, cd, cm, Cp_min = run()
        else:
            with stdout_redirected():
                a, cl, cd, cm, Cp_min = run()
        return {'alpha':a,  'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}

    def get_xfoil_data(self, a_start=-6, a_end=12, a_step=0.25, a_init=0, Re_start=10000.0, Re_end=5000000.0, n_Res=50, mach=0, max_iter=20, repanel=True, parallel=True, verbose=True):
        """ # TODO finish docstring
        Calculates aerodynamic performance data for a particular airfoil with XFoil.
        Does a 2D grid sweep of the alpha-Reynolds space at a particular Mach number.
        Populates two new instance variables:
            * self.xfoil_data_1D: A dict of XFoil data at all calculated operating points (1D arrays, NaNs removed)
            * self.xfoil_data_2D: A dict of XFoil data at all calculated operating points (2D arrays, NaNs present)
        :param a_start: Lower bound of angle of attack [deg]
        :param a_end: Upper bound of angle of attack [deg]
        :param a_step: Angle of attack increment size [deg]
        :param a_init: Angle of attack to initialize runs at. Should solve easily (0 recommended) [deg]
        :param Re_start: Reynolds number to begin sweep at. [unitless]
        :param Re_end: Reynolds number to end sweep at. [unitless]
        :param n_Res: Number of Reynolds numbers to sweep. Points are log-spaced.
        :param mach: Mach number to sweep at.
        :param max_iter: Maximum number of XFoil iterations per op-point.
        :param repanel: Should we interally repanel the airfoil within XFoil before running? [boolean]
            Consider disabling this if you try to do optimization based on this data (for smoothness reasons).
            Otherwise, it's generally a good idea to leave this on.
        :param parallel: Should we run in parallel? Generally results in significant speedup, but might not run
            correctly on some machines. Disable this if it's a problem. [boolean]
        :param verbose: Should we do verbose output? [boolean]
        :return: None (in-place operation that creates self.xfoil_data_1D and self.xfoil_data_2D)
        """
        if not a_init > a_start:
            raise AssertionError
        else:
            assert a_init < a_end
            assert Re_start < Re_end
            assert n_Res >= 1
            assert mach >= 0
            Res = np.logspace(np.log10(Re_start), np.log10(Re_end), n_Res)

            def get_xfoil_data_at_Re(Re):
                import numpy as np
                run_data_upper = self.xfoil_aseq(a_start=(a_init + a_step),
                  a_end=a_end,
                  a_step=a_step,
                  Re=Re,
                  repanel=repanel,
                  max_iter=max_iter,
                  M=mach,
                  reset_bls=True)
                run_data_lower = self.xfoil_aseq(a_start=a_init,
                  a_end=a_start,
                  a_step=(-a_step),
                  Re=Re,
                  repanel=repanel,
                  max_iter=max_iter,
                  M=mach,
                  reset_bls=True)
                run_data = {k:np.hstack((run_data_lower[k][::-1], run_data_upper[k])) for k in run_data_upper.keys()}
                return run_data

            start_time = time.time()
            if not parallel:
                runs_data = [get_xfoil_data_at_Re(Re) for Re in Res]
            else:
                pool = mp.Pool(mp.cpu_count())
                runs_data = pool.map(get_xfoil_data_at_Re, Res)
                pool.close()
        run_time = time.time() - start_time
        if verbose:
            print('XFoil Runtime: %.3f sec' % run_time)
        xfoil_data_2D = {}
        for k in runs_data[0].keys():
            xfoil_data_2D[k] = np.vstack([d[k] for d in runs_data])

        xfoil_data_2D['Re'] = np.tile(Res, (
         xfoil_data_2D['alpha'].shape[1],
         1)).T
        np.place(arr=(xfoil_data_2D['Re']),
          mask=(np.isnan(xfoil_data_2D['alpha'])),
          vals=(np.NaN))
        xfoil_data_2D['alpha_indices'] = np.arange(a_start, a_end + a_step / 2, a_step)
        xfoil_data_2D['Re_indices'] = Res
        self.xfoil_data_2D = xfoil_data_2D
        xfoil_data_1D = {k:remove_nans(xfoil_data_2D[k].reshape(-1)) for k in xfoil_data_2D.keys()}
        self.xfoil_data_1D = xfoil_data_1D

    def has_xfoil_data(self, raise_exception_if_absent=True):
        """
        Runs a quick check to see if this airfoil has XFoil data.
        :param raise_exception_if_absent: Boolean flag to raise an Exception if XFoil data is not found.
        :return: Boolean of whether or not XFoil data is present.
        """
        data_present = hasattr(self, 'xfoil_data_1D') and hasattr(self, 'xfoil_data_2D')
        if not data_present:
            if raise_exception_if_absent:
                raise Exception("This Airfoil does not yet have XFoil data,\n                so you can't run the function you've called.\n                To get XFoil data, first call:\n                    Airfoil.get_xfoil_data()\n                which will perform an in-place update that\n                provides the data.")
        return data_present

    def plot_xfoil_data_contours(self):
        self.has_xfoil_data()
        from matplotlib import colors
        d = self.xfoil_data_1D
        fig = plt.figure(figsize=(10, 8), dpi=200)
        ax = fig.add_subplot(311)
        coords = self.coordinates
        plt.plot((coords[:, 0]), (coords[:, 1]), '.-', color='#280887')
        plt.xlabel('$x/c$')
        plt.ylabel('$y/c$')
        plt.title('XFoil Data for %s Airfoil' % self.name)
        plt.axis('equal')
        style.use('default')
        ax = fig.add_subplot(323)
        x = d['Re']
        y = d['alpha']
        z = d['Cl']
        levels = np.linspace(-0.5, 1.5, 21)
        norm = None
        CF = ax.tricontourf(x, y, z, levels=levels, norm=norm, cmap='plasma', extend='both')
        C = ax.tricontour(x, y, z, levels=levels, norm=norm, colors='k', extend='both', linewidths=0.5)
        cbar = plt.colorbar(CF, format='%.2f')
        cbar.set_label('$C_l$')
        plt.grid(False)
        plt.xlabel('$Re$')
        plt.ylabel('$\\alpha$')
        plt.title('$C_l$ from $Re$, $\\alpha$')
        ax.set_xscale('log')
        ax = fig.add_subplot(324)
        x = d['Re']
        y = d['alpha']
        z = d['Cd']
        levels = np.logspace(-2.5, -1, 21)
        norm = colors.PowerNorm(gamma=0.5, vmin=(np.min(levels)), vmax=(np.max(levels)))
        CF = ax.tricontourf(x, y, z, levels=levels, norm=norm, cmap='plasma', extend='both')
        C = ax.tricontour(x, y, z, levels=levels, norm=norm, colors='k', extend='both', linewidths=0.5)
        cbar = plt.colorbar(CF, format='%.3f')
        cbar.set_label('$C_d$')
        plt.grid(False)
        plt.xlabel('$Re$')
        plt.ylabel('$\\alpha$')
        plt.title('$C_d$ from $Re$, $\\alpha$')
        ax.set_xscale('log')
        ax = fig.add_subplot(325)
        x = d['Re']
        y = d['alpha']
        z = d['Cl'] / d['Cd']
        x = x[(d['alpha'] >= 0)]
        y = y[(d['alpha'] >= 0)]
        z = z[(d['alpha'] >= 0)]
        levels = np.logspace(1, np.log10(150), 21)
        norm = colors.PowerNorm(gamma=0.5, vmin=(np.min(levels)), vmax=(np.max(levels)))
        CF = ax.tricontourf(x, y, z, levels=levels, norm=norm, cmap='plasma', extend='both')
        C = ax.tricontour(x, y, z, levels=levels, norm=norm, colors='k', extend='both', linewidths=0.5)
        cbar = plt.colorbar(CF, format='%.1f')
        cbar.set_label('$L/D$')
        plt.grid(False)
        plt.xlabel('$Re$')
        plt.ylabel('$\\alpha$')
        plt.title('$L/D$ from $Re$, $\\alpha$')
        ax.set_xscale('log')
        ax = fig.add_subplot(326)
        x = d['Re']
        y = d['alpha']
        z = d['Cm']
        levels = np.linspace(-0.15, 0, 21)
        norm = None
        CF = ax.tricontourf(x, y, z, levels=levels, norm=norm, cmap='plasma', extend='both')
        C = ax.tricontour(x, y, z, levels=levels, norm=norm, colors='k', extend='both', linewidths=0.5)
        cbar = plt.colorbar(CF, format='%.2f')
        cbar.set_label('$C_m$')
        plt.grid(False)
        plt.xlabel('$Re$')
        plt.ylabel('$\\alpha$')
        plt.title('$C_m$ from $Re$, $\\alpha$')
        ax.set_xscale('log')
        plt.tight_layout()
        plt.show()

    def plot_xfoil_data_polars(self, n_lines_max=20, Cd_plot_max=0.04):
        self.has_xfoil_data()
        n_lines_max = min(n_lines_max, len(self.xfoil_data_2D['Re_indices']))
        fig, ax = plt.subplots(1, 1, figsize=(7, 6), dpi=200)
        indices = np.array((np.round(np.linspace(0, len(self.xfoil_data_2D['Re_indices']) - 1, n_lines_max))),
          dtype=int)
        indices_worth_plotting = [np.min(remove_nans(self.xfoil_data_2D['Cd'][index, :])) < Cd_plot_max for index in indices]
        indices = indices[indices_worth_plotting]
        colors = plt.cm.rainbow(np.linspace(0, 1, len(indices)))[::-1]
        for i, Re in enumerate(self.xfoil_data_2D['Re_indices'][indices]):
            Cds = remove_nans(self.xfoil_data_2D['Cd'][indices[i], :])
            Cls = remove_nans(self.xfoil_data_2D['Cl'][indices[i], :])
            Cd_min = np.min(Cds)
            if Cd_min < Cd_plot_max:
                plt.plot((Cds * 10000.0),
                  Cls,
                  label=('Re = %s' % eng_string(Re)),
                  color=(colors[i]))

        plt.xlim(0, Cd_plot_max * 10000.0)
        plt.ylim(0, 2)
        plt.xlabel('$C_d \\cdot 10^4$')
        plt.ylabel('$C_l$')
        plt.title('XFoil Polars for %s Airfoil' % self.name)
        plt.tight_layout()
        plt.legend()
        plt.show()