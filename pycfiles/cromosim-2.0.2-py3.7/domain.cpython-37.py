# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cromosim/domain.py
# Compiled at: 2020-04-23 17:01:27
# Size of source mod 2**32: 30297 bytes
import numpy as np, scipy as sp, sys, random, matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Rectangle, Polygon
from matplotlib.lines import Line2D
import PIL
from PIL import Image
from PIL import ImageDraw
import skfmm

class Destination:
    __doc__ = '\n    A Destination object contains all the information necessary to direct\n    people to a goal, for example a door, a staircase or another floor.\n\n    Attributes\n    ----------\n\n    name: string\n       name of the destination\n    colors: list\n       List of colors ``[ [r,g,b],... ]`` drawing the destination.\n       For example, a door can be represented by a red line.\n    excluded_colors: list\n        List of colors ``[ [r,g,b],... ]`` representing obstacles that cannot be crossed for\n        someone wishing to go to this destination: the walls of course, but\n        possibly another objects only visible to the people concerned by\n        this destination.\n    desired_velocity_from_color: list\n        Allows you to associate a desired velocity (vx, vy) with a\n        color (r, g, b):\n            ``[ [r,g,b, vx,vy],... ]``.\n    fmm_speed: numpy array\n        To automatically calculate the desired velocity leading to this\n        destination, a Fast-Marching method is used to calculate the travel\n        time to this destination. The opposite of the gradient of this time\n        gives the desired velocity. This method solves the Eikonal equation\n        ``|grad D| = 1/fmm_speed``. By changing the ``fmm_speed`` (1 everywhere by\n        default) you can make certain areas slower and thus modify the\n        desired velocity to divert people\n    velocity_scale: float\n        Multiplying coefficient used in front of the desired velocity vector\n        (which is renormalized). For example on a staircase one may wish to\n        reduce the speed of people.\n    next_destination: string\n        Name of the next destination. Useful for linking destinations one\n        after the other\n    next_domain: string\n        Name of the next domain where is the next_destination\n    next_transit_box: list\n        The people in the current domain present in this box will be duplicated\n        in the next_domain. A box is defined by four points:\n            ``[x0, y0, x1, y1, x2, y2, x3, y3]``\n    distance: numpy array\n        Distance (if ``fmm_speed`` == 1) or travel time (if ``fmm_speed`` != 1)\n        to the destination\n    desired_velocity_X: numpy array\n        First component of the desired velocity\n    desired_velocity_Y: numpy array\n        Second component of the desired velocity\n\n    Examples\n    --------\n\n     * Examples with one destination:\n        ``cromosim/examples/domain/domain_room.py``\n        ``cromosim/examples/domain/domain_stadium.py``\n     * Example with several destinations:\n        ``cromosim/examples/domain/domain_shibuya_crossing.py``\n     * Example with a destination described in a json file\n        ``cromosim/examples/domain/domain_from_json.py``\n    '

    def __init__(self, name, colors, excluded_colors=[], desired_velocity_from_color=[], fmm_speed=None, velocity_scale=1, next_destination=None, next_domain=None, next_transit_box=None):
        """
        Constructor of a Destination object

        Parameters
        ----------

        name: string
           name of the destination
        colors: list ``[ [r,g,b],... ]``
           List of colors drawing the destination. For example, a door can be
           represented by a red line.
        excluded_colors: = list ``[ [r,g,b],... ]``
            List of colors representing obstacles that cannot be crossed for
            someone wishing to go to this destination: the walls of course, but
            possibly another objects only visible to the people concerned by
            this destination.
        desired_velocity_from_color: list ``[ [r,g,b, vx,vy],... ]``
            Allows you to associate a desired velocity (vx, vy) with a
            color (r, g, b)
        fmm_speed:= numpy array
            To automatically calculate the desired velocity leading to this
            destination, a Fast-Marching method is used to calculate the travel
            time to this destination. The opposite of the gradient of this time
            gives the desired velocity. This method solves the Eikonal equation
            |grad D| = 1/fmm_speed. By changing the fmm_speed (1 everywhere by
            default) you can make certain areas slower and thus modify the
            desired velocity to divert people
        velocity_scale: float
            Multiplying coefficient used in front of the desired velocity vector
            (which is renormalized). For example on a staircase one may wish to
            reduce the speed of people.
        next_destination: string
            Name of the next destination. Useful for linking destinations one
            after the other
        next_domain:
            Name of the next domain where is the next_destination
        next_transit_box:
            The people in the current domain present in this box will be duplicated
            in the ``next_domain``.

        """
        self.name = name
        self.colors = colors
        self.excluded_colors = excluded_colors
        self.desired_velocity_from_color = desired_velocity_from_color
        self.fmm_speed = fmm_speed
        self.velocity_scale = velocity_scale
        self.next_destination = next_destination
        self.next_transit_box = next_transit_box
        self.next_domain = next_domain
        self.distance = None
        self.desired_velocity_X = None
        self.desired_velocity_Y = None

    def __str__(self):
        """
        Print this Destination object
        """
        return '--> Destination: \n    name: ' + str(self.name) + '\n    colors: ' + str(self.colors) + '\n    excluded_colors: ' + str(self.excluded_colors) + '\n    desired_velocity_from_color: ' + str(self.desired_velocity_from_color) + '\n    next_destination: ' + str(self.next_destination) + '\n    next_domain: ' + str(self.next_domain) + '\n    velocity_scale: ' + str(self.velocity_scale)


