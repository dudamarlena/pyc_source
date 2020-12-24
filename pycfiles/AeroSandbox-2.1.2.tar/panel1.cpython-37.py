# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics\panel1.py
# Compiled at: 2019-12-22 22:43:09
# Size of source mod 2**32: 47780 bytes
from .aerodynamics import *

class panel1(AeroProblem):

    def run(self, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print('Running PANEL1 calculation...')
        self.make_panels()
        self.setup_LHS()
        self.setup_RHS()
        self.calculate_vortex_strengths()
        if self.verbose:
            print('PANEL1 calculation complete!')

    def make_panels(self):
        if self.verbose:
            print('Meshing...')
        collocation_points = np.empty((0, 3))
        normal_directions = np.empty((0, 3))
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
                inner_airfoil = inner_xsec.airfoil.get_sharp_TE_airfoil().add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point=(inner_xsec.control_surface_hinge_point))
                outer_airfoil = outer_xsec.airfoil.get_sharp_TE_airfoil().add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point=(inner_xsec.control_surface_hinge_point))
                inner_xsec_coordinates_nondim = inner_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                outer_xsec_coordinates_nondim = outer_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                inner_panel_coordinates = xsec_xyz_le[section_num, :] + (xsec_local_back[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[section_num] + xsec_local_up[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[section_num] * xsec_scaling_factor[section_num])
                outer_panel_coordinates = xsec_xyz_le[section_num + 1, :] + (xsec_local_back[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[(section_num + 1)] + xsec_local_up[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[(section_num + 1)] * xsec_scaling_factor[(section_num + 1)])
                n_spanwise_coordinates = xsec.spanwise_panels + 1
                if xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                else:
                    if xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = cosspace(n_points=n_spanwise_coordinates)
                    else:
                        raise Exception('Bad value of section.spanwise_spacing!')
                section_panel_coordinates = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_panel_coordinates, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_panel_coordinates, 1)
                front_inner_coordinates = section_panel_coordinates[1:, :-1, :]
                front_outer_coordinates = section_panel_coordinates[1:, 1:, :]
                back_inner_coordinates = section_panel_coordinates[:-1, :-1, :]
                back_outer_coordinates = section_panel_coordinates[:-1, 1:, :]
                section_is_trailing_edge_lower = np.vstack((
                 np.zeros((wing.chordwise_panels * 2 - 1, xsec.spanwise_panels), dtype=bool),
                 np.ones((1, xsec.spanwise_panels), dtype=bool)))
                section_is_trailing_edge_upper = np.flipud(section_is_trailing_edge_lower)
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
                collocations_to_add = 0.5 * (0.5 * front_inner_coordinates + 0.5 * back_inner_coordinates) + 0.5 * (0.5 * front_outer_coordinates + 0.5 * back_outer_coordinates)
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
                if wing.symmetric:
                    if inner_xsec.control_surface_type == 'asymmetric':
                        inner_airfoil = inner_xsec.airfoil.get_sharp_TE_airfoil().add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point=(inner_xsec.control_surface_hinge_point))
                        outer_airfoil = outer_xsec.airfoil.get_sharp_TE_airfoil().add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point=(inner_xsec.control_surface_hinge_point))
                        inner_xsec_coordinates_nondim = inner_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                        outer_xsec_coordinates_nondim = outer_airfoil.get_repaneled_airfoil(n_points_per_side=n_chordwise_coordinates).coordinates
                        inner_panel_coordinates = xsec_xyz_le[section_num, :] + (xsec_local_back[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[section_num] + xsec_local_up[section_num, :] * np.expand_dims(inner_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[section_num] * xsec_scaling_factor[section_num])
                        outer_panel_coordinates = xsec_xyz_le[section_num + 1, :] + (xsec_local_back[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 0], 1) * xsec_chord[(section_num + 1)] + xsec_local_up[section_num + 1, :] * np.expand_dims(outer_xsec_coordinates_nondim[:, 1], 1) * xsec_chord[(section_num + 1)] * xsec_scaling_factor[(section_num + 1)])
                        section_panel_coordinates = np.expand_dims(1 - nondim_spanwise_coordinates, 2) * np.expand_dims(inner_panel_coordinates, 1) + np.expand_dims(nondim_spanwise_coordinates, 2) * np.expand_dims(outer_panel_coordinates, 1)
                        front_inner_coordinates = section_panel_coordinates[1:, :-1, :]
                        front_outer_coordinates = section_panel_coordinates[1:, 1:, :]
                        back_inner_coordinates = section_panel_coordinates[:-1, :-1, :]
                        back_outer_coordinates = section_panel_coordinates[:-1, 1:, :]
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
                        collocations_to_add = 0.5 * (0.5 * front_inner_coordinates + 0.5 * back_inner_coordinates) + 0.5 * (0.5 * front_outer_coordinates + 0.5 * back_outer_coordinates)
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

        self.front_left_vertices = front_left_vertices
        self.front_right_vertices = front_right_vertices
        self.back_left_vertices = back_left_vertices
        self.back_right_vertices = back_right_vertices
        self.areas = areas
        self.is_trailing_edge_upper = is_trailing_edge_upper
        self.is_trailing_edge_lower = is_trailing_edge_lower
        self.collocation_points = collocation_points
        self.normal_directions = normal_directions
        self.left_horseshoe_vortex_vertices = back_left_vertices[is_trailing_edge_upper]
        self.right_horseshoe_vortex_vertices = back_right_vertices[is_trailing_edge_upper]
        self.horseshoe_vortex_centers = (self.left_horseshoe_vortex_vertices + self.right_horseshoe_vortex_vertices) / 2
        self.n_panels = len(self.collocation_points)
        self.n_horseshoes = len(self.left_horseshoe_vortex_vertices)
        if self.verbose:
            print('Meshing complete!')

    def setup_LHS(self):
        if self.verbose:
            print('Calculating the collocation influence matrix...')
        self.Vij = self.calculate_Vij(self.collocation_points)
        self.AIC = np.sum((self.Vij * np.expand_dims(self.normal_directions, 1)),
          axis=2)
        if self.verbose:
            print('Enforcing Kutta condition...')
        trailing_edge_upper_indices = np.argwhere(self.is_trailing_edge_upper)
        trailing_edge_lower_indices = np.argwhere(self.is_trailing_edge_lower)
        kutta_condition_submatrix = np.zeros((self.n_horseshoes, self.n_panels))
        np.put_along_axis(kutta_condition_submatrix,
          trailing_edge_upper_indices,
          1,
          axis=1)
        np.put_along_axis(kutta_condition_submatrix,
          trailing_edge_lower_indices,
          (-1),
          axis=1)
        zeros_submatrix = -np.eye(self.n_horseshoes)
        kutta_and_zeros = np.hstack((kutta_condition_submatrix, zeros_submatrix))
        self.LHS_matrix = np.vstack((self.AIC, kutta_and_zeros))

    def setup_RHS(self):
        if self.verbose:
            print('Calculating the freestream influence...')
        self.steady_freestream_velocity = np.expand_dims(self.op_point.compute_freestream_velocity_geometry_axes(), 0)
        self.rotation_freestream_velocities = self.op_point.compute_rotation_velocity_geometry_axes(self.collocation_points)
        self.freestream_velocities = self.steady_freestream_velocity + self.rotation_freestream_velocities
        self.freestream_influences = np.sum((self.freestream_velocities * self.normal_directions), axis=1)
        kutta_zeros = np.zeros(self.n_horseshoes)
        self.RHS_vector = np.hstack((-self.freestream_influences, kutta_zeros))

    def calculate_vortex_strengths(self):
        if self.verbose:
            print('Calculating vortex strengths...')
        self.solution = np.linalg.solve(self.LHS_matrix, self.RHS_vector)
        self.doublet_strengths = self.solution[:self.n_panels]
        self.horseshoe_vortex_strengths = self.solution[self.n_panels:]
        print('horseshoe_vortex_strengths sum: ', np.sum(self.horseshoe_vortex_strengths))

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
        Vij_doublets = self.calculate_Vij_doublets(points)
        Vij_horseshoes = self.calculate_Vij_horseshoes(points)
        Vij = np.hstack((Vij_doublets, Vij_horseshoes))
        return Vij

    def calculate_Vij_doublets(self, points):
        points = np.reshape(points, (-1, 3))
        n_points = len(points)
        n_vortices = self.n_panels
        points = np.expand_dims(points, 1)
        v1 = points - self.front_left_vertices
        v2 = points - self.front_right_vertices
        v3 = points - self.back_right_vertices
        v4 = points - self.back_left_vertices
        v1_cross_v2 = np.cross(v1, v2, axis=2)
        v2_cross_v3 = np.cross(v2, v3, axis=2)
        v3_cross_v4 = np.cross(v3, v4, axis=2)
        v4_cross_v1 = np.cross(v4, v1, axis=2)
        v1_dot_v2 = np.einsum('ijk,ijk->ij', v1, v2)
        v2_dot_v3 = np.einsum('ijk,ijk->ij', v2, v3)
        v3_dot_v4 = np.einsum('ijk,ijk->ij', v3, v4)
        v4_dot_v1 = np.einsum('ijk,ijk->ij', v4, v1)
        norm_v1 = np.linalg.norm(v1, axis=2)
        norm_v2 = np.linalg.norm(v2, axis=2)
        norm_v3 = np.linalg.norm(v3, axis=2)
        norm_v4 = np.linalg.norm(v4, axis=2)
        norm_v1_inv = 1 / norm_v1
        norm_v2_inv = 1 / norm_v2
        norm_v3_inv = 1 / norm_v3
        norm_v4_inv = 1 / norm_v4
        v1_v2_singularity_indices = np.einsum('ijk,ijk->ij', v1_cross_v2, v1_cross_v2) < 3e-16
        v1_dot_v2 = v1_dot_v2 + v1_v2_singularity_indices
        v2_v3_singularity_indices = np.einsum('ijk,ijk->ij', v2_cross_v3, v2_cross_v3) < 3e-16
        v2_dot_v3 = v2_dot_v3 + v2_v3_singularity_indices
        v3_v4_singularity_indices = np.einsum('ijk,ijk->ij', v3_cross_v4, v3_cross_v4) < 3e-16
        v3_dot_v4 = v3_dot_v4 + v3_v4_singularity_indices
        v4_v1_singularity_indices = np.einsum('ijk,ijk->ij', v4_cross_v1, v4_cross_v1) < 3e-16
        v4_dot_v1 = v4_dot_v1 + v4_v1_singularity_indices
        term1 = (norm_v1_inv + norm_v2_inv) / (norm_v1 * norm_v2 + v1_dot_v2)
        term1 = np.expand_dims(term1, 2)
        term2 = (norm_v2_inv + norm_v3_inv) / (norm_v2 * norm_v3 + v2_dot_v3)
        term2 = np.expand_dims(term2, 2)
        term3 = (norm_v3_inv + norm_v4_inv) / (norm_v3 * norm_v4 + v3_dot_v4)
        term3 = np.expand_dims(term3, 2)
        term4 = (norm_v4_inv + norm_v1_inv) / (norm_v4 * norm_v1 + v4_dot_v1)
        term4 = np.expand_dims(term4, 2)
        Vij_doublets = 1 / (4 * np.pi) * (v1_cross_v2 * term1 + v2_cross_v3 * term2 + v3_cross_v4 * term3 + v4_cross_v1 * term4)
        return Vij_doublets

    def calculate_Vij_horseshoes(self, points):
        left_vortex_vertices = self.left_horseshoe_vortex_vertices
        right_vortex_vertices = self.right_horseshoe_vortex_vertices
        points = np.reshape(points, (-1, 3))
        n_points = len(points)
        n_vortices = len(left_vortex_vertices)
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
        Vij_horseshoes = 1 / (4 * np.pi) * (a_cross_b * term1 + a_cross_x * term2 - b_cross_x * term3)
        return Vij_horseshoes

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
        solution_expanded = np.expand_dims(self.solution, 1)
        Vi_x = Vij[:, :, 0] @ solution_expanded
        Vi_y = Vij[:, :, 1] @ solution_expanded
        Vi_z = Vij[:, :, 2] @ solution_expanded
        Vi = np.hstack((Vi_x, Vi_y, Vi_z))
        return Vi

    def get_velocity_at_point(self, point):
        point = np.reshape(point, (-1, 3))
        Vi = self.get_induced_velocity_at_point(point)
        freestream = self.op_point.compute_freestream_velocity_geometry_axes()
        V = Vi + freestream
        return V

    def get_streamlines(self, seed_points, n_steps=300, length=0.7):
        length_per_step = length / n_steps
        n_streamlines = len(seed_points)
        streamlines = np.zeros((n_streamlines, n_steps, 3))
        streamlines[:, 0, :] = seed_points
        for step_num in range(1, n_steps):
            update_amount = self.get_velocity_at_point(streamlines[:, step_num - 1, :])
            update_amount = update_amount * length_per_step / np.expand_dims(np.linalg.norm(update_amount, axis=1), axis=1)
            streamlines[:, step_num, :] = streamlines[:, step_num - 1, :] + update_amount

        return streamlines

    def draw(self, shading_type='solid', streamlines_type='trailing', points_type=None):
        print('Drawing...')
        plotter = pv.Plotter()
        if shading_type is not None:
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
            if shading_type == 'solid':
                plotter.add_mesh(wing_surfaces, color='tan', show_edges=True, smooth_shading=True)
            else:
                if shading_type == 'doublet_strengths':
                    if not hasattr(self, 'doublet_strengths'):
                        print('Doublet strengths not found, running again.')
                        self.run()
                    scalars = self.doublet_strengths
                    cmap = plt.cm.get_cmap('viridis')
                    plotter.add_mesh(wing_surfaces, scalars=scalars, cmap=cmap, color='tan', show_edges=True, smooth_shading=True)
                    plotter.add_scalar_bar(title='Doublet Strengths', n_labels=5, shadow=True, font_family='arial')
                else:
                    if shading_type == 'delta_cp':
                        if not hasattr(self, 'delta_cp'):
                            self.calculate_delta_cp()
                        delta_cp_min = -1.5
                        delta_cp_max = 1.5
                        scalars = np.minimum(np.maximum(self.delta_cp, delta_cp_min), delta_cp_max)
                        cmap = plt.cm.get_cmap('viridis')
                        plotter.add_mesh(wing_surfaces, scalars=scalars, cmap=cmap, color='tan', show_edges=True, smooth_shading=True)
                        plotter.add_scalar_bar(title='Pressure Coefficient Differential', n_labels=5, shadow=True, font_family='arial')
                    else:
                        if shading_type == 'all_trailing_edges':
                            scalars = np.logical_or(self.is_trailing_edge_upper, self.is_trailing_edge_lower)
                            scalars = scalars.astype(int)
                            plotter.add_mesh(wing_surfaces, scalars=scalars, color='tan', show_edges=True, smooth_shading=True)
                        else:
                            if shading_type == 'upper_trailing_edges':
                                scalars = self.is_trailing_edge_upper
                                scalars = scalars.astype(int)
                                plotter.add_mesh(wing_surfaces, scalars=scalars, color='tan', show_edges=True, smooth_shading=True)
        if streamlines_type is not None:
            if streamlines_type == 'trailing':
                seed_points = np.vstack((
                 (0.5 * (self.back_left_vertices + self.back_right_vertices))[self.is_trailing_edge_upper],
                 (0.5 * (self.front_left_vertices + self.front_right_vertices))[self.is_trailing_edge_lower]))
            else:
                if streamlines_type == 'line':
                    seed_points = linspace_3D((0, 0, -0.05), (0, 0, 0.05), 30)
                else:
                    seed_points = streamlines_type
            streamlines = self.get_streamlines(seed_points=seed_points)
            for streamline_num in range(len(streamlines)):
                plotter.add_lines((streamlines[streamline_num, :, :]), width=1, color='#50C7C7')

        if points_type is not None:
            points = getattr(self, points_type)
            plotter.add_points(points)
        plotter.show_grid(color='#444444')
        plotter.set_background(color='black')
        plotter.show(cpos=(-1, -1, 1), full_screen=False)