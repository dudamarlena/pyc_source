# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\geometry.py
# Compiled at: 2020-04-19 12:30:33
# Size of source mod 2**32: 64750 bytes
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from aerosandbox.visualization import Figure3D
import copy
try:
    from xfoil import XFoil
    from xfoil import model as xfoil_model
except ModuleNotFoundError:
    pass

from aerosandbox.tools.casadi_tools import *
pio.renderers.default = 'browser'

class AeroSandboxObject:

    def substitute_solution(self, sol):
        """
        Substitutes a solution from CasADi's solver.
        :param sol:
        :return:
        """
        for attrib_name in dir(self):
            attrib_orig = getattr(self, attrib_name)
            if not isinstance(attrib_orig, bool):
                if isinstance(attrib_orig, int):
                    continue
                try:
                    setattr(self, attrib_name, sol.value(attrib_orig))
                except NotImplementedError:
                    pass

                if isinstance(attrib_orig, list):
                    try:
                        new_attrib_orig = []
                        for item in attrib_orig:
                            new_attrib_orig.append(item.substitute_solution(sol))

                        setattr(self, attrib_name, new_attrib_orig)
                    except:
                        pass

                try:
                    setattr(self, attrib_name, attrib_orig.substitute_solution(sol))
                except:
                    pass

        return self


