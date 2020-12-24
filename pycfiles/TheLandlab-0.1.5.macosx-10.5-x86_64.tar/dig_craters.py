# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/craters/dig_craters.py
# Compiled at: 2015-02-11 19:25:27
"""
This component supercedes an older version, "craters.py".
This component excavates impact craters across a surface. The properties of the
craters broadly follow those observed for the Moon. Craters obey realistic size-
frequency distributions; at the moment this is forced to follow the Shoemaker
scaling, N = k*D^-2.9.
Importantly, this module incorporates a dependence of  ejecta distribution on
impact momentum.
At the moment, this component does not produce complex craters, largely because
it is optimized to run for craters in the meter-km scale. Craters are dug
perpendicular to the local surface, unless this would steepen local slopes so
much as to severely violate mass balance for the crater,or if slopes would
exceed 90 degrees. In other respects, strength effects are not well
incorporated.
As yet, this module does not have a true time interface - a single call of
excavate_a_crater() will dig a single crater, and adjust its size appropriately
for the Shoemaker distribution. It can't yet adjust itself to imposed timesteps
other than this natural timestep.
At the moment, this component requires you to run on a square regular grid.
"""
from random import random
import numpy
from sympy import Symbol
from sympy.solvers import solve
from sympy.utilities.lambdify import lambdify
from time import sleep
from itertools import izip
import pandas as pd
from landlab import ModelParameterDictionary

