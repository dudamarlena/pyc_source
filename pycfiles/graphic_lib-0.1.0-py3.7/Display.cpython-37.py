# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\graphic_lib\Display\Display.py
# Compiled at: 2020-03-15 07:29:07
# Size of source mod 2**32: 4794 bytes
from dataclasses import dataclass

@dataclass
class Color:
    red: int
    green: int
    blue: int

    def __mul__(self, brightness_coeficient):
        return Color(int(self.red * brightness_coeficient), int(self.green * brightness_coeficient), int(self.blue * brightness_coeficient))

    def __str__(self):
        return f"{self.red} {self.green} {self.blue}"


class FIRST_PIXEL_POSITION:
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4

    @classmethod
    def is_top_begin(cls, first_pixel_position):
        return first_pixel_position == cls.TOP_LEFT or first_pixel_position == cls.TOP_RIGHT

    @classmethod
    def is_left_begin(cls, first_pixel_position):
        return first_pixel_position == cls.TOP_LEFT or first_pixel_position == cls.BOTTOM_LEFT


class Display:

    def __init__(self, lines_lengths, first_pixel_position, views, model, framebuffer):
        self.first_pixel_position = first_pixel_position
        self.lines_lengths = lines_lengths
        self.frame_buffer = framebuffer(sum(lines_lengths))
        self.brightness = 255
        self.views = {}
        self.model = model
        for view in views.items():
            self.views[view[0]] = view[1](lines_lengths, model)

        self.current_view = list(self.views.keys())[0]

    def set_brightness(self, brightness):
        self.brightness = brightness

    def redraw(self):
        self.frame_buffer.clear()
        self.views[self.current_view].set_up()
        self.views[self.current_view].redraw()
        for y in range(5):
            for x in range(self.lines_lengths[y]):
                if y < self.views[self.current_view].height:
                    if x < self.lines_lengths[y]:
                        if self.views[self.current_view].framebuffer[y][x].red == 0:
                            if self.views[self.current_view].framebuffer[y][x].blue == 0:
                                if self.views[self.current_view].framebuffer[y][x].green == 0:
                                    continue
                    self(x, y).set_color(self.views[self.current_view].framebuffer[y][x])

        self.frame_buffer.show()

    def update(self):
        if self.model.Mode != self.current_view:
            self.current_view = self.model.Mode
            self.views[self.current_view].set_up()
        self.frame_buffer.clear()
        self.views[self.current_view].update()
        self.views[self.current_view].redraw()
        for y in range(5):
            for x in range(self.lines_lengths[y]):
                if y < self.views[self.current_view].height and x < self.lines_lengths[y]:
                    if not self.model.auto_brightness:
                        self(x, y).set_color(self.views[self.current_view].framebuffer[y][x] * self.model.Display_brightness)
                    else:
                        self(x, y).set_color(self.views[self.current_view].framebuffer[y][x] * self.model.brightness_coeficient)

        self.frame_buffer.show()

    def __call__--- This code section failed: ---

 L.  88         0  LOAD_FAST                'self'
                2  LOAD_METHOD              number_of_preceding_lines_pixels
                4  LOAD_FAST                'y'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'index'

 L.  90        10  LOAD_FAST                'self'
               12  LOAD_ATTR                first_pixel_position
               14  LOAD_GLOBAL              FIRST_PIXEL_POSITION
               16  LOAD_ATTR                TOP_LEFT
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    70  'to 70'

 L.  91        22  LOAD_FAST                'y'
               24  LOAD_CONST               2
               26  BINARY_MODULO    
               28  LOAD_CONST               0
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    44  'to 44'

 L.  92        34  LOAD_FAST                'index'
               36  LOAD_FAST                'x'
               38  INPLACE_ADD      
               40  STORE_FAST               'index'
               42  JUMP_FORWARD        378  'to 378'
             44_0  COME_FROM            32  '32'

 L.  94        44  LOAD_FAST                'index'
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                lines_lengths
               50  LOAD_FAST                'y'
               52  BINARY_SUBSCR    
               54  LOAD_CONST               1
               56  BINARY_SUBTRACT  
               58  LOAD_FAST                'x'
               60  BINARY_SUBTRACT  
               62  INPLACE_ADD      
               64  STORE_FAST               'index'
            66_68  JUMP_FORWARD        378  'to 378'
             70_0  COME_FROM            20  '20'

 L.  96        70  LOAD_FAST                'self'
               72  LOAD_ATTR                first_pixel_position
               74  LOAD_GLOBAL              FIRST_PIXEL_POSITION
               76  LOAD_ATTR                TOP_RIGHT
               78  COMPARE_OP               ==
               80  POP_JUMP_IF_FALSE   128  'to 128'

 L.  97        82  LOAD_FAST                'y'
               84  LOAD_CONST               2
               86  BINARY_MODULO    
               88  LOAD_CONST               0
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE   118  'to 118'

 L.  98        94  LOAD_FAST                'index'
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                lines_lengths
              100  LOAD_FAST                'y'
              102  BINARY_SUBSCR    
              104  LOAD_CONST               1
              106  BINARY_SUBTRACT  
              108  LOAD_FAST                'x'
              110  BINARY_SUBTRACT  
              112  INPLACE_ADD      
              114  STORE_FAST               'index'
              116  JUMP_FORWARD        126  'to 126'
            118_0  COME_FROM            92  '92'

 L. 100       118  LOAD_FAST                'index'
              120  LOAD_FAST                'x'
              122  INPLACE_ADD      
              124  STORE_FAST               'index'
            126_0  COME_FROM           116  '116'
              126  JUMP_FORWARD        378  'to 378'
            128_0  COME_FROM            80  '80'

 L. 102       128  LOAD_FAST                'self'
              130  LOAD_ATTR                first_pixel_position
              132  LOAD_GLOBAL              FIRST_PIXEL_POSITION
              134  LOAD_ATTR                BOTTOM_LEFT
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   250  'to 250'

 L. 103       140  LOAD_GLOBAL              len
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                lines_lengths
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  LOAD_CONST               2
              150  BINARY_MODULO    
              152  LOAD_CONST               0
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   204  'to 204'

 L. 104       158  LOAD_FAST                'y'
              160  LOAD_CONST               2
              162  BINARY_MODULO    
              164  LOAD_CONST               0
              166  COMPARE_OP               ==
              168  POP_JUMP_IF_FALSE   194  'to 194'

 L. 105       170  LOAD_FAST                'index'
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                lines_lengths
              176  LOAD_FAST                'y'
              178  BINARY_SUBSCR    
              180  LOAD_CONST               1
              182  BINARY_SUBTRACT  
              184  LOAD_FAST                'x'
              186  BINARY_SUBTRACT  
              188  INPLACE_ADD      
              190  STORE_FAST               'index'
              192  JUMP_ABSOLUTE       248  'to 248'
            194_0  COME_FROM           168  '168'

 L. 107       194  LOAD_FAST                'index'
              196  LOAD_FAST                'x'
              198  INPLACE_ADD      
              200  STORE_FAST               'index'
              202  JUMP_FORWARD        248  'to 248'
            204_0  COME_FROM           156  '156'

 L. 109       204  LOAD_FAST                'y'
              206  LOAD_CONST               2
              208  BINARY_MODULO    
              210  LOAD_CONST               0
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   226  'to 226'

 L. 110       216  LOAD_FAST                'index'
              218  LOAD_FAST                'x'
              220  INPLACE_ADD      
              222  STORE_FAST               'index'
              224  JUMP_FORWARD        248  'to 248'
            226_0  COME_FROM           214  '214'

 L. 112       226  LOAD_FAST                'index'
              228  LOAD_FAST                'self'
              230  LOAD_ATTR                lines_lengths
              232  LOAD_FAST                'y'
              234  BINARY_SUBSCR    
              236  LOAD_CONST               1
              238  BINARY_SUBTRACT  
              240  LOAD_FAST                'x'
              242  BINARY_SUBTRACT  
              244  INPLACE_ADD      
              246  STORE_FAST               'index'
            248_0  COME_FROM           224  '224'
            248_1  COME_FROM           202  '202'
              248  JUMP_FORWARD        378  'to 378'
            250_0  COME_FROM           138  '138'

 L. 114       250  LOAD_FAST                'self'
              252  LOAD_ATTR                first_pixel_position
              254  LOAD_GLOBAL              FIRST_PIXEL_POSITION
              256  LOAD_ATTR                BOTTOM_RIGHT
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   378  'to 378'

 L. 115       264  LOAD_GLOBAL              len
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                lines_lengths
              270  CALL_FUNCTION_1       1  '1 positional argument'
              272  LOAD_CONST               2
              274  BINARY_MODULO    
              276  LOAD_CONST               0
              278  COMPARE_OP               ==
          280_282  POP_JUMP_IF_FALSE   332  'to 332'

 L. 116       284  LOAD_FAST                'y'
              286  LOAD_CONST               2
              288  BINARY_MODULO    
              290  LOAD_CONST               0
              292  COMPARE_OP               ==
          294_296  POP_JUMP_IF_FALSE   308  'to 308'

 L. 117       298  LOAD_FAST                'index'
              300  LOAD_FAST                'x'
              302  INPLACE_ADD      
              304  STORE_FAST               'index'
              306  JUMP_FORWARD        330  'to 330'
            308_0  COME_FROM           294  '294'

 L. 119       308  LOAD_FAST                'index'
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                lines_lengths
              314  LOAD_FAST                'y'
              316  BINARY_SUBSCR    
              318  LOAD_CONST               1
              320  BINARY_SUBTRACT  
              322  LOAD_FAST                'x'
              324  BINARY_SUBTRACT  
              326  INPLACE_ADD      
              328  STORE_FAST               'index'
            330_0  COME_FROM           306  '306'
              330  JUMP_FORWARD        378  'to 378'
            332_0  COME_FROM           280  '280'

 L. 121       332  LOAD_FAST                'y'
              334  LOAD_CONST               2
              336  BINARY_MODULO    
              338  LOAD_CONST               0
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   370  'to 370'

 L. 122       346  LOAD_FAST                'index'
              348  LOAD_FAST                'self'
              350  LOAD_ATTR                lines_lengths
            352_0  COME_FROM            42  '42'
              352  LOAD_FAST                'y'
              354  BINARY_SUBSCR    
              356  LOAD_CONST               1
              358  BINARY_SUBTRACT  
              360  LOAD_FAST                'x'
              362  BINARY_SUBTRACT  
              364  INPLACE_ADD      
              366  STORE_FAST               'index'
              368  JUMP_FORWARD        378  'to 378'
            370_0  COME_FROM           342  '342'

 L. 124       370  LOAD_FAST                'index'
              372  LOAD_FAST                'x'
              374  INPLACE_ADD      
              376  STORE_FAST               'index'
            378_0  COME_FROM           368  '368'
            378_1  COME_FROM           330  '330'
            378_2  COME_FROM           260  '260'
            378_3  COME_FROM           248  '248'
            378_4  COME_FROM           126  '126'
            378_5  COME_FROM            66  '66'

 L. 126       378  LOAD_FAST                'self'
              380  LOAD_ATTR                frame_buffer
              382  LOAD_FAST                'index'
              384  BINARY_SUBSCR    
              386  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 352_0

    def number_of_preceding_lines_pixels(self, y):
        if FIRST_PIXEL_POSITION.is_top_begin(self.first_pixel_position):
            step = 1
            start = 0
        else:
            step = -1
            start = len(self.lines_lengths) - 1
        return sum([self.lines_lengths[i] for i in range(start, y, step)])