class Airplane(AeroSandboxObject):
    __doc__ = '\n    Definition for an airplane (or other vehicle/item to analyze).\n    '

    def __init__(self, name='Untitled', x_ref=0, y_ref=0, z_ref=0, mass_props=None, wings=[], fuselages=[], s_ref=None, c_ref=None, b_ref=None):
        self.name = name
        self.xyz_ref = cas.vertcat(x_ref, y_ref, z_ref)
        self.wings = wings
        self.fuselages = fuselages
        if len(self.wings) > 0:
            self.set_ref_dims_from_wing(main_wing_index=0)
        if s_ref is not None:
            self.s_ref = s_ref
        if c_ref is not None:
            self.c_ref = c_ref
        if b_ref is not None:
            self.b_ref = b_ref
        assert self.name is not None
        assert self.xyz_ref is not None
        assert self.s_ref is not None
        assert self.c_ref is not None
        assert self.b_ref is not None

    def __repr__(self):
        return 'Airplane %s (%i wings, %i fuselages)' % (
         self.name,
         len(self.wings),
         len(self.fuselages))

    def set_ref_dims_from_wing(self, main_wing_index=0):
        main_wing = self.wings[main_wing_index]
        self.s_ref = main_wing.area()
        self.b_ref = main_wing.span()
        self.c_ref = main_wing.mean_geometric_chord()

    def set_paneling_everywhere(self, n_chordwise_panels, n_spanwise_panels):
        for wing in self.wings:
            wing.chordwise_panels = n_chordwise_panels
            for xsec in wing.xsecs:
                xsec.spanwise_panels = n_spanwise_panels

    def set_spanwise_paneling_everywhere(self, n_spanwise_panels):
        for wing in self.wings:
            for xsec in wing.xsecs:
                xsec.spanwise_panels = n_spanwise_panels

    def draw(self, show=True, colorscale='mint', colorbar_title='Component ID', draw_quarter_chord=True):
        """
        Draws the airplane using a Plotly interface.
        :param show: Do you want to show the figure? [boolean]
        :param colorscale: Which colorscale do you want to use? ("viridis", "plasma", mint", etc.)
        :param draw_quarter_chord: Do you want to draw the quarter-chord? [boolean]
        :return: A plotly figure object [go.Figure]
        """
        fig = Figure3D()
        for wing_id in range(len(self.wings)):
            wing = self.wings[wing_id]
            for xsec_id in range(len(wing.xsecs) - 1):
                xsec_1 = wing.xsecs[xsec_id]
                xsec_2 = wing.xsecs[(xsec_id + 1)]
                le_start = xsec_1.xyz_le + wing.xyz_le
                te_start = xsec_1.xyz_te() + wing.xyz_le
                le_end = xsec_2.xyz_le + wing.xyz_le
                te_end = xsec_2.xyz_te() + wing.xyz_le
                fig.add_quad(points=[
                 le_start,
                 le_end,
                 te_end,
                 te_start],
                  intensity=wing_id,
                  mirror=(wing.symmetric))
                if draw_quarter_chord:
                    fig.add_line(points=[
                     0.75 * le_start + 0.25 * te_start,
                     0.75 * le_end + 0.25 * te_end],
                      mirror=(wing.symmetric))

        for fuse_id in range(len(self.fuselages)):
            fuse = self.fuselages[fuse_id]
            for xsec_id in range(len(fuse.xsecs) - 1):
                xsec_1 = fuse.xsecs[xsec_id]
                xsec_2 = fuse.xsecs[(xsec_id + 1)]
                r1 = xsec_1.radius
                r2 = xsec_2.radius
                points_1 = np.zeros((fuse.circumferential_panels, 3))
                points_2 = np.zeros((fuse.circumferential_panels, 3))
                for point_index in range(fuse.circumferential_panels):
                    rot = angle_axis_rotation_matrix(2 * cas.pi * point_index / fuse.circumferential_panels, [
                     1, 0, 0], True).toarray()
                    points_1[point_index, :] = rot @ np.array([0, 0, r1])
                    points_2[point_index, :] = rot @ np.array([0, 0, r2])

                points_1 = points_1 + np.array(fuse.xyz_le).reshape(-1) + np.array(xsec_1.xyz_c).reshape(-1)
                points_2 = points_2 + np.array(fuse.xyz_le).reshape(-1) + np.array(xsec_2.xyz_c).reshape(-1)
                for point_index in range(fuse.circumferential_panels):
                    fig.add_quad(points=[
                     points_1[point_index % fuse.circumferential_panels, :],
                     points_1[(point_index + 1) % fuse.circumferential_panels, :],
                     points_2[(point_index + 1) % fuse.circumferential_panels, :],
                     points_2[point_index % fuse.circumferential_panels, :]],
                      intensity=fuse_id,
                      mirror=(fuse.symmetric))

        return fig.draw(show=show,
          colorscale=colorscale,
          colorbar_title=colorbar_title)

    def is_symmetric(self):
        """
        Returns a boolean describing whether the airplane is geometrically entirely symmetric across the XZ-plane.
        :return: [boolean]
        """
        for wing in self.wings:
            for xsec in wing.xsecs:
                if not xsec.control_surface_type == 'symmetric':
                    if not xsec.control_surface_deflection == 0:
                        return False
                    else:
                        if not (wing.symmetric or xsec.xyz_le[1] == 0):
                            return False
                        if not xsec.twist == 0:
                            return xsec.twist_axis[0] == 0 and xsec.twist_axis[2] == 0 or False
                        return xsec.airfoil.CL_function(0, 1000000.0, 0, 0) == 0 or False
                    return xsec.airfoil.Cm_function(0, 1000000.0, 0, 0) == 0 or False

        return True

    def write_aswing(self, filepath=None):
        """
        Contributed by Brent Avery, Edited by Peter Sharpe. Work in progress.
        Writes a geometry file compatible with Mark Drela's ASWing.
        :param filepath: Filepath to write to. Should include ".asw" extension [string]
        :return: None
        """
        if filepath is None:
            filepath = '%s.asw' % self.name
        with open(filepath, 'w+') as (f):
            f.write('\n'.join([
             '#============',
             'Name',
             self.name,
             'End',
             '',
             '#============',
             'Units',
             'L 0.3048 m',
             'T 1.0  s',
             'F 4.450 N',
             'End',
             '',
             '#============',
             'Constant',
             '#  g     rho_0     a_0',
             '%f %f %f' % (9.81, 1.205, 343.3),
             'End',
             '', '#============',
             'Reference',
             '#   Sref    Cref    Bref',
             '%f %f %f' % (self.s_ref, self.c_ref, self.b_ref),
             'End',
             '',
             '#============',
             'Ground',
             '#  Nbeam  t',
             '%i %i' % (1, 0),
             'End']))
            for i, wing in enumerate(self.wings):
                xsecs = wing.xsecs
                chordalfa = []
                coords = []
                max_le = {abs(xsecs[(-1)].x_le - xsecs[0].x_le): 'sec.x_le', 
                 abs(xsecs[(-1)].y_le - xsecs[0].y_le): 'sec.y_le', 
                 abs(xsecs[(-1)].z_le - xsecs[0].z_le): 'sec.z_le'}
                for xsec in xsecs:
                    if max_le.get(max(max_le)) == 'sec.x_le':
                        t = xsec.x_le
                    else:
                        if max_le.get(max(max_le)) == 'sec.y_le':
                            t = xsec.y_le
                        else:
                            if max_le.get(max(max_le)) == 'sec.z_le':
                                t = xsec.z_le
                            chordalfa.append('    '.join([str(t), str(xsec.chord), str(xsec.twist)]))
                            coords.append('    '.join([
                             str(t), str(xsec.x_le + wing.xyz_le[0]), str(xsec.y_le + wing.xyz_le[1]),
                             str(xsec.z_le + wing.xyz_le[2])]))

                f.write('\n'.join([
                 '',
                 '#============',
                 'Beam %i' % (i + 1),
                 wing.name,
                 't    chord    twist',
                 '\n'.join(chordalfa),
                 '#',
                 't    x    y    z',
                 '\n'.join(coords),
                 'End']))


