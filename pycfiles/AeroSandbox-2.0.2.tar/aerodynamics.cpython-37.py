# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics.py
# Compiled at: 2019-08-05 23:38:08
# Size of source mod 2**32: 172031 bytes
import autograd.numpy as np
from autograd import grad
import scipy.linalg as sp_linalg
from numba import jit
import matplotlib.pyplot as plt
import matplotlib as mpl, sys
from .plotting import *
from .geometry import *
from .performance import *
import cProfile, functools, os

def profile(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        try:
            profiler.enable()
            ret = func(*args, **kwargs)
            profiler.disable()
            return ret
        finally:
            filename = os.path.expanduser(os.path.join('~', func.__name__ + '.pstat'))
            profiler.dump_stats(filename)

    return wrapper


class AeroProblem:

    def __init__(self, airplane, op_point):
        self.airplane = airplane
        self.op_point = op_point


class vlm1(AeroProblem):

    def run(self, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print('Running VLM1 calculation...')
        print('DEPRECATION WARNING: VLM1 has been wholly eclipsed in performance and functionality by VLM2 and VLM3. The VLM1 source code has been left intact for validation purposes and backwards-compatibility, but it will not be supported going forward.')
        self.make_panels()
        self.setup_geometry()
        self.setup_operating_point()
        self.calculate_vortex_strengths()
        self.calculate_forces()
        if self.verbose:
            print('VLM1 calculation complete!')

    def make_panels(self):
        if self.verbose:
            print('Making panels...')
        c = np.empty((0, 3))
        n = np.empty((0, 3))
        lv = np.empty((0, 3))
        rv = np.empty((0, 3))
        front_left_vertices = np.empty((0, 3))
        front_right_vertices = np.empty((0, 3))
        back_left_vertices = np.empty((0, 3))
        back_right_vertices = np.empty((0, 3))
        is_trailing_edge = np.empty(0, dtype=bool)
        for wing in self.airplane.wings:
            n_chordwise_coordinates = wing.chordwise_panels + 1
            if wing.chordwise_spacing == 'uniform':
                nondim_chordwise_coordinates = np.linspace(0, 1, n_chordwise_coordinates)
            else:
                if wing.chordwise_spacing == 'cosine':
                    nondim_chordwise_coordinates = cosspace(n_points=n_chordwise_coordinates)
                else:
                    raise Exception('Bad value of wing.chordwise_spacing!')
            wing_coordinates = np.empty((n_chordwise_coordinates, 0, 3))
            wing_normals = np.empty((wing.chordwise_panels, 0, 3))
            for XSec_number in range(len(wing.xsecs) - 1):
                xsec = wing.xsecs[XSec_number]
                next_xsec = wing.xsecs[(XSec_number + 1)]
                n_spanwise_coordinates = xsec.spanwise_panels + 1
                if xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                else:
                    if xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = cosspace(n_points=n_spanwise_coordinates)
                    else:
                        raise Exception('Bad value of section.spanwise_spacing!')
                xsec_xyz_le = xsec.xyz_le + wing.xyz_le
                xsec_xyz_te = xsec.xyz_te() + wing.xyz_le
                next_xsec_xyz_le = next_xsec.xyz_le + wing.xyz_le
                next_xsec_xyz_te = next_xsec.xyz_te() + wing.xyz_le
                section_coordinates = np.empty(shape=(n_chordwise_coordinates, n_spanwise_coordinates, 3))
                for spanwise_coordinate_num in range(len(nondim_spanwise_coordinates)):
                    nondim_spanwise_coordinate = nondim_spanwise_coordinates[spanwise_coordinate_num]
                    local_xyz_le = (1 - nondim_spanwise_coordinate) * xsec_xyz_le + nondim_spanwise_coordinate * next_xsec_xyz_le
                    local_xyz_te = (1 - nondim_spanwise_coordinate) * xsec_xyz_te + nondim_spanwise_coordinate * next_xsec_xyz_te
                    for chordwise_coordinate_num in range(len(nondim_chordwise_coordinates)):
                        nondim_chordwise_coordinate = nondim_chordwise_coordinates[chordwise_coordinate_num]
                        local_coordinate = (1 - nondim_chordwise_coordinate) * local_xyz_le + nondim_chordwise_coordinate * local_xyz_te
                        section_coordinates[chordwise_coordinate_num, spanwise_coordinate_num, :] = local_coordinate

                is_last_section = XSec_number == len(wing.xsecs) - 2
                if not is_last_section:
                    section_coordinates = section_coordinates[:, :-1, :]
                wing_coordinates = np.concatenate((wing_coordinates, section_coordinates), axis=1)
                xsec_chord_vector = xsec_xyz_te - xsec_xyz_le
                next_xsec_chord_vector = next_xsec_xyz_te - next_xsec_xyz_le
                quarter_chord_vector = 0.75 * next_xsec_xyz_le + 0.25 * next_xsec_xyz_te - (0.75 * xsec_xyz_le + 0.25 * xsec_xyz_te)
                xsec_up = np.cross(xsec_chord_vector, quarter_chord_vector)
                xsec_up /= np.linalg.norm(xsec_up)
                xsec_back = xsec_chord_vector / np.linalg.norm(xsec_chord_vector)
                next_xsec_up = np.cross(next_xsec_chord_vector, quarter_chord_vector)
                next_xsec_up /= np.linalg.norm(next_xsec_up)
                next_xsec_back = next_xsec_chord_vector / np.linalg.norm(next_xsec_chord_vector)
                nondim_chordwise_collocation_coordinates = 0.25 * nondim_chordwise_coordinates[:-1] + 0.75 * nondim_chordwise_coordinates[1:]
                xsec_normals_2d = xsec.airfoil.get_mcl_normal_direction_at_chord_fraction(nondim_chordwise_collocation_coordinates)
                next_xsec_normals_2d = next_xsec.airfoil.get_mcl_normal_direction_at_chord_fraction(nondim_chordwise_collocation_coordinates)
                xsec_normals = xsec_up * np.expand_dims((xsec_normals_2d[:, 1]), axis=1) + xsec_back * np.expand_dims((xsec_normals_2d[:, 0]), axis=1)
                next_xsec_normals = next_xsec_up * np.expand_dims((next_xsec_normals_2d[:, 1]), axis=1) + next_xsec_back * np.expand_dims((next_xsec_normals_2d[:, 0]), axis=1)
                nondim_spanwise_collocation_coordinates = 0.5 * nondim_spanwise_coordinates[:-1] + 0.5 * nondim_spanwise_coordinates[1:]
                section_normals = np.expand_dims(xsec_normals, axis=1) * (1 - np.reshape(nondim_spanwise_collocation_coordinates, (1,
                                                                                                                                   -1,
                                                                                                                                   1))) + np.expand_dims(next_xsec_normals, axis=1) * np.reshape(nondim_spanwise_collocation_coordinates, (1,
                                                                                                                                                                                                                                           -1,
                                                                                                                                                                                                                                           1))
                wing_normals = np.concatenate((wing_normals, section_normals), axis=1)

            front_inboard_vertices = wing_coordinates[:-1, :-1, :]
            front_outboard_vertices = wing_coordinates[:-1, 1:, :]
            back_inboard_vertices = wing_coordinates[1:, :-1, :]
            back_outboard_vertices = wing_coordinates[1:, 1:, :]
            is_trailing_edge_this_wing = np.vstack((
             np.zeros((wing_coordinates.shape[0] - 2, wing_coordinates.shape[1] - 1), dtype=bool),
             np.ones((1, wing_coordinates.shape[1] - 1), dtype=bool)))
            collocation_points = 0.25 * (front_inboard_vertices + front_outboard_vertices) / 2 + 0.75 * (back_inboard_vertices + back_outboard_vertices) / 2
            inboard_vortex_points = 0.75 * front_inboard_vertices + 0.25 * back_inboard_vertices
            outboard_vortex_points = 0.75 * front_outboard_vertices + 0.25 * back_outboard_vertices
            collocation_points = np.reshape(collocation_points, (-1, 3), order='F')
            wing_normals = np.reshape(wing_normals, (-1, 3), order='F')
            inboard_vortex_points = np.reshape(inboard_vortex_points, (-1, 3), order='F')
            outboard_vortex_points = np.reshape(outboard_vortex_points, (-1, 3), order='F')
            front_inboard_vertices = np.reshape(front_inboard_vertices, (-1, 3), order='F')
            front_outboard_vertices = np.reshape(front_outboard_vertices, (-1, 3), order='F')
            back_inboard_vertices = np.reshape(back_inboard_vertices, (-1, 3), order='F')
            back_outboard_vertices = np.reshape(back_outboard_vertices, (-1, 3), order='F')
            is_trailing_edge_this_wing = np.reshape(is_trailing_edge_this_wing, (-1), order='F')
            c = np.vstack((c, collocation_points))
            n = np.vstack((n, wing_normals))
            lv = np.vstack((lv, inboard_vortex_points))
            rv = np.vstack((rv, outboard_vortex_points))
            front_left_vertices = np.vstack((front_left_vertices, front_inboard_vertices))
            front_right_vertices = np.vstack((front_right_vertices, front_outboard_vertices))
            back_left_vertices = np.vstack((back_left_vertices, back_inboard_vertices))
            back_right_vertices = np.vstack((back_right_vertices, back_outboard_vertices))
            is_trailing_edge = np.hstack((is_trailing_edge, is_trailing_edge_this_wing))
            if wing.symmetric:
                inboard_vortex_points = reflect_over_XZ_plane(inboard_vortex_points)
                outboard_vortex_points = reflect_over_XZ_plane(outboard_vortex_points)
                collocation_points = reflect_over_XZ_plane(collocation_points)
                wing_normals = reflect_over_XZ_plane(wing_normals)
                front_inboard_vertices = reflect_over_XZ_plane(front_inboard_vertices)
                front_outboard_vertices = reflect_over_XZ_plane(front_outboard_vertices)
                back_inboard_vertices = reflect_over_XZ_plane(back_inboard_vertices)
                back_outboard_vertices = reflect_over_XZ_plane(back_outboard_vertices)
                c = np.vstack((c, collocation_points))
                n = np.vstack((n, wing_normals))
                lv = np.vstack((lv, outboard_vortex_points))
                rv = np.vstack((rv, inboard_vortex_points))
                front_left_vertices = np.vstack((front_left_vertices, front_outboard_vertices))
                front_right_vertices = np.vstack((front_right_vertices, front_inboard_vertices))
                back_left_vertices = np.vstack((back_left_vertices, back_outboard_vertices))
                back_right_vertices = np.vstack((back_right_vertices, back_inboard_vertices))
                is_trailing_edge = np.hstack((is_trailing_edge, is_trailing_edge_this_wing))

        n[(n[:, 0] < 0)] *= -1
        n[(n[:, 1] < 0)] *= -1
        n[(n[:, 2] < 0)] *= -1
        self.c = c
        self.n = n
        self.lv = lv
        self.rv = rv
        self.front_left_vertices = front_left_vertices
        self.front_right_vertices = front_right_vertices
        self.back_left_vertices = back_left_vertices
        self.back_right_vertices = back_right_vertices
        self.n_panels = len(c)
        self.is_trailing_edge = is_trailing_edge

    def setup_geometry(self):
        if self.verbose:
            print('Calculating the collocation influence matrix...')
        self.Vij_collocations = self.calculate_Vij(self.c)
        n_expanded = np.expand_dims(self.n, 1)
        self.AIC = np.sum((self.Vij_collocations * n_expanded),
          axis=2)
        if self.verbose:
            print('Calculating the vortex center influence matrix...')
        self.vortex_centers = (self.lv + self.rv) / 2
        self.Vij_centers = self.calculate_Vij(self.vortex_centers)
        if self.verbose:
            print('LU factorizing the AIC matrix...')
        self.lu, self.piv = sp_linalg.lu_factor(self.AIC)

    def setup_operating_point(self):
        if self.verbose:
            print('Calculating the freestream influence...')
        self.steady_freestream_velocity = self.op_point.compute_freestream_velocity_geometry_axes() * np.ones((
         self.n_panels, 1))
        self.rotation_freestream_velocities = np.zeros((
         self.n_panels, 3))
        self.freestream_velocities = self.steady_freestream_velocity + self.rotation_freestream_velocities
        self.freestream_influences = np.sum((self.freestream_velocities * self.n), axis=1)

    def calculate_vortex_strengths(self):
        if self.verbose:
            print('Calculating vortex strengths...')
        self.vortex_strengths = sp_linalg.lu_solve((self.lu, self.piv), -self.freestream_influences)

    def calculate_forces(self):
        if self.verbose:
            print('Calculating forces on each panel...')
        else:
            Vi_x = self.Vij_centers[:, :, 0] @ self.vortex_strengths + self.freestream_velocities[:, 0]
            Vi_y = self.Vij_centers[:, :, 1] @ self.vortex_strengths + self.freestream_velocities[:, 1]
            Vi_z = self.Vij_centers[:, :, 2] @ self.vortex_strengths + self.freestream_velocities[:, 2]
            Vi_x = np.expand_dims(Vi_x, axis=1)
            Vi_y = np.expand_dims(Vi_y, axis=1)
            Vi_z = np.expand_dims(Vi_z, axis=1)
            Vi = np.hstack((Vi_x, Vi_y, Vi_z))
            self.li = self.rv - self.lv
            density = self.op_point.density
            Vi_cross_li = np.cross(Vi, (self.li), axis=1)
            vortex_strengths_expanded = np.expand_dims((self.vortex_strengths), axis=1)
            self.Fi_geometry = density * Vi_cross_li * vortex_strengths_expanded
            if self.verbose:
                print('Calculating total forces and moments...')
            self.Ftotal_geometry = np.sum((self.Fi_geometry), axis=0)
            self.Ftotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Ftotal_geometry
            self.Mtotal_geometry = np.sum((np.cross(self.vortex_centers - self.airplane.xyz_ref, self.Fi_geometry)), axis=0)
            self.Mtotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Mtotal_geometry
            q = self.op_point.dynamic_pressure()
            s_ref = self.airplane.s_ref
            b_ref = self.airplane.b_ref
            c_ref = self.airplane.c_ref
            self.CL = -self.Ftotal_wind[2] / q / s_ref
            self.CDi = -self.Ftotal_wind[0] / q / s_ref
            self.CY = self.Ftotal_wind[1] / q / s_ref
            self.Cl = self.Mtotal_wind[0] / q / b_ref
            self.Cm = self.Mtotal_wind[1] / q / c_ref
            self.Cn = self.Mtotal_wind[2] / q / b_ref
            if self.CDi == 0:
                self.CL_over_CDi = 0
            else:
                self.CL_over_CDi = self.CL / self.CDi
        if self.verbose:
            print('\nForces\n-----')
        if self.verbose:
            print('CL: ', self.CL)
        if self.verbose:
            print('CDi: ', self.CDi)
        if self.verbose:
            print('CY: ', self.CY)
        if self.verbose:
            print('CL/CDi: ', self.CL_over_CDi)
        if self.verbose:
            print('\nMoments\n-----')
        if self.verbose:
            print('Cl: ', self.Cl)
        if self.verbose:
            print('Cm: ', self.Cm)
        if self.verbose:
            print('Cn: ', self.Cn)

    def calculate_delta_cp(self):
        front_to_back = 0.5 * (self.front_left_vertices + self.front_right_vertices - self.back_left_vertices - self.back_right_vertices)
        self.areas_approx = np.linalg.norm((self.li), axis=1) * np.linalg.norm(front_to_back, axis=1)
        self.Fi_normal = np.einsum('ij,ij->i', self.Fi_geometry, self.n)
        self.pressure_normal = self.Fi_normal / self.areas_approx
        self.delta_cp = self.pressure_normal / self.op_point.dynamic_pressure()

    def get_induced_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vij = self.calculate_Vij(point)
        vortex_strengths_expanded = np.expand_dims(self.vortex_strengths, 1)
        Vi_x = Vij[:, :, 0] @ vortex_strengths_expanded
        Vi_y = Vij[:, :, 1] @ vortex_strengths_expanded
        Vi_z = Vij[:, :, 2] @ vortex_strengths_expanded
        Vi = np.hstack((Vi_x, Vi_y, Vi_z))
        return Vi

    def get_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vi = self.get_induced_velocity_at_point(point)
        freestream = self.op_point.compute_freestream_velocity_geometry_axes()
        V = Vi + freestream
        return V

    def calculate_Vij(self, points):
        points = np.reshape(points, (-1, 3))
        n_points = len(points)
        n_vortices = len(self.lv)
        c_tiled = np.expand_dims(points, 1)
        a = c_tiled - self.lv
        b = c_tiled - self.rv
        a_cross_b = np.cross(a, b, axis=2)
        a_dot_b = np.einsum('ijk,ijk->ij', a, b)
        a_cross_x = np.zeros((n_points, n_vortices, 3))
        a_cross_x[:, :, 1] = a[:, :, 2]
        a_cross_x[:, :, 2] = -a[:, :, 1]
        a_dot_x = a[:, :, 0]
        b_cross_x = np.zeros((n_points, n_vortices, 3))
        b_cross_x[:, :, 1] = b[:, :, 2]
        b_cross_x[:, :, 2] = -b[:, :, 1]
        b_dot_x = b[:, :, 0]
        norm_a = np.linalg.norm(a, axis=2)
        norm_b = np.linalg.norm(b, axis=2)
        norm_a_inv = 1 / norm_a
        norm_b_inv = 1 / norm_b
        bound_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_b, a_cross_b) < 3e-16
        a_dot_b[bound_vortex_singularity_indices] = np.inf
        left_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_x, a_cross_x) < 3e-16
        a_dot_x[left_vortex_singularity_indices] = np.inf
        right_vortex_singularity_indices = np.einsum('ijk,ijk->ij', b_cross_x, b_cross_x) < 3e-16
        b_dot_x[right_vortex_singularity_indices] = np.inf
        term1 = (norm_a_inv + norm_b_inv) / (norm_a * norm_b + a_dot_b)
        term2 = norm_a_inv / (norm_a - a_dot_x)
        term3 = norm_b_inv / (norm_b - b_dot_x)
        term1 = np.expand_dims(term1, 2)
        term2 = np.expand_dims(term2, 2)
        term3 = np.expand_dims(term3, 2)
        Vij = 1 / (4 * np.pi) * (a_cross_b * term1 + a_cross_x * term2 - b_cross_x * term3)
        return Vij

    def calculate_streamlines(self):
        n_steps = 100
        length = 1
        length_per_step = length / n_steps
        seed_points = (0.5 * (self.back_left_vertices + self.back_right_vertices))[self.is_trailing_edge]
        n_streamlines = len(seed_points)
        streamlines = np.zeros((n_streamlines, n_steps, 3))
        streamlines[:, 0, :] = seed_points
        for step_num in range(1, n_steps):
            update_amount = self.get_velocity_at_point(streamlines[:, step_num - 1, :])
            update_amount = update_amount / np.expand_dims(np.linalg.norm(update_amount, axis=1), axis=1)
            update_amount *= length_per_step
            streamlines[:, step_num, :] = streamlines[:, step_num - 1, :] + update_amount

        self.streamlines = streamlines

    def draw(self, draw_delta_cp=True, draw_streamlines=True):
        vertices = np.vstack((
         self.front_left_vertices,
         self.front_right_vertices,
         self.back_right_vertices,
         self.back_left_vertices))
        faces = np.transpose(np.vstack((
         4 * np.ones(self.n_panels),
         np.arange(self.n_panels),
         np.arange(self.n_panels) + self.n_panels,
         np.arange(self.n_panels) + 2 * self.n_panels,
         np.arange(self.n_panels) + 3 * self.n_panels)))
        faces = np.reshape(faces, (-1), order='C')
        wing_surfaces = pv.PolyData(vertices, faces)
        plotter = pv.Plotter()
        if draw_delta_cp:
            if not hasattr(self, 'delta_cp'):
                self.calculate_delta_cp()
            scalars = np.minimum(np.maximum(self.delta_cp, -1), 1)
            cmap = plt.cm.get_cmap('viridis')
            plotter.add_mesh(wing_surfaces, scalars=scalars, cmap=cmap, color='tan', show_edges=True, smooth_shading=True)
            plotter.add_scalar_bar(title='Pressure Coefficient', n_labels=5, shadow=True, font_family='arial')
        if draw_streamlines:
            if not hasattr(self, 'streamlines'):
                self.calculate_streamlines()
            for streamline_num in range(len(self.streamlines)):
                plotter.add_lines((self.streamlines[streamline_num, :, :]), width=1.5, color='#50C7C7')

        plotter.show_grid(color='#444444')
        plotter.set_background(color='black')
        plotter.show(cpos=(-1, -1, 1), full_screen=False)

    def draw_legacy(self, draw_collocation_points=False, draw_panel_numbers=False, draw_vortex_strengths=False, draw_forces=False, draw_pressures=False, draw_pressures_as_vectors=False):
        fig, ax = fig3d()
        n_panels = len(self.panels)
        if draw_vortex_strengths:
            min_strength = 0
            max_strength = 0
            for panel in self.panels:
                min_strength = min(min_strength, panel.influencing_objects[0].strength)
                max_strength = max(max_strength, panel.influencing_objects[0].strength)

            print('Colorbar min: ', min_strength)
            print('Colorbar max: ', max_strength)
        else:
            if draw_pressures:
                min_delta_cp = 0
                max_delta_cp = 0
                for panel in self.panels:
                    min_delta_cp = min(min_delta_cp, panel.delta_cp)
                    max_delta_cp = max(max_delta_cp, panel.delta_cp)

                print('Colorbar min: ', min_delta_cp)
                print('Colorbar max: ', max_delta_cp)
        for panel_num in range(n_panels):
            sys.stdout.write('\r')
            sys.stdout.write('Drawing panel %i of %i' % (panel_num + 1, n_panels))
            sys.stdout.flush()
            panel = self.panels[panel_num]
            if draw_vortex_strengths:
                strength = panel.influencing_objects[0].strength
                normalized_strength = 1 * (strength - min_strength) / (max_strength - min_strength)
                colormap = mpl.cm.get_cmap('viridis')
                color = colormap(normalized_strength)
                panel.draw_legacy(show=False,
                  fig_to_plot_on=fig,
                  ax_to_plot_on=ax,
                  draw_collocation_point=draw_collocation_points,
                  shading_color=color)
            else:
                if draw_pressures:
                    delta_cp = panel.delta_cp
                    min_delta_cp = -2
                    max_delta_cp = 2
                    normalized_delta_cp = 1 * (delta_cp - min_delta_cp) / (max_delta_cp - min_delta_cp)
                    colormap = mpl.cm.get_cmap('viridis')
                    color = colormap(normalized_delta_cp)
                    panel.draw_legacy(show=False,
                      fig_to_plot_on=fig,
                      ax_to_plot_on=ax,
                      draw_collocation_point=draw_collocation_points,
                      shading_color=color)
                else:
                    panel.draw_legacy(show=False,
                      fig_to_plot_on=fig,
                      ax_to_plot_on=ax,
                      draw_collocation_point=draw_collocation_points,
                      shading_color=(0.5, 0.5, 0.5))
            if draw_forces:
                force_scale = 10
                centroid = panel.centroid()
                tail = centroid
                head = centroid + force_scale * panel.force_geometry_axes
                x = np.array([tail[0], head[0]])
                y = np.array([tail[1], head[1]])
                z = np.array([tail[2], head[2]])
                ax.plot(x, y, z, color='#0A5E08')
            elif draw_pressures_as_vectors:
                pressure_scale = 0.001
                centroid = panel.centroid()
                tail = centroid
                head = centroid + pressure_scale * panel.force_geometry_axes / panel.area()
                x = np.array([tail[0], head[0]])
                y = np.array([tail[1], head[1]])
                z = np.array([tail[2], head[2]])
                ax.plot(x, y, z, color='#0A5E08')
            if draw_panel_numbers:
                ax.text(panel.collocation_point[0], panel.collocation_point[1], panel.collocation_point[2], str(panel_num))

        x, y, z, s = self.airplane.get_bounding_cube()
        ax.set_xlim3d((x - s, x + s))
        ax.set_ylim3d((y - s, y + s))
        ax.set_zlim3d((z - s, z + s))
        plt.tight_layout()
        plt.show()


