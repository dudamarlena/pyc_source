# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\texture.py
# Compiled at: 2020-04-19 09:46:22
# Size of source mod 2**32: 19721 bytes
"""
Code related to working with textures.
"""
import os, math, PIL.Image, PIL.ImageOps, PIL.ImageDraw
from typing import Optional
from typing import List
from arcadeplus import lerp
from arcadeplus import RectList
from arcadeplus import Color
from arcadeplus import calculate_points

def _lerp_color(start_color: Color, end_color: Color, u: float) -> Color:
    return (
     int(lerp(start_color[0], end_color[0], u)),
     int(lerp(start_color[1], end_color[1], u)),
     int(lerp(start_color[2], end_color[2], u)))


class Matrix3x3:

    def __init__(self):
        self.reset()

    def reset(self):
        self.v = [
         1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        return self

    def multiply(self, o: List[float]):
        self.v = [self.v[0] * o[0] + self.v[3] * o[1] + self.v[6] * o[2],
         self.v[1] * o[0] + self.v[4] * o[1] + self.v[7] * o[2],
         self.v[2] * o[0] + self.v[5] * o[1] + self.v[8] * o[2],
         self.v[0] * o[3] + self.v[3] * o[4] + self.v[6] * o[5],
         self.v[1] * o[3] + self.v[4] * o[4] + self.v[7] * o[5],
         self.v[2] * o[3] + self.v[5] * o[4] + self.v[8] * o[5],
         self.v[0] * o[6] + self.v[3] * o[7] + self.v[6] * o[8],
         self.v[1] * o[6] + self.v[4] * o[7] + self.v[7] * o[8],
         self.v[2] * o[6] + self.v[5] * o[7] + self.v[8] * o[8]]
        return self

    def scale(self, sx: float, sy: float):
        return self.multiply([1.0 / sx, 0.0, 0.0, 0.0, 1.0 / sy, 0.0, 0.0, 0.0, 1.0])

    def translate(self, tx: float, ty: float):
        return self.multiply([1.0, 0.0, 0.0, 0.0, 1.0, 0.0, -tx, ty, 1.0])

    def rotate(self, phi: float):
        s = math.sin(math.radians(phi))
        c = math.cos(math.radians(phi))
        return self.multiply([c, s, 0.0, -s, c, 0.0, 0.0, 0.0, 1.0])

    def shear(self, sx: float, sy: float):
        return self.multiply([1.0, sy, 0.0, sx, 1.0, 0.0, 0.0, 0.0, 1.0])


class Texture:
    __doc__ = '\n    Class that represents a texture.\n    Usually created by the :class:`load_texture` or :class:`load_textures` commands.\n\n    Attributes:\n        :name: Unique name of the texture. Used by load_textures for caching.\n               If you are manually creating a texture, you can just set this\n               to whatever.\n        :image: A :py:class:`PIL.Image.Image` object.\n        :width: Width of the texture in pixels.\n        :height: Height of the texture in pixels.\n    '

    def __init__(self, name: str, image: PIL.Image.Image=None):
        from arcadeplus.sprite import Sprite
        from arcadeplus.sprite_list import SpriteList
        if image:
            assert isinstance(image, PIL.Image.Image)
        self.name = name
        self.image = image
        self._sprite = None
        self._sprite_list = None
        self.hit_box_points = None

    @property
    def width(self) -> int:
        """
        Width of the texture in pixels.
        """
        if self.image:
            return self.image.width
        return 0

    @property
    def height(self) -> int:
        """
        Height of the texture in pixels.
        """
        if self.image:
            return self.image.height
        return 0

    def _create_cached_sprite(self):
        from arcadeplus.sprite import Sprite
        from arcadeplus.sprite_list import SpriteList
        if self._sprite is None:
            self._sprite = Sprite()
            self._sprite.texture = self
            self._sprite.textures = [self]
            self._sprite_list = SpriteList()
            self._sprite_list.append(self._sprite)

    def draw_sized(self, center_x: float, center_y: float, width: float, height: float, angle: float=0, alpha: int=255):
        self._create_cached_sprite()
        if self._sprite:
            if self._sprite_list:
                self._sprite.center_x = center_x
                self._sprite.center_y = center_y
                self._sprite.height = height
                self._sprite.width = width
                self._sprite.angle = angle
                self._sprite.alpha = alpha
                self._sprite_list.draw()

    def draw_transformed(self, left: float, bottom: float, width: float, height: float, angle: float=0, alpha: int=255, texture_transform: Matrix3x3=Matrix3x3()):
        self._create_cached_sprite()
        if self._sprite:
            if self._sprite_list:
                self._sprite.center_x = left + width / 2
                self._sprite.center_y = bottom + height / 2
                self._sprite.width = width
                self._sprite.height = height
                self._sprite.angle = angle
                self._sprite.alpha = alpha
                self._sprite.texture_transform = texture_transform
                self._sprite_list.draw()

    def draw_scaled(self, center_x: float, center_y: float, scale: float=1.0, angle: float=0, alpha: int=255):
        """
        Draw the texture.

        :param float center_x: X location of where to draw the texture.
        :param float center_y: Y location of where to draw the texture.
        :param float scale: Scale to draw rectangle. Defaults to 1.
        :param float angle: Angle to rotate the texture by.
        :param int alpha: The transparency of the texture `(0-255)`.
        """
        self._create_cached_sprite()
        if self._sprite:
            if self._sprite_list:
                self._sprite.center_x = center_x
                self._sprite.center_y = center_y
                self._sprite.scale = scale
                self._sprite.angle = angle
                self._sprite.alpha = alpha
                self._sprite_list.draw()


def load_textures(file_name: str, image_location_list: RectList, mirrored: bool=False, flipped: bool=False) -> List[Texture]:
    """
    Load a set of textures from a single image file.

    :param str file_name: Name of the file.
    :param List image_location_list: List of image sub-locations. Each rectangle should be
           a `List` of four floats: `[x, y, width, height]`.
    :param bool mirrored: If set to `True`, the image is mirrored left to right.
    :param bool flipped: If set to `True`, the image is flipped upside down.

    :returns: List of :class:`Texture`'s.

    :raises: ValueError
    """
    cache_file_name = '{}'.format(file_name)
    if cache_file_name in load_texture.texture_cache:
        texture = load_texture.texture_cache[cache_file_name]
        source_image = texture.image
    else:
        if isinstance(file_name, str):
            if str(file_name).startswith(':resources:'):
                import os
                path = os.path.dirname(os.path.abspath(__file__))
                file_name = f"{path}/resources/{file_name[11:]}"
        source_image = PIL.Image.open(file_name)
        result = Texture(cache_file_name, source_image)
        load_texture.texture_cache[cache_file_name] = result
    source_image_width, source_image_height = source_image.size
    texture_info_list = []
    for image_location in image_location_list:
        x, y, width, height = image_location
        if width <= 0:
            raise ValueError('Texture has a width of {}, must be > 0.'.format(width))
        if x > source_image_width:
            raise ValueError("Can't load texture starting at an x of {} when the image is only {} across.".format(x, source_image_width))
        if y > source_image_height:
            raise ValueError("Can't load texture starting at an y of {} when the image is only {} high.".format(y, source_image_height))
        if x + width > source_image_width:
            raise ValueError("Can't load texture ending at an x of {} when the image is only {} wide.".format(x + width, source_image_width))
        if y + height > source_image_height:
            raise ValueError("Can't load texture ending at an y of {} when the image is only {} high.".format(y + height, source_image_height))
        cache_name = '{}{}{}{}{}{}{}'.format(file_name, x, y, width, height, flipped, mirrored)
        if cache_name in load_texture.texture_cache:
            result = load_texture.texture_cache[cache_name]
        else:
            image = source_image.crop((x, y, x + width, y + height))
            if mirrored:
                image = PIL.ImageOps.mirror(image)
            if flipped:
                image = PIL.ImageOps.flip(image)
            result = Texture(cache_name, image)
            load_texture.texture_cache[cache_name] = result
        texture_info_list.append(result)

    return texture_info_list


def load_texture--- This code section failed: ---

 L. 287         0  LOAD_STR                 '{}{}{}{}{}{}{}'
                2  LOAD_METHOD              format
                4  LOAD_FAST                'file_name'
                6  LOAD_FAST                'x'
                8  LOAD_FAST                'y'
               10  LOAD_FAST                'width'
               12  LOAD_FAST                'height'
               14  LOAD_FAST                'flipped'
               16  LOAD_FAST                'mirrored'
               18  CALL_METHOD_7         7  '7 positional arguments'
               20  STORE_FAST               'cache_name'

 L. 288        22  LOAD_FAST                'can_cache'
               24  POP_JUMP_IF_FALSE    46  'to 46'
               26  LOAD_FAST                'cache_name'
               28  LOAD_GLOBAL              load_texture
               30  LOAD_ATTR                texture_cache
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    46  'to 46'

 L. 289        36  LOAD_GLOBAL              load_texture
               38  LOAD_ATTR                texture_cache
               40  LOAD_FAST                'cache_name'
               42  BINARY_SUBSCR    
               44  RETURN_VALUE     
             46_0  COME_FROM            34  '34'
             46_1  COME_FROM            24  '24'

 L. 292        46  LOAD_FAST                'file_name'
               48  FORMAT_VALUE          0  ''
               50  STORE_FAST               'cache_file_name'

 L. 293        52  LOAD_FAST                'cache_file_name'
               54  LOAD_GLOBAL              load_texture
               56  LOAD_ATTR                texture_cache
               58  COMPARE_OP               in
               60  POP_JUMP_IF_FALSE    80  'to 80'

 L. 294        62  LOAD_GLOBAL              load_texture
               64  LOAD_ATTR                texture_cache
               66  LOAD_FAST                'cache_file_name'
               68  BINARY_SUBSCR    
               70  STORE_FAST               'texture'

 L. 295        72  LOAD_FAST                'texture'
               74  LOAD_ATTR                image
               76  STORE_FAST               'source_image'
               78  JUMP_FORWARD        192  'to 192'
             80_0  COME_FROM            60  '60'

 L. 298        80  LOAD_GLOBAL              isinstance
               82  LOAD_FAST                'file_name'
               84  LOAD_GLOBAL              str
               86  CALL_FUNCTION_2       2  '2 positional arguments'
               88  POP_JUMP_IF_FALSE   154  'to 154'
               90  LOAD_GLOBAL              str
               92  LOAD_FAST                'file_name'
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_METHOD              startswith
               98  LOAD_STR                 ':resources:'
              100  CALL_METHOD_1         1  '1 positional argument'
              102  POP_JUMP_IF_FALSE   154  'to 154'

 L. 299       104  LOAD_CONST               0
              106  LOAD_CONST               None
              108  IMPORT_NAME              os
              110  STORE_FAST               'os'

 L. 300       112  LOAD_FAST                'os'
              114  LOAD_ATTR                path
              116  LOAD_METHOD              dirname
              118  LOAD_FAST                'os'
              120  LOAD_ATTR                path
              122  LOAD_METHOD              abspath
              124  LOAD_GLOBAL              __file__
              126  CALL_METHOD_1         1  '1 positional argument'
              128  CALL_METHOD_1         1  '1 positional argument'
              130  STORE_FAST               'path'

 L. 301       132  LOAD_FAST                'path'
              134  FORMAT_VALUE          0  ''
              136  LOAD_STR                 '/resources/'
              138  LOAD_FAST                'file_name'
              140  LOAD_CONST               11
              142  LOAD_CONST               None
              144  BUILD_SLICE_2         2 
              146  BINARY_SUBSCR    
              148  FORMAT_VALUE          0  ''
              150  BUILD_STRING_3        3 
              152  STORE_FAST               'file_name'
            154_0  COME_FROM           102  '102'
            154_1  COME_FROM            88  '88'

 L. 303       154  LOAD_GLOBAL              PIL
              156  LOAD_ATTR                Image
              158  LOAD_METHOD              open
              160  LOAD_FAST                'file_name'
              162  CALL_METHOD_1         1  '1 positional argument'
              164  LOAD_METHOD              convert
              166  LOAD_STR                 'RGBA'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  STORE_FAST               'source_image'

 L. 304       172  LOAD_GLOBAL              Texture
              174  LOAD_FAST                'cache_file_name'
              176  LOAD_FAST                'source_image'
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  STORE_FAST               'result'

 L. 305       182  LOAD_FAST                'result'
              184  LOAD_GLOBAL              load_texture
              186  LOAD_ATTR                texture_cache
              188  LOAD_FAST                'cache_file_name'
              190  STORE_SUBSCR     
            192_0  COME_FROM            78  '78'

 L. 307       192  LOAD_FAST                'source_image'
              194  LOAD_ATTR                size
              196  UNPACK_SEQUENCE_2     2 
              198  STORE_FAST               'source_image_width'
              200  STORE_FAST               'source_image_height'

 L. 309       202  LOAD_FAST                'x'
              204  LOAD_CONST               0
              206  COMPARE_OP               !=
              208  POP_JUMP_IF_TRUE    236  'to 236'
              210  LOAD_FAST                'y'
              212  LOAD_CONST               0
              214  COMPARE_OP               !=
              216  POP_JUMP_IF_TRUE    236  'to 236'
              218  LOAD_FAST                'width'
              220  LOAD_CONST               0
              222  COMPARE_OP               !=
              224  POP_JUMP_IF_TRUE    236  'to 236'
              226  LOAD_FAST                'height'
              228  LOAD_CONST               0
              230  COMPARE_OP               !=
          232_234  POP_JUMP_IF_FALSE   384  'to 384'
            236_0  COME_FROM           224  '224'
            236_1  COME_FROM           216  '216'
            236_2  COME_FROM           208  '208'

 L. 310       236  LOAD_FAST                'x'
              238  LOAD_FAST                'source_image_width'
              240  COMPARE_OP               >
          242_244  POP_JUMP_IF_FALSE   262  'to 262'

 L. 311       246  LOAD_GLOBAL              ValueError
              248  LOAD_STR                 "Can't load texture starting at an x of {} when the image is only {} across."
              250  LOAD_METHOD              format

 L. 313       252  LOAD_FAST                'x'
              254  LOAD_FAST                'source_image_width'
              256  CALL_METHOD_2         2  '2 positional arguments'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  RAISE_VARARGS_1       1  'exception instance'
            262_0  COME_FROM           242  '242'

 L. 314       262  LOAD_FAST                'y'
              264  LOAD_FAST                'source_image_height'
              266  COMPARE_OP               >
          268_270  POP_JUMP_IF_FALSE   288  'to 288'

 L. 315       272  LOAD_GLOBAL              ValueError
              274  LOAD_STR                 "Can't load texture starting at an y of {} when the image is only {} high."
              276  LOAD_METHOD              format

 L. 317       278  LOAD_FAST                'y'
              280  LOAD_FAST                'source_image_height'
              282  CALL_METHOD_2         2  '2 positional arguments'
              284  CALL_FUNCTION_1       1  '1 positional argument'
              286  RAISE_VARARGS_1       1  'exception instance'
            288_0  COME_FROM           268  '268'

 L. 318       288  LOAD_FAST                'x'
              290  LOAD_FAST                'width'
              292  BINARY_ADD       
              294  LOAD_FAST                'source_image_width'
              296  COMPARE_OP               >
          298_300  POP_JUMP_IF_FALSE   322  'to 322'

 L. 319       302  LOAD_GLOBAL              ValueError
              304  LOAD_STR                 "Can't load texture ending at an x of {} when the image is only {} wide."
              306  LOAD_METHOD              format

 L. 321       308  LOAD_FAST                'x'
              310  LOAD_FAST                'width'
              312  BINARY_ADD       
              314  LOAD_FAST                'source_image_width'
              316  CALL_METHOD_2         2  '2 positional arguments'
              318  CALL_FUNCTION_1       1  '1 positional argument'
              320  RAISE_VARARGS_1       1  'exception instance'
            322_0  COME_FROM           298  '298'

 L. 322       322  LOAD_FAST                'y'
              324  LOAD_FAST                'height'
              326  BINARY_ADD       
              328  LOAD_FAST                'source_image_height'
              330  COMPARE_OP               >
          332_334  POP_JUMP_IF_FALSE   356  'to 356'

 L. 323       336  LOAD_GLOBAL              ValueError
              338  LOAD_STR                 "Can't load texture ending at an y of {} when the image is only {} high."
              340  LOAD_METHOD              format

 L. 325       342  LOAD_FAST                'y'
              344  LOAD_FAST                'height'
              346  BINARY_ADD       
              348  LOAD_FAST                'source_image_height'
              350  CALL_METHOD_2         2  '2 positional arguments'
              352  CALL_FUNCTION_1       1  '1 positional argument'
              354  RAISE_VARARGS_1       1  'exception instance'
            356_0  COME_FROM           332  '332'

 L. 327       356  LOAD_FAST                'source_image'
              358  LOAD_METHOD              crop
              360  LOAD_FAST                'x'
              362  LOAD_FAST                'y'
              364  LOAD_FAST                'x'
              366  LOAD_FAST                'width'
              368  BINARY_ADD       
              370  LOAD_FAST                'y'
              372  LOAD_FAST                'height'
              374  BINARY_ADD       
              376  BUILD_TUPLE_4         4 
              378  CALL_METHOD_1         1  '1 positional argument'
              380  STORE_FAST               'image'
              382  JUMP_FORWARD        388  'to 388'
            384_0  COME_FROM           232  '232'

 L. 329       384  LOAD_FAST                'source_image'
              386  STORE_FAST               'image'
            388_0  COME_FROM           382  '382'

 L. 332       388  LOAD_FAST                'mirrored'
          390_392  POP_JUMP_IF_FALSE   406  'to 406'

 L. 333       394  LOAD_GLOBAL              PIL
              396  LOAD_ATTR                ImageOps
              398  LOAD_METHOD              mirror
              400  LOAD_FAST                'image'
              402  CALL_METHOD_1         1  '1 positional argument'
              404  STORE_FAST               'image'
            406_0  COME_FROM           390  '390'

 L. 335       406  LOAD_FAST                'flipped'
          408_410  POP_JUMP_IF_FALSE   424  'to 424'

 L. 336       412  LOAD_GLOBAL              PIL
              414  LOAD_ATTR                ImageOps
              416  LOAD_METHOD              flip
              418  LOAD_FAST                'image'
              420  CALL_METHOD_1         1  '1 positional argument'
              422  STORE_FAST               'image'
            424_0  COME_FROM           408  '408'

 L. 338       424  LOAD_GLOBAL              Texture
              426  LOAD_FAST                'cache_name'
              428  LOAD_FAST                'image'
              430  CALL_FUNCTION_2       2  '2 positional arguments'
              432  STORE_FAST               'result'

 L. 339       434  LOAD_FAST                'result'
              436  LOAD_GLOBAL              load_texture
              438  LOAD_ATTR                texture_cache
              440  LOAD_FAST                'cache_name'
              442  STORE_SUBSCR     

 L. 340       444  LOAD_GLOBAL              calculate_points
              446  LOAD_FAST                'image'
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  LOAD_FAST                'result'
              452  STORE_ATTR               hit_box_points

 L. 341       454  LOAD_FAST                'result'
              456  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 382


load_texture.texture_cache = dict()

def cleanup_texture_cache():
    """
    This cleans up the cache of textures. Useful when running unit tests so that
    the next test starts clean.
    """
    load_texture.texture_cache = dict()
    import gc
    gc.collect()


def load_spritesheet(file_name: str, sprite_width: int, sprite_height: int, columns: int, count: int) -> List[Texture]:
    """

    :param str file_name: Name of the file to that holds the texture.
    :param int sprite_width: X position of the crop area of the texture.
    :param int sprite_height: Y position of the crop area of the texture.
    :param int columns: Number of tiles wide the image is.
    :param int count: Number of tiles in the image.

    :returns List: List of :class:`Texture` objects.
    """
    texture_list = []
    if isinstance(file_name, str):
        if str(file_name).startswith(':resources:'):
            path = os.path.dirname(os.path.abspath(__file__))
            file_name = f"{path}/resources/{file_name[11:]}"
    source_image = PIL.Image.open(file_name).convert('RGBA')
    for sprite_no in range(count):
        row = sprite_no // columns
        column = sprite_no % columns
        start_x = sprite_width * column
        start_y = sprite_height * row
        image = source_image.crop((start_x, start_y, start_x + sprite_width, start_y + sprite_height))
        texture = Texture(f"{file_name}-{sprite_no}", image)
        texture_list.append(texture)

    return texture_list


def make_circle_texture(diameter: int, color: Color) -> Texture:
    """
    Return a Texture of a circle with the given diameter and color.

    :param int diameter: Diameter of the circle and dimensions of the square :class:`Texture` returned.
    :param Color color: Color of the circle.

    :returns: New :class:`Texture` object.
    """
    bg_color = (0, 0, 0, 0)
    img = PIL.Image.new('RGBA', (diameter, diameter), bg_color)
    draw = PIL.ImageDraw.Draw(img)
    draw.ellipse((0, 0, diameter - 1, diameter - 1), fill=color)
    name = '{}:{}:{}'.format('circle_texture', diameter, color)
    return Texture(name, img)


def make_soft_circle_texture(diameter: int, color: Color, center_alpha: int=255, outer_alpha: int=0) -> Texture:
    """
    Return a :class:`Texture` of a circle with the given diameter and color, fading out at its edges.

    :param int diameter: Diameter of the circle and dimensions of the square :class:`Texture` returned.
    :param Color color: Color of the circle.
    :param int center_alpha: Alpha value of the circle at its center.
    :param int outer_alpha: Alpha value of the circle at its edges.

    :returns: New :class:`Texture` object.
    """
    bg_color = (0, 0, 0, 0)
    img = PIL.Image.new('RGBA', (diameter, diameter), bg_color)
    draw = PIL.ImageDraw.Draw(img)
    max_radius = int(diameter // 2)
    center = max_radius
    for radius in range(max_radius, 0, -1):
        alpha = int(lerp(center_alpha, outer_alpha, radius / max_radius))
        clr = (color[0], color[1], color[2], alpha)
        draw.ellipse((center - radius, center - radius, center + radius - 1, center + radius - 1), fill=clr)

    name = '{}:{}:{}:{}:{}'.format('soft_circle_texture', diameter, color, center_alpha, outer_alpha)
    return Texture(name, img)


def make_soft_square_texture(size: int, color: Color, center_alpha: int=255, outer_alpha: int=0) -> Texture:
    """
    Return a :class:`Texture` of a square with the given diameter and color, fading out at its edges.

    :param int size: Diameter of the square and dimensions of the square Texture returned.
    :param Color color: Color of the square.
    :param int center_alpha: Alpha value of the square at its center.
    :param int outer_alpha: Alpha value of the square at its edges.

    :returns: New :class:`Texture` object.
    """
    bg_color = (0, 0, 0, 0)
    img = PIL.Image.new('RGBA', (size, size), bg_color)
    draw = PIL.ImageDraw.Draw(img)
    half_size = int(size // 2)
    for cur_size in range(0, half_size):
        alpha = int(lerp(outer_alpha, center_alpha, cur_size / half_size))
        clr = (color[0], color[1], color[2], alpha)
        draw.rectangle((cur_size, cur_size, size - cur_size, size - cur_size), clr, None)

    name = '{}:{}:{}:{}:{}'.format('gradientsquare', size, color, center_alpha, outer_alpha)
    return Texture(name, img)


def trim_image(image: PIL.Image.Image) -> PIL.Image.Image:
    """
    Crops the extra whitespace out of an image.

    :returns: New :py:class:`PIL.Image.Image` object.
    """
    bbox = image.getbbox()
    return image.crop(bbox)