class Domain:
    __doc__ = '\n    To define the computational domain:\n     * a background: empty (white) or a PNG image which only\n       contains the colors white, red (for the doors) and black\n       (for the walls)\n     * supplementary doors represented by matplotlib shapes:\n        ``line2D``\n     * supplementary walls represented by matplotlib shapes:\n        ``line2D``, ``circle``, ``ellipse``, ``rectangle`` or ``polygon``\n\n    To compute the obstacle distances and the desired velocities\n\n    Attributes\n    ----------\n\n    pixel_size: float\n        size of a pixel in meters\n    width: int\n        width of the background image (number of pixels)\n    height: int\n        height of the background image (number of pixels)\n    xmin: float\n        x coordinate of the origin (bottom left corner)\n    xmax: float\n        ``xmax = xmin + width*pixel_size``\n    ymin: float\n        y coordinate of the origin (bottom left corner)\n    ymax: float\n        ``ymax = ymin + height*pixel_size``\n    X: numpy array\n        x coordinates (meshgrid)\n    Y: numpy array\n        y coordinates (meshgrid)\n    image: numpy array\n        pixel array (r,g,b,a)\n        The Pillow image is converted to a numpy arrays, then\n        using ``flipud``\n        the origin of the image is put it down left instead the\n        top left\n    image_red: numpy array\n        red values of the image (r,g,b,a)\n    image_green: numpy array\n        green values of the image (r,g,b,a)\n    image_blue: numpy array\n        blue values of the image (r,g,b,a)\n    wall_mask: numpy array\n        boolean array: true for wall pixels\n    wall_mask_id: numpy array\n        wall pixel indices\n    wall_distance: numpy array\n        distance (m) to the wall\n    wall_grad_X: numpy array\n        gradient of the distance to the wall (first component)\n    wall_grad_Y: numpy array\n        gradient of the distance to the wall (second component)\n    door_distance: numpy array\n        distance (m) to the door\n    desired_velocity_X: numpy array\n        opposite of the gradient of the distance to the door: desired velocity\n         (first component)\n    desired_velocity_Y: numpy array\n        opposite of the gradient of the distance to the door: desired velocity\n        (second component)\n\n    Examples\n    --------\n\n    * A simple room\n        ``cromosim/examples/domain/domain_room.py``\n    * A circular domain\n        ``cromosim/examples/domain/domain_stadium.py``\n    * A domain with several destinations\n        ``cromosim/examples/domain/domain_shibuya_crossing.py``\n    * A domain built from json file (where is its description)\n        ``cromosim/examples/domain/domain_from_json.py``\n    '

    def __init__(self, name='Domain', background='White', pixel_size=1.0, xmin=0.0, width=100, ymin=0.0, height=100, wall_colors=[
 [
  0, 0, 0]], npzfile=None):
        """
        Constructor of a Domain object

        Parameters
        ----------

        name: string
            domain name (default: 'Domain')
        background: string
            name of the background image (default: 'White', no image)
        pixel_size: float
            size of a pixel in meters (default: 1.0)
        xmin: float
            x coordinate of the origin, bottom left corner (default: 0.0)
        ymin: float
            y coordinate of the origin, bottom left corner (default: 0.0)
        width: int
            width of the background image (default: 100 pixels)
        height: int
            height of the background image (default: 100 pixels)
        npzfile: string
            to build domain from a npz file which contains all variables
        """
        if npzfile is None:
            self._Domain__shapes = []
            self._Domain__outline_color_shapes = []
            self._Domain__fill_color_shapes = []
            self._Domain__image_filename = ''
            self.name = name
            self._Domain__background = background
            self.destinations = None
            self.pixel_size = pixel_size
            self.xmin, self.ymin = [xmin, ymin]
            if self._Domain__background != 'White':
                self.image = Image.open(self._Domain__background)
                self.width = self.image.size[0]
                self.height = self.image.size[1]
            else:
                self.width, self.height = [
                 width, height]
                self.image = Image.new('RGB', (self.width, self.height), 'white')
            self.xmax = self.xmin + self.width * pixel_size
            self.ymax = self.ymin + self.height * pixel_size
            self.X, self.Y = sp.meshgrid(sp.arange(self.width), sp.arange(self.height))
            self.X = 0.5 * self.pixel_size + self.xmin + self.X * self.pixel_size
            self.Y = 0.5 * self.pixel_size + self.ymin + self.Y * self.pixel_size
            self.wall_colors = wall_colors
            self.wall_mask = None
            self.wall_id = None
            self.wall_distance = None
            self.wall_grad_X = None
            self.wall_grad_Y = None
            self.draw = ImageDraw.Draw(self.image)
        else:
            data = sp.load(npzfile, allow_pickle=True)
            self._Domain__shapes = data['__shapes'].tolist()
            self._Domain__outline_color_shapes = data['__outline_color_shapes'].tolist()
            self._Domain__fill_color_shapes = data['__fill_color_shapes'].tolist()
            self._Domain__image_filename = data['__image_filename']
            self.name = str(data['name'])
            self._Domain__background = str(data['__background'])
            self.destinations = dict(data['destinations'].tolist())
            self.pixel_size = data['pixel_size']
            self.xmin = data['xmin']
            self.ymin = data['ymin']
            self.xmax = data['xmax']
            self.ymax = data['ymax']
            self.width = data['width']
            self.height = data['height']
            self.X = data['X']
            self.Y = data['Y']
            self.wall_colors = data['wall_colors']
            self.wall_mask = data['wall_mask']
            self.wall_id = data['wall_id']
            self.wall_distance = data['wall_distance']
            self.wall_grad_X = data['wall_grad_X']
            self.wall_grad_Y = data['wall_grad_Y']
            self.image = data['image']

    def save(self, outfile):
        """To save the content of the domain in a file

        Parameters
        ----------

        outfile: string
            output filename
        """
        sp.savez(outfile, __shapes=(self._Domain__shapes),
          __outline_color_shapes=(self._Domain__outline_color_shapes),
          __fill_color_shapes=(self._Domain__fill_color_shapes),
          __image_filename=(self._Domain__image_filename),
          name=(self.name),
          __background=(self._Domain__background),
          pixel_size=(self.pixel_size),
          xmin=(self.xmin),
          ymin=(self.ymin),
          xmax=(self.xmax),
          ymax=(self.ymax),
          width=(self.width),
          height=(self.height),
          X=(self.X),
          Y=(self.Y),
          wall_colors=(self.wall_colors),
          wall_mask=(self.wall_mask),
          wall_id=(self.wall_id),
          wall_distance=(self.wall_distance),
          wall_grad_X=(self.wall_grad_X),
          wall_grad_Y=(self.wall_grad_Y),
          destinations=(self.destinations),
          image=(self.image))

    def add_shape--- This code section failed: ---

 L. 390         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _Domain__shapes
                4  LOAD_METHOD              append
                6  LOAD_FAST                'shape'
                8  CALL_METHOD_1         1  '1 positional argument'
               10  POP_TOP          

 L. 391        12  LOAD_FAST                'self'
               14  LOAD_ATTR                _Domain__outline_color_shapes
               16  LOAD_METHOD              append
               18  LOAD_FAST                'outline_color'
               20  CALL_METHOD_1         1  '1 positional argument'
               22  POP_TOP          

 L. 392        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _Domain__fill_color_shapes
               28  LOAD_METHOD              append
               30  LOAD_FAST                'fill_color'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  POP_TOP          

 L. 393        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'shape'
               40  LOAD_GLOBAL              Circle
               42  CALL_FUNCTION_2       2  '2 positional arguments'
               44  POP_JUMP_IF_TRUE     78  'to 78'
               46  LOAD_GLOBAL              isinstance
               48  LOAD_FAST                'shape'
               50  LOAD_GLOBAL              Ellipse
               52  CALL_FUNCTION_2       2  '2 positional arguments'
               54  POP_JUMP_IF_TRUE     78  'to 78'

 L. 394        56  LOAD_GLOBAL              isinstance
               58  LOAD_FAST                'shape'
               60  LOAD_GLOBAL              Rectangle
               62  CALL_FUNCTION_2       2  '2 positional arguments'
               64  POP_JUMP_IF_TRUE     78  'to 78'
               66  LOAD_GLOBAL              isinstance
               68  LOAD_FAST                'shape'
               70  LOAD_GLOBAL              Polygon
               72  CALL_FUNCTION_2       2  '2 positional arguments'
            74_76  POP_JUMP_IF_FALSE   348  'to 348'
             78_0  COME_FROM            64  '64'
             78_1  COME_FROM            54  '54'
             78_2  COME_FROM            44  '44'

 L. 395        78  LOAD_FAST                'shape'
               80  LOAD_METHOD              get_verts
               82  CALL_METHOD_0         0  '0 positional arguments'
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                pixel_size
               88  BINARY_TRUE_DIVIDE
               90  STORE_FAST               'xy'

 L. 396        92  LOAD_FAST                'self'
               94  LOAD_ATTR                height
               96  LOAD_FAST                'xy'
               98  LOAD_CONST               None
              100  LOAD_CONST               None
              102  BUILD_SLICE_2         2 
              104  LOAD_CONST               1
              106  BUILD_TUPLE_2         2 
              108  BINARY_SUBSCR    
              110  BINARY_SUBTRACT  
              112  LOAD_FAST                'xy'
              114  LOAD_CONST               None
              116  LOAD_CONST               None
              118  BUILD_SLICE_2         2 
              120  LOAD_CONST               1
              122  BUILD_TUPLE_2         2 
              124  STORE_SUBSCR     

 L. 397       126  LOAD_FAST                'self'
              128  LOAD_ATTR                draw
              130  LOAD_ATTR                polygon
              132  LOAD_GLOBAL              sp
              134  LOAD_METHOD              around
              136  LOAD_FAST                'xy'
              138  LOAD_METHOD              flatten
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  LOAD_METHOD              tolist
              146  CALL_METHOD_0         0  '0 positional arguments'

 L. 400       148  LOAD_STR                 'rgb('
              150  LOAD_GLOBAL              str
              152  LOAD_FAST                'outline_color'
              154  LOAD_CONST               0
              156  BINARY_SUBSCR    
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  BINARY_ADD       
              162  LOAD_STR                 ','
              164  BINARY_ADD       
              166  LOAD_GLOBAL              str
              168  LOAD_FAST                'outline_color'
              170  LOAD_CONST               1
              172  BINARY_SUBSCR    
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  BINARY_ADD       
              178  LOAD_STR                 ','
              180  BINARY_ADD       
              182  LOAD_GLOBAL              str
              184  LOAD_FAST                'outline_color'
              186  LOAD_CONST               2
              188  BINARY_SUBSCR    
              190  CALL_FUNCTION_1       1  '1 positional argument'
              192  BINARY_ADD       
              194  LOAD_STR                 ')'
              196  BINARY_ADD       

 L. 403       198  LOAD_STR                 'rgb('
              200  LOAD_GLOBAL              str
              202  LOAD_FAST                'fill_color'
              204  LOAD_CONST               0
              206  BINARY_SUBSCR    
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  BINARY_ADD       
              212  LOAD_STR                 ','
              214  BINARY_ADD       
              216  LOAD_GLOBAL              str
              218  LOAD_FAST                'fill_color'
              220  LOAD_CONST               1
              222  BINARY_SUBSCR    
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  BINARY_ADD       
              228  LOAD_STR                 ','
              230  BINARY_ADD       
              232  LOAD_GLOBAL              str
              234  LOAD_FAST                'fill_color'
              236  LOAD_CONST               2
              238  BINARY_SUBSCR    
              240  CALL_FUNCTION_1       1  '1 positional argument'
              242  BINARY_ADD       
              244  LOAD_STR                 ')'
              246  BINARY_ADD       
              248  LOAD_CONST               ('outline', 'fill')
              250  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              252  POP_TOP          

 L. 404       254  LOAD_FAST                'shape'
              256  LOAD_METHOD              get_linewidth
              258  CALL_METHOD_0         0  '0 positional arguments'
              260  STORE_FAST               'linewidth'

 L. 405       262  LOAD_FAST                'self'
              264  LOAD_ATTR                draw
              266  LOAD_ATTR                line
              268  LOAD_GLOBAL              sp
              270  LOAD_METHOD              around
              272  LOAD_FAST                'xy'
              274  LOAD_METHOD              flatten
              276  CALL_METHOD_0         0  '0 positional arguments'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  LOAD_METHOD              tolist
              282  CALL_METHOD_0         0  '0 positional arguments'

 L. 406       284  LOAD_GLOBAL              int
              286  LOAD_FAST                'linewidth'
              288  CALL_FUNCTION_1       1  '1 positional argument'

 L. 409       290  LOAD_STR                 'rgb('
              292  LOAD_GLOBAL              str
              294  LOAD_FAST                'outline_color'
              296  LOAD_CONST               0
              298  BINARY_SUBSCR    
              300  CALL_FUNCTION_1       1  '1 positional argument'
              302  BINARY_ADD       
              304  LOAD_STR                 ','
              306  BINARY_ADD       
              308  LOAD_GLOBAL              str
              310  LOAD_FAST                'outline_color'
              312  LOAD_CONST               1
              314  BINARY_SUBSCR    
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  BINARY_ADD       
              320  LOAD_STR                 ','
              322  BINARY_ADD       
              324  LOAD_GLOBAL              str
              326  LOAD_FAST                'outline_color'
              328  LOAD_CONST               2
              330  BINARY_SUBSCR    
              332  CALL_FUNCTION_1       1  '1 positional argument'
              334  BINARY_ADD       
              336  LOAD_STR                 ')'
              338  BINARY_ADD       
              340  LOAD_CONST               ('width', 'fill')
              342  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              344  POP_TOP          
              346  JUMP_FORWARD        500  'to 500'
            348_0  COME_FROM            74  '74'

 L. 410       348  LOAD_GLOBAL              isinstance
              350  LOAD_FAST                'shape'
              352  LOAD_GLOBAL              Line2D
              354  CALL_FUNCTION_2       2  '2 positional arguments'
          356_358  POP_JUMP_IF_FALSE   500  'to 500'

 L. 411       360  LOAD_FAST                'shape'
              362  LOAD_METHOD              get_linewidth
              364  CALL_METHOD_0         0  '0 positional arguments'
              366  STORE_FAST               'linewidth'

 L. 412       368  LOAD_FAST                'shape'
              370  LOAD_METHOD              get_xydata
              372  CALL_METHOD_0         0  '0 positional arguments'
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                pixel_size
              378  BINARY_TRUE_DIVIDE
              380  STORE_FAST               'xy'

 L. 413       382  LOAD_FAST                'self'
              384  LOAD_ATTR                height
              386  LOAD_FAST                'xy'
              388  LOAD_CONST               None
              390  LOAD_CONST               None
              392  BUILD_SLICE_2         2 
              394  LOAD_CONST               1
              396  BUILD_TUPLE_2         2 
              398  BINARY_SUBSCR    
              400  BINARY_SUBTRACT  
              402  LOAD_FAST                'xy'
              404  LOAD_CONST               None
              406  LOAD_CONST               None
              408  BUILD_SLICE_2         2 
              410  LOAD_CONST               1
              412  BUILD_TUPLE_2         2 
              414  STORE_SUBSCR     

 L. 414       416  LOAD_FAST                'self'
              418  LOAD_ATTR                draw
              420  LOAD_ATTR                line
              422  LOAD_GLOBAL              sp
              424  LOAD_METHOD              around
              426  LOAD_FAST                'xy'
              428  LOAD_METHOD              flatten
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  LOAD_METHOD              tolist
              436  CALL_METHOD_0         0  '0 positional arguments'

 L. 415       438  LOAD_GLOBAL              int
              440  LOAD_FAST                'linewidth'
              442  CALL_FUNCTION_1       1  '1 positional argument'

 L. 418       444  LOAD_STR                 'rgb('
              446  LOAD_GLOBAL              str
              448  LOAD_FAST                'outline_color'
              450  LOAD_CONST               0
              452  BINARY_SUBSCR    
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  BINARY_ADD       
              458  LOAD_STR                 ','
              460  BINARY_ADD       
              462  LOAD_GLOBAL              str
              464  LOAD_FAST                'outline_color'
              466  LOAD_CONST               1
              468  BINARY_SUBSCR    
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  BINARY_ADD       
              474  LOAD_STR                 ','
              476  BINARY_ADD       
              478  LOAD_GLOBAL              str
              480  LOAD_FAST                'outline_color'
              482  LOAD_CONST               2
              484  BINARY_SUBSCR    
              486  CALL_FUNCTION_1       1  '1 positional argument'
              488  BINARY_ADD       
              490  LOAD_STR                 ')'
              492  BINARY_ADD       
              494  LOAD_CONST               ('width', 'fill')
              496  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              498  POP_TOP          
            500_0  COME_FROM           356  '356'
            500_1  COME_FROM           346  '346'

