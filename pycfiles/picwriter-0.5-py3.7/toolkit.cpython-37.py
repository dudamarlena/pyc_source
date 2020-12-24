# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\toolkit.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 27498 bytes
"""
Set of helper functions that make it easier to manipulate
and work with subclasses defined in **components** module
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, math, gdspy
TOL = 1e-06
CURRENT_CELLS = {}
CURRENT_CELL_NAMES = {}

def add(top_cell, component_cell, center=(0, 0), x_reflection=False):
    """ First creates a CellReference to subcell, then adds this to topcell at location center.

        Args:
           * **top_cell** (gdspy.Cell):  Cell being added to
           * **component_cell** (gdspy.Cell):  Cell of the component being added

        Keyword Args:
           * **port** (tuple): location for the subcell to be added
           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians).  Defaults to 'EAST' (zero degrees of rotation).

        Returns:
           None
    """
    if isinstance(component_cell, gdspy.Cell):
        top_cell.add(gdspy.CellReference(component_cell,
          origin=center, x_reflection=x_reflection))
    else:
        if isinstance(component_cell, Component):
            component_cell.addto(top_cell)
        else:
            try:
                top_cell.add(component_cell)
            except:
                raise ValueError('Improper inputs given to add()')


def getCellName(name):
    global CURRENT_CELL_NAMES
    if name not in CURRENT_CELL_NAMES.keys():
        CURRENT_CELL_NAMES[name] = 1
    else:
        CURRENT_CELL_NAMES[name] += 1
    return str(name) + '_' + str(CURRENT_CELL_NAMES[name])


def build_mask(cell, wgt, final_layer=None, final_datatype=None):
    """ Builds the appropriate mask according to the resist specifications and fabrication type.  Does this by applying a boolean 'XOR' or 'AND' operation on the waveguide and clad masks.

        Args:
           * **cell** (gdspy.Cell):  Cell with components.  Final mask is placed in this cell.
           * **wgt** (WaveguideTemplate):  Waveguide template containing the resist information, and layers/datatypes for the waveguides and cladding.

        Keyword Args:
           * **final_layer** (int): layer to place the mask on (defaults to `wgt.clad_layer + 1`)
           * **final_datatype** (int): datatype to place the mask on (defaults to `0`)

        Returns:
           None

    """
    fl = wgt.clad_layer + 1 if final_layer == None else final_layer
    fd = 0 if final_datatype == None else final_datatype
    polygons = cell.get_polygons(by_spec=True)
    try:
        pWG = polygons[(wgt.wg_layer, wgt.wg_datatype)]
        pCLAD = polygons[(wgt.clad_layer, wgt.clad_datatype)]
    except KeyError:
        print('Warning! No objects written to layer/datatype specified by WaveguideTemplate')

    if wgt.resist == '+':
        cell.add(gdspy.fast_boolean(pWG,
          pCLAD,
          'xor',
          precision=0.001,
          max_points=199,
          layer=fl,
          datatype=fd))
    else:
        if wgt.resist == '-':
            cell.add(gdspy.fast_boolean(pWG,
              pCLAD,
              'and',
              precision=0.001,
              max_points=199,
              layer=fl,
              datatype=fd))


def get_trace_length(trace, wgt):
    """ Returns the total length of a curved waveguide trace.

    Args:
       * **trace** (list): tracelist of (x,y) points all specifying 90 degree angles.
       * **wgt** (WaveguideTemplate): template for the waveguide, the bend_radius of which is used to compute the length of the curved section.

    Returns:
       float corresponding to the length of the waveguide trace

    """
    length = 0.0
    dbr = 2 * wgt.bend_radius - 0.5 * np.pi * wgt.bend_radius
    for i in range(len(trace) - 1):
        pt2, pt1 = trace[(i + 1)], trace[i]
        length += np.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)

    length = length - dbr * (len(trace) - 1)
    return length


def get_keys(cell):
    """ Returns a list of the keys available in a portlist, such as 'input', 'output', 'top_output', etc.  Only works for picwriter components.

        Args:
           * **cell** (gdspy.Cell):  Cell from which to get get the portlist

        Returns:
           List of portlist keys corresponding to 'cell'.

    """
    return list(cell.portlist.keys())


def get_angle(pt1, pt2):
    """
    Given two cardinal points, returns the corresponding angle
    in *radians*.  Must be an integer multiple of pi/2.

    Args:
       * **pt1** (tuple):  Point 1
       * **pt2** (tuple):  Point 2

    Returns:
       float  Angle (integer multiple of pi/2)

    Example::

        import picwriter.toolkit as tk
        print(tk.get_angle((0, 0), (0, 100)))

    The above prints 1.5707963267948966

    """
    dx, dy = pt2[0] - pt1[0], pt2[1] - pt1[1]
    if abs(dx) <= TOL and dy > 0:
        angle = 0.5 * np.pi
    else:
        if abs(dy) <= TOL and dx < 0:
            angle = np.pi
        else:
            if abs(dx) <= TOL and dy < 0:
                angle = 1.5 * np.pi
            else:
                if abs(dy) <= TOL and dx > 0:
                    angle = 0.0
                else:
                    raise ValueError('Warning! The angle between the two points must be an integer multiples of 90deg from each other')
    return angle


def get_exact_angle(pt1, pt2):
    """
    Given two cardinal points, returns the corresponding angle
    in *radians*.

    Args:
       * **pt1** (tuple):  Point 1
       * **pt2** (tuple):  Point 2

    Returns:
       float  Angle (in radians)

    Example::

        import picwriter.toolkit as tk
        print(tk.get_angle((0, 0), (100, 100)))

    The above prints 0.785398163

    """
    dx, dy = pt2[0] - pt1[0], pt2[1] - pt1[1]
    return math.atan2(dy, dx) % (2 * np.pi)


def dist(pt1, pt2):
    """
    Given two cardinal points, returns the distance between the two.

    Args:
       * **pt1** (tuple):  Point 1
       * **pt2** (tuple):  Point 2

    Returns:
       float  Distance

    Example::

        import picwriter.toolkit as tk
        print(tk.dist((0, 0), (100, 100)))

    The above prints 141.42135623730951

    """
    return np.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)


def get_direction(pt1, pt2):
    """  Returns a cardinal direction (``'NORTH'``, ``'WEST'``, ``'SOUTH'``, and ``'EAST'``)
        that corresponds to a cartesian point `pt1 (tuple), pointing
        TOWARDS a second point `pt2`

        Args:
           * **pt1** (tuple):  Point 1
           * **pt2** (tuple):  Point 2

        Returns:
           string  (``'NORTH'``, ``'WEST'``, ``'SOUTH'``, and ``'EAST'``)

        Example::

            import picwriter.toolkit as tk
            tk.get_direction((0,0), (-100,0))

        The above prints 'WEST'

    """
    dx, dy = pt2[0] - pt1[0], pt2[1] - pt1[1]
    if abs(dx) <= TOL:
        if dy > 0:
            return 'NORTH'
    if abs(dy) <= TOL:
        if dx < 0:
            return 'WEST'
    if abs(dx) <= TOL:
        if dy < 0:
            return 'SOUTH'
    return 'EAST'


def get_turn--- This code section failed: ---

 L. 268         0  LOAD_FAST                'dir1'
                2  LOAD_STR                 'NORTH'
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    16  'to 16'
                8  LOAD_FAST                'dir2'
               10  LOAD_STR                 'WEST'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_TRUE     64  'to 64'
             16_0  COME_FROM             6  '6'

 L. 269        16  LOAD_FAST                'dir1'
               18  LOAD_STR                 'WEST'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    32  'to 32'
               24  LOAD_FAST                'dir2'
               26  LOAD_STR                 'SOUTH'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_TRUE     64  'to 64'
             32_0  COME_FROM            22  '22'

 L. 270        32  LOAD_FAST                'dir1'
               34  LOAD_STR                 'SOUTH'
               36  COMPARE_OP               ==
               38  POP_JUMP_IF_FALSE    48  'to 48'
               40  LOAD_FAST                'dir2'
               42  LOAD_STR                 'EAST'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_TRUE     64  'to 64'
             48_0  COME_FROM            38  '38'

 L. 271        48  LOAD_FAST                'dir1'
               50  LOAD_STR                 'EAST'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    74  'to 74'
               56  LOAD_FAST                'dir2'
               58  LOAD_STR                 'NORTH'
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    74  'to 74'
             64_0  COME_FROM            46  '46'
             64_1  COME_FROM            30  '30'
             64_2  COME_FROM            14  '14'

 L. 273        64  LOAD_GLOBAL              np
               66  LOAD_ATTR                pi
               68  LOAD_CONST               2.0
               70  BINARY_TRUE_DIVIDE
               72  RETURN_VALUE     
             74_0  COME_FROM            62  '62'
             74_1  COME_FROM            54  '54'

 L. 275        74  LOAD_FAST                'dir1'
               76  LOAD_STR                 'NORTH'
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE    90  'to 90'
               82  LOAD_FAST                'dir2'
               84  LOAD_STR                 'EAST'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_TRUE    138  'to 138'
             90_0  COME_FROM            80  '80'

 L. 276        90  LOAD_FAST                'dir1'
               92  LOAD_STR                 'EAST'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   106  'to 106'
               98  LOAD_FAST                'dir2'
              100  LOAD_STR                 'SOUTH'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_TRUE    138  'to 138'
            106_0  COME_FROM            96  '96'

 L. 277       106  LOAD_FAST                'dir1'
              108  LOAD_STR                 'SOUTH'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   122  'to 122'
              114  LOAD_FAST                'dir2'
              116  LOAD_STR                 'WEST'
              118  COMPARE_OP               ==
              120  POP_JUMP_IF_TRUE    138  'to 138'
            122_0  COME_FROM           112  '112'

 L. 278       122  LOAD_FAST                'dir1'
              124  LOAD_STR                 'WEST'
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   150  'to 150'
              130  LOAD_FAST                'dir2'
              132  LOAD_STR                 'NORTH'
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   150  'to 150'
            138_0  COME_FROM           120  '120'
            138_1  COME_FROM           104  '104'
            138_2  COME_FROM            88  '88'

 L. 280       138  LOAD_GLOBAL              np
              140  LOAD_ATTR                pi
              142  UNARY_NEGATIVE   
              144  LOAD_CONST               2.0
              146  BINARY_TRUE_DIVIDE
              148  RETURN_VALUE     
            150_0  COME_FROM           136  '136'
            150_1  COME_FROM           128  '128'

Parse error at or near `COME_FROM' instruction at offset 74_1