class Wing(AeroSandboxObject):
    __doc__ = '\n    Definition for a wing.\n    If the wing is symmetric across the XZ plane, just define the right half and supply "symmetric = True" in the constructor.\n    If the wing is not symmetric across the XZ plane, just define the wing.\n    '

    def __init__(self, name='Untitled Wing', x_le=0, y_le=0, z_le=0, xsecs=[], symmetric=False, chordwise_panels=8, chordwise_spacing='cosine'):
        self.name = name
        self.xyz_le = cas.vertcat(x_le, y_le, z_le)
        self.xsecs = xsecs
        self.symmetric = symmetric
        self.chordwise_panels = chordwise_panels
        self.chordwise_spacing = chordwise_spacing

    def __repr__(self):
        return 'Wing %s (%i xsecs, %s)' % (
         self.name,
         len(self.xsecs),
         'symmetric' if self.symmetric else 'not symmetric')

    def area(self, type='wetted'):
        """
        Returns the area, with options for various ways of measuring this.
         * wetted: wetted area
         * projected: area projected onto the XY plane (top-down view)
        :param type:
        :return:
        """
        area = 0
        for i in range(len(self.xsecs) - 1):
            chord_eff = (self.xsecs[i].chord + self.xsecs[(i + 1)].chord) / 2
            this_xyz_te = self.xsecs[i].xyz_te()
            that_xyz_te = self.xsecs[(i + 1)].xyz_te()
            if type == 'wetted':
                span_le_eff = cas.sqrt((self.xsecs[i].xyz_le[1] - self.xsecs[(i + 1)].xyz_le[1]) ** 2 + (self.xsecs[i].xyz_le[2] - self.xsecs[(i + 1)].xyz_le[2]) ** 2)
                span_te_eff = cas.sqrt((this_xyz_te[1] - that_xyz_te[1]) ** 2 + (this_xyz_te[2] - that_xyz_te[2]) ** 2)
            else:
                if type == 'projected':
                    span_le_eff = cas.fabs(self.xsecs[i].xyz_le[1] - self.xsecs[(i + 1)].xyz_le[1])
                    span_te_eff = cas.fabs(this_xyz_te[1] - that_xyz_te[1])
                else:
                    raise ValueError("Bad value of 'type'!")
            span_eff = (span_le_eff + span_te_eff) / 2
            area += chord_eff * span_eff

        if self.symmetric:
            area *= 2
        return area

    def span(self, type='wetted'):
        """
        Returns the span, with options for various ways of measuring this.
         * wetted: Adds up YZ-distances of each section piece by piece
         * yz: YZ-distance between the root and tip of the wing
         * y: Y-distance between the root and tip of the wing
         * z: Z-distance between the root and tip of the wing
        If symmetric, this is doubled to obtain the full span.
        :param type: One of the above options, as a string.
        :return: span
        """
        if type == 'wetted':
            span = 0
            for i in range(len(self.xsecs) - 1):
                sect1_xyz_le = self.xsecs[i].xyz_le
                sect2_xyz_le = self.xsecs[(i + 1)].xyz_le
                sect1_xyz_te = self.xsecs[i].xyz_te()
                sect2_xyz_te = self.xsecs[(i + 1)].xyz_te()
                span_le = cas.sqrt((sect1_xyz_le[1] - sect2_xyz_le[1]) ** 2 + (sect1_xyz_le[2] - sect2_xyz_le[2]) ** 2)
                span_te = cas.sqrt((sect1_xyz_te[1] - sect2_xyz_te[1]) ** 2 + (sect1_xyz_te[2] - sect2_xyz_te[2]) ** 2)
                span_eff = (span_le + span_te) / 2
                span += span_eff

        else:
            if type == 'yz':
                root = self.xsecs[0]
                tip = self.xsecs[(-1)]
                span = cas.sqrt((root.xyz_le[1] - tip.xyz_le[1]) ** 2 + (root.xyz_le[2] - tip.xyz_le[2]) ** 2)
            else:
                if type == 'y':
                    root = self.xsecs[0]
                    tip = self.xsecs[(-1)]
                    span = cas.fabs(tip.xyz_le[1] - root.xyz_le[1])
                else:
                    if type == 'z':
                        root = self.xsecs[0]
                        tip = self.xsecs[(-1)]
                        span = cas.fabs(tip.xyz_le[2] - root.xyz_le[2])
                    else:
                        raise ValueError("Bad value of 'type'!")
        if self.symmetric:
            span *= 2
        return span

    def aspect_ratio(self):
        return self.span() ** 2 / self.area()

    def has_symmetric_control_surfaces(self):
        for xsec in self.xsecs:
            if not xsec.control_surface_type == 'symmetric':
                return False

        return True

    def mean_geometric_chord(self):
        """
        Returns the mean geometric chord of the wing (S/b).
        :return:
        """
        return self.area() / self.span()

    def mean_twist_angle(self):
        r"""
        Returns the mean twist angle (in degrees) of the wing, weighted by span.
        You can think of it as \int_{b}(twist)db, where b is span.
        WARNING: This function's output is only exact in the case where all of the cross sections have the same twist axis!
        :return: mean twist angle (in degrees)
        """
        span = []
        for i in range(len(self.xsecs) - 1):
            sect1_xyz_le = self.xsecs[i].xyz_le
            sect2_xyz_le = self.xsecs[(i + 1)].xyz_le
            sect1_xyz_te = self.xsecs[i].xyz_te()
            sect2_xyz_te = self.xsecs[(i + 1)].xyz_te()
            span_le = cas.sqrt((sect1_xyz_le[1] - sect2_xyz_le[1]) ** 2 + (sect1_xyz_le[2] - sect2_xyz_le[2]) ** 2)
            span_te = cas.sqrt((sect1_xyz_te[1] - sect2_xyz_te[1]) ** 2 + (sect1_xyz_te[2] - sect2_xyz_te[2]) ** 2)
            span_eff = (span_le + span_te) / 2
            span.append(span_eff)

        twist_span_product = 0
        for i in range(len(self.xsecs)):
            xsec = self.xsecs[i]
            if i > 0:
                twist_span_product += xsec.twist * span[(i - 1)] / 2
            if i < len(self.xsecs) - 1:
                twist_span_product += xsec.twist * span[i] / 2

        mean_twist = twist_span_product / cas.sum1((cas.vertcat)(*span))
        return mean_twist

    def mean_sweep_angle(self):
        """
        Returns the mean quarter-chord sweep angle (in degrees) of the wing, relative to the x-axis.
        Positive sweep is backwards, negative sweep is forward.
        :return:
        """
        root_quarter_chord = 0.75 * self.xsecs[0].xyz_le + 0.25 * self.xsecs[0].xyz_te()
        tip_quarter_chord = 0.75 * self.xsecs[(-1)].xyz_le + 0.25 * self.xsecs[(-1)].xyz_te()
        vec = tip_quarter_chord - root_quarter_chord
        vec_norm = vec / cas.norm_2(vec)
        sin_sweep = vec_norm[0]
        sweep_deg = cas.asin(sin_sweep) * 180 / cas.pi
        return sweep_deg

    def approximate_center_of_pressure(self):
        """
        Returns the approximate location of the center of pressure. Given as the area-weighted quarter chord of the wing.
        :return: [x, y, z] of the approximate center of pressure
        """
        areas = []
        quarter_chord_centroids = []
        for i in range(len(self.xsecs) - 1):
            chord_eff = (self.xsecs[i].chord + self.xsecs[(i + 1)].chord) / 2
            this_xyz_te = self.xsecs[i].xyz_te()
            that_xyz_te = self.xsecs[(i + 1)].xyz_te()
            span_le_eff = cas.sqrt((self.xsecs[i].xyz_le[1] - self.xsecs[(i + 1)].xyz_le[1]) ** 2 + (self.xsecs[i].xyz_le[2] - self.xsecs[(i + 1)].xyz_le[2]) ** 2)
            span_te_eff = cas.sqrt((this_xyz_te[1] - that_xyz_te[1]) ** 2 + (this_xyz_te[2] - that_xyz_te[2]) ** 2)
            span_eff = (span_le_eff + span_te_eff) / 2
            areas.append(chord_eff * span_eff)
            quarter_chord_centroids.append((0.75 * self.xsecs[i].xyz_le + 0.25 * self.xsecs[i].xyz_te() + 0.75 * self.xsecs[(i + 1)].xyz_le + 0.25 * self.xsecs[(i + 1)].xyz_te()) / 2 + self.xyz_le)

        areas = (cas.vertcat)(*areas)
        quarter_chord_centroids = cas.transpose((cas.horzcat)(*quarter_chord_centroids))
        total_area = cas.sum1(areas)
        approximate_cop = cas.sum1(areas / cas.sum1(areas) * quarter_chord_centroids)
        if self.symmetric:
            approximate_cop[:, 1] = 0
        return approximate_cop