class vlm2(AeroProblem):

    def run(self, verbose=True):
        self.verbose = verbose
        print('DEPRECATION WARNING: VLM2 has been wholly eclipsed in performance and functionality by VLM3. The VLM2 source code has been left intact for validation purposes and backwards-compatibility, but it will not be supported going forward.')
        if self.verbose:
            print('Running VLM2 calculation...')
        self.make_panels()
        self.setup_geometry()
        self.setup_operating_point()
        self.calculate_vortex_strengths()
        self.calculate_forces()
        if self.verbose:
            print('VLM2 calculation complete!')

    def run_stability(self, verbose=True):
        self.verbose = verbose

    def make_panels(self):
        if self.verbose:
            print('Meshing...')
        self.mcl_coordinates_structured_list = []
        self.normals_structured_list = []
        for wing_num in range(len(self.airplane.wings)):
            wing = self.airplane.wings[wing_num]
            n_chordwise_coordinates = wing.chordwise_panels + 1
            if wing.chordwise_spacing == 'uniform':
                nondim_chordwise_coordinates = np.linspace(0, 1, n_chordwise_coordinates)
            else:
                if wing.chordwise_spacing == 'cosine':
                    nondim_chordwise_coordinates = cosspace(0, 1, n_chordwise_coordinates)
                else:
                    raise Exception('Bad value of wing.chordwise_spacing!')
            xsec_xyz_le = np.empty((0, 3))
            xsec_xyz_te = np.empty((0, 3))
            for xsec in wing.xsecs:
                xsec_xyz_le = np.vstack((xsec_xyz_le, xsec.xyz_le + wing.xyz_le))
                xsec_xyz_te = np.vstack((xsec_xyz_te, xsec.xyz_te() + wing.xyz_le))

            xsec_xyz_quarter_chords = 0.75 * xsec_xyz_le + 0.25 * xsec_xyz_te
            section_quarter_chords = xsec_xyz_quarter_chords[1:, :] - xsec_xyz_quarter_chords[:-1, :]
            section_quarter_chords_proj = section_quarter_chords[:, 1:] / np.expand_dims(np.linalg.norm((section_quarter_chords[:, 1:]), axis=1), axis=1)
            section_quarter_chords_proj = np.hstack((
             np.zeros((section_quarter_chords_proj.shape[0], 1)), section_quarter_chords_proj))
            if len(wing.xsecs) > 2:
                xsec_local_normal_inners = section_quarter_chords_proj[:-1, :] + section_quarter_chords_proj[1:, :]
                xsec_local_normal_inners = xsec_local_normal_inners / np.expand_dims(np.linalg.norm(xsec_local_normal_inners, axis=1), axis=1)
                xsec_local_normal = np.vstack((
                 section_quarter_chords_proj[0, :],
                 xsec_local_normal_inners,
                 section_quarter_chords_proj[-1, :]))
            else:
                xsec_local_normal = np.vstack((
                 section_quarter_chords_proj[0, :],
                 section_quarter_chords_proj[-1, :]))
            xsec_local_back = xsec_xyz_te - xsec_xyz_le
            xsec_chord = np.linalg.norm(xsec_local_back, axis=1)
            xsec_local_back = xsec_local_back / np.expand_dims(xsec_chord, axis=1)
            xsec_local_up = np.cross(xsec_local_back, xsec_local_normal, axis=1)
            xsec_scaling_factor = 1 / np.sqrt((1 + np.sum((section_quarter_chords_proj[1:, :] * section_quarter_chords_proj[:-1, :]),
              axis=1)) / 2)
            xsec_scaling_factor = np.hstack((1, xsec_scaling_factor, 1))
            xsec_camber = np.empty((n_chordwise_coordinates, 0))
            for xsec in wing.xsecs:
                camber = xsec.airfoil.get_camber_at_chord_fraction(nondim_chordwise_coordinates)
                camber = np.expand_dims(camber, axis=1)
                xsec_camber = np.hstack((xsec_camber, camber))

            xsec_mcl_coordinates = xsec_xyz_le + xsec_local_back * np.expand_dims(xsec_chord, axis=2) * np.expand_dims(np.expand_dims(nondim_chordwise_coordinates, 1), 2) + xsec_local_up * np.expand_dims((xsec_chord * xsec_scaling_factor), axis=2) * np.expand_dims(xsec_camber, 2)
            wing_mcl_coordinates = np.empty((n_chordwise_coordinates, 0, 3))
            for section_num in range(len(wing.xsecs) - 1):
                xsec = wing.xsecs[section_num]
                n_spanwise_coordinates = xsec.spanwise_panels + 1
                if xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                else:
                    if xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = cosspace(n_points=n_spanwise_coordinates)
                    else:
                        raise Exception('Bad value of section.spanwise_spacing!')
                is_last_section = section_num == len(wing.xsecs) - 2
                if not is_last_section:
                    nondim_spanwise_coordinates = nondim_spanwise_coordinates[:-1]
                section_mcl_coordinates = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(xsec_mcl_coordinates[:, section_num, :], 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(xsec_mcl_coordinates[:, section_num + 1, :], 1)
                wing_mcl_coordinates = np.hstack((wing_mcl_coordinates, section_mcl_coordinates))

            self.mcl_coordinates_structured_list.append(wing_mcl_coordinates)
            if wing.symmetric:
                wing_mcl_coordinates_sym = reflect_over_XZ_plane(wing_mcl_coordinates)
                wing_mcl_coordinates_sym = np.fliplr(wing_mcl_coordinates_sym)
                self.mcl_coordinates_structured_list.append(wing_mcl_coordinates_sym)
            nondim_xsec_normals = np.empty((
             wing.chordwise_panels, 0, 2))
            nondim_collocation_coordinates = 0.25 * nondim_chordwise_coordinates[:-1] + 0.75 * nondim_chordwise_coordinates[1:]
            for xsec in wing.xsecs:
                nondim_normals = xsec.airfoil.get_mcl_normal_direction_at_chord_fraction(nondim_collocation_coordinates)
                nondim_normals = np.expand_dims(nondim_normals, 1)
                nondim_xsec_normals = np.hstack((nondim_xsec_normals, nondim_normals))

            wing_normals = np.empty((wing.chordwise_panels, 0, 3))
            for section_num in range(len(wing.xsecs) - 1):
                xsec = wing.xsecs[section_num]
                n_spanwise_coordinates = xsec.spanwise_panels + 1
                if xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                else:
                    if xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = cosspace(n_points=n_spanwise_coordinates)
                    else:
                        raise Exception('Bad value of section.spanwise_spacing!')
                is_last_section = section_num == len(wing.xsecs) - 2
                nondim_spanwise_coordinates = (nondim_spanwise_coordinates[1:] + nondim_spanwise_coordinates[:-1]) / 2
                inner_xsec_back = xsec_local_back[section_num]
                outer_xsec_back = xsec_local_back[(section_num + 1)]
                section_normal = section_quarter_chords_proj[section_num]
                inner_xsec_up = np.cross(inner_xsec_back, section_normal)
                outer_xsec_up = np.cross(outer_xsec_back, section_normal)
                control_surface_hinge_point_index = np.interp(x=(xsec.control_surface_hinge_point),
                  xp=nondim_collocation_coordinates,
                  fp=(np.arange(wing.chordwise_panels)))
                deflection_angle = xsec.control_surface_deflection
                rot_matrix = angle_axis_rotation_matrix(angle=(np.radians(deflection_angle)),
                  axis=section_normal,
                  axis_already_normalized=True)
                inner_xsec_back_rotated = np.matmul(rot_matrix, inner_xsec_back)
                outer_xsec_back_rotated = np.matmul(rot_matrix, outer_xsec_back)
                inner_xsec_up_rotated = np.matmul(rot_matrix, inner_xsec_up)
                outer_xsec_up_rotated = np.matmul(rot_matrix, outer_xsec_up)
                if control_surface_hinge_point_index <= 0:
                    inner_xsec_backs = inner_xsec_back_rotated * np.ones((wing.chordwise_panels, 3))
                    outer_xsec_backs = outer_xsec_back_rotated * np.ones((wing.chordwise_panels, 3))
                    inner_xsec_ups = inner_xsec_up_rotated * np.ones((wing.chordwise_panels, 3))
                    outer_xsec_ups = outer_xsec_up_rotated * np.ones((wing.chordwise_panels, 3))
                else:
                    if control_surface_hinge_point_index >= wing.chordwise_panels:
                        inner_xsec_backs = inner_xsec_back * np.ones((wing.chordwise_panels, 3))
                        outer_xsec_backs = outer_xsec_back * np.ones((wing.chordwise_panels, 3))
                        inner_xsec_ups = inner_xsec_up * np.ones((wing.chordwise_panels, 3))
                        outer_xsec_ups = outer_xsec_up * np.ones((wing.chordwise_panels, 3))
                    else:
                        last_unmodified_index = np.int(np.floor(control_surface_hinge_point_index))
                        fraction_to_modify = 1 - (control_surface_hinge_point_index - last_unmodified_index)
                        rot_matrix = angle_axis_rotation_matrix(angle=(np.radians(xsec.control_surface_deflection * fraction_to_modify)),
                          axis=section_normal,
                          axis_already_normalized=True)
                        inner_xsec_back_semirotated = np.matmul(rot_matrix, inner_xsec_back)
                        outer_xsec_back_semirotated = np.matmul(rot_matrix, outer_xsec_back)
                        inner_xsec_up_semirotated = np.matmul(rot_matrix, inner_xsec_up)
                        outer_xsec_up_semirotated = np.matmul(rot_matrix, outer_xsec_up)
                        inner_xsec_backs = np.vstack((
                         np.tile(inner_xsec_back, reps=(last_unmodified_index, 1)),
                         inner_xsec_back_semirotated,
                         np.tile(inner_xsec_back_rotated, reps=(
                          wing.chordwise_panels - last_unmodified_index - 1, 1))))
                        inner_xsec_ups = np.vstack((
                         np.tile(inner_xsec_up, reps=(last_unmodified_index, 1)),
                         inner_xsec_up_semirotated,
                         np.tile(inner_xsec_up_rotated, reps=(
                          wing.chordwise_panels - last_unmodified_index - 1, 1))))
                        outer_xsec_backs = np.vstack((
                         np.tile(outer_xsec_back, reps=(last_unmodified_index, 1)),
                         outer_xsec_back_semirotated,
                         np.tile(outer_xsec_back_rotated, reps=(
                          wing.chordwise_panels - last_unmodified_index - 1, 1))))
                        outer_xsec_ups = np.vstack((
                         np.tile(outer_xsec_up, reps=(last_unmodified_index, 1)),
                         outer_xsec_up_semirotated,
                         np.tile(outer_xsec_up_rotated, reps=(
                          wing.chordwise_panels - last_unmodified_index - 1, 1))))
                inner_xsec_normals = np.expand_dims(nondim_xsec_normals[:, section_num, 0], 1) * inner_xsec_backs + np.expand_dims(nondim_xsec_normals[:, section_num, 1], 1) * inner_xsec_ups
                outer_xsec_normals = np.expand_dims(nondim_xsec_normals[:, section_num + 1, 0], 1) * outer_xsec_backs + np.expand_dims(nondim_xsec_normals[:, section_num + 1, 1], 1) * outer_xsec_ups
                section_normals = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_xsec_normals, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_xsec_normals, 1)
                section_normals = section_normals / np.expand_dims(np.linalg.norm(section_normals, axis=2), 2)
                wing_normals = np.hstack((wing_normals, section_normals))

            self.normals_structured_list.append(wing_normals)
            if wing.symmetric:
                if wing.has_symmetric_control_surfaces():
                    self.normals_structured_list.append(np.fliplr(reflect_over_XZ_plane(wing_normals)))
                else:
                    wing_normals = np.empty((wing.chordwise_panels, 0, 3))
                    for section_num in range(len(wing.xsecs) - 1):
                        xsec = wing.xsecs[section_num]
                        n_spanwise_coordinates = xsec.spanwise_panels + 1
                        if xsec.spanwise_spacing == 'uniform':
                            nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                        else:
                            if xsec.spanwise_spacing == 'cosine':
                                nondim_spanwise_coordinates = cosspace(n_points=n_spanwise_coordinates)
                            else:
                                raise Exception('Bad value of section.spanwise_spacing!')
                        is_last_section = section_num == len(wing.xsecs) - 2
                        nondim_spanwise_coordinates = (nondim_spanwise_coordinates[1:] + nondim_spanwise_coordinates[:-1]) / 2
                        inner_xsec_back = xsec_local_back[section_num]
                        outer_xsec_back = xsec_local_back[(section_num + 1)]
                        section_normal = section_quarter_chords_proj[section_num]
                        inner_xsec_up = np.cross(inner_xsec_back, section_normal)
                        outer_xsec_up = np.cross(outer_xsec_back, section_normal)
                        control_surface_hinge_point_index = np.interp(x=(xsec.control_surface_hinge_point),
                          xp=nondim_collocation_coordinates,
                          fp=(np.arange(wing.chordwise_panels)))
                        deflection_angle = xsec.control_surface_deflection
                        if xsec.control_surface_type == 'asymmetric':
                            deflection_angle = -deflection_angle
                        else:
                            rot_matrix = angle_axis_rotation_matrix(angle=(np.radians(deflection_angle)),
                              axis=section_normal,
                              axis_already_normalized=True)
                            inner_xsec_back_rotated = np.matmul(rot_matrix, inner_xsec_back)
                            outer_xsec_back_rotated = np.matmul(rot_matrix, outer_xsec_back)
                            inner_xsec_up_rotated = np.matmul(rot_matrix, inner_xsec_up)
                            outer_xsec_up_rotated = np.matmul(rot_matrix, outer_xsec_up)
                            if control_surface_hinge_point_index <= 0:
                                inner_xsec_backs = inner_xsec_back_rotated * np.ones((wing.chordwise_panels, 3))
                                outer_xsec_backs = outer_xsec_back_rotated * np.ones((wing.chordwise_panels, 3))
                                inner_xsec_ups = inner_xsec_up_rotated * np.ones((wing.chordwise_panels, 3))
                                outer_xsec_ups = outer_xsec_up_rotated * np.ones((wing.chordwise_panels, 3))
                            else:
                                if control_surface_hinge_point_index >= wing.chordwise_panels:
                                    inner_xsec_backs = inner_xsec_back * np.ones((wing.chordwise_panels, 3))
                                    outer_xsec_backs = outer_xsec_back * np.ones((wing.chordwise_panels, 3))
                                    inner_xsec_ups = inner_xsec_up * np.ones((wing.chordwise_panels, 3))
                                    outer_xsec_ups = outer_xsec_up * np.ones((wing.chordwise_panels, 3))
                                else:
                                    last_unmodified_index = np.int(np.floor(control_surface_hinge_point_index))
                                    fraction_to_modify = 1 - (control_surface_hinge_point_index - last_unmodified_index)
                                    rot_matrix = angle_axis_rotation_matrix(angle=(np.radians(xsec.control_surface_deflection * fraction_to_modify)),
                                      axis=section_normal,
                                      axis_already_normalized=True)
                                    inner_xsec_back_semirotated = np.matmul(rot_matrix, inner_xsec_back)
                                    outer_xsec_back_semirotated = np.matmul(rot_matrix, outer_xsec_back)
                                    inner_xsec_up_semirotated = np.matmul(rot_matrix, inner_xsec_up)
                                    outer_xsec_up_semirotated = np.matmul(rot_matrix, outer_xsec_up)
                                    inner_xsec_backs = np.vstack((
                                     np.tile(inner_xsec_back, reps=(last_unmodified_index, 1)),
                                     inner_xsec_back_semirotated,
                                     np.tile(inner_xsec_back_rotated, reps=(
                                      wing.chordwise_panels - last_unmodified_index - 1, 1))))
                                    inner_xsec_ups = np.vstack((
                                     np.tile(inner_xsec_up, reps=(last_unmodified_index, 1)),
                                     inner_xsec_up_semirotated,
                                     np.tile(inner_xsec_up_rotated, reps=(
                                      wing.chordwise_panels - last_unmodified_index - 1, 1))))
                                    outer_xsec_backs = np.vstack((
                                     np.tile(outer_xsec_back, reps=(last_unmodified_index, 1)),
                                     outer_xsec_back_semirotated,
                                     np.tile(outer_xsec_back_rotated, reps=(
                                      wing.chordwise_panels - last_unmodified_index - 1, 1))))
                                    outer_xsec_ups = np.vstack((
                                     np.tile(outer_xsec_up, reps=(last_unmodified_index, 1)),
                                     outer_xsec_up_semirotated,
                                     np.tile(outer_xsec_up_rotated, reps=(
                                      wing.chordwise_panels - last_unmodified_index - 1, 1))))
                        inner_xsec_normals = np.expand_dims(nondim_xsec_normals[:, section_num, 0], 1) * inner_xsec_backs + np.expand_dims(nondim_xsec_normals[:, section_num, 1], 1) * inner_xsec_ups
                        outer_xsec_normals = np.expand_dims(nondim_xsec_normals[:, section_num + 1, 0], 1) * outer_xsec_backs + np.expand_dims(nondim_xsec_normals[:, section_num + 1, 1], 1) * outer_xsec_ups
                        section_normals = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_xsec_normals, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_xsec_normals, 1)
                        section_normals = section_normals / np.expand_dims(np.linalg.norm(section_normals, axis=2), 2)
                        wing_normals = np.hstack((wing_normals, section_normals))

                    self.normals_structured_list.append(np.flip((reflect_over_XZ_plane(wing_normals)), axis=1))

        if self.verbose:
            print('Meshing complete!')
        self.n_wings = len(self.mcl_coordinates_structured_list)
        self.front_left_vertices_list = []
        self.front_right_vertices_list = []
        self.back_left_vertices_list = []
        self.back_right_vertices_list = []
        self.vortex_left_list = []
        self.vortex_right_list = []
        self.collocations_list = []
        self.normals_list = []
        for wing_num in range(self.n_wings):
            wing_front_left_vertices = self.mcl_coordinates_structured_list[wing_num][:-1, :-1, :]
            wing_front_right_vertices = self.mcl_coordinates_structured_list[wing_num][:-1, 1:, :]
            wing_back_left_vertices = self.mcl_coordinates_structured_list[wing_num][1:, :-1, :]
            wing_back_right_vertices = self.mcl_coordinates_structured_list[wing_num][1:, 1:, :]
            self.front_left_vertices_list.append(np.reshape(wing_front_left_vertices, (-1,
                                                                                       3)))
            self.front_right_vertices_list.append(np.reshape(wing_front_right_vertices, (-1,
                                                                                         3)))
            self.back_left_vertices_list.append(np.reshape(wing_back_left_vertices, (-1,
                                                                                     3)))
            self.back_right_vertices_list.append(np.reshape(wing_back_right_vertices, (-1,
                                                                                       3)))
            self.collocations_list.append(np.reshape(0.5 * (0.25 * wing_front_left_vertices + 0.75 * wing_back_left_vertices) + 0.5 * (0.25 * wing_front_right_vertices + 0.75 * wing_back_right_vertices), (-1,
                                                                                                                                                                                                             3)))
            self.vortex_left_list.append(np.reshape(0.75 * wing_front_left_vertices + 0.25 * wing_back_left_vertices, (-1,
                                                                                                                       3)))
            self.vortex_right_list.append(np.reshape(0.75 * wing_front_right_vertices + 0.25 * wing_back_right_vertices, (-1,
                                                                                                                          3)))
            self.normals_list.append(np.reshape(self.normals_structured_list[wing_num], (-1,
                                                                                         3)))

        self.front_left_vertices_unrolled = np.vstack(self.front_left_vertices_list)
        self.front_right_vertices_unrolled = np.vstack(self.front_right_vertices_list)
        self.back_left_vertices_unrolled = np.vstack(self.back_left_vertices_list)
        self.back_right_vertices_unrolled = np.vstack(self.back_right_vertices_list)
        self.collocations_unrolled = np.vstack(self.collocations_list)
        self.vortex_left_unrolled = np.vstack(self.vortex_left_list)
        self.vortex_right_unrolled = np.vstack(self.vortex_right_list)
        self.vortex_centers_unrolled = (self.vortex_left_unrolled + self.vortex_right_unrolled) / 2
        self.normals_unrolled = np.vstack(self.normals_list)
        self.n_panels = len(self.normals_unrolled)

    def setup_geometry(self):
        if self.verbose:
            print('Calculating the collocation influence matrix...')
        self.Vij_collocations = self.calculate_Vij(self.collocations_unrolled)
        normals_expanded = np.expand_dims(self.normals_unrolled, 1)
        self.AIC = np.sum((self.Vij_collocations * normals_expanded),
          axis=2)
        if self.verbose:
            print('Calculating the vortex center influence matrix...')
        self.Vij_centers = self.calculate_Vij(self.vortex_centers_unrolled)

    def setup_operating_point(self):
        if self.verbose:
            print('Calculating the freestream influence...')
        self.steady_freestream_velocity = self.op_point.compute_freestream_velocity_geometry_axes() * np.ones((
         self.n_panels, 1))
        self.rotation_freestream_velocities = self.op_point.compute_rotation_velocity_geometry_axes(self.collocations_unrolled)
        self.freestream_velocities = self.steady_freestream_velocity + self.rotation_freestream_velocities
        self.freestream_influences = np.sum((self.freestream_velocities * self.normals_unrolled), axis=1)

    def calculate_vortex_strengths(self):
        if self.verbose:
            print('Calculating vortex strengths...')
        self.vortex_strengths = np.linalg.solve(self.AIC, -self.freestream_influences)

    def calculate_forces(self):
        if self.verbose:
            print('Calculating forces on each panel...')
        else:
            Vi_x = self.Vij_centers[:, :, 0] @ self.vortex_strengths + self.freestream_velocities[:, 0]
            Vi_y = self.Vij_centers[:, :, 1] @ self.vortex_strengths + self.freestream_velocities[:, 1]
            Vi_z = self.Vij_centers[:, :, 2] @ self.vortex_strengths + self.freestream_velocities[:, 2]
            Vi_x = np.expand_dims(Vi_x, axis=1)
            Vi_y = np.expand_dims(Vi_y, axis=1)
            Vi_z = np.expand_dims(Vi_z, axis=1)
            Vi = np.hstack((Vi_x, Vi_y, Vi_z))
            li_pieces = []
            for wing_num in range(self.n_wings):
                wing_mcl_coordinates = self.mcl_coordinates_structured_list[wing_num]
                wing_vortex_points = 0.75 * wing_mcl_coordinates[:-1, :, :] + 0.25 * wing_mcl_coordinates[1:, :, :]
                li_piece = wing_vortex_points[:, 1:, :] - wing_vortex_points[:, :-1, :]
                li_piece = np.reshape(li_piece, (-1, 3))
                li_pieces.append(li_piece)

            self.li = np.vstack(li_pieces)
            density = self.op_point.density
            Vi_cross_li = np.cross(Vi, (self.li), axis=1)
            vortex_strengths_expanded = np.expand_dims((self.vortex_strengths), axis=1)
            self.Fi_geometry = density * Vi_cross_li * vortex_strengths_expanded
            if self.verbose:
                print('Calculating total forces and moments...')
            self.Ftotal_geometry = np.sum((self.Fi_geometry), axis=0)
            self.Ftotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Ftotal_geometry
            self.Mtotal_geometry = np.sum((np.cross(self.vortex_centers_unrolled - self.airplane.xyz_ref, self.Fi_geometry)), axis=0)
            self.Mtotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Mtotal_geometry
            q = self.op_point.dynamic_pressure()
            s_ref = self.airplane.s_ref
            b_ref = self.airplane.b_ref
            c_ref = self.airplane.c_ref
            self.CL = -self.Ftotal_wind[2] / q / s_ref
            self.CDi = -self.Ftotal_wind[0] / q / s_ref
            self.CY = self.Ftotal_wind[1] / q / s_ref
            self.Cl = self.Mtotal_wind[0] / q / b_ref
            self.Cm = self.Mtotal_wind[1] / q / c_ref
            self.Cn = self.Mtotal_wind[2] / q / b_ref
            if self.CDi == 0:
                self.CL_over_CDi = 0
            else:
                self.CL_over_CDi = self.CL / self.CDi
        if self.verbose:
            print('\nForces\n-----')
        if self.verbose:
            print('CL: ', self.CL)
        if self.verbose:
            print('CDi: ', self.CDi)
        if self.verbose:
            print('CY: ', self.CY)
        if self.verbose:
            print('CL/CDi: ', self.CL_over_CDi)
        if self.verbose:
            print('\nMoments\n-----')
        if self.verbose:
            print('Cl: ', self.Cl)
        if self.verbose:
            print('Cm: ', self.Cm)
        if self.verbose:
            print('Cn: ', self.Cn)

    def calculate_Vij_wing_by_wing(self, points):
        points = np.reshape(points, (-1, 3))
        n_points = len(points)
        Vij_pieces = []
        for wing_num in range(self.n_wings):
            wing_mcl_coordinates = self.mcl_coordinates_structured_list[wing_num]
            wing_vortex_points = 0.75 * wing_mcl_coordinates[:-1, :, :] + 0.25 * wing_mcl_coordinates[1:, :, :]
            wing_ab = np.expand_dims(np.expand_dims(points, 1), 2) - wing_vortex_points
            wing_ab_shape = wing_ab.shape
            wing_ab_cross_x = np.stack((
             np.zeros((n_points, wing_ab_shape[1], wing_ab_shape[2])),
             wing_ab[:, :, :, 2],
             -wing_ab[:, :, :, 1]),
              axis=3)
            wing_ab_dot_x = wing_ab[:, :, :, 0]
            wing_a_cross_b = np.cross((wing_ab[:, :, :-1, :]),
              (wing_ab[:, :, 1:, :]),
              axis=3)
            wing_a_dot_b = np.einsum('ijkl,ijkl->ijk', wing_ab[:, :, :-1, :], wing_ab[:, :, 1:, :])
            wing_ab_norm = np.linalg.norm(wing_ab, axis=3)
            wing_ab_norm_inv = 1 / wing_ab_norm
            bound_vortex_singularity_indices = np.einsum('ijkl,ijkl->ijk', wing_a_cross_b, wing_a_cross_b) < 3e-16
            wing_a_dot_b = wing_a_dot_b + bound_vortex_singularity_indices
            side_vortex_singularity_indices = np.einsum('ijkl,ijkl->ijk', wing_ab_cross_x, wing_ab_cross_x) < 3e-16
            wing_ab_dot_x = wing_ab_dot_x + side_vortex_singularity_indices
            wing_a_cross_x = wing_ab_cross_x[:, :, :-1, :]
            wing_b_cross_x = wing_ab_cross_x[:, :, 1:, :]
            wing_a_dot_x = wing_ab_dot_x[:, :, :-1]
            wing_b_dot_x = wing_ab_dot_x[:, :, 1:]
            wing_a_norm = wing_ab_norm[:, :, :-1]
            wing_b_norm = wing_ab_norm[:, :, 1:]
            wing_a_norm_inv = wing_ab_norm_inv[:, :, :-1]
            wing_b_norm_inv = wing_ab_norm_inv[:, :, 1:]
            wing_a_cross_b = np.reshape(wing_a_cross_b, (n_points, -1, 3))
            wing_a_cross_x = np.reshape(wing_a_cross_x, (n_points, -1, 3))
            wing_b_cross_x = np.reshape(wing_b_cross_x, (n_points, -1, 3))
            wing_a_dot_b = np.reshape(wing_a_dot_b, (n_points, -1))
            wing_a_dot_x = np.reshape(wing_a_dot_x, (n_points, -1))
            wing_b_dot_x = np.reshape(wing_b_dot_x, (n_points, -1))
            wing_a_norm = np.reshape(wing_a_norm, (n_points, -1))
            wing_b_norm = np.reshape(wing_b_norm, (n_points, -1))
            wing_a_norm_inv = np.reshape(wing_a_norm_inv, (n_points, -1))
            wing_b_norm_inv = np.reshape(wing_b_norm_inv, (n_points, -1))
            term1 = (wing_a_norm_inv + wing_b_norm_inv) / (wing_a_norm * wing_b_norm + wing_a_dot_b)
            term2 = wing_a_norm_inv / (wing_a_norm - wing_a_dot_x)
            term3 = wing_b_norm_inv / (wing_b_norm - wing_b_dot_x)
            term1 = np.expand_dims(term1, 2)
            term2 = np.expand_dims(term2, 2)
            term3 = np.expand_dims(term3, 2)
            Vij_piece = 1 / (4 * np.pi) * (wing_a_cross_b * term1 + wing_a_cross_x * term2 - wing_b_cross_x * term3)
            Vij_pieces.append(Vij_piece)

        Vij = np.hstack(Vij_pieces)
        return Vij

    def calculate_Vij(self, points):
        left_vortex_points = self.vortex_left_unrolled
        right_vortex_points = self.vortex_right_unrolled
        points = np.reshape(points, (-1, 3))
        n_points = len(points)
        n_vortices = self.n_panels
        points = np.expand_dims(points, 1)
        a = points - left_vortex_points
        b = points - right_vortex_points
        a_cross_b = np.cross(a, b, axis=2)
        a_dot_b = np.einsum('ijk,ijk->ij', a, b)
        a_cross_x = np.stack((
         np.zeros((n_points, n_vortices)),
         a[:, :, 2],
         -a[:, :, 1]),
          axis=2)
        a_dot_x = a[:, :, 0]
        b_cross_x = np.stack((
         np.zeros((n_points, n_vortices)),
         b[:, :, 2],
         -b[:, :, 1]),
          axis=2)
        b_dot_x = b[:, :, 0]
        norm_a = np.linalg.norm(a, axis=2)
        norm_b = np.linalg.norm(b, axis=2)
        norm_a_inv = 1 / norm_a
        norm_b_inv = 1 / norm_b
        bound_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_b, a_cross_b) < 3e-16
        a_dot_b = a_dot_b + bound_vortex_singularity_indices
        left_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_x, a_cross_x) < 3e-16
        a_dot_x = a_dot_x + left_vortex_singularity_indices
        right_vortex_singularity_indices = np.einsum('ijk,ijk->ij', b_cross_x, b_cross_x) < 3e-16
        b_dot_x = b_dot_x + right_vortex_singularity_indices
        term1 = (norm_a_inv + norm_b_inv) / (norm_a * norm_b + a_dot_b)
        term2 = norm_a_inv / (norm_a - a_dot_x)
        term3 = norm_b_inv / (norm_b - b_dot_x)
        term1 = np.expand_dims(term1, 2)
        term2 = np.expand_dims(term2, 2)
        term3 = np.expand_dims(term3, 2)
        Vij = 1 / (4 * np.pi) * (a_cross_b * term1 + a_cross_x * term2 - b_cross_x * term3)
        return Vij

    def calculate_delta_cp(self):
        diag1 = self.front_left_vertices_unrolled - self.back_right_vertices_unrolled
        diag2 = self.front_right_vertices_unrolled - self.back_left_vertices_unrolled
        self.areas = np.linalg.norm(np.cross(diag1, diag2, axis=1), axis=1) / 2
        self.Fi_normal = np.einsum('ij,ij->i', self.Fi_geometry, self.normals_unrolled)
        self.pressure_normal = self.Fi_normal / self.areas
        self.delta_cp = self.pressure_normal / self.op_point.dynamic_pressure()

    def get_induced_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vij = self.calculate_Vij(point)
        vortex_strengths_expanded = np.expand_dims(self.vortex_strengths, 1)
        Vi_x = Vij[:, :, 0] @ vortex_strengths_expanded
        Vi_y = Vij[:, :, 1] @ vortex_strengths_expanded
        Vi_z = Vij[:, :, 2] @ vortex_strengths_expanded
        Vi = np.hstack((Vi_x, Vi_y, Vi_z))
        return Vi

    def get_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vi = self.get_induced_velocity_at_point(point)
        freestream = self.op_point.compute_freestream_velocity_geometry_axes()
        V = Vi + freestream
        return V

    def calculate_streamlines(self):
        n_steps = 100
        length = 1
        length_per_step = length / n_steps
        seed_points_list = []
        for wing_num in range(self.n_wings):
            wing_mcl_coordinates = self.mcl_coordinates_structured_list[wing_num]
            wing_te_coordinates = wing_mcl_coordinates[-1, :, :]
            wing_seed_points = (wing_te_coordinates[:-1, :] + wing_te_coordinates[1:, :]) / 2
            seed_points_list.append(wing_seed_points)

        seed_points = np.vstack(seed_points_list)
        n_streamlines = len(seed_points)
        streamlines = np.zeros((n_streamlines, n_steps, 3))
        streamlines[:, 0, :] = seed_points
        for step_num in range(1, n_steps):
            update_amount = self.get_velocity_at_point(streamlines[:, step_num - 1, :])
            update_amount = update_amount * length_per_step / np.expand_dims(np.linalg.norm(update_amount, axis=1), axis=1)
            streamlines[:, step_num, :] = streamlines[:, step_num - 1, :] + update_amount

        self.streamlines = streamlines

    def draw(self, draw_delta_cp=True, draw_streamlines=True):
        print('Drawing...')
        vertices = np.vstack((
         self.front_left_vertices_unrolled,
         self.front_right_vertices_unrolled,
         self.back_right_vertices_unrolled,
         self.back_left_vertices_unrolled))
        faces = np.transpose(np.vstack((
         4 * np.ones(self.n_panels),
         np.arange(self.n_panels),
         np.arange(self.n_panels) + self.n_panels,
         np.arange(self.n_panels) + 2 * self.n_panels,
         np.arange(self.n_panels) + 3 * self.n_panels)))
        faces = np.reshape(faces, (-1), order='C')
        wing_surfaces = pv.PolyData(vertices, faces)
        plotter = pv.Plotter()
        if draw_delta_cp:
            if not hasattr(self, 'delta_cp'):
                self.calculate_delta_cp()
            delta_cp_min = -1.5
            delta_cp_max = 1.5
            scalars = np.minimum(np.maximum(self.delta_cp, delta_cp_min), delta_cp_max)
            cmap = plt.cm.get_cmap('viridis')
            plotter.add_mesh(wing_surfaces, scalars=scalars, cmap=cmap, color='tan', show_edges=True, smooth_shading=True)
            plotter.add_scalar_bar(title='Pressure Coefficient Differential', n_labels=5, shadow=True, font_family='arial')
        if draw_streamlines:
            if not hasattr(self, 'streamlines'):
                self.calculate_streamlines()
            for streamline_num in range(len(self.streamlines)):
                plotter.add_lines((self.streamlines[streamline_num, :, :]), width=1, color='#50C7C7')

        plotter.show_grid(color='#444444')
        plotter.set_background(color='black')
        plotter.show(cpos=(-1, -1, 1), full_screen=False)


