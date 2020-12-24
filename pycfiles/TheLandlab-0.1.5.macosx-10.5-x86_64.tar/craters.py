# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/components/craters/craters.py
# Compiled at: 2014-09-23 12:37:24
"""
.. deprecated:: 0.4
This code is no longer supported.
Use 'dig_craters.py" instead.
"""
from random import random
import math, numpy
from collections import deque
import sys, time, scipy.optimize as opt
from sympy import Symbol
from sympy.solvers import solve
from sympy.utilities.lambdify import lambdify
from landlab import RasterModelGrid
from pylab import plot, draw, show, contour, imshow, colorbar
from copy import deepcopy as copy

class data(object):
    """
    This is where all the whole-grid data lives, as arrays over the various elements of the grid.
    """

    def __init__(self, grid):
        self.elev = grid.zeros(centering='node')
        self.flag_already_in_the_list = grid.zeros(centering='node')
        self.craters_over_max_radius_not_plotted = grid.zeros(centering='node')
        self.impact_sequence = []


class impactor(object):
    """
    This class holds all parameters decribing properties of a single impact structure, and contains methods for recalculating fresh and internally consistent data describing such a impact structure.
    Built DEJH Spring 2013.
    """

    def __init__(self, min_radius=0.005):
        self._xcoord = -999.0
        self._ycoord = -999.0
        self.tan_repose = numpy.tan(32.0 * numpy.pi / 180.0)
        self._str_regime_cutoff = 0.3
        self._simple_radius_depth_ratio_Pike = 2.55
        self._simple_cr_radius_cutoff = 7.5
        self._complex_cr_radius_cutoff = 10.0
        self._max_complex_cr_radius = 70.0
        self._minimum_crater = min_radius
        self.ivanov_a = [-3.0876, -3.557528, 0.781027, 1.021521, -0.156012, -0.444058, 0.019977, 0.08685, -0.005874, -0.006809, 0.000825, 5.54e-05]
        self._impactor_angle_to_surface = -999.0
        self._angle_to_vertical = -999.0
        self._minimum_ejecta_thickness = 1e-08
        self._beta_factor = 0.5
        self.total_counted_craters = self.ivanov_prod_equ_as_Nequals(self._minimum_crater * 2.0)
        self.ivanov_prod_fn = lambda x, N_as_fraction: self.ivanov_prod_equ(x, N_as_fraction / self.total_counted_craters)
        self.ivanov_prod_fn_1stderiv = lambda x, N_as_fraction: self.ivanov_prod_equ_1stderiv(x, N_as_fraction)
        self.V = Symbol('V')
        self.r0 = Symbol('r0')
        self.T = Symbol('T')
        self.r = Symbol('r')
        self.solution_for_rim_thickness = solve(8.0 / 3.0 * self.T * numpy.pi * self.r0 ** 2 + 0.33333 * numpy.pi * self.T * (self.r0 ** 2 + (self.r0 - self.T / self.tan_repose) ** 2 + self.r0 * (self.r0 - self.T / self.tan_repose)) - self.V, self.T)
        self.expression_for_local_thickness = self.T * (self.r / self.r0) ** (-2.75)

    def get_complex_radius_depth_ratio(self):
        """
        This method returns the ratio of radius to max depth for a complex crater, which is itself a function of that crater's radius. This equation is from Pike '77, as quoted in Holsapple '93, p. 358.
        """
        return self._radius ** 0.7

    def get_crater_shape_exp(self):
        """
        This method assumes the max depth and radius of a crater are known. It provides n for a power law of form d = D*(r/R)**n, where D and R are the known values, by assuming the outer edges of the crater sit at angle of repose. This gives very sensible answers; n~2 for big, complex craters (Garvin et al, 2000, p.333: "There is a strong tendency for craters to become more paraboloidal with increasing diameter, independent of location.") and n~1.3 for ~2km simple craters (Garvin following Croft has ~1.18).
        """
        return 0.51 * self._radius / self._depth

    def get_complex_peak_radius(self):
        """
        This method returns the radial distance to the edge of a complex crater central mound, based on the crater radius. This follows an equation presented in Melosh's Planetary Surface Processes.
        """
        return 0.22 * self._radius

    def get_complex_peak_str_uplift(self):
        """
        This method returns the radial maximum structural uplift, interpreted as a height, of a complex crater central mound, based on the crater radius. This follows an equation presented in Melosh's Planetary Surface Processes, adjusted for R, not D.
        """
        return 0.13 * self._radius ** 1.1

    def ivanov_prod_equ(self, D, N):
        """
        This function expresses the crater production function after Ivanov, 1999, in the form 0 = f(D, N). N is the total number density of craters greater than x diameter. Remember, N is in km^-2 Ga^-1. If N = N_counted / N_max, then this is the CPF which will yield the PDF when solved for D given N.
        """
        sum_terms = numpy.empty(12, dtype=float)
        sum_terms[0] = self.ivanov_a[0] - math.log10(N)
        for i in range(1, 12):
            sum_terms[i] = self.ivanov_a[i] * math.log10(D) ** i

        return numpy.sum(sum_terms)

    def ivanov_prod_equ_as_Nequals(self, D):
        """
        This function expresses Ivanov's CPF in the normal form, N = f(D). It returns N (not log10(N)!).
        """
        sum_terms = numpy.empty(12, dtype=float)
        for i in range(0, 12):
            sum_terms[i] = self.ivanov_a[i] * math.log10(D) ** i

        return pow(10.0, numpy.sum(sum_terms))

    def ivanov_prod_equ_1stderiv(self, D, N):
        """
        This is a helper function for the Newton-Raphson optimized solver in solve_ivanov_for_crater_diam. It returns the first derivative for the production function. Note that the N term is a dummy variable used for consistency in the opt.newton(), and does nothing here.
        """
        sum_terms = numpy.empty(11, dtype=float)
        ln_of_10 = math.log(10)
        for i in range(1, 12):
            sum_terms[i - 1] = self.ivanov_a[i] * i * math.log(D) ** (i - 1.0) / ln_of_10 ** i

        return numpy.sum(sum_terms) / D

    def ivanov_prod_equ_2ndderiv(self, D):
        """
        This is a helper function for the Newton-Raphson optimized solver in solve_ivanov_for_crater_diam. It returns the second derivative for the production function.
        """
        ln_of_10 = math.log(10)
        sum_terms = numpy.empty(11, dtype=float)
        sum_terms[0] = self.ivanov_a[1] / ln_of_10
        for i in range(2, 12):
            sum_terms[i - 1] = i * self.ivanov_a[i] * (math.log(D) - i + 1.0) * math.log(D) ** (i - 2.0) / ln_of_10 ** i

        return -numpy.sum(sum_terms) / (D * D)

    def solve_ivanov_for_crater_diam(self, N_by_fract):
        """
        Uses a Newton Raphson method to return a random diameter drawn from an Ivanov crater distribution, when provided with a uniformly distributed random number 0->1.
        """
        args_in = (
         N_by_fract,)
        x_0 = (10.0 ** self.ivanov_a[0] / (self.total_counted_craters * N_by_fract)) ** 0.345
        return opt.newton(func=self.ivanov_prod_fn, x0=x_0, fprime=self.ivanov_prod_fn_1stderiv, args=args_in, tol=0.001)

    def set_cr_radius_from_shoemaker(self, data):
        """
        This method is a less accurate (but faster) alternative to the Newton-Raphson-on-Ivanov-distn also available in this object. It takes a random number between 0 and 1, and returns a crater radius based on a py distn N = kD^-2.9, following Shoemaker et al., 1970.
        """
        self._radius = self._minimum_crater * random() ** (-0.345)
        if self._radius > self._max_complex_cr_radius:
            data.craters_over_max_radius_not_plotted.append(self._radius)
            print 'Drew a crater above the maximum permitted size. Drawing a new crater...'
            self.set_size(data)

    def set_coords(self, grid, data):
        """
        This method selects a random location inside the grid onto which to map an impact. It also sets variables for the closest grid node to the impact, and the elevation at that node.
        """
        self._xcoord = random() * grid.get_grid_xdimension()
        self._ycoord = random() * grid.get_grid_ydimension()
        self.closest_node_index = grid.snap_coords_to_grid(self._xcoord, self._ycoord)
        self.closest_node_elev = data.elev[self.closest_node_index]

    def set_impactor_angles(self):
        """
        This method sets the angle of impact, assuming the only effect is rotation of the planet under the impactor bombardment (i.e., if the target looks like a circle to the oncoming impactor, there's more limb area there to hit). As long as target is rotating relative to the sun, other (directional) effects should cancel. Angle is given to horizontal. Also sets a random azimuth.
        """
        self._angle_to_vertical = numpy.arcsin(random())
        self._azimuth_of_travel = random() * 2.0 * numpy.pi

    def set_size(self, data):
        """
        This method draws a crater radius at random from the PDF describing crater sizes dictated by the Ivanov distribution, with the probability of obtaining that crater size depending on the relative abundance of that size. Note this method works with the Ivanov distribution according to diameter, but returns a radius.
        """
        self._radius = 0.5 * self.solve_ivanov_for_crater_diam(random())
        if self._radius > self._max_complex_cr_radius:
            data.craters_over_max_radius_not_plotted.append(self._radius)
            print 'Drew a crater above the maximum permitted size. Drawing a new crater...'
            self.set_size(data)

    def set_depth_from_size(self):
        """
        This method sets a known crater with diameter as either simple or complex, then sets its maximum depth at the center (inferred for complex craters).
        """
        if self._radius < self._simple_cr_radius_cutoff:
            self._crater_type = 0
        elif self._radius > self._complex_cr_radius_cutoff:
            self._crater_type = 1
        else:
            py_complex_at_radius = (self._radius - self._simple_cr_radius_cutoff) / (self._complex_cr_radius_cutoff - self._simple_cr_radius_cutoff)
            if random() > py_complex_at_radius:
                self._crater_type = 0
            else:
                self._crater_type = 1
        if not self._crater_type:
            self._depth = self._radius / self._simple_radius_depth_ratio_Pike
        else:
            self._depth = self._radius / self.get_complex_radius_depth_ratio()
            self._complex_peak_radius = self.get_complex_peak_radius()
            self._complex_peak_str_uplift = self.get_complex_peak_str_uplift()
        print 'Depth: ', self._depth

    def set_crater_volume(self):
        """
        This method uses known crater depth and radius and sets the volume of the excavated cavity.
        """
        self._cavity_volume = 0.51 * numpy.pi * self._depth * self._radius ** 3.0 / (0.51 * self._radius + 2.0 * self._depth)

    def create_lambda_fn_for_ejecta_thickness(self):
        """
        This method takes the complicated equation that relates "flat" ejecta thickness (symmetrical, with impact angle=0) to radius and cavity volume which is set in __init__(), and solves it for a given pair of impact specific parameters, V_cavity & crater radius.
        Both the cavity volume and crater radius need to have been set before this method is called.
        Method returns a lambda function for the radially symmetrical ejecta thickness distribution as a function of distance from crater center, r. i.e., call unique_expression_for_local_thickness(r) to calculate a thickness.
        Added DEJH Sept 2013.
        """
        local_solution_for_rim_thickness = self.solution_for_rim_thickness[0].subs(self.V, self._cavity_volume)
        unique_expression_for_local_thickness = self.expression_for_local_thickness.subs({self.r0: self._radius, self.T: local_solution_for_rim_thickness})
        unique_expression_for_local_thickness = lambdify(self.r, unique_expression_for_local_thickness)
        return unique_expression_for_local_thickness

    def set_crater_mean_slope_v2(self, grid, data):
        """
        This method takes a crater of known radius, and which has already been "snapped" to the grid through snap_impact_to_grid(mygrid), and returns a spatially averaged value for the local slope of the preexisting topo beneath the cavity footprint. This version of the method works by taking four transects across the crater area every 45 degrees around its rim, calculating the slope along each, then setting the slope as the greatest, positive downwards and in the appropriate D8 direction. This function also sets the mean surface dip direction.
        In here, we start to assume a convex and structured grid, such that if pts N and W on the rim are in the grid, so is the point NW.
        This version is vectorized, and so hopefully faster.
        DEJH, Sept 2013.
        """
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
        slope_array = numpy.where(distance_array, (data.elev[radial_points1] - data.elev[radial_points2]) / distance_array, numpy.nan)
        slope_array = numpy.arctan(slope_array)
        try:
            hi_mag_slope_index = numpy.nanargmax(numpy.fabs(slope_array))
            hi_mag_slope = slope_array[hi_mag_slope_index]
        except:
            self.surface_slope = 1e-10
            self.surface_dip_direction = self._azimuth_of_travel
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
            print 'The slope under the crater cavity footprint is: ', self._surface_slope

    def set_elev_change_crawler--- This code section failed: ---

 L. 328         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_angle_to_vertical'
                6  STORE_FAST            3  '_angle_to_vertical'

 L. 329         9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             1  '_surface_slope'
               15  STORE_FAST            4  '_surface_slope'

 L. 330        18  LOAD_FAST             0  'self'
               21  LOAD_ATTR             2  '_surface_dip_direction'
               24  STORE_FAST            5  '_surface_dip_direction'

 L. 331        27  LOAD_FAST             0  'self'
               30  LOAD_ATTR             3  '_azimuth_of_travel'
               33  STORE_FAST            6  '_azimuth_of_travel'

 L. 332        36  LOAD_GLOBAL           4  'numpy'
               39  LOAD_ATTR             5  'pi'
               42  STORE_FAST            7  'pi'

 L. 333        45  LOAD_CONST               2.0
               48  LOAD_FAST             7  'pi'
               51  BINARY_MULTIPLY  
               52  STORE_FAST            8  'twopi'

 L. 334        55  LOAD_GLOBAL           4  'numpy'
               58  LOAD_ATTR             6  'tan'
               61  STORE_FAST            9  'tan'

 L. 335        64  LOAD_GLOBAL           4  'numpy'
               67  LOAD_ATTR             7  'cos'
               70  STORE_FAST           10  'cos'

 L. 336        73  LOAD_GLOBAL           4  'numpy'
               76  LOAD_ATTR             8  'sin'
               79  STORE_FAST           11  'sin'

 L. 337        82  LOAD_GLOBAL           4  'numpy'
               85  LOAD_ATTR             9  'sqrt'
               88  STORE_FAST           12  'sqrt'

 L. 339        91  LOAD_GLOBAL           4  'numpy'
               94  LOAD_ATTR            10  'arccos'
               97  STORE_FAST           13  'arccos'

 L. 341       100  LOAD_FAST             0  'self'
              103  LOAD_ATTR            11  '_radius'
              106  STORE_FAST           14  '_radius'

 L. 342       109  LOAD_FAST             0  'self'
              112  LOAD_ATTR            12  'tan_repose'
              115  STORE_FAST           15  'tan_repose'

 L. 343       118  LOAD_CONST               0.0
              121  LOAD_FAST             0  'self'
              124  STORE_ATTR           13  'mass_balance_in_impact'

 L. 344       127  LOAD_CONST               0.0
              130  STORE_FAST           16  'crater_vol_below_ground'

 L. 347       133  LOAD_GLOBAL          14  'deque'
              136  LOAD_FAST             0  'self'
              139  LOAD_ATTR            15  'closest_node_index'
              142  BUILD_LIST_1          1 
              145  CALL_FUNCTION_1       1  None
              148  STORE_FAST           17  'crater_node_list'

 L. 350       151  LOAD_GLOBAL           4  'numpy'
              154  LOAD_ATTR            16  'zeros'
              157  LOAD_FAST             1  'grid'
              160  LOAD_ATTR            17  'number_of_nodes'
              163  CALL_FUNCTION_1       1  None
              166  STORE_FAST           18  'flag_already_in_the_list'

 L. 353       169  LOAD_FAST             0  'self'
              172  LOAD_ATTR            18  'get_crater_shape_exp'
              175  CALL_FUNCTION_0       0  None
              178  STORE_FAST           19  'crater_bowl_exp'

 L. 354       181  LOAD_CONST               'Crater shape exponent: '
              184  PRINT_ITEM       
              185  LOAD_FAST            19  'crater_bowl_exp'
              188  PRINT_ITEM_CONT  
              189  PRINT_NEWLINE_CONT

 L. 357       190  SETUP_LOOP          349  'to 542'

 L. 359       193  LOAD_FAST             5  '_surface_dip_direction'
              196  LOAD_FAST             6  '_azimuth_of_travel'
              199  BINARY_SUBTRACT  
              200  STORE_FAST           20  'rake_in_surface_plane'

 L. 360       203  LOAD_CONST               '_surface_dip_direction: '
              206  PRINT_ITEM       
              207  LOAD_FAST             5  '_surface_dip_direction'
              210  PRINT_ITEM_CONT  
              211  PRINT_NEWLINE_CONT

 L. 361       212  LOAD_CONST               '_azimuth_of_travel: '
              215  PRINT_ITEM       
              216  LOAD_FAST             6  '_azimuth_of_travel'
              219  PRINT_ITEM_CONT  
              220  PRINT_NEWLINE_CONT

 L. 362       221  LOAD_CONST               '_angle_to_vertical: '
              224  PRINT_ITEM       
              225  LOAD_FAST             3  '_angle_to_vertical'
              228  PRINT_ITEM_CONT  
              229  PRINT_NEWLINE_CONT

 L. 363       230  LOAD_GLOBAL           4  'numpy'
              233  LOAD_ATTR            19  'fabs'
              236  LOAD_FAST            20  'rake_in_surface_plane'
              239  CALL_FUNCTION_1       1  None
              242  STORE_FAST           21  'absolute_rake'

 L. 364       245  LOAD_FAST             4  '_surface_slope'
              248  POP_JUMP_IF_TRUE    266  'to 266'

 L. 365       251  LOAD_CONST               0.0
              254  STORE_FAST           22  'epsilon'

 L. 366       257  LOAD_FAST             3  '_angle_to_vertical'
              260  STORE_FAST           23  'beta_eff'
              263  JUMP_FORWARD        156  'to 422'

 L. 368       266  LOAD_FAST            21  'absolute_rake'
              269  LOAD_CONST               0.5
              272  LOAD_FAST             7  'pi'
              275  BINARY_MULTIPLY  
              276  LOAD_CONST               1.5
              279  LOAD_FAST             7  'pi'
              282  BINARY_MULTIPLY  
              283  BUILD_TUPLE_2         2 
              286  COMPARE_OP            6  in
              289  POP_JUMP_IF_FALSE   301  'to 301'

 L. 369       292  LOAD_CONST               0.0
              295  STORE_FAST           22  'epsilon'
              298  JUMP_FORWARD         62  'to 363'

 L. 371       301  LOAD_FAST            13  'arccos'
              304  LOAD_FAST            10  'cos'
              307  LOAD_FAST            20  'rake_in_surface_plane'
              310  CALL_FUNCTION_1       1  None
              313  LOAD_FAST            10  'cos'
              316  LOAD_FAST             4  '_surface_slope'
              319  CALL_FUNCTION_1       1  None
              322  BINARY_MULTIPLY  
              323  LOAD_FAST            12  'sqrt'
              326  LOAD_CONST               1.0
              329  LOAD_FAST             9  'tan'
              332  LOAD_FAST            20  'rake_in_surface_plane'
              335  CALL_FUNCTION_1       1  None
              338  LOAD_FAST            10  'cos'
              341  LOAD_FAST             4  '_surface_slope'
              344  CALL_FUNCTION_1       1  None
              347  BINARY_DIVIDE    
              348  LOAD_CONST               2.0
              351  BINARY_POWER     
              352  BINARY_ADD       
              353  CALL_FUNCTION_1       1  None
              356  BINARY_MULTIPLY  
              357  CALL_FUNCTION_1       1  None
              360  STORE_FAST           22  'epsilon'
            363_0  COME_FROM           298  '298'

 L. 373       363  LOAD_FAST            21  'absolute_rake'
              366  LOAD_CONST               0.5
              369  LOAD_FAST             7  'pi'
              372  BINARY_MULTIPLY  
              373  COMPARE_OP            1  <=
              376  POP_JUMP_IF_TRUE    395  'to 395'
              379  LOAD_FAST            21  'absolute_rake'
              382  LOAD_CONST               1.5
              385  LOAD_FAST             7  'pi'
              388  BINARY_MULTIPLY  
              389  COMPARE_OP            5  >=
            392_0  COME_FROM           376  '376'
              392  POP_JUMP_IF_FALSE   408  'to 408'

 L. 374       395  LOAD_FAST             3  '_angle_to_vertical'
              398  LOAD_FAST            22  'epsilon'
              401  BINARY_ADD       
              402  STORE_FAST           23  'beta_eff'
              405  JUMP_FORWARD         14  'to 422'

 L. 376       408  LOAD_FAST             3  '_angle_to_vertical'
              411  LOAD_FAST            22  'epsilon'
              414  BINARY_ADD       
              415  LOAD_FAST             7  'pi'
              418  BINARY_SUBTRACT  
              419  STORE_FAST           23  'beta_eff'
            422_0  COME_FROM           405  '405'
            422_1  COME_FROM           263  '263'

 L. 377       422  LOAD_CONST               'Beta effective: '
              425  PRINT_ITEM       
              426  LOAD_FAST            23  'beta_eff'
              429  PRINT_ITEM_CONT  
              430  PRINT_NEWLINE_CONT

 L. 379       431  LOAD_CONST               0.0
              434  LOAD_FAST            23  'beta_eff'
              437  DUP_TOP          
              438  ROT_THREE        
              439  COMPARE_OP            1  <=
              442  JUMP_IF_FALSE_OR_POP   454  'to 454'
              445  LOAD_CONST               90.0
              448  COMPARE_OP            1  <=
              451  JUMP_FORWARD          2  'to 456'
            454_0  COME_FROM           442  '442'
              454  ROT_TWO          
              455  POP_TOP          
            456_0  COME_FROM           451  '451'
              456  POP_JUMP_IF_FALSE   469  'to 469'

 L. 380       459  LOAD_FAST             6  '_azimuth_of_travel'
              462  STORE_FAST           24  '_ejecta_azimuth'

 L. 381       465  BREAK_LOOP       
              466  JUMP_BACK           193  'to 193'

 L. 382       469  LOAD_FAST            23  'beta_eff'
              472  LOAD_CONST               0.0
              475  COMPARE_OP            0  <
              478  POP_JUMP_IF_FALSE   506  'to 506'

 L. 384       481  LOAD_FAST            23  'beta_eff'
              484  UNARY_NEGATIVE   
              485  STORE_FAST           23  'beta_eff'

 L. 385       488  LOAD_FAST             6  '_azimuth_of_travel'
              491  LOAD_FAST             7  'pi'
              494  BINARY_ADD       
              495  LOAD_FAST             8  'twopi'
              498  BINARY_MODULO    
              499  STORE_FAST           24  '_ejecta_azimuth'

 L. 386       502  BREAK_LOOP       
              503  JUMP_BACK           193  'to 193'

 L. 388       506  LOAD_CONST               'Impact geometry was not possible! Refreshing the impactor angle...'
              509  PRINT_ITEM       
              510  PRINT_NEWLINE_CONT

 L. 389       511  LOAD_FAST             0  'self'
              514  LOAD_ATTR            20  'set_impactor_angles'
              517  CALL_FUNCTION_0       0  None
              520  POP_TOP          

 L. 390       521  LOAD_FAST             0  'self'
              524  LOAD_ATTR             3  '_azimuth_of_travel'
              527  STORE_FAST            6  '_azimuth_of_travel'

 L. 391       530  LOAD_FAST             0  'self'
              533  LOAD_ATTR             0  '_angle_to_vertical'
              536  STORE_FAST            3  '_angle_to_vertical'
              539  JUMP_BACK           193  'to 193'
            542_0  COME_FROM           190  '190'

 L. 394       542  LOAD_FAST             9  'tan'
              545  LOAD_FAST            23  'beta_eff'
              548  LOAD_FAST             0  'self'
              551  LOAD_ATTR            21  '_beta_factor'
              554  BINARY_MULTIPLY  
              555  CALL_FUNCTION_1       1  None
              558  STORE_FAST           25  'tan_beta'

 L. 395       561  LOAD_FAST            25  'tan_beta'
              564  LOAD_FAST            25  'tan_beta'
              567  BINARY_MULTIPLY  
              568  STORE_FAST           26  'tan_beta_sqd'

 L. 398       571  LOAD_FAST             0  'self'
              574  LOAD_ATTR            22  'create_lambda_fn_for_ejecta_thickness'
              577  CALL_FUNCTION_0       0  None
              580  STORE_FAST           27  'unique_expression_for_local_thickness'

 L. 399       583  LOAD_FAST            27  'unique_expression_for_local_thickness'
              586  LOAD_FAST            14  '_radius'
              589  CALL_FUNCTION_1       1  None
              592  STORE_FAST           28  'thickness_at_rim'

 L. 400       595  LOAD_CONST               'thickness_at_rim: '
              598  PRINT_ITEM       
              599  LOAD_FAST            28  'thickness_at_rim'
              602  PRINT_ITEM_CONT  
              603  PRINT_NEWLINE_CONT

 L. 403       604  SETUP_LOOP          728  'to 1335'
            607_0  COME_FROM           633  '633'

 L. 404       607  SETUP_EXCEPT         16  'to 626'

 L. 405       610  LOAD_FAST            17  'crater_node_list'
              613  LOAD_ATTR            23  'popleft'
              616  CALL_FUNCTION_0       0  None
              619  STORE_FAST           29  'active_node'
              622  POP_BLOCK        
              623  JUMP_FORWARD          8  'to 634'
            626_0  COME_FROM           607  '607'

 L. 406       626  POP_TOP          
              627  POP_TOP          
              628  POP_TOP          

 L. 407       629  BREAK_LOOP       
              630  JUMP_BACK           607  'to 607'
              633  END_FINALLY      
            634_0  COME_FROM           623  '623'

 L. 409       634  LOAD_FAST             2  'data'
              637  LOAD_ATTR            24  'elev'
              640  LOAD_FAST            29  'active_node'
              643  BINARY_SUBSCR    
              644  STORE_FAST           30  'pre_elev'

 L. 410       647  LOAD_FAST             1  'grid'
              650  LOAD_ATTR            25  'get_distances_of_nodes_to_point'
              653  LOAD_FAST             0  'self'
              656  LOAD_ATTR            26  '_xcoord'
              659  LOAD_FAST             0  'self'
              662  LOAD_ATTR            27  '_ycoord'
              665  BUILD_TUPLE_2         2 
              668  LOAD_CONST               'get_az'
              671  LOAD_CONST               'angles'
              674  LOAD_CONST               'node_subset'
              677  LOAD_FAST            29  'active_node'
              680  CALL_FUNCTION_513   513  None
              683  UNPACK_SEQUENCE_2     2 
              686  STORE_FAST           31  '_r_to_center'
              689  STORE_FAST           32  '_theta'

 L. 415       692  LOAD_FAST             0  'self'
              695  LOAD_ATTR            28  'closest_node_elev'
              698  LOAD_FAST            28  'thickness_at_rim'
              701  BINARY_ADD       
              702  LOAD_FAST             0  'self'
              705  LOAD_ATTR            29  '_depth'
              708  BINARY_SUBTRACT  
              709  STORE_FAST           33  '_new_z'

 L. 416       712  LOAD_FAST            31  '_r_to_center'
              715  LOAD_FAST            14  '_radius'
              718  COMPARE_OP            1  <=
              721  POP_JUMP_IF_FALSE   752  'to 752'

 L. 417       724  LOAD_FAST            33  '_new_z'
              727  LOAD_FAST             0  'self'
              730  LOAD_ATTR            29  '_depth'
              733  LOAD_FAST            31  '_r_to_center'
              736  LOAD_FAST            14  '_radius'
              739  BINARY_DIVIDE    
              740  LOAD_FAST            19  'crater_bowl_exp'
              743  BINARY_POWER     
              744  BINARY_MULTIPLY  
              745  INPLACE_ADD      
              746  STORE_FAST           33  '_new_z'
              749  JUMP_FORWARD         25  'to 777'

 L. 419       752  LOAD_FAST            33  '_new_z'
              755  LOAD_FAST             0  'self'
              758  LOAD_ATTR            29  '_depth'
              761  LOAD_FAST            31  '_r_to_center'
              764  LOAD_FAST            14  '_radius'
              767  BINARY_SUBTRACT  
              768  LOAD_FAST            15  'tan_repose'
              771  BINARY_MULTIPLY  
              772  BINARY_ADD       
              773  INPLACE_ADD      
              774  STORE_FAST           33  '_new_z'
            777_0  COME_FROM           749  '749'

 L. 424       777  LOAD_FAST            33  '_new_z'
              780  LOAD_FAST            30  'pre_elev'
              783  COMPARE_OP            0  <
              786  POP_JUMP_IF_FALSE   974  'to 974'

 L. 425       789  LOAD_FAST             0  'self'
              792  LOAD_ATTR            30  '_crater_type'
              795  POP_JUMP_IF_FALSE   847  'to 847'

 L. 426       798  LOAD_FAST            31  '_r_to_center'
              801  LOAD_FAST             0  'self'
              804  LOAD_ATTR            31  '_complex_peak_radius'
              807  COMPARE_OP            1  <=
              810  POP_JUMP_IF_FALSE   847  'to 847'

 L. 427       813  LOAD_FAST            33  '_new_z'
              816  LOAD_FAST             0  'self'
              819  LOAD_ATTR            32  '_complex_peak_str_uplift'
              822  LOAD_CONST               1.0
              825  LOAD_FAST            31  '_r_to_center'
              828  LOAD_FAST             0  'self'
              831  LOAD_ATTR            31  '_complex_peak_radius'
              834  BINARY_DIVIDE    
              835  BINARY_SUBTRACT  
              836  BINARY_MULTIPLY  
              837  BINARY_ADD       
              838  STORE_FAST           33  '_new_z'
              841  JUMP_ABSOLUTE       847  'to 847'
              844  JUMP_FORWARD          0  'to 847'
            847_0  COME_FROM           844  '844'

 L. 428       847  LOAD_FAST            33  '_new_z'
              850  STORE_FAST           34  'elev'

 L. 429       853  LOAD_FAST            30  'pre_elev'
              856  LOAD_FAST            33  '_new_z'
              859  BINARY_SUBTRACT  
              860  STORE_FAST           35  'depth_excavated'

 L. 430       863  LOAD_FAST            16  'crater_vol_below_ground'
              866  LOAD_FAST            35  'depth_excavated'
              869  INPLACE_ADD      
              870  STORE_FAST           16  'crater_vol_below_ground'

 L. 431       873  LOAD_FAST             0  'self'
              876  DUP_TOP          
              877  LOAD_ATTR            13  'mass_balance_in_impact'
              880  LOAD_FAST            35  'depth_excavated'
              883  INPLACE_SUBTRACT 
              884  ROT_TWO          
              885  STORE_ATTR           13  'mass_balance_in_impact'

 L. 432       888  LOAD_FAST             1  'grid'
              891  LOAD_ATTR            33  'get_neighbor_list'
              894  LOAD_FAST            29  'active_node'
              897  CALL_FUNCTION_1       1  None
              900  STORE_FAST           36  'neighbors_active_node'

 L. 433       903  SETUP_LOOP          413  'to 1319'
              906  LOAD_FAST            36  'neighbors_active_node'
              909  GET_ITER         
              910  FOR_ITER             57  'to 970'
              913  STORE_FAST           37  'x'

 L. 434       916  LOAD_FAST            18  'flag_already_in_the_list'
              919  LOAD_FAST            37  'x'
              922  BINARY_SUBSCR    
              923  POP_JUMP_IF_TRUE    910  'to 910'

 L. 435       926  LOAD_FAST            37  'x'
              929  LOAD_CONST               -1
              932  COMPARE_OP            3  !=
              935  POP_JUMP_IF_FALSE   967  'to 967'

 L. 436       938  LOAD_FAST            17  'crater_node_list'
              941  LOAD_ATTR            34  'append'
              944  LOAD_FAST            37  'x'
              947  CALL_FUNCTION_1       1  None
              950  POP_TOP          

 L. 437       951  LOAD_CONST               1
              954  LOAD_FAST            18  'flag_already_in_the_list'
              957  LOAD_FAST            37  'x'
              960  STORE_SUBSCR     
              961  JUMP_ABSOLUTE       967  'to 967'
              964  JUMP_BACK           910  'to 910'
              967  JUMP_BACK           910  'to 910'
              970  POP_BLOCK        
            971_0  COME_FROM           903  '903'
              971  JUMP_FORWARD        345  'to 1319'

 L. 440       974  LOAD_FAST            27  'unique_expression_for_local_thickness'
              977  LOAD_FAST            31  '_r_to_center'
              980  CALL_FUNCTION_1       1  None
              983  STORE_FAST           38  '_flat_thickness_above_surface'

 L. 441       986  LOAD_FAST            24  '_ejecta_azimuth'
              989  LOAD_FAST            32  '_theta'
              992  BINARY_SUBTRACT  
              993  STORE_FAST           39  '_theta_eff'

 L. 442       996  LOAD_FAST            11  'sin'
              999  LOAD_FAST            39  '_theta_eff'
             1002  CALL_FUNCTION_1       1  None
             1005  LOAD_CONST               2.0
             1008  BINARY_POWER     
             1009  STORE_FAST           40  '_sin_theta_sqd'

 L. 443      1012  LOAD_FAST            10  'cos'
             1015  LOAD_FAST            39  '_theta_eff'
             1018  CALL_FUNCTION_1       1  None
             1021  STORE_FAST           41  '_cos_theta'

 L. 449      1024  LOAD_FAST            25  'tan_beta'
             1027  LOAD_FAST            41  '_cos_theta'
             1030  BINARY_MULTIPLY  
             1031  LOAD_FAST            12  'sqrt'
             1034  LOAD_CONST               1.0
             1037  LOAD_FAST            40  '_sin_theta_sqd'
             1040  LOAD_FAST            26  'tan_beta_sqd'
             1043  BINARY_MULTIPLY  
             1044  BINARY_SUBTRACT  
             1045  CALL_FUNCTION_1       1  None
             1048  BINARY_ADD       
             1049  STORE_FAST           42  '_vec_mu_theta_by_mu0'

 L. 450      1052  LOAD_FAST            26  'tan_beta_sqd'
             1055  LOAD_FAST            41  '_cos_theta'
             1058  LOAD_CONST               2.0
             1061  BINARY_POWER     
             1062  LOAD_FAST            40  '_sin_theta_sqd'
             1065  BINARY_SUBTRACT  
             1066  BINARY_MULTIPLY  
             1067  LOAD_CONST               2.0
             1070  LOAD_FAST            25  'tan_beta'
             1073  BINARY_MULTIPLY  
             1074  LOAD_FAST            41  '_cos_theta'
             1077  BINARY_MULTIPLY  
             1078  LOAD_FAST            12  'sqrt'
             1081  LOAD_CONST               1.0
             1084  LOAD_FAST            26  'tan_beta_sqd'
             1087  LOAD_FAST            40  '_sin_theta_sqd'
             1090  BINARY_MULTIPLY  
             1091  BINARY_SUBTRACT  
             1092  CALL_FUNCTION_1       1  None
             1095  BINARY_MULTIPLY  
             1096  BINARY_ADD       
             1097  LOAD_CONST               1.0
             1100  BINARY_ADD       
             1101  LOAD_FAST             8  'twopi'
             1104  BINARY_DIVIDE    
             1105  STORE_FAST           43  '_vec_f_theta'

 L. 453      1108  LOAD_FAST            43  '_vec_f_theta'
             1111  LOAD_FAST            42  '_vec_mu_theta_by_mu0'
             1114  BINARY_DIVIDE    
             1115  LOAD_FAST             8  'twopi'
             1118  BINARY_MULTIPLY  
             1119  LOAD_FAST            38  '_flat_thickness_above_surface'
             1122  BINARY_MULTIPLY  
             1123  STORE_FAST           44  '_thickness'

 L. 455      1126  LOAD_FAST            44  '_thickness'
             1129  LOAD_CONST               0.0
             1132  COMPARE_OP            0  <
             1135  POP_JUMP_IF_FALSE  1147  'to 1147'

 L. 456      1138  LOAD_CONST               0.0
             1141  STORE_FAST           44  '_thickness'
             1144  JUMP_FORWARD          0  'to 1147'
           1147_0  COME_FROM          1144  '1144'

 L. 458      1147  LOAD_FAST            30  'pre_elev'
             1150  LOAD_FAST            44  '_thickness'
             1153  BINARY_ADD       
             1154  STORE_FAST           45  'potential_ejecta_thickness'

 L. 459      1157  LOAD_FAST            33  '_new_z'
             1160  LOAD_FAST            45  'potential_ejecta_thickness'
             1163  COMPARE_OP            1  <=
             1166  POP_JUMP_IF_FALSE  1197  'to 1197'

 L. 460      1169  LOAD_FAST            33  '_new_z'
             1172  STORE_FAST           34  'elev'

 L. 461      1175  LOAD_FAST             0  'self'
             1178  DUP_TOP          
             1179  LOAD_ATTR            13  'mass_balance_in_impact'
             1182  LOAD_FAST            34  'elev'
             1185  LOAD_FAST            30  'pre_elev'
             1188  BINARY_SUBTRACT  
             1189  INPLACE_ADD      
             1190  ROT_TWO          
             1191  STORE_ATTR           13  'mass_balance_in_impact'
             1194  JUMP_FORWARD         21  'to 1218'

 L. 463      1197  LOAD_FAST            45  'potential_ejecta_thickness'
             1200  STORE_FAST           34  'elev'

 L. 464      1203  LOAD_FAST             0  'self'
             1206  DUP_TOP          
             1207  LOAD_ATTR            13  'mass_balance_in_impact'
             1210  LOAD_FAST            44  '_thickness'
             1213  INPLACE_ADD      
             1214  ROT_TWO          
             1215  STORE_ATTR           13  'mass_balance_in_impact'
           1218_0  COME_FROM          1194  '1194'

 L. 466      1218  LOAD_FAST            44  '_thickness'
             1221  LOAD_FAST             0  'self'
             1224  LOAD_ATTR            35  '_minimum_ejecta_thickness'
             1227  COMPARE_OP            4  >
             1230  POP_JUMP_IF_FALSE  1319  'to 1319'

 L. 467      1233  LOAD_FAST             1  'grid'
             1236  LOAD_ATTR            33  'get_neighbor_list'
             1239  LOAD_FAST            29  'active_node'
             1242  CALL_FUNCTION_1       1  None
             1245  STORE_FAST           36  'neighbors_active_node'

 L. 468      1248  SETUP_LOOP           68  'to 1319'
             1251  LOAD_FAST            36  'neighbors_active_node'
             1254  GET_ITER         
             1255  FOR_ITER             57  'to 1315'
             1258  STORE_FAST           37  'x'

 L. 469      1261  LOAD_FAST            18  'flag_already_in_the_list'
             1264  LOAD_FAST            37  'x'
             1267  BINARY_SUBSCR    
             1268  POP_JUMP_IF_TRUE   1255  'to 1255'

 L. 470      1271  LOAD_FAST            37  'x'
             1274  LOAD_CONST               -1
             1277  COMPARE_OP            3  !=
             1280  POP_JUMP_IF_FALSE  1312  'to 1312'

 L. 471      1283  LOAD_FAST            17  'crater_node_list'
             1286  LOAD_ATTR            34  'append'
             1289  LOAD_FAST            37  'x'
             1292  CALL_FUNCTION_1       1  None
             1295  POP_TOP          

 L. 472      1296  LOAD_CONST               1
             1299  LOAD_FAST            18  'flag_already_in_the_list'
             1302  LOAD_FAST            37  'x'
             1305  STORE_SUBSCR     
             1306  JUMP_ABSOLUTE      1312  'to 1312'
             1309  JUMP_BACK          1255  'to 1255'
             1312  JUMP_BACK          1255  'to 1255'
             1315  POP_BLOCK        
           1316_0  COME_FROM          1248  '1248'
             1316  JUMP_FORWARD          0  'to 1319'
           1319_0  COME_FROM          1248  '1248'
           1319_1  COME_FROM           903  '903'

 L. 475      1319  LOAD_FAST            34  'elev'
             1322  LOAD_FAST             2  'data'
             1325  LOAD_ATTR            24  'elev'
             1328  LOAD_FAST            29  'active_node'
             1331  STORE_SUBSCR     
             1332  JUMP_BACK           607  'to 607'
           1335_0  COME_FROM           604  '604'

 L. 477      1335  LOAD_FAST             0  'self'
             1338  LOAD_ATTR            13  'mass_balance_in_impact'
             1341  LOAD_FAST            16  'crater_vol_below_ground'
             1344  BINARY_DIVIDE    
             1345  LOAD_FAST             0  'self'
             1348  STORE_ATTR           13  'mass_balance_in_impact'

 L. 478      1351  LOAD_FAST            24  '_ejecta_azimuth'
             1354  LOAD_FAST             0  'self'
             1357  STORE_ATTR           36  'ejecta_azimuth'

 L. 479      1360  LOAD_FAST            23  'beta_eff'
             1363  LOAD_FAST             0  'self'
             1366  STORE_ATTR           37  'impactor_angle_to_surface_normal'

 L. 483      1369  LOAD_FAST             2  'data'
             1372  LOAD_ATTR            24  'elev'
             1375  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 607_0

    def set_elev_change_only_beneath_footprint(self, grid, data):
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
        elev = data.elev
        tan_repose = self.tan_repose
        crater_bowl_exp = self.get_crater_shape_exp()
        while 1:
            rake_in_surface_plane = _surface_dip_direction - _azimuth_of_travel
            print '_surface_dip_direction: ', _surface_dip_direction
            print '_azimuth_of_travel: ', _azimuth_of_travel
            print '_angle_to_vertical: ', _angle_to_vertical
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
        print 'thickness_at_rim: ', thickness_at_rim
        print 'max_radius_ejecta: ', max_radius_ejecta_on_flat
        footprint_center_x = self._xcoord + sin(_azimuth_of_travel) * max_radius_ejecta_on_flat * tan_beta
        footprint_center_y = self._ycoord + cos(_azimuth_of_travel) * max_radius_ejecta_on_flat * tan_beta
        distances_to_footprint_center = grid.get_distances_of_nodes_to_point((footprint_center_x, footprint_center_y))
        distances_to_crater_center, azimuths_to_crater_center = grid.get_distances_of_nodes_to_point((self._xcoord, self._ycoord), get_az=1)
        footprint_nodes = numpy.logical_or(distances_to_footprint_center <= max_radius_ejecta_on_flat, distances_to_crater_center <= max_radius_ejecta_on_flat)
        elevs_under_footprint = elev[footprint_nodes]
        old_elevs_under_footprint = numpy.copy(elevs_under_footprint)
        _vec_r_to_center = distances_to_crater_center[footprint_nodes]
        _vec_theta = azimuths_to_crater_center[footprint_nodes]
        _vec_new_z = numpy.empty_like(_vec_r_to_center)
        _nodes_within_crater = _vec_r_to_center <= _radius
        _nodes_outside_crater = numpy.logical_not(_nodes_within_crater)
        _vec_new_z[:] = self.closest_node_elev + thickness_at_rim - self._depth
        _vec_new_z[_nodes_within_crater] += self._depth * (_vec_r_to_center[_nodes_within_crater] / _radius) ** crater_bowl_exp
        _vec_new_z[_nodes_outside_crater] += self._depth + (_vec_r_to_center[_nodes_outside_crater] - _radius) * tan_repose
        _nodes_below_surface = _vec_new_z < elev[footprint_nodes]
        _nodes_above_surface = numpy.logical_not(_nodes_below_surface)
        if self._crater_type:
            central_peak_pts = _vec_r_to_center <= self._complex_peak_radius
            _vec_new_z[central_peak_pts] = _vec_new_z[central_peak_pts] + self._complex_peak_str_uplift * (1.0 - _vec_r_to_center[central_peak_pts] / self._complex_peak_radius)
        elevs_under_footprint[_nodes_below_surface] = _vec_new_z[_nodes_below_surface]
        _vec_flat_thickness_above_surface = unique_expression_for_local_thickness(_vec_r_to_center[_nodes_above_surface])
        _vec_theta_eff = _ejecta_azimuth - _vec_theta[_nodes_above_surface]
        _vec_sin_theta_sqd = sin(_vec_theta_eff) ** 2.0
        _vec_cos_theta = cos(_vec_theta_eff)
        _vec_mu_theta_by_mu0 = tan_beta * _vec_cos_theta + sqrt(1.0 - _vec_sin_theta_sqd * tan_beta_sqd)
        _vec_f_theta = (tan_beta_sqd * (_vec_cos_theta ** 2.0 - _vec_sin_theta_sqd) + 2.0 * tan_beta * _vec_cos_theta * sqrt(1.0 - tan_beta_sqd * _vec_sin_theta_sqd) + 1.0) / twopi
        _vec_thickness = _vec_f_theta / _vec_mu_theta_by_mu0 * twopi * _vec_flat_thickness_above_surface
        _vec_thickness = where(_vec_thickness >= 0.0, _vec_thickness, 0.0)
        elevs_under_footprint[_nodes_above_surface] = where(_vec_new_z[_nodes_above_surface] <= elevs_under_footprint[_nodes_above_surface] + _vec_thickness, _vec_new_z[_nodes_above_surface], elevs_under_footprint[_nodes_above_surface] + _vec_thickness)
        data.elev[footprint_nodes] = elevs_under_footprint
        elev_diff = elevs_under_footprint - old_elevs_under_footprint
        self.mass_balance_in_impact = numpy.sum(elev_diff) / -numpy.sum(elev_diff[(elev_diff < 0.0)])
        self.ejecta_azimuth = _ejecta_azimuth
        self.impactor_angle_to_surface_normal = beta_eff
        print 'Vol of crater cavity: ', self._cavity_volume
        return data.elev

    def excavate_a_crater(self, grid, data, **kwds):
        """
            This method executes the most of the other methods of this crater class, and makes the geomorphic changes to a mesh associated with a single bolide impact with randomized properties. It receives parameters of the model grid, and the vector data storage class. It is the primary interface method of this class.
            This method is optimized to only calculate the elevation changes for an impact within its ejecta footprint.
            A fixed crater size can be specified with the input variable "forced_radius" (in km), and a fixed impact angle with "forced_angle" (in degrees from vertical - impact azimuth will always be assumed as travel eastwards). Position can be specified with forced_pos, which takes an array-like object with two entries, which are the x and y coordinate in relative position on the grid (e.g., [0.5, 0.5]).
        """
        try:
            self._radius = kwds['forced_radius']
        except:
            print 'Randomly generating impact radius...'
            self.set_cr_radius_from_shoemaker(data)

        print 'Radius: ', self._radius
        self.set_depth_from_size()
        self.set_crater_volume()
        try:
            self._xcoord = kwds['forced_pos'][0] * grid.get_grid_xdimension()
        except:
            print 'Randomly generating impact site...'
            self.set_coords(grid, data)
        else:
            try:
                self._ycoord = kwds['forced_pos'][1] * grid.get_grid_ydimension()
                print self._xcoord, self._ycoord
                self.closest_node_index = grid.snap_coords_to_grid(self._xcoord, self._ycoord)
                self.closest_node_elev = data.elev[self.closest_node_index]
            except:
                print 'Could not set specified position. Was a 2 item iterable provided?'

            try:
                self._angle_to_vertical = kwds['forced_angle'] * numpy.pi / 180.0
            except:
                print 'Randomly generating impactor angle...'
                self.set_impactor_angles()
            else:
                self._azimuth_of_travel = 0.5 * numpy.pi

            try:
                self._minimum_crater = kwds['minimum_radius']
            except:
                pass

        self.set_crater_mean_slope_v2(grid, data)
        if numpy.isnan(self._surface_slope):
            print 'Surface slope is not defined for this crater! Is it too big? Crater will not be drawn.'
        else:
            self.set_elev_change_only_beneath_footprint(grid, data)
        print 'Impactor angle to ground normal: ', self.impactor_angle_to_surface_normal
        print 'Mass balance in impact: ', self.mass_balance_in_impact
        print '*****'
        data.impact_sequence.append({'x': self._xcoord, 'y': self._ycoord, 'r': self._radius, 'volume': self._cavity_volume, 'surface_slope': self._surface_slope, 'normal_angle': self.impactor_angle_to_surface_normal, 'impact_az': self._azimuth_of_travel, 'ejecta_az': self.ejecta_azimuth, 'mass_balance': self.mass_balance_in_impact})


