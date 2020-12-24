# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\physics_engines.py
# Compiled at: 2020-04-07 19:56:23
# Size of source mod 2**32: 14118 bytes
__doc__ = '\nPhysics engines for top-down or platformers.\n'
from arcadeplus import check_for_collision_with_list
from arcadeplus import check_for_collision
from arcadeplus import Sprite
from arcadeplus import SpriteList

def _circular_check(player, walls):
    """
    This is a horrible kludge to 'guess' our way out of a collision
    Returns:

    """
    original_x = player.center_x
    original_y = player.center_y
    vary = 1
    while True:
        try_list = [
         [
          original_x, original_y + vary],
         [
          original_x, original_y - vary],
         [
          original_x + vary, original_y],
         [
          original_x - vary, original_y],
         [
          original_x + vary, original_y + vary],
         [
          original_x + vary, original_y - vary],
         [
          original_x - vary, original_y + vary],
         [
          original_x - vary, original_y - vary]]
        for my_item in try_list:
            x, y = my_item
            player.center_x = x
            player.center_y = y
            check_hit_list = check_for_collision_with_list(player, walls)
            if len(check_hit_list) == 0:
                return

        vary *= 2


def _move_sprite--- This code section failed: ---

 L.  46         0  LOAD_FAST                'moving_sprite'
                2  DUP_TOP          
                4  LOAD_ATTR                angle
                6  LOAD_FAST                'moving_sprite'
                8  LOAD_ATTR                change_angle
               10  INPLACE_ADD      
               12  ROT_TWO          
               14  STORE_ATTR               angle

 L.  48        16  LOAD_GLOBAL              check_for_collision_with_list
               18  LOAD_FAST                'moving_sprite'
               20  LOAD_FAST                'walls'
               22  CALL_FUNCTION_2       2  ''
               24  STORE_FAST               'hit_list'

 L.  50        26  LOAD_GLOBAL              len
               28  LOAD_FAST                'hit_list'
               30  CALL_FUNCTION_1       1  ''
               32  LOAD_CONST               0
               34  COMPARE_OP               >
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L.  52        38  LOAD_GLOBAL              _circular_check
               40  LOAD_FAST                'moving_sprite'
               42  LOAD_FAST                'walls'
               44  CALL_FUNCTION_2       2  ''
               46  POP_TOP          
             48_0  COME_FROM            36  '36'

 L.  55        48  LOAD_FAST                'moving_sprite'
               50  DUP_TOP          
               52  LOAD_ATTR                center_y
               54  LOAD_FAST                'moving_sprite'
               56  LOAD_ATTR                change_y
               58  INPLACE_ADD      
               60  ROT_TWO          
               62  STORE_ATTR               center_y

 L.  58        64  LOAD_GLOBAL              check_for_collision_with_list
               66  LOAD_FAST                'moving_sprite'
               68  LOAD_FAST                'walls'
               70  CALL_FUNCTION_2       2  ''
               72  STORE_FAST               'hit_list_x'

 L.  60        74  LOAD_FAST                'hit_list_x'
               76  STORE_FAST               'complete_hit_list'

 L.  63        78  LOAD_GLOBAL              len
               80  LOAD_FAST                'hit_list_x'
               82  CALL_FUNCTION_1       1  ''
               84  LOAD_CONST               0
               86  COMPARE_OP               >
               88  POP_JUMP_IF_FALSE   240  'to 240'

 L.  64        90  LOAD_FAST                'moving_sprite'
               92  LOAD_ATTR                change_y
               94  LOAD_CONST               0
               96  COMPARE_OP               >
               98  POP_JUMP_IF_FALSE   140  'to 140'

 L.  65       100  SETUP_LOOP          222  'to 222'
              102  LOAD_GLOBAL              len
              104  LOAD_GLOBAL              check_for_collision_with_list
              106  LOAD_FAST                'moving_sprite'
              108  LOAD_FAST                'walls'
              110  CALL_FUNCTION_2       2  ''
              112  CALL_FUNCTION_1       1  ''
              114  LOAD_CONST               0
              116  COMPARE_OP               >
              118  POP_JUMP_IF_FALSE   136  'to 136'

 L.  66       120  LOAD_FAST                'moving_sprite'
              122  DUP_TOP          
              124  LOAD_ATTR                center_y
              126  LOAD_CONST               1
              128  INPLACE_SUBTRACT 
              130  ROT_TWO          
              132  STORE_ATTR               center_y
              134  JUMP_BACK           102  'to 102'
            136_0  COME_FROM           118  '118'
              136  POP_BLOCK        
              138  JUMP_FORWARD        222  'to 222'
            140_0  COME_FROM            98  '98'

 L.  69       140  LOAD_FAST                'moving_sprite'
              142  LOAD_ATTR                change_y
              144  LOAD_CONST               0
              146  COMPARE_OP               <
              148  POP_JUMP_IF_FALSE   222  'to 222'

 L.  71       150  SETUP_LOOP          222  'to 222'
              152  LOAD_FAST                'hit_list_x'
              154  GET_ITER         
            156_0  COME_FROM           198  '198'
              156  FOR_ITER            218  'to 218'
              158  STORE_FAST               'item'

 L.  72       160  SETUP_LOOP          190  'to 190'
              162  LOAD_GLOBAL              check_for_collision
              164  LOAD_FAST                'moving_sprite'
              166  LOAD_FAST                'item'
              168  CALL_FUNCTION_2       2  ''
              170  POP_JUMP_IF_FALSE   188  'to 188'

 L.  74       172  LOAD_FAST                'moving_sprite'
              174  DUP_TOP          
              176  LOAD_ATTR                center_y
              178  LOAD_CONST               0.25
              180  INPLACE_ADD      
              182  ROT_TWO          
              184  STORE_ATTR               center_y
              186  JUMP_BACK           162  'to 162'
            188_0  COME_FROM           170  '170'
              188  POP_BLOCK        
            190_0  COME_FROM_LOOP      160  '160'

 L.  76       190  LOAD_FAST                'item'
              192  LOAD_ATTR                change_x
              194  LOAD_CONST               0
              196  COMPARE_OP               !=
              198  POP_JUMP_IF_FALSE   156  'to 156'

 L.  77       200  LOAD_FAST                'moving_sprite'
              202  DUP_TOP          
              204  LOAD_ATTR                center_x
              206  LOAD_FAST                'item'
              208  LOAD_ATTR                change_x
              210  INPLACE_ADD      
              212  ROT_TWO          
              214  STORE_ATTR               center_x
              216  JUMP_BACK           156  'to 156'
              218  POP_BLOCK        
              220  JUMP_FORWARD        222  'to 222'
            222_0  COME_FROM           220  '220'
            222_1  COME_FROM_LOOP      150  '150'
            222_2  COME_FROM           148  '148'
            222_3  COME_FROM           138  '138'
            222_4  COME_FROM_LOOP      100  '100'

 L.  90       222  LOAD_GLOBAL              min
              224  LOAD_CONST               0.0
              226  LOAD_FAST                'hit_list_x'
              228  LOAD_CONST               0
              230  BINARY_SUBSCR    
              232  LOAD_ATTR                change_y
              234  CALL_FUNCTION_2       2  ''
              236  LOAD_FAST                'moving_sprite'
              238  STORE_ATTR               change_y
            240_0  COME_FROM            88  '88'

 L.  93       240  LOAD_GLOBAL              round
              242  LOAD_FAST                'moving_sprite'
              244  LOAD_ATTR                center_y
              246  LOAD_CONST               2
              248  CALL_FUNCTION_2       2  ''
              250  LOAD_FAST                'moving_sprite'
              252  STORE_ATTR               center_y

 L.  97       254  LOAD_FAST                'moving_sprite'
              256  DUP_TOP          
              258  LOAD_ATTR                center_x
              260  LOAD_FAST                'moving_sprite'
              262  LOAD_ATTR                change_x
              264  INPLACE_ADD      
              266  ROT_TWO          
              268  STORE_ATTR               center_x

 L.  99       270  LOAD_CONST               True
              272  STORE_FAST               'check_again'

 L. 100   274_276  SETUP_LOOP          666  'to 666'
            278_0  COME_FROM           348  '348'
              278  LOAD_FAST                'check_again'
          280_282  POP_JUMP_IF_FALSE   664  'to 664'

 L. 101       284  LOAD_CONST               False
              286  STORE_FAST               'check_again'

 L. 103       288  LOAD_GLOBAL              check_for_collision_with_list
              290  LOAD_FAST                'moving_sprite'
              292  LOAD_FAST                'walls'
              294  CALL_FUNCTION_2       2  ''
              296  STORE_FAST               'hit_list_y'

 L. 104       298  LOAD_FAST                'hit_list_x'
              300  STORE_FAST               'complete_hit_list'

 L. 105       302  SETUP_LOOP          338  'to 338'
              304  LOAD_FAST                'hit_list_y'
              306  GET_ITER         
            308_0  COME_FROM           318  '318'
              308  FOR_ITER            336  'to 336'
              310  STORE_FAST               'sprite'

 L. 106       312  LOAD_FAST                'sprite'
              314  LOAD_FAST                'complete_hit_list'
              316  COMPARE_OP               not-in
          318_320  POP_JUMP_IF_FALSE   308  'to 308'

 L. 107       322  LOAD_FAST                'complete_hit_list'
              324  LOAD_METHOD              append
              326  LOAD_FAST                'sprite'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
          332_334  JUMP_BACK           308  'to 308'
              336  POP_BLOCK        
            338_0  COME_FROM_LOOP      302  '302'

 L. 110       338  LOAD_GLOBAL              len
              340  LOAD_FAST                'hit_list_y'
              342  CALL_FUNCTION_1       1  ''
              344  LOAD_CONST               0
              346  COMPARE_OP               >
          348_350  POP_JUMP_IF_FALSE   278  'to 278'

 L. 111       352  LOAD_FAST                'moving_sprite'
              354  LOAD_ATTR                change_x
              356  STORE_FAST               'change_x'

 L. 112       358  LOAD_FAST                'change_x'
              360  LOAD_CONST               0
              362  COMPARE_OP               >
          364_366  POP_JUMP_IF_FALSE   504  'to 504'

 L. 113       368  LOAD_FAST                'ramp_up'
          370_372  POP_JUMP_IF_FALSE   460  'to 460'

 L. 115       374  SETUP_LOOP          502  'to 502'
              376  LOAD_FAST                'hit_list_y'
              378  GET_ITER         
            380_0  COME_FROM           414  '414'
              380  FOR_ITER            456  'to 456'
              382  STORE_FAST               '_'

 L. 118       384  LOAD_FAST                'moving_sprite'
              386  DUP_TOP          
              388  LOAD_ATTR                center_y
              390  LOAD_FAST                'change_x'
              392  INPLACE_ADD      
              394  ROT_TWO          
              396  STORE_ATTR               center_y

 L. 119       398  LOAD_GLOBAL              len
              400  LOAD_GLOBAL              check_for_collision_with_list
              402  LOAD_FAST                'moving_sprite'
              404  LOAD_FAST                'walls'
              406  CALL_FUNCTION_2       2  ''
              408  CALL_FUNCTION_1       1  ''
              410  LOAD_CONST               0
              412  COMPARE_OP               >
          414_416  POP_JUMP_IF_FALSE   380  'to 380'

 L. 121       418  LOAD_FAST                'moving_sprite'
              420  DUP_TOP          
              422  LOAD_ATTR                center_y
              424  LOAD_FAST                'change_x'
              426  INPLACE_SUBTRACT 
              428  ROT_TWO          
              430  STORE_ATTR               center_y

 L. 122       432  LOAD_FAST                'moving_sprite'
              434  DUP_TOP          
              436  LOAD_ATTR                center_x
              438  LOAD_CONST               1
              440  INPLACE_SUBTRACT 
              442  ROT_TWO          
              444  STORE_ATTR               center_x

 L. 124       446  LOAD_CONST               True
              448  STORE_FAST               'check_again'

 L. 125       450  BREAK_LOOP       
          452_454  JUMP_BACK           380  'to 380'
              456  POP_BLOCK        
              458  JUMP_FORWARD        502  'to 502'
            460_0  COME_FROM           370  '370'

 L. 130       460  SETUP_LOOP          660  'to 660'
              462  LOAD_GLOBAL              len
              464  LOAD_GLOBAL              check_for_collision_with_list
              466  LOAD_FAST                'moving_sprite'
              468  LOAD_FAST                'walls'
              470  CALL_FUNCTION_2       2  ''
              472  CALL_FUNCTION_1       1  ''
              474  LOAD_CONST               0
              476  COMPARE_OP               >
          478_480  POP_JUMP_IF_FALSE   500  'to 500'

 L. 131       482  LOAD_FAST                'moving_sprite'
              484  DUP_TOP          
              486  LOAD_ATTR                center_x
              488  LOAD_CONST               1
              490  INPLACE_SUBTRACT 
              492  ROT_TWO          
              494  STORE_ATTR               center_x
          496_498  JUMP_BACK           462  'to 462'
            500_0  COME_FROM           478  '478'
              500  POP_BLOCK        
            502_0  COME_FROM_LOOP      460  '460'
            502_1  COME_FROM           458  '458'
            502_2  COME_FROM_LOOP      374  '374'
              502  JUMP_BACK           278  'to 278'
            504_0  COME_FROM           364  '364'

 L. 133       504  LOAD_FAST                'change_x'
              506  LOAD_CONST               0
              508  COMPARE_OP               <
          510_512  POP_JUMP_IF_FALSE   652  'to 652'

 L. 134       514  LOAD_FAST                'ramp_up'
          516_518  POP_JUMP_IF_FALSE   608  'to 608'

 L. 135       520  SETUP_LOOP          650  'to 650'
              522  LOAD_FAST                'hit_list_y'
              524  GET_ITER         
            526_0  COME_FROM           560  '560'
              526  FOR_ITER            604  'to 604'
              528  STORE_FAST               'item'

 L. 137       530  LOAD_FAST                'moving_sprite'
              532  DUP_TOP          
              534  LOAD_ATTR                center_y
              536  LOAD_FAST                'change_x'
              538  INPLACE_SUBTRACT 
              540  ROT_TWO          
              542  STORE_ATTR               center_y

 L. 138       544  LOAD_GLOBAL              len
              546  LOAD_GLOBAL              check_for_collision_with_list
              548  LOAD_FAST                'moving_sprite'
              550  LOAD_FAST                'walls'
              552  CALL_FUNCTION_2       2  ''
              554  CALL_FUNCTION_1       1  ''
              556  LOAD_CONST               0
              558  COMPARE_OP               >
          560_562  POP_JUMP_IF_FALSE   526  'to 526'

 L. 140       564  LOAD_FAST                'moving_sprite'
              566  DUP_TOP          
              568  LOAD_ATTR                center_y
              570  LOAD_FAST                'change_x'
              572  INPLACE_ADD      
              574  ROT_TWO          
              576  STORE_ATTR               center_y

 L. 141       578  LOAD_GLOBAL              max
              580  LOAD_FAST                'item'
              582  LOAD_ATTR                right
              584  LOAD_FAST                'moving_sprite'
              586  LOAD_ATTR                left
              588  CALL_FUNCTION_2       2  ''
              590  LOAD_FAST                'moving_sprite'
              592  STORE_ATTR               left

 L. 144       594  LOAD_CONST               True
              596  STORE_FAST               'check_again'

 L. 145       598  BREAK_LOOP       
          600_602  JUMP_BACK           526  'to 526'
              604  POP_BLOCK        
              606  JUMP_FORWARD        650  'to 650'
            608_0  COME_FROM           516  '516'

 L. 148       608  SETUP_LOOP          660  'to 660'
              610  LOAD_GLOBAL              len
              612  LOAD_GLOBAL              check_for_collision_with_list
              614  LOAD_FAST                'moving_sprite'
              616  LOAD_FAST                'walls'
              618  CALL_FUNCTION_2       2  ''
              620  CALL_FUNCTION_1       1  ''
              622  LOAD_CONST               0
              624  COMPARE_OP               >
          626_628  POP_JUMP_IF_FALSE   648  'to 648'

 L. 149       630  LOAD_FAST                'moving_sprite'
              632  DUP_TOP          
              634  LOAD_ATTR                center_x
              636  LOAD_CONST               1
              638  INPLACE_ADD      
              640  ROT_TWO          
              642  STORE_ATTR               center_x
          644_646  JUMP_BACK           610  'to 610'
            648_0  COME_FROM           626  '626'
              648  POP_BLOCK        
            650_0  COME_FROM_LOOP      608  '608'
            650_1  COME_FROM           606  '606'
            650_2  COME_FROM_LOOP      520  '520'
              650  JUMP_BACK           278  'to 278'
            652_0  COME_FROM           510  '510'

 L. 152       652  LOAD_GLOBAL              print
              654  LOAD_STR                 "Error, x collision while player wasn't moving.\nMake sure you aren't calling multiple updates, like a physics engine update and an all sprites list update."
              656  CALL_FUNCTION_1       1  ''
              658  POP_TOP          
          660_662  JUMP_BACK           278  'to 278'
            664_0  COME_FROM           280  '280'
              664  POP_BLOCK        
            666_0  COME_FROM_LOOP      274  '274'

 L. 157       666  LOAD_FAST                'complete_hit_list'
              668  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_GLOBAL' instruction at offset 240