class vlm3(AeroProblem):

    def run(self, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print('Running VLM3 calculation...')
        self.make_panels()
        self.setup_geometry()
        self.setup_operating_point()
        self.calculate_vortex_strengths()
        self.calculate_forces()
        if self.verbose:
            print('VLM3 calculation complete!')

    def run_stability(self, verbose=True):
        self.verbose = verbose

    def make_panels(self):
        if self.verbose:
            print('Meshing...')
        collocation_points = np.empty((0, 3))
        normal_directions = np.empty((0, 3))
        left_vortex_vertices = np.empty((0, 3))
        right_vortex_vertices = np.empty((0, 3))
        front_left_vertices = np.empty((0, 3))
        front_right_vertices = np.empty((0, 3))
        back_left_vertices = np.empty((0, 3))
        back_right_vertices = np.empty((0, 3))
        areas = np.empty(0)
        is_trailing_edge = np.empty(0, dtype=bool)
        for wing_num in range(len(self.airplane.wings)):
            wing = self.airplane.wings[wing_num]
            n_chordwise_coordinates = wing.chordwise_panels + 1
            if wing.chordwise_spacing == 'uniform':
                nondim_chordwise_coordinates = np.linspace(0, 1, n_chordwise_coordinates)
            else:
                if wing.chordwise_spacing == 'cosine':
                    nondim_chordwise_coordinates = cosspace(0, 1, n_chordwise_coordinates)
                else:
                    raise Exception('Bad value of wing.chordwise_spacing!')
            xsec_xyz_le = np.empty((0, 3))
            xsec_xyz_te = np.empty((0, 3))
            for xsec in wing.xsecs:
                xsec_xyz_le = np.vstack((xsec_xyz_le, xsec.xyz_le + wing.xyz_le))
                xsec_xyz_te = np.vstack((xsec_xyz_te, xsec.xyz_te() + wing.xyz_le))

            xsec_xyz_quarter_chords = 0.75 * xsec_xyz_le + 0.25 * xsec_xyz_te
            section_quarter_chords = xsec_xyz_quarter_chords[1:, :] - xsec_xyz_quarter_chords[:-1, :]
            section_quarter_chords_proj = section_quarter_chords[:, 1:] / np.expand_dims(np.linalg.norm((section_quarter_chords[:, 1:]), axis=1), axis=1)
            section_quarter_chords_proj = np.hstack((
             np.zeros((section_quarter_chords_proj.shape[0], 1)), section_quarter_chords_proj))
            if len(wing.xsecs) > 2:
                xsec_local_normal_inners = section_quarter_chords_proj[:-1, :] + section_quarter_chords_proj[1:, :]
                xsec_local_normal_inners = xsec_local_normal_inners / np.expand_dims(np.linalg.norm(xsec_local_normal_inners, axis=1), axis=1)
                xsec_local_normal = np.vstack((
                 section_quarter_chords_proj[0, :],
                 xsec_local_normal_inners,
                 section_quarter_chords_proj[-1, :]))
            else:
                xsec_local_normal = np.vstack((
                 section_quarter_chords_proj[0, :],
                 section_quarter_chords_proj[-1, :]))
            xsec_local_back = xsec_xyz_te - xsec_xyz_le
            xsec_chord = np.linalg.norm(xsec_local_back, axis=1)
            xsec_local_back = xsec_local_back / np.expand_dims(xsec_chord, axis=1)
            xsec_local_up = np.cross(xsec_local_back, xsec_local_normal, axis=1)
            xsec_scaling_factor = 1 / np.sqrt((1 + np.sum((section_quarter_chords_proj[1:, :] * section_quarter_chords_proj[:-1, :]),
              axis=1)) / 2)
            xsec_scaling_factor = np.hstack((1, xsec_scaling_factor, 1))
            for section_num in range(len(wing.xsecs) - 1):
                inner_xsec = wing.xsecs[section_num]
                outer_xsec = wing.xsecs[(section_num + 1)]
                inner_airfoil = inner_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point=(inner_xsec.control_surface_hinge_point))
                outer_airfoil = outer_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point=(inner_xsec.control_surface_hinge_point))
                inner_xsec_mcl_nondim = inner_airfoil.get_downsampled_mcl(nondim_chordwise_coordinates)
                outer_xsec_mcl_nondim = outer_airfoil.get_downsampled_mcl(nondim_chordwise_coordinates)
                inner_xsec_mcl = xsec_xyz_le[section_num, :] + (xsec_local_back[section_num, :] * np.expand_dims(inner_xsec_mcl_nondim[:, 0], 1) * xsec_chord[section_num] + xsec_local_up[section_num, :] * np.expand_dims(inner_xsec_mcl_nondim[:, 1], 1) * xsec_chord[section_num] * xsec_scaling_factor[section_num])
                outer_xsec_mcl = xsec_xyz_le[section_num + 1, :] + (xsec_local_back[section_num + 1, :] * np.expand_dims(outer_xsec_mcl_nondim[:, 0], 1) * xsec_chord[(section_num + 1)] + xsec_local_up[section_num + 1, :] * np.expand_dims(outer_xsec_mcl_nondim[:, 1], 1) * xsec_chord[(section_num + 1)] * xsec_scaling_factor[(section_num + 1)])
                n_spanwise_coordinates = xsec.spanwise_panels + 1
                if xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                else:
                    if xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = cosspace(n_points=n_spanwise_coordinates)
                    else:
                        raise Exception('Bad value of section.spanwise_spacing!')
                section_mcl_coordinates = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_xsec_mcl, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_xsec_mcl, 1)
                front_inner_coordinates = section_mcl_coordinates[:-1, :-1, :]
                front_outer_coordinates = section_mcl_coordinates[:-1, 1:, :]
                back_inner_coordinates = section_mcl_coordinates[1:, :-1, :]
                back_outer_coordinates = section_mcl_coordinates[1:, 1:, :]
                section_is_trailing_edge = np.vstack((
                 np.zeros((wing.chordwise_panels - 1, xsec.spanwise_panels), dtype=bool),
                 np.ones((1, xsec.spanwise_panels), dtype=bool)))
                front_inner_coordinates = np.reshape(front_inner_coordinates, (-1,
                                                                               3), order='F')
                front_outer_coordinates = np.reshape(front_outer_coordinates, (-1,
                                                                               3), order='F')
                back_inner_coordinates = np.reshape(back_inner_coordinates, (-1, 3), order='F')
                back_outer_coordinates = np.reshape(back_outer_coordinates, (-1, 3), order='F')
                section_is_trailing_edge = np.reshape(section_is_trailing_edge, (-1), order='F')
                diag1 = front_outer_coordinates - back_inner_coordinates
                diag2 = front_inner_coordinates - back_outer_coordinates
                diag_cross = np.cross(diag1, diag2, axis=1)
                diag_cross_norm = np.linalg.norm(diag_cross, axis=1)
                normals_to_add = diag_cross / np.expand_dims(diag_cross_norm, axis=1)
                areas_to_add = diag_cross_norm / 2
                collocations_to_add = 0.5 * (0.25 * front_inner_coordinates + 0.75 * back_inner_coordinates) + 0.5 * (0.25 * front_outer_coordinates + 0.75 * back_outer_coordinates)
                inner_vortex_vertices_to_add = 0.75 * front_inner_coordinates + 0.25 * back_inner_coordinates
                outer_vortex_vertices_to_add = 0.75 * front_outer_coordinates + 0.25 * back_outer_coordinates
                front_left_vertices = np.vstack((
                 front_left_vertices,
                 front_inner_coordinates))
                front_right_vertices = np.vstack((
                 front_right_vertices,
                 front_outer_coordinates))
                back_left_vertices = np.vstack((
                 back_left_vertices,
                 back_inner_coordinates))
                back_right_vertices = np.vstack((
                 back_right_vertices,
                 back_outer_coordinates))
                areas = np.hstack((
                 areas,
                 areas_to_add))
                is_trailing_edge = np.hstack((
                 is_trailing_edge,
                 section_is_trailing_edge))
                collocation_points = np.vstack((
                 collocation_points,
                 collocations_to_add))
                normal_directions = np.vstack((
                 normal_directions,
                 normals_to_add))
                left_vortex_vertices = np.vstack((
                 left_vortex_vertices,
                 inner_vortex_vertices_to_add))
                right_vortex_vertices = np.vstack((
                 right_vortex_vertices,
                 outer_vortex_vertices_to_add))
                if wing.symmetric:
                    if inner_xsec.control_surface_type == 'asymmetric':
                        inner_airfoil = inner_xsec.airfoil.add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point=(inner_xsec.control_surface_hinge_point))
                        outer_airfoil = outer_xsec.airfoil.add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point=(inner_xsec.control_surface_hinge_point))
                        inner_xsec_mcl_nondim = inner_airfoil.get_downsampled_mcl(nondim_chordwise_coordinates)
                        outer_xsec_mcl_nondim = outer_airfoil.get_downsampled_mcl(nondim_chordwise_coordinates)
                        inner_xsec_mcl = xsec_xyz_le[section_num, :] + (xsec_local_back[section_num, :] * np.expand_dims(inner_xsec_mcl_nondim[:, 0], 1) * xsec_chord[section_num] + xsec_local_up[section_num, :] * np.expand_dims(inner_xsec_mcl_nondim[:, 1], 1) * xsec_chord[section_num] * xsec_scaling_factor[section_num])
                        outer_xsec_mcl = xsec_xyz_le[section_num + 1, :] + (xsec_local_back[section_num + 1, :] * np.expand_dims(outer_xsec_mcl_nondim[:, 0], 1) * xsec_chord[(section_num + 1)] + xsec_local_up[section_num + 1, :] * np.expand_dims(outer_xsec_mcl_nondim[:, 1], 1) * xsec_chord[(section_num + 1)] * xsec_scaling_factor[(section_num + 1)])
                        section_mcl_coordinates = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_xsec_mcl, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_xsec_mcl, 1)
                        front_inner_coordinates = section_mcl_coordinates[:-1, :-1, :]
                        front_outer_coordinates = section_mcl_coordinates[:-1, 1:, :]
                        back_inner_coordinates = section_mcl_coordinates[1:, :-1, :]
                        back_outer_coordinates = section_mcl_coordinates[1:, 1:, :]
                        front_inner_coordinates = np.reshape(front_inner_coordinates, (-1,
                                                                                       3), order='F')
                        front_outer_coordinates = np.reshape(front_outer_coordinates, (-1,
                                                                                       3), order='F')
                        back_inner_coordinates = np.reshape(back_inner_coordinates, (-1,
                                                                                     3), order='F')
                        back_outer_coordinates = np.reshape(back_outer_coordinates, (-1,
                                                                                     3), order='F')
                        diag1 = front_outer_coordinates - back_inner_coordinates
                        diag2 = front_inner_coordinates - back_outer_coordinates
                        diag_cross = np.cross(diag1, diag2, axis=1)
                        diag_cross_norm = np.linalg.norm(diag_cross, axis=1)
                        normals_to_add = diag_cross / np.expand_dims(diag_cross_norm, axis=1)
                        areas_to_add = diag_cross_norm / 2
                        collocations_to_add = 0.5 * (0.25 * front_inner_coordinates + 0.75 * back_inner_coordinates) + 0.5 * (0.25 * front_outer_coordinates + 0.75 * back_outer_coordinates)
                        inner_vortex_vertices_to_add = 0.75 * front_inner_coordinates + 0.25 * back_inner_coordinates
                        outer_vortex_vertices_to_add = 0.75 * front_outer_coordinates + 0.25 * back_outer_coordinates
                    front_left_vertices = np.vstack((
                     front_left_vertices,
                     reflect_over_XZ_plane(front_outer_coordinates)))
                    front_right_vertices = np.vstack((
                     front_right_vertices,
                     reflect_over_XZ_plane(front_inner_coordinates)))
                    back_left_vertices = np.vstack((
                     back_left_vertices,
                     reflect_over_XZ_plane(back_outer_coordinates)))
                    back_right_vertices = np.vstack((
                     back_right_vertices,
                     reflect_over_XZ_plane(back_inner_coordinates)))
                    areas = np.hstack((
                     areas,
                     areas_to_add))
                    is_trailing_edge = np.hstack((
                     is_trailing_edge,
                     section_is_trailing_edge))
                    collocation_points = np.vstack((
                     collocation_points,
                     reflect_over_XZ_plane(collocations_to_add)))
                    normal_directions = np.vstack((
                     normal_directions,
                     reflect_over_XZ_plane(normals_to_add)))
                    left_vortex_vertices = np.vstack((
                     left_vortex_vertices,
                     reflect_over_XZ_plane(outer_vortex_vertices_to_add)))
                    right_vortex_vertices = np.vstack((
                     right_vortex_vertices,
                     reflect_over_XZ_plane(inner_vortex_vertices_to_add)))

        self.front_left_vertices = front_left_vertices
        self.front_right_vertices = front_right_vertices
        self.back_left_vertices = back_left_vertices
        self.back_right_vertices = back_right_vertices
        self.areas = areas
        self.is_trailing_edge = is_trailing_edge
        self.collocation_points = collocation_points
        self.normal_directions = normal_directions
        self.left_vortex_vertices = left_vortex_vertices
        self.right_vortex_vertices = right_vortex_vertices
        self.vortex_centers = (self.left_vortex_vertices + self.right_vortex_vertices) / 2
        self.vortex_bound_leg = self.right_vortex_vertices - self.left_vortex_vertices
        self.n_panels = len(self.collocation_points)
        if self.verbose:
            print('Meshing complete!')

    def setup_geometry(self):
        if self.verbose:
            print('Calculating the collocation influence matrix...')
        self.Vij_collocations = self.calculate_Vij(self.collocation_points)
        self.AIC = np.sum((self.Vij_collocations * np.expand_dims(self.normal_directions, 1)),
          axis=2)
        if self.verbose:
            print('Calculating the vortex center influence matrix...')
        self.Vij_centers = self.calculate_Vij(self.vortex_centers)

    def setup_operating_point(self):
        if self.verbose:
            print('Calculating the freestream influence...')
        self.steady_freestream_velocity = np.expand_dims(self.op_point.compute_freestream_velocity_geometry_axes(), 0)
        self.rotation_freestream_velocities = self.op_point.compute_rotation_velocity_geometry_axes(self.collocation_points)
        self.freestream_velocities = self.steady_freestream_velocity + self.rotation_freestream_velocities
        self.freestream_influences = np.sum((self.freestream_velocities * self.normal_directions), axis=1)

    def calculate_vortex_strengths(self):
        if self.verbose:
            print('Calculating vortex strengths...')
        self.vortex_strengths = np.linalg.solve(self.AIC, -self.freestream_influences)

    def calculate_forces(self):
        if self.verbose:
            print('Calculating forces on each panel...')
        else:
            Vi_x = self.Vij_centers[:, :, 0] @ self.vortex_strengths + self.freestream_velocities[:, 0]
            Vi_y = self.Vij_centers[:, :, 1] @ self.vortex_strengths + self.freestream_velocities[:, 1]
            Vi_z = self.Vij_centers[:, :, 2] @ self.vortex_strengths + self.freestream_velocities[:, 2]
            Vi_x = np.expand_dims(Vi_x, axis=1)
            Vi_y = np.expand_dims(Vi_y, axis=1)
            Vi_z = np.expand_dims(Vi_z, axis=1)
            Vi = np.hstack((Vi_x, Vi_y, Vi_z))
            density = self.op_point.density
            Vi_cross_li = np.cross(Vi, (self.vortex_bound_leg), axis=1)
            vortex_strengths_expanded = np.expand_dims((self.vortex_strengths), axis=1)
            self.Fi_geometry = density * Vi_cross_li * vortex_strengths_expanded
            if self.verbose:
                print('Calculating total forces and moments...')
            self.Ftotal_geometry = np.sum((self.Fi_geometry), axis=0)
            self.Ftotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Ftotal_geometry
            self.Mtotal_geometry = np.sum((np.cross(self.vortex_centers - self.airplane.xyz_ref, self.Fi_geometry)), axis=0)
            self.Mtotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Mtotal_geometry
            q = self.op_point.dynamic_pressure()
            s_ref = self.airplane.s_ref
            b_ref = self.airplane.b_ref
            c_ref = self.airplane.c_ref
            self.CL = -self.Ftotal_wind[2] / q / s_ref
            self.CDi = -self.Ftotal_wind[0] / q / s_ref
            self.CY = self.Ftotal_wind[1] / q / s_ref
            self.Cl = self.Mtotal_wind[0] / q / b_ref
            self.Cm = self.Mtotal_wind[1] / q / c_ref
            self.Cn = self.Mtotal_wind[2] / q / b_ref
            if self.CDi == 0:
                self.CL_over_CDi = 0
            else:
                self.CL_over_CDi = self.CL / self.CDi
        if self.verbose:
            print('\nForces\n-----')
        if self.verbose:
            print('CL: ', self.CL)
        if self.verbose:
            print('CDi: ', self.CDi)
        if self.verbose:
            print('CY: ', self.CY)
        if self.verbose:
            print('CL/CDi: ', self.CL_over_CDi)
        if self.verbose:
            print('\nMoments\n-----')
        if self.verbose:
            print('Cl: ', self.Cl)
        if self.verbose:
            print('Cm: ', self.Cm)
        if self.verbose:
            print('Cn: ', self.Cn)

    def calculate_Vij(self, points):
        left_vortex_vertices = self.left_vortex_vertices
        right_vortex_vertices = self.right_vortex_vertices
        points = np.reshape(points, (-1, 3))
        n_points = len(points)
        n_vortices = self.n_panels
        points = np.expand_dims(points, 1)
        a = points - left_vortex_vertices
        b = points - right_vortex_vertices
        a_cross_b = np.cross(a, b, axis=2)
        a_dot_b = np.einsum('ijk,ijk->ij', a, b)
        a_cross_x = np.stack((
         np.zeros((n_points, n_vortices)),
         a[:, :, 2],
         -a[:, :, 1]),
          axis=2)
        a_dot_x = a[:, :, 0]
        b_cross_x = np.stack((
         np.zeros((n_points, n_vortices)),
         b[:, :, 2],
         -b[:, :, 1]),
          axis=2)
        b_dot_x = b[:, :, 0]
        norm_a = np.linalg.norm(a, axis=2)
        norm_b = np.linalg.norm(b, axis=2)
        norm_a_inv = 1 / norm_a
        norm_b_inv = 1 / norm_b
        bound_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_b, a_cross_b) < 3e-16
        a_dot_b = a_dot_b + bound_vortex_singularity_indices
        left_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_x, a_cross_x) < 3e-16
        a_dot_x = a_dot_x + left_vortex_singularity_indices
        right_vortex_singularity_indices = np.einsum('ijk,ijk->ij', b_cross_x, b_cross_x) < 3e-16
        b_dot_x = b_dot_x + right_vortex_singularity_indices
        term1 = (norm_a_inv + norm_b_inv) / (norm_a * norm_b + a_dot_b)
        term2 = norm_a_inv / (norm_a - a_dot_x)
        term3 = norm_b_inv / (norm_b - b_dot_x)
        term1 = np.expand_dims(term1, 2)
        term2 = np.expand_dims(term2, 2)
        term3 = np.expand_dims(term3, 2)
        Vij = 1 / (4 * np.pi) * (a_cross_b * term1 + a_cross_x * term2 - b_cross_x * term3)
        return Vij

    def calculate_delta_cp(self):
        diag1 = self.front_left_vertices - self.back_right_vertices
        diag2 = self.front_right_vertices - self.back_left_vertices
        self.areas = np.linalg.norm(np.cross(diag1, diag2, axis=1), axis=1) / 2
        self.Fi_normal = np.einsum('ij,ij->i', self.Fi_geometry, self.normal_directions)
        self.pressure_normal = self.Fi_normal / self.areas
        self.delta_cp = self.pressure_normal / self.op_point.dynamic_pressure()

    def get_induced_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vij = self.calculate_Vij(point)
        vortex_strengths_expanded = np.expand_dims(self.vortex_strengths, 1)
        Vi_x = Vij[:, :, 0] @ vortex_strengths_expanded
        Vi_y = Vij[:, :, 1] @ vortex_strengths_expanded
        Vi_z = Vij[:, :, 2] @ vortex_strengths_expanded
        Vi = np.hstack((Vi_x, Vi_y, Vi_z))
        return Vi

    def get_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vi = self.get_induced_velocity_at_point(point)
        freestream = self.op_point.compute_freestream_velocity_geometry_axes()
        V = Vi + freestream
        return V

    def calculate_streamlines(self):
        n_steps = 100
        length = 1
        length_per_step = length / n_steps
        seed_points = (0.5 * (self.back_left_vertices + self.back_right_vertices))[self.is_trailing_edge]
        n_streamlines = len(seed_points)
        streamlines = np.zeros((n_streamlines, n_steps, 3))
        streamlines[:, 0, :] = seed_points
        for step_num in range(1, n_steps):
            update_amount = self.get_velocity_at_point(streamlines[:, step_num - 1, :])
            update_amount = update_amount * length_per_step / np.expand_dims(np.linalg.norm(update_amount, axis=1), axis=1)
            streamlines[:, step_num, :] = streamlines[:, step_num - 1, :] + update_amount

        self.streamlines = streamlines

    def draw(self, draw_delta_cp=True, draw_streamlines=True):
        print('Drawing...')
        vertices = np.vstack((
         self.front_left_vertices,
         self.front_right_vertices,
         self.back_right_vertices,
         self.back_left_vertices))
        faces = np.transpose(np.vstack((
         4 * np.ones(self.n_panels),
         np.arange(self.n_panels),
         np.arange(self.n_panels) + self.n_panels,
         np.arange(self.n_panels) + 2 * self.n_panels,
         np.arange(self.n_panels) + 3 * self.n_panels)))
        faces = np.reshape(faces, (-1), order='C')
        wing_surfaces = pv.PolyData(vertices, faces)
        plotter = pv.Plotter()
        if draw_delta_cp:
            if not hasattr(self, 'delta_cp'):
                self.calculate_delta_cp()
            delta_cp_min = -1.5
            delta_cp_max = 1.5
            scalars = np.minimum(np.maximum(self.delta_cp, delta_cp_min), delta_cp_max)
            cmap = plt.cm.get_cmap('viridis')
            plotter.add_mesh(wing_surfaces, scalars=scalars, cmap=cmap, color='tan', show_edges=True, smooth_shading=True)
            plotter.add_scalar_bar(title='Pressure Coefficient Differential', n_labels=5, shadow=True, font_family='arial')
        if draw_streamlines:
            if not hasattr(self, 'streamlines'):
                self.calculate_streamlines()
            for streamline_num in range(len(self.streamlines)):
                plotter.add_lines((self.streamlines[streamline_num, :, :]), width=1, color='#50C7C7')

        plotter.show_grid(color='#444444')
        plotter.set_background(color='black')
        plotter.show(cpos=(-1, -1, 1), full_screen=False)


