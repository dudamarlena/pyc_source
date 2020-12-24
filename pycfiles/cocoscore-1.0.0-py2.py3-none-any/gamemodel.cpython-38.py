# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\samples\tetrico\gamemodel.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 10694 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
import copy, random, weakref, pyglet
from cocos.euclid import Point2
from constants import *
from status import status
from colors import *
import levels
__all__ = [
 'GameModel']

class GameModel(pyglet.event.EventDispatcher):

    def __init__(self):
        super(GameModel, self).__init__()
        self.init()
        self.block = None
        self.map = {}
        status.reset()
        status.level = levels.levels[0]

    def start(self):
        self.set_next_level()

    def set_controller(self, ctrl):
        self.ctrl = weakref.ref(ctrl)

    def init_map(self):
        """creates a map"""
        self.map = {}
        for i in range(COLUMNS):
            for j in range(ROWS):
                self.map[(i, j)] = 0

    def check_line--- This code section failed: ---

 L.  65         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lines'

 L.  66         4  LOAD_GLOBAL              range
                6  LOAD_GLOBAL              ROWS
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
               12  FOR_ITER             78  'to 78'
               14  STORE_FAST               'j'

 L.  67        16  LOAD_GLOBAL              range
               18  LOAD_GLOBAL              COLUMNS
               20  CALL_FUNCTION_1       1  ''
               22  GET_ITER         
             24_0  COME_FROM            62  '62'
               24  FOR_ITER             76  'to 76'
               26  STORE_FAST               'i'

 L.  68        28  LOAD_FAST                'self'
               30  LOAD_ATTR                map
               32  LOAD_METHOD              get
               34  LOAD_FAST                'i'
               36  LOAD_FAST                'j'
               38  BUILD_TUPLE_2         2 
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'c'

 L.  69        44  LOAD_FAST                'c'
               46  POP_JUMP_IF_TRUE     52  'to 52'

 L.  70        48  POP_TOP          
               50  JUMP_BACK            12  'to 12'
             52_0  COME_FROM            46  '46'

 L.  71        52  LOAD_FAST                'i'
               54  LOAD_GLOBAL              COLUMNS
               56  LOAD_CONST               1
               58  BINARY_SUBTRACT  
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    24  'to 24'

 L.  72        64  LOAD_FAST                'lines'
               66  LOAD_METHOD              append
               68  LOAD_FAST                'j'
               70  CALL_METHOD_1         1  ''
               72  POP_TOP          
               74  JUMP_BACK            24  'to 24'
               76  JUMP_BACK            12  'to 12'

 L.  74        78  LOAD_FAST                'lines'
               80  LOAD_METHOD              reverse
               82  CALL_METHOD_0         0  ''
               84  POP_TOP          

 L.  76        86  BUILD_LIST_0          0 
               88  STORE_FAST               'effects'

 L.  77        90  LOAD_FAST                'lines'
               92  GET_ITER         
               94  FOR_ITER            148  'to 148'
               96  STORE_FAST               'j'

 L.  78        98  LOAD_GLOBAL              range
              100  LOAD_GLOBAL              COLUMNS
              102  CALL_FUNCTION_1       1  ''
              104  GET_ITER         
            106_0  COME_FROM           132  '132'
              106  FOR_ITER            146  'to 146'
              108  STORE_FAST               'i'

 L.  79       110  LOAD_FAST                'self'
              112  LOAD_ATTR                map
              114  LOAD_FAST                'i'
              116  LOAD_FAST                'j'
              118  BUILD_TUPLE_2         2 
              120  BINARY_SUBSCR    
              122  STORE_FAST               'e'

 L.  80       124  LOAD_FAST                'e'
              126  LOAD_GLOBAL              Colors
              128  LOAD_ATTR                specials
              130  COMPARE_OP               in
              132  POP_JUMP_IF_FALSE   106  'to 106'

 L.  81       134  LOAD_FAST                'effects'
              136  LOAD_METHOD              append
              138  LOAD_FAST                'e'
              140  CALL_METHOD_1         1  ''
              142  POP_TOP          
              144  JUMP_BACK           106  'to 106'
              146  JUMP_BACK            94  'to 94'

 L.  83       148  LOAD_FAST                'effects'
              150  POP_JUMP_IF_FALSE   162  'to 162'

 L.  84       152  LOAD_FAST                'self'
              154  LOAD_METHOD              process_effects
              156  LOAD_FAST                'effects'
              158  CALL_METHOD_1         1  ''
              160  POP_TOP          
            162_0  COME_FROM           150  '150'

 L.  86       162  LOAD_FAST                'lines'
              164  GET_ITER         
              166  FOR_ITER            234  'to 234'
              168  STORE_FAST               'l'

 L.  87       170  LOAD_GLOBAL              range
              172  LOAD_FAST                'l'
              174  LOAD_GLOBAL              ROWS
              176  LOAD_CONST               1
              178  BINARY_SUBTRACT  
              180  CALL_FUNCTION_2       2  ''
              182  GET_ITER         
              184  FOR_ITER            232  'to 232'
              186  STORE_FAST               'j'

 L.  88       188  LOAD_GLOBAL              range
              190  LOAD_GLOBAL              COLUMNS
              192  CALL_FUNCTION_1       1  ''
              194  GET_ITER         
              196  FOR_ITER            230  'to 230'
              198  STORE_FAST               'i'

 L.  89       200  LOAD_FAST                'self'
              202  LOAD_ATTR                map
              204  LOAD_FAST                'i'
              206  LOAD_FAST                'j'
              208  LOAD_CONST               1
              210  BINARY_ADD       
              212  BUILD_TUPLE_2         2 
              214  BINARY_SUBSCR    
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                map
              220  LOAD_FAST                'i'
              222  LOAD_FAST                'j'
              224  BUILD_TUPLE_2         2 
              226  STORE_SUBSCR     
              228  JUMP_BACK           196  'to 196'
              230  JUMP_BACK           184  'to 184'
              232  JUMP_BACK           166  'to 166'

 L.  91       234  LOAD_FAST                'lines'
          236_238  POP_JUMP_IF_FALSE   370  'to 370'

 L.  92       240  LOAD_GLOBAL              status
              242  DUP_TOP          
              244  LOAD_ATTR                score
              246  LOAD_GLOBAL              pow
              248  LOAD_CONST               2
              250  LOAD_GLOBAL              len
              252  LOAD_FAST                'lines'
              254  CALL_FUNCTION_1       1  ''
              256  CALL_FUNCTION_2       2  ''
              258  LOAD_CONST               1
              260  BINARY_SUBTRACT  
              262  INPLACE_ADD      
              264  ROT_TWO          
              266  STORE_ATTR               score

 L.  93       268  LOAD_GLOBAL              status
              270  DUP_TOP          
              272  LOAD_ATTR                lines
              274  LOAD_GLOBAL              len
              276  LOAD_FAST                'lines'
              278  CALL_FUNCTION_1       1  ''
              280  INPLACE_ADD      
              282  ROT_TWO          
              284  STORE_ATTR               lines

 L.  94       286  LOAD_FAST                'self'
              288  LOAD_METHOD              dispatch_event
              290  LOAD_STR                 'on_line_complete'
              292  LOAD_FAST                'lines'
              294  CALL_METHOD_2         2  ''
              296  POP_TOP          

 L.  96       298  LOAD_GLOBAL              status
              300  LOAD_ATTR                lines
              302  LOAD_GLOBAL              status
              304  LOAD_ATTR                level
              306  LOAD_ATTR                lines
              308  COMPARE_OP               >=
          310_312  POP_JUMP_IF_FALSE   370  'to 370'

 L.  97       314  LOAD_FAST                'self'
              316  LOAD_METHOD              ctrl
              318  CALL_METHOD_0         0  ''
              320  LOAD_METHOD              pause_controller
              322  CALL_METHOD_0         0  ''
              324  POP_TOP          

 L.  98       326  LOAD_GLOBAL              status
              328  LOAD_ATTR                level_idx
              330  LOAD_CONST               1
              332  BINARY_ADD       
              334  LOAD_GLOBAL              len
              336  LOAD_GLOBAL              levels
              338  LOAD_ATTR                levels
              340  CALL_FUNCTION_1       1  ''
              342  COMPARE_OP               >=
          344_346  POP_JUMP_IF_FALSE   360  'to 360'

 L.  99       348  LOAD_FAST                'self'
              350  LOAD_METHOD              dispatch_event
              352  LOAD_STR                 'on_win'
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          
              358  JUMP_FORWARD        370  'to 370'
            360_0  COME_FROM           344  '344'

 L. 101       360  LOAD_FAST                'self'
              362  LOAD_METHOD              dispatch_event
              364  LOAD_STR                 'on_level_complete'
              366  CALL_METHOD_1         1  ''
              368  POP_TOP          
            370_0  COME_FROM           358  '358'
            370_1  COME_FROM           310  '310'
            370_2  COME_FROM           236  '236'