def dig_some_craters(use_existing_grid=0, grid_dimension_in=1000, dx_in=0.0025, n_craters=1, surface_slope=0.0, **kwds):
    """
    Ad hoc driver code to make this file run as a standalone.
    If a surface_slope is specified, it should be in degrees, and the resulting surface will dip west.
    If use_existing_grid is set, it should (for now) be a tuple containing (grid, data).
    If force_crater_properties is specified, it should be keywords for excavate_a_crater(), comprising as many as desired of: forced_radius=value, forced_angle=value, forced_pos=(rel_x,rel_y).
    """
    nr = grid_dimension_in
    nc = grid_dimension_in
    dx = dx_in
    nt = n_craters
    if not use_existing_grid:
        mg = RasterModelGrid(nr, nc, dx)
        vectors = data(mg)
        if not surface_slope:
            vectors.elev[:] = 1.0
        else:
            vertical_rise_in_one_node_step = dx * numpy.tan(surface_slope * numpy.pi / 180.0)
            for i in range(nr):
                vectors.elev = numpy.tile(numpy.array(range(nr)) * vertical_rise_in_one_node_step, nr)

        vectors.elev += numpy.random.uniform(0.0, 1e-05, vectors.elev.shape)
    else:
        try:
            mg = use_existing_grid[0]
            vectors = use_existing_grid[1]
        except:
            print 'Could not set variables for existing grid!'

        if 'cr' not in locals():
            cr = impactor()
        for i in xrange(0, nt):
            print 'Crater number ', i
            cr.excavate_a_crater(mg, vectors, **kwds)

    elev_raster = mg.node_vector_to_raster(vectors.elev, flip_vertically=True)
    vectors.viewing_raster = copy(elev_raster)
    return (cr, mg, vectors)