class panel1(AeroProblem):

    def run(self, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print('Running PANEL1 calculation...')
        self.make_panels()
        self.setup_geometry()
        self.setup_operating_point()
        self.calculate_vortex_strengths()
        self.calculate_forces()
        if self.verbose:
            print('PANEL1 calculation complete!')

    def make_panels(self):
        if self.verbose:
            print('Meshing...')
        collocation_points = np.empty((0, 3))
        normal_directions = np.empty((0, 3))
        left_vortex_vertices = np.empty((0, 3))
        right_vortex_vertices = np.empty((0, 3))
        front_left_vertices = np.empty((0, 3))
        front_right_vertices = np.empty((0, 3))
        back_left_vertices = np.empty((0, 3))
        back_right_vertices = np.empty((0, 3))
        areas = np.empty(0)
        is_trailing_edge_upper = np.empty(0, dtype=bool)
        is_trailing_edge_lower = np.empty(0, dtype=bool)
        for wing_num in range(len(self.airplane.wings)):
            wing = self.airplane.wings[wing_num]
            n_chordwise_coordinates = wing.chordwise_panels + 1
            if wing.chordwise_spacing == 'uniform':
                nondim_chordwise_coordinates = np.linspace(0, 1, n_chordwise_coordinates)
            else:
                if wing.chordwise_spacing == 'cosine':
                    nondim_chordwise_coordinates = cosspace(0, 1, n_chordwise_coordinates)
                else:
                    raise Exception('Bad value of wing.chordwise_spacing!')
            xsec_xyz_le = np.empty((0, 3))
            xsec_xyz_te = np.empty((0, 3))
            for xsec in wing.xsecs:
                xsec_xyz_le = np.vstack((xsec_xyz_le, xsec.xyz_le + wing.xyz_le))
                xsec_xyz_te = np.vstack((xsec_xyz_te, xsec.xyz_te() + wing.xyz_le))

            xsec_xyz_quarter_chords = 0.75 * xsec_xyz_le + 0.25 * xsec_xyz_te
            section_quarter_chords = xsec_xyz_quarter_chords[1:, :] - xsec_xyz_quarter_chords[:-1, :]
            section_quarter_chords_proj = section_quarter_chords[:, 1:] / np.expand_dims(np.linalg.norm((section_quarter_chords[:, 1:]), axis=1), axis=1)
            section_quarter_chords_proj = np.hstack((
             np.zeros((section_quarter_chords_proj.shape[0], 1)), section_quarter_chords_proj))
            if len(wing.xsecs) > 2:
                xsec_local_normal_inners = section_quarter_chords_proj[:-1, :] + section_quarter_chords_proj[1:, :]
                xsec_local_normal_inners = xsec_local_normal_inners / np.expand_dims(np.linalg.norm(xsec_local_normal_inners, axis=1), axis=1)
                xsec_local_normal = np.vstack((
                 section_quarter_chords_proj[0, :],
                 xsec_local_normal_inners,
                 section_quarter_chords_proj[-1, :]))
            else:
                xsec_local_normal = np.vstack((
                 section_quarter_chords_proj[0, :],
                 section_quarter_chords_proj[-1, :]))
            xsec_local_back = xsec_xyz_te - xsec_xyz_le
            xsec_chord = np.linalg.norm(xsec_local_back, axis=1)
            xsec_local_back = xsec_local_back / np.expand_dims(xsec_chord, axis=1)
            xsec_local_up = np.cross(xsec_local_back, xsec_local_normal, axis=1)
            xsec_scaling_factor = 1 / np.sqrt((1 + np.sum((section_quarter_chords_proj[1:, :] * section_quarter_chords_proj[:-1, :]),
              axis=1)) / 2)
            xsec_scaling_factor = np.hstack((1, xsec_scaling_factor, 1))
            for section_num in range(len(wing.xsecs) - 1):
                inner_xsec = wing.xsecs[section_num]
                outer_xsec = wing.xsecs[(section_num + 1)]
                inner_airfoil = inner_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point=(inner_xsec.control_surface_hinge_point))
                outer_airfoil = outer_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point=(inner_xsec.control_surface_hinge_point))
                inner_xsec_coordinates_nondim = inner_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                outer_xsec_coordinates_nondim = outer_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                inner_xsec_mcl = xsec_xyz_le[section_num, :] + (xsec_local_back[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[section_num] + xsec_local_up[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[section_num] * xsec_scaling_factor[section_num])
                outer_xsec_mcl = xsec_xyz_le[section_num + 1, :] + (xsec_local_back[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[(section_num + 1)] + xsec_local_up[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[(section_num + 1)] * xsec_scaling_factor[(section_num + 1)])
                n_spanwise_coordinates = xsec.spanwise_panels + 1
                if xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                else:
                    if xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = cosspace(n_points=n_spanwise_coordinates)
                    else:
                        raise Exception('Bad value of section.spanwise_spacing!')
                section_mcl_coordinates = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_xsec_mcl, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_xsec_mcl, 1)
                front_inner_coordinates = section_mcl_coordinates[:-1, :-1, :]
                front_outer_coordinates = section_mcl_coordinates[:-1, 1:, :]
                back_inner_coordinates = section_mcl_coordinates[1:, :-1, :]
                back_outer_coordinates = section_mcl_coordinates[1:, 1:, :]
                section_is_trailing_edge_upper = np.vstack((
                 np.zeros((wing.chordwise_panels * 2 - 1, xsec.spanwise_panels), dtype=bool),
                 np.ones((1, xsec.spanwise_panels), dtype=bool)))
                section_is_trailing_edge_lower = np.flipud(section_is_trailing_edge_upper)
                front_inner_coordinates = np.reshape(front_inner_coordinates, (-1,
                                                                               3), order='F')
                front_outer_coordinates = np.reshape(front_outer_coordinates, (-1,
                                                                               3), order='F')
                back_inner_coordinates = np.reshape(back_inner_coordinates, (-1, 3), order='F')
                back_outer_coordinates = np.reshape(back_outer_coordinates, (-1, 3), order='F')
                section_is_trailing_edge_upper = np.reshape(section_is_trailing_edge_upper, (-1), order='F')
                section_is_trailing_edge_lower = np.reshape(section_is_trailing_edge_lower, (-1), order='F')
                diag1 = front_outer_coordinates - back_inner_coordinates
                diag2 = front_inner_coordinates - back_outer_coordinates
                diag_cross = np.cross(diag1, diag2, axis=1)
                diag_cross_norm = np.linalg.norm(diag_cross, axis=1)
                normals_to_add = diag_cross / np.expand_dims(diag_cross_norm, axis=1)
                areas_to_add = diag_cross_norm / 2
                collocations_to_add = 0.5 * (0.25 * front_inner_coordinates + 0.75 * back_inner_coordinates) + 0.5 * (0.25 * front_outer_coordinates + 0.75 * back_outer_coordinates)
                inner_vortex_vertices_to_add = 0.75 * front_inner_coordinates + 0.25 * back_inner_coordinates
                outer_vortex_vertices_to_add = 0.75 * front_outer_coordinates + 0.25 * back_outer_coordinates
                front_left_vertices = np.vstack((
                 front_left_vertices,
                 front_inner_coordinates))
                front_right_vertices = np.vstack((
                 front_right_vertices,
                 front_outer_coordinates))
                back_left_vertices = np.vstack((
                 back_left_vertices,
                 back_inner_coordinates))
                back_right_vertices = np.vstack((
                 back_right_vertices,
                 back_outer_coordinates))
                areas = np.hstack((
                 areas,
                 areas_to_add))
                is_trailing_edge_upper = np.hstack((
                 is_trailing_edge_upper,
                 section_is_trailing_edge_upper))
                is_trailing_edge_lower = np.hstack((
                 is_trailing_edge_lower,
                 section_is_trailing_edge_lower))
                collocation_points = np.vstack((
                 collocation_points,
                 collocations_to_add))
                normal_directions = np.vstack((
                 normal_directions,
                 normals_to_add))
                left_vortex_vertices = np.vstack((
                 left_vortex_vertices,
                 inner_vortex_vertices_to_add))
                right_vortex_vertices = np.vstack((
                 right_vortex_vertices,
                 outer_vortex_vertices_to_add))
                if wing.symmetric:
                    if inner_xsec.control_surface_type == 'asymmetric':
                        inner_airfoil = inner_xsec.airfoil.add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point=(inner_xsec.control_surface_hinge_point))
                        outer_airfoil = outer_xsec.airfoil.add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point=(inner_xsec.control_surface_hinge_point))
                        inner_xsec_coordinates_nondim = inner_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                        outer_xsec_coordinates_nondim = outer_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                        inner_xsec_mcl = xsec_xyz_le[section_num, :] + (xsec_local_back[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[section_num] + xsec_local_up[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[section_num] * xsec_scaling_factor[section_num])
                        outer_xsec_mcl = xsec_xyz_le[section_num + 1, :] + (xsec_local_back[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[(section_num + 1)] + xsec_local_up[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[(section_num + 1)] * xsec_scaling_factor[(section_num + 1)])
                        section_mcl_coordinates = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_xsec_mcl, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_xsec_mcl, 1)
                        front_inner_coordinates = section_mcl_coordinates[:-1, :-1, :]
                        front_outer_coordinates = section_mcl_coordinates[:-1, 1:, :]
                        back_inner_coordinates = section_mcl_coordinates[1:, :-1, :]
                        back_outer_coordinates = section_mcl_coordinates[1:, 1:, :]
                        front_inner_coordinates = np.reshape(front_inner_coordinates, (-1,
                                                                                       3), order='F')
                        front_outer_coordinates = np.reshape(front_outer_coordinates, (-1,
                                                                                       3), order='F')
                        back_inner_coordinates = np.reshape(back_inner_coordinates, (-1,
                                                                                     3), order='F')
                        back_outer_coordinates = np.reshape(back_outer_coordinates, (-1,
                                                                                     3), order='F')
                        diag1 = front_outer_coordinates - back_inner_coordinates
                        diag2 = front_inner_coordinates - back_outer_coordinates
                        diag_cross = np.cross(diag1, diag2, axis=1)
                        diag_cross_norm = np.linalg.norm(diag_cross, axis=1)
                        normals_to_add = diag_cross / np.expand_dims(diag_cross_norm, axis=1)
                        areas_to_add = diag_cross_norm / 2
                        collocations_to_add = 0.5 * (0.25 * front_inner_coordinates + 0.75 * back_inner_coordinates) + 0.5 * (0.25 * front_outer_coordinates + 0.75 * back_outer_coordinates)
                        inner_vortex_vertices_to_add = 0.75 * front_inner_coordinates + 0.25 * back_inner_coordinates
                        outer_vortex_vertices_to_add = 0.75 * front_outer_coordinates + 0.25 * back_outer_coordinates
                    front_left_vertices = np.vstack((
                     front_left_vertices,
                     reflect_over_XZ_plane(front_outer_coordinates)))
                    front_right_vertices = np.vstack((
                     front_right_vertices,
                     reflect_over_XZ_plane(front_inner_coordinates)))
                    back_left_vertices = np.vstack((
                     back_left_vertices,
                     reflect_over_XZ_plane(back_outer_coordinates)))
                    back_right_vertices = np.vstack((
                     back_right_vertices,
                     reflect_over_XZ_plane(back_inner_coordinates)))
                    areas = np.hstack((
                     areas,
                     areas_to_add))
                    is_trailing_edge_upper = np.hstack((
                     is_trailing_edge_upper,
                     section_is_trailing_edge_upper))
                    is_trailing_edge_lower = np.hstack((
                     is_trailing_edge_lower,
                     section_is_trailing_edge_lower))
                    collocation_points = np.vstack((
                     collocation_points,
                     reflect_over_XZ_plane(collocations_to_add)))
                    normal_directions = np.vstack((
                     normal_directions,
                     reflect_over_XZ_plane(normals_to_add)))
                    left_vortex_vertices = np.vstack((
                     left_vortex_vertices,
                     reflect_over_XZ_plane(outer_vortex_vertices_to_add)))
                    right_vortex_vertices = np.vstack((
                     right_vortex_vertices,
                     reflect_over_XZ_plane(inner_vortex_vertices_to_add)))

        self.front_left_vertices = front_left_vertices
        self.front_right_vertices = front_right_vertices
        self.back_left_vertices = back_left_vertices
        self.back_right_vertices = back_right_vertices
        self.areas = areas
        self.is_trailing_edge_upper = is_trailing_edge_upper
        self.is_trailing_edge_lower = is_trailing_edge_lower
        self.collocation_points = collocation_points
        self.normal_directions = normal_directions
        self.left_vortex_vertices = left_vortex_vertices
        self.right_vortex_vertices = right_vortex_vertices
        self.vortex_centers = (self.left_vortex_vertices + self.right_vortex_vertices) / 2
        self.vortex_bound_leg = self.right_vortex_vertices - self.left_vortex_vertices
        self.n_panels = len(self.collocation_points)
        if self.verbose:
            print('Meshing complete!')

    def setup_geometry(self):
        if self.verbose:
            print('Calculating the collocation influence matrix...')
        self.Vij_collocations = self.calculate_Vij(self.collocation_points)
        self.AIC = np.sum((self.Vij_collocations * np.expand_dims(self.normal_directions, 1)),
          axis=2)
        if self.verbose:
            print('Calculating the vortex center influence matrix...')
        self.Vij_centers = self.calculate_Vij(self.vortex_centers)

    def setup_operating_point(self):
        if self.verbose:
            print('Calculating the freestream influence...')
        self.steady_freestream_velocity = np.expand_dims(self.op_point.compute_freestream_velocity_geometry_axes(), 0)
        self.rotation_freestream_velocities = self.op_point.compute_rotation_velocity_geometry_axes(self.collocation_points)
        self.freestream_velocities = self.steady_freestream_velocity + self.rotation_freestream_velocities
        self.freestream_influences = np.sum((self.freestream_velocities * self.normal_directions), axis=1)

    def calculate_vortex_strengths(self):
        if self.verbose:
            print('Calculating vortex strengths...')
        self.vortex_strengths = np.linalg.solve(self.AIC, -self.freestream_influences)

    def calculate_forces(self):
        if self.verbose:
            print('Calculating forces on each panel...')
        else:
            Vi_x = self.Vij_centers[:, :, 0] @ self.vortex_strengths + self.freestream_velocities[:, 0]
            Vi_y = self.Vij_centers[:, :, 1] @ self.vortex_strengths + self.freestream_velocities[:, 1]
            Vi_z = self.Vij_centers[:, :, 2] @ self.vortex_strengths + self.freestream_velocities[:, 2]
            Vi_x = np.expand_dims(Vi_x, axis=1)
            Vi_y = np.expand_dims(Vi_y, axis=1)
            Vi_z = np.expand_dims(Vi_z, axis=1)
            Vi = np.hstack((Vi_x, Vi_y, Vi_z))
            density = self.op_point.density
            Vi_cross_li = np.cross(Vi, (self.vortex_bound_leg), axis=1)
            vortex_strengths_expanded = np.expand_dims((self.vortex_strengths), axis=1)
            self.Fi_geometry = density * Vi_cross_li * vortex_strengths_expanded
            if self.verbose:
                print('Calculating total forces and moments...')
            self.Ftotal_geometry = np.sum((self.Fi_geometry), axis=0)
            self.Ftotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Ftotal_geometry
            self.Mtotal_geometry = np.sum((np.cross(self.vortex_centers - self.airplane.xyz_ref, self.Fi_geometry)), axis=0)
            self.Mtotal_wind = np.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Mtotal_geometry
            q = self.op_point.dynamic_pressure()
            s_ref = self.airplane.s_ref
            b_ref = self.airplane.b_ref
            c_ref = self.airplane.c_ref
            self.CL = -self.Ftotal_wind[2] / q / s_ref
            self.CDi = -self.Ftotal_wind[0] / q / s_ref
            self.CY = self.Ftotal_wind[1] / q / s_ref
            self.Cl = self.Mtotal_wind[0] / q / b_ref
            self.Cm = self.Mtotal_wind[1] / q / c_ref
            self.Cn = self.Mtotal_wind[2] / q / b_ref
            if self.CDi == 0:
                self.CL_over_CDi = 0
            else:
                self.CL_over_CDi = self.CL / self.CDi
        if self.verbose:
            print('\nForces\n-----')
        if self.verbose:
            print('CL: ', self.CL)
        if self.verbose:
            print('CDi: ', self.CDi)
        if self.verbose:
            print('CY: ', self.CY)
        if self.verbose:
            print('CL/CDi: ', self.CL_over_CDi)
        if self.verbose:
            print('\nMoments\n-----')
        if self.verbose:
            print('Cl: ', self.Cl)
        if self.verbose:
            print('Cm: ', self.Cm)
        if self.verbose:
            print('Cn: ', self.Cn)

    def calculate_Vij(self, points):
        left_vortex_vertices = self.left_vortex_vertices
        right_vortex_vertices = self.right_vortex_vertices
        points = np.reshape(points, (-1, 3))
        n_points = len(points)
        n_vortices = self.n_panels
        points = np.expand_dims(points, 1)
        a = points - left_vortex_vertices
        b = points - right_vortex_vertices
        a_cross_b = np.cross(a, b, axis=2)
        a_dot_b = np.einsum('ijk,ijk->ij', a, b)
        a_cross_x = np.stack((
         np.zeros((n_points, n_vortices)),
         a[:, :, 2],
         -a[:, :, 1]),
          axis=2)
        a_dot_x = a[:, :, 0]
        b_cross_x = np.stack((
         np.zeros((n_points, n_vortices)),
         b[:, :, 2],
         -b[:, :, 1]),
          axis=2)
        b_dot_x = b[:, :, 0]
        norm_a = np.linalg.norm(a, axis=2)
        norm_b = np.linalg.norm(b, axis=2)
        norm_a_inv = 1 / norm_a
        norm_b_inv = 1 / norm_b
        bound_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_b, a_cross_b) < 3e-16
        a_dot_b = a_dot_b + bound_vortex_singularity_indices
        left_vortex_singularity_indices = np.einsum('ijk,ijk->ij', a_cross_x, a_cross_x) < 3e-16
        a_dot_x = a_dot_x + left_vortex_singularity_indices
        right_vortex_singularity_indices = np.einsum('ijk,ijk->ij', b_cross_x, b_cross_x) < 3e-16
        b_dot_x = b_dot_x + right_vortex_singularity_indices
        term1 = (norm_a_inv + norm_b_inv) / (norm_a * norm_b + a_dot_b)
        term2 = norm_a_inv / (norm_a - a_dot_x)
        term3 = norm_b_inv / (norm_b - b_dot_x)
        term1 = np.expand_dims(term1, 2)
        term2 = np.expand_dims(term2, 2)
        term3 = np.expand_dims(term3, 2)
        Vij = 1 / (4 * np.pi) * (a_cross_b * term1 + a_cross_x * term2 - b_cross_x * term3)
        return Vij

    def calculate_delta_cp(self):
        diag1 = self.front_left_vertices - self.back_right_vertices
        diag2 = self.front_right_vertices - self.back_left_vertices
        self.areas = np.linalg.norm(np.cross(diag1, diag2, axis=1), axis=1) / 2
        self.Fi_normal = np.einsum('ij,ij->i', self.Fi_geometry, self.normal_directions)
        self.pressure_normal = self.Fi_normal / self.areas
        self.delta_cp = self.pressure_normal / self.op_point.dynamic_pressure()

    def get_induced_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vij = self.calculate_Vij(point)
        vortex_strengths_expanded = np.expand_dims(self.vortex_strengths, 1)
        Vi_x = Vij[:, :, 0] @ vortex_strengths_expanded
        Vi_y = Vij[:, :, 1] @ vortex_strengths_expanded
        Vi_z = Vij[:, :, 2] @ vortex_strengths_expanded
        Vi = np.hstack((Vi_x, Vi_y, Vi_z))
        return Vi

    def get_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vi = self.get_induced_velocity_at_point(point)
        freestream = self.op_point.compute_freestream_velocity_geometry_axes()
        V = Vi + freestream
        return V

    def calculate_streamlines(self):
        n_steps = 100
        length = 1
        length_per_step = length / n_steps
        seed_points = (0.5 * (self.back_left_vertices + self.back_right_vertices))[self.is_trailing_edge]
        n_streamlines = len(seed_points)
        streamlines = np.zeros((n_streamlines, n_steps, 3))
        streamlines[:, 0, :] = seed_points
        for step_num in range(1, n_steps):
            update_amount = self.get_velocity_at_point(streamlines[:, step_num - 1, :])
            update_amount = update_amount * length_per_step / np.expand_dims(np.linalg.norm(update_amount, axis=1), axis=1)
            streamlines[:, step_num, :] = streamlines[:, step_num - 1, :] + update_amount

        self.streamlines = streamlines

    def draw(self, shading='delta_cp', draw_streamlines=True):
        print('Drawing...')
        vertices = np.vstack((
         self.front_left_vertices,
         self.front_right_vertices,
         self.back_right_vertices,
         self.back_left_vertices))
        faces = np.transpose(np.vstack((
         4 * np.ones(self.n_panels),
         np.arange(self.n_panels),
         np.arange(self.n_panels) + self.n_panels,
         np.arange(self.n_panels) + 2 * self.n_panels,
         np.arange(self.n_panels) + 3 * self.n_panels)))
        faces = np.reshape(faces, (-1), order='C')
        wing_surfaces = pv.PolyData(vertices, faces)
        plotter = pv.Plotter()
        if shading == 'none':
            plotter.add_mesh(wing_surfaces, color='tan', show_edges=True, smooth_shading=True)
        else:
            if shading == 'delta_cp':
                if not hasattr(self, 'delta_cp'):
                    self.calculate_delta_cp()
                delta_cp_min = -1.5
                delta_cp_max = 1.5
                scalars = np.minimum(np.maximum(self.delta_cp, delta_cp_min), delta_cp_max)
                cmap = plt.cm.get_cmap('viridis')
                plotter.add_mesh(wing_surfaces, scalars=scalars, cmap=cmap, color='tan', show_edges=True, smooth_shading=True)
                plotter.add_scalar_bar(title='Pressure Coefficient Differential', n_labels=5, shadow=True, font_family='arial')
            else:
                if shading == 'trailing_edges':
                    scalars = np.logical_or(self.is_trailing_edge_upper, self.is_trailing_edge_lower)
                    scalars = scalars.astype(int)
                    plotter.add_mesh(wing_surfaces, scalars=scalars, color='tan', show_edges=True, smooth_shading=True)
                if draw_streamlines:
                    if not hasattr(self, 'streamlines'):
                        self.calculate_streamlines()
                    for streamline_num in range(len(self.streamlines)):
                        plotter.add_lines((self.streamlines[streamline_num, :, :]), width=1, color='#50C7C7')

                plotter.show_grid(color='#444444')
                plotter.set_background(color='black')
                plotter.show(cpos=(-1, -1, 1), full_screen=False)