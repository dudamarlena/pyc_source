# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics\casvlm1.py
# Compiled at: 2020-04-18 12:07:31
# Size of source mod 2**32: 37942 bytes
from aerosandbox.aerodynamics.aerodynamics import *
from aerosandbox.geometry import *

class Casvlm1(AeroProblem):

    def __init__(self, airplane, op_point, opti, run_setup=True):
        super().__init__(airplane, op_point)
        self.opti = opti
        if run_setup:
            self.setup()

    def setup(self, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print('Setting up casVLM1 calculation...')
        self.make_panels()
        self.setup_geometry()
        self.setup_operating_point()
        self.calculate_vortex_strengths()
        self.calculate_forces()
        if self.verbose:
            print('casVLM1 setup complete! Ready to pass into the solver...')

    def make_panels(self):
        if self.verbose:
            print('Meshing...')
        front_left_vertices = []
        front_right_vertices = []
        back_left_vertices = []
        back_right_vertices = []
        is_trailing_edge = []
        normal_directions = []
        for wing_num in range(len(self.airplane.wings)):
            wing = self.airplane.wings[wing_num]
            n_chordwise_coordinates = wing.chordwise_panels + 1
            if wing.chordwise_spacing == 'uniform':
                nondim_chordwise_coordinates = np.linspace(0, 1, n_chordwise_coordinates)
            elif wing.chordwise_spacing == 'cosine':
                nondim_chordwise_coordinates = np_cosspace(0, 1, n_chordwise_coordinates)
            else:
                raise Exception('Bad init_val of wing.chordwise_spacing!')
            for section_num in range(len(wing.xsecs) - 1):
                inner_xsec = wing.xsecs[section_num]
                outer_xsec = wing.xsecs[(section_num + 1)]
                inner_xsec_xyz_le = inner_xsec.xyz_le + wing.xyz_le
                inner_xsec_xyz_te = inner_xsec.xyz_te() + wing.xyz_le
                outer_xsec_xyz_le = outer_xsec.xyz_le + wing.xyz_le
                outer_xsec_xyz_te = outer_xsec.xyz_te() + wing.xyz_le
                inner_airfoil = inner_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point_x=(inner_xsec.control_surface_hinge_point))
                outer_airfoil = outer_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                  hinge_point_x=(inner_xsec.control_surface_hinge_point))
                inner_xsec_mcl_y_nondim = inner_airfoil.local_camber(nondim_chordwise_coordinates)
                outer_xsec_mcl_y_nondim = outer_airfoil.local_camber(nondim_chordwise_coordinates)
                inner_xsec_mcl_angle = cas.atan2(cas.diff(inner_xsec_mcl_y_nondim), cas.diff(nondim_chordwise_coordinates)) - inner_xsec.twist * np.pi / 180
                outer_xsec_mcl_angle = cas.atan2(cas.diff(outer_xsec_mcl_y_nondim), cas.diff(nondim_chordwise_coordinates)) - outer_xsec.twist * np.pi / 180
                effective_twist_axis = outer_xsec_xyz_le - inner_xsec_xyz_le
                effective_twist_axis[0] = 0.0
                n_spanwise_coordinates = inner_xsec.spanwise_panels + 1
                if inner_xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                elif inner_xsec.spanwise_spacing == 'cosine':
                    nondim_spanwise_coordinates = np_cosspace(0, 1, n_spanwise_coordinates)
                else:
                    raise Exception('Bad init_val of section.spanwise_spacing!')
                for chord_index in range(wing.chordwise_panels):
                    for span_index in range(inner_xsec.spanwise_panels):
                        nondim_chordwise_coordinate = nondim_chordwise_coordinates[chord_index]
                        nondim_spanwise_coordinate = nondim_spanwise_coordinates[span_index]
                        nondim_chordwise_coordinate_next = nondim_chordwise_coordinates[(chord_index + 1)]
                        nondim_spanwise_coordinate_next = nondim_spanwise_coordinates[(span_index + 1)]
                        front_left_vertices.append((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + inner_xsec_xyz_te * nondim_chordwise_coordinate) * (1 - nondim_spanwise_coordinate) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + outer_xsec_xyz_te * nondim_chordwise_coordinate) * nondim_spanwise_coordinate)
                        front_right_vertices.append((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + inner_xsec_xyz_te * nondim_chordwise_coordinate) * (1 - nondim_spanwise_coordinate_next) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + outer_xsec_xyz_te * nondim_chordwise_coordinate) * nondim_spanwise_coordinate_next)
                        back_left_vertices.append((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + inner_xsec_xyz_te * nondim_chordwise_coordinate_next) * (1 - nondim_spanwise_coordinate) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + outer_xsec_xyz_te * nondim_chordwise_coordinate_next) * nondim_spanwise_coordinate)
                        back_right_vertices.append((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + inner_xsec_xyz_te * nondim_chordwise_coordinate_next) * (1 - nondim_spanwise_coordinate_next) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + outer_xsec_xyz_te * nondim_chordwise_coordinate_next) * nondim_spanwise_coordinate_next)
                        is_trailing_edge.append(chord_index == wing.chordwise_panels - 1)
                        angle = inner_xsec_mcl_angle[chord_index] * (1 - nondim_spanwise_coordinate) + inner_xsec_mcl_angle[chord_index] * nondim_spanwise_coordinate
                        rot = angle_axis_rotation_matrix(-angle - np.pi / 2, effective_twist_axis)
                        normal_directions.append(rot @ cas.vertcat(1, 0, 0))

                if wing.symmetric:
                    inner_xsec = wing.xsecs[section_num]
                    outer_xsec = wing.xsecs[(section_num + 1)]
                    if inner_xsec.control_surface_type == 'symmetric':
                        inner_airfoil = inner_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                          hinge_point_x=(inner_xsec.control_surface_hinge_point))
                        outer_airfoil = outer_xsec.airfoil.add_control_surface(deflection=(inner_xsec.control_surface_deflection),
                          hinge_point_x=(inner_xsec.control_surface_hinge_point))
                    elif inner_xsec.control_surface_type == 'asymmetric':
                        inner_airfoil = inner_xsec.airfoil.add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point_x=(inner_xsec.control_surface_hinge_point))
                        outer_airfoil = outer_xsec.airfoil.add_control_surface(deflection=(-inner_xsec.control_surface_deflection),
                          hinge_point_x=(inner_xsec.control_surface_hinge_point))
                    else:
                        raise ValueError('Invalid input for control_surface_type!')
                    inner_xsec_mcl_y_nondim = inner_airfoil.local_camber(nondim_chordwise_coordinates)
                    outer_xsec_mcl_y_nondim = outer_airfoil.local_camber(nondim_chordwise_coordinates)
                    inner_xsec_mcl_angle = cas.atan2(cas.diff(inner_xsec_mcl_y_nondim), cas.diff(nondim_chordwise_coordinates)) - inner_xsec.twist * np.pi / 180
                    outer_xsec_mcl_angle = cas.atan2(cas.diff(outer_xsec_mcl_y_nondim), cas.diff(nondim_chordwise_coordinates)) - outer_xsec.twist * np.pi / 180
                    effective_twist_axis = outer_xsec_xyz_le - inner_xsec_xyz_le
                    effective_twist_axis[0] = 0.0
                    n_spanwise_coordinates = inner_xsec.spanwise_panels + 1
                    if inner_xsec.spanwise_spacing == 'uniform':
                        nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                    elif inner_xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = np_cosspace(0, 1, n_spanwise_coordinates)
                    else:
                        raise Exception('Bad init_val of section.spanwise_spacing!')
                    for chord_index in range(wing.chordwise_panels):
                        for span_index in range(inner_xsec.spanwise_panels):
                            nondim_chordwise_coordinate = nondim_chordwise_coordinates[chord_index]
                            nondim_spanwise_coordinate = nondim_spanwise_coordinates[span_index]
                            nondim_chordwise_coordinate_next = nondim_chordwise_coordinates[(chord_index + 1)]
                            nondim_spanwise_coordinate_next = nondim_spanwise_coordinates[(span_index + 1)]
                            front_right_vertices.append(reflect_over_XZ_plane((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + inner_xsec_xyz_te * nondim_chordwise_coordinate) * (1 - nondim_spanwise_coordinate) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + outer_xsec_xyz_te * nondim_chordwise_coordinate) * nondim_spanwise_coordinate))
                            front_left_vertices.append(reflect_over_XZ_plane((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + inner_xsec_xyz_te * nondim_chordwise_coordinate) * (1 - nondim_spanwise_coordinate_next) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate) + outer_xsec_xyz_te * nondim_chordwise_coordinate) * nondim_spanwise_coordinate_next))
                            back_right_vertices.append(reflect_over_XZ_plane((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + inner_xsec_xyz_te * nondim_chordwise_coordinate_next) * (1 - nondim_spanwise_coordinate) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + outer_xsec_xyz_te * nondim_chordwise_coordinate_next) * nondim_spanwise_coordinate))
                            back_left_vertices.append(reflect_over_XZ_plane((inner_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + inner_xsec_xyz_te * nondim_chordwise_coordinate_next) * (1 - nondim_spanwise_coordinate_next) + (outer_xsec_xyz_le * (1 - nondim_chordwise_coordinate_next) + outer_xsec_xyz_te * nondim_chordwise_coordinate_next) * nondim_spanwise_coordinate_next))
                            is_trailing_edge.append(chord_index == wing.chordwise_panels - 1)
                            angle = inner_xsec_mcl_angle[chord_index] * (1 - nondim_spanwise_coordinate) + inner_xsec_mcl_angle[chord_index] * nondim_spanwise_coordinate
                            rot = angle_axis_rotation_matrix(-angle - np.pi / 2, effective_twist_axis)
                            normal_directions.append(reflect_over_XZ_plane(rot @ cas.vertcat(1, 0, 0)))

        self.front_left_vertices = cas.MX(cas.transpose((cas.horzcat)(*front_left_vertices)))
        self.front_right_vertices = cas.MX(cas.transpose((cas.horzcat)(*front_right_vertices)))
        self.back_left_vertices = cas.MX(cas.transpose((cas.horzcat)(*back_left_vertices)))
        self.back_right_vertices = cas.MX(cas.transpose((cas.horzcat)(*back_right_vertices)))
        self.normal_directions = cas.MX(cas.transpose((cas.horzcat)(*normal_directions)))
        self.is_trailing_edge = is_trailing_edge
        diag1 = self.front_right_vertices - self.back_left_vertices
        diag2 = self.front_left_vertices - self.back_right_vertices
        cross = cas.cross(diag1, diag2)
        cross_norm = cas.sqrt(cross[:, 0] ** 2 + cross[:, 1] ** 2 + cross[:, 2] ** 2)
        self.areas = cross_norm / 2
        self.left_vortex_vertices = 0.75 * self.front_left_vertices + 0.25 * self.back_left_vertices
        self.right_vortex_vertices = 0.75 * self.front_right_vertices + 0.25 * self.back_right_vertices
        self.vortex_centers = (self.left_vortex_vertices + self.right_vortex_vertices) / 2
        self.vortex_bound_leg = self.right_vortex_vertices - self.left_vortex_vertices
        self.collocation_points = 0.5 * (0.25 * self.front_left_vertices + 0.75 * self.back_left_vertices) + 0.5 * (0.25 * self.front_right_vertices + 0.75 * self.back_right_vertices)
        self.n_panels = self.collocation_points.shape[0]
        if self.verbose:
            print('Meshing complete!')

    def setup_geometry(self):
        if self.verbose:
            print('Calculating the collocation influence matrix...')
        self.Vij_collocations_x, self.Vij_collocations_y, self.Vij_collocations_z = self.calculate_Vij(self.collocation_points)
        self.AIC = self.Vij_collocations_x * self.normal_directions[:, 0] + self.Vij_collocations_y * self.normal_directions[:, 1] + self.Vij_collocations_z * self.normal_directions[:, 2]
        if self.verbose:
            print('Calculating the vortex center influence matrix...')
        self.Vij_centers_x, self.Vij_centers_y, self.Vij_centers_z = self.calculate_Vij(self.vortex_centers)

    def setup_operating_point(self):
        if self.verbose:
            print('Calculating the freestream influence...')
        self.steady_freestream_velocity = self.op_point.compute_freestream_velocity_geometry_axes()
        self.rotation_freestream_velocities = self.op_point.compute_rotation_velocity_geometry_axes(self.collocation_points)
        self.freestream_velocities = cas.transpose(self.steady_freestream_velocity + cas.transpose(self.rotation_freestream_velocities))
        self.freestream_influences = self.freestream_velocities[:, 0] * self.normal_directions[:, 0] + self.freestream_velocities[:, 1] * self.normal_directions[:, 1] + self.freestream_velocities[:, 2] * self.normal_directions[:, 2]

    def calculate_vortex_strengths(self):
        if self.verbose:
            print('Calculating vortex strengths...')
        self.vortex_strengths = cas.solve(self.AIC, -self.freestream_influences)

    def calculate_forces(self):
        if self.verbose:
            print('Calculating forces on each panel...')
        Vi_x = self.Vij_centers_x @ self.vortex_strengths + self.freestream_velocities[:, 0]
        Vi_y = self.Vij_centers_y @ self.vortex_strengths + self.freestream_velocities[:, 1]
        Vi_z = self.Vij_centers_z @ self.vortex_strengths + self.freestream_velocities[:, 2]
        Vi = cas.horzcat(Vi_x, Vi_y, Vi_z)
        density = self.op_point.density
        Vi_cross_li = cas.horzcat(Vi_y * self.vortex_bound_leg[:, 2] - Vi_z * self.vortex_bound_leg[:, 1], Vi_z * self.vortex_bound_leg[:, 0] - Vi_x * self.vortex_bound_leg[:, 2], Vi_x * self.vortex_bound_leg[:, 1] - Vi_y * self.vortex_bound_leg[:, 0])
        self.forces_geometry = density * Vi_cross_li * self.vortex_strengths
        if self.verbose:
            print('Calculating total forces and moments...')
        self.force_total_geometry = cas.vertcat(cas.sum1(self.forces_geometry[:, 0]), cas.sum1(self.forces_geometry[:, 1]), cas.sum1(self.forces_geometry[:, 2]))
        self.force_total_wind = cas.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.force_total_geometry
        self.moments_geometry = cas.cross(cas.transpose(cas.transpose(self.vortex_centers) - self.airplane.xyz_ref), self.forces_geometry)
        self.Mtotal_geometry = cas.vertcat(cas.sum1(self.moments_geometry[:, 0]), cas.sum1(self.moments_geometry[:, 1]), cas.sum1(self.moments_geometry[:, 2]))
        self.moment_total_wind = cas.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ self.Mtotal_geometry
        self.lift_force = -self.force_total_wind[2]
        self.drag_force_induced = -self.force_total_wind[0]
        self.side_force = self.force_total_wind[1]
        q = self.op_point.dynamic_pressure()
        s_ref = self.airplane.s_ref
        b_ref = self.airplane.b_ref
        c_ref = self.airplane.c_ref
        self.CL = self.lift_force / q / s_ref
        self.CDi = self.drag_force_induced / q / s_ref
        self.CY = self.side_force / q / s_ref
        self.Cl = self.moment_total_wind[0] / q / s_ref / b_ref
        self.Cm = self.moment_total_wind[1] / q / s_ref / c_ref
        self.Cn = self.moment_total_wind[2] / q / s_ref / b_ref
        self.CL_over_CDi = cas.if_else(self.CDi == 0, 0, self.CL / self.CDi)

    def calculate_Vij(self, points, align_trailing_vortices_with_freestream=False):
        n_points = points.shape[0]
        a_x = points[:, 0] - cas.repmat(cas.transpose(self.left_vortex_vertices[:, 0]), n_points, 1)
        a_y = points[:, 1] - cas.repmat(cas.transpose(self.left_vortex_vertices[:, 1]), n_points, 1)
        a_z = points[:, 2] - cas.repmat(cas.transpose(self.left_vortex_vertices[:, 2]), n_points, 1)
        b_x = points[:, 0] - cas.repmat(cas.transpose(self.right_vortex_vertices[:, 0]), n_points, 1)
        b_y = points[:, 1] - cas.repmat(cas.transpose(self.right_vortex_vertices[:, 1]), n_points, 1)
        b_z = points[:, 2] - cas.repmat(cas.transpose(self.right_vortex_vertices[:, 2]), n_points, 1)
        if align_trailing_vortices_with_freestream:
            freestream_direction = self.op_point.compute_freestream_direction_geometry_axes()
            u_x = freestream_direction[0]
            u_y = freestream_direction[1]
            u_z = freestream_direction[2]
        else:
            u_x = 1
            u_y = 0
            u_z = 0
        a_cross_b_x = a_y * b_z - a_z * b_y
        a_cross_b_y = a_z * b_x - a_x * b_z
        a_cross_b_z = a_x * b_y - a_y * b_x
        a_dot_b = a_x * b_x + a_y * b_y + a_z * b_z
        a_cross_u_x = a_y * u_z - a_z * u_y
        a_cross_u_y = a_z * u_x - a_x * u_z
        a_cross_u_z = a_x * u_y - a_y * u_x
        a_dot_u = a_x * u_x + a_y * u_y + a_z * u_z
        b_cross_u_x = b_y * u_z - b_z * u_y
        b_cross_u_y = b_z * u_x - b_x * u_z
        b_cross_u_z = b_x * u_y - b_y * u_x
        b_dot_u = b_x * u_x + b_y * u_y + b_z * u_z
        norm_a = cas.sqrt(a_x ** 2 + a_y ** 2 + a_z ** 2)
        norm_b = cas.sqrt(b_x ** 2 + b_y ** 2 + b_z ** 2)
        norm_a_inv = 1 / norm_a
        norm_b_inv = 1 / norm_b
        a_dot_b -= 1e-08
        term1 = (norm_a_inv + norm_b_inv) / (norm_a * norm_b + a_dot_b)
        term2 = norm_a_inv / (norm_a - a_dot_u)
        term3 = norm_b_inv / (norm_b - b_dot_u)
        Vij_x = 1 / (4 * np.pi) * (a_cross_b_x * term1 + a_cross_u_x * term2 - b_cross_u_x * term3)
        Vij_y = 1 / (4 * np.pi) * (a_cross_b_y * term1 + a_cross_u_y * term2 - b_cross_u_y * term3)
        Vij_z = 1 / (4 * np.pi) * (a_cross_b_z * term1 + a_cross_u_z * term2 - b_cross_u_z * term3)
        return (
         Vij_x, Vij_y, Vij_z)

    def get_induced_velocity_at_point(self, point):
        if not self.opti.return_status() == 'Solve_Succeeded':
            print('WARNING: This method should only be used after a solution has been found!!!\nRunning anyway for debugging purposes - this is likely to not work.')
        Vij_x, Vij_y, Vij_z = self.calculate_Vij(point)
        Vi_x = Vij_x @ self.vortex_strengths
        Vi_y = Vij_y @ self.vortex_strengths
        Vi_z = Vij_z @ self.vortex_strengths
        get = lambda x: self.opti.debug.value(x)
        Vi_x = get(Vi_x)
        Vi_y = get(Vi_y)
        Vi_z = get(Vi_z)
        Vi = np.vstack((Vi_x, Vi_y, Vi_z)).T
        return Vi

    def get_velocity_at_point(self, point):
        Vi = self.get_induced_velocity_at_point(point)
        freestream = self.op_point.compute_freestream_velocity_geometry_axes()
        V = cas.transpose(cas.transpose(Vi) + freestream)
        return V

    def calculate_streamlines(self, seed_points=None, n_steps=100, length=None):
        if length is None:
            length = self.airplane.c_ref * 5
        if seed_points is None:
            seed_points = (self.back_left_vertices + self.back_right_vertices) / 2
        length_per_step = length / n_steps
        streamlines = [
         seed_points]
        for step_num in range(1, n_steps):
            update_amount = self.get_velocity_at_point(streamlines[(-1)])
            norm_update_amount = cas.sqrt(update_amount[:, 0] ** 2 + update_amount[:, 1] ** 2 + update_amount[:, 2] ** 2)
            update_amount = length_per_step * update_amount / norm_update_amount
            streamlines.append(streamlines[(-1)] + update_amount)

        self.streamlines = streamlines

    def draw(self, data_to_plot=None, data_name=None, show=True, draw_streamlines=True, recalculate_streamlines=False):
        """
        Draws the solution. Note: Must be called on a SOLVED AeroProblem object.
        To solve an AeroProblem, use opti.solve(). To substitute a solved solution, use ap = ap.substitute_solution(sol).
        :return:
        """
        if self.verbose:
            print('Drawing...')
        else:
            if self.verbose:
                if not self.opti.return_status() == 'Solve_Succeeded':
                    print('WARNING: This method should only be used after a solution has been found!\nRunning anyway for debugging purposes - this is likely to not work...')
            get = lambda x: self.opti.debug.value(x)
            front_left_vertices = get(self.front_left_vertices)
            front_right_vertices = get(self.front_right_vertices)
            back_left_vertices = get(self.back_left_vertices)
            back_right_vertices = get(self.back_right_vertices)
            left_vortex_vertices = get(self.left_vortex_vertices)
            right_vortex_vertices = get(self.right_vortex_vertices)
            self.vortex_strengths = get(self.vortex_strengths)
            try:
                data_to_plot = get(data_to_plot)
            except NotImplementedError:
                pass

        if data_to_plot is None:
            data_name = 'Vortex Strengths'
            data_to_plot = get(self.vortex_strengths)
        fig = Figure3D()
        for index in range(len(front_left_vertices)):
            fig.add_quad(points=[
             front_left_vertices[index, :],
             front_right_vertices[index, :],
             back_right_vertices[index, :],
             back_left_vertices[index, :]],
              intensity=(data_to_plot[index]),
              outline=True)

        for fuse_id in range(len(self.airplane.fuselages)):
            fuse = self.airplane.fuselages[fuse_id]
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
                      intensity=0,
                      mirror=(fuse.symmetric))

        if draw_streamlines:
            if not hasattr(self, 'streamlines') or recalculate_streamlines:
                if self.verbose:
                    print('Calculating streamlines...')
                is_trailing_edge = np.array((self.is_trailing_edge), dtype=bool)
                seed_points = (back_left_vertices[is_trailing_edge] + back_right_vertices[is_trailing_edge]) / 2
                self.calculate_streamlines(seed_points=seed_points)
            if self.verbose:
                print('Parsing streamline data...')
            n_streamlines = self.streamlines[0].shape[0]
            n_timesteps = len(self.streamlines)
            for streamlines_num in range(n_streamlines):
                streamline = [self.streamlines[ts][streamlines_num, :] for ts in range(n_timesteps)]
                fig.add_streamline(points=streamline)

        return fig.draw(show=show,
          colorbar_title=data_name)