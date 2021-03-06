# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics\vlm1.py
# Compiled at: 2019-08-07 12:55:29
# Size of source mod 2**32: 33174 bytes
from .aerodynamics import *

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