class PhysicsEngineSimple:
    """PhysicsEngineSimple"""

    def __init__(self, player_sprite: Sprite, walls: SpriteList):
        """
        Create a simple physics engine.

        :param Sprite player_sprite: The moving sprite
        :param SpriteList walls: The sprites it can't move through
        """
        assert isinstance(player_sprite, Sprite)
        assert isinstance(walls, SpriteList)
        self.player_sprite = player_sprite
        self.walls = walls

    def update(self):
        """
        Move everything and resolve collisions.

        :Returns: SpriteList with all sprites contacted. Empty list if no sprites.
        """
        complete_hit_list = _move_sprite((self.player_sprite), (self.walls), ramp_up=False)
        return complete_hit_list


class PhysicsEnginePlatformer:
    """PhysicsEnginePlatformer"""

    def __init__(self, player_sprite: Sprite, platforms: SpriteList, gravity_constant: float=0.5, ladders: SpriteList=None):
        """
        Create a physics engine for a platformer.

        :param Sprite player_sprite: The moving sprite
        :param SpriteList platforms: The sprites it can't move through
        :param float gravity_constant: Downward acceleration per frame
        :param SpriteList ladders: Ladders the user can climb on
        """
        if ladders is not None:
            if not isinstance(ladders, SpriteList):
                raise TypeError('Fourth parameter should be a SpriteList of ladders')
        self.player_sprite = player_sprite
        self.platforms = platforms
        self.gravity_constant = gravity_constant
        self.jumps_since_ground = 0
        self.allowed_jumps = 1
        self.allow_multi_jump = False
        self.ladders = ladders

    def is_on_ladder(self):
        if self.ladders:
            hit_list = check_for_collision_with_list(self.player_sprite, self.ladders)
            if len(hit_list) > 0:
                return True
        return False

    def can_jump(self, y_distance=5) -> bool:
        """
        Method that looks to see if there is a floor under
        the player_sprite. If there is a floor, the player can jump
        and we return a True.

        :returns: True if there is a platform below us
        :rtype: bool
        """
        self.player_sprite.center_y -= y_distance
        hit_list = check_for_collision_with_list(self.player_sprite, self.platforms)
        self.player_sprite.center_y += y_distance
        if len(hit_list) > 0:
            self.jumps_since_ground = 0
        if (len(hit_list) > 0 or self).allow_multi_jump:
            if self.jumps_since_ground < self.allowed_jumps:
                return True
        return False

    def enable_multi_jump(self, allowed_jumps: int):
        """
        Enables multi-jump.
        allowed_jumps should include the initial jump.
        (1 allows only a single jump, 2 enables double-jump, etc)

        If you enable multi-jump, you MUST call increment_jump_counter()
        every time the player jumps. Otherwise they can jump infinitely.

        :param int allowed_jumps:
        """
        self.allowed_jumps = allowed_jumps
        self.allow_multi_jump = True

    def disable_multi_jump(self):
        """
        Disables multi-jump.

        Calling this function also removes the requirement to
        call increment_jump_counter() every time the player jumps.
        """
        self.allow_multi_jump = False
        self.allowed_jumps = 1
        self.jumps_since_ground = 0

    def jump(self, velocity: int):
        self.player_sprite.change_y = velocity
        self.increment_jump_counter()

    def increment_jump_counter(self):
        """
        Updates the jump counter for multi-jump tracking
        """
        if self.allow_multi_jump:
            self.jumps_since_ground += 1

    def update(self):
        """
        Move everything and resolve collisions.

        :Returns: SpriteList with all sprites contacted. Empty list if no sprites.
        """
        if not self.is_on_ladder():
            self.player_sprite.change_y -= self.gravity_constant
        complete_hit_list = _move_sprite((self.player_sprite), (self.platforms), ramp_up=True)
        for platform in self.platforms:
            if not platform.change_x != 0:
                if platform.change_y != 0:
                    platform.center_x += platform.change_x
                    if platform.boundary_left is not None:
                        if platform.left <= platform.boundary_left:
                            platform.left = platform.boundary_left
                            if platform.change_x < 0:
                                platform.change_x *= -1
                    if platform.boundary_right is not None:
                        if platform.right >= platform.boundary_right:
                            platform.right = platform.boundary_right
                            if platform.change_x > 0:
                                platform.change_x *= -1
                    if check_for_collision(self.player_sprite, platform):
                        if platform.change_x < 0:
                            self.player_sprite.right = platform.left
                        if platform.change_x > 0:
                            self.player_sprite.left = platform.right
                    platform.center_y += platform.change_y
                    if platform.boundary_top is not None and platform.top >= platform.boundary_top:
                        platform.top = platform.boundary_top
                        if platform.change_y > 0:
                            platform.change_y *= -1
                if platform.boundary_bottom is not None and platform.bottom <= platform.boundary_bottom:
                    platform.bottom = platform.boundary_bottom
                    if platform.change_y < 0:
                        platform.change_y *= -1

        return complete_hit_list