def dig_one_crater_then_degrade(loops=1, step=500):
    crater_time_sequ = {}
    cr, mg, vectors = dig_some_craters(grid_dimension_in=1000, dx_in=0.002, n_craters=1, forced_radius=0.5, forced_angle=0.0, forced_pos=(0.5,
                                                                                                                                          0.5))
    crater_time_sequ[0] = copy(vectors.impact_sequence)
    numpy.savetxt('saved_elevs0', vectors.viewing_raster)
    for i in xrange(0, loops):
        cr, mg, vectors = dig_some_craters(use_existing_grid=(mg, vectors), n_craters=step)
        crater_time_sequ[i + 1] = copy(vectors.impact_sequence)
        numpy.savetxt('saved_elevs' + str(i + 1), vectors.viewing_raster)

    return crater_time_sequ


def ten_times_reduction(mg_in, vectors_in, loops=25):
    """
    Depreciated in favour of step_reduce_size.
    """
    crater_time_sequ_50_m_min = {}
    crater_time_sequ_5_m_min = {}
    profile_list = []
    xsec_list = []
    for i in xrange(0, loops):
        mg_in, vectors_in, profile, xsec = dig_some_craters(mg_in, vectors_in, nt_in=10000, min_radius=0.05)
        crater_time_sequ_50_m_min[i] = copy(vectors_in)

    for i in xrange(0, loops):
        mg_in, vectors_in, profile, xsec = dig_some_craters(mg_in, vectors_in, nt_in=10000, min_radius=0.005)
        crater_time_sequ_5_m_min[i] = copy(vectors_in)

    return (
     crater_time_sequ_50_m_min, crater_time_sequ_5_m_min)