class impactor(object):
    """
    This class holds all parameters decribing properties of a single impact
    structure, and contains methods for recalculating fresh and internally 
    consistent data describing such a impact structure.
    Built DEJH Winter 2013, after an earlier version, Spring 2013.
    """

    def __init__(self, grid, input_stream):
        self.grid = grid
        inputs = ModelParameterDictionary(input_stream)
        try:
            self.elev = grid.at_node['topographic_elevation']
        except:
            print 'elevations not found in grid!'

        self._minimum_crater = inputs.read_float('min_radius')
        self._minimum_ejecta_thickness = inputs.read_float('min_ejecta_thickness')
        self._record_impacts_flag = inputs.read_int('record_impacts')
        try:
            self._radius = inputs.read_float('forced_radius')
        except:
            print 'Impact radii will be randomly generated.'
            self.radius_auto_flag = 1
            self.set_cr_radius_from_shoemaker()
        else:
            self.radius_auto_flag = 0

        try:
            self._xcoord = 0.5 * grid.dx + inputs.read_float('x_position') * (grid.get_grid_xdimension() - grid.dx)
            self._ycoord = 0.5 * grid.dx + inputs.read_float('y_position') * (grid.get_grid_ydimension() - grid.dx)
        except:
            print 'Impact sites will be randomly generated.'
            self.position_auto_flag = 1
            self.set_coords()
        else:
            self.position_auto_flag = 0
            self.closest_node_index = grid.find_nearest_node((self._xcoord, self._ycoord))
            self.closest_node_elev = self.elev[self.closest_node_index]

        try:
            self._angle_to_vertical = inputs.read_float('forced_angle') * numpy.pi / 180.0
            assert self._angle_to_vertical <= 0.5 * numpy.pi
        except:
            print 'Impactor angles will be randomly generated.'
            self.angle_auto_flag = 1
            self.set_impactor_angles()
        else:
            self.angle_auto_flag = 0
            self._azimuth_of_travel = 0.5 * numpy.pi

        self.cheater_flag = 0
        self.tan_repose = numpy.tan(32.0 * numpy.pi / 180.0)
        self._beta_factor = 0.5
        self._simple_radius_depth_ratio_Pike = 2.55
        self.V = Symbol('V')
        self.r0 = Symbol('r0')
        self.T = Symbol('T')
        self.r = Symbol('r')
        self.solution_for_rim_thickness = solve(8.0 / 3.0 * self.T * numpy.pi * self.r0 ** 2 + 0.33333 * numpy.pi * self.T * (self.r0 ** 2 + (self.r0 - self.T / self.tan_repose) ** 2 + self.r0 * (self.r0 - self.T / self.tan_repose)) - self.V, self.T)
        self.expression_for_local_thickness = self.T * (self.r / self.r0) ** (-2.75)
        self.loop_dict = {}
        if not numpy.all(numpy.equal(grid.node_status[numpy.nonzero(grid.node_status)], 3)):
            self.looped_BCs = False
            print '*****-----*****-----*****'
            print 'This module is designed to run with looped boundary conditions.'
            print 'Proceed at your own risk!'
            print 'Significant mass leaks are likely to develop.'
            print '*****-----*****-----*****'
            sleep(3.0)
        else:
            self.looped_BCs = True
        self.grid = grid
        self.twod_node_store = numpy.empty((self.grid.number_of_node_rows, self.grid.number_of_node_columns), dtype=int)
        self.dummy_1 = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.dummy_2 = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.dummy_3 = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.dummy_4 = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.dummy_5 = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.dummy_6 = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.dummy_int = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=int)
        self.dummy_bool = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=bool)
        self.double_dummy = numpy.empty((2, self.grid.number_of_node_rows * self.grid.number_of_node_columns), dtype=float)
        self.crater_footprint_max = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=int)
        self.footprint_max = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=int)
        self._vec_r_to_center = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self._vec_theta = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.slope_offsets_rel_to_center = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self._vec_new_z = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.z_difference = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.elevs_ground_less_new_z = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self._vec_flat_thickness_above_surface = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self._vec_mu_theta_by_mu0 = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self._vec_f_theta = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self._vec_thickness = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.final_elev_diffs = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.elev_diff = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=float)
        self.pre_impact_elev = self.elev.copy()
        self.impact_property_dict = {}
        print 'Craters component setup complete!'

    def draw_new_parameters(self):
        """
        This method updates the core properties of radius, position and angle to
        vertical for a new impact crater.
        """
        if self.radius_auto_flag == 1:
            self.set_cr_radius_from_shoemaker()
        if self.position_auto_flag == 1:
            self.set_coords()
        if self.angle_auto_flag == 1:
            self.set_impactor_angles()

    def get_crater_shape_exp(self):
        """
        This method assumes the max depth and radius of a crater are known.
        It provides n for a power law of form d = D*(r/R)**n, where D and R are
        the known values, by assuming the outer edges of the crater sit at angle
        of repose. This gives very sensible answers; n~2 for big, complex
        craters (Garvin et al, 2000, p.333: "There is a strong tendency for
        craters to become more paraboloidal with increasing diameter,
        independent of location.") and n~1.3 for ~2km simple craters (Garvin,
        following Croft has ~1.18).
        """
        return 0.51 * self._radius / self._depth

    def set_cr_radius_from_shoemaker(self):
        """
        This method takes a random number between 0 and 1, and returns a crater
        radius based on a py distn N = kD^-2.9, following Shoemaker et al., 1970.
        """
        self._radius = self._minimum_crater * random() ** (-0.345)

    def set_coords(self):
        """
        This method selects a random location inside the grid onto which to map
        an impact. It also sets variables for the closest grid node to the
        impact, and the elevation at that node.
        """
        grid = self.grid
        self._xcoord = 0.5 * grid.dx + random() * (grid.get_grid_xdimension() - grid.dx)
        self._ycoord = 0.5 * grid.dx + random() * (grid.get_grid_ydimension() - grid.dx)
        self.closest_node_index = grid.find_nearest_node((self._xcoord, self._ycoord))
        self.closest_node_elev = self.elev[self.closest_node_index]

    def check_coords_and_angles_for_grazing(self):
        """
        This method migrates the coords of a given impactor if its normal angle
        means it would clip other topo before striking home.
        It assumes both set_impactor_angles() and set_coords() have already both
        been called.
        """
        sin_az = numpy.sin(self._azimuth_of_travel)
        cos_az = numpy.cos(self._azimuth_of_travel)
        alpha = self._azimuth_of_travel - numpy.pi
        cos_alpha = numpy.cos(alpha)
        sin_alpha = numpy.sin(alpha)
        grid = self.grid
        gridx = grid.get_grid_xdimension()
        gridy = grid.get_grid_ydimension()
        dx = grid.dx
        x = self._xcoord
        y = self._ycoord
        height = self.closest_node_elev
        not_done = True
        impact_at_edge = False
        counter = 0
        while not_done and counter < 30:
            print '...'
            if sin_alpha < 0.0:
                line_horiz = -(x - 0.5 * dx)
            else:
                line_horiz = gridx - x - 0.5 * dx
            if cos_alpha < 0.0:
                line_vert = -(y - 0.5 * dx)
            else:
                line_vert = gridy - y - 0.5 * dx
            hyp_line_vert = numpy.fabs(line_vert / cos_alpha)
            hyp_line_horiz = numpy.fabs(line_horiz / sin_alpha)
            num_divisions = int(min(hyp_line_vert, hyp_line_horiz) // dx)
            if num_divisions > 0:
                self.dummy_1[:num_divisions] = xrange(num_divisions)
                numpy.add(self.dummy_1[:num_divisions], 1.0, out=self.dummy_2[:num_divisions])
                numpy.multiply(self.dummy_2[:num_divisions], dx, out=self.dummy_1[:num_divisions])
            else:
                self.dummy_1[:1] = numpy.array((0.0, ))
                num_divisions = 1
                impact_at_edge = True
                print 'AD HOC FIX'
            numpy.multiply(self.dummy_1[:num_divisions], sin_alpha, out=self.dummy_2[:num_divisions])
            numpy.add(self.dummy_2[:num_divisions], x, out=self.dummy_5[:num_divisions])
            numpy.multiply(self.dummy_1[:num_divisions], cos_alpha, out=self.dummy_2[:num_divisions])
            numpy.add(self.dummy_2[:num_divisions], y, out=self.dummy_6[:num_divisions])
            assert numpy.all(self.dummy_5[:num_divisions] >= 0) or impact_at_edge
            self.dummy_2[:num_divisions] = grid.find_nearest_node((self.dummy_5[:num_divisions], self.dummy_6[:num_divisions]))
            try:
                numpy.divide(self.dummy_1[:num_divisions], numpy.tan(self._angle_to_vertical), out=self.dummy_3[:num_divisions])
                numpy.add(self.dummy_3[:num_divisions], height, out=self.dummy_4[:num_divisions])
            except ZeroDivisionError:
                not_done = False
            else:
                try:
                    numpy.less_equal(self.dummy_4[num_divisions - 1::-1], self.elev[self.dummy_2[num_divisions - 1::-1].astype(int, copy=False)], out=self.dummy_int[:num_divisions])
                    reversed_index = numpy.argmax(self.dummy_int[:num_divisions])
                    intersect_pt_node_status = self.grid.node_status[self.dummy_2[num_divisions - 1::-1][reversed_index]]
                except IndexError:
                    print len(self.dummy_4[:num_divisions])
                    assert len(self.dummy_4[:num_divisions]) == 1
                    numpy.less_equal(self.dummy_4[:num_divisions], self.elev[self.dummy_2[:num_divisions].astype(int, copy=False)], out=self.dummy_int[:num_divisions])
                    reversed_index = numpy.argmax(self.dummy_int[:num_divisions])
                    intersect_pt_node_status = self.grid.node_status[self.dummy_2[:num_divisions]]

                if numpy.any(self.dummy_int[:num_divisions]):
                    if reversed_index and intersect_pt_node_status != 3 and not impact_at_edge:
                        print 'migrating...'
                        index_of_impact = num_divisions - reversed_index
                        self._xcoord = self.dummy_5[:num_divisions][index_of_impact]
                        self._ycoord = self.dummy_6[:num_divisions][index_of_impact]
                        self.closest_node_index = self.dummy_2[:num_divisions][index_of_impact]
                        self.closest_node_elev = self.elev[self.closest_node_index]
                        not_done = False
                    elif self.looped_BCs:
                        print 'Need to loop the impact trajectory...'
                        shorter_edge = numpy.argmin(numpy.array([hyp_line_vert, hyp_line_horiz]))
                        if shorter_edge:
                            if sin_alpha > 0.0:
                                horiz_coord = 0.50001 * dx
                                vert_coord = y + (gridx - x - 0.5 * dx) * cos_alpha / sin_alpha
                                height += numpy.sqrt((gridx - x - 0.5 * dx) ** 2.0 + (vert_coord - y) ** 2.0) / numpy.tan(self._angle_to_vertical)
                            else:
                                horiz_coord = gridx - 0.50001 * dx
                                vert_coord = y - (x - 0.5 * dx) * cos_alpha / sin_alpha
                                height += numpy.sqrt((x - 0.5 * dx) ** 2.0 + (vert_coord - y) ** 2.0) / numpy.tan(self._angle_to_vertical)
                        elif cos_alpha > 0.0:
                            vert_coord = 0.50001 * dx
                            horiz_coord = x + (gridy - y - 0.5 * dx) * sin_alpha / cos_alpha
                            height += numpy.sqrt((gridy - y - 0.5 * dx) ** 2.0 + (horiz_coord - x) ** 2.0) / numpy.tan(self._angle_to_vertical)
                        else:
                            vert_coord = gridy - 0.50001 * dx
                            horiz_coord = x - (y - 0.5 * dx) * sin_alpha / cos_alpha
                            height += numpy.sqrt((y - 0.5 * dx) ** 2.0 + (horiz_coord - x) ** 2.0) / numpy.tan(self._angle_to_vertical)
                        x = horiz_coord
                        y = vert_coord
                        print x / gridx, y / gridy
                        counter += 1
                        if counter >= 30:
                            self._radius = 1e-06
                            print 'Aborted this crater. Its trajectory was not physically plausible!'
                    elif self.position_auto_flag == 1:
                        self.draw_new_parameters()
                        self.check_coords_and_angles_for_grazing()
                        not_done = False
                    else:
                        self._radius = 1e-06
                        print 'Aborted this crater. Its trajectory was not physically plausible!'
                        not_done = False
                else:
                    not_done = False

    def set_impactor_angles(self):
        """
        This method sets the angle of impact, assuming the only effect is
        rotation of the planet under the impactor bombardment (i.e., if the
        target looks like a circle to the oncoming impactor, there's more limb
        area there to hit). As long as target is rotating relative to the sun,
        other (directional) effects should cancel. i.e., it draws from a sine
        distribution.
        Angle is given to vertical.
        Also sets a random azimuth.
        """
        self._angle_to_vertical = abs(numpy.arcsin(random()))
        self._azimuth_of_travel = random() * 2.0 * numpy.pi

    def set_depth_from_size(self):
        """
        This method sets the maximum depth at the center for a crater of known
        (i.e., already set) radius.
        """
        self._depth = self._radius / self._simple_radius_depth_ratio_Pike

    def set_crater_volume(self):
        """
        This method uses known crater depth and radius and sets the volume of
        the excavated cavity.
        Note this is is the cavity volume, not the subsurface excavation vol.
        The true excavated volume is used to set the ejecta volumes in the 
        ..._BAND_AID methods.
        """
        radius = self._radius
        depth = self._depth
        self._cavity_volume = 0.51 * numpy.pi * depth * radius * radius * radius / (0.51 * radius + 2.0 * depth)

    def create_lambda_fn_for_ejecta_thickness(self):
        """
        This method takes the complicated equation that relates "flat" ejecta
        thickness (symmetrical, with impact angle=0) to radius and cavity volume
        which is set in __init__(), and solves it for a given pair of impact
        specific parameters, V_cavity & crater radius.
        Both the cavity volume and crater radius need to have been set before
        this method is called.
        Method returns a lambda function for the radially symmetrical ejecta
        thickness distribution as a function of distance from crater center, r.
        i.e., call unique_expression_for_local_thickness(r) to calculate a
        thickness.
        Added DEJH Sept 2013.
        """
        local_solution_for_rim_thickness = self.solution_for_rim_thickness[0].subs(self.V, self._cavity_volume)
        unique_expression_for_local_thickness = self.expression_for_local_thickness.subs({self.r0: self._radius, self.T: local_solution_for_rim_thickness})
        unique_expression_for_local_thickness = lambdify(self.r, unique_expression_for_local_thickness)
        return unique_expression_for_local_thickness

    def create_lambda_fn_for_ejecta_thickness_BAND_AID(self, excavated_vol):
        """
        This method takes the complicated equation that relates "flat" ejecta
        thickness (symmetrical, with impact angle=0) to radius and cavity volume
        which is set in __init__(), and solves it for a given pair of impact
        specific parameters, V_cavity & crater radius.
        Both the cavity volume and crater radius need to have been set before
        this method is called.
        Method returns a lambda function for the radially symmetrical ejecta
        thickness distribution as a function of distance from crater center, r.
        i.e., call unique_expression_for_local_thickness(r) to calculate a
        thickness.
        This method is exactly equivalent to the non _BAND_AID equivalent,
        except it takes the volume to use as a parameter rather than reading it
        from the impactor object.
        Added DEJH Sept 2013.
        """
        local_solution_for_rim_thickness = self.solution_for_rim_thickness[0].subs(self.V, excavated_vol)
        unique_expression_for_local_thickness = self.expression_for_local_thickness.subs({self.r0: self._radius, self.T: local_solution_for_rim_thickness})
        unique_expression_for_local_thickness = lambdify(self.r, unique_expression_for_local_thickness)
        return unique_expression_for_local_thickness

    def set_crater_mean_slope_v2(self):
        """
        This method takes a crater of known radius, and which has already been
        "snapped" to the grid through snap_impact_to_grid(mygrid), and returns a
        spatially averaged value for the local slope of the preexisting topo
        beneath the cavity footprint. This version of the method works by taking
        four transects across the crater area every 45 degrees around its rim,
        calculating the slope along each, then setting the slope as the greatest,
        positive downwards and in the appropriate D8 direction. This function
        also sets the mean surface dip direction.
        In here, we start to assume a convex and structured grid, such that if
        pts N and W on the rim are in the grid, so is the point NW.
        This version is vectorized, and so hopefully faster.
        This method is largely superceded by set_crater_mean_slope_v3(), which
        uses an GIS-style routine to set slopes. However, it may still be 
        preferable for grid-marginal craters.
        DEJH, Sept 2013.
        """
        grid = self.grid
        divisions = 4
        half_crater_radius = 0.707 * self._radius
        slope_pts1 = numpy.array([[self._xcoord, self._ycoord + self._radius],
         [
          self._xcoord + half_crater_radius, self._ycoord + half_crater_radius],
         [
          self._xcoord + self._radius, self._ycoord],
         [
          self._xcoord + half_crater_radius, self._ycoord - half_crater_radius]])
        slope_pts2 = numpy.array([[self._xcoord, self._ycoord - self._radius],
         [
          self._xcoord - half_crater_radius, self._ycoord - half_crater_radius],
         [
          self._xcoord - self._radius, self._ycoord],
         [
          self._xcoord - half_crater_radius, self._ycoord + half_crater_radius]])
        inbounds_test1 = grid.is_point_on_grid(slope_pts1[:, 0], slope_pts1[:, 1])
        inbounds_test2 = grid.is_point_on_grid(slope_pts2[:, 0], slope_pts2[:, 1])
        distance_array = (inbounds_test1.astype(float) + inbounds_test2.astype(float)) * self._radius
        radial_points1 = numpy.where(inbounds_test1, (slope_pts1[:, 0], slope_pts1[:, 1]), [[self._xcoord], [self._ycoord]])
        radial_points2 = numpy.where(inbounds_test2, (slope_pts2[:, 0], slope_pts2[:, 1]), [[self._xcoord], [self._ycoord]])
        radial_points1 = grid.find_nearest_node((radial_points1[0, :], radial_points1[1, :]))
        radial_points2 = grid.find_nearest_node((radial_points2[0, :], radial_points2[1, :]))
        slope_array = numpy.where(distance_array, (self.elev[radial_points1] - self.elev[radial_points2]) / distance_array, numpy.nan)
        slope_array = numpy.arctan(slope_array)
        try:
            hi_mag_slope_index = numpy.nanargmax(numpy.fabs(slope_array))
            hi_mag_slope = slope_array[hi_mag_slope_index]
        except:
            self._surface_slope = 1e-10
            print 'Unable to assign crater slope by this method. Is crater of size comparable with grid?'
            print 'Setting slope to zero'

        if hi_mag_slope > 0.0:
            self._surface_dip_direction = (hi_mag_slope_index / float(divisions) + 1.0) * numpy.pi
        else:
            if not hi_mag_slope:
                self._surface_dip_direction = self._azimuth_of_travel
            else:
                self._surface_dip_direction = numpy.pi * hi_mag_slope_index / float(divisions)
            self._surface_slope = numpy.fabs(hi_mag_slope)

    def set_crater_mean_slope_v3(self):
        """
        Runs on a square which encapsulates the crater.
        If some of the nodes are off the grid AND the boundaries aren't looped, 
        it falls back on v2.
        If they are, it will freely loo the nodes back onto the grid, and return
        a real slope.
        This version uses the Horn, 1981 algorithm, the same one used by many
        GIS packages.
        """
        grid = self.grid
        elev = self.elev
        r = 0.7071 * self._radius
        x = self._xcoord
        y = self._ycoord
        slope_pts = numpy.array([[x - r, y - r], [x, y - r], [x + r, y - r], [x - r, y], [x, y], [x + r, y], [x - r, y + r], [x, y + r], [x + r, y + r]])
        pts_on_grid = grid.is_point_on_grid(slope_pts[:, 0], slope_pts[:, 1])
        if not numpy.all(pts_on_grid) and not self.looped_BCs:
            slope_coords_ongrid = slope_pts[pts_on_grid]
            slope_pts_ongrid = grid.find_nearest_node((slope_coords_ongrid[:, 0], slope_coords_ongrid[:, 1]))
            cardinal_elevs = elev[slope_pts_ongrid]
            self.closest_node_index = grid.find_nearest_node((self._xcoord, self._ycoord))
            self.set_crater_mean_slope_v2()
        else:
            slope_pts %= numpy.array([self.grid.get_grid_xdimension(), self.grid.get_grid_ydimension()])
            slope_pts_ongrid = grid.find_nearest_node((slope_pts[:, 0], slope_pts[:, 1]))
            self.closest_node_index = slope_pts_ongrid[4]
            cardinal_elevs = elev[slope_pts_ongrid]
            S_we = (cardinal_elevs[6] + 2 * cardinal_elevs[3] + cardinal_elevs[0] - (cardinal_elevs[8] + 2 * cardinal_elevs[5] + cardinal_elevs[2])) / (8.0 * r)
            S_sn = (cardinal_elevs[0] + 2 * cardinal_elevs[1] + cardinal_elevs[2] - (cardinal_elevs[6] + 2 * cardinal_elevs[7] + cardinal_elevs[8])) / (8.0 * r)
            self._surface_slope = numpy.sqrt(S_we * S_we + S_sn * S_sn)
            if not S_we:
                if S_sn < 0.0:
                    self._surface_dip_direction = numpy.pi
                else:
                    self._surface_dip_direction = 0.0
            else:
                angle_to_xaxis = numpy.arctan(S_sn / S_we)
                self._surface_dip_direction = (1.0 - numpy.sign(S_we)) * 0.5 * numpy.pi + (0.5 * numpy.pi - angle_to_xaxis)
        self.closest_node_elev = numpy.mean(cardinal_elevs)

    def set_elev_change_only_beneath_footprint_BAND_AID_memory_save(self):
        """
        This is a method to take an existing impact properties and a known 
        nearest node to the impact site, and alter the topography to model the 
        impact. It assumes crater radius and depth are known, models cavity 
        shape as a power law where n is a function of R/D, and models ejecta 
        thickness as an exponential decay,sensitive to both ballistic range from 
        tilting and momentum transfer in impact (after Furbish). We DO NOT yet 
        model transition to peak ring craters, or enhanced diffusion by ejecta 
        in the strength regime. All craters are dug perpendicular to the geoid, 
        not the surface.
        This version of the code does NOT correct for slope dip direction - 
        because Furbish showed momentum almost always wins, and these impactors 
        have a lot of momentum!
        NB - this function ASSUMES that the "beta factor" in the model is <=0.5, 
        i.e., nonlinearities can't develop in the ejecta field, and the impact 
        point is always within the (circular) ejecta footprint.
        This version of this method ("_band_aid"!) uses a quick and dirty fix 
        which substitutes the actual excavated volume into the equn to derive 
        ejecta thicknesses. It also digs craters perpendicular to the local 
        surface, mimicking some aspects of a "strength dominated" impact - 
        unless doing so would create extremely strongly tilted craters, excavate
        large sheets of material, or otherwise destabilize the mass balance of
        the component.
        It pays no regard for the inefficiency of doing that!
        Created DEJH Dec 2013
        """
        _angle_to_vertical = self._angle_to_vertical
        _surface_slope = self._surface_slope
        _surface_dip_direction = self._surface_dip_direction
        _azimuth_of_travel = self._azimuth_of_travel
        pi = numpy.pi
        twopi = 2.0 * pi
        tan = numpy.tan
        cos = numpy.cos
        sin = numpy.sin
        sqrt = numpy.sqrt
        arccos = numpy.arccos
        where = numpy.where
        _radius = self._radius
        elev = self.elev
        tan_repose = self.tan_repose
        grid = self.grid
        self.cheater_flag = 0
        elev_diff_below_ground = 0.0
        total_elev_diff = 0.0
        all_the_footprint_nodes = numpy.empty(self.grid.number_of_node_rows * self.grid.number_of_node_columns, dtype=int)
        number_of_total_footprint_nodes = 0.0
        crater_bowl_exp = self.get_crater_shape_exp()
        counter = 0
        while 1:
            rake_in_surface_plane = _surface_dip_direction - _azimuth_of_travel
            absolute_rake = numpy.fabs(rake_in_surface_plane)
            if not _surface_slope:
                epsilon = 0.0
                beta_eff = _angle_to_vertical
            else:
                if absolute_rake in (0.5 * pi, 1.5 * pi):
                    epsilon = 0.0
                else:
                    epsilon = arccos(cos(rake_in_surface_plane) * cos(_surface_slope) * sqrt(1.0 + (tan(rake_in_surface_plane) / cos(_surface_slope)) ** 2.0))
                if absolute_rake <= 0.5 * pi or absolute_rake >= 1.5 * pi:
                    beta_eff = _angle_to_vertical + epsilon
                else:
                    beta_eff = _angle_to_vertical + epsilon - pi
            print 'Beta effective: ', beta_eff
            if 0.0 <= beta_eff <= 0.5 * numpy.pi:
                _ejecta_azimuth = _azimuth_of_travel
                break
            elif -0.5 * numpy.pi < beta_eff < 0.0:
                beta_eff = -beta_eff
                _ejecta_azimuth = (_azimuth_of_travel + pi) % twopi
                break
            else:
                print 'Impact geometry was not possible! Refreshing the impactor angle...'
                self.set_impactor_angles()
                _azimuth_of_travel = self._azimuth_of_travel
                _angle_to_vertical = self._angle_to_vertical
                if counter > 20:
                    beta_eff = 0.0
                    _ejecta_azimuth = self._azimuth_of_travel
                    break
                else:
                    counter += 1

        mass_bal_corrector_for_slope = self.correct_for_slope()
        mass_bal_corrector_for_angle_to_vertical = self.correct_for_angle_to_vertical()
        mass_bal_corrector_for_size = self.correct_for_crater_size()
        tan_beta = tan(beta_eff * self._beta_factor)
        tan_beta_sqd = tan_beta * tan_beta
        crater_edge_type_flag, crater_num_repeats = self.footprint_edge_type((self._xcoord, self._ycoord), 4.0 * _radius)
        crater_footprint_iterator = self.create_square_footprint((self._xcoord, self._ycoord), 4.0 * _radius, crater_edge_type_flag, self.crater_footprint_max)
        crater_center_offset_iterator = self.center_offset_list_for_looped_BCs((self._xcoord, self._ycoord), crater_edge_type_flag, crater_num_repeats)
        excavated_volume = 0.0
        for footprint_tuple, j in izip(crater_footprint_iterator, crater_center_offset_iterator):
            i = footprint_tuple[0]
            self.crater_footprint_max = footprint_tuple[1]
            grid.get_distances_of_nodes_to_point(j, get_az='angles', node_subset=self.crater_footprint_max[:i], out_distance=self._vec_r_to_center[:i], out_azimuth=self._vec_theta[:i])
            numpy.subtract(self._vec_theta[:i], self._surface_dip_direction, out=self.dummy_1[:i])
            numpy.cos(self.dummy_1[:i], out=self.dummy_2[:i])
            numpy.multiply(self.dummy_2[:i], self._vec_r_to_center[:i], out=self.dummy_1[:i])
            numpy.multiply(self.dummy_1[:i], -numpy.tan(self._surface_slope), out=self.slope_offsets_rel_to_center[:i])
            numpy.add(self.slope_offsets_rel_to_center[:i], self.closest_node_elev - 0.9 * self._depth, out=self.dummy_1[:i])
            numpy.divide(self._vec_r_to_center[:i], _radius, out=self.dummy_2[:i])
            numpy.power(self.dummy_2[:i], crater_bowl_exp, out=self.dummy_3[:i])
            numpy.multiply(self.dummy_3[:i], self._depth, out=self.dummy_2[:i])
            numpy.add(self.dummy_2[:i], self.dummy_1[:i], out=self._vec_new_z[:i])
            numpy.subtract(self.elev[self.crater_footprint_max[:i]], self._vec_new_z[:i], out=self.z_difference[:i])
            numpy.less_equal(self.z_difference[:i], 0.0, self.dummy_bool[:i])
            self.z_difference[:i][self.dummy_bool[:i]] = 0.0
            excavated_volume += numpy.sum(self.z_difference[:i]) * grid.dx * grid.dx

        unique_expression_for_local_thickness = self.create_lambda_fn_for_ejecta_thickness_BAND_AID(excavated_volume * mass_bal_corrector_for_slope * mass_bal_corrector_for_angle_to_vertical * mass_bal_corrector_for_size)
        thickness_at_rim = unique_expression_for_local_thickness(_radius)
        if thickness_at_rim < 0.0:
            thickness_at_rim = 0.0
        print 'First pass thickness: ', thickness_at_rim
        print 'dist above ground: ', thickness_at_rim - self._depth
        if crater_edge_type_flag == 'C' or crater_edge_type_flag == 'X':
            self._vec_new_z[:i].fill(self.closest_node_elev + thickness_at_rim - self._depth)
            print 'dist above ground: ', thickness_at_rim - self._depth
            numpy.add(self.dummy_2[:i], self._vec_new_z[:i], out=self._vec_new_z[:i])
            numpy.subtract(self.pre_impact_elev[self.crater_footprint_max[:i]], self._vec_new_z[:i], out=self.elevs_ground_less_new_z[:i])
            volume_to_fill_inner_crater_divots = 0.0
            numpy.less_equal(self.elevs_ground_less_new_z[:i], 0.0, self.dummy_bool[:i])
            self.elevs_ground_less_new_z[:i][self.dummy_bool[:i]] = 0.0
            volume_to_remove_highs = numpy.sum(self.elevs_ground_less_new_z[:i]) * grid.dx * grid.dx
            unique_expression_for_local_thickness = self.create_lambda_fn_for_ejecta_thickness_BAND_AID((volume_to_remove_highs - volume_to_fill_inner_crater_divots) * mass_bal_corrector_for_slope * mass_bal_corrector_for_angle_to_vertical * mass_bal_corrector_for_size)
            thickness_at_rim = unique_expression_for_local_thickness(_radius)
        else:
            crater_edge_type_flag, crater_num_repeats = self.footprint_edge_type((self._xcoord, self._ycoord), 4.0 * _radius)
            crater_footprint_iterator = self.create_square_footprint((self._xcoord, self._ycoord), 4.0 * _radius, crater_edge_type_flag, self.crater_footprint_max)
            crater_center_offset_iterator = self.center_offset_list_for_looped_BCs((self._xcoord, self._ycoord), crater_edge_type_flag, crater_num_repeats)
            volume_to_remove_highs = 0.0
            for footprint_tuple, center_tuple in izip(crater_footprint_iterator, crater_center_offset_iterator):
                print 'recalc values...'
                i = footprint_tuple[0]
                self.crater_footprint_max = footprint_tuple[1]
                footprint_nodes = self.crater_footprint_max[:i]
                grid.get_distances_of_nodes_to_point(center_tuple, get_az='angles', node_subset=footprint_nodes, out_distance=self._vec_r_to_center[:i], out_azimuth=self._vec_theta[:i])
                self._vec_new_z[:i].fill(self.closest_node_elev + thickness_at_rim - self._depth)
                numpy.divide(self._vec_r_to_center[:i], _radius, out=self.dummy_2[:i])
                numpy.power(self.dummy_2[:i], crater_bowl_exp, out=self.dummy_3[:i])
                numpy.multiply(self.dummy_3[:i], self._depth, out=self.dummy_2[:i])
                numpy.add(self.dummy_2[:i], self._vec_new_z[:i], out=self._vec_new_z[:i])
                numpy.subtract(self.pre_impact_elev[footprint_nodes], self._vec_new_z[:i], out=self.elevs_ground_less_new_z[:i])
                volume_to_fill_inner_crater_divots = 0.0
                numpy.less_equal(self.elevs_ground_less_new_z[:i], 0.0, self.dummy_bool[:i])
                self.elevs_ground_less_new_z[:i][self.dummy_bool[:i]] = 0.0
                volume_to_remove_highs += numpy.sum(self.elevs_ground_less_new_z[:i]) * grid.dx * grid.dx

            unique_expression_for_local_thickness = self.create_lambda_fn_for_ejecta_thickness_BAND_AID((volume_to_remove_highs - volume_to_fill_inner_crater_divots) * mass_bal_corrector_for_slope * mass_bal_corrector_for_angle_to_vertical * mass_bal_corrector_for_size)
            thickness_at_rim = unique_expression_for_local_thickness(_radius)
        print volume_to_remove_highs
        print volume_to_fill_inner_crater_divots
        if thickness_at_rim < 0.0:
            thickness_at_rim = 0.0
        self.rim_thickness = thickness_at_rim
        max_radius_ejecta_on_flat = _radius * (thickness_at_rim / self._minimum_ejecta_thickness) ** 0.3636
        displacement_distance = max_radius_ejecta_on_flat * tan_beta
        x_impact_offset = sin(_azimuth_of_travel) * displacement_distance
        y_impact_offset = cos(_azimuth_of_travel) * displacement_distance
        if x_impact_offset + 4 * self._radius > max_radius_ejecta_on_flat:
            print 'A low-angle crater!'
            max_radius_ejecta_on_flat = x_impact_offset + 4.0 * self._radius
        if y_impact_offset + 4 * self._radius > max_radius_ejecta_on_flat:
            print 'A low-angle crater!'
            max_radius_ejecta_on_flat = y_impact_offset + 4.0 * self._radius
        footprint_center_x = self._xcoord + x_impact_offset
        footprint_center_y = self._ycoord + y_impact_offset
        edge_type_flag, num_repeats = self.footprint_edge_type((footprint_center_x, footprint_center_y), max_radius_ejecta_on_flat)
        print edge_type_flag
        footprint_iterator = self.create_square_footprint((footprint_center_x, footprint_center_y), max_radius_ejecta_on_flat, edge_type_flag, self.crater_footprint_max)
        center_offset_iterator = self.center_offset_list_for_looped_BCs((self._xcoord, self._ycoord), edge_type_flag, num_repeats)
        total_elev_diffs = 0.0
        elev_diffs_below_ground = 0.0
        for footprint_tuple, center_tuple in izip(footprint_iterator, center_offset_iterator):
            i = footprint_tuple[0]
            self.crater_footprint_max = footprint_tuple[1]
            print 'looping... effective center is at ', center_tuple
            footprint_nodes = self.crater_footprint_max[:i]
            grid.get_distances_of_nodes_to_point(center_tuple, get_az='angles', node_subset=footprint_nodes, out_distance=self._vec_r_to_center[:i], out_azimuth=self._vec_theta[:i])
            self._vec_new_z[:i].fill(self.closest_node_elev + thickness_at_rim - self._depth)
            numpy.divide(self._vec_r_to_center[:i], _radius, out=self.dummy_2[:i])
            numpy.power(self.dummy_2[:i], crater_bowl_exp, out=self.dummy_3[:i])
            numpy.multiply(self.dummy_3[:i], self._depth, out=self.dummy_2[:i])
            numpy.add(self.dummy_2[:i], self._vec_new_z[:i], out=self._vec_new_z[:i])
            self._vec_flat_thickness_above_surface[:i] = unique_expression_for_local_thickness(self._vec_r_to_center[:i])
            numpy.subtract(_ejecta_azimuth, self._vec_theta[:i], out=self.dummy_1[:i])
            numpy.cos(self.dummy_1[:i], out=self.dummy_2[:i])
            numpy.sin(self.dummy_1[:i], out=self.dummy_3[:i])
            numpy.square(self.dummy_3[:i], out=self.dummy_1[:i])
            numpy.multiply(self.dummy_1[:i], tan_beta_sqd, out=self.dummy_4[:i])
            if tan_beta_sqd > 1.0:
                print 'tan_beta_sqd error!', beta_eff, tan_beta_sqd, epsilon
                raise ValueError
            numpy.subtract(1.0, self.dummy_4[:i], out=self.dummy_3[:i])
            if numpy.any(numpy.less(self.dummy_3[:i], 0.0)):
                print 'about to crash...', numpy.sum(numpy.less(self.dummy_3[:i], 0.0)), self.dummy_3[:i][numpy.where(numpy.less(self.dummy_3[:i], 0.0))]
                raise ValueError
            numpy.sqrt(self.dummy_3[:i], out=self.dummy_4[:i])
            numpy.multiply(self.dummy_2[:i], tan_beta, out=self.dummy_3[:i])
            numpy.add(self.dummy_3[:i], self.dummy_4[:i], out=self._vec_mu_theta_by_mu0[:i])
            numpy.square(self.dummy_2[:i], out=self.dummy_3[:i])
            numpy.subtract(self.dummy_3[:i], self.dummy_1[:i], out=self.dummy_4[:i])
            numpy.multiply(self.dummy_4[:i], tan_beta_sqd, out=self.dummy_3[:i])
            numpy.multiply(self.dummy_1[:i], tan_beta_sqd, out=self.dummy_4[:i])
            numpy.subtract(1.0, self.dummy_4[:i], out=self.dummy_1[:i])
            numpy.sqrt(self.dummy_1[:i], out=self.dummy_4[:i])
            numpy.multiply(self.dummy_2[:i], self.dummy_4[:i], out=self.dummy_1[:i])
            numpy.multiply(self.dummy_1[:i], 2.0 * tan_beta, out=self.dummy_4[:i])
            numpy.add(self.dummy_3[:i], self.dummy_4[:i], out=self.dummy_1[:i])
            numpy.add(self.dummy_1[:i], 1.0, out=self.dummy_3[:i])
            numpy.divide(self.dummy_3[:i], twopi, out=self._vec_f_theta[:i])
            numpy.divide(self._vec_f_theta[:i], self._vec_mu_theta_by_mu0[:i], out=self.dummy_1[:i])
            numpy.multiply(self.dummy_1[:i], self._vec_flat_thickness_above_surface[:i], out=self.dummy_2[:i])
            numpy.multiply(self.dummy_2[:i], twopi, out=self._vec_thickness[:i])
            numpy.less(self._vec_thickness[:i], 0.0, self.dummy_bool[:i])
            self._vec_thickness[:i][self.dummy_bool[:i]] = 0.0
            numpy.add(self.pre_impact_elev[footprint_nodes], self._vec_thickness[:i], out=self.dummy_1[:i])
            self.double_dummy[0, :i] = self.dummy_1[:i]
            self.double_dummy[1, :i] = self._vec_new_z[:i]
            numpy.amin(self.double_dummy[:, :i], axis=0, out=self.dummy_2[:i])
            numpy.subtract(self.dummy_2[:i], self.pre_impact_elev[footprint_nodes], out=self.final_elev_diffs[:i])
            numpy.add(self.final_elev_diffs[:i], self.elev[footprint_nodes], out=self.dummy_1[:i])
            self.elev[footprint_nodes] = self.dummy_1[:i]
            total_elev_diffs += numpy.sum(self.final_elev_diffs[:i])
            numpy.less(self.final_elev_diffs[:i], 0.0, out=self.dummy_bool[:i])
            elev_diffs_below_ground += -numpy.sum(self.final_elev_diffs[:i][self.dummy_bool[:i]])

        print total_elev_diffs
        print elev_diffs_below_ground
        self.mass_balance_in_impact = total_elev_diffs / elev_diffs_below_ground
        self.ejecta_azimuth = _ejecta_azimuth
        self.impactor_angle_to_surface_normal = beta_eff
        return self.elev

    def footprint_edge_type(self, center, eff_radius):
        """
        Returns the edge type of a given node footprint to be build with create_
        square_footprint()  around the given center.
        Returns 2 values:
        * One of N,S,E,W,NW,NE,SW,SE, if the footprint overlaps a single edge or
          corner; 'C' for an entirely enclosed footprint; 'I' if it intersects 
          opposite sides of the grid (i.e., bigger than the grid); 'X' if looped
          boundaries aren't set.
        * An integer. If the first return is 'I', this is the number of "whole" 
          grids the footprint could enclose (minimum 1). If it's something else,
          returns 0.
        """
        assert type(center) == tuple
        assert len(center) == 2
        grid_x = self.grid.get_grid_xdimension() - self.grid.dx
        grid_y = self.grid.get_grid_ydimension() - self.grid.dx
        print 'center, r, x', center[0], eff_radius, grid_x
        left_repeats = -int((center[0] - eff_radius) // grid_x)
        right_repeats = int((center[0] + eff_radius) // grid_x)
        top_repeats = int((center[1] + eff_radius) // grid_y)
        bottom_repeats = -int((center[1] - eff_radius) // grid_y)
        if left_repeats and right_repeats or top_repeats and bottom_repeats:
            big_foot = True
        else:
            big_foot = False
        if big_foot and self.looped_BCs:
            return ('I', int(max([left_repeats, right_repeats, top_repeats, bottom_repeats])))
        else:
            if self.looped_BCs:
                if left_repeats:
                    if top_repeats:
                        flag = 'NW'
                    elif bottom_repeats:
                        flag = 'SW'
                    else:
                        flag = 'W'
                elif right_repeats:
                    if top_repeats:
                        flag = 'NE'
                    elif bottom_repeats:
                        flag = 'SE'
                    else:
                        flag = 'E'
                elif top_repeats:
                    flag = 'N'
                elif bottom_repeats:
                    flag = 'S'
                else:
                    flag = 'C'
                return (flag, 0)
            return ('X', 0)

    def create_square_footprint(self, center, eff_radius, footprint_edge_type, array_in=None):
        """
        This method creates a square footprint of nodes around a given center
        point, with a specified halfwidth.
        It is designed to avoid the need to actually search the whole grid
        in order to establish the footprint, to accelerate the craters
        module.
        "Center" is a tuple, (x,y), the footprint's center.
        eff_radius is the footprint halfwidth.
        footprint_edge_type and whole_grid_repeats are the outputs from 
        footprint_edge_type() for this footprint.
        The function is a generator, designed to interface with a loop on the
        grids it outputs. The method generates intelligently:
        -If loops AREN'T active, it returns just a single array and terminates.
        Note we can never return the IDs of the boundary nodes - we shouldn't 
        ever be operating directly on them in the meat of this module.
        -If loops ARE active, it differentiates between big ('I') footprints 
        and the others-
            Edge type 'C' - the entire footprint is within the grid, and one
              array is output.
            Edge type 'N', 'E', 'S', 'W' - the footprint overlaps with one
              edge only. Two arrays follow; the center grid nodes, then the 
              edge nodes.
            Edge type 'NE','SE','SW','NW' - the footprint overlaps with a 
              corner and two edges. three arrays follow; the center tile, then
              the edges (clockwise), then the corner.

          If it's 'I', it means the footprint is "large" compared to the
          grid. The method then uses the integer stored in whole_grid_repeats. 
          this works as 1: one whole grid plus edges needed. 
          2: a 3x3 grid surrounded by edges. 3: a 5x5 grid surrounded by edges.
          The intention is that these will be rare enough just using whole grids
          is not too inefficient.
        
        
          ______________________________________
          |                                     | 'I'
          |      * * * * * * * * * * *          |
          |      *  ___              *          |
          |      * |   | 'C'        _*___       |
          |      * |___|           | *   | 'E'  |
          |      *                 | *   |      |
          |    __*__               |_*___|      |
          |   |  *  | 'SW'           *          |
          |   |  * * * * * * * * * * *          |
          |   |_____|                           |
          |                                     |
          |_____________________________________|
                
                
        """
        if array_in is not None:
            x = numpy.empty(self.grid.number_of_node_columns - 2)
            y_column = numpy.empty(self.grid.number_of_node_rows - 2).reshape((self.grid.number_of_node_rows - 2, 1))
        assert type(center) == tuple
        assert len(center) == 2
        if footprint_edge_type == 'I':
            if array_in is not None:
                number_of_footprint_nodes = self.grid.number_of_interior_nodes
                array_in = self.grid.get_interior_nodes()
                while 1:
                    yield (
                     number_of_footprint_nodes, array_in)

            else:
                while 1:
                    yield self.grid.get_interior_nodes()

        else:
            center_array = numpy.array(center)
            dx = self.grid.dx
            max_cols = self.grid.number_of_node_columns - 2
            max_rows = self.grid.number_of_node_rows - 2
            max_dims_array = numpy.array([max_cols, max_rows])
            left_bottom = ((center_array - eff_radius) // dx).astype(int) + 1
            right_top = ((center_array + eff_radius) // dx).astype(int)
            right_top_nonzero = right_top.copy()
            left_bottom_nonzero = numpy.where(left_bottom < 1, 1, left_bottom)
            if right_top_nonzero[0] > max_cols:
                right_top_nonzero[0] = max_cols
            if right_top_nonzero[1] > max_rows:
                right_top_nonzero[1] = max_rows
            if array_in is not None:
                len_x = right_top_nonzero[0] - left_bottom_nonzero[0] + 1
                len_y = right_top_nonzero[1] - left_bottom_nonzero[1] + 1
                x[:len_x] = numpy.arange(right_top_nonzero[0] - left_bottom_nonzero[0] + 1) + left_bottom_nonzero[0]
                y_column[:len_y] = numpy.arange(right_top_nonzero[1] - left_bottom_nonzero[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero[1]
                self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
            else:
                x = numpy.arange(right_top_nonzero[0] - left_bottom_nonzero[0] + 1) + left_bottom_nonzero[0]
                y = numpy.arange(right_top_nonzero[1] - left_bottom_nonzero[1] + 1) + left_bottom_nonzero[1]
                y_column = y.reshape((y.shape[0], 1))
                footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                center_nodes = footprint_nodes_2dim.flatten()
            flag = footprint_edge_type
            if flag != 'C' and self.looped_BCs:
                if array_in is not None:
                    yield (
                     len_x * len_y, array_in)
                else:
                    yield center_nodes
                left_bottom_nonzero_edge = (max_dims_array + left_bottom - 1) % max_dims_array + 1
                right_top_nonzero_edge = (right_top - max_dims_array - 1) % max_dims_array + 1
                if flag == 'N':
                    if array_in is not None:
                        len_x = right_top_nonzero_edge[0] - left_bottom_nonzero_edge[0] + 1
                        len_y = right_top_nonzero_edge[1]
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0] - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1]).reshape((len_y, 1)) + 1
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(right_top_nonzero_edge[0] - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(right_top_nonzero_edge[1]) + 1
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        yield footprint_nodes_2dim.flatten()
                        return

                elif flag == 'S':
                    if array_in is not None:
                        len_x = right_top_nonzero_edge[0] - left_bottom_nonzero_edge[0] + 1
                        len_y = max_rows - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0] - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(right_top_nonzero_edge[0] - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        yield footprint_nodes_2dim.flatten()
                        return

                elif flag == 'E':
                    if array_in is not None:
                        len_x = right_top_nonzero_edge[0]
                        len_y = right_top_nonzero_edge[1] - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1] - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y = numpy.arange(right_top_nonzero_edge[1] - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        yield footprint_nodes_2dim.flatten()
                        return

                elif flag == 'W':
                    if array_in is not None:
                        len_x = max_cols - left_bottom_nonzero_edge[0] + 1
                        len_y = right_top_nonzero_edge[1] - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1] - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(right_top_nonzero_edge[1] - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        yield footprint_nodes_2dim.flatten()
                        return

                elif flag == 'NW':
                    if array_in is not None:
                        len_x = max_cols - left_bottom_nonzero_edge[0] + 1
                        len_y = max_rows - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = right_top_nonzero_edge[0]
                        len_y = right_top_nonzero_edge[1]
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1]).reshape((len_y, 1)) + 1
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = max_cols - left_bottom_nonzero_edge[0] + 1
                        len_y = right_top_nonzero_edge[1]
                        x[:len_x] = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1]).reshape((len_y, 1)) + 1
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        west = footprint_nodes_2dim.flatten()
                        yield west
                        x = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y = numpy.arange(right_top_nonzero_edge[1]) + 1
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        north = footprint_nodes_2dim.flatten()
                        yield north
                        x = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(right_top_nonzero_edge[1]) + 1
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        corner = footprint_nodes_2dim.flatten()
                        yield corner
                        return

                elif flag == 'NE':
                    if array_in is not None:
                        len_x = max_cols - left_bottom_nonzero_edge[0] + 1
                        len_y = right_top_nonzero_edge[1]
                        x[:len_x] = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1]).reshape((len_y, 1)) + 1
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = right_top_nonzero_edge[0]
                        len_y = max_rows - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y_column[:len_y] = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = right_top_nonzero_edge[0]
                        len_y = right_top_nonzero_edge[1]
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1]).reshape((len_y, 1)) + 1
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(right_top_nonzero_edge[1]) + 1
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        north = footprint_nodes_2dim.flatten()
                        yield north
                        x = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        east = footprint_nodes_2dim.flatten()
                        yield east
                        x = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y = numpy.arange(right_top_nonzero_edge[1]) + 1
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        corner = footprint_nodes_2dim.flatten()
                        yield corner
                        return

                elif flag == 'SE':
                    if array_in is not None:
                        len_x = right_top_nonzero_edge[0]
                        len_y = right_top_nonzero_edge[1]
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1]).reshape((len_y, 1)) + 1
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = max_cols - left_bottom_nonzero_edge[0] + 1
                        len_y = max_rows - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = right_top_nonzero_edge[0]
                        len_y = max_rows - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y_column[:len_y] = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y = numpy.arange(right_top_nonzero_edge[1]) + 1
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        east = footprint_nodes_2dim.flatten()
                        yield east
                        x = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        south = footprint_nodes_2dim.flatten()
                        yield south
                        x = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        corner = footprint_nodes_2dim.flatten()
                        yield corner
                        return

                elif flag == 'SW':
                    if array_in is not None:
                        len_x = right_top_nonzero_edge[0]
                        len_y = max_rows - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y_column[:len_y] = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = max_cols - left_bottom_nonzero_edge[0] + 1
                        len_y = right_top_nonzero_edge[1]
                        x[:len_x] = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(right_top_nonzero_edge[1]).reshape((len_y, 1)) + 1
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        len_x = max_cols - left_bottom_nonzero_edge[0] + 1
                        len_y = max_rows - left_bottom_nonzero_edge[1] + 1
                        x[:len_x] = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y_column[:len_y] = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1).reshape((len_y, 1)) + left_bottom_nonzero_edge[1]
                        self.twod_node_store[:len_y, :len_x] = x[:len_x] + y_column[:len_y] * self.grid.number_of_node_columns
                        array_in[:(len_x * len_y)] = self.twod_node_store[:len_y, :len_x].flatten()
                        yield (len_x * len_y, array_in)
                        return
                    else:
                        x = numpy.arange(right_top_nonzero_edge[0]) + 1
                        y = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        south = footprint_nodes_2dim.flatten()
                        yield south
                        x = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(right_top_nonzero_edge[1]) + 1
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        west = footprint_nodes_2dim.flatten()
                        yield west
                        x = numpy.arange(max_cols - left_bottom_nonzero_edge[0] + 1) + left_bottom_nonzero_edge[0]
                        y = numpy.arange(max_rows - left_bottom_nonzero_edge[1] + 1) + left_bottom_nonzero_edge[1]
                        y_column = y.reshape((y.shape[0], 1))
                        footprint_nodes_2dim = x + y_column * self.grid.number_of_node_columns
                        corner = footprint_nodes_2dim.flatten()
                        yield corner
                        return

                else:
                    raise IndexError('Corner flag not set correctly!')
            elif flag == 'C' and self.looped_BCs:
                if array_in is not None:
                    yield (
                     len_x * len_y, array_in)
                    return
                else:
                    yield center_nodes
                    return

            else:
                if array_in is not None:
                    yield (
                     len_x * len_y, array_in)
                    return
                else:
                    yield center_nodes
                    return

        return

    def center_offset_list_for_looped_BCs(self, center_tuple, flag_from_footprint_edge_type, whole_grid_repeats_from_fet):
        """
        This helper method takes the output from the function self.footprint_
        edge_type() and returns a list of center tuples paired with the arrays
        in that output so that iterating on those arrays is easier.
        If the output flag is 'I' (a big footprint), it instead returns a 
        number_of_tiles long list (e.g., 9, 25, 49...) of the relevant
        offsets, in effective ID order (i.e., from bottom left, working across
        line-by-line), as (x, y) tuples.
        
        It needs to be supplied with the second output from self.create_square
        _footprint() also.
        
        This method is a generator.
        """
        grid_x = self.grid.get_grid_xdimension() - self.grid.dx
        grid_y = self.grid.get_grid_ydimension() - self.grid.dx
        assert type(center_tuple) == tuple
        if flag_from_footprint_edge_type == 'I':
            assert type(whole_grid_repeats_from_fet) == int
            for i in xrange(2 * whole_grid_repeats_from_fet + 1):
                x_offset = center_tuple[0] + (i - whole_grid_repeats_from_fet) * grid_x
                for j in xrange(2 * whole_grid_repeats_from_fet + 1):
                    y_offset = center_tuple[1] + (j - whole_grid_repeats_from_fet) * grid_y
                    yield (x_offset, y_offset)

        else:
            yield center_tuple
            if flag_from_footprint_edge_type == 'C' or flag_from_footprint_edge_type == 'X':
                return
            if flag_from_footprint_edge_type == 'N':
                yield (
                 center_tuple[0], center_tuple[1] - grid_y)
                return
            if flag_from_footprint_edge_type == 'S':
                yield (
                 center_tuple[0], center_tuple[1] + grid_y)
                return
            if flag_from_footprint_edge_type == 'E':
                yield (
                 center_tuple[0] - grid_x, center_tuple[1])
                return
            if flag_from_footprint_edge_type == 'W':
                yield (
                 center_tuple[0] + grid_x, center_tuple[1])
                return
            if flag_from_footprint_edge_type == 'NE':
                yield (
                 center_tuple[0], center_tuple[1] - grid_y)
                yield (center_tuple[0] - grid_x, center_tuple[1])
                yield (center_tuple[0] - grid_x, center_tuple[1] - grid_y)
                return
            if flag_from_footprint_edge_type == 'SE':
                yield (
                 center_tuple[0] - grid_x, center_tuple[1])
                yield (center_tuple[0], center_tuple[1] + grid_y)
                yield (center_tuple[0] - grid_x, center_tuple[1] + grid_y)
                return
            if flag_from_footprint_edge_type == 'SW':
                yield (
                 center_tuple[0], center_tuple[1] + grid_y)
                yield (center_tuple[0] + grid_x, center_tuple[1])
                yield (center_tuple[0] + grid_x, center_tuple[1] + grid_y)
                return
            if flag_from_footprint_edge_type == 'NW':
                yield (
                 center_tuple[0] + grid_x, center_tuple[1])
                yield (center_tuple[0], center_tuple[1] - grid_y)
                yield (center_tuple[0] + grid_x, center_tuple[1] - grid_y)
                return
            raise IndexError('boundary type not recognised!')

    def correct_for_slope(self):
        """
        This method uses an empirically observed correlation between surface
        slope and mass_balance to correct the mass balance in the impact back
        towards zero.
        The calibration is performed only for vertical impacts. A second,
        subsequent calibration is needed to correct for impact angle losses (a 
        different geometrical effect).
        It returns 1/(mass_bal+1), which is the multiplier to use on 
        """
        coeffs = numpy.array([1907.25634, -2223.53553, 994.701549,
         -204.517399, 20.4931537, -0.584367364,
         -0.353244682])
        powers = numpy.array([6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0])
        synthetic_mass_balance = coeffs * self._surface_slope ** powers
        return 1.0 / (numpy.sum(synthetic_mass_balance) + 1.0)

    def correct_for_angle_to_vertical(self):
        coeffs = numpy.array([-1.52913024e-11, 3.86656244e-09, -3.8159669e-07,
         1.76792349e-05, -0.000404787246, 0.00304029462,
         0.0428318928])
        powers = numpy.array([6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0])
        synthetic_mass_balance = coeffs * (self._angle_to_vertical * 180.0 / numpy.pi) ** powers
        return 1.0 / (numpy.sum(synthetic_mass_balance) + 1.0)

    def correct_for_crater_size(self):
        """
        NB: the largest crater in the size calibration was 320m in radius.
        Larger craters may have poor mass balances. Though, the mass balance
        problems related to size become much less severe as the craters get
        larger.
        """
        coeffs = numpy.array([-24164.281, 22557.3864, -8137.32097,
         1445.81478, -132.71984, 5.97063876,
         -0.0417789847])
        powers = numpy.array([6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0])
        synthetic_mass_balance = coeffs * self._radius ** powers
        return 1.0 / (numpy.sum(synthetic_mass_balance) + 1.0)

    def excavate_a_crater_noangle(self, grid):
        """
        This method executes the most of the other methods of this crater
        class, and makes the geomorphic changes to a mesh associated with a
        single bolide impact with randomized properties. It receives and works
        on the data fields attached to the model grid. 
        This version calls the _no_angle() method above, and thus produces
        always radially symmetric distributions.
        ***This is one of the primary interface method of this class.***
        """
        self.grid = grid
        self.elev = grid.at_node['topographic_elevation']
        self.draw_new_parameters()
        self.closest_node_index = grid.find_nearest_node((self._xcoord, self._ycoord))
        self.closest_node_elev = self.elev[self.closest_node_index]
        self.check_coords_and_angles_for_grazing()
        self.set_crater_mean_slope_v3()
        self.set_depth_from_size()
        self.set_crater_volume()
        if self._radius != 1e-06:
            if numpy.isnan(self._surface_slope):
                print 'Surface slope is not defined for this crater! Is it too big? Crater will not be drawn.'
            else:
                self.set_elev_change_only_beneath_footprint_no_angular_BAND_AID()
            print 'Mass balance in impact: ', self.mass_balance_in_impact
            self.impact_property_dict = {'x': self._xcoord, 'y': self._ycoord, 'r': self._radius, 'volume': self._cavity_volume, 'surface_slope': self._surface_slope, 'normal_angle': self.impactor_angle_to_surface_normal, 'impact_az': self._azimuth_of_travel, 'ejecta_az': self.ejecta_azimuth, 'mass_balance': self.mass_balance_in_impact, 'redug_crater': self.cheater_flag}
        else:
            self.impact_property_dict = {'x': -1.0, 'y': -1.0, 'r': -1.0, 'volume': -1.0, 'surface_slope': -1.0, 'normal_angle': -1.0, 'impact_az': -1.0, 'ejecta_az': -1.0, 'mass_balance': -1.0, 'redug_crater': -1}
        return self.grid

    def excavate_a_crater_furbish(self, grid, single_process=False):
        """
        This method executes the most of the other methods of this crater
        class, and makes the geomorphic changes to a mesh associated with a
        single bolide impact with randomized properties. It receives and works
        on the data fields attached to the model grid. 
        This version implements the full, angle dependent versions of the
        methods, following Furbish et al., 2007.
        ***This is one of the primary interface method of this class.***
        """
        self.grid = grid
        self.elev = grid.at_node['topographic_elevation']
        self.draw_new_parameters()
        self.closest_node_index = grid.find_nearest_node((self._xcoord, self._ycoord))
        self.closest_node_elev = self.elev[self.closest_node_index]
        self.check_coords_and_angles_for_grazing()
        self.set_crater_mean_slope_v3()
        self.set_depth_from_size()
        self.set_crater_volume()
        if not single_process:
            self.pre_impact_elev = self.elev.copy()
        if self._radius != 1e-06:
            if numpy.isnan(self._surface_slope):
                print 'Surface slope is not defined for this crater! Is it too big? Crater will not be drawn.'
            else:
                self.set_elev_change_only_beneath_footprint_BAND_AID_memory_save()
                print 'Rim thickness: ', self.rim_thickness
            print 'Mass balance in impact: ', self.mass_balance_in_impact
            if self.mass_balance_in_impact < -0.9 or numpy.isnan(self.mass_balance_in_impact):
                print 'radius: ', self._radius
                print 'location: ', self._xcoord, self._ycoord
                print 'surface dip dir: ', self._surface_dip_direction
                print 'surface slope: ', self._surface_slope
                print 'travel azimuth: ', self._azimuth_of_travel
                print 'angle to normal: ', self.impactor_angle_to_surface_normal
                print 'Cavity volume: ', self._cavity_volume
                print 'Rim thickness: ', self.rim_thickness
            print '*****'
        return self.grid

    def crawl_roughness(self, window_dimension, accelerate=True):
        """
        Takes a dimension, D, then passes a DxD window over the elevation grid.
        Returns the mean and standard error (SD/sqrt(n)) of the local relief in
        all windows of that size possible on the grid.
        self.elev_r, the rasterized form of the grid, must already exist.
        """
        D = window_dimension
        reliefs = []
        if accelerate and D / min([self.grid.shape[0], self.grid.shape[1]]) < 0.1:
            for i in xrange(0, self.grid.shape[1] - D, D):
                for j in xrange(0, self.grid.shape[0] - D, D):
                    min_elev = numpy.amin(self.elev_r[j:j + D, i:i + D])
                    max_elev = numpy.amax(self.elev_r[j:j + D, i:i + D])
                    reliefs.append(max_elev - min_elev)

        else:
            for i in xrange(self.grid.shape[1] - D):
                for j in xrange(self.grid.shape[0] - D):
                    min_elev = numpy.amin(self.elev_r[j:j + D, i:i + D])
                    max_elev = numpy.amax(self.elev_r[j:j + D, i:i + D])
                    reliefs.append(max_elev - min_elev)

        reliefs = numpy.array(reliefs)
        mean_relief = numpy.mean(reliefs)
        stderr_relief = numpy.std(reliefs) / numpy.sqrt(len(reliefs))
        return (
         mean_relief, stderr_relief)

    def calculate_scale_roughness_dependence(self, elevations, min_window_size=2, max_window_size=100, step=5):
        self.elev = elevations
        self.elev_r = self.grid.node_vector_to_raster(elevations)
        assert max_window_size < min([self.grid.shape[0], self.grid.shape[1]])
        window_sizes = numpy.arange(min_window_size, max_window_size + 1, step, dtype=int)
        means = []
        stderrs = []
        for i in window_sizes:
            print 'calculating window size ', i
            mean_relief, stderr_relief = self.crawl_roughness(i)
            means.append(mean_relief)
            stderrs.append(stderr_relief)

        return (window_sizes, numpy.array(means), numpy.array(stderrs))

    def calculate_smoothed_ffts(self, elevations, smoothing_window=10000):
        """
        Takes the elevations on the grid, and returns the real part of the fast
        Fourier transform of those elevations, smoothed at the supplied scale.
        Smoothing is applied on a log scale, but the returned values are both in
        their natural forms (i.e., not logged).
        
        Returns the frequency domain values, and the fft real part at each of
        those frequencies.
        """
        self.elev = elevations
        fft = numpy.log(numpy.fft.fft(elevations))
        fftfreq = numpy.fft.fftfreq(len(elevations))
        fftreal = fft.real[numpy.logical_not(numpy.isnan(fftfreq))]
        fftfreq = fftfreq[numpy.logical_not(numpy.isnan(fftfreq))]
        fftfreq_nonan = fftfreq[numpy.logical_not(numpy.isnan(fftreal))]
        fftreal_nonan = fftreal[numpy.logical_not(numpy.isnan(fftreal))]
        fftreal_series = pd.Series(fftreal_nonan)
        fftreal_smoothed = pd.rolling_mean(fftreal_series, smoothing_window)
        return (
         fftfreq_nonan, numpy.exp(fftreal_smoothed))

    @property
    def crater_radius(self):
        return self._radius

    @property
    def impact_xy_location(self):
        return (
         self._xcoord, self._ycoord)

    @property
    def surface_slope_beneath_crater(self):
        return self._surface_slope

    @property
    def surface_dip_direction_beneath_crater(self):
        self._surface_dip_direction

    @property
    def impactor_travel_azimuth(self):
        return self._azimuth_of_travel

    @property
    def impact_angle_to_normal(self):
        return self.impactor_angle_to_surface_normal

    @property
    def cavity_volume(self):
        return self._cavity_volume

    @property
    def ejecta_direction_azimuth(self):
        return self.ejecta_azimuth

    @property
    def mass_balance(self):
        """
        Mass balance in the impact. Negative means mass loss in the impact.
        """
        return self.mass_balance_in_impact

    @property
    def slope_insensitive(self):
        return self.cheater_flag