Parse error at or near `LOAD_FAST' instruction at offset 78

    def init(self):
        status.lines = 0
        self.init_map()

    def set_next_level(self):
        self.ctrl().resume_controller()
        if status.level_idx is None:
            status.level_idx = 0
        else:
            status.level_idx += 1
        l = levels.levels[status.level_idx]
        self.init()
        status.level = l()
        self.random_block()
        self.random_block()
        self.dispatch_event('on_new_level')

    def process_effects(self, effects):
        d = {}
        elements = set(effects)
        for e in elements:
            d[e] = effects.count(e)

        self.dispatch_event('on_special_effect', d)

    def merge_block(self):
        """merges a block in the map"""
        for i in range(self.block.x):
            for j in range(self.block.x):
                c = self.block.get(i, j)
                if c:
                    self.map[(i + self.block.pos.x, j + self.block.pos.y)] = c

    def are_valid_movements--- This code section failed: ---

 L. 146         0  LOAD_GLOBAL              range
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                block
                6  LOAD_ATTR                x
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
               12  FOR_ITER            126  'to 126'
               14  STORE_FAST               'i'

 L. 147        16  LOAD_GLOBAL              range
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                block
               22  LOAD_ATTR                x
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM           112  '112'
             28_1  COME_FROM            44  '44'
               28  FOR_ITER            124  'to 124'
               30  STORE_FAST               'j'

 L. 148        32  LOAD_FAST                'self'
               34  LOAD_ATTR                block
               36  LOAD_METHOD              get
               38  LOAD_FAST                'i'
               40  LOAD_FAST                'j'
               42  CALL_METHOD_2         2  ''
               44  POP_JUMP_IF_FALSE    28  'to 28'

 L. 149        46  LOAD_FAST                'j'
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                block
               52  LOAD_ATTR                pos
               54  LOAD_ATTR                y
               56  BINARY_ADD       
               58  LOAD_CONST               0
               60  COMPARE_OP               ==
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 150        64  POP_TOP          
               66  POP_TOP          
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            62  '62'

 L. 151        72  LOAD_FAST                'self'
               74  LOAD_ATTR                map
               76  LOAD_METHOD              get
               78  LOAD_FAST                'i'
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                block
               84  LOAD_ATTR                pos
               86  LOAD_ATTR                x
               88  BINARY_ADD       
               90  LOAD_FAST                'j'
               92  LOAD_FAST                'self'
               94  LOAD_ATTR                block
               96  LOAD_ATTR                pos
               98  LOAD_ATTR                y
              100  BINARY_ADD       
              102  LOAD_CONST               1
              104  BINARY_SUBTRACT  
              106  BUILD_TUPLE_2         2 
              108  LOAD_CONST               False
              110  CALL_METHOD_2         2  ''
              112  POP_JUMP_IF_FALSE    28  'to 28'

 L. 152       114  POP_TOP          
              116  POP_TOP          
              118  LOAD_CONST               False
              120  RETURN_VALUE     
              122  JUMP_BACK            28  'to 28'
              124  JUMP_BACK            12  'to 12'

 L. 153       126  LOAD_CONST               True
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 68

    def block_right(self):
        """moves right the block 1 square"""
        self.block.backup()
        self.block.pos.x += 1
        if not self.is_valid_block():
            self.block.restore()
        else:
            self.dispatch_event('on_move_block')

    def block_left(self):
        """moves left the block 1 square"""
        self.block.backup()
        self.block.pos.x -= 1
        if not self.is_valid_block():
            self.block.restore()
        else:
            self.dispatch_event('on_move_block')

    def block_down(self, sound=True):
        """moves down the block 1 square"""
        self.block.backup()
        self.block.pos.y -= 1
        if not self.is_valid_block():
            self.block.restore()
            self.next_block()
        elif sound:
            self.dispatch_event('on_move_block')

    def block_drop(self):
        """drops the block"""
        while True:
            self.block.backup()
            self.block.pos.y -= 1
            if not self.is_valid_block():
                self.block.restore()
                break

        self.dispatch_event('on_drop_block')

    def block_rotate(self):
        """rotates the block"""
        self.block.backup()
        self.block.rotate()
        if not self.is_valid_block():
            self.block.restore()
        else:
            self.dispatch_event('on_move_block')

    def next_block(self):
        """merge current block in grid,
        check if there are lines completed,
        and choose a new random block"""
        self.merge_block()
        self.check_line()
        self.random_block()
        if not self.is_valid_block():
            self.ctrl().pause_controller()
            self.dispatch_event('on_game_over')

    def random_block(self):
        """puts the next block in stage"""
        self.block = status.next_piece
        block = random.choice((
         Block_L,
         Block_L2,
         Block_O,
         Block_I,
         Block_Z,
         Block_Z2,
         Block_A))
        status.next_piece = block()
        if not self.block:
            self.random_block()

    def is_valid_block--- This code section failed: ---

 L. 234         0  LOAD_GLOBAL              range
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                block
                6  LOAD_ATTR                x
                8  CALL_FUNCTION_1       1  ''
               10  GET_ITER         
               12  FOR_ITER            174  'to 174'
               14  STORE_FAST               'i'

 L. 235        16  LOAD_GLOBAL              range
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                block
               22  LOAD_ATTR                x
               24  CALL_FUNCTION_1       1  ''
               26  GET_ITER         
             28_0  COME_FROM           160  '160'
             28_1  COME_FROM            44  '44'
               28  FOR_ITER            172  'to 172'
               30  STORE_FAST               'j'

 L. 236        32  LOAD_FAST                'self'
               34  LOAD_ATTR                block
               36  LOAD_METHOD              get
               38  LOAD_FAST                'i'
               40  LOAD_FAST                'j'
               42  CALL_METHOD_2         2  ''
               44  POP_JUMP_IF_FALSE    28  'to 28'

 L. 237        46  LOAD_FAST                'self'
               48  LOAD_ATTR                block
               50  LOAD_ATTR                pos
               52  LOAD_ATTR                x
               54  LOAD_FAST                'i'
               56  BINARY_ADD       
               58  LOAD_CONST               0
               60  COMPARE_OP               <
               62  POP_JUMP_IF_FALSE    72  'to 72'

 L. 238        64  POP_TOP          
               66  POP_TOP          
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            62  '62'

 L. 239        72  LOAD_FAST                'self'
               74  LOAD_ATTR                block
               76  LOAD_ATTR                pos
               78  LOAD_ATTR                x
               80  LOAD_FAST                'i'
               82  BINARY_ADD       
               84  LOAD_GLOBAL              COLUMNS
               86  COMPARE_OP               >=
               88  POP_JUMP_IF_FALSE    98  'to 98'

 L. 240        90  POP_TOP          
               92  POP_TOP          
               94  LOAD_CONST               False
               96  RETURN_VALUE     
             98_0  COME_FROM            88  '88'

 L. 241        98  LOAD_FAST                'self'
              100  LOAD_ATTR                block
              102  LOAD_ATTR                pos
              104  LOAD_ATTR                y
              106  LOAD_FAST                'j'
              108  BINARY_ADD       
              110  LOAD_CONST               0
              112  COMPARE_OP               <
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L. 242       116  POP_TOP          
              118  POP_TOP          
              120  LOAD_CONST               False
              122  RETURN_VALUE     
            124_0  COME_FROM           114  '114'

 L. 243       124  LOAD_FAST                'self'
              126  LOAD_ATTR                map
              128  LOAD_METHOD              get
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                block
              134  LOAD_ATTR                pos
              136  LOAD_ATTR                x
              138  LOAD_FAST                'i'
              140  BINARY_ADD       
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                block
              146  LOAD_ATTR                pos
              148  LOAD_ATTR                y
              150  LOAD_FAST                'j'
              152  BINARY_ADD       
              154  BUILD_TUPLE_2         2 
              156  LOAD_CONST               False
              158  CALL_METHOD_2         2  ''
              160  POP_JUMP_IF_FALSE    28  'to 28'

 L. 244       162  POP_TOP          
              164  POP_TOP          
              166  LOAD_CONST               False
              168  RETURN_VALUE     
              170  JUMP_BACK            28  'to 28'
              172  JUMP_BACK            12  'to 12'

 L. 245       174  LOAD_CONST               True
              176  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 68


class Block(object):
    """Block"""

    def __init__(self):
        super(Block, self).__init__()
        self.pos = Point2(COLUMNS // 2 - 1, ROWS)
        self.rot = 0
        for x in range(len(self._shape)):
            for y in range(len(self._shape[x])):
                if self._shape[x][y]:
                    r = random.random()
                    if r < status.level.prob:
                        color = random.choice(status.level.blocks)
                    else:
                        color = self.color
                    self._shape[x][y] = color

    def draw(self):
        """draw the block"""
        for i in range(self.x):
            for j in range(self.x):
                c = self.get(i, j)
                if c:
                    Colors.images[c].blit((i + self.pos.x) * SQUARE_SIZE, (j + self.pos.y) * SQUARE_SIZE)

    def rotate(self):
        """rotate the block"""
        self.rot = (self.rot + 1) % self.mod

    def backup(self):
        """saves a copy of the block"""
        self.save_pos = copy.copy(self.pos)
        self.save_rot = self.rot

    def restore(self):
        """restore a copy of the block"""
        self.pos = self.save_pos
        self.rot = self.save_rot

    def get(self, x, y):
        """get position x,y of the block"""
        if self.rot == 0:
            i, j = x, y
        elif self.rot == 1:
            i, j = y, self.x - x - 1
        elif self.rot == 2:
            i, j = self.x - x - 1, self.x - y - 1
        elif self.rot == 3:
            i, j = self.x - y - 1, x
        return self._shape[i][j]


class Block_I(Block):
    x = 4
    mod = 2
    color = Colors.RED

    def __init__(self):
        self._shape = [
         [
          0, 1, 0, 0],
         [
          0, 1, 0, 0],
         [
          0, 1, 0, 0],
         [
          0, 1, 0, 0]]
        super(Block_I, self).__init__()


class Block_Z(Block):
    x = 3
    color = Colors.ORANGE
    mod = 2

    def __init__(self):
        self._shape = [
         [
          0, 0, 0],
         [
          1, 1, 0],
         [
          0, 1, 1]]
        super(Block_Z, self).__init__()


class Block_Z2(Block):
    x = 3
    color = Colors.CYAN
    mod = 2

    def __init__(self):
        self._shape = [
         [
          0, 0, 0],
         [
          0, 1, 1],
         [
          1, 1, 0]]
        super(Block_Z2, self).__init__()


class Block_O(Block):
    x = 2
    color = Colors.BLUE
    mod = 4

    def __init__(self):
        self._shape = [
         [
          1, 1],
         [
          1, 1]]
        super(Block_O, self).__init__()


class Block_L(Block):
    x = 3
    color = Colors.MAGENTA
    mod = 4

    def __init__(self):
        self._shape = [
         [
          1, 0, 0],
         [
          1, 0, 0],
         [
          1, 1, 0]]
        super(Block_L, self).__init__()


class Block_L2(Block):
    x = 3
    color = Colors.YELLOW
    mod = 4

    def __init__(self):
        self._shape = [
         [
          0, 0, 1],
         [
          0, 0, 1],
         [
          0, 1, 1]]
        super(Block_L2, self).__init__()


class Block_A(Block):
    x = 3
    color = Colors.GREEN
    mod = 4

    def __init__(self):
        self._shape = [
         [
          0, 0, 0],
         [
          0, 1, 0],
         [
          1, 1, 1]]
        super(Block_A, self).__init__()


GameModel.register_event_type('on_special_effect')
GameModel.register_event_type('on_line_complete')
GameModel.register_event_type('on_level_complete')
GameModel.register_event_type('on_new_level')
GameModel.register_event_type('on_game_over')
GameModel.register_event_type('on_move_block')
GameModel.register_event_type('on_drop_block')
GameModel.register_event_type('on_win')
# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L. 191        46  BREAK_LOOP           50  'to 50'