def step_reduce_size(mg_in, vectors_in, loops=[
 25, 25], interval=10000, min_radius_in=[0.05, 0.005]):
    crater_time_sequ_1st = {}
    crater_time_sequ_2nd = {}
    profile_list = []
    xsec_list = []
    for i in xrange(0, loops[0]):
        mg_in, vectors_in, profile, xsec = dig_some_craters(mg_in, vectors_in, nt_in=interval, min_radius=min_radius_in[0])
        crater_time_sequ_1st[i] = copy(vectors_in)

    for i in xrange(0, loops[1]):
        mg_in, vectors_in, profile, xsec = dig_some_craters(mg_in, vectors_in, nt_in=interval, min_radius=min_radius_in[1])
        crater_time_sequ_2nd[i] = copy(vectors_in)

    return (
     crater_time_sequ_1st, crater_time_sequ_2nd)


def plot_hypsometry(plotting_rasters):
    """
    This function plots hypsometry (elev above minimum vs no. of px below it) for each of plotting rasters provided to the function. If plotting_rasters is a dictionary of data, where the plotting rasters are stored as data.plotting_raster, the function will return all entries. If it is a single plotting raster, or a single 'data' object, only that raster will plot. Call 'show()' manually after running this code.
    """

    def plot_a_hypsometry_curve(elevs, color=0):
        min_elev = numpy.amin(elevs)
        rel_relief = (elevs.flatten() - min_elev) / (numpy.amax(elevs) - min_elev)
        rel_relief.sort()
        hyps_x_axis = 1.0 - numpy.array(range(rel_relief.size), dtype=float) / rel_relief.size
        input_color = color * 0.9
        plot(hyps_x_axis, rel_relief, color=str(input_color))

    if type(plotting_rasters) == dict:
        for i in range(len(plotting_rasters)):
            fraction = float(i) / len(plotting_rasters)
            plot_a_hypsometry_curve(plotting_rasters[i].viewing_raster, color=fraction)

    elif type(plotting_rasters) == numpy.ndarray:
        plot_a_hypsometry_curve(plotting_rasters)
    else:
        try:
            plot_a_hypsometry_curve(plotting_rasters.viewing_raster)
        except:
            print 'Input type not recognised!'


def mass_balance_tests():
    """
    This script applies tests to try to pin down the cause of the weird mass balance issues existing in this module.
    """
    pass


if __name__ == '__main__':
    dig_one_crater_then_degrade(loops=4, step=20)