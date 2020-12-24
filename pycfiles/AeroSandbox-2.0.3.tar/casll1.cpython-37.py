# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\aerodynamics\casll1.py
# Compiled at: 2020-04-18 12:07:31
# Size of source mod 2**32: 49853 bytes
from aerosandbox.aerodynamics.aerodynamics import *
from aerosandbox.geometry import *
from aerosandbox.visualization import Figure3D

class Casll1(AeroProblem):

    def __init__(self, airplane, op_point, opti, run_setup=True):
        super().__init__(airplane, op_point)
        self.opti = opti
        if run_setup:
            self.setup()

    def setup--- This code section failed: ---

 L.  31         0  LOAD_FAST                'verbose'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               verbose

 L.  32         6  LOAD_FAST                'self'
                8  LOAD_ATTR                verbose
               10  POP_JUMP_IF_FALSE    20  'to 20'

 L.  33        12  LOAD_GLOBAL              print
               14  LOAD_STR                 '\n Initializing CasLL1 Analysis...\n-----------------------'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  POP_TOP          
             20_0  COME_FROM            10  '10'

 L.  35        20  LOAD_FAST                'run_symmetric_if_possible'
               22  POP_JUMP_IF_FALSE   148  'to 148'

 L.  36        24  SETUP_EXCEPT         76  'to 76'

 L.  38        26  LOAD_FAST                'self'
               28  LOAD_ATTR                op_point
               30  LOAD_ATTR                beta
               32  LOAD_CONST               0
               34  COMPARE_OP               ==
               36  JUMP_IF_FALSE_OR_POP    70  'to 70'

 L.  39        38  LOAD_FAST                'self'
               40  LOAD_ATTR                op_point
               42  LOAD_ATTR                p
               44  LOAD_CONST               0
               46  COMPARE_OP               ==
               48  JUMP_IF_FALSE_OR_POP    70  'to 70'

 L.  40        50  LOAD_FAST                'self'
               52  LOAD_ATTR                op_point
               54  LOAD_ATTR                r
               56  LOAD_CONST               0
               58  COMPARE_OP               ==
               60  JUMP_IF_FALSE_OR_POP    70  'to 70'

 L.  41        62  LOAD_FAST                'self'
               64  LOAD_ATTR                airplane
               66  LOAD_METHOD              is_symmetric
               68  CALL_METHOD_0         0  '0 positional arguments'
             70_0  COME_FROM            60  '60'
             70_1  COME_FROM            48  '48'
             70_2  COME_FROM            36  '36'
               70  STORE_FAST               'symmetric_problem'
               72  POP_BLOCK        
               74  JUMP_FORWARD        100  'to 100'
             76_0  COME_FROM_EXCEPT     24  '24'

 L.  43        76  DUP_TOP          
               78  LOAD_GLOBAL              RuntimeError
               80  COMPARE_OP               exception-match
               82  POP_JUMP_IF_FALSE    98  'to 98'
               84  POP_TOP          
               86  POP_TOP          
               88  POP_TOP          

 L.  44        90  LOAD_CONST               False
               92  STORE_FAST               'symmetric_problem'
               94  POP_EXCEPT       
               96  JUMP_FORWARD        100  'to 100'
             98_0  COME_FROM            82  '82'
               98  END_FINALLY      
            100_0  COME_FROM            96  '96'
            100_1  COME_FROM            74  '74'

 L.  46       100  LOAD_FAST                'symmetric_problem'
              102  POP_JUMP_IF_FALSE   126  'to 126'

 L.  47       104  LOAD_CONST               True
              106  LOAD_FAST                'self'
              108  STORE_ATTR               symmetric_problem

 L.  48       110  LOAD_FAST                'self'
              112  LOAD_ATTR                verbose
              114  POP_JUMP_IF_FALSE   146  'to 146'

 L.  49       116  LOAD_GLOBAL              print
              118  LOAD_STR                 'Symmetry confirmed; running as symmetric problem...'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  POP_TOP          
              124  JUMP_ABSOLUTE       168  'to 168'
            126_0  COME_FROM           102  '102'

 L.  51       126  LOAD_CONST               False
              128  LOAD_FAST                'self'
              130  STORE_ATTR               symmetric_problem

 L.  52       132  LOAD_FAST                'self'
              134  LOAD_ATTR                verbose
              136  POP_JUMP_IF_FALSE   168  'to 168'

 L.  53       138  LOAD_GLOBAL              print

 L.  54       140  LOAD_STR                 'Problem appears to be asymmetric, so a symmetric solve is not possible; running as asymmetric problem...'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  POP_TOP          
            146_0  COME_FROM           114  '114'
              146  JUMP_FORWARD        168  'to 168'
            148_0  COME_FROM            22  '22'

 L.  56       148  LOAD_CONST               False
              150  LOAD_FAST                'self'
              152  STORE_ATTR               symmetric_problem

 L.  57       154  LOAD_FAST                'self'
              156  LOAD_ATTR                verbose
              158  POP_JUMP_IF_FALSE   168  'to 168'

 L.  58       160  LOAD_GLOBAL              print
              162  LOAD_STR                 'Running as asymmetric problem...'
              164  CALL_FUNCTION_1       1  '1 positional argument'
              166  POP_TOP          
            168_0  COME_FROM           158  '158'
            168_1  COME_FROM           146  '146'
            168_2  COME_FROM           136  '136'

 L.  60       168  LOAD_FAST                'self'
              170  LOAD_ATTR                verbose
              172  POP_JUMP_IF_FALSE   182  'to 182'

 L.  61       174  LOAD_GLOBAL              print
              176  LOAD_STR                 'Setting up casLL1 calculation...'
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  POP_TOP          
            182_0  COME_FROM           172  '172'

 L.  63       182  LOAD_FAST                'self'
              184  LOAD_METHOD              make_panels
              186  CALL_METHOD_0         0  '0 positional arguments'
              188  POP_TOP          

 L.  64       190  LOAD_FAST                'self'
              192  LOAD_METHOD              setup_geometry
              194  CALL_METHOD_0         0  '0 positional arguments'
              196  POP_TOP          

 L.  65       198  LOAD_FAST                'self'
              200  LOAD_METHOD              setup_operating_point
              202  CALL_METHOD_0         0  '0 positional arguments'
              204  POP_TOP          

 L.  66       206  LOAD_FAST                'self'
              208  LOAD_METHOD              calculate_vortex_strengths
              210  CALL_METHOD_0         0  '0 positional arguments'
              212  POP_TOP          

 L.  67       214  LOAD_FAST                'self'
              216  LOAD_METHOD              calculate_forces
              218  CALL_METHOD_0         0  '0 positional arguments'
              220  POP_TOP          

 L.  69       222  LOAD_FAST                'self'
              224  LOAD_ATTR                verbose
              226  POP_JUMP_IF_FALSE   236  'to 236'

 L.  70       228  LOAD_GLOBAL              print
              230  LOAD_STR                 'casLL1 setup complete! Ready to pass into the solver...'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  POP_TOP          
            236_0  COME_FROM           226  '226'

