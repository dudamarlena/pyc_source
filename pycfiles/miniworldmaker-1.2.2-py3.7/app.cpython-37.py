# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\app\app.py
# Compiled at: 2020-02-16 10:07:47
# Size of source mod 2**32: 16323 bytes
import logging, os, sys
from collections import deque
import miniworldmaker.containers.actionbar as a_bar
import pkg_resources, pygame
from deprecated import deprecated
from miniworldmaker.containers import color_toolbar
import miniworldmaker.containers as container_file
from miniworldmaker.containers import event_console
from miniworldmaker.containers import inspect_actor_toolbar
from miniworldmaker.containers import level_designer_toolbar
from miniworldmaker.tools import keys
version = pkg_resources.require('MiniWorldMaker')[0].version
print('Show new MiniWorldMaker v.{0} Window'.format(version))
print("Press 'F5'  to add Event-console")
print("Press 'F6'  to add Actor-Toolbar")
print("Press 'F7'  to add Level-Designer")
print("Press 'F8'  to add Color-Toolbar")

class App:
    __doc__ = 'The class app contains the game itself. It is called the first time you call board.show().\n    '
    log = logging.getLogger('miniworldmaker')
    board = None
    window = None
    quit = False

    def __init__(self, title):
        self.title = title
        self._containers = []
        self._containers_right = []
        self._containers_bottom = []
        App.window = self
        self.default_size = 200
        self.dirty = 1
        self._containers_width = 0
        self._containers_height = 0
        self.repaint_areas = []
        self.window_surface = None
        self.log_events = 'None'
        self.event_console = None
        self.action_bar = None
        self.event_queue = deque()
        self.docks = 0
        self.actor_toolbar = None
        self.level_designer = None
        self.full_screen = False
        self.color_console = False
        self.dirty = True
        pygame.display.set_caption(title)
        my_path = os.path.abspath(os.path.dirname(__file__))
        try:
            path = os.path.join(my_path, '../resources/logo_small_32.png')
            surface = pygame.image.load(path)
            pygame.display.set_icon(surface)
        except:
            pass

    def _display_update(self):
        self._recalculate_dimensions()
        if self.full_screen:
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
        else:
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.window_surface.set_alpha(None)

    @deprecated(version='1.0.44', reason='You should use App.run()')
    def show(self, image, full_screen: bool=False, log=False):
        """
        deprecated
        """
        self.run(image, full_screen, log)

    def run(self, image, full_screen: bool=False, log=False):
        """
        runs the main_loop

        Lines after this statement are not reachable

        Args:
            self:
            image:
            full_screen:
            log:

        Returns:

        """
        self.full_screen = full_screen
        self._recalculate_dimensions()
        self._setup_images()
        self._display_update()
        pygame.display.update([image.get_rect()])
        if log is True:
            logging.basicConfig(level=(logging.DEBUG))
        else:
            logging.basicConfig(level=(logging.INFO))
        self.window.window_surface.blit(image, self.board.rect)
        App.log.info('Created window with width: {0}, height: {1}'.format(self.window_width, self.window_height))
        import miniworldmaker.tokens.token as tkn
        for token_class in tkn.Token.all_subclasses():
            tkn.Token.check_for_deprecated_methods(token_class)

        while not App.quit:
            self._update()

        pygame.display.quit()
        sys.exit()

    def _setup_images(self):
        from pathlib import Path
        from miniworldmaker.appearances import appearance
        jpgs = list(Path('./images/').rglob('*.[jJ][pP][gG]'))
        jpegs = list(Path('./images/w wwsdsdwasd').rglob('*.[jJ][pP][eE][gG]'))
        pngs = list(Path('./images/').rglob('*.[pP][nN][gG]'))
        images = jpgs + jpegs + pngs
        for img_path in images:
            _image = appearance.Appearance.load_image(img_path)

    def _update(self):
        self._process_pygame_events()
        if self.dirty:
            self._display_update()
            self.dirty = False
        if not App.quit:
            self.repaint_areas = []
            if self.dirty:
                self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
                self.dirty = 0
            while self.event_queue:
                element = self.event_queue.pop()
                for ct in self._containers:
                    ct.handle_event(element[0], element[1])

            self.event_queue.clear()
            for ct in self._containers:
                if ct.dirty:
                    ct.update()
                    ct.repaint()
                    ct.blit_surface_to_window_surface()

            self.board._update_all_costumes()
            self.board._update_background()
            pygame.display.update(self.repaint_areas)
            self.repaint_areas = []

    def _update_containers(self):
        top_left = 0
        for ct in self._containers_right:
            ct.container_top_left_x = top_left
            top_left += ct.container_width

        top_left = 0
        for ct in self._containers_bottom:
            ct.container_top_left_y = top_left
            top_left += ct.container_height

        self.dirty = 1

    def add_container(self, container, dock, size=None) -> container_file.Container:
        self._recalculate_dimensions()
        for ct in self._containers:
            print('add container', container, self.window_height)

        if dock == 'right' or dock == 'top_left':
            self._containers_right.append(container)
        if dock == 'bottom' or dock == 'top_left':
            self._containers_bottom.append(container)
        self._containers.append(container)
        if size is None:
            size = container.default_size
        container._add_to_window(self, dock, size)
        self._display_update()
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1

        if self.board:
            for token in self.board.tokens:
                token.dirty = 1

        return container

    def remove_container(self, container):
        self._containers.remove(container)
        if container in self._containers_right:
            self._containers_right.remove(container)
        if container in self._containers_bottom:
            self._containers_bottom.remove(container)
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1

        if self.board:
            for token in self.board._tokens:
                token.dirty = 1

        self._update_containers()
        self._update()

    def reset(self):
        """
        Entfernt alle Akteure aus dem Grid und setzt sie an ihre Ursprungspositionen.
        """
        for container in self._containers:
            container.remove()
            self.remove_container(container)

    def _recalculate_dimensions(self):
        self._update_containers()
        containers_width = 0
        for container in self._containers:
            if container.window_docking_position == 'top_left':
                containers_width = container.container_width
            else:
                if container.window_docking_position == 'right':
                    containers_width += container.container_width

        containers_height = 0
        for container in self._containers:
            if container.window_docking_position == 'top_left':
                containers_height = container.container_height
            else:
                if container.window_docking_position == 'bottom':
                    containers_height += container.container_height

        self.dirty = 1
        self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
        self._containers_width, self._containers_height = containers_width, containers_height

    @property
    def window_width(self):
        return self._containers_width

    @property
    def window_height(self):
        return self._containers_height

    def get_container_by_pixel(self, pixel_x: int, pixel_y: int):
        for container in self._containers:
            if container.rect.collidepoint((pixel_x, pixel_y)):
                return container

    def _process_pygame_events--- This code section failed: ---

 L. 249         0  LOAD_GLOBAL              pygame
                2  LOAD_ATTR                key
                4  LOAD_METHOD              get_pressed
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  LOAD_METHOD              count
               10  LOAD_CONST               1
               12  CALL_METHOD_1         1  '1 positional argument'
               14  LOAD_CONST               0
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    98  'to 98'

 L. 250        20  LOAD_GLOBAL              pygame
               22  LOAD_ATTR                key
               24  LOAD_METHOD              get_pressed
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  STORE_FAST               'keys_pressed'

 L. 251        30  LOAD_GLOBAL              keys
               32  LOAD_METHOD              key_codes_to_keys
               34  LOAD_FAST                'keys_pressed'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  STORE_FAST               'key_codes'

 L. 252        40  LOAD_STR                 'STRG'
               42  LOAD_FAST                'key_codes'
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  LOAD_STR                 'Q'
               50  LOAD_FAST                'key_codes'
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L. 253        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _call_quit_event
               60  CALL_METHOD_0         0  '0 positional arguments'
               62  POP_TOP          
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM            46  '46'

 L. 254        64  LOAD_FAST                'self'
               66  LOAD_METHOD              send_event_to_containers
               68  LOAD_STR                 'key_pressed'
               70  LOAD_GLOBAL              keys
               72  LOAD_METHOD              key_codes_to_keys
               74  LOAD_FAST                'keys_pressed'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  POP_TOP          

 L. 255        82  LOAD_FAST                'self'
               84  LOAD_METHOD              key_pressed
               86  LOAD_GLOBAL              keys
               88  LOAD_METHOD              key_codes_to_keys
               90  LOAD_FAST                'keys_pressed'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  POP_TOP          
             98_0  COME_FROM            18  '18'

 L. 256    98_100  SETUP_LOOP         1062  'to 1062'
              102  LOAD_GLOBAL              pygame
              104  LOAD_ATTR                event
              106  LOAD_METHOD              get
              108  CALL_METHOD_0         0  '0 positional arguments'
              110  GET_ITER         
            112_0  COME_FROM           266  '266'
          112_114  FOR_ITER           1060  'to 1060'
              116  STORE_FAST               'event'

 L. 258       118  LOAD_FAST                'event'
              120  LOAD_ATTR                type
              122  LOAD_GLOBAL              pygame
              124  LOAD_ATTR                QUIT
              126  COMPARE_OP               ==
              128  POP_JUMP_IF_FALSE   140  'to 140'

 L. 259       130  LOAD_FAST                'self'
              132  LOAD_METHOD              _call_quit_event
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  POP_TOP          
              138  JUMP_BACK           112  'to 112'
            140_0  COME_FROM           128  '128'

 L. 261       140  LOAD_FAST                'event'
              142  LOAD_ATTR                type
              144  LOAD_GLOBAL              pygame
              146  LOAD_ATTR                MOUSEBUTTONDOWN
              148  COMPARE_OP               ==
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 262       152  LOAD_FAST                'self'
              154  LOAD_METHOD              send_mouse_down
              156  LOAD_FAST                'event'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          
              162  JUMP_BACK           112  'to 112'
            164_0  COME_FROM           150  '150'

 L. 263       164  LOAD_FAST                'event'
              166  LOAD_ATTR                type
              168  LOAD_GLOBAL              pygame
              170  LOAD_ATTR                MOUSEMOTION
              172  COMPARE_OP               ==
              174  POP_JUMP_IF_FALSE   212  'to 212'

 L. 264       176  LOAD_GLOBAL              pygame
              178  LOAD_ATTR                mouse
              180  LOAD_METHOD              get_pos
              182  CALL_METHOD_0         0  '0 positional arguments'
              184  STORE_FAST               'pos'

 L. 265       186  LOAD_FAST                'self'
              188  LOAD_METHOD              send_event_to_containers
              190  LOAD_STR                 'mouse_motion'
              192  LOAD_FAST                'pos'
              194  LOAD_CONST               0
              196  BINARY_SUBSCR    
              198  LOAD_FAST                'pos'
              200  LOAD_CONST               1
              202  BINARY_SUBSCR    
              204  BUILD_TUPLE_2         2 
              206  CALL_METHOD_2         2  '2 positional arguments'
              208  POP_TOP          
              210  JUMP_BACK           112  'to 112'
            212_0  COME_FROM           174  '174'

 L. 267       212  LOAD_FAST                'event'
              214  LOAD_ATTR                type
              216  LOAD_GLOBAL              pygame
              218  LOAD_ATTR                KEYUP
              220  COMPARE_OP               ==
          222_224  POP_JUMP_IF_FALSE   256  'to 256'

 L. 268       226  LOAD_GLOBAL              keys
              228  LOAD_METHOD              key_codes_to_keys
              230  LOAD_GLOBAL              pygame
              232  LOAD_ATTR                key
              234  LOAD_METHOD              get_pressed
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  STORE_FAST               'keys_pressed'

 L. 269       242  LOAD_FAST                'self'
              244  LOAD_METHOD              send_event_to_containers
              246  LOAD_STR                 'key_up'
              248  LOAD_FAST                'keys_pressed'
              250  CALL_METHOD_2         2  '2 positional arguments'
              252  POP_TOP          
              254  JUMP_BACK           112  'to 112'
            256_0  COME_FROM           222  '222'

 L. 270       256  LOAD_FAST                'event'
              258  LOAD_ATTR                type
              260  LOAD_GLOBAL              pygame
              262  LOAD_ATTR                KEYDOWN
              264  COMPARE_OP               ==
              266  POP_JUMP_IF_FALSE   112  'to 112'

 L. 271       268  LOAD_GLOBAL              keys
              270  LOAD_METHOD              key_codes_to_keys
              272  LOAD_GLOBAL              pygame
              274  LOAD_ATTR                key
              276  LOAD_METHOD              get_pressed
              278  CALL_METHOD_0         0  '0 positional arguments'
              280  CALL_METHOD_1         1  '1 positional argument'
              282  STORE_FAST               'keys_pressed'

 L. 272       284  LOAD_STR                 'F5'
              286  LOAD_FAST                'keys_pressed'
              288  COMPARE_OP               in
          290_292  POP_JUMP_IF_FALSE   470  'to 470'

 L. 273       294  LOAD_FAST                'self'
              296  LOAD_ATTR                event_console
          298_300  POP_JUMP_IF_TRUE    398  'to 398'

 L. 274       302  LOAD_GLOBAL              event_console
              304  LOAD_METHOD              EventConsole
              306  CALL_METHOD_0         0  '0 positional arguments'
              308  LOAD_FAST                'self'
              310  STORE_ATTR               event_console

 L. 275       312  LOAD_FAST                'self'
              314  LOAD_ATTR                add_container
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                event_console
              320  LOAD_STR                 'right'
              322  LOAD_CONST               ('dock',)
              324  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              326  POP_TOP          

 L. 276       328  LOAD_FAST                'self'
              330  LOAD_ATTR                docks
              332  LOAD_CONST               0
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   370  'to 370'

 L. 277       340  LOAD_GLOBAL              a_bar
              342  LOAD_METHOD              ActionBar
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                board
              348  CALL_METHOD_1         1  '1 positional argument'
              350  LOAD_FAST                'self'
              352  STORE_ATTR               action_bar

 L. 278       354  LOAD_FAST                'self'
              356  LOAD_ATTR                add_container
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                action_bar
              362  LOAD_STR                 'bottom'
              364  LOAD_CONST               ('dock',)
              366  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              368  POP_TOP          
            370_0  COME_FROM           336  '336'

 L. 279       370  LOAD_FAST                'self'
              372  DUP_TOP          
              374  LOAD_ATTR                docks
              376  LOAD_CONST               1
              378  INPLACE_ADD      
              380  ROT_TWO          
              382  STORE_ATTR               docks

 L. 280       384  LOAD_FAST                'self'
              386  LOAD_ATTR                log
              388  LOAD_METHOD              info
              390  LOAD_STR                 'Added event console'
              392  CALL_METHOD_1         1  '1 positional argument'
              394  POP_TOP          
              396  JUMP_FORWARD        468  'to 468'
            398_0  COME_FROM           298  '298'

 L. 281       398  LOAD_FAST                'self'
              400  LOAD_ATTR                event_console
          402_404  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 282       406  LOAD_FAST                'self'
              408  LOAD_METHOD              remove_container
              410  LOAD_FAST                'self'
              412  LOAD_ATTR                event_console
              414  CALL_METHOD_1         1  '1 positional argument'
              416  POP_TOP          

 L. 283       418  LOAD_FAST                'self'
              420  DUP_TOP          
              422  LOAD_ATTR                docks
              424  LOAD_CONST               1
              426  INPLACE_SUBTRACT 
              428  ROT_TWO          
              430  STORE_ATTR               docks

 L. 284       432  LOAD_FAST                'self'
              434  LOAD_ATTR                docks
              436  LOAD_CONST               0
              438  COMPARE_OP               ==
          440_442  POP_JUMP_IF_FALSE   462  'to 462'

 L. 285       444  LOAD_FAST                'self'
              446  LOAD_METHOD              remove_container
              448  LOAD_FAST                'self'
              450  LOAD_ATTR                action_bar
              452  CALL_METHOD_1         1  '1 positional argument'
              454  POP_TOP          

 L. 286       456  LOAD_CONST               True
              458  LOAD_FAST                'self'
              460  STORE_ATTR               running
            462_0  COME_FROM           440  '440'

 L. 287       462  LOAD_CONST               None
              464  LOAD_FAST                'self'
              466  STORE_ATTR               event_console
            468_0  COME_FROM           396  '396'
              468  JUMP_BACK           112  'to 112'
            470_0  COME_FROM           290  '290'

 L. 288       470  LOAD_STR                 'F6'
              472  LOAD_FAST                'keys_pressed'
              474  COMPARE_OP               in
          476_478  POP_JUMP_IF_FALSE   662  'to 662'

 L. 289       480  LOAD_FAST                'self'
              482  LOAD_ATTR                actor_toolbar
          484_486  POP_JUMP_IF_TRUE    588  'to 588'

 L. 290       488  LOAD_GLOBAL              inspect_actor_toolbar
              490  LOAD_METHOD              InspectActorToolbar
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                board
              496  CALL_METHOD_1         1  '1 positional argument'
              498  LOAD_FAST                'self'
              500  STORE_ATTR               actor_toolbar

 L. 291       502  LOAD_FAST                'self'
              504  LOAD_ATTR                docks
              506  LOAD_CONST               0
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_FALSE   544  'to 544'

 L. 292       514  LOAD_GLOBAL              a_bar
              516  LOAD_METHOD              ActionBar
              518  LOAD_FAST                'self'
              520  LOAD_ATTR                board
              522  CALL_METHOD_1         1  '1 positional argument'
              524  LOAD_FAST                'self'
              526  STORE_ATTR               action_bar

 L. 293       528  LOAD_FAST                'self'
              530  LOAD_ATTR                add_container
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                action_bar
              536  LOAD_STR                 'bottom'
              538  LOAD_CONST               ('dock',)
              540  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              542  POP_TOP          
            544_0  COME_FROM           510  '510'

 L. 294       544  LOAD_FAST                'self'
              546  DUP_TOP          
              548  LOAD_ATTR                docks
              550  LOAD_CONST               1
              552  INPLACE_ADD      
              554  ROT_TWO          
              556  STORE_ATTR               docks

 L. 295       558  LOAD_FAST                'self'
              560  LOAD_ATTR                add_container
              562  LOAD_FAST                'self'
              564  LOAD_ATTR                actor_toolbar
              566  LOAD_STR                 'right'
              568  LOAD_CONST               ('dock',)
              570  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              572  POP_TOP          

 L. 296       574  LOAD_FAST                'self'
              576  LOAD_ATTR                log
              578  LOAD_METHOD              info
              580  LOAD_STR                 'Added active actor toolbar'
              582  CALL_METHOD_1         1  '1 positional argument'
              584  POP_TOP          
              586  JUMP_FORWARD        660  'to 660'
            588_0  COME_FROM           484  '484'

 L. 297       588  LOAD_FAST                'self'
              590  LOAD_ATTR                actor_toolbar
          592_594  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 298       596  LOAD_FAST                'self'
              598  LOAD_METHOD              remove_container
              600  LOAD_FAST                'self'
              602  LOAD_ATTR                actor_toolbar
              604  CALL_METHOD_1         1  '1 positional argument'
              606  POP_TOP          

 L. 299       608  LOAD_FAST                'self'
              610  DUP_TOP          
              612  LOAD_ATTR                docks
              614  LOAD_CONST               1
              616  INPLACE_SUBTRACT 
              618  ROT_TWO          
              620  STORE_ATTR               docks

 L. 300       622  LOAD_FAST                'self'
              624  LOAD_ATTR                docks
              626  LOAD_CONST               0
              628  COMPARE_OP               ==
          630_632  POP_JUMP_IF_FALSE   654  'to 654'

 L. 301       634  LOAD_FAST                'self'
              636  LOAD_METHOD              remove_container
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                action_bar
              642  CALL_METHOD_1         1  '1 positional argument'
              644  POP_TOP          

 L. 302       646  LOAD_CONST               True
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                board
              652  STORE_ATTR               is_running
            654_0  COME_FROM           630  '630'

 L. 303       654  LOAD_CONST               None
              656  LOAD_FAST                'self'
              658  STORE_ATTR               actor_toolbar
            660_0  COME_FROM           586  '586'
              660  JUMP_BACK           112  'to 112'
            662_0  COME_FROM           476  '476'

 L. 304       662  LOAD_STR                 'F7'
              664  LOAD_FAST                'keys_pressed'
              666  COMPARE_OP               in
          668_670  POP_JUMP_IF_FALSE   854  'to 854'

 L. 305       672  LOAD_FAST                'self'
              674  LOAD_ATTR                level_designer
          676_678  POP_JUMP_IF_TRUE    780  'to 780'

 L. 306       680  LOAD_GLOBAL              level_designer_toolbar
              682  LOAD_METHOD              LevelDesignerToolbar
              684  LOAD_FAST                'self'
              686  LOAD_ATTR                board
              688  CALL_METHOD_1         1  '1 positional argument'
              690  LOAD_FAST                'self'
              692  STORE_ATTR               level_designer

 L. 307       694  LOAD_FAST                'self'
              696  LOAD_ATTR                docks
              698  LOAD_CONST               0
              700  COMPARE_OP               ==
          702_704  POP_JUMP_IF_FALSE   736  'to 736'

 L. 308       706  LOAD_GLOBAL              a_bar
              708  LOAD_METHOD              ActionBar
              710  LOAD_FAST                'self'
              712  LOAD_ATTR                board
              714  CALL_METHOD_1         1  '1 positional argument'
              716  LOAD_FAST                'self'
              718  STORE_ATTR               action_bar

 L. 309       720  LOAD_FAST                'self'
              722  LOAD_ATTR                add_container
              724  LOAD_FAST                'self'
              726  LOAD_ATTR                action_bar
              728  LOAD_STR                 'bottom'
              730  LOAD_CONST               ('dock',)
              732  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              734  POP_TOP          
            736_0  COME_FROM           702  '702'

 L. 310       736  LOAD_FAST                'self'
              738  DUP_TOP          
              740  LOAD_ATTR                docks
              742  LOAD_CONST               1
              744  INPLACE_ADD      
              746  ROT_TWO          
              748  STORE_ATTR               docks

 L. 311       750  LOAD_FAST                'self'
              752  LOAD_ATTR                add_container
              754  LOAD_FAST                'self'
              756  LOAD_ATTR                level_designer
              758  LOAD_STR                 'right'
              760  LOAD_CONST               ('dock',)
              762  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              764  POP_TOP          

 L. 312       766  LOAD_FAST                'self'
              768  LOAD_ATTR                log
              770  LOAD_METHOD              info
              772  LOAD_STR                 'Added level designer'
              774  CALL_METHOD_1         1  '1 positional argument'
              776  POP_TOP          
              778  JUMP_FORWARD        852  'to 852'
            780_0  COME_FROM           676  '676'

 L. 313       780  LOAD_FAST                'self'
              782  LOAD_ATTR                level_designer
          784_786  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 314       788  LOAD_FAST                'self'
              790  LOAD_METHOD              remove_container
              792  LOAD_FAST                'self'
              794  LOAD_ATTR                level_designer
              796  CALL_METHOD_1         1  '1 positional argument'
              798  POP_TOP          

 L. 315       800  LOAD_CONST               None
              802  LOAD_FAST                'self'
              804  STORE_ATTR               level_designer

 L. 316       806  LOAD_FAST                'self'
              808  DUP_TOP          
              810  LOAD_ATTR                docks
              812  LOAD_CONST               1
              814  INPLACE_SUBTRACT 
              816  ROT_TWO          
              818  STORE_ATTR               docks

 L. 317       820  LOAD_FAST                'self'
              822  LOAD_ATTR                docks
              824  LOAD_CONST               0
              826  COMPARE_OP               ==
          828_830  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 318       832  LOAD_CONST               True
              834  LOAD_FAST                'self'
              836  LOAD_ATTR                board
              838  STORE_ATTR               is_running

 L. 319       840  LOAD_FAST                'self'
              842  LOAD_METHOD              remove_container
              844  LOAD_FAST                'self'
              846  LOAD_ATTR                action_bar
              848  CALL_METHOD_1         1  '1 positional argument'
              850  POP_TOP          
            852_0  COME_FROM           778  '778'
              852  JUMP_BACK           112  'to 112'
            854_0  COME_FROM           668  '668'

 L. 320       854  LOAD_STR                 'F8'
              856  LOAD_FAST                'keys_pressed'
              858  COMPARE_OP               in
          860_862  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 321       864  LOAD_FAST                'self'
              866  LOAD_ATTR                color_console
          868_870  POP_JUMP_IF_TRUE    972  'to 972'

 L. 322       872  LOAD_GLOBAL              color_toolbar
              874  LOAD_METHOD              ColorToolbar
              876  LOAD_FAST                'self'
              878  LOAD_ATTR                board
              880  CALL_METHOD_1         1  '1 positional argument'
              882  LOAD_FAST                'self'
              884  STORE_ATTR               color_console

 L. 323       886  LOAD_FAST                'self'
              888  LOAD_ATTR                docks
              890  LOAD_CONST               0
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_FALSE   928  'to 928'

 L. 324       898  LOAD_GLOBAL              a_bar
              900  LOAD_METHOD              ActionBar
              902  LOAD_FAST                'self'
              904  LOAD_ATTR                board
              906  CALL_METHOD_1         1  '1 positional argument'
              908  LOAD_FAST                'self'
              910  STORE_ATTR               action_bar

 L. 325       912  LOAD_FAST                'self'
              914  LOAD_ATTR                add_container
              916  LOAD_FAST                'self'
              918  LOAD_ATTR                action_bar
              920  LOAD_STR                 'bottom'
              922  LOAD_CONST               ('dock',)
              924  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              926  POP_TOP          
            928_0  COME_FROM           894  '894'

 L. 326       928  LOAD_FAST                'self'
              930  DUP_TOP          
              932  LOAD_ATTR                docks
              934  LOAD_CONST               1
              936  INPLACE_ADD      
              938  ROT_TWO          
              940  STORE_ATTR               docks

 L. 327       942  LOAD_FAST                'self'
              944  LOAD_ATTR                add_container
              946  LOAD_FAST                'self'
              948  LOAD_ATTR                color_console
              950  LOAD_STR                 'right'
              952  LOAD_CONST               ('dock',)
              954  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              956  POP_TOP          

 L. 328       958  LOAD_FAST                'self'
              960  LOAD_ATTR                log
              962  LOAD_METHOD              info
              964  LOAD_STR                 'Added level designer'
              966  CALL_METHOD_1         1  '1 positional argument'
              968  POP_TOP          
              970  JUMP_FORWARD       1044  'to 1044'
            972_0  COME_FROM           868  '868'

 L. 329       972  LOAD_FAST                'self'
              974  LOAD_ATTR                color_console
          976_978  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 330       980  LOAD_FAST                'self'
              982  LOAD_METHOD              remove_container
              984  LOAD_FAST                'self'
              986  LOAD_ATTR                color_console
              988  CALL_METHOD_1         1  '1 positional argument'
              990  POP_TOP          

 L. 331       992  LOAD_CONST               None
              994  LOAD_FAST                'self'
              996  STORE_ATTR               color_console

 L. 332       998  LOAD_FAST                'self'
             1000  DUP_TOP          
             1002  LOAD_ATTR                docks
             1004  LOAD_CONST               1
             1006  INPLACE_SUBTRACT 
             1008  ROT_TWO          
             1010  STORE_ATTR               docks

 L. 333      1012  LOAD_FAST                'self'
             1014  LOAD_ATTR                docks
             1016  LOAD_CONST               0
             1018  COMPARE_OP               ==
         1020_1022  POP_JUMP_IF_FALSE  1058  'to 1058'

 L. 334      1024  LOAD_CONST               True
             1026  LOAD_FAST                'self'
             1028  LOAD_ATTR                board
             1030  STORE_ATTR               is_running

 L. 335      1032  LOAD_FAST                'self'
             1034  LOAD_METHOD              remove_container
             1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                action_bar
             1040  CALL_METHOD_1         1  '1 positional argument'
             1042  POP_TOP          
           1044_0  COME_FROM           970  '970'
             1044  JUMP_BACK           112  'to 112'
           1046_0  COME_FROM           860  '860'

 L. 337      1046  LOAD_FAST                'self'
             1048  LOAD_METHOD              send_event_to_containers
             1050  LOAD_STR                 'key_down'
             1052  LOAD_FAST                'keys_pressed'
             1054  CALL_METHOD_2         2  '2 positional arguments'
             1056  POP_TOP          
           1058_0  COME_FROM          1020  '1020'
           1058_1  COME_FROM           976  '976'
           1058_2  COME_FROM           828  '828'
           1058_3  COME_FROM           784  '784'
           1058_4  COME_FROM           592  '592'
           1058_5  COME_FROM           402  '402'
             1058  JUMP_BACK           112  'to 112'
             1060  POP_BLOCK        
           1062_0  COME_FROM_LOOP       98  '98'

 L. 338      1062  LOAD_CONST               False
             1064  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 1062_0

    def send_mouse_down(self, event):
        pos = pygame.mouse.get_pos()
        if event.button == 1:
            self.send_event_to_containers('mouse_left', (pos[0], pos[1]))
        if event.button == 3:
            self.send_event_to_containers('mouse_right', (pos[0], pos[1]))
        if event.button == 4:
            self.send_event_to_containers('wheel_up', (pos[0], pos[1]))
        if event.button == 5:
            self.send_event_to_containers('wheel_down', (pos[0], pos[1]))
        for token in self.board.tokens:
            if hasattr(token, 'on_clicked_left') and token.sensing_point(pos):
                self.send_event_to_containers('clicked_left', (token, (pos[0], pos[1])))

    def send_event_to_containers(self, event, data):
        events = []
        for container in self._containers:
            e = (
             event, data)
            if event in container.registered_events or 'all' in container.registered_events:
                if event not in events:
                    self.event_queue.appendleft(e)
                    events.append(event)

    def get_keys(self):
        key_codes = []
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
        return key_codes

    def _call_quit_event(self):
        App.quit = True

    def key_pressed(self, key):

        def wrapper_accepting_arguments(key):
            print('My arguments are: {0}, {1}'.format(key))
            function(key)

        return wrapper_accepting_arguments