class WingXSec(AeroSandboxObject):
    __doc__ = '\n    Definition for a wing cross section ("X-section").\n    '

    def __init__(self, x_le=0, y_le=0, z_le=0, chord=0, twist=0, twist_axis=cas.DM([0, 1, 0]), airfoil=None, control_surface_type='symmetric', control_surface_hinge_point=0.75, control_surface_deflection=0, spanwise_panels=8, spanwise_spacing='cosine'):
        if airfoil is None:
            raise ValueError("'airfoil' argument missing! (Needs an object of Airfoil type)")
        self.x_le = x_le
        self.y_le = y_le
        self.z_le = z_le
        self.chord = chord
        self.twist = twist
        self.twist_axis = twist_axis
        self.airfoil = airfoil
        self.control_surface_type = control_surface_type
        self.control_surface_hinge_point = control_surface_hinge_point
        self.control_surface_deflection = control_surface_deflection
        self.spanwise_panels = spanwise_panels
        self.spanwise_spacing = spanwise_spacing
        self.xyz_le = cas.vertcat(x_le, y_le, z_le)

    def __repr__(self):
        return 'WingXSec (airfoil = %s, chord = %f, twist = %f)' % (
         self.airfoil.name,
         self.chord,
         self.twist)

    def xyz_te(self):
        rot = angle_axis_rotation_matrix(self.twist * cas.pi / 180, self.twist_axis)
        xyz_te = self.xyz_le + rot @ cas.vertcat(self.chord, 0, 0)
        return xyz_te


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
        from . import airfoils
        try:
            with importlib.resources.open_text(airfoils, name) as (f):
                raw_text = f.readlines()
        except:
            with importlib.resources.open_text(airfoils, name + '.dat') as (f):
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

    def draw(self, draw_mcl=True):
        x = np.array(self.coordinates[:, 0]).reshape(-1)
        y = np.array(self.coordinates[:, 1]).reshape(-1)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x,
          y=y,
          mode='lines+markers',
          name='Airfoil'))
        if draw_mcl:
            x_mcl = np.linspace(0, 1, 101)
            y_mcl = self.local_camber(x_mcl)
            fig.add_trace(go.Scatter(x=x_mcl,
              y=y_mcl,
              mode='lines+markers',
              name='Mean Camber Line (MCL)'))
        fig.update_layout(xaxis_title='x',
          yaxis_title='y',
          yaxis=dict(scaleanchor='x', scaleratio=1),
          title=('%s Airfoil' % self.name))
        fig.show()

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

    def xfoil_a(self, alpha, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=100, verbose=True):
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
        cl, cd, cm, Cp_min = xf.a(alpha)
        a = alpha
        return {'alpha':a, 
         'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}

    def xfoil_cl(self, cl, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=100, verbose=True):
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
        a, cd, cm, Cp_min = xf.cl(cl)
        cl = cl
        return {'alpha':a, 
         'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}

    def xfoil_aseq(self, a_start, a_end, a_step, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=100, verbose=True):
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
        a, cl, cd, cm, Cp_min = xf.aseq(a_start, a_end, a_step)
        return {'alpha':a, 
         'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}

    def xfoil_cseq(self, cl_start, cl_end, cl_step, Re=0, M=0, n_crit=9, xtr_bot=1, xtr_top=1, reset_bls=False, repanel=False, max_iter=100, verbose=True):
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
        a, cl, cd, cm, Cp_min = xf.cseq(cl_start, cl_end, cl_step)
        return {'alpha':a, 
         'Cl':cl, 
         'Cd':cd, 
         'Cm':cm, 
         'Cp_min':Cp_min}


class Fuselage(AeroSandboxObject):
    __doc__ = '\n    Definition for a fuselage or other slender body (pod, etc.).\n    For now, all fuselages are assumed to be circular and fairly closely aligned with the body x axis. (<10 deg or so) # TODO update if this changes\n    '

    def __init__(self, name='Untitled Fuselage', x_le=0, y_le=0, z_le=0, xsecs=[], symmetric=False, circumferential_panels=24):
        self.name = name
        self.xyz_le = cas.vertcat(x_le, y_le, z_le)
        self.xsecs = xsecs
        self.symmetric = symmetric
        assert circumferential_panels % 2 == 0
        self.circumferential_panels = circumferential_panels

    def area_wetted(self):
        """
        Returns the wetted area of the fuselage.

        If the Fuselage is symmetric (i.e. two symmetric wingtip pods),
        returns the combined wetted area of both pods.
        :return:
        """
        area = 0
        for i in range(len(self.xsecs) - 1):
            this_radius = self.xsecs[i].radius
            next_radius = self.xsecs[(i + 1)].radius
            x_separation = self.xsecs[(i + 1)].x_c - self.xsecs[i].x_c
            area += cas.pi * (this_radius + next_radius) * cas.sqrt((this_radius - next_radius) ** 2 + x_separation ** 2)

        if self.symmetric:
            area *= 2
        return area

    def area_projected(self):
        """
        Returns the area of the fuselage as projected onto the XY plane (top-down view).

        If the Fuselage is symmetric (i.e. two symmetric wingtip pods),
        returns the combined projected area of both pods.
        :return:
        """
        area = 0
        for i in range(len(self.xsecs) - 1):
            this_radius = self.xsecs[i].radius
            next_radius = self.xsecs[(i + 1)].radius
            x_separation = self.xsecs[(i + 1)].x_c - self.xsecs[i].x_c
            area += (this_radius + next_radius) * x_separation

        if self.symmetric:
            area *= 2
        return area

    def length(self):
        """
        Returns the total front-to-back length of the fuselage. Measured as the difference between the x-coordinates
        of the leading and trailing cross sections.
        :return:
        """
        return cas.fabs(self.xsecs[(-1)].x_c - self.xsecs[0].x_c)


class FuselageXSec(AeroSandboxObject):
    __doc__ = '\n    Definition for a fuselage cross section ("X-section").\n    '

    def __init__(self, x_c=0, y_c=0, z_c=0, radius=0):
        self.x_c = x_c
        self.y_c = y_c
        self.z_c = z_c
        self.radius = radius
        self.xyz_c = cas.vertcat(x_c, y_c, z_c)

    def xsec_area(self):
        """
        Returns the FuselageXSec's cross-sectional (xsec) area.
        :return:
        """
        return cas.pi * self.radius ** 2


def reflect_over_XZ_plane(input_vector):
    output_vector = input_vector
    shape = output_vector.shape
    if len(shape) == 1 and shape[0] == 3:
        output_vector = output_vector * cas.vertcat(1, -1, 1)
    else:
        if len(shape) == 2 and shape[1] == 1 and shape[0] == 3:
            output_vector = output_vector * cas.vertcat(1, -1, 1)
        else:
            if len(shape) == 2 and shape[1] == 3:
                output_vector = cas.horzcat(output_vector[:, 0], -1 * output_vector[:, 1], output_vector[:, 2])
            else:
                raise Exception('Invalid input for reflect_over_XZ_plane!')
    return output_vector


def cosspace(min=0, max=1, n_points=50):
    mean = (max + min) / 2
    amp = (max - min) / 2
    return mean + amp * cas.cos(cas.linspace(cas.pi, 0, n_points))


def np_cosspace(min=0, max=1, n_points=50):
    mean = (max + min) / 2
    amp = (max - min) / 2
    return mean + amp * np.cos(np.linspace(np.pi, 0, n_points))


def angle_axis_rotation_matrix(angle, axis, axis_already_normalized=False):
    if not axis_already_normalized:
        axis = axis / cas.norm_2(axis)
    sintheta = cas.sin(angle)
    costheta = cas.cos(angle)
    cpm = cas.vertcat(cas.horzcat(0, -axis[2], axis[1]), cas.horzcat(axis[2], 0, -axis[0]), cas.horzcat(-axis[1], axis[0], 0))
    outer_axis = axis @ cas.transpose(axis)
    rot_matrix = costheta * cas.DM.eye(3) + sintheta * cpm + (1 - costheta) * outer_axis
    return rot_matrix


def linspace_3D(start, stop, n_points):
    x = cas.linspace(start[0], stop[0], n_points)
    y = cas.linspace(start[1], stop[1], n_points)
    z = cas.linspace(start[2], stop[2], n_points)
    points = cas.horzcat(x, y, z)
    return points


def plot_point_cloud(p):
    """
    Plots an Nx3 point cloud
    :param p:
    :return:
    """
    p = np.array(p)
    px.scatter_3d(x=(p[:, 0]), y=(p[:, 1]), z=(p[:, 2])).show()