Parse error at or near `JUMP_FORWARD' instruction at offset 346

    def build_domain(self):
        """To build the domain: reads the background image (if supplied)         and initializes all the color arrrays
        """
        self._Domain__image_filename = self.name + '_domain.png'
        self.image.save(self._Domain__image_filename)
        self.image = np.flipud(np.array(self.image))
        self.image_red = self.image[:, :, 0]
        self.image_green = self.image[:, :, 1]
        self.image_blue = self.image[:, :, 2]
        self.wall_mask = sp.zeros_like(self.image_red)
        for c in self.wall_colors:
            self.wall_mask += (self.image_red == c[0]) * (self.image_green == c[1]) * (self.image_blue == c[2])

        self.wall_id = sp.where(self.wall_mask > 0)
        if self.wall_id[0].size > 0:
            self.compute_wall_distance()
        else:
            print('WARNING: Failed to compute wall distance!')
            print('WARNING: Wall colors are ', self.wall_colors)
            print('WARNING: Check that there are pixels with these colors!')
            sys.exit()

    def compute_wall_distance(self):
        """To compute the geodesic distance to the walls in using
        a fast-marching method
        """
        phi = sp.ones(self.image_red.shape)
        if len(self.wall_id[0]) > 0:
            phi[self.wall_id] = 0
            self.wall_distance = skfmm.distance(phi, dx=(self.pixel_size))
            grad = np.gradient((self.wall_distance), edge_order=2)
            grad_X = grad[1] / self.pixel_size
            grad_Y = grad[0] / self.pixel_size
            norm = np.sqrt(grad_X ** 2 + grad_Y ** 2)
            norm = (norm > 0) * norm + (norm == 0) * 0.001
            self.wall_grad_X = grad_X / norm
            self.wall_grad_Y = grad_Y / norm
        else:
            self.wall_distance = 1e+99 * np.ones(self.image_red.shape)

    def add_destination(self, dest):
        """To compute the desired velocities to this destination
        and then to add this Destination object to this domain.

        Parameters
        ----------

        dest: Destination
            contains the Destination object which must be added to this domain
        """
        excluded_color_mask = sp.zeros_like(self.image_red)
        for c in dest.excluded_colors:
            excluded_color_mask += (self.image_red == c[0]) * (self.image_green == c[1]) * (self.image_blue == c[2])

        excluded_color_id = sp.where(excluded_color_mask > 0)
        dest_mask = sp.zeros_like(self.image_red)
        for ic, rgb in enumerate(dest.colors):
            dest_mask = (self.image_red == rgb[0]) * (self.image_green == rgb[1]) * (self.image_blue == rgb[2])

        mask_id = sp.where(dest_mask >= 1)
        if dest.fmm_speed is not None:
            if dest.fmm_speed.shape != self.image_red.shape:
                print('Bad speed shape ! Failed to compute the destination distance...')
                sys.exit()
        else:
            dest.fmm_speed = sp.ones_like(self.image_red)
        if mask_id[0].size > 0:
            dest_mask[mask_id] = True
            phi = sp.ones(self.image_red.shape)
            phi[mask_id] = 0
            phi = sp.ma.MaskedArray(phi, mask=excluded_color_mask)
            dest.distance = skfmm.travel_time(phi, (dest.fmm_speed), dx=(self.pixel_size))
            if excluded_color_id[0].size > 0:
                tmp_dist = dest.distance.filled(9999)
            else:
                tmp_dist = dest.distance
            grad = sp.gradient(tmp_dist, edge_order=2)
        else:
            dest.distance = -sp.ones_like(self.image_red)
            grad = sp.gradient((sp.zeros_like(self.image_red)), edge_order=2)
        for l, rgbgrad in enumerate(dest.desired_velocity_from_color):
            test = (self.image_red == int(rgbgrad[0])) * (self.image_green == int(rgbgrad[1])) * (self.image_blue == int(rgbgrad[2]))
            indices = sp.where(test == True)
            grad[1][indices] = -rgbgrad[3]
            grad[0][indices] = -rgbgrad[4]

        grad_X = -grad[1] / self.pixel_size
        grad_Y = -grad[0] / self.pixel_size
        norm = np.sqrt(grad_X ** 2 + grad_Y ** 2)
        norm = (norm > 0) * norm + (norm == 0) * 0.001
        dest.desired_velocity_X = grad_X / norm
        dest.desired_velocity_Y = grad_Y / norm
        try:
            self.destinations[dest.name] = dest
        except:
            self.destinations = {dest.name: dest}

    def people_desired_velocity(self, xyr, people_dest, I=None, J=None):
        """This function determines people desired velocities from the desired         velocity array computed by Domain thanks to a fast-marching method.

        Parameters
        ----------
        xyr: numpy array
            people coordinates and radius: x,y,r
        people_dest: list of string
            destination for each individual
        I: numpy array (None by default)
            people index i
        J: numpy array (None by default)
            people index j

        Returns
        -------
        I: numpy array
            people index i
        J: numpy array
            people index j
        Vd: numpy array
            people desired velocity
        """
        if I is None or J is None:
            I = sp.floor((xyr[:, 1] - self.ymin - 0.5 * self.pixel_size) / self.pixel_size).astype(int)
            J = sp.floor((xyr[:, 0] - self.xmin - 0.5 * self.pixel_size) / self.pixel_size).astype(int)
        Vd = sp.zeros((xyr.shape[0], 2))
        for id, dest_name in enumerate(np.unique(people_dest)):
            ind = np.where(np.array(people_dest) == dest_name)[0]
            scale = self.destinations[dest_name].velocity_scale
            Vd[(ind, 0)] = xyr[(ind, 3)] * scale * self.destinations[dest_name].desired_velocity_X[(I[ind], J[ind])]
            Vd[(ind, 1)] = xyr[(ind, 3)] * scale * self.destinations[dest_name].desired_velocity_Y[(I[ind], J[ind])]

        return (
         I, J, Vd)

    def people_target_distance(self, xyr, people_dest, I=None, J=None):
        """This function determines distances to the current target for all people

        Parameters
        ----------
        xyr: numpy array
            people coordinates and radius: ``x,y,r``
        people_dest: list of string
            destination for each individual
        I: numpy array (None by default)
            people index ``i``
        J: numpy array (None by default)
            people index ``j``
        Returns
        -------
        I: numpy array
            people index i
        J: numpy array
            people index j
        D: numpy array
            distances to the current target
        """
        if I is None or J is None:
            I = sp.floor((xyr[:, 1] - self.ymin - 0.5 * self.pixel_size) / self.pixel_size).astype(int)
            J = sp.floor((xyr[:, 0] - self.xmin - 0.5 * self.pixel_size) / self.pixel_size).astype(int)
        D = np.zeros(xyr.shape[0])
        for id, dest_name in enumerate(np.unique(people_dest)):
            ind = np.where(np.array(people_dest) == dest_name)[0]
            D[ind] = self.destinations[dest_name].distance[(I[ind], J[ind])] - xyr[(ind, 2)]

        return (
         I, J, D)

    def people_wall_distance(self, xyr, I=None, J=None):
        """This function determines distances to the nearest wall for all people

        Parameters
        ----------
        xyr: numpy array
            people coordinates and radius: ``x,y,r``
        I: numpy array (None by default)
            people index ``i``
        J: numpy array (None by default)
            people index ``j``

        Returns
        -------
        I: numpy array
            people index ``i``
        J: numpy array
            people index ``j``
        D: numpy array
            distances to the nearest wall
        """
        if I is None or J is None:
            I = sp.floor((xyr[:, 1] - self.ymin - 0.5 * self.pixel_size) / self.pixel_size).astype(int)
            J = sp.floor((xyr[:, 0] - self.xmin - 0.5 * self.pixel_size) / self.pixel_size).astype(int)
        D = self.wall_distance[(I, J)] - xyr[:, 2]
        return (I, J, D)

    def plot(self, id=1, title='', savefig=False, filename='fig.png', dpi=150):
        """To plot the computational domain

        Parameters
        ----------

        id: integer
            Figure id (number)
        title: string
            Figure title
        savefig: boolean
            writes the figure as a png file if true
        filename: string
            png filename used to write the figure
        dpi: integer
            number of pixel per inch for the saved figure
        """
        fig = plt.figure(id)
        ax1 = fig.add_subplot(111)
        ax1.imshow((self.image), interpolation='nearest', extent=[self.xmin, self.xmax,
         self.ymin, self.ymax],
          origin='lower')
        ax1.set_axis_off()
        ax1.set_title(title)
        plt.draw()
        if savefig:
            fig.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0)

    def plot_wall_dist(self, step=10, scale=10, scale_units='inches', id=1, title='', savefig=False, filename='fig.png', dpi=150):
        """To plot the wall distances

        Parameters
        ----------

        id: integer
            Figure id (number)
        title: string
            Figure title
        savefig: boolean
            writes the figure as a png file if true
        filename: string
            png filename used to write the figure
        dpi: integer
            number of pixel per inch for the saved figure
        """
        fig = plt.figure(id)
        ax1 = fig.add_subplot(111)
        ax1.imshow((self.image), interpolation='nearest', extent=[
         self.xmin, self.xmax, self.ymin, self.ymax],
          origin='lower')
        ax1.imshow((self.wall_distance), interpolation='nearest', extent=[
         self.xmin, self.xmax, self.ymin, self.ymax],
          alpha=0.7,
          origin='lower')
        ax1.quiver((self.X[::step, ::step]), (self.Y[::step, ::step]), (self.wall_grad_X[::step, ::step]),
          (self.wall_grad_Y[::step, ::step]),
          scale=scale,
          scale_units=scale_units)
        ax1.set_axis_off()
        ax1.set_title(title)
        plt.draw()
        if savefig:
            fig.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0)

    def plot_desired_velocity(self, destination_name, step=10, scale=10, scale_units='inches', id=1, title='', savefig=False, filename='fig.png', dpi=150):
        """To plot the desired velocity

        Parameters
        ----------
        destination_name: string
            name of the considered destination
        step: integer
            draw an arrow every step pixels
        scale: integer
            scaling for the quiver arrows
        scale_units: string
            unit name for quiver arrow scaling
        id: integer
            Figure id (number)
        title: string
            Figure title
        savefig: boolean
            writes the figure as a png file if true
        filename: string
            png filename used to write the figure
        dpi: integer
            number of pixel per inch for the saved figure
        """
        fig = plt.figure(id)
        ax1 = fig.add_subplot(111)
        ax1.imshow((self.image), interpolation='nearest', extent=[
         self.xmin, self.xmax, self.ymin, self.ymax],
          origin='lower')
        ax1.imshow((self.destinations[destination_name].distance), interpolation='nearest', extent=[
         self.xmin, self.xmax, self.ymin, self.ymax],
          alpha=0.7,
          origin='lower')
        ax1.quiver((self.X[::step, ::step]), (self.Y[::step, ::step]), (self.destinations[destination_name].desired_velocity_X[::step, ::step]),
          (self.destinations[destination_name].desired_velocity_Y[::step, ::step]),
          scale=scale,
          scale_units=scale_units)
        ax1.set_title(title)
        ax1.set_axis_off()
        plt.draw()
        if savefig:
            fig.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0)

    def __str__(self):
        """To print the main caracteristics of a Domain object
        """
        return '--> ' + self.name + ':\n    dimensions: [' + str(self.xmin) + ',' + str(self.xmax) + ']x[' + str(self.ymin) + ',' + str(self.ymax) + ']' + '\n    width: ' + str(self.width) + ' height: ' + str(self.height) + '\n    background image: ' + str(self._Domain__background) + '\n    image of the domain: ' + str(self._Domain__image_filename) + '\n    wall_colors: ' + str(self.wall_colors) + '\n    destinations: ' + str(self.destinations)