Parse error at or near `POP_TOP' instruction at offset 234

    def make_panels(self):
        if self.verbose:
            print('Meshing...')
        front_left_vertices = []
        front_right_vertices = []
        back_left_vertices = []
        back_right_vertices = []
        CL_functions = []
        CDp_functions = []
        Cm_functions = []
        wing_id = []
        for wing_num in range(len(self.airplane.wings)):
            wing = self.airplane.wings[wing_num]
            for section_num in range(len(wing.xsecs) - 1):
                inner_xsec = wing.xsecs[section_num]
                outer_xsec = wing.xsecs[(section_num + 1)]
                inner_xsec_xyz_le = inner_xsec.xyz_le + wing.xyz_le
                inner_xsec_xyz_te = inner_xsec.xyz_te() + wing.xyz_le
                outer_xsec_xyz_le = outer_xsec.xyz_le + wing.xyz_le
                outer_xsec_xyz_te = outer_xsec.xyz_te() + wing.xyz_le
                n_spanwise_coordinates = inner_xsec.spanwise_panels + 1
                if inner_xsec.spanwise_spacing == 'uniform':
                    nondim_spanwise_coordinates = np.linspace(0, 1, n_spanwise_coordinates)
                else:
                    if inner_xsec.spanwise_spacing == 'cosine':
                        nondim_spanwise_coordinates = np_cosspace(0, 1, n_spanwise_coordinates)
                    else:
                        raise Exception('Bad init_val of section.spanwise_spacing!')
                for span_index in range(inner_xsec.spanwise_panels):
                    nondim_spanwise_coordinate = nondim_spanwise_coordinates[span_index]
                    nondim_spanwise_coordinate_next = nondim_spanwise_coordinates[(span_index + 1)]
                    front_left_vertex = inner_xsec_xyz_le * (1 - nondim_spanwise_coordinate) + outer_xsec_xyz_le * nondim_spanwise_coordinate
                    front_right_vertex = inner_xsec_xyz_le * (1 - nondim_spanwise_coordinate_next) + outer_xsec_xyz_le * nondim_spanwise_coordinate_next
                    back_left_vertex = inner_xsec_xyz_te * (1 - nondim_spanwise_coordinate) + outer_xsec_xyz_te * nondim_spanwise_coordinate
                    back_right_vertex = inner_xsec_xyz_te * (1 - nondim_spanwise_coordinate_next) + outer_xsec_xyz_te * nondim_spanwise_coordinate_next
                    front_left_vertices.append(front_left_vertex)
                    front_right_vertices.append(front_right_vertex)
                    back_left_vertices.append(back_left_vertex)
                    back_right_vertices.append(back_right_vertex)
                    CL_functions.append(lambda alpha, Re, mach, inner_xsec=inner_xsec, outer_xsec=outer_xsec, nondim_spanwise_coordinate=nondim_spanwise_coordinate: inner_xsec.airfoil.CL_function(alpha=alpha,
                      Re=Re,
                      mach=mach,
                      deflection=(inner_xsec.control_surface_deflection)) * (1 - nondim_spanwise_coordinate) + outer_xsec.airfoil.CL_function(alpha=alpha,
                      Re=Re,
                      mach=mach,
                      deflection=(inner_xsec.control_surface_deflection)) * nondim_spanwise_coordinate)
                    CDp_functions.append(lambda alpha, Re, mach, inner_xsec=inner_xsec, outer_xsec=outer_xsec, nondim_spanwise_coordinate=nondim_spanwise_coordinate: inner_xsec.airfoil.CDp_function(alpha=alpha,
                      Re=Re,
                      mach=mach,
                      deflection=(inner_xsec.control_surface_deflection)) * (1 - nondim_spanwise_coordinate) + outer_xsec.airfoil.CDp_function(alpha=alpha,
                      Re=Re,
                      mach=mach,
                      deflection=(inner_xsec.control_surface_deflection)) * nondim_spanwise_coordinate)
                    Cm_functions.append(lambda alpha, Re, mach, inner_xsec=inner_xsec, outer_xsec=outer_xsec, nondim_spanwise_coordinate=nondim_spanwise_coordinate: inner_xsec.airfoil.Cm_function(alpha=alpha,
                      Re=Re,
                      mach=mach,
                      deflection=(inner_xsec.control_surface_deflection)) * (1 - nondim_spanwise_coordinate) + outer_xsec.airfoil.Cm_function(alpha=alpha,
                      Re=Re,
                      mach=mach,
                      deflection=(inner_xsec.control_surface_deflection)) * nondim_spanwise_coordinate)
                    wing_id.append(wing_num)
                    if wing.symmetric:
                        self.symmetric_problem or front_right_vertices.append(reflect_over_XZ_plane(front_left_vertex))
                        front_left_vertices.append(reflect_over_XZ_plane(front_right_vertex))
                        back_right_vertices.append(reflect_over_XZ_plane(back_left_vertex))
                        back_left_vertices.append(reflect_over_XZ_plane(back_right_vertex))
                        CL_functions.append(lambda alpha, Re, mach, inner_xsec=inner_xsec, outer_xsec=outer_xsec, nondim_spanwise_coordinate=nondim_spanwise_coordinate: inner_xsec.airfoil.CL_function(alpha=alpha,
                          Re=Re,
                          mach=mach,
                          deflection=(-inner_xsec.control_surface_deflection if inner_xsec.control_surface_type == 'asymmetric' else inner_xsec.control_surface_deflection)) * (1 - nondim_spanwise_coordinate) + outer_xsec.airfoil.CL_function(alpha=alpha,
                          Re=Re,
                          mach=mach,
                          deflection=(-inner_xsec.control_surface_deflection if inner_xsec.control_surface_type == 'asymmetric' else inner_xsec.control_surface_deflection)) * nondim_spanwise_coordinate)
                        CDp_functions.append(lambda alpha, Re, mach, inner_xsec=inner_xsec, outer_xsec=outer_xsec, nondim_spanwise_coordinate=nondim_spanwise_coordinate: inner_xsec.airfoil.CDp_function(alpha=alpha,
                          Re=Re,
                          mach=mach,
                          deflection=(-inner_xsec.control_surface_deflection if inner_xsec.control_surface_type == 'asymmetric' else inner_xsec.control_surface_deflection)) * (1 - nondim_spanwise_coordinate) + outer_xsec.airfoil.CDp_function(alpha=alpha,
                          Re=Re,
                          mach=mach,
                          deflection=(-inner_xsec.control_surface_deflection if inner_xsec.control_surface_type == 'asymmetric' else inner_xsec.control_surface_deflection)) * nondim_spanwise_coordinate)
                        Cm_functions.append(lambda alpha, Re, mach, inner_xsec=inner_xsec, outer_xsec=outer_xsec, nondim_spanwise_coordinate=nondim_spanwise_coordinate: inner_xsec.airfoil.Cm_function(alpha=alpha,
                          Re=Re,
                          mach=mach,
                          deflection=(-inner_xsec.control_surface_deflection if inner_xsec.control_surface_type == 'asymmetric' else inner_xsec.control_surface_deflection)) * (1 - nondim_spanwise_coordinate) + outer_xsec.airfoil.Cm_function(alpha=alpha,
                          Re=Re,
                          mach=mach,
                          deflection=(-inner_xsec.control_surface_deflection if inner_xsec.control_surface_type == 'asymmetric' else inner_xsec.control_surface_deflection)) * nondim_spanwise_coordinate)
                        wing_id.append(wing_num)

        self.front_left_vertices = cas.transpose((cas.horzcat)(*front_left_vertices))
        self.front_right_vertices = cas.transpose((cas.horzcat)(*front_right_vertices))
        self.back_left_vertices = cas.transpose((cas.horzcat)(*back_left_vertices))
        self.back_right_vertices = cas.transpose((cas.horzcat)(*back_right_vertices))
        self.CL_functions = CL_functions
        self.CDp_functions = CDp_functions
        self.Cm_functions = Cm_functions
        self.wing_id = wing_id
        if self.symmetric_problem:
            self.use_symmetry = [self.airplane.wings[i].symmetric for i in self.wing_id]
        self.left_vortex_vertices = 0.75 * self.front_left_vertices + 0.25 * self.back_left_vertices
        self.right_vortex_vertices = 0.75 * self.front_right_vertices + 0.25 * self.back_right_vertices
        self.vortex_centers = (self.left_vortex_vertices + self.right_vortex_vertices) / 2
        self.vortex_bound_leg = self.right_vortex_vertices - self.left_vortex_vertices
        diag1 = self.front_right_vertices - self.back_left_vertices
        diag2 = self.front_left_vertices - self.back_right_vertices
        cross = cas.cross(diag1, diag2)
        cross_norm = cas.sqrt(cross[:, 0] ** 2 + cross[:, 1] ** 2 + cross[:, 2] ** 2)
        self.areas = cross_norm / 2
        self.normal_directions = cross / cross_norm
        chord_vectors = (self.back_left_vertices + self.back_right_vertices) / 2 - (self.front_left_vertices + self.front_right_vertices) / 2
        self.chords = cas.sqrt(chord_vectors[:, 0] ** 2 + chord_vectors[:, 1] ** 2 + chord_vectors[:, 2] ** 2)
        self.chordwise_directions = chord_vectors / self.chords
        self.wing_directions = self.vortex_bound_leg / cas.sqrt(self.vortex_bound_leg[:, 0] ** 2 + self.vortex_bound_leg[:, 1] ** 2 + self.vortex_bound_leg[:, 2] ** 2)
        self.local_forward_directions = cas.cross(self.normal_directions, self.wing_directions)
        self.n_panels = self.front_left_vertices.shape[0]
        fuse_centerline_points = []
        fuse_radii = []
        for fuse_num in range(len(self.airplane.fuselages)):
            fuse = self.airplane.fuselages[fuse_num]
            this_fuse_centerline_points = [xsec.xyz_c + fuse.xyz_le for xsec in fuse.xsecs]
            this_fuse_centerline_points = cas.transpose((cas.horzcat)(*this_fuse_centerline_points))
            this_fuse_radii = [xsec.radius for xsec in fuse.xsecs]
            this_fuse_radii = (cas.vertcat)(*this_fuse_radii)
            fuse_centerline_points.append(this_fuse_centerline_points)
            fuse_radii.append(this_fuse_radii)
            if self.symmetric_problem or fuse.symmetric:
                fuse_centerline_points.append(reflect_over_XZ_plane(this_fuse_centerline_points))
                fuse_radii.append(this_fuse_radii)

        self.fuse_centerline_points = fuse_centerline_points
        self.fuse_radii = fuse_radii
        if self.verbose:
            print('Meshing complete!')

    def setup_geometry(self):
        if self.verbose:
            print('Calculating the vortex center velocity influence matrix...')
        self.Vij_x, self.Vij_y, self.Vij_z = self.calculate_Vij(self.vortex_centers)
        if self.verbose:
            print('Calculating fuselage influences...')
        self.beta = cas.sqrt(1 - self.op_point.mach)
        self.fuselage_velocities = self.calculate_fuselage_influences(self.vortex_centers)

    def setup_operating_point(self):
        if self.verbose:
            print('Calculating the freestream influence...')
        self.steady_freestream_velocity = self.op_point.compute_freestream_velocity_geometry_axes()
        self.rotation_freestream_velocities = self.op_point.compute_rotation_velocity_geometry_axes(self.vortex_centers)
        self.freestream_velocities = cas.transpose(self.steady_freestream_velocity + cas.transpose(self.rotation_freestream_velocities))

    def calculate_vortex_strengths(self):
        if self.verbose:
            print('Calculating vortex strengths...')
        self.vortex_strengths = self.opti.variable(self.n_panels)
        self.opti.set_initial(self.vortex_strengths, 0)
        self.induced_velocities = cas.horzcat(self.Vij_x @ self.vortex_strengths, self.Vij_y @ self.vortex_strengths, self.Vij_z @ self.vortex_strengths)
        self.velocities = self.induced_velocities + self.freestream_velocities + self.fuselage_velocities
        self.alpha_eff_perpendiculars = cas.atan2(self.velocities[:, 0] * self.normal_directions[:, 0] + self.velocities[:, 1] * self.normal_directions[:, 1] + self.velocities[:, 2] * self.normal_directions[:, 2], self.velocities[:, 0] * -self.local_forward_directions[:, 0] + self.velocities[:, 1] * -self.local_forward_directions[:, 1] + self.velocities[:, 2] * -self.local_forward_directions[:, 2]) * (180 / cas.pi)
        self.velocity_magnitudes = cas.sqrt(self.velocities[:, 0] ** 2 + self.velocities[:, 1] ** 2 + self.velocities[:, 2] ** 2)
        self.Res = self.op_point.density * self.velocity_magnitudes * self.chords / self.op_point.viscosity
        self.machs = [self.op_point.mach] * self.n_panels
        self.cos_sweeps = (self.velocities[:, 0] * -self.local_forward_directions[:, 0] + self.velocities[:, 1] * -self.local_forward_directions[:, 1] + self.velocities[:, 2] * -self.local_forward_directions[:, 2]) / self.velocity_magnitudes
        self.chord_perpendiculars = self.chords * self.cos_sweeps
        self.velocity_magnitude_perpendiculars = self.velocity_magnitudes * self.cos_sweeps
        self.Res_perpendicular = self.Res * self.cos_sweeps
        self.machs_perpendicular = self.machs * self.cos_sweeps
        CL_locals = [self.CL_functions[i](alpha=(self.alpha_eff_perpendiculars[i]), Re=(self.Res_perpendicular[i]), mach=(self.machs_perpendicular[i])) for i in range(self.n_panels)]
        CDp_locals = [self.CDp_functions[i](alpha=(self.alpha_eff_perpendiculars[i]), Re=(self.Res_perpendicular[i]), mach=(self.machs_perpendicular[i])) for i in range(self.n_panels)]
        Cm_locals = [self.Cm_functions[i](alpha=(self.alpha_eff_perpendiculars[i]), Re=(self.Res_perpendicular[i]), mach=(self.machs_perpendicular[i])) for i in range(self.n_panels)]
        self.CL_locals = (cas.vertcat)(*CL_locals)
        self.CDp_locals = (cas.vertcat)(*CDp_locals)
        self.Cm_locals = (cas.vertcat)(*Cm_locals)
        self.Vi_cross_li = cas.horzcat(self.velocities[:, 1] * self.vortex_bound_leg[:, 2] - self.velocities[:, 2] * self.vortex_bound_leg[:, 1], self.velocities[:, 2] * self.vortex_bound_leg[:, 0] - self.velocities[:, 0] * self.vortex_bound_leg[:, 2], self.velocities[:, 0] * self.vortex_bound_leg[:, 1] - self.velocities[:, 1] * self.vortex_bound_leg[:, 0])
        Vi_cross_li_magnitudes = cas.sqrt(self.Vi_cross_li[:, 0] ** 2 + self.Vi_cross_li[:, 1] ** 2 + self.Vi_cross_li[:, 2] ** 2)
        self.opti.subject_to([
         self.vortex_strengths * Vi_cross_li_magnitudes * 2 / self.velocity_magnitude_perpendiculars ** 2 / self.areas == self.CL_locals])

    def calculate_forces(self):
        if self.verbose:
            print('Calculating induced forces...')
        self.forces_inviscid_geometry = self.op_point.density * self.Vi_cross_li * self.vortex_strengths
        force_total_inviscid_geometry = cas.vertcat(cas.sum1(self.forces_inviscid_geometry[:, 0]), cas.sum1(self.forces_inviscid_geometry[:, 1]), cas.sum1(self.forces_inviscid_geometry[:, 2]))
        if self.symmetric_problem:
            forces_inviscid_geometry_from_symmetry = cas.if_else(self.use_symmetry, reflect_over_XZ_plane(self.forces_inviscid_geometry), 0)
            force_total_inviscid_geometry_from_symmetry = cas.vertcat(cas.sum1(forces_inviscid_geometry_from_symmetry[:, 0]), cas.sum1(forces_inviscid_geometry_from_symmetry[:, 1]), cas.sum1(forces_inviscid_geometry_from_symmetry[:, 2]))
            force_total_inviscid_geometry += force_total_inviscid_geometry_from_symmetry
        self.force_total_inviscid_wind = cas.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ force_total_inviscid_geometry
        if self.verbose:
            print('Calculating induced moments...')
        self.moments_inviscid_geometry = cas.cross(cas.transpose(cas.transpose(self.vortex_centers) - self.airplane.xyz_ref), self.forces_inviscid_geometry)
        moment_total_inviscid_geometry = cas.vertcat(cas.sum1(self.moments_inviscid_geometry[:, 0]), cas.sum1(self.moments_inviscid_geometry[:, 1]), cas.sum1(self.moments_inviscid_geometry[:, 2]))
        if self.symmetric_problem:
            moments_inviscid_geometry_from_symmetry = cas.if_else(self.use_symmetry, -reflect_over_XZ_plane(self.moments_inviscid_geometry), 0)
            moment_total_inviscid_geometry_from_symmetry = cas.vertcat(cas.sum1(moments_inviscid_geometry_from_symmetry[:, 0]), cas.sum1(moments_inviscid_geometry_from_symmetry[:, 1]), cas.sum1(moments_inviscid_geometry_from_symmetry[:, 2]))
            moment_total_inviscid_geometry += moment_total_inviscid_geometry_from_symmetry
        self.moment_total_inviscid_wind = cas.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ moment_total_inviscid_geometry
        if self.verbose:
            print('Calculating profile forces...')
        self.forces_profile_geometry = 0.5 * self.op_point.density * self.velocity_magnitudes * self.velocities * self.CDp_locals * self.areas
        force_total_profile_geometry = cas.vertcat(cas.sum1(self.forces_profile_geometry[:, 0]), cas.sum1(self.forces_profile_geometry[:, 1]), cas.sum1(self.forces_profile_geometry[:, 2]))
        if self.symmetric_problem:
            forces_profile_geometry_from_symmetry = cas.if_else(self.use_symmetry, reflect_over_XZ_plane(self.forces_profile_geometry), 0)
            force_total_profile_geometry_from_symmetry = cas.vertcat(cas.sum1(forces_profile_geometry_from_symmetry[:, 0]), cas.sum1(forces_profile_geometry_from_symmetry[:, 1]), cas.sum1(forces_profile_geometry_from_symmetry[:, 2]))
            force_total_profile_geometry += force_total_profile_geometry_from_symmetry
        self.force_total_profile_wind = cas.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ force_total_profile_geometry
        if self.verbose:
            print('Calculating profile moments...')
        self.moments_profile_geometry = cas.cross(cas.transpose(cas.transpose(self.vortex_centers) - self.airplane.xyz_ref), self.forces_profile_geometry)
        moment_total_profile_geometry = cas.vertcat(cas.sum1(self.moments_profile_geometry[:, 0]), cas.sum1(self.moments_profile_geometry[:, 1]), cas.sum1(self.moments_profile_geometry[:, 2]))
        if self.symmetric_problem:
            moments_profile_geometry_from_symmetry = cas.if_else(self.use_symmetry, -reflect_over_XZ_plane(self.moments_profile_geometry), 0)
            moment_total_profile_geometry_from_symmetry = cas.vertcat(cas.sum1(moments_profile_geometry_from_symmetry[:, 0]), cas.sum1(moments_profile_geometry_from_symmetry[:, 1]), cas.sum1(moments_profile_geometry_from_symmetry[:, 2]))
            moment_total_profile_geometry += moment_total_profile_geometry_from_symmetry
        self.moment_total_profile_wind = cas.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ moment_total_profile_geometry
        if self.verbose:
            print('Calculating pitching moments...')
        bound_leg_YZ = self.vortex_bound_leg
        bound_leg_YZ[:, 0] = 0
        self.moments_pitching_geometry = 0.5 * self.op_point.density * self.velocity_magnitudes ** 2 * self.Cm_locals * self.chords ** 2 * bound_leg_YZ
        moment_total_pitching_geometry = cas.vertcat(cas.sum1(self.moments_pitching_geometry[:, 0]), cas.sum1(self.moments_pitching_geometry[:, 1]), cas.sum1(self.moments_pitching_geometry[:, 2]))
        if self.symmetric_problem:
            moments_pitching_geometry_from_symmetry = cas.if_else(self.use_symmetry, -reflect_over_XZ_plane(self.moments_pitching_geometry), 0)
            moment_total_pitching_geometry_from_symmetry = cas.vertcat(cas.sum1(moments_pitching_geometry_from_symmetry[:, 0]), cas.sum1(moments_pitching_geometry_from_symmetry[:, 1]), cas.sum1(moments_pitching_geometry_from_symmetry[:, 2]))
            moment_total_pitching_geometry += moment_total_pitching_geometry_from_symmetry
        self.moment_total_pitching_wind = cas.transpose(self.op_point.compute_rotation_matrix_wind_to_geometry()) @ moment_total_pitching_geometry
        if self.verbose:
            print('Calculating total forces and moments...')
        self.force_total_wind = self.force_total_inviscid_wind + self.force_total_profile_wind
        self.moment_total_wind = self.moment_total_inviscid_wind + self.moment_total_profile_wind
        self.lift_force = -self.force_total_wind[2]
        self.drag_force = -self.force_total_wind[0]
        self.drag_force_induced = -self.force_total_inviscid_wind[0]
        self.drag_force_profile = -self.force_total_profile_wind[0]
        self.side_force = self.force_total_wind[1]
        q = self.op_point.dynamic_pressure()
        s_ref = self.airplane.s_ref
        b_ref = self.airplane.b_ref
        c_ref = self.airplane.c_ref
        self.CL = self.lift_force / q / s_ref
        self.CD = self.drag_force / q / s_ref
        self.CDi = self.drag_force_induced / q / s_ref
        self.CDp = self.drag_force_profile / q / s_ref
        self.CY = self.side_force / q / s_ref
        self.Cl = self.moment_total_wind[0] / q / s_ref / b_ref
        self.Cm = self.moment_total_wind[1] / q / s_ref / c_ref
        self.Cn = self.moment_total_wind[2] / q / s_ref / b_ref
        self.CL_over_CD = cas.if_else(self.CD == 0, 0, self.CL / self.CD)

    def calculate_Vij(self, points, align_trailing_vortices_with_freestream=True):
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
        a_cross_b_squared = a_cross_b_x ** 2 + a_cross_b_y ** 2 + a_cross_b_z ** 2
        a_dot_b = cas.if_else(a_cross_b_squared < 1e-08, a_dot_b + 1, a_dot_b)
        a_cross_u_squared = a_cross_u_x ** 2 + a_cross_u_y ** 2 + a_cross_u_z ** 2
        a_dot_u = cas.if_else(a_cross_u_squared < 1e-08, a_dot_u + 1, a_dot_u)
        b_cross_u_squared = b_cross_u_x ** 2 + b_cross_u_y ** 2 + b_cross_u_z ** 2
        b_dot_u = cas.if_else(b_cross_u_squared < 1e-08, b_dot_u + 1, b_dot_u)
        term1 = (norm_a_inv + norm_b_inv) / (norm_a * norm_b + a_dot_b)
        term2 = norm_a_inv / (norm_a - a_dot_u)
        term3 = norm_b_inv / (norm_b - b_dot_u)
        Vij_x = 1 / (4 * np.pi) * (a_cross_b_x * term1 + a_cross_u_x * term2 - b_cross_u_x * term3)
        Vij_y = 1 / (4 * np.pi) * (a_cross_b_y * term1 + a_cross_u_y * term2 - b_cross_u_y * term3)
        Vij_z = 1 / (4 * np.pi) * (a_cross_b_z * term1 + a_cross_u_z * term2 - b_cross_u_z * term3)
        if self.symmetric_problem:
            a_x = points[:, 0] - cas.repmat(cas.transpose(self.right_vortex_vertices[:, 0]), n_points, 1)
            a_y = points[:, 1] - cas.repmat(cas.transpose(-self.right_vortex_vertices[:, 1]), n_points, 1)
            a_z = points[:, 2] - cas.repmat(cas.transpose(self.right_vortex_vertices[:, 2]), n_points, 1)
            b_x = points[:, 0] - cas.repmat(cas.transpose(self.left_vortex_vertices[:, 0]), n_points, 1)
            b_y = points[:, 1] - cas.repmat(cas.transpose(-self.left_vortex_vertices[:, 1]), n_points, 1)
            b_z = points[:, 2] - cas.repmat(cas.transpose(self.left_vortex_vertices[:, 2]), n_points, 1)
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
            a_cross_b_squared = a_cross_b_x ** 2 + a_cross_b_y ** 2 + a_cross_b_z ** 2
            a_dot_b = cas.if_else(a_cross_b_squared < 1e-08, a_dot_b + 1, a_dot_b)
            a_cross_u_squared = a_cross_u_x ** 2 + a_cross_u_y ** 2 + a_cross_u_z ** 2
            a_dot_u = cas.if_else(a_cross_u_squared < 1e-08, a_dot_u + 1, a_dot_u)
            b_cross_u_squared = b_cross_u_x ** 2 + b_cross_u_y ** 2 + b_cross_u_z ** 2
            b_dot_u = cas.if_else(b_cross_u_squared < 1e-08, b_dot_u + 1, b_dot_u)
            term1 = (norm_a_inv + norm_b_inv) / (norm_a * norm_b + a_dot_b)
            term2 = norm_a_inv / (norm_a - a_dot_u)
            term3 = norm_b_inv / (norm_b - b_dot_u)
            Vij_x_from_symmetry = 1 / (4 * np.pi) * (a_cross_b_x * term1 + a_cross_u_x * term2 - b_cross_u_x * term3)
            Vij_y_from_symmetry = 1 / (4 * np.pi) * (a_cross_b_y * term1 + a_cross_u_y * term2 - b_cross_u_y * term3)
            Vij_z_from_symmetry = 1 / (4 * np.pi) * (a_cross_b_z * term1 + a_cross_u_z * term2 - b_cross_u_z * term3)
            Vij_x += cas.transpose(cas.if_else(self.use_symmetry, cas.transpose(Vij_x_from_symmetry), 0))
            Vij_y += cas.transpose(cas.if_else(self.use_symmetry, cas.transpose(Vij_y_from_symmetry), 0))
            Vij_z += cas.transpose(cas.if_else(self.use_symmetry, cas.transpose(Vij_z_from_symmetry), 0))
        return (Vij_x, Vij_y, Vij_z)

    def calculate_fuselage_influences(self, points):
        n_points = points.shape[0]
        fuselage_influences_x = cas.GenDM_zeros(n_points, 1)
        fuselage_influences_y = cas.GenDM_zeros(n_points, 1)
        fuselage_influences_z = cas.GenDM_zeros(n_points, 1)
        for fuse_num in range(len(self.airplane.fuselages)):
            this_fuse_centerline_points = self.fuse_centerline_points[fuse_num]
            this_fuse_radii = self.fuse_radii[fuse_num]
            dx = points[:, 0] - cas.repmat(cas.transpose(this_fuse_centerline_points[:, 0]), n_points, 1)
            dy = points[:, 1] - cas.repmat(cas.transpose(this_fuse_centerline_points[:, 1]), n_points, 1)
            dz = points[:, 2] - cas.repmat(cas.transpose(this_fuse_centerline_points[:, 2]), n_points, 1)
            source_x = (dx[:, 1:] + dx[:, :-1]) / 2
            source_y = (dy[:, 1:] + dy[:, :-1]) / 2
            source_z = (dz[:, 1:] + dz[:, :-1]) / 2
            areas = cas.pi * this_fuse_radii ** 2
            freestream_x_component = self.op_point.compute_freestream_velocity_geometry_axes()[0]
            strengths = freestream_x_component * cas.diff(areas)
            denominator = 4 * cas.pi * (source_x ** 2 + source_y ** 2 + source_z ** 2) ** 1.5
            u = cas.transpose(strengths * cas.transpose(source_x / denominator))
            v = cas.transpose(strengths * cas.transpose(source_y / denominator))
            w = cas.transpose(strengths * cas.transpose(source_z / denominator))
            fuselage_influences_x += cas.sum2(u)
            fuselage_influences_y += cas.sum2(v)
            fuselage_influences_z += cas.sum2(w)

        fuselage_influences = cas.horzcat(fuselage_influences_x, fuselage_influences_y, fuselage_influences_z)
        return fuselage_influences

    def get_induced_velocity_at_point(self, point):
        if self.verbose:
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
        Vi = self.get_induced_velocity_at_point(point) + self.calculate_fuselage_influences(point)
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
            CL_locals = get(self.CL_locals)
            chords = get(self.chords)
            c_ref = get(self.airplane.c_ref)
            data_name = 'Cl * c / c_ref'
            data_to_plot = CL_locals * chords / c_ref
        fig = Figure3D()
        for index in range(len(front_left_vertices)):
            fig.add_quad(points=[
             front_left_vertices[index, :],
             front_right_vertices[index, :],
             back_right_vertices[index, :],
             back_left_vertices[index, :]],
              intensity=(data_to_plot[index]),
              outline=True,
              mirror=(self.symmetric_problem and self.use_symmetry[index]))
            fig.add_line(points=[
             left_vortex_vertices[index],
             right_vortex_vertices[index]],
              mirror=(self.symmetric_problem and self.use_symmetry[index]))

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
                seed_points = (back_left_vertices + back_right_vertices) / 2
                self.calculate_streamlines(seed_points=seed_points)
            if self.verbose:
                print('Parsing streamline data...')
            n_streamlines = self.streamlines[0].shape[0]
            n_timesteps = len(self.streamlines)
            for streamlines_num in range(n_streamlines):
                streamline = [self.streamlines[ts][streamlines_num, :] for ts in range(n_timesteps)]
                fig.add_streamline(points=streamline,
                  mirror=(self.symmetric_problem))

        return fig.draw(show=show,
          colorbar_title=data_name)