def flip_direction(direction):
    """  Returns the opposite of `direction`, where each direction is either ``'NORTH'``, ``'WEST'``, ``'SOUTH'``, or ``'EAST'``

        Args:
           * **direction** (direction):  Direction to be flipped
           * **pt2** (tuple):  Point 2

        Returns:
           direction (``'NORTH'``, ``'WEST'``, ``'SOUTH'``, or ``'EAST'``)

    """
    if direction == 'NORTH':
        return 'SOUTH'
    if direction == 'SOUTH':
        return 'NORTH'
    if direction == 'WEST':
        return 'EAST'
    if direction == 'EAST':
        return 'WEST'
    if isinstance(direction, float):
        return (direction + np.pi) % (2 * np.pi)


def translate_point(pt, length, direction, height=0.0):
    """  Returns the point (tuple) corresponding to `pt` translated by distance `length` in direction `direction` where each direction is either ``'NORTH'``, ``'WEST'``, ``'SOUTH'``, or ``'EAST'``

        Args:
           * **pt** (tuple):  Starting point
           * **length** (float): Distance to move in *direction*
           * **direction** (direction):  Direction to move in
           
        Keyword Args:
           * **height** (float):  Distance to move perpendicular to *direction*.  Defaults to 0.

        Returns:
           point, tuple (x, y)

    """
    if isinstance(direction, float):
        return (
         pt[0] + length * np.cos(direction) - height * np.sin(direction),
         pt[1] + length * np.sin(direction) + height * np.cos(direction))
    if str(direction) == 'NORTH':
        return (
         pt[0] - height, pt[1] + length)
    if str(direction) == 'SOUTH':
        return (
         pt[0] + height, pt[1] - length)
    if str(direction) == 'WEST':
        return (
         pt[0] - length, pt[1] - height)
    if str(direction) == 'EAST':
        return (
         pt[0] + length, pt[1] + height)


