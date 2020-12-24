# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/craters/dig_craters_copy.py
# Compiled at: 2015-02-11 19:25:27
"""
This component excavates impact craters across a surface. The properties of the
craters broadly follow those observed for the Moon. Craters obey realistic size-
frequency distributions; at the moment this is forced to follow the Shoemaker
scaling, N = k*D^-2.9.
Importantly, this module incorporates a dependence of  ejecta distribution on
impact momentum.
At the moment, this component does not produce complex craters, and all craters
form perpendicular to the geoid (i.e., strength effects are not well
incorporated).
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
            self._xcoord = inputs.read_float('x_position') * (grid.get_grid_xdimension() - grid.dx)
            self._ycoord = inputs.read_float('y_position') * (grid.get_grid_ydimension() - grid.dx)
        except:
            print 'Impact sites will be randomly generated.'
            self.position_auto_flag = 1
            self.set_coords()
        else:
            self.position_auto_flag = 0
            self.closest_node_index = grid.snap_coords_to_grid(self._xcoord, self._ycoord)
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

        self.tan_repose = numpy.tan(32.0 * numpy.pi / 180.0)
        self._beta_factor = 0.5
        self._simple_radius_depth_ratio_Pike = 2.55
        self.V = Symbol('V')
        self.r0 = Symbol('r0')
        self.T = Symbol('T')
        self.r = Symbol('r')
        self.solution_for_rim_thickness = solve(8.0 / 3.0 * self.T * numpy.pi * self.r0 ** 2 + 0.33333 * numpy.pi * self.T * (self.r0 ** 2 + (self.r0 - self.T / self.tan_repose) ** 2 + self.r0 * (self.r0 - self.T / self.tan_repose)) - self.V, self.T)
        self.expression_for_local_thickness = self.T * (self.r / self.r0) ** (-2.75)
        self.impact_property_dict = {}
        print 'Craters component setup complete!'

    def draw_new_parameters(self):
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
        self._xcoord = random() * (grid.get_grid_xdimension() - grid.dx)
        self._ycoord = random() * (grid.get_grid_ydimension() - grid.dx)
        self.closest_node_index = grid.snap_coords_to_grid(self._xcoord, self._ycoord)
        self.closest_node_elev = self.elev[self.closest_node_index]

    def set_impactor_angles(self):
        """
        This method sets the angle of impact, assuming the only effect is
        rotation of the planet under the impactor bombardment (i.e., if the
        target looks like a circle to the oncoming impactor, there's more limb
        area there to hit). As long as target is rotating relative to the sun,
        other (directional) effects should cancel. Angle is given to horizontal.
        Also sets a random azimuth.
        """
        self._angle_to_vertical = numpy.arcsin(random())
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
        radial_points1 = grid.snap_coords_to_grid(radial_points1[0, :], radial_points1[1, :])
        radial_points2 = grid.snap_coords_to_grid(radial_points2[0, :], radial_points2[1, :])
        slope_array = numpy.where(distance_array, (self.elev[radial_points1] - self.elev[radial_points2]) / distance_array, numpy.nan)
        slope_array = numpy.arctan(slope_array)
        try:
            hi_mag_slope_index = numpy.nanargmax(numpy.fabs(slope_array))
            hi_mag_slope = slope_array[hi_mag_slope_index]
        except:
            self._surface_slope = 1e-10
            self._surface_dip_direction = self._azimuth_of_travel
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
        If some of the nodes are off the grid, falls back on v2.
        """
        grid = self.grid
        r = self._radius
        x = self._xcoord
        y = self._ycoord
        dx = grid.dx
        slope_pts = numpy.array([[x - r, y - r], [x, y - r], [x + r, y - r], [x - r, y], [x, y], [x + r, y], [x - r, y + r], [x, y + r], [x + r, y + r]])
        if not numpy.all(grid.is_point_on_grid(slope_pts[:, 0], slope_pts[:, 1])):
            self.set_crater_mean_slope_v2()
        else:
            slope_pts_ongrid = grid.snap_coords_to_grid(slope_pts[:, 0], slope_pts[:, 1])
            cardinal_elevs = self.elev[slope_pts_ongrid]
            S_we = (cardinal_elevs[6] + 2 * cardinal_elevs[3] + cardinal_elevs[0] - (cardinal_elevs[8] + 2 * cardinal_elevs[5] + cardinal_elevs[2])) / (8.0 * dx)
            S_sn = (cardinal_elevs[0] + 2 * cardinal_elevs[1] + cardinal_elevs[2] - (cardinal_elevs[6] + 2 * cardinal_elevs[7] + cardinal_elevs[8])) / (8.0 * dx)
            self._surface_slope = numpy.sqrt(S_we * S_we + S_sn * S_sn)
            try:
                angle_to_xaxis = numpy.arctan(S_sn / S_we)
            except:
                if S_sn < 0.0:
                    self._surface_dip_direction = numpy.pi
                else:
                    self._surface_dip_direction = 0.0
            else:
                self._surface_dip_direction = (1.0 - numpy.sign(S_we)) * 0.5 * numpy.pi + (0.5 * numpy.pi - angle_to_xaxis)

    def set_elev_change_only_beneath_footprint(self):
        """
        This is a method to take an existing impact properties and a known nearest node to the impact site, and alter the topography to model the impact. It assumes crater radius and depth are known, models cavity shape as a power law where n is a function of R/D, and models ejecta thickness as an exponential decay,sensitive to both ballistic range from tilting and momentum transfer in impact (after Furbish). We DO NOT yet model transition to peak ring craters, or enhanced diffusion by ejecta in the strength regime. Peak ring craters are rejected from the distribution. This version of this method is designed to remove the sheer walls around the edges of craters, and replace them with a true dipping rim.
        This routine differs from other set_elev_change...() as it adjusts elevations only on nodes which fall w/i a certain footprint, rather than crawling out from the central impact point to a threshold depth or solving the whole grid. 
        This version of the code does NOT correct for slope dip direction - because Furbish showed momentum almost always wins, and these impactors have a lot of momentum!
        NB - this function ASSUMES that the "beta factor" in the model is <=0.5, i.e., nonlinearities can't develop in the ejecta field, and the impact point is always within the (circular) ejecta footprint.
        Created DEJH Sept 2013.
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
        crater_bowl_exp = self.get_crater_shape_exp()
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
            if 0.0 <= beta_eff <= 90.0:
                _ejecta_azimuth = _azimuth_of_travel
                break
            elif beta_eff < 0.0:
                beta_eff = -beta_eff
                _ejecta_azimuth = (_azimuth_of_travel + pi) % twopi
                break
            else:
                print 'Impact geometry was not possible! Refreshing the impactor angle...'
                self.set_impactor_angles()
                _azimuth_of_travel = self._azimuth_of_travel
                _angle_to_vertical = self._angle_to_vertical

        tan_beta = tan(beta_eff * self._beta_factor)
        tan_beta_sqd = tan_beta * tan_beta
        unique_expression_for_local_thickness = self.create_lambda_fn_for_ejecta_thickness()
        thickness_at_rim = unique_expression_for_local_thickness(_radius)
        max_radius_ejecta_on_flat = _radius * (thickness_at_rim / self._minimum_ejecta_thickness) ** 0.3636
        displacement_distance = max_radius_ejecta_on_flat * tan_beta
        excess_excavation_radius = max_radius_ejecta_on_flat - displacement_distance < _radius
        footprint_center_x = self._xcoord + sin(_azimuth_of_travel) * displacement_distance
        footprint_center_y = self._ycoord + cos(_azimuth_of_travel) * displacement_distance
        footprint_nodes = self.create_square_footprint((footprint_center_x, footprint_center_y), max_radius_ejecta_on_flat)
        if excess_excavation_radius:
            print 'A low-angle crater!'
            cavity_footprint = self.create_square_footprint((self._xcoord, self._ycoord), _radius)
            footprint_nodes = numpy.unique(numpy.concatenate((footprint_nodes, cavity_footprint)))
        _vec_r_to_center, _vec_theta = grid.get_distances_of_nodes_to_point((self._xcoord, self._ycoord), get_az='angles', node_subset=footprint_nodes)
        elevs_under_footprint = elev[footprint_nodes]
        old_elevs_under_footprint = elevs_under_footprint.copy()
        _vec_new_z = numpy.empty_like(_vec_r_to_center)
        _nodes_within_crater = _vec_r_to_center <= _radius
        _nodes_outside_crater = numpy.logical_not(_nodes_within_crater)
        _vec_new_z.fill(self.closest_node_elev + thickness_at_rim - self._depth)
        _vec_new_z[_nodes_within_crater] += self._depth * (_vec_r_to_center[_nodes_within_crater] / _radius) ** crater_bowl_exp
        _vec_new_z[_nodes_outside_crater] += self._depth + (_vec_r_to_center[_nodes_outside_crater] - _radius) * tan_repose
        _nodes_below_surface = _vec_new_z < elevs_under_footprint
        _nodes_above_surface = numpy.logical_not(_nodes_below_surface)
        elevs_under_footprint[_nodes_below_surface] = _vec_new_z[_nodes_below_surface]
        _vec_flat_thickness_above_surface = unique_expression_for_local_thickness(_vec_r_to_center[_nodes_above_surface])
        _vec_theta_eff = _ejecta_azimuth - _vec_theta[_nodes_above_surface]
        _vec_sin_theta_sqd = sin(_vec_theta_eff) ** 2.0
        _vec_cos_theta = cos(_vec_theta_eff)
        _vec_mu_theta_by_mu0 = tan_beta * _vec_cos_theta + sqrt(1.0 - _vec_sin_theta_sqd * tan_beta_sqd)
        _vec_f_theta = (tan_beta_sqd * (_vec_cos_theta ** 2.0 - _vec_sin_theta_sqd) + 2.0 * tan_beta * _vec_cos_theta * sqrt(1.0 - tan_beta_sqd * _vec_sin_theta_sqd) + 1.0) / twopi
        _vec_thickness = _vec_f_theta / _vec_mu_theta_by_mu0 * twopi * _vec_flat_thickness_above_surface
        _vec_thickness_positive = where(_vec_thickness >= 0.0, _vec_thickness, 0.0)
        elevs_under_footprint[_nodes_above_surface] = where(_vec_new_z[_nodes_above_surface] <= elevs_under_footprint[_nodes_above_surface] + _vec_thickness_positive, _vec_new_z[_nodes_above_surface], elevs_under_footprint[_nodes_above_surface] + _vec_thickness_positive)
        self.elev[footprint_nodes] = elevs_under_footprint
        elev_diff = elevs_under_footprint - old_elevs_under_footprint
        self.mass_balance_in_impact = numpy.sum(elev_diff) / -numpy.sum(elev_diff[(elev_diff < 0.0)])
        self.ejecta_azimuth = _ejecta_azimuth
        self.impactor_angle_to_surface_normal = beta_eff
        del _vec_r_to_center
        del _vec_theta
        del _vec_new_z
        del _nodes_below_surface
        del _nodes_above_surface
        del _vec_sin_theta_sqd
        del _vec_mu_theta_by_mu0
        del _vec_f_theta
        del _vec_thickness_positive
        del elevs_under_footprint
        del elev_diff
        return self.elev

    def set_elev_change_only_beneath_footprint_BAND_AID(self):
        """
        This is a method to take an existing impact properties and a known nearest node to the impact site, and alter the topography to model the impact. It assumes crater radius and depth are known, models cavity shape as a power law where n is a function of R/D, and models ejecta thickness as an exponential decay,sensitive to both ballistic range from tilting and momentum transfer in impact (after Furbish). We DO NOT yet model transition to peak ring craters, or enhanced diffusion by ejecta in the strength regime. Peak ring craters are rejected from the distribution. This version of this method is designed to remove the sheer walls around the edges of craters, and replace them with a true dipping rim.
        This routine differs from other set_elev_change...() as it adjusts elevations only on nodes which fall w/i a certain footprint, rather than crawling out from the central impact point to a threshold depth or solving the whole grid. 
        This version of the code does NOT correct for slope dip direction - because Furbish showed momentum almost always wins, and these impactors have a lot of momentum!
        NB - this function ASSUMES that the "beta factor" in the model is <=0.5, i.e., nonlinearities can't develop in the ejecta field, and the impact point is always within the (circular) ejecta footprint.
        Created DEJH Sept 2013.
        This version of this method ("_band_aid"!) uses a quick and dirty fix which substitutes the actual excavated volume into the equn to derive ejecta thicknesses.
        It pays no regard for the inefficiency of doing that!
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
        crater_bowl_exp = self.get_crater_shape_exp()
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
            if 0.0 <= beta_eff <= 90.0:
                _ejecta_azimuth = _azimuth_of_travel
                break
            elif beta_eff < 0.0:
                beta_eff = -beta_eff
                _ejecta_azimuth = (_azimuth_of_travel + pi) % twopi
                break
            else:
                print 'Impact geometry was not possible! Refreshing the impactor angle...'
                self.set_impactor_angles()
                _azimuth_of_travel = self._azimuth_of_travel
                _angle_to_vertical = self._angle_to_vertical

        tan_beta = tan(beta_eff * self._beta_factor)
        tan_beta_sqd = tan_beta * tan_beta
        excavation_nodes = self.create_square_footprint((self._xcoord, self._ycoord), 4.0 * _radius)
        _vec_r_to_center_excav = grid.get_distances_of_nodes_to_point((self._xcoord, self._ycoord), node_subset=excavation_nodes)
        _vec_new_z_excav = numpy.empty_like(_vec_r_to_center_excav)
        _vec_new_z_excav.fill(self.closest_node_elev - 0.9 * self._depth)
        _vec_new_z_excav += self._depth * (_vec_r_to_center_excav / _radius) ** crater_bowl_exp
        z_difference = self.elev[excavation_nodes] - _vec_new_z_excav
        excavated_volume = numpy.sum(numpy.where(z_difference > 0.0, z_difference, 0.0)) * grid.dx * grid.dx
        unique_expression_for_local_thickness = self.create_lambda_fn_for_ejecta_thickness_BAND_AID(excavated_volume)
        thickness_at_rim = unique_expression_for_local_thickness(_radius)
        max_radius_ejecta_on_flat = _radius * (thickness_at_rim / self._minimum_ejecta_thickness) ** 0.3636
        displacement_distance = max_radius_ejecta_on_flat * tan_beta
        excess_excavation_radius = max_radius_ejecta_on_flat - displacement_distance < _radius
        footprint_center_x = self._xcoord + sin(_azimuth_of_travel) * displacement_distance
        footprint_center_y = self._ycoord + cos(_azimuth_of_travel) * displacement_distance
        footprint_nodes = self.create_square_footprint((footprint_center_x, footprint_center_y), max_radius_ejecta_on_flat)
        if excess_excavation_radius:
            print 'A low-angle crater!'
            cavity_footprint = self.create_square_footprint((self._xcoord, self._ycoord), _radius)
            footprint_nodes = numpy.unique(numpy.concatenate((footprint_nodes, cavity_footprint)))
        _vec_r_to_center, _vec_theta = grid.get_distances_of_nodes_to_point((self._xcoord, self._ycoord), get_az='angles', node_subset=footprint_nodes)
        elevs_under_footprint = elev[footprint_nodes]
        old_elevs_under_footprint = elevs_under_footprint.copy()
        _vec_new_z = numpy.empty_like(_vec_r_to_center)
        _nodes_within_crater = _vec_r_to_center <= _radius
        _nodes_outside_crater = numpy.logical_not(_nodes_within_crater)
        _vec_new_z.fill(self.closest_node_elev + thickness_at_rim - self._depth)
        _vec_new_z[_nodes_within_crater] += self._depth * (_vec_r_to_center[_nodes_within_crater] / _radius) ** crater_bowl_exp
        _vec_new_z[_nodes_outside_crater] += self._depth + (_vec_r_to_center[_nodes_outside_crater] - _radius) * tan_repose
        _nodes_below_surface = _vec_new_z < elevs_under_footprint
        _nodes_above_surface = numpy.logical_not(_nodes_below_surface)
        elevs_under_footprint[_nodes_below_surface] = _vec_new_z[_nodes_below_surface]
        _vec_flat_thickness_above_surface = unique_expression_for_local_thickness(_vec_r_to_center[_nodes_above_surface])
        _vec_theta_eff = _ejecta_azimuth - _vec_theta[_nodes_above_surface]
        _vec_sin_theta_sqd = sin(_vec_theta_eff) ** 2.0
        _vec_cos_theta = cos(_vec_theta_eff)
        _vec_mu_theta_by_mu0 = tan_beta * _vec_cos_theta + sqrt(1.0 - _vec_sin_theta_sqd * tan_beta_sqd)
        _vec_f_theta = (tan_beta_sqd * (_vec_cos_theta ** 2.0 - _vec_sin_theta_sqd) + 2.0 * tan_beta * _vec_cos_theta * sqrt(1.0 - tan_beta_sqd * _vec_sin_theta_sqd) + 1.0) / twopi
        _vec_thickness = _vec_f_theta / _vec_mu_theta_by_mu0 * twopi * _vec_flat_thickness_above_surface
        _vec_thickness_positive = where(_vec_thickness >= 0.0, _vec_thickness, 0.0)
        elevs_under_footprint[_nodes_above_surface] = where(_vec_new_z[_nodes_above_surface] <= elevs_under_footprint[_nodes_above_surface] + _vec_thickness_positive, _vec_new_z[_nodes_above_surface], elevs_under_footprint[_nodes_above_surface] + _vec_thickness_positive)
        self.elev[footprint_nodes] = elevs_under_footprint
        elev_diff = elevs_under_footprint - old_elevs_under_footprint
        self.mass_balance_in_impact = numpy.sum(elev_diff) / -numpy.sum(elev_diff[(elev_diff < 0.0)])
        self.ejecta_azimuth = _ejecta_azimuth
        self.impactor_angle_to_surface_normal = beta_eff
        return self.elev

    def set_elev_change_only_beneath_footprint_ballistic_angles(self):
        """
        This is a method to take an existing impact properties and a known nearest node to the impact site, and alter the topography to model the impact. It assumes crater radius and depth are known, models cavity shape as a power law where n is a function of R/D, and models ejecta thickness as an exponential decay,sensitive to both ballistic range from tilting and momentum transfer in impact (after Furbish). We DO NOT yet model transition to peak ring craters, or enhanced diffusion by ejecta in the strength regime. Peak ring craters are rejected from the distribution. This version of this method is designed to remove the sheer walls around the edges of craters, and replace them with a true dipping rim.
        This routine differs from other set_elev_change...() as it adjusts elevations only on nodes which fall w/i a certain footprint, rather than crawling out from the central impact point to a threshold depth or solving the whole grid. 
        This version of the code does NOT correct for slope dip direction - because Furbish showed momentum almost always wins, and these impactors have a lot of momentum!
        NB - this function ASSUMES that the "beta factor" in the model is <=0.5, i.e., nonlinearities can't develop in the ejecta field, and the impact point is always within the (circular) ejecta footprint.
        Created DEJH Sept 2013.
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
        ejection_angle = numpy.pi / 4.0
        crater_bowl_exp = self.get_crater_shape_exp()
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
            if 0.0 <= beta_eff <= 90.0:
                _ejecta_azimuth = _azimuth_of_travel
                break
            elif beta_eff < 0.0:
                beta_eff = -beta_eff
                _ejecta_azimuth = (_azimuth_of_travel + pi) % twopi
                break
            else:
                print 'Impact geometry was not possible! Refreshing the impactor angle...'
                self.set_impactor_angles()
                _azimuth_of_travel = self._azimuth_of_travel
                _angle_to_vertical = self._angle_to_vertical

        tan_beta = tan(beta_eff * self._beta_factor)
        tan_beta_sqd = tan_beta * tan_beta
        unique_expression_for_local_thickness = self.create_lambda_fn_for_ejecta_thickness()
        thickness_at_rim = unique_expression_for_local_thickness(_radius)
        max_radius_ejecta_on_flat = _radius * (thickness_at_rim / self._minimum_ejecta_thickness) ** 0.3636
        max_ejecta_multiple = 1.0 / numpy.cos(_surface_slope) * (1.0 + numpy.tan(_surface_slope) * numpy.tan(ejection_angle))
        footprint_nodes = self.create_square_footprint((self._xcoord, self._ycoord), max_radius_ejecta_on_flat * max_ejecta_multiple)
        _vec_r_to_center, _vec_theta = grid.get_distances_of_nodes_to_point((self._xcoord, self._ycoord), get_az='angles', node_subset=footprint_nodes)
        ballistic_offset_modulator = 1.0 / numpy.cos(_surface_slope) * (1.0 + numpy.cos(_vec_theta - self._surface_dip_direction) * numpy.tan(_surface_slope) * numpy.tan(ejection_angle))
        elevs_under_footprint = elev[footprint_nodes]
        old_elevs_under_footprint = elevs_under_footprint.copy()
        _vec_new_z = numpy.empty_like(_vec_r_to_center)
        _nodes_within_crater = _vec_r_to_center <= _radius
        _nodes_outside_crater = numpy.logical_not(_nodes_within_crater)
        _vec_new_z.fill(self.closest_node_elev + thickness_at_rim - self._depth)
        _vec_new_z[_nodes_within_crater] += self._depth * (_vec_r_to_center[_nodes_within_crater] / _radius) ** crater_bowl_exp
        _vec_new_z[_nodes_outside_crater] += self._depth + (_vec_r_to_center[_nodes_outside_crater] - _radius) * tan_repose
        _nodes_below_surface = _vec_new_z < elevs_under_footprint
        _nodes_above_surface = numpy.logical_not(_nodes_below_surface)
        elevs_under_footprint[_nodes_below_surface] = _vec_new_z[_nodes_below_surface]
        _vec_flat_thickness_above_surface = unique_expression_for_local_thickness(_vec_r_to_center[_nodes_above_surface] * ballistic_offset_modulator[_nodes_above_surface] ** 2.75)
        _vec_theta_eff = _ejecta_azimuth - _vec_theta[_nodes_above_surface]
        _vec_sin_theta_sqd = sin(_vec_theta_eff) ** 2.0
        _vec_cos_theta = cos(_vec_theta_eff)
        _vec_thickness = _vec_flat_thickness_above_surface
        _vec_thickness_positive = where(_vec_thickness >= 0.0, _vec_thickness, 0.0)
        elevs_under_footprint[_nodes_above_surface] = where(_vec_new_z[_nodes_above_surface] <= elevs_under_footprint[_nodes_above_surface] + _vec_thickness_positive, _vec_new_z[_nodes_above_surface], elevs_under_footprint[_nodes_above_surface] + _vec_thickness_positive)
        self.elev[footprint_nodes] = elevs_under_footprint
        elev_diff = elevs_under_footprint - old_elevs_under_footprint
        self.mass_balance_in_impact = numpy.sum(elev_diff) / -numpy.sum(elev_diff[(elev_diff < 0.0)])
        self.ejecta_azimuth = _ejecta_azimuth
        self.impactor_angle_to_surface_normal = beta_eff
        del _vec_r_to_center
        del _vec_theta
        del _vec_new_z
        del _nodes_below_surface
        del _nodes_above_surface
        del _vec_sin_theta_sqd
        del _vec_thickness_positive
        del elevs_under_footprint
        del elev_diff
        return self.elev

    def create_square_footprint(self, center, eff_radius):
        """
        This method creates a square footprint of nodes around a given center
        point, with a specified halfwidth.
        It is designed to avoid the need to actually search the whole grid
        in order to establish the footprint, to accelerate the craters
        module.
        "Center" is a tuple, (x,y).
        """
        assert type(center) == tuple
        assert len(center) == 2
        center_array = numpy.array(center)
        dx = self.grid.dx
        max_cols = self.grid.number_of_node_columns
        max_rows = self.grid.number_of_node_rows
        left_bottom = ((center_array - eff_radius) // dx).astype(int) + 1
        right_top_nonzero = ((center_array + eff_radius) // dx).astype(int)
        left_bottom_nonzero = numpy.where(left_bottom < 0, 0, left_bottom)
        if right_top_nonzero[0] > max_cols - 1:
            right_top_nonzero[0] = max_cols - 1
        if right_top_nonzero[1] > max_rows - 1:
            right_top_nonzero[1] = max_rows - 1
        x = numpy.arange(right_top_nonzero[0] - left_bottom_nonzero[0] + 1) + left_bottom_nonzero[0]
        y = numpy.arange(right_top_nonzero[1] - left_bottom_nonzero[1] + 1) + left_bottom_nonzero[1]
        y_column = y.reshape((y.shape[0], 1))
        footprint_nodes_2dim = x + y_column * max_cols
        return footprint_nodes_2dim.flatten()

    def create_square_footprint_allow_looping(self, center, eff_radius):
        """
        This method creates a square footprint of nodes around a given center
        point, with a specified halfwidth.
        It is designed to avoid the need to actually search the whole grid
        in order to establish the footprint, to accelerate the craters
        module.
        This version returns an array of arrays. The first is the solution on the
        "main" grid. The next eight entries are the areas corresponding to tiled
        looped grids, in the order [SW,S,SE,W,E,NW,N,NE]. If looping is not
        needed, these arrays are returned as numpy.nans.
        "Center" is a tuple, (x,y).
        """
        assert type(center) == tuple
        assert len(center) == 2
        center_array = numpy.array(center)
        dx = self.grid.dx
        max_cols = self.grid.number_of_node_columns
        max_rows = self.grid.number_of_node_rows
        left_bottom = ((center_array - eff_radius) // dx).astype(int) + 1
        right_top = ((center_array + eff_radius) // dx).astype(int)
        right_top_nonzero = numpy.empty(2)
        left_bottom_excesses = numpy.where(left_bottom < 0, -left_bottom, 0)
        right_top_excesses = numpy.empty(2)
        return_list = numpy.empty(9)
        all_excesses = numpy.empty(4)
        all_excesses[0] = left_bottom_excesses[1]
        all_excesses[1] = left_bottom_excesses[0]
        left_bottom_nonzero = numpy.where(left_bottom < 0, 0, left_bottom)
        if right_top[0] > max_cols - 1:
            right_top_nonzero[0] = max_cols - 1
            all_excesses[2] = right_top[0] - max_cols + 1
        else:
            right_top_nonzero[0] = right_top[0]
            all_excesses[2] = 0.0
        if right_top[1] > max_rows - 1:
            right_top_nonzero[1] = max_rows - 1
            all_excesses[3] = right_top[1] - max_rows + 1
        else:
            right_top_nonzero[1] = right_top[1]
            all_excesses[3] = 0.0
        x = numpy.arange(right_top_nonzero[0] - left_bottom_nonzero[0] + 1) + left_bottom_nonzero[0]
        y = numpy.arange(right_top_nonzero[1] - left_bottom_nonzero[1] + 1) + left_bottom_nonzero[1]
        y_column = y.reshape((y.shape[0], 1))
        footprint_nodes_2dim = x + y_column * max_cols
        return_list[0] = footprint_nodes_2dim.flatten()
        unsaturated_excesses = numpy.empty(4)
        unsaturated_excesses[[0, 3]] = numpy.where(all_excesses[[0, 3]] // max_rows == 0.0, all_excesses[[0, 3]], max_rows - 1)
        unsaturated_excesses[[1, 2]] = numpy.where(all_excesses[[1, 2]] // max_cols == 0.0, all_excesses[[1, 2]], max_cols - 1)
        if unsaturated_excesses[0] and unsaturated_excesses[1]:
            x = numpy.arange(unsaturated_excesses[1] + 1) + unsaturated_excesses[1]
            y = numpy.arange(unsaturated_excesses[0] + 1) + unsaturated_excesses[0]
            y_column = y.reshape((y.shape[0], 1))
            return_list[1] = (x + y_column * max_cols).flatten()
            if unsaturated_excesses[2]:
                x = numpy.arange(max_cols + 1)
                return_list[2] = (x + y_column * max_cols).flatten()
                x = numpy.arange(unsaturated_excesses[2] + 1)
                return_list[3] = (x + y_column * max_cols).flatten()
            else:
                x = numpy.arange(right_top_nonzero[0] + 1)
                return_list[2] = (x + y_column * max_cols).flatten()
                return_list[3] = numpy.nan
            if unsaturated_excesses[3]:
                x = numpy.arange(unsaturated_excesses[1] + 1) + unsaturated_excesses[1]
                y = numpy.arange(max_rows + 1)
                y_column = y.reshape((y.shape[0], 1))
                return_list[4] = (x + y_column * max_cols).flatten()
                y = numpy.arange(unsaturated_excesses[3] + 1)
                y_column = y.reshape((y.shape[0], 1))
                return_list[6] = (x + y_column * max_cols).flatten()
            else:
                y = numpy.arange(right_top_nonzero[1] + 1)
                y_column = y.reshape((y.shape[0], 1))
                return_list[4] = (x + y_column * max_cols).flatten()
                return_list[6] = numpy.nan
        if unsaturated_excesses[0] and not unsaturated_excesses[1] and not unsaturated_excesses[2]:
            x = numpy.arange(right_top_nonzero[0] - left_bottom_nonzero[0] + 1) + left_bottom_nonzero[0]
            y = numpy.arange(unsaturated_excesses[0] + 1) + unsaturated_excesses[0]
            y_column = y.reshape((y.shape[0], 1))
            return_list[2] = (x + y_column * max_cols).flatten()
            return_list[1] = numpy.nan
            return_list[3] = numpy.nan
        if unsaturated_excesses[1] and not unsaturated_excesses[0] and not unsaturated_excesses[3]:
            x = numpy.arange(unsaturated_excesses[1] + 1) + unsaturated_excesses[1]
            y = numpy.arange(right_top_nonzero[1] - left_bottom_nonzero[1] + 1) + left_bottom_nonzero[1]
            y_column = y.reshape((y.shape[0], 1))
            return_list[2] = (x + y_column * max_cols).flatten()
            return_list[1] = numpy.nan
            return_list[3] = numpy.nan
        if unsaturated_excesses[3] and unsaturated_excesses[1]:
            x = numpy.arange(unsaturated_excesses[1] + 1) + unsaturated_excesses[1]
            y = numpy.arange(unsaturated_excesses[3] + 1)
            y_column = y.reshape((y.shape[0], 1))
            return_list[1] = (x + y_column * max_cols).flatten()
        return footprint_nodes_2dim.flatten()

    def excavate_a_crater(self, grid):
        """
        This method executes the most of the other methods of this crater
        class, and makes the geomorphic changes to a mesh associated with a
        single bolide impact with randomized properties. It receives
        parameters of the model grid, and the vector data storage class. It
        is the primary interface method of this class.
        This method is optimized to only calculate the elevation changes for
        an impact within its ejecta footprint.
        """
        self.grid = grid
        self.elev = grid.at_node['topographic_elevation']
        self.draw_new_parameters()
        self.set_depth_from_size()
        self.set_crater_volume()
        self.closest_node_index = grid.snap_coords_to_grid(self._xcoord, self._ycoord)
        self.closest_node_elev = self.elev[self.closest_node_index]
        self.set_crater_mean_slope_v3()
        if numpy.isnan(self._surface_slope):
            print 'Surface slope is not defined for this crater! Is it too big? Crater will not be drawn.'
        else:
            self.set_elev_change_only_beneath_footprint()
        print 'Mass balance in impact: ', self.mass_balance_in_impact
        self.impact_property_dict = {'x': self._xcoord, 'y': self._ycoord, 'r': self._radius, 'volume': self._cavity_volume, 'surface_slope': self._surface_slope, 'normal_angle': self.impactor_angle_to_surface_normal, 'impact_az': self._azimuth_of_travel, 'ejecta_az': self.ejecta_azimuth, 'mass_balance': self.mass_balance_in_impact}
        return self.grid