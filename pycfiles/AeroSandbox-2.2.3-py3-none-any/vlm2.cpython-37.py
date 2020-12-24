# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics\vlm2.py
# Compiled at: 2019-08-07 12:55:29
# Size of source mod 2**32: 56928 bytes
from .aerodynamics import *

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
            elif wing.chordwise_spacing == 'cosine':
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
                elif xsec.spanwise_spacing == 'cosine':
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
                elif xsec.spanwise_spacing == 'cosine':
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
                elif control_surface_hinge_point_index >= wing.chordwise_panels:
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
                        elif xsec.spanwise_spacing == 'cosine':
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
                            elif control_surface_hinge_point_index >= wing.chordwise_panels:
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