def normalize_angle(angle):
    """  Returns the angle (in radians) between -pi and +pi that corresponds to the input angle

        Args:
           * **angle** (float):  Angle to normalize

        Returns:
           float  Angle

    """
    angle = angle % (2 * np.pi)
    if angle > np.pi:
        angle -= 2 * np.pi
    return angle


def get_curve_length(func, start, end, grid=0.001):
    """  Returns the length (in microns) of a curve defined by the function `func` on the interval [start, end]

        Args:
           * **func** (function):  Function that takes a single (floating point) argument, and returns a (x,y) tuple.
           * **start** (float):  Starting value (argument passed to `func`).
           * **end** (float):  Ending value (argument passed to `func`).
           
        Keyword Args:
           * **grid** (float):  Grid resolution used to determine when curve length has converged.  Defaults to 0.001.

        Returns:
           float  Length

    """

    def get_cur_length(pt_list):
        length = 0
        for i in range(len(pt_list) - 1):
            pt1, pt2 = pt_list[i], pt_list[(i + 1)]
            length += np.sqrt((pt2[1] - pt1[1]) ** 2 + (pt2[0] - pt1[0]) ** 2)

        return length

    num_pts = 2
    error = 2 * grid
    pts = [func(i) for i in np.linspace(start, end, num_pts)]
    prev_length = get_cur_length(pts)
    while error > grid:
        print('num_pts = ' + str(num_pts))
        print('prev_length = ' + str(prev_length))
        num_pts = num_pts * 2
        pts = [func(i) for i in np.linspace(start, end, num_pts)]
        cur_length = get_cur_length(pts)
        error = abs(cur_length - prev_length)
        prev_length = cur_length

    print('num_pts = ' + str(num_pts))
    print('Final length! = ' + str(prev_length))
    return cur_length


def build_waveguide_polygon(func, wg_width, start_direction, end_direction, start_val=0, end_val=1, grid=0.001):
    """
        Args:
           * **func** (function):  Function that takes a single (floating point) argument, and returns a (x,y) tuple.
           * **wg_width** (float):  Waveguide width
           * **num_pts** (int):  Number of points that make up the waveguide path
           * **start_direction** (float):  Starting direction of the path, in *radians*.
           * **end_direction** (float):  End direction of the path, in *radians*.
           
        Keyword Args:
           * **start_val** (float):  Starting value (argument passed to `func`).  Defaults to 0.
           * **end_val** (float):  Ending value (argument passed to `func`).  Defaults to 1.
           * **grid** (float): Grid resolution used to determine when curve length has converged.  Guarantees that polygon formed by the points results in no more than a grid/2.0 error from the true position.  Defaults to 0.001

        Returns:
           Two lists, one for each edge of the waveguide.
    
    """

    def get_path_points(func, wg_width, num_pts, start_direction, end_direction, start_val=0, end_val=1):
        poly_list1, poly_list2 = [], []
        center_pts = [func(i) for i in np.linspace(start_val, end_val, num_pts)]
        angle = (start_direction + np.pi / 2.0) % (2 * np.pi)
        poly_list1.append((
         center_pts[0][0] + wg_width / 2.0 * np.cos(angle),
         center_pts[0][1] + wg_width / 2.0 * np.sin(angle)))
        angle = (start_direction - np.pi / 2.0) % (2 * np.pi)
        poly_list2.append((
         center_pts[0][0] + wg_width / 2.0 * np.cos(angle),
         center_pts[0][1] + wg_width / 2.0 * np.sin(angle)))
        for i in range(len(center_pts) - 2):
            prev_pt, cur_pt, next_pt = center_pts[i], center_pts[(i + 1)], center_pts[(i + 2)]
            d1, d2 = np.arctan2(cur_pt[1] - prev_pt[1], cur_pt[0] - prev_pt[0]) % (2 * np.pi), np.arctan2(next_pt[1] - cur_pt[1], next_pt[0] - cur_pt[0]) % (2 * np.pi)
            angle = ((d1 + d2) / 2.0 + np.pi / 2.0) % (2 * np.pi)
            poly_list1.append((
             cur_pt[0] + wg_width / 2.0 * np.cos(angle),
             cur_pt[1] + wg_width / 2.0 * np.sin(angle)))
            angle = ((d1 + d2) / 2.0 - np.pi / 2.0) % (2 * np.pi)
            poly_list2.append((
             cur_pt[0] + wg_width / 2.0 * np.cos(angle),
             cur_pt[1] + wg_width / 2.0 * np.sin(angle)))

        angle = (end_direction + np.pi + np.pi / 2.0) % (2 * np.pi)
        poly_list1.append((
         center_pts[(-1)][0] + wg_width / 2.0 * np.cos(angle),
         center_pts[(-1)][1] + wg_width / 2.0 * np.sin(angle)))
        angle = (end_direction + np.pi - np.pi / 2.0) % (2 * np.pi)
        poly_list2.append((
         center_pts[(-1)][0] + wg_width / 2.0 * np.cos(angle),
         center_pts[(-1)][1] + wg_width / 2.0 * np.sin(angle)))
        return (
         poly_list1, poly_list2)

    def check_path(path, grid):
        """ Determines if a path has sufficiently low grid error (and if so, returns True, else False).
        Does this by iterating through the points, and computing the area of the triangle formed by any
        3 consecutive points on path.  If this area, divided by the length between the first & last point, is greater than 0.5*grid,
        then the the error is too large!
        """
        for i in range(len(path) - 2):
            pt1, pt2, pt3 = path[i], path[(i + 1)], path[(i + 2)]
            area = abs((pt1[0] * (pt2[1] - pt3[1]) + pt2[0] * (pt3[1] - pt1[1]) + pt3[0] * (pt1[1] - pt2[1])) / 2.0)
            length = np.sqrt((pt3[1] - pt1[1]) ** 2 + (pt3[0] - pt1[0]) ** 2)
            if area / length > 0.5 * grid:
                return False

        return True

    num_pts = 16
    isPathOK = False
    firstIter = True
    cur_path1, cur_path2 = [], []
    while isPathOK == False:
        if not firstIter:
            prev_path1, prev_path2 = cur_path1, cur_path2
        cur_path1, cur_path2 = get_path_points(func,
          wg_width,
          num_pts,
          start_direction,
          end_direction,
          start_val=start_val,
          end_val=end_val)
        if firstIter:
            prev_path1, prev_path2 = cur_path1, cur_path2
            firstIter = False
        isPathOK = check_path(cur_path1, grid) and check_path(cur_path2, grid)
        num_pts = num_pts * 2

    path_points = prev_path1 + prev_path2[::-1]
    return path_points


