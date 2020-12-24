# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\windows\miniworldwindow.py
# Compiled at: 2019-06-22 10:15:58
# Size of source mod 2**32: 16304 bytes
import logging, os, sys
import miniworldmaker.containers.actionbar as a_bar
import pkg_resources, pygame
from miniworldmaker.containers import color_toolbar
import miniworldmaker.containers as container_file
from miniworldmaker.containers import event_console
from miniworldmaker.containers import inspect_actor_toolbar
from miniworldmaker.containers import level_designer_toolbar
from miniworldmaker.tools import keys
version = pkg_resources.require('MiniWorldMaker')[0].version
print('Show new MiniWorldMaker v.{0} Window'.format(version))
print("Press '^' to get Actors at mouse_position")
print("Press 'F1' to show help")
print("Press 'F2' to show events in command line")
print("Press 'F3'  to show move-events in command line")
print("Press 'F4'  to show key-events in command line")
print("Press 'F5'  to add Event-console")
print("Press 'F6'  to add Actor-Toolbar")
print("Press 'F7'  to add Level-Designer")
print("Press 'F8'  to add Color-Toolbar")

class MiniWorldWindow:
    log = logging.getLogger('miniworldmaker')
    board = None
    window = None
    quit = False

    def __init__(self, title):
        self.title = title
        self._containers = []
        self._containers_right = []
        self._containers_bottom = []
        MiniWorldWindow.window = self
        self.default_size = 200
        self.dirty = 1
        self._containers_width = 0
        self._containers_height = 0
        self.repaint_areas = []
        self.window_surface = None
        self.log_events = 'None'
        self.event_console = None
        self.action_bar = None
        self.docks = 0
        self.actor_toolbar = None
        self.level_designer = None
        self.full_screen = False
        self.color_console = False
        pygame.display.set_caption(title)
        my_path = os.path.abspath(os.path.dirname(__file__))
        try:
            path = os.path.join(my_path, '../resources/logo_small_32.png')
            surface = pygame.image.load(path)
            pygame.display.set_icon(surface)
        except:
            pass

    def display_update(self):
        self._recalculate_dimensions()
        if self.full_screen:
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.window_surface.set_alpha(None)

    def show(self, image, full_screen: bool=False, log=False):
        self.full_screen = full_screen
        self._recalculate_dimensions()
        self.display_update()
        if log is True:
            logging.basicConfig(level=(logging.DEBUG))
        else:
            logging.basicConfig(level=(logging.INFO))
        self.window.window_surface.blit(image, self.board.rect)
        MiniWorldWindow.log.info('Created window with width: {0}, height: {1}'.format(self.window_width, self.window_height))
        pygame.display.update([image.get_rect()])
        while not MiniWorldWindow.quit:
            self.update()

        pygame.quit()

    def update(self):
        self.process_pygame_events()
        if not MiniWorldWindow.quit:
            self.repaint_areas = []
            if self.dirty:
                self.repaint_areas.append(pygame.Rect(0, 0, self.window_width, self.window_height))
                self.dirty = 0
            for ct in self._containers:
                if ct.dirty:
                    ct.update()
                    ct.repaint()
                    ct.blit_surface_to_window_surface()

            pygame.display.update(self.repaint_areas)
            self.repaint_areas = []

    def update_containers(self):
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
            print('container', container, self.window_height)

        if dock == 'right' or dock == 'top_left':
            self._containers_right.append(container)
        if dock == 'bottom' or dock == 'top_left':
            self._containers_bottom.append(container)
        self._containers.append(container)
        if size is None:
            size = container.default_size
        container._add_to_window(self, dock, size)
        self.display_update()
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1

        if self.board:
            for token in self.board._tokens:
                token.dirty = 1

        return container

    def remove_container(self, container):
        self._containers.remove(container)
        if container in self._containers_right:
            self._containers_right.remove(container)
        if container in self._containers_bottom:
            self._containers_bottom.remove(container)
        self.display_update()
        self.dirty = 1
        for ct in self._containers:
            ct.dirty = 1

        if self.board:
            for token in self.board._tokens:
                token.dirty = 1

        self.update_containers()
        self.update()

    def reset(self):
        """
        Entfernt alle Akteure aus dem Grid und setzt sie an ihre Ursprungspositionen.
        """
        for container in self._containers:
            container.remove()
            self.remove_container(container)

    def _recalculate_dimensions(self):
        self.update_containers()
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

    def process_pygame_events--- This code section failed: ---

 L. 195         0  LOAD_GLOBAL              pygame
                2  LOAD_ATTR                key
                4  LOAD_METHOD              get_pressed
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  LOAD_METHOD              count
               10  LOAD_CONST               1
               12  CALL_METHOD_1         1  '1 positional argument'
               14  LOAD_CONST               0
               16  COMPARE_OP               !=
               18  POP_JUMP_IF_FALSE    82  'to 82'

 L. 196        20  LOAD_GLOBAL              pygame
               22  LOAD_ATTR                key
               24  LOAD_METHOD              get_pressed
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  STORE_FAST               'keys_pressed'

 L. 197        30  LOAD_GLOBAL              keys
               32  LOAD_METHOD              key_codes_to_keys
               34  LOAD_FAST                'keys_pressed'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  STORE_FAST               'key_codes'

 L. 198        40  LOAD_STR                 'STRG'
               42  LOAD_FAST                'key_codes'
               44  COMPARE_OP               in
               46  POP_JUMP_IF_FALSE    64  'to 64'
               48  LOAD_STR                 'Q'
               50  LOAD_FAST                'key_codes'
               52  COMPARE_OP               in
               54  POP_JUMP_IF_FALSE    64  'to 64'

 L. 199        56  LOAD_FAST                'self'
               58  LOAD_METHOD              _call_quit_event
               60  CALL_METHOD_0         0  '0 positional arguments'
               62  POP_TOP          
             64_0  COME_FROM            54  '54'
             64_1  COME_FROM            46  '46'

 L. 200        64  LOAD_FAST                'self'
               66  LOAD_METHOD              send_event_to_containers
               68  LOAD_STR                 'key_pressed'
               70  LOAD_GLOBAL              keys
               72  LOAD_METHOD              key_codes_to_keys
               74  LOAD_FAST                'keys_pressed'
               76  CALL_METHOD_1         1  '1 positional argument'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  POP_TOP          
             82_0  COME_FROM            18  '18'

 L. 201     82_84  SETUP_LOOP         1500  'to 1500'
               86  LOAD_GLOBAL              pygame
               88  LOAD_ATTR                event
               90  LOAD_METHOD              get
               92  CALL_METHOD_0         0  '0 positional arguments'
               94  GET_ITER         
             96_0  COME_FROM           444  '444'
            96_98  FOR_ITER           1498  'to 1498'
              100  STORE_FAST               'event'

 L. 203       102  LOAD_FAST                'event'
              104  LOAD_ATTR                type
              106  LOAD_GLOBAL              pygame
              108  LOAD_ATTR                QUIT
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   124  'to 124'

 L. 204       114  LOAD_FAST                'self'
              116  LOAD_METHOD              _call_quit_event
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  POP_TOP          
              122  JUMP_BACK            96  'to 96'
            124_0  COME_FROM           112  '112'

 L. 206       124  LOAD_FAST                'event'
              126  LOAD_ATTR                type
              128  LOAD_GLOBAL              pygame
              130  LOAD_ATTR                MOUSEBUTTONDOWN
              132  COMPARE_OP               ==
          134_136  POP_JUMP_IF_FALSE   340  'to 340'

 L. 207       138  LOAD_GLOBAL              pygame
              140  LOAD_ATTR                mouse
              142  LOAD_METHOD              get_pos
              144  CALL_METHOD_0         0  '0 positional arguments'
              146  STORE_FAST               'pos'

 L. 208       148  LOAD_GLOBAL              set
              150  CALL_FUNCTION_0       0  '0 positional arguments'
              152  STORE_FAST               'container_set'

 L. 209       154  LOAD_FAST                'self'
              156  LOAD_METHOD              get_container_by_pixel
              158  LOAD_FAST                'pos'
              160  LOAD_CONST               0
              162  BINARY_SUBSCR    
              164  LOAD_FAST                'pos'
              166  LOAD_CONST               1
              168  BINARY_SUBSCR    
              170  CALL_METHOD_2         2  '2 positional arguments'
              172  STORE_FAST               'clicked_container'

 L. 210       174  LOAD_FAST                'container_set'
              176  LOAD_METHOD              add
              178  LOAD_FAST                'clicked_container'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_TOP          

 L. 211       184  SETUP_LOOP          338  'to 338'
              186  LOAD_FAST                'container_set'
              188  GET_ITER         
            190_0  COME_FROM           308  '308'
              190  FOR_ITER            336  'to 336'
              192  STORE_FAST               'container'

 L. 212       194  LOAD_FAST                'event'
              196  LOAD_ATTR                button
              198  LOAD_CONST               1
              200  COMPARE_OP               ==
              202  POP_JUMP_IF_FALSE   228  'to 228'

 L. 213       204  LOAD_FAST                'self'
              206  LOAD_METHOD              send_event_to_containers
              208  LOAD_STR                 'mouse_left'
              210  LOAD_FAST                'pos'
              212  LOAD_CONST               0
              214  BINARY_SUBSCR    
              216  LOAD_FAST                'pos'
              218  LOAD_CONST               1
              220  BINARY_SUBSCR    
              222  BUILD_TUPLE_2         2 
              224  CALL_METHOD_2         2  '2 positional arguments'
              226  POP_TOP          
            228_0  COME_FROM           202  '202'

 L. 214       228  LOAD_FAST                'event'
              230  LOAD_ATTR                button
              232  LOAD_CONST               3
              234  COMPARE_OP               ==
          236_238  POP_JUMP_IF_FALSE   264  'to 264'

 L. 215       240  LOAD_FAST                'self'
              242  LOAD_METHOD              send_event_to_containers
              244  LOAD_STR                 'mouse_right'
              246  LOAD_FAST                'pos'
              248  LOAD_CONST               0
              250  BINARY_SUBSCR    
              252  LOAD_FAST                'pos'
              254  LOAD_CONST               1
              256  BINARY_SUBSCR    
              258  BUILD_TUPLE_2         2 
              260  CALL_METHOD_2         2  '2 positional arguments'
              262  POP_TOP          
            264_0  COME_FROM           236  '236'

 L. 216       264  LOAD_FAST                'event'
              266  LOAD_ATTR                button
              268  LOAD_CONST               4
              270  COMPARE_OP               ==
          272_274  POP_JUMP_IF_FALSE   300  'to 300'

 L. 217       276  LOAD_FAST                'self'
              278  LOAD_METHOD              send_event_to_containers
              280  LOAD_STR                 'wheel_up'
              282  LOAD_FAST                'pos'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  LOAD_FAST                'pos'
              290  LOAD_CONST               1
              292  BINARY_SUBSCR    
              294  BUILD_TUPLE_2         2 
              296  CALL_METHOD_2         2  '2 positional arguments'
              298  POP_TOP          
            300_0  COME_FROM           272  '272'

 L. 218       300  LOAD_FAST                'event'
              302  LOAD_ATTR                button
              304  LOAD_CONST               5
              306  COMPARE_OP               ==
              308  POP_JUMP_IF_FALSE   190  'to 190'

 L. 219       310  LOAD_FAST                'self'
              312  LOAD_METHOD              send_event_to_containers
              314  LOAD_STR                 'wheel_down'
              316  LOAD_FAST                'pos'
              318  LOAD_CONST               0
              320  BINARY_SUBSCR    
              322  LOAD_FAST                'pos'
              324  LOAD_CONST               1
              326  BINARY_SUBSCR    
              328  BUILD_TUPLE_2         2 
              330  CALL_METHOD_2         2  '2 positional arguments'
              332  POP_TOP          
              334  JUMP_BACK           190  'to 190'
              336  POP_BLOCK        
            338_0  COME_FROM_LOOP      184  '184'
              338  JUMP_BACK            96  'to 96'
            340_0  COME_FROM           134  '134'

 L. 220       340  LOAD_FAST                'event'
              342  LOAD_ATTR                type
              344  LOAD_GLOBAL              pygame
              346  LOAD_ATTR                MOUSEMOTION
              348  COMPARE_OP               ==
          350_352  POP_JUMP_IF_FALSE   390  'to 390'

 L. 221       354  LOAD_GLOBAL              pygame
              356  LOAD_ATTR                mouse
              358  LOAD_METHOD              get_pos
              360  CALL_METHOD_0         0  '0 positional arguments'
              362  STORE_FAST               'pos'

 L. 222       364  LOAD_FAST                'self'
              366  LOAD_METHOD              send_event_to_containers
              368  LOAD_STR                 'mouse_motion'
              370  LOAD_FAST                'pos'
              372  LOAD_CONST               0
              374  BINARY_SUBSCR    
              376  LOAD_FAST                'pos'
              378  LOAD_CONST               1
              380  BINARY_SUBSCR    
              382  BUILD_TUPLE_2         2 
              384  CALL_METHOD_2         2  '2 positional arguments'
              386  POP_TOP          
              388  JUMP_BACK            96  'to 96'
            390_0  COME_FROM           350  '350'

 L. 224       390  LOAD_FAST                'event'
              392  LOAD_ATTR                type
              394  LOAD_GLOBAL              pygame
              396  LOAD_ATTR                KEYUP
              398  COMPARE_OP               ==
          400_402  POP_JUMP_IF_FALSE   434  'to 434'

 L. 225       404  LOAD_GLOBAL              keys
              406  LOAD_METHOD              key_codes_to_keys
              408  LOAD_GLOBAL              pygame
              410  LOAD_ATTR                key
              412  LOAD_METHOD              get_pressed
              414  CALL_METHOD_0         0  '0 positional arguments'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  STORE_FAST               'keys_pressed'

 L. 226       420  LOAD_FAST                'self'
              422  LOAD_METHOD              send_event_to_containers
              424  LOAD_STR                 'key_up'
              426  LOAD_FAST                'keys_pressed'
              428  CALL_METHOD_2         2  '2 positional arguments'
              430  POP_TOP          
              432  JUMP_BACK            96  'to 96'
            434_0  COME_FROM           400  '400'

 L. 228       434  LOAD_FAST                'event'
              436  LOAD_ATTR                type
              438  LOAD_GLOBAL              pygame
              440  LOAD_ATTR                KEYDOWN
              442  COMPARE_OP               ==
              444  POP_JUMP_IF_FALSE    96  'to 96'

 L. 229       446  LOAD_GLOBAL              keys
              448  LOAD_METHOD              key_codes_to_keys
              450  LOAD_GLOBAL              pygame
              452  LOAD_ATTR                key
              454  LOAD_METHOD              get_pressed
              456  CALL_METHOD_0         0  '0 positional arguments'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  STORE_FAST               'keys_pressed'

 L. 230       462  LOAD_STR                 '^'
              464  LOAD_FAST                'keys_pressed'
              466  COMPARE_OP               in
          468_470  POP_JUMP_IF_FALSE   520  'to 520'

 L. 231       472  LOAD_FAST                'self'
              474  LOAD_ATTR                board
              476  LOAD_METHOD              get_tokens_by_pixel
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                board
              482  LOAD_METHOD              get_mouse_position
              484  CALL_METHOD_0         0  '0 positional arguments'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  STORE_FAST               'tokens_at_pos'

 L. 232       490  SETUP_LOOP          518  'to 518'
              492  LOAD_FAST                'tokens_at_pos'
              494  GET_ITER         
              496  FOR_ITER            516  'to 516'
              498  STORE_FAST               'token'

 L. 233       500  LOAD_GLOBAL              MiniWorldWindow
              502  LOAD_ATTR                log
              504  LOAD_METHOD              info
              506  LOAD_FAST                'token'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  POP_TOP          
          512_514  JUMP_BACK           496  'to 496'
              516  POP_BLOCK        
            518_0  COME_FROM_LOOP      490  '490'
              518  JUMP_BACK            96  'to 96'
            520_0  COME_FROM           468  '468'

 L. 234       520  LOAD_STR                 'F1'
              522  LOAD_FAST                'keys_pressed'
              524  COMPARE_OP               in
          526_528  POP_JUMP_IF_FALSE   540  'to 540'

 L. 235       530  LOAD_FAST                'self'
              532  LOAD_METHOD              help
              534  CALL_METHOD_0         0  '0 positional arguments'
              536  POP_TOP          
              538  JUMP_BACK            96  'to 96'
            540_0  COME_FROM           526  '526'

 L. 236       540  LOAD_STR                 'F2'
              542  LOAD_FAST                'keys_pressed'
              544  COMPARE_OP               in
          546_548  POP_JUMP_IF_FALSE   602  'to 602'

 L. 237       550  LOAD_FAST                'self'
              552  LOAD_ATTR                log_events
              554  LOAD_STR                 'all'
              556  COMPARE_OP               is-not
          558_560  POP_JUMP_IF_FALSE   582  'to 582'

 L. 238       562  LOAD_STR                 'all'
              564  LOAD_FAST                'self'
              566  STORE_ATTR               log_events

 L. 239       568  LOAD_FAST                'self'
              570  LOAD_ATTR                log
              572  LOAD_METHOD              info
              574  LOAD_STR                 'Log all events'
              576  CALL_METHOD_1         1  '1 positional argument'
              578  POP_TOP          
              580  JUMP_FORWARD        600  'to 600'
            582_0  COME_FROM           558  '558'

 L. 241       582  LOAD_STR                 'None'
              584  LOAD_FAST                'self'
              586  STORE_ATTR               log_events

 L. 242       588  LOAD_FAST                'self'
              590  LOAD_ATTR                log
              592  LOAD_METHOD              info
              594  LOAD_STR                 'Stopped logging events'
              596  CALL_METHOD_1         1  '1 positional argument'
              598  POP_TOP          
            600_0  COME_FROM           580  '580'
              600  JUMP_BACK            96  'to 96'
            602_0  COME_FROM           546  '546'

 L. 243       602  LOAD_STR                 'F3'
              604  LOAD_FAST                'keys_pressed'
              606  COMPARE_OP               in
          608_610  POP_JUMP_IF_FALSE   664  'to 664'

 L. 244       612  LOAD_FAST                'self'
              614  LOAD_ATTR                log_events
              616  LOAD_STR                 'move'
              618  COMPARE_OP               is-not
          620_622  POP_JUMP_IF_FALSE   644  'to 644'

 L. 245       624  LOAD_STR                 'move'
              626  LOAD_FAST                'self'
              628  STORE_ATTR               log_events

 L. 246       630  LOAD_FAST                'self'
              632  LOAD_ATTR                log
              634  LOAD_METHOD              info
              636  LOAD_STR                 'Log move events'
              638  CALL_METHOD_1         1  '1 positional argument'
              640  POP_TOP          
              642  JUMP_FORWARD        662  'to 662'
            644_0  COME_FROM           620  '620'

 L. 248       644  LOAD_STR                 'None'
              646  LOAD_FAST                'self'
              648  STORE_ATTR               log_events

 L. 249       650  LOAD_FAST                'self'
              652  LOAD_ATTR                log
              654  LOAD_METHOD              info
              656  LOAD_STR                 'Stopped logging events'
              658  CALL_METHOD_1         1  '1 positional argument'
              660  POP_TOP          
            662_0  COME_FROM           642  '642'
              662  JUMP_BACK            96  'to 96'
            664_0  COME_FROM           608  '608'

 L. 250       664  LOAD_STR                 'F4'
              666  LOAD_FAST                'keys_pressed'
              668  COMPARE_OP               in
          670_672  POP_JUMP_IF_FALSE   726  'to 726'

 L. 251       674  LOAD_FAST                'self'
              676  LOAD_ATTR                log_events
              678  LOAD_STR                 'key_events'
              680  COMPARE_OP               is-not
          682_684  POP_JUMP_IF_FALSE   706  'to 706'

 L. 252       686  LOAD_STR                 'key_events'
              688  LOAD_FAST                'self'
              690  STORE_ATTR               log_events

 L. 253       692  LOAD_FAST                'self'
              694  LOAD_ATTR                log
              696  LOAD_METHOD              info
              698  LOAD_STR                 'Log key events'
              700  CALL_METHOD_1         1  '1 positional argument'
              702  POP_TOP          
              704  JUMP_FORWARD        724  'to 724'
            706_0  COME_FROM           682  '682'

 L. 255       706  LOAD_STR                 'None'
              708  LOAD_FAST                'self'
              710  STORE_ATTR               log_events

 L. 256       712  LOAD_FAST                'self'
              714  LOAD_ATTR                log
              716  LOAD_METHOD              info
              718  LOAD_STR                 'Stopped logging events'
              720  CALL_METHOD_1         1  '1 positional argument'
              722  POP_TOP          
            724_0  COME_FROM           704  '704'
              724  JUMP_BACK            96  'to 96'
            726_0  COME_FROM           670  '670'

 L. 257       726  LOAD_STR                 'F5'
              728  LOAD_FAST                'keys_pressed'
              730  COMPARE_OP               in
          732_734  POP_JUMP_IF_FALSE   912  'to 912'

 L. 258       736  LOAD_FAST                'self'
              738  LOAD_ATTR                event_console
          740_742  POP_JUMP_IF_TRUE    840  'to 840'

 L. 259       744  LOAD_GLOBAL              event_console
              746  LOAD_METHOD              EventConsole
              748  CALL_METHOD_0         0  '0 positional arguments'
              750  LOAD_FAST                'self'
              752  STORE_ATTR               event_console

 L. 260       754  LOAD_FAST                'self'
              756  LOAD_ATTR                add_container
              758  LOAD_FAST                'self'
              760  LOAD_ATTR                event_console
              762  LOAD_STR                 'right'
              764  LOAD_CONST               ('dock',)
              766  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              768  POP_TOP          

 L. 261       770  LOAD_FAST                'self'
              772  LOAD_ATTR                docks
              774  LOAD_CONST               0
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   812  'to 812'

 L. 262       782  LOAD_GLOBAL              a_bar
              784  LOAD_METHOD              ActionBar
              786  LOAD_FAST                'self'
              788  LOAD_ATTR                board
              790  CALL_METHOD_1         1  '1 positional argument'
              792  LOAD_FAST                'self'
              794  STORE_ATTR               action_bar

 L. 263       796  LOAD_FAST                'self'
              798  LOAD_ATTR                add_container
              800  LOAD_FAST                'self'
              802  LOAD_ATTR                action_bar
              804  LOAD_STR                 'bottom'
              806  LOAD_CONST               ('dock',)
              808  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              810  POP_TOP          
            812_0  COME_FROM           778  '778'

 L. 264       812  LOAD_FAST                'self'
              814  DUP_TOP          
              816  LOAD_ATTR                docks
              818  LOAD_CONST               1
              820  INPLACE_ADD      
              822  ROT_TWO          
              824  STORE_ATTR               docks

 L. 265       826  LOAD_FAST                'self'
              828  LOAD_ATTR                log
              830  LOAD_METHOD              info
              832  LOAD_STR                 'Added event console'
              834  CALL_METHOD_1         1  '1 positional argument'
              836  POP_TOP          
              838  JUMP_FORWARD        910  'to 910'
            840_0  COME_FROM           740  '740'

 L. 266       840  LOAD_FAST                'self'
              842  LOAD_ATTR                event_console
          844_846  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 267       848  LOAD_FAST                'self'
              850  LOAD_METHOD              remove_container
              852  LOAD_FAST                'self'
              854  LOAD_ATTR                event_console
              856  CALL_METHOD_1         1  '1 positional argument'
              858  POP_TOP          

 L. 268       860  LOAD_FAST                'self'
              862  DUP_TOP          
              864  LOAD_ATTR                docks
              866  LOAD_CONST               1
              868  INPLACE_SUBTRACT 
              870  ROT_TWO          
              872  STORE_ATTR               docks

 L. 269       874  LOAD_FAST                'self'
              876  LOAD_ATTR                docks
              878  LOAD_CONST               0
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_FALSE   904  'to 904'

 L. 270       886  LOAD_FAST                'self'
              888  LOAD_METHOD              remove_container
              890  LOAD_FAST                'self'
              892  LOAD_ATTR                action_bar
              894  CALL_METHOD_1         1  '1 positional argument'
              896  POP_TOP          

 L. 271       898  LOAD_CONST               True
              900  LOAD_FAST                'self'
              902  STORE_ATTR               running
            904_0  COME_FROM           882  '882'

 L. 272       904  LOAD_CONST               None
              906  LOAD_FAST                'self'
              908  STORE_ATTR               event_console
            910_0  COME_FROM           838  '838'
              910  JUMP_BACK            96  'to 96'
            912_0  COME_FROM           732  '732'

 L. 273       912  LOAD_STR                 'F6'
              914  LOAD_FAST                'keys_pressed'
              916  COMPARE_OP               in
          918_920  POP_JUMP_IF_FALSE  1100  'to 1100'

 L. 274       922  LOAD_FAST                'self'
              924  LOAD_ATTR                actor_toolbar
          926_928  POP_JUMP_IF_TRUE   1026  'to 1026'

 L. 275       930  LOAD_GLOBAL              inspect_actor_toolbar
              932  LOAD_METHOD              InspectActorToolbar
              934  CALL_METHOD_0         0  '0 positional arguments'
              936  LOAD_FAST                'self'
              938  STORE_ATTR               actor_toolbar

 L. 276       940  LOAD_FAST                'self'
              942  LOAD_ATTR                docks
              944  LOAD_CONST               0
              946  COMPARE_OP               ==
          948_950  POP_JUMP_IF_FALSE   982  'to 982'

 L. 277       952  LOAD_GLOBAL              a_bar
              954  LOAD_METHOD              ActionBar
              956  LOAD_FAST                'self'
              958  LOAD_ATTR                board
              960  CALL_METHOD_1         1  '1 positional argument'
              962  LOAD_FAST                'self'
              964  STORE_ATTR               action_bar

 L. 278       966  LOAD_FAST                'self'
              968  LOAD_ATTR                add_container
              970  LOAD_FAST                'self'
              972  LOAD_ATTR                action_bar
              974  LOAD_STR                 'bottom'
              976  LOAD_CONST               ('dock',)
              978  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              980  POP_TOP          
            982_0  COME_FROM           948  '948'

 L. 279       982  LOAD_FAST                'self'
              984  DUP_TOP          
              986  LOAD_ATTR                docks
              988  LOAD_CONST               1
              990  INPLACE_ADD      
              992  ROT_TWO          
              994  STORE_ATTR               docks

 L. 280       996  LOAD_FAST                'self'
              998  LOAD_ATTR                add_container
             1000  LOAD_FAST                'self'
             1002  LOAD_ATTR                actor_toolbar
             1004  LOAD_STR                 'right'
             1006  LOAD_CONST               ('dock',)
             1008  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1010  POP_TOP          

 L. 281      1012  LOAD_FAST                'self'
             1014  LOAD_ATTR                log
             1016  LOAD_METHOD              info
             1018  LOAD_STR                 'Added active actor toolbar'
             1020  CALL_METHOD_1         1  '1 positional argument'
             1022  POP_TOP          
             1024  JUMP_FORWARD       1098  'to 1098'
           1026_0  COME_FROM           926  '926'

 L. 282      1026  LOAD_FAST                'self'
             1028  LOAD_ATTR                actor_toolbar
         1030_1032  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 283      1034  LOAD_FAST                'self'
             1036  LOAD_METHOD              remove_container
             1038  LOAD_FAST                'self'
             1040  LOAD_ATTR                actor_toolbar
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  POP_TOP          

 L. 284      1046  LOAD_FAST                'self'
             1048  DUP_TOP          
             1050  LOAD_ATTR                docks
             1052  LOAD_CONST               1
             1054  INPLACE_SUBTRACT 
             1056  ROT_TWO          
             1058  STORE_ATTR               docks

 L. 285      1060  LOAD_FAST                'self'
             1062  LOAD_ATTR                docks
             1064  LOAD_CONST               0
             1066  COMPARE_OP               ==
         1068_1070  POP_JUMP_IF_FALSE  1092  'to 1092'

 L. 286      1072  LOAD_FAST                'self'
             1074  LOAD_METHOD              remove_container
             1076  LOAD_FAST                'self'
             1078  LOAD_ATTR                action_bar
             1080  CALL_METHOD_1         1  '1 positional argument'
             1082  POP_TOP          

 L. 287      1084  LOAD_CONST               True
             1086  LOAD_FAST                'self'
             1088  LOAD_ATTR                board
             1090  STORE_ATTR               is_running
           1092_0  COME_FROM          1068  '1068'

 L. 288      1092  LOAD_CONST               None
             1094  LOAD_FAST                'self'
             1096  STORE_ATTR               actor_toolbar
           1098_0  COME_FROM          1024  '1024'
             1098  JUMP_BACK            96  'to 96'
           1100_0  COME_FROM           918  '918'

 L. 289      1100  LOAD_STR                 'F7'
             1102  LOAD_FAST                'keys_pressed'
             1104  COMPARE_OP               in
         1106_1108  POP_JUMP_IF_FALSE  1292  'to 1292'

 L. 290      1110  LOAD_FAST                'self'
             1112  LOAD_ATTR                level_designer
         1114_1116  POP_JUMP_IF_TRUE   1218  'to 1218'

 L. 291      1118  LOAD_GLOBAL              level_designer_toolbar
             1120  LOAD_METHOD              LevelDesignerToolbar
             1122  LOAD_FAST                'self'
             1124  LOAD_ATTR                board
             1126  CALL_METHOD_1         1  '1 positional argument'
             1128  LOAD_FAST                'self'
             1130  STORE_ATTR               level_designer

 L. 292      1132  LOAD_FAST                'self'
             1134  LOAD_ATTR                docks
             1136  LOAD_CONST               0
             1138  COMPARE_OP               ==
         1140_1142  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 293      1144  LOAD_GLOBAL              a_bar
             1146  LOAD_METHOD              ActionBar
             1148  LOAD_FAST                'self'
             1150  LOAD_ATTR                board
             1152  CALL_METHOD_1         1  '1 positional argument'
             1154  LOAD_FAST                'self'
             1156  STORE_ATTR               action_bar

 L. 294      1158  LOAD_FAST                'self'
             1160  LOAD_ATTR                add_container
             1162  LOAD_FAST                'self'
             1164  LOAD_ATTR                action_bar
             1166  LOAD_STR                 'bottom'
             1168  LOAD_CONST               ('dock',)
             1170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1172  POP_TOP          
           1174_0  COME_FROM          1140  '1140'

 L. 295      1174  LOAD_FAST                'self'
             1176  DUP_TOP          
             1178  LOAD_ATTR                docks
             1180  LOAD_CONST               1
             1182  INPLACE_ADD      
             1184  ROT_TWO          
             1186  STORE_ATTR               docks

 L. 296      1188  LOAD_FAST                'self'
             1190  LOAD_ATTR                add_container
             1192  LOAD_FAST                'self'
             1194  LOAD_ATTR                level_designer
             1196  LOAD_STR                 'right'
             1198  LOAD_CONST               ('dock',)
             1200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1202  POP_TOP          

 L. 297      1204  LOAD_FAST                'self'
             1206  LOAD_ATTR                log
             1208  LOAD_METHOD              info
             1210  LOAD_STR                 'Added level designer'
             1212  CALL_METHOD_1         1  '1 positional argument'
             1214  POP_TOP          
             1216  JUMP_FORWARD       1290  'to 1290'
           1218_0  COME_FROM          1114  '1114'

 L. 298      1218  LOAD_FAST                'self'
             1220  LOAD_ATTR                level_designer
         1222_1224  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 299      1226  LOAD_FAST                'self'
             1228  LOAD_METHOD              remove_container
             1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                level_designer
             1234  CALL_METHOD_1         1  '1 positional argument'
             1236  POP_TOP          

 L. 300      1238  LOAD_CONST               None
             1240  LOAD_FAST                'self'
             1242  STORE_ATTR               level_designer

 L. 301      1244  LOAD_FAST                'self'
             1246  DUP_TOP          
             1248  LOAD_ATTR                docks
             1250  LOAD_CONST               1
             1252  INPLACE_SUBTRACT 
             1254  ROT_TWO          
             1256  STORE_ATTR               docks

 L. 302      1258  LOAD_FAST                'self'
             1260  LOAD_ATTR                docks
             1262  LOAD_CONST               0
             1264  COMPARE_OP               ==
         1266_1268  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 303      1270  LOAD_CONST               True
             1272  LOAD_FAST                'self'
             1274  LOAD_ATTR                board
             1276  STORE_ATTR               is_running

 L. 304      1278  LOAD_FAST                'self'
             1280  LOAD_METHOD              remove_container
             1282  LOAD_FAST                'self'
             1284  LOAD_ATTR                action_bar
             1286  CALL_METHOD_1         1  '1 positional argument'
             1288  POP_TOP          
           1290_0  COME_FROM          1216  '1216'
             1290  JUMP_BACK            96  'to 96'
           1292_0  COME_FROM          1106  '1106'

 L. 305      1292  LOAD_STR                 'F8'
             1294  LOAD_FAST                'keys_pressed'
             1296  COMPARE_OP               in
         1298_1300  POP_JUMP_IF_FALSE  1484  'to 1484'

 L. 306      1302  LOAD_FAST                'self'
             1304  LOAD_ATTR                color_console
         1306_1308  POP_JUMP_IF_TRUE   1410  'to 1410'

 L. 307      1310  LOAD_GLOBAL              color_toolbar
             1312  LOAD_METHOD              ColorToolbar
             1314  LOAD_FAST                'self'
             1316  LOAD_ATTR                board
             1318  CALL_METHOD_1         1  '1 positional argument'
             1320  LOAD_FAST                'self'
             1322  STORE_ATTR               color_console

 L. 308      1324  LOAD_FAST                'self'
             1326  LOAD_ATTR                docks
             1328  LOAD_CONST               0
             1330  COMPARE_OP               ==
         1332_1334  POP_JUMP_IF_FALSE  1366  'to 1366'

 L. 309      1336  LOAD_GLOBAL              a_bar
             1338  LOAD_METHOD              ActionBar
             1340  LOAD_FAST                'self'
             1342  LOAD_ATTR                board
             1344  CALL_METHOD_1         1  '1 positional argument'
             1346  LOAD_FAST                'self'
             1348  STORE_ATTR               action_bar

 L. 310      1350  LOAD_FAST                'self'
             1352  LOAD_ATTR                add_container
             1354  LOAD_FAST                'self'
             1356  LOAD_ATTR                action_bar
             1358  LOAD_STR                 'bottom'
             1360  LOAD_CONST               ('dock',)
             1362  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1364  POP_TOP          
           1366_0  COME_FROM          1332  '1332'

 L. 311      1366  LOAD_FAST                'self'
             1368  DUP_TOP          
             1370  LOAD_ATTR                docks
             1372  LOAD_CONST               1
             1374  INPLACE_ADD      
             1376  ROT_TWO          
             1378  STORE_ATTR               docks

 L. 312      1380  LOAD_FAST                'self'
             1382  LOAD_ATTR                add_container
             1384  LOAD_FAST                'self'
             1386  LOAD_ATTR                color_console
             1388  LOAD_STR                 'right'
             1390  LOAD_CONST               ('dock',)
             1392  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1394  POP_TOP          

 L. 313      1396  LOAD_FAST                'self'
             1398  LOAD_ATTR                log
             1400  LOAD_METHOD              info
             1402  LOAD_STR                 'Added level designer'
             1404  CALL_METHOD_1         1  '1 positional argument'
             1406  POP_TOP          
             1408  JUMP_FORWARD       1482  'to 1482'
           1410_0  COME_FROM          1306  '1306'

 L. 314      1410  LOAD_FAST                'self'
             1412  LOAD_ATTR                color_console
         1414_1416  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 315      1418  LOAD_FAST                'self'
             1420  LOAD_METHOD              remove_container
             1422  LOAD_FAST                'self'
             1424  LOAD_ATTR                color_console
             1426  CALL_METHOD_1         1  '1 positional argument'
             1428  POP_TOP          

 L. 316      1430  LOAD_CONST               None
             1432  LOAD_FAST                'self'
             1434  STORE_ATTR               color_console

 L. 317      1436  LOAD_FAST                'self'
             1438  DUP_TOP          
             1440  LOAD_ATTR                docks
             1442  LOAD_CONST               1
             1444  INPLACE_SUBTRACT 
             1446  ROT_TWO          
             1448  STORE_ATTR               docks

 L. 318      1450  LOAD_FAST                'self'
             1452  LOAD_ATTR                docks
             1454  LOAD_CONST               0
             1456  COMPARE_OP               ==
         1458_1460  POP_JUMP_IF_FALSE  1496  'to 1496'

 L. 319      1462  LOAD_CONST               True
             1464  LOAD_FAST                'self'
             1466  LOAD_ATTR                board
             1468  STORE_ATTR               is_running

 L. 320      1470  LOAD_FAST                'self'
             1472  LOAD_METHOD              remove_container
             1474  LOAD_FAST                'self'
             1476  LOAD_ATTR                action_bar
             1478  CALL_METHOD_1         1  '1 positional argument'
             1480  POP_TOP          
           1482_0  COME_FROM          1408  '1408'
             1482  JUMP_BACK            96  'to 96'
           1484_0  COME_FROM          1298  '1298'

 L. 322      1484  LOAD_FAST                'self'
             1486  LOAD_METHOD              send_event_to_containers
             1488  LOAD_STR                 'key_down'
             1490  LOAD_FAST                'keys_pressed'
             1492  CALL_METHOD_2         2  '2 positional arguments'
             1494  POP_TOP          
           1496_0  COME_FROM          1458  '1458'
           1496_1  COME_FROM          1414  '1414'
           1496_2  COME_FROM          1266  '1266'
           1496_3  COME_FROM          1222  '1222'
           1496_4  COME_FROM          1030  '1030'
           1496_5  COME_FROM           844  '844'
             1496  JUMP_BACK            96  'to 96'
             1498  POP_BLOCK        
           1500_0  COME_FROM_LOOP       82  '82'

 L. 323      1500  LOAD_CONST               False
             1502  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 1500_0

    def send_event_to_containers--- This code section failed: ---

 L. 326         0  SETUP_LOOP          242  'to 242'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _containers
                6  GET_ITER         
              8_0  COME_FROM           216  '216'
              8_1  COME_FROM           200  '200'
              8_2  COME_FROM            30  '30'
                8  FOR_ITER            240  'to 240'
               10  STORE_FAST               'container'

 L. 327        12  LOAD_FAST                'event'
               14  LOAD_FAST                'container'
               16  LOAD_ATTR                register_events
               18  COMPARE_OP               in
               20  POP_JUMP_IF_TRUE     32  'to 32'
               22  LOAD_STR                 'all'
               24  LOAD_FAST                'container'
               26  LOAD_ATTR                register_events
               28  COMPARE_OP               in
               30  POP_JUMP_IF_FALSE     8  'to 8'
             32_0  COME_FROM            20  '20'

 L. 328        32  LOAD_FAST                'container'
               34  LOAD_METHOD              pass_event
               36  LOAD_FAST                'event'
               38  LOAD_FAST                'data'
               40  CALL_METHOD_2         2  '2 positional arguments'
               42  POP_TOP          

 L. 329        44  LOAD_STR                 'mouse'
               46  LOAD_FAST                'event'
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE   110  'to 110'

 L. 330        52  LOAD_STR                 'debug'
               54  LOAD_FAST                'container'
               56  LOAD_ATTR                register_events
               58  COMPARE_OP               in
               60  POP_JUMP_IF_TRUE     96  'to 96'
               62  LOAD_STR                 'mouse'
               64  LOAD_FAST                'container'
               66  LOAD_ATTR                register_events
               68  COMPARE_OP               in
               70  POP_JUMP_IF_TRUE     96  'to 96'
               72  LOAD_FAST                'container'
               74  LOAD_FAST                'self'
               76  LOAD_METHOD              get_container_by_pixel
               78  LOAD_FAST                'data'
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_FAST                'data'
               86  LOAD_CONST               1
               88  BINARY_SUBSCR    
               90  CALL_METHOD_2         2  '2 positional arguments'
               92  COMPARE_OP               ==
               94  POP_JUMP_IF_FALSE   122  'to 122'
             96_0  COME_FROM            70  '70'
             96_1  COME_FROM            60  '60'

 L. 331        96  LOAD_FAST                'container'
               98  LOAD_METHOD              get_event
              100  LOAD_FAST                'event'
              102  LOAD_FAST                'data'
              104  CALL_METHOD_2         2  '2 positional arguments'
              106  POP_TOP          
              108  JUMP_FORWARD        122  'to 122'
            110_0  COME_FROM            50  '50'

 L. 333       110  LOAD_FAST                'container'
              112  LOAD_METHOD              get_event
              114  LOAD_FAST                'event'
              116  LOAD_FAST                'data'
              118  CALL_METHOD_2         2  '2 positional arguments'
              120  POP_TOP          
            122_0  COME_FROM           108  '108'
            122_1  COME_FROM            94  '94'

 L. 334       122  LOAD_FAST                'self'
              124  LOAD_ATTR                log_events
              126  LOAD_STR                 'all'
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   154  'to 154'

 L. 335       132  LOAD_GLOBAL              MiniWorldWindow
              134  LOAD_ATTR                log
              136  LOAD_METHOD              info
              138  LOAD_STR                 "Event: '{0}' with data: {1}"
              140  LOAD_METHOD              format
              142  LOAD_FAST                'event'
              144  LOAD_FAST                'data'
              146  CALL_METHOD_2         2  '2 positional arguments'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  POP_TOP          
              152  JUMP_BACK             8  'to 8'
            154_0  COME_FROM           130  '130'

 L. 337       154  LOAD_FAST                'self'
              156  LOAD_ATTR                log_events
              158  LOAD_STR                 'move'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   192  'to 192'
              164  LOAD_FAST                'event'
              166  LOAD_STR                 'move'
              168  COMPARE_OP               ==
              170  POP_JUMP_IF_FALSE   192  'to 192'

 L. 338       172  LOAD_GLOBAL              MiniWorldWindow
              174  LOAD_ATTR                log
              176  LOAD_METHOD              info
              178  LOAD_STR                 "Event: '{0}' with data: {1}"
              180  LOAD_METHOD              format
              182  LOAD_FAST                'event'
              184  LOAD_FAST                'data'
              186  CALL_METHOD_2         2  '2 positional arguments'
              188  CALL_METHOD_1         1  '1 positional argument'
              190  POP_TOP          
            192_0  COME_FROM           170  '170'
            192_1  COME_FROM           162  '162'

 L. 339       192  LOAD_FAST                'self'
              194  LOAD_ATTR                log_events
              196  LOAD_STR                 'key'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE     8  'to 8'
              202  LOAD_FAST                'event'
              204  LOAD_STR                 'key_pressed'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_TRUE    218  'to 218'
              210  LOAD_FAST                'event'
              212  LOAD_STR                 'key_pressed'
              214  COMPARE_OP               ==
              216  POP_JUMP_IF_FALSE     8  'to 8'
            218_0  COME_FROM           208  '208'

 L. 340       218  LOAD_GLOBAL              MiniWorldWindow
              220  LOAD_ATTR                log
              222  LOAD_METHOD              info
              224  LOAD_STR                 "Event: '{0}' with data: {1}"
              226  LOAD_METHOD              format
              228  LOAD_FAST                'event'
              230  LOAD_FAST                'data'
              232  CALL_METHOD_2         2  '2 positional arguments'
              234  CALL_METHOD_1         1  '1 positional argument'
              236  POP_TOP          
              238  JUMP_BACK             8  'to 8'
              240  POP_BLOCK        
            242_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 110_0

    def get_keys(self):
        key_codes = []
        if pygame.key.get_pressed().count(1) != 0:
            keys_pressed = pygame.key.get_pressed()
            key_codes = keys.key_codes_to_keys(keys_pressed)
        return key_codes

    def _call_quit_event(self):
        MiniWorldWindow.quit = True
        pygame.quit()
        sys.exit(0)