class Component:
    __doc__ = ' Super class for all objects created in PICwriter.  This class handles rotations, naming, etc. for all components,\n        so that writing python code for new cells requires less overhead.  Component is a wrapper around gdspy Cell objects.\n\n        Args:\n           * **name** (string):  The name prefix to be used for these \n\n        Keyword Args:\n           * **angle** (float): Angle in radians (between 0 and pi/2) at which the waveguide bends towards the coupling region.  Default=pi/6.\n\n    '

    def __init__(self, name, *args):
        self.name_prefix = name
        self.portlist = {}
        self.port = (0, 0)
        self.direction = 0.0
        self._hash_cell_(args[0])

    def _auto_transform_--- This code section failed: ---

 L. 571       0_2  SETUP_LOOP         1008  'to 1008'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                portlist
                8  LOAD_METHOD              keys
               10  CALL_METHOD_0         0  '0 positional arguments'
               12  GET_ITER         
            14_16  FOR_ITER           1006  'to 1006'
               18  STORE_FAST               'key'

 L. 572        20  LOAD_FAST                'self'
               22  LOAD_ATTR                portlist
               24  LOAD_FAST                'key'
               26  BINARY_SUBSCR    
               28  LOAD_STR                 'port'
               30  BINARY_SUBSCR    
               32  STORE_FAST               'cur_port'

 L. 575        34  LOAD_FAST                'self'
               36  LOAD_ATTR                direction
               38  LOAD_STR                 'EAST'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 577        44  LOAD_CONST               0.0
               46  STORE_FAST               'angle'
            48_50  JUMP_FORWARD        894  'to 894'
             52_0  COME_FROM            42  '42'

 L. 579        52  LOAD_FAST                'self'
               54  LOAD_ATTR                direction
               56  LOAD_STR                 'NORTH'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE   210  'to 210'

 L. 580        62  LOAD_GLOBAL              np
               64  LOAD_ATTR                pi
               66  LOAD_CONST               2.0
               68  BINARY_TRUE_DIVIDE
               70  STORE_FAST               'angle'

 L. 582        72  LOAD_FAST                'self'
               74  LOAD_ATTR                portlist
               76  LOAD_FAST                'key'
               78  BINARY_SUBSCR    
               80  LOAD_STR                 'direction'
               82  BINARY_SUBSCR    
               84  LOAD_STR                 'NORTH'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L. 583        90  LOAD_STR                 'WEST'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                portlist
               96  LOAD_FAST                'key'
               98  BINARY_SUBSCR    
              100  LOAD_STR                 'direction'
              102  STORE_SUBSCR     
              104  JUMP_FORWARD        894  'to 894'
            106_0  COME_FROM            88  '88'

 L. 584       106  LOAD_FAST                'self'
              108  LOAD_ATTR                portlist
              110  LOAD_FAST                'key'
              112  BINARY_SUBSCR    
              114  LOAD_STR                 'direction'
              116  BINARY_SUBSCR    
              118  LOAD_STR                 'WEST'
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   140  'to 140'

 L. 585       124  LOAD_STR                 'SOUTH'
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                portlist
              130  LOAD_FAST                'key'
              132  BINARY_SUBSCR    
              134  LOAD_STR                 'direction'
              136  STORE_SUBSCR     
              138  JUMP_FORWARD        894  'to 894'
            140_0  COME_FROM           122  '122'

 L. 586       140  LOAD_FAST                'self'
              142  LOAD_ATTR                portlist
              144  LOAD_FAST                'key'
              146  BINARY_SUBSCR    
              148  LOAD_STR                 'direction'
              150  BINARY_SUBSCR    
              152  LOAD_STR                 'SOUTH'
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   174  'to 174'

 L. 587       158  LOAD_STR                 'EAST'
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                portlist
              164  LOAD_FAST                'key'
              166  BINARY_SUBSCR    
              168  LOAD_STR                 'direction'
              170  STORE_SUBSCR     
              172  JUMP_FORWARD        894  'to 894'
            174_0  COME_FROM           156  '156'

 L. 588       174  LOAD_FAST                'self'
              176  LOAD_ATTR                portlist
              178  LOAD_FAST                'key'
              180  BINARY_SUBSCR    
              182  LOAD_STR                 'direction'
              184  BINARY_SUBSCR    
              186  LOAD_STR                 'EAST'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   206  'to 206'

 L. 589       192  LOAD_STR                 'NORTH'
              194  LOAD_FAST                'self'
              196  LOAD_ATTR                portlist
              198  LOAD_FAST                'key'
              200  BINARY_SUBSCR    
              202  LOAD_STR                 'direction'
              204  STORE_SUBSCR     
            206_0  COME_FROM           190  '190'
          206_208  JUMP_FORWARD        894  'to 894'
            210_0  COME_FROM            60  '60'

 L. 590       210  LOAD_FAST                'self'
              212  LOAD_ATTR                direction
              214  LOAD_STR                 'WEST'
              216  COMPARE_OP               ==
          218_220  POP_JUMP_IF_FALSE   374  'to 374'

 L. 591       222  LOAD_GLOBAL              np
              224  LOAD_ATTR                pi
              226  STORE_FAST               'angle'

 L. 593       228  LOAD_FAST                'self'
              230  LOAD_ATTR                portlist
              232  LOAD_FAST                'key'
              234  BINARY_SUBSCR    
              236  LOAD_STR                 'direction'
              238  BINARY_SUBSCR    
              240  LOAD_STR                 'NORTH'
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_FALSE   264  'to 264'

 L. 594       248  LOAD_STR                 'SOUTH'
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                portlist
              254  LOAD_FAST                'key'
              256  BINARY_SUBSCR    
              258  LOAD_STR                 'direction'
              260  STORE_SUBSCR     
              262  JUMP_FORWARD        894  'to 894'
            264_0  COME_FROM           244  '244'

 L. 595       264  LOAD_FAST                'self'
              266  LOAD_ATTR                portlist
              268  LOAD_FAST                'key'
              270  BINARY_SUBSCR    
              272  LOAD_STR                 'direction'
              274  BINARY_SUBSCR    
              276  LOAD_STR                 'WEST'
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   300  'to 300'

 L. 596       284  LOAD_STR                 'EAST'
              286  LOAD_FAST                'self'
              288  LOAD_ATTR                portlist
              290  LOAD_FAST                'key'
              292  BINARY_SUBSCR    
              294  LOAD_STR                 'direction'
              296  STORE_SUBSCR     
              298  JUMP_FORWARD        894  'to 894'
            300_0  COME_FROM           280  '280'

 L. 597       300  LOAD_FAST                'self'
              302  LOAD_ATTR                portlist
              304  LOAD_FAST                'key'
              306  BINARY_SUBSCR    
              308  LOAD_STR                 'direction'
              310  BINARY_SUBSCR    
              312  LOAD_STR                 'SOUTH'
              314  COMPARE_OP               ==
          316_318  POP_JUMP_IF_FALSE   336  'to 336'

 L. 598       320  LOAD_STR                 'NORTH'
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                portlist
              326  LOAD_FAST                'key'
              328  BINARY_SUBSCR    
              330  LOAD_STR                 'direction'
              332  STORE_SUBSCR     
              334  JUMP_FORWARD        894  'to 894'
            336_0  COME_FROM           316  '316'

 L. 599       336  LOAD_FAST                'self'
              338  LOAD_ATTR                portlist
              340  LOAD_FAST                'key'
              342  BINARY_SUBSCR    
              344  LOAD_STR                 'direction'
              346  BINARY_SUBSCR    
              348  LOAD_STR                 'EAST'
              350  COMPARE_OP               ==
          352_354  POP_JUMP_IF_FALSE   894  'to 894'

 L. 600       356  LOAD_STR                 'WEST'
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                portlist
              362  LOAD_FAST                'key'
              364  BINARY_SUBSCR    
              366  LOAD_STR                 'direction'
              368  STORE_SUBSCR     
          370_372  JUMP_FORWARD        894  'to 894'
            374_0  COME_FROM           218  '218'

 L. 601       374  LOAD_FAST                'self'
              376  LOAD_ATTR                direction
              378  LOAD_STR                 'SOUTH'
              380  COMPARE_OP               ==
          382_384  POP_JUMP_IF_FALSE   546  'to 546'

 L. 602       386  LOAD_CONST               3
              388  LOAD_GLOBAL              np
              390  LOAD_ATTR                pi
              392  BINARY_MULTIPLY  
              394  LOAD_CONST               2.0
              396  BINARY_TRUE_DIVIDE
              398  STORE_FAST               'angle'

 L. 604       400  LOAD_FAST                'self'
              402  LOAD_ATTR                portlist
              404  LOAD_FAST                'key'
              406  BINARY_SUBSCR    
              408  LOAD_STR                 'direction'
              410  BINARY_SUBSCR    
              412  LOAD_STR                 'NORTH'
              414  COMPARE_OP               ==
          416_418  POP_JUMP_IF_FALSE   436  'to 436'

 L. 605       420  LOAD_STR                 'EAST'
              422  LOAD_FAST                'self'
              424  LOAD_ATTR                portlist
              426  LOAD_FAST                'key'
              428  BINARY_SUBSCR    
              430  LOAD_STR                 'direction'
              432  STORE_SUBSCR     
              434  JUMP_FORWARD        894  'to 894'
            436_0  COME_FROM           416  '416'

 L. 606       436  LOAD_FAST                'self'
              438  LOAD_ATTR                portlist
              440  LOAD_FAST                'key'
              442  BINARY_SUBSCR    
              444  LOAD_STR                 'direction'
              446  BINARY_SUBSCR    
              448  LOAD_STR                 'EAST'
              450  COMPARE_OP               ==
          452_454  POP_JUMP_IF_FALSE   472  'to 472'

 L. 607       456  LOAD_STR                 'SOUTH'
              458  LOAD_FAST                'self'
              460  LOAD_ATTR                portlist
              462  LOAD_FAST                'key'
              464  BINARY_SUBSCR    
              466  LOAD_STR                 'direction'
              468  STORE_SUBSCR     
              470  JUMP_FORWARD        894  'to 894'
            472_0  COME_FROM           452  '452'

 L. 608       472  LOAD_FAST                'self'
              474  LOAD_ATTR                portlist
              476  LOAD_FAST                'key'
              478  BINARY_SUBSCR    
              480  LOAD_STR                 'direction'
              482  BINARY_SUBSCR    
              484  LOAD_STR                 'SOUTH'
              486  COMPARE_OP               ==
          488_490  POP_JUMP_IF_FALSE   508  'to 508'

 L. 609       492  LOAD_STR                 'WEST'
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                portlist
              498  LOAD_FAST                'key'
              500  BINARY_SUBSCR    
              502  LOAD_STR                 'direction'
              504  STORE_SUBSCR     
              506  JUMP_FORWARD        894  'to 894'
            508_0  COME_FROM           488  '488'

 L. 610       508  LOAD_FAST                'self'
              510  LOAD_ATTR                portlist
              512  LOAD_FAST                'key'
              514  BINARY_SUBSCR    
              516  LOAD_STR                 'direction'
              518  BINARY_SUBSCR    
              520  LOAD_STR                 'WEST'
              522  COMPARE_OP               ==
          524_526  POP_JUMP_IF_FALSE   894  'to 894'

 L. 611       528  LOAD_STR                 'NORTH'
              530  LOAD_FAST                'self'
              532  LOAD_ATTR                portlist
              534  LOAD_FAST                'key'
              536  BINARY_SUBSCR    
              538  LOAD_STR                 'direction'
              540  STORE_SUBSCR     
          542_544  JUMP_FORWARD        894  'to 894'
            546_0  COME_FROM           382  '382'

 L. 612       546  LOAD_GLOBAL              isinstance
              548  LOAD_FAST                'self'
              550  LOAD_ATTR                direction
              552  LOAD_GLOBAL              float
              554  CALL_FUNCTION_2       2  '2 positional arguments'
          556_558  POP_JUMP_IF_TRUE    574  'to 574'
              560  LOAD_GLOBAL              isinstance
              562  LOAD_FAST                'self'
              564  LOAD_ATTR                direction
              566  LOAD_GLOBAL              int
              568  CALL_FUNCTION_2       2  '2 positional arguments'
          570_572  POP_JUMP_IF_FALSE   894  'to 894'
            574_0  COME_FROM           556  '556'

 L. 613       574  LOAD_GLOBAL              float
              576  LOAD_FAST                'self'
              578  LOAD_ATTR                direction
              580  CALL_FUNCTION_1       1  '1 positional argument'
              582  STORE_FAST               'angle'

 L. 615       584  LOAD_GLOBAL              isinstance
              586  LOAD_FAST                'self'
              588  LOAD_ATTR                portlist
              590  LOAD_FAST                'key'
              592  BINARY_SUBSCR    
              594  LOAD_STR                 'direction'
              596  BINARY_SUBSCR    
              598  LOAD_GLOBAL              float
              600  CALL_FUNCTION_2       2  '2 positional arguments'
          602_604  POP_JUMP_IF_TRUE    628  'to 628'
              606  LOAD_GLOBAL              isinstance

 L. 616       608  LOAD_FAST                'self'
              610  LOAD_ATTR                portlist
              612  LOAD_FAST                'key'
              614  BINARY_SUBSCR    
              616  LOAD_STR                 'direction'
              618  BINARY_SUBSCR    
              620  LOAD_GLOBAL              int
              622  CALL_FUNCTION_2       2  '2 positional arguments'
          624_626  POP_JUMP_IF_FALSE   668  'to 668'
            628_0  COME_FROM           602  '602'

 L. 619       628  LOAD_FAST                'self'
              630  LOAD_ATTR                portlist
              632  LOAD_FAST                'key'
              634  BINARY_SUBSCR    
              636  LOAD_STR                 'direction'
              638  BINARY_SUBSCR    
              640  LOAD_FAST                'angle'
              642  BINARY_ADD       

 L. 620       644  LOAD_CONST               2
              646  LOAD_GLOBAL              np
              648  LOAD_ATTR                pi
              650  BINARY_MULTIPLY  
              652  BINARY_MODULO    
              654  LOAD_FAST                'self'
              656  LOAD_ATTR                portlist
              658  LOAD_FAST                'key'
              660  BINARY_SUBSCR    
              662  LOAD_STR                 'direction'
              664  STORE_SUBSCR     
              666  JUMP_FORWARD        894  'to 894'
            668_0  COME_FROM           624  '624'

 L. 622       668  LOAD_FAST                'self'
              670  LOAD_ATTR                portlist
              672  LOAD_FAST                'key'
              674  BINARY_SUBSCR    
              676  LOAD_STR                 'direction'
              678  BINARY_SUBSCR    
              680  LOAD_STR                 'EAST'
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   718  'to 718'

 L. 623       688  LOAD_CONST               0.0
              690  LOAD_FAST                'angle'
              692  BINARY_ADD       
              694  LOAD_CONST               2
              696  LOAD_GLOBAL              np
              698  LOAD_ATTR                pi
              700  BINARY_MULTIPLY  
              702  BINARY_MODULO    
              704  LOAD_FAST                'self'
              706  LOAD_ATTR                portlist
              708  LOAD_FAST                'key'
              710  BINARY_SUBSCR    
              712  LOAD_STR                 'direction'
              714  STORE_SUBSCR     
              716  JUMP_FORWARD        894  'to 894'
            718_0  COME_FROM           684  '684'

 L. 624       718  LOAD_FAST                'self'
              720  LOAD_ATTR                portlist
              722  LOAD_FAST                'key'
              724  BINARY_SUBSCR    
              726  LOAD_STR                 'direction'
              728  BINARY_SUBSCR    
              730  LOAD_STR                 'NORTH'
              732  COMPARE_OP               ==
          734_736  POP_JUMP_IF_FALSE   774  'to 774'

 L. 625       738  LOAD_GLOBAL              np
              740  LOAD_ATTR                pi
              742  LOAD_CONST               2
              744  BINARY_TRUE_DIVIDE
              746  LOAD_FAST                'angle'
              748  BINARY_ADD       

 L. 626       750  LOAD_CONST               2
              752  LOAD_GLOBAL              np
              754  LOAD_ATTR                pi
              756  BINARY_MULTIPLY  
              758  BINARY_MODULO    
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                portlist
              764  LOAD_FAST                'key'
              766  BINARY_SUBSCR    
              768  LOAD_STR                 'direction'
              770  STORE_SUBSCR     
              772  JUMP_FORWARD        894  'to 894'
            774_0  COME_FROM           734  '734'

 L. 628       774  LOAD_FAST                'self'
              776  LOAD_ATTR                portlist
              778  LOAD_FAST                'key'
              780  BINARY_SUBSCR    
              782  LOAD_STR                 'direction'
            784_0  COME_FROM           434  '434'
            784_1  COME_FROM           262  '262'
              784  BINARY_SUBSCR    
              786  LOAD_STR                 'WEST'
              788  COMPARE_OP               ==
            790_0  COME_FROM           104  '104'
          790_792  POP_JUMP_IF_FALSE   826  'to 826'

 L. 629       794  LOAD_GLOBAL              np
              796  LOAD_ATTR                pi
              798  LOAD_FAST                'angle'
              800  BINARY_ADD       
              802  LOAD_CONST               2
              804  LOAD_GLOBAL              np
              806  LOAD_ATTR                pi
              808  BINARY_MULTIPLY  
              810  BINARY_MODULO    
              812  LOAD_FAST                'self'
              814  LOAD_ATTR                portlist
              816  LOAD_FAST                'key'
              818  BINARY_SUBSCR    
            820_0  COME_FROM           470  '470'
            820_1  COME_FROM           298  '298'
              820  LOAD_STR                 'direction'
              822  STORE_SUBSCR     
            824_0  COME_FROM           138  '138'
              824  JUMP_FORWARD        894  'to 894'
            826_0  COME_FROM           790  '790'

 L. 630       826  LOAD_FAST                'self'
              828  LOAD_ATTR                portlist
              830  LOAD_FAST                'key'
              832  BINARY_SUBSCR    
              834  LOAD_STR                 'direction'
              836  BINARY_SUBSCR    
              838  LOAD_STR                 'SOUTH'
              840  COMPARE_OP               ==
          842_844  POP_JUMP_IF_FALSE   886  'to 886'

 L. 631       846  LOAD_CONST               3
              848  LOAD_GLOBAL              np
              850  LOAD_ATTR                pi
              852  BINARY_MULTIPLY  
              854  LOAD_CONST               2
            856_0  COME_FROM           506  '506'
            856_1  COME_FROM           334  '334'
              856  BINARY_TRUE_DIVIDE
            858_0  COME_FROM           172  '172'
              858  LOAD_FAST                'angle'
              860  BINARY_ADD       

 L. 632       862  LOAD_CONST               2
              864  LOAD_GLOBAL              np
              866  LOAD_ATTR                pi
              868  BINARY_MULTIPLY  
              870  BINARY_MODULO    
              872  LOAD_FAST                'self'
              874  LOAD_ATTR                portlist
              876  LOAD_FAST                'key'
              878  BINARY_SUBSCR    
              880  LOAD_STR                 'direction'
              882  STORE_SUBSCR     
              884  JUMP_FORWARD        894  'to 894'
            886_0  COME_FROM           842  '842'

 L. 635       886  LOAD_GLOBAL              ValueError

 L. 636       888  LOAD_STR                 'One of the portlist directions has an invalid value.'
              890  CALL_FUNCTION_1       1  '1 positional argument'
              892  RAISE_VARARGS_1       1  'exception instance'
            894_0  COME_FROM           884  '884'
            894_1  COME_FROM           824  '824'
            894_2  COME_FROM           772  '772'
            894_3  COME_FROM           716  '716'
            894_4  COME_FROM           666  '666'
            894_5  COME_FROM           570  '570'
            894_6  COME_FROM           542  '542'
            894_7  COME_FROM           524  '524'
            894_8  COME_FROM           370  '370'
            894_9  COME_FROM           352  '352'
           894_10  COME_FROM           206  '206'
           894_11  COME_FROM            48  '48'

 L. 639       894  LOAD_FAST                'cur_port'
              896  LOAD_CONST               0
              898  BINARY_SUBSCR    
              900  LOAD_GLOBAL              np
              902  LOAD_METHOD              cos
              904  LOAD_FAST                'angle'
              906  CALL_METHOD_1         1  '1 positional argument'
              908  BINARY_MULTIPLY  
              910  LOAD_FAST                'cur_port'
              912  LOAD_CONST               1
              914  BINARY_SUBSCR    
              916  LOAD_GLOBAL              np
              918  LOAD_METHOD              sin
              920  LOAD_FAST                'angle'
              922  CALL_METHOD_1         1  '1 positional argument'
              924  BINARY_MULTIPLY  
              926  BINARY_SUBTRACT  
              928  STORE_FAST               'dx'

 L. 640       930  LOAD_FAST                'cur_port'
              932  LOAD_CONST               0
              934  BINARY_SUBSCR    
              936  LOAD_GLOBAL              np
              938  LOAD_METHOD              sin
              940  LOAD_FAST                'angle'
              942  CALL_METHOD_1         1  '1 positional argument'
              944  BINARY_MULTIPLY  
              946  LOAD_FAST                'cur_port'
              948  LOAD_CONST               1
              950  BINARY_SUBSCR    
              952  LOAD_GLOBAL              np
              954  LOAD_METHOD              cos
              956  LOAD_FAST                'angle'
              958  CALL_METHOD_1         1  '1 positional argument'
              960  BINARY_MULTIPLY  
              962  BINARY_ADD       
              964  STORE_FAST               'dy'

 L. 642       966  LOAD_FAST                'self'
              968  LOAD_ATTR                port
              970  LOAD_CONST               0
              972  BINARY_SUBSCR    
              974  LOAD_FAST                'dx'
              976  BINARY_ADD       
              978  LOAD_FAST                'self'
              980  LOAD_ATTR                port
              982  LOAD_CONST               1
              984  BINARY_SUBSCR    
              986  LOAD_FAST                'dy'
              988  BINARY_ADD       
              990  BUILD_TUPLE_2         2 
              992  LOAD_FAST                'self'
              994  LOAD_ATTR                portlist
              996  LOAD_FAST                'key'
              998  BINARY_SUBSCR    
             1000  LOAD_STR                 'port'
             1002  STORE_SUBSCR     
             1004  JUMP_BACK            14  'to 14'
             1006  POP_BLOCK        
           1008_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 784_0

    def _hash_cell_(self, *args):
        """ Check to see if the same exact cell has been created already (with the same parameters).
        If not, add the cell to the global CURRENT_CELLS dictionary.
        If so, point to the identical cell in the CURRENT_CELLS dictionary.
        """
        global CURRENT_CELLS
        dont_hash = [
         'port', 'direction', 'self']
        args = args[0]
        new_args = []
        for k in args.keys():
            if k not in dont_hash:
                try:
                    if 'WaveguideTemplate' in args[k].name or 'MetalTemplate' in args[k].name:
                        new_args.append(args[k].name)
                except:
                    new_args.append(args[k])

        properties = self.name_prefix + ''.join([str(p) for p in new_args])
        self.cell_hash = properties
        if self.cell_hash not in CURRENT_CELLS.keys():
            CURRENT_CELLS[self.cell_hash] = gdspy.Cell(getCellName(self.name_prefix))
            self.first_cell = True
        else:
            self.first_cell = False

    def __get_cell(self):
        return CURRENT_CELLS[self.cell_hash]

    def __direction_to_rotation(self, direction):
        if isinstance(direction, float):
            return direction * 180.0 / np.pi
        if str(direction) == 'EAST':
            return 0.0
        if str(direction) == 'NORTH':
            return 90.0
        if str(direction) == 'WEST':
            return 180.0
        if str(direction) == 'SOUTH':
            return 270.0

    def add(self, element, origin=(0, 0), rotation=0.0, x_reflection=False):
        """ Add a reference to an element or list of elements to the cell associated with this component """
        this_cell = CURRENT_CELLS[self.cell_hash]
        if self.first_cell == True:
            if isinstance(element, Component):
                element_cell = CURRENT_CELLS[element.cell_hash]
                rot = self._Component__direction_to_rotation(element.direction)
                this_cell.add(gdspy.CellReference(element_cell,
                  origin=(element.port),
                  rotation=rot,
                  x_reflection=x_reflection))
            else:
                if isinstance(element, gdspy.Cell):
                    this_cell.add(gdspy.CellReference(element,
                      origin=origin,
                      rotation=rotation,
                      x_reflection=x_reflection))
                else:
                    this_cell.add(element)

    def addto(self, top_cell, x_reflection=False):
        rot = self._Component__direction_to_rotation(self.direction)
        if isinstance(top_cell, gdspy.Cell):
            top_cell.add(gdspy.CellReference((CURRENT_CELLS[self.cell_hash]),
              origin=(self.port),
              rotation=rot,
              x_reflection=x_reflection))
        else:
            if isinstance(top_cell, Component):
                tc = CURRENT_CELLS[top_cell.cell_hash]
                tc.add(gdspy.CellReference((CURRENT_CELLS[self.cell_hash]),
                  origin=(self.port),
                  rotation=rot,
                  x_reflection=x_reflection))