# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\gamegridp\gamegrid.py
# Compiled at: 2018-09-13 06:55:27
# Size of source mod 2**32: 48216 bytes
"""
Created on Mon Apr 16 21:49:29 2018

@author: asieb
"""
import logging, os, easygui, pygame, math
from gamegridp import gamegrid_actionbar
from gamegridp import gamegrid_console
from gamegridp import gamegrid_toolbar
from gamegridp import keys
import sys, sqlite3 as lite
from collections import defaultdict

class GameGrid(object):
    __doc__ = '\n    Das GameGrid\n        Das **GameGrid** ist ein **Spielfeld**, welches in einzelne Zellen unterteilt ist.\n        Es kann unterschieden werden zwischen zwei Arten von GameGrids:\n\n        Die Zellengröße ist 1:\n            Es handelt sich um ein pixelgenaues Spiel bei dem die exakte Position\n            der Akteure von Bedeutung ist.\n        Die Zellengröße ist größer als 1:\n            Es handelt sich um ein Spiel, das auf einzelnen Feldern basiert.\n\n        Für beide Arten von Spielen gibt es einige Subklassen, die Spezialfunktionen zur Verfügung stellen.\n\n    Attributes\n    ----------\n\n    cell_size : int\n        Die Größe einer einzelnen Zelle in Pixeln.\n    toolbar : gamegridp.Toolbar\n        Die Toolbar auf der rechten Seite\n    actionbar : gamegridp.Actionbar\n        Die Actionbar unterhalb des Spielfeldes.\n    console : gamegridp.Console\n        Die Konsole unterhalb des Spielfeldes.\n    is_running : bool\n        Bestimmt, ob Act() in jedem Durchlauf der Mainloop ausgeführt wird.\n    speed: int\n        Die Geschwindigkeit mit der das Spiel läuft (bisher nur als Max. Geschwindigkeit definiert)\n    rows : int\n        Die Anzahl der Zeilen.\n    columns : int\n        Die Anzahl der Spalten.\n    '

    def __init__(self, title, cell_size=32, columns=8, rows=8, margin=0, background_color=(255, 255, 255), cell_color=(0, 0, 0), img_path=None, img_action='upscale', speed=60, toolbar=False, console=False, actionbar=True):
        self.__is_setting_up__ = False
        self.title = title
        self._logging = logging.getLogger('GameGrid')
        self._GameGrid__done = False
        self._grid = []
        self._info = False
        self._actors = pygame.sprite.LayeredDirty()
        self._collision_partners = pygame.sprite.Group()
        self._current_colliding_actors_pairs = []
        self._frame = 0
        self._tick = 0
        self._resolution = ()
        self._running = False
        self.effects = set()
        self._cell_margin = 0
        self._collision_type = 'cell'
        self._cell_transparency = 0
        self._clock = None
        self._grid_rows = 0
        self._grid_columns = 0
        self._background_color = (255, 255, 255)
        self._cell_color = (0, 0, 0)
        self._repaint_areas = []
        self._key_pressed = False
        self._key = 0
        self._speed = speed
        self._animated = False
        self._show_bounding_boxes = False
        self._show_direction_marker = False
        self.images_dict = {}
        self.screen_surface = pygame.display.get_surface()
        self.dirty = 1
        self._cell_size = cell_size
        if self.cell_size == 1:
            self._collision_type = 'bounding_box'
        else:
            self._collision_type = 'bounding_box'
        if cell_size == 1:
            self._type = 'pixel'
        else:
            self._type = 'cell'
        if toolbar is True:
            self.toolbar = gamegrid_toolbar.Toolbar(self)
        else:
            self.toolbar = None
        if actionbar is True:
            self.actionbar = gamegrid_actionbar.Actionbar(self)
        else:
            self.actionbar = None
        if console is True:
            self.console = gamegrid_console.Console(self, 5)
        else:
            self.console = None
        self._cell_margin = margin
        self._grid_columns = columns
        self._grid_rows = rows
        self._background_color = background_color
        self._cell_color = cell_color
        for row in range(rows):
            self._grid.append([])
            for column in range(columns):
                self._grid[row].append(0)

        if self.toolbar is not None:
            _toolbar_width = self.toolbar.width
        else:
            _toolbar_width = 0
        if self.actionbar is not None:
            _actionbar_height = self.actionbar.height
        else:
            _actionbar_height = 0
        if self.console is not None:
            _console_height = self.console.height
        else:
            _console_height = 0
        x_res = self.grid_width_in_pixels + _toolbar_width
        y_res = self.grid_height_in_pixels + _actionbar_height + _console_height
        if self.toolbar is not None:
            self.toolbar.set_height(y_res)
            self.toolbar.set_posx(self.grid_width_in_pixels)
        if self.actionbar is not None:
            self.actionbar.set_width(x_res)
            self.actionbar.set_posy(self.grid_height_in_pixels)
        if self.console is not None:
            self.console.set_width(x_res)
            self.console.set_posy(self.grid_height_in_pixels + _actionbar_height)
        self._resolution = (
         x_res, y_res)
        WINDOW_SIZE = (self._resolution[0], self._resolution[1])
        self._logging.info('gamegrid.__init__(): Created windows of dimension: (' + str(self._resolution[0]) + ',' + str(self._resolution[1]) + ')')
        self.screen_surface = pygame.display.set_mode(WINDOW_SIZE)
        self.grid_surface = pygame.Surface((self.grid_width_in_pixels, self.grid_height_in_pixels))
        self.background = pygame.Surface((self.grid_width_in_pixels, self.grid_height_in_pixels))
        self.background.fill(self._cell_color)
        pygame.display.set_caption(title)
        self.screen_surface.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
        self.last_update = pygame.time.get_ticks()
        self._frame = 0
        pygame.init()
        self.set_image(img_path, img_action)
        self._setup()

    __actor_id__ = 0

    @property
    def is_running(self):
        return self._running

    @is_running.setter
    def is_running(self, value):
        self._running = value

    @property
    def cell_size(self):
        """die Größe der einzelne Zellen des Grids."""
        return self._cell_size

    @property
    def cell_margin(self):
        """
        returns the margin between cells
        """
        return self._cell_margin

    @cell_size.setter
    def cell_size(self, value: int):
        """ Sets the cell-size"""
        self._cell_size = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def rows(self):
        """
        returns the margin between cells
        """
        return self._grid_rows

    @property
    def columns(self):
        """
        returns the margin between cells
        """
        return self._grid_columns

    def schedule_repaint(self, rect):
        if rect not in self._repaint_areas:
            self._repaint_areas.append(rect)

    def set_image(self, img_path: str, img_action: str='upscale', size=None):
        """
        Setzt das Hintergrundbild des Grids

        :param img_path: Der Pfad zum Bild als relativer Dateipfad
        :param img_action: Die Aktion, die mit dem Bild durchgeführt werden soll (scale, upscale, fill, crop
        :param size: Die Größe auf die das Bild skaliert / zugeschnitten etc. werden soll
        """
        self._logging.info('gamegrid.set_image : Set new image with action:' + str(img_action) + ' and path:' + str(img_path))
        if img_path is not None:
            self.background = pygame.image.load(img_path).convert()
            self._cell_transparency = 0
            if img_path is not None:
                if img_action == 'scale':
                    if size is None:
                        self.background = pygame.transform.scale(self.background, (
                         self.grid_width_in_pixels,
                         self.grid_height_in_pixels))
                    else:
                        self.background = pygame.transform.scale(self.background, (size[0], size[1]))
                    self.background = pygame.transform.scale(self.background, (self.grid_width_in_pixels, self.grid_height_in_pixels))
            if img_path is not None:
                if img_action == 'upscale':
                    if self.background.get_width() < self.grid_width_in_pixels or self.background.get_height() < self.grid_height_in_pixels:
                        self.background = pygame.transform.scale(self.background, (self.grid_width_in_pixels, self.grid_height_in_pixels))
            if img_path is not None and img_action == 'fill':
                if size is None:
                    self.background = pygame.transform.scale(self.background, (
                     self.cell_size, self.cell_size))
                else:
                    self.background = pygame.transform.scale(self.background, (size[0], size[1]))
                i = 0
                j = 0
                surface = pygame.Surface((self.grid_width_in_pixels, self.grid_height_in_pixels))
                while i < self.grid_width_in_pixels:
                    j = 0
                    while j < self.grid_height_in_pixels:
                        surface.blit(self.background, (i, j), (0, 0, self.background.get_width(),
                         self.background.get_height()))
                        j = j + self.background.get_height() + self.cell_margin

                    i = i + self.background.get_width() + self.cell_margin

                self.background = surface
        else:
            self._cell_transparency = None
            self.backround = pygame.Surface((self.grid_width_in_pixels, self.grid_height_in_pixels))
        cropped_surface = pygame.Surface((self.grid_width_in_pixels, self.grid_height_in_pixels))
        cropped_surface.fill((255, 255, 255))
        cropped_surface.blit(self.background, (0, 0), (
         0, 0, self.grid_width_in_pixels, self.grid_height_in_pixels))
        self.background = cropped_surface
        if self._cell_margin > 0:
            i = 0
            while i <= self.grid_width_in_pixels:
                pygame.draw.rect(self.background, self._background_color, [
                 i, 0, self._cell_margin, self.grid_height_in_pixels])
                i += self.cell_size + self._cell_margin

            i = 0
            while i <= self.grid_height_in_pixels:
                pygame.draw.rect(self.background, self._background_color, [
                 0, i, self.grid_width_in_pixels, self._cell_margin])
                i += self.cell_size + self._cell_margin

        self.actors.clear(self.grid_surface, self.background)

    def act(self):
        """
        Überschreibe diese Methode in deinen Kind-Klassen
        """
        pass

    def add_actor(self, actor, location=None):
        """
        Fügt einen Actor zum Grid hinzu

        Parameters
        ----------
        actor : gamegridp.Actor
            Der Actor, der hinzugefügt werden soll
        location :
            Der Ort, an dem der Actor hinzugefügt werden soll.

        """
        self._actors.add(actor)
        actor.dirty = 1
        if location is not None:
            actor.location = location
            actor.actor_id = self.__actor_id__
            self.__actor_id__ = self.__actor_id__ + 1

    def _update_actor(self, actor, attribute, value):
        """
        Wird aufgerufen, wenn ein Actor eine Aktualisierung des Grids anfordert
        (Beispiel: Umstellen der Eigenschaft is_static)
        Parameters
        ----------
        actor

        Returns
        -------

        """
        pass

    def __act_all(self):
        for actor in self._actors:
            actor.act()

        self.act()

    def draw(self):
        """
        draws the entire window with grid, actionbar and toolbar
        :return:
        """
        self.actors.update()
        if self.dirty:
            self._repaint_areas.append(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))
            for actor in self.actors:
                actor.dirty = 1

            self.dirty = 0
        self._repaint_areas.extend(self.actors.draw(self.grid_surface))
        self._GameGrid__draw_grid()
        self._GameGrid__draw_actionbar()
        self._GameGrid__draw_toolbar()
        self._GameGrid__draw_console()
        pygame.display.update(self._repaint_areas)
        self._repaint_areas = []

    def __draw_grid(self):
        self.screen_surface.blit(self.grid_surface, (0, 0, self.grid_surface.get_width(), self.grid_surface.get_height()))
        for actor in self._actors:
            actor._next_sprite()

    def __draw_toolbar(self):
        if self.toolbar is not None:
            self.toolbar.draw()

    def __draw_console(self):
        if self.console is not None:
            self.console.draw()

    def __draw_actionbar(self):
        if self.actionbar is not None:
            self.actionbar.draw()

    @property
    def actors(self):
        """
        returns all actors in grid
        :return: a list of all actors
        """
        return self._actors

    @property
    def frame(self) -> int:
        """
        Returns the actual frame
        :return: the value of actual frame
        """
        return self._frame

    @property
    def grid_width_in_pixels(self) -> int:
        """ returns the grid with in pixes
        :return: The grid_width in pixels
        """
        return self._grid_columns * self.cell_size + (self._grid_columns + 1) * self._cell_margin

    @property
    def grid_height_in_pixels(self) -> int:
        """ returns the grid-height in pixels"""
        height = self._grid_rows * self.cell_size + (self._grid_rows + 1) * self._cell_margin
        return height

    def grid_dimensions_in_pixels(self) -> tuple:
        """
        Returns the grid-dimension in pixesls
        :return:
        """
        return (
         self.grid_width_in_pixels, self.grid_height_in_pixels)

    def is_at_left_border(self, rect) -> bool:
        """
        Überprüfe, ob das Rechteck über den linken Rand hinausragt

        :param rect:
        :return: True, falls Ja, ansonsten False
        """
        if rect.topleft[0] <= 0:
            return True
        else:
            return False

    def is_at_bottom_border(self, rect):
        """
        Überprüfe, ob das Rechteck über den unteren Rand hinausragt

        :param rect:
        :return: True, falls Ja, ansonsten False
        """
        if rect.topleft[1] + rect.height >= self.grid_height_in_pixels:
            return True
        else:
            return False

    def is_at_right_border(self, rect):
        """
        Überprüfe, ob das Rechteck über den rechten Rand hinausragt

        :param rect:
        :return: True, falls Ja, ansonsten False
        """
        if rect.topleft[0] + rect.width >= self.grid_width_in_pixels:
            return True
        else:
            return False

    def is_at_top_border(self, rect):
        """
        Überprüfe, ob das Rechteck über den oberen Rand hinausragt

        :param rect:
        :return: True, falls Ja, ansonsten False
        """
        if rect.topleft[1] <= 0:
            return True
        else:
            return False

    def is_rectangle_in_grid(self, rect) -> bool:
        """
        Überprüfe, ob das Rechteck komplett im Grid ist.

        :param rect: Ein Rechteck
        :return: True, falls Ja, ansonsten False
        """
        if rect.topleft[0] < 0 or rect.topleft[1] < 0 or rect.topleft[0] + rect.width > self.grid_width_in_pixels or rect.topleft[1] + rect.height > self.grid_height_in_pixels:
            self._logging.debug('is_rectangle_in_grid() : false)')
            return False
        else:
            self._logging.debug('is_rectangle_in_grid() : true)')
            return True

    def is_empty_cell(self, cell: tuple) -> bool:
        """
        Überprüfe, ob eine Zelle leer ist.

        :param cell: Die Zellenkoordinaten als Tupel (x,y)
        :return: True, falls Ja, ansonsten False
        """
        if not self.get_all_actors_at_location(cell):
            return True
        else:
            return False

    def __listen--- This code section failed: ---

 L. 505         0  LOAD_FAST                'self'
                2  LOAD_ATTR                __is_setting_up__
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L. 506         6  LOAD_CONST               None
                8  RETURN_END_IF    
             10_0  COME_FROM             4  '4'

 L. 507        10  LOAD_CONST               False
               12  STORE_FAST               'key_pressed'

 L. 508        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _logging
               18  LOAD_ATTR                debug
               20  LOAD_STR                 'gamegrid.__listen__() : Listen...'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  POP_TOP          

 L. 509        26  LOAD_CONST               False
               28  STORE_FAST               'do_act'

 L. 510        30  SETUP_LOOP         1106  'to 1106'
               34  LOAD_GLOBAL              pygame
               36  LOAD_ATTR                event
               38  LOAD_ATTR                get
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  GET_ITER         
               44  FOR_ITER           1104  'to 1104'
               48  STORE_FAST               'event'

 L. 511        50  LOAD_CONST               False
               52  STORE_FAST               'key'

 L. 512        54  LOAD_CONST               False
               56  STORE_FAST               'cell'

 L. 514        58  LOAD_FAST                'event'
               60  LOAD_ATTR                type
               62  LOAD_GLOBAL              pygame
               64  LOAD_ATTR                QUIT
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE    96  'to 96'

 L. 515        70  LOAD_CONST               True
               72  LOAD_FAST                'self'
               74  STORE_ATTR               _GameGrid__done

 L. 516        76  LOAD_GLOBAL              pygame
               78  LOAD_ATTR                quit
               80  CALL_FUNCTION_0       0  '0 positional arguments'
               82  POP_TOP          

 L. 517        84  LOAD_GLOBAL              os
               86  LOAD_ATTR                _exit
               88  LOAD_CONST               0
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  POP_TOP          
               94  JUMP_BACK            44  'to 44'
               96  ELSE                     '1102'

 L. 519        96  LOAD_FAST                'event'
               98  LOAD_ATTR                type
              100  LOAD_GLOBAL              pygame
              102  LOAD_ATTR                MOUSEBUTTONDOWN
              104  COMPARE_OP               ==
              106  POP_JUMP_IF_FALSE  1062  'to 1062'

 L. 520       110  LOAD_GLOBAL              pygame
              112  LOAD_ATTR                mouse
              114  LOAD_ATTR                get_pos
              116  CALL_FUNCTION_0       0  '0 positional arguments'
              118  STORE_FAST               'pos'

 L. 521       120  LOAD_FAST                'self'
              122  LOAD_ATTR                _logging
              124  LOAD_ATTR                debug
              126  LOAD_STR                 'gamegrid.__listen__(): Mouseclick with button:'
              128  LOAD_GLOBAL              str
              130  LOAD_FAST                'event'
              132  LOAD_ATTR                button
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  BINARY_ADD       
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  POP_TOP          

 L. 523       142  LOAD_FAST                'pos'
              144  LOAD_CONST               0
              146  BINARY_SUBSCR    
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                grid_width_in_pixels
              152  COMPARE_OP               <
              154  JUMP_IF_FALSE_OR_POP   178  'to 178'
              156  LOAD_FAST                'pos'

 L. 524       158  LOAD_CONST               1
              160  BINARY_SUBSCR    
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                grid_height_in_pixels
              166  COMPARE_OP               <
              168  JUMP_IF_FALSE_OR_POP   178  'to 178'
              170  LOAD_FAST                'event'
              172  LOAD_ATTR                button
              174  LOAD_CONST               1
              176  COMPARE_OP               ==
            178_0  COME_FROM           168  '168'
            178_1  COME_FROM           154  '154'
              178  POP_JUMP_IF_FALSE   272  'to 272'

 L. 525       182  LOAD_FAST                'self'
              184  LOAD_ATTR                _GameGrid__pixel_to_cell
              186  LOAD_FAST                'pos'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  STORE_FAST               'cell_location'

 L. 526       192  LOAD_FAST                'self'
              194  LOAD_ATTR                _logging
              196  LOAD_ATTR                debug
              198  LOAD_STR                 'gamegrid.__listen__() : '
              200  LOAD_GLOBAL              str
              202  LOAD_FAST                'cell_location'
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  BINARY_ADD       
              208  CALL_FUNCTION_1       1  '1 positional argument'
              210  POP_TOP          

 L. 527       212  LOAD_FAST                'cell_location'
              214  LOAD_CONST               0
              216  BINARY_SUBSCR    
              218  STORE_FAST               'column'

 L. 528       220  LOAD_FAST                'cell_location'
              222  LOAD_CONST               1
              224  BINARY_SUBSCR    
              226  STORE_FAST               'row'

 L. 529       228  LOAD_FAST                'column'
              230  LOAD_FAST                'row'
              232  BUILD_TUPLE_2         2 
              234  STORE_FAST               'cell_clicked'

 L. 530       236  LOAD_FAST                'self'
              238  LOAD_ATTR                _GameGrid__listen_all
              240  LOAD_STR                 'mouse_left'
              242  LOAD_FAST                'cell_location'
              244  CALL_FUNCTION_2       2  '2 positional arguments'
              246  POP_TOP          

 L. 531       248  LOAD_FAST                'self'
              250  LOAD_ATTR                _logging
              252  LOAD_ATTR                debug
              254  LOAD_STR                 'gamegrid.__listen__(): Mouseclick left at grid-position:'

 L. 532       256  LOAD_GLOBAL              str
              258  LOAD_FAST                'cell_clicked'
              260  CALL_FUNCTION_1       1  '1 positional argument'
              262  BINARY_ADD       
              264  CALL_FUNCTION_1       1  '1 positional argument'
              266  POP_TOP          
              268  JUMP_ABSOLUTE      1102  'to 1102'
              272  ELSE                     '1060'

 L. 533       272  LOAD_FAST                'pos'
              274  LOAD_CONST               0
              276  BINARY_SUBSCR    
              278  LOAD_FAST                'self'
              280  LOAD_ATTR                grid_width_in_pixels
              282  COMPARE_OP               <
              284  POP_JUMP_IF_FALSE   406  'to 406'
              288  LOAD_FAST                'pos'

 L. 534       290  LOAD_CONST               1
              292  BINARY_SUBSCR    
              294  LOAD_FAST                'self'
              296  LOAD_ATTR                grid_height_in_pixels
              298  COMPARE_OP               <
              300  POP_JUMP_IF_FALSE   406  'to 406'
              304  LOAD_FAST                'event'
              306  LOAD_ATTR                button
              308  LOAD_CONST               3
              310  COMPARE_OP               ==
              312  POP_JUMP_IF_FALSE   406  'to 406'

 L. 535       316  LOAD_FAST                'self'
              318  LOAD_ATTR                _GameGrid__pixel_to_cell
              320  LOAD_FAST                'pos'
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  STORE_FAST               'cell_location'

 L. 536       326  LOAD_FAST                'self'
              328  LOAD_ATTR                _logging
              330  LOAD_ATTR                debug
              332  LOAD_STR                 'gamegrid.__listen__() : '
              334  LOAD_GLOBAL              str
              336  LOAD_FAST                'cell_location'
              338  CALL_FUNCTION_1       1  '1 positional argument'
              340  BINARY_ADD       
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  POP_TOP          

 L. 537       346  LOAD_FAST                'cell_location'
              348  LOAD_CONST               0
              350  BINARY_SUBSCR    
              352  STORE_FAST               'column'

 L. 538       354  LOAD_FAST                'cell_location'
              356  LOAD_CONST               1
              358  BINARY_SUBSCR    
              360  STORE_FAST               'row'

 L. 539       362  LOAD_FAST                'column'
              364  LOAD_FAST                'row'
              366  BUILD_TUPLE_2         2 
              368  STORE_FAST               'cell_clicked'

 L. 540       370  LOAD_FAST                'self'
              372  LOAD_ATTR                _logging
              374  LOAD_ATTR                info
              376  LOAD_STR                 'gamegrid.__listen__(): - Mouseclick right at grid-position:'

 L. 541       378  LOAD_GLOBAL              str
              380  LOAD_FAST                'cell_clicked'
              382  CALL_FUNCTION_1       1  '1 positional argument'
              384  BINARY_ADD       
              386  CALL_FUNCTION_1       1  '1 positional argument'
              388  POP_TOP          

 L. 542       390  LOAD_FAST                'self'
              392  LOAD_ATTR                _GameGrid__listen_all
              394  LOAD_STR                 'mouse_right'
              396  LOAD_FAST                'cell_location'
              398  CALL_FUNCTION_2       2  '2 positional arguments'
              400  POP_TOP          
              402  JUMP_ABSOLUTE      1102  'to 1102'
            406_0  COME_FROM           300  '300'
            406_1  COME_FROM           284  '284'

 L. 544       406  LOAD_FAST                'pos'
              408  LOAD_CONST               1
              410  BINARY_SUBSCR    
              412  LOAD_FAST                'self'
              414  LOAD_ATTR                grid_height_in_pixels
              416  COMPARE_OP               >=
              418  POP_JUMP_IF_FALSE   990  'to 990'

 L. 545       422  LOAD_CONST               1
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                actionbar
              428  STORE_ATTR               dirty

 L. 546       430  LOAD_FAST                'pos'
              432  LOAD_CONST               0
              434  BINARY_SUBSCR    
              436  LOAD_CONST               5
              438  COMPARE_OP               >
              440  POP_JUMP_IF_FALSE   486  'to 486'
              444  LOAD_FAST                'pos'
              446  LOAD_CONST               0
              448  BINARY_SUBSCR    
              450  LOAD_CONST               60
              452  COMPARE_OP               <
              454  POP_JUMP_IF_FALSE   486  'to 486'

 L. 547       458  LOAD_FAST                'self'
              460  LOAD_ATTR                _running
              462  POP_JUMP_IF_TRUE    988  'to 988'

 L. 548       466  LOAD_FAST                'self'
              468  LOAD_ATTR                _logging
              470  LOAD_ATTR                debug
              472  LOAD_STR                 'gamegrid.__listen__(): : Act'
              474  CALL_FUNCTION_1       1  '1 positional argument'
              476  POP_TOP          

 L. 549       478  LOAD_CONST               True
              480  RETURN_END_IF    
            482_0  COME_FROM           462  '462'
              482  JUMP_ABSOLUTE      1060  'to 1060'
            486_0  COME_FROM           440  '440'

 L. 550       486  LOAD_FAST                'pos'
              488  LOAD_CONST               1
              490  BINARY_SUBSCR    
              492  LOAD_FAST                'self'
              494  LOAD_ATTR                grid_height_in_pixels
              496  COMPARE_OP               >=
              498  POP_JUMP_IF_FALSE   562  'to 562'
              502  LOAD_FAST                'pos'
              504  LOAD_CONST               0
              506  BINARY_SUBSCR    
              508  LOAD_CONST               60
              510  COMPARE_OP               >
              512  POP_JUMP_IF_FALSE   562  'to 562'
              516  LOAD_FAST                'pos'

 L. 551       518  LOAD_CONST               0
              520  BINARY_SUBSCR    
              522  LOAD_CONST               120
              524  COMPARE_OP               <
              526  POP_JUMP_IF_FALSE   562  'to 562'
              530  LOAD_FAST                'self'
              532  LOAD_ATTR                _running
              534  UNARY_NOT        
              536  POP_JUMP_IF_FALSE   562  'to 562'

 L. 552       540  LOAD_CONST               True
              542  LOAD_FAST                'self'
              544  STORE_ATTR               _running

 L. 553       546  LOAD_FAST                'self'
              548  LOAD_ATTR                _logging
              550  LOAD_ATTR                debug
              552  LOAD_STR                 'gamegrid.__listen__(): : Play'
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  POP_TOP          
              558  JUMP_ABSOLUTE      1060  'to 1060'
            562_0  COME_FROM           526  '526'
            562_1  COME_FROM           512  '512'
            562_2  COME_FROM           498  '498'

 L. 554       562  LOAD_FAST                'pos'
              564  LOAD_CONST               1
              566  BINARY_SUBSCR    
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                grid_height_in_pixels
              572  COMPARE_OP               >=
              574  POP_JUMP_IF_FALSE   636  'to 636'
              578  LOAD_FAST                'pos'
              580  LOAD_CONST               0
              582  BINARY_SUBSCR    
              584  LOAD_CONST               60
              586  COMPARE_OP               >
              588  POP_JUMP_IF_FALSE   636  'to 636'
              592  LOAD_FAST                'pos'
              594  LOAD_CONST               0
              596  BINARY_SUBSCR    
              598  LOAD_CONST               120
              600  COMPARE_OP               <
              602  POP_JUMP_IF_FALSE   636  'to 636'
              606  LOAD_FAST                'self'
              608  LOAD_ATTR                _running
              610  POP_JUMP_IF_FALSE   636  'to 636'

 L. 555       614  LOAD_CONST               False
              616  LOAD_FAST                'self'
              618  STORE_ATTR               _running

 L. 556       620  LOAD_FAST                'self'
              622  LOAD_ATTR                _logging
              624  LOAD_ATTR                debug
              626  LOAD_STR                 'gamegrid.__listen__() : Pause'
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  POP_TOP          
              632  JUMP_ABSOLUTE      1060  'to 1060'
            636_0  COME_FROM           602  '602'
            636_1  COME_FROM           588  '588'
            636_2  COME_FROM           574  '574'

 L. 557       636  LOAD_FAST                'pos'
              638  LOAD_CONST               1
              640  BINARY_SUBSCR    
              642  LOAD_FAST                'self'
              644  LOAD_ATTR                grid_height_in_pixels
              646  COMPARE_OP               >=
              648  POP_JUMP_IF_FALSE   710  'to 710'
              652  LOAD_FAST                'pos'
              654  LOAD_CONST               0
              656  BINARY_SUBSCR    
              658  LOAD_CONST               120
              660  COMPARE_OP               >
              662  POP_JUMP_IF_FALSE   710  'to 710'
              666  LOAD_FAST                'pos'
              668  LOAD_CONST               0
              670  BINARY_SUBSCR    
              672  LOAD_CONST               220
              674  COMPARE_OP               <
              676  POP_JUMP_IF_FALSE   710  'to 710'

 L. 558       680  LOAD_FAST                'self'
              682  LOAD_ATTR                _logging
              684  LOAD_ATTR                debug
              686  LOAD_STR                 'gamegrid.__listen__() : Reset'
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  POP_TOP          

 L. 559       692  LOAD_CONST               False
              694  LOAD_FAST                'self'
              696  STORE_ATTR               _running

 L. 560       698  LOAD_FAST                'self'
              700  LOAD_ATTR                reset
              702  CALL_FUNCTION_0       0  '0 positional arguments'
              704  POP_TOP          
              706  JUMP_ABSOLUTE      1060  'to 1060'
            710_0  COME_FROM           662  '662'
            710_1  COME_FROM           648  '648'

 L. 561       710  LOAD_FAST                'pos'
              712  LOAD_CONST               1
              714  BINARY_SUBSCR    
              716  LOAD_FAST                'self'
              718  LOAD_ATTR                grid_height_in_pixels
              720  COMPARE_OP               >=
              722  POP_JUMP_IF_FALSE   850  'to 850'
              726  LOAD_FAST                'pos'
              728  LOAD_CONST               0
              730  BINARY_SUBSCR    
              732  LOAD_CONST               220
              734  COMPARE_OP               >
              736  POP_JUMP_IF_FALSE   850  'to 850'
              740  LOAD_FAST                'pos'
              742  LOAD_CONST               0
              744  BINARY_SUBSCR    
              746  LOAD_CONST               280
              748  COMPARE_OP               <
              750  POP_JUMP_IF_FALSE   850  'to 850'

 L. 562       754  LOAD_FAST                'self'
              756  LOAD_ATTR                _logging
              758  LOAD_ATTR                debug
              760  LOAD_STR                 'gamegrid.__listen__() : Info'
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  POP_TOP          

 L. 563       766  LOAD_FAST                'self'
              768  LOAD_ATTR                _info
              770  LOAD_CONST               True
              772  COMPARE_OP               ==
              774  POP_JUMP_IF_FALSE   812  'to 812'

 L. 564       778  LOAD_CONST               False
              780  LOAD_FAST                'self'
              782  STORE_ATTR               _show_bounding_boxes

 L. 565       784  LOAD_CONST               False
              786  LOAD_FAST                'self'
              788  STORE_ATTR               _show_direction_marker

 L. 566       790  LOAD_CONST               False
              792  LOAD_FAST                'self'
              794  STORE_ATTR               _info

 L. 567       796  LOAD_CONST               1
              798  LOAD_FAST                'self'
              800  STORE_ATTR               dirty

 L. 568       802  LOAD_CONST               1
              804  LOAD_FAST                'self'
              806  LOAD_ATTR                actionbar
              808  STORE_ATTR               dirty
              810  JUMP_FORWARD        848  'to 848'
              812  ELSE                     '848'

 L. 569       812  LOAD_FAST                'self'
              814  LOAD_ATTR                _info
              816  LOAD_CONST               False
              818  COMPARE_OP               ==
              820  POP_JUMP_IF_FALSE   988  'to 988'

 L. 570       824  LOAD_CONST               True
              826  LOAD_FAST                'self'
              828  STORE_ATTR               _show_bounding_boxes

 L. 571       830  LOAD_CONST               True
              832  LOAD_FAST                'self'
              834  STORE_ATTR               _show_direction_marker

 L. 572       836  LOAD_CONST               1
              838  LOAD_FAST                'self'
              840  STORE_ATTR               dirty

 L. 573       842  LOAD_CONST               True
              844  LOAD_FAST                'self'
              846  STORE_ATTR               _info
            848_0  COME_FROM           810  '810'
              848  JUMP_FORWARD        988  'to 988'
            850_0  COME_FROM           736  '736'
            850_1  COME_FROM           722  '722'

 L. 574       850  LOAD_FAST                'pos'
              852  LOAD_CONST               1
              854  BINARY_SUBSCR    
              856  LOAD_FAST                'self'
              858  LOAD_ATTR                grid_height_in_pixels
              860  COMPARE_OP               >=
              862  POP_JUMP_IF_FALSE   920  'to 920'
              866  LOAD_FAST                'pos'
              868  LOAD_CONST               0
              870  BINARY_SUBSCR    
              872  LOAD_CONST               285
              874  COMPARE_OP               >
              876  POP_JUMP_IF_FALSE   920  'to 920'
              880  LOAD_FAST                'pos'
              882  LOAD_CONST               0
              884  BINARY_SUBSCR    
              886  LOAD_CONST               345
              888  COMPARE_OP               <
              890  POP_JUMP_IF_FALSE   920  'to 920'

 L. 575       894  LOAD_FAST                'self'
              896  LOAD_ATTR                speed
              898  LOAD_CONST               0
              900  COMPARE_OP               >
              902  POP_JUMP_IF_FALSE   988  'to 988'

 L. 576       906  LOAD_FAST                'self'
              908  LOAD_ATTR                speed
              910  LOAD_CONST               1
              912  BINARY_SUBTRACT  
              914  LOAD_FAST                'self'
              916  STORE_ATTR               speed
              918  JUMP_FORWARD        988  'to 988'
            920_0  COME_FROM           876  '876'
            920_1  COME_FROM           862  '862'

 L. 577       920  LOAD_FAST                'pos'
              922  LOAD_CONST               1
              924  BINARY_SUBSCR    
              926  LOAD_FAST                'self'
              928  LOAD_ATTR                grid_height_in_pixels
              930  COMPARE_OP               >=
              932  POP_JUMP_IF_FALSE  1060  'to 1060'
              936  LOAD_FAST                'pos'
              938  LOAD_CONST               0
              940  BINARY_SUBSCR    
              942  LOAD_CONST               345
              944  COMPARE_OP               >
              946  POP_JUMP_IF_FALSE  1060  'to 1060'
              950  LOAD_FAST                'pos'
              952  LOAD_CONST               0
              954  BINARY_SUBSCR    
              956  LOAD_CONST               395
              958  COMPARE_OP               <
              960  POP_JUMP_IF_FALSE  1060  'to 1060'

 L. 578       964  LOAD_FAST                'self'
              966  LOAD_ATTR                speed
              968  LOAD_CONST               60
              970  COMPARE_OP               <
              972  POP_JUMP_IF_FALSE  1060  'to 1060'

 L. 579       976  LOAD_FAST                'self'
              978  LOAD_ATTR                speed
              980  LOAD_CONST               1
              982  BINARY_ADD       
              984  LOAD_FAST                'self'
              986  STORE_ATTR               speed
            988_0  COME_FROM           918  '918'
            988_1  COME_FROM           902  '902'
            988_2  COME_FROM           848  '848'
            988_3  COME_FROM           820  '820'
              988  JUMP_FORWARD       1060  'to 1060'
              990  ELSE                     '1060'

 L. 580       990  LOAD_FAST                'pos'
              992  LOAD_CONST               0
              994  BINARY_SUBSCR    
              996  LOAD_FAST                'self'
              998  LOAD_ATTR                grid_width_in_pixels
             1000  COMPARE_OP               >
             1002  POP_JUMP_IF_FALSE  1102  'to 1102'

 L. 581      1006  LOAD_FAST                'self'
             1008  LOAD_ATTR                toolbar
             1010  LOAD_ATTR                listen
             1012  LOAD_STR                 'mouse_left'
             1014  LOAD_FAST                'pos'
             1016  LOAD_CONST               0
             1018  BINARY_SUBSCR    
             1020  LOAD_FAST                'pos'
             1022  LOAD_CONST               1
             1024  BINARY_SUBSCR    
             1026  BUILD_TUPLE_2         2 
             1028  LOAD_CONST               ('position',)
             1030  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1032  STORE_FAST               'toolbar_event'

 L. 582      1034  LOAD_FAST                'toolbar_event'
             1036  POP_JUMP_IF_FALSE  1102  'to 1102'

 L. 583      1040  LOAD_FAST                'self'
             1042  LOAD_ATTR                _GameGrid__listen_all
             1044  LOAD_FAST                'toolbar_event'
             1046  LOAD_CONST               0
             1048  BINARY_SUBSCR    
             1050  LOAD_FAST                'toolbar_event'
             1052  LOAD_CONST               1
             1054  BINARY_SUBSCR    
             1056  CALL_FUNCTION_2       2  '2 positional arguments'
             1058  POP_TOP          
           1060_0  COME_FROM           988  '988'
           1060_1  COME_FROM           972  '972'
           1060_2  COME_FROM           960  '960'
           1060_3  COME_FROM           946  '946'
           1060_4  COME_FROM           932  '932'
             1060  JUMP_BACK            44  'to 44'
             1062  ELSE                     '1102'

 L. 584      1062  LOAD_FAST                'event'
             1064  LOAD_ATTR                type
             1066  LOAD_GLOBAL              pygame
             1068  LOAD_ATTR                KEYDOWN
             1070  COMPARE_OP               ==
             1072  POP_JUMP_IF_FALSE    44  'to 44'

 L. 585      1074  LOAD_GLOBAL              pygame
             1076  LOAD_ATTR                key
             1078  LOAD_ATTR                get_pressed
             1080  CALL_FUNCTION_0       0  '0 positional arguments'
             1082  STORE_FAST               'keys_pressed'

 L. 586      1084  LOAD_FAST                'self'
             1086  LOAD_ATTR                _GameGrid__listen_all
             1088  LOAD_STR                 'key_down'
             1090  LOAD_GLOBAL              keys
             1092  LOAD_ATTR                key_pressed_to_key
             1094  LOAD_FAST                'keys_pressed'
             1096  CALL_FUNCTION_1       1  '1 positional argument'
             1098  CALL_FUNCTION_2       2  '2 positional arguments'
             1100  POP_TOP          
           1102_0  COME_FROM          1036  '1036'
           1102_1  COME_FROM          1002  '1002'
             1102  JUMP_BACK            44  'to 44'
             1104  POP_BLOCK        
           1106_0  COME_FROM_LOOP       30  '30'

 L. 587      1106  LOAD_GLOBAL              pygame
             1108  LOAD_ATTR                key
             1110  LOAD_ATTR                get_pressed
             1112  CALL_FUNCTION_0       0  '0 positional arguments'
             1114  LOAD_ATTR                count
             1116  LOAD_CONST               1
             1118  CALL_FUNCTION_1       1  '1 positional argument'
             1120  LOAD_CONST               0
             1122  COMPARE_OP               !=
             1124  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 588      1128  LOAD_GLOBAL              pygame
             1130  LOAD_ATTR                key
             1132  LOAD_ATTR                get_pressed
             1134  CALL_FUNCTION_0       0  '0 positional arguments'
             1136  STORE_FAST               'keys_pressed'

 L. 589      1138  LOAD_FAST                'self'
             1140  LOAD_ATTR                _GameGrid__listen_all
             1142  LOAD_STR                 'key'
             1144  LOAD_GLOBAL              keys
             1146  LOAD_ATTR                key_pressed_to_key
             1148  LOAD_FAST                'keys_pressed'
             1150  CALL_FUNCTION_1       1  '1 positional argument'
             1152  CALL_FUNCTION_2       2  '2 positional arguments'
             1154  POP_TOP          

 L. 590      1156  LOAD_FAST                'self'
             1158  LOAD_ATTR                _GameGrid__listen_all
             1160  LOAD_STR                 'key_pressed'
             1162  LOAD_GLOBAL              keys
             1164  LOAD_ATTR                key_pressed_to_key
             1166  LOAD_FAST                'keys_pressed'
             1168  CALL_FUNCTION_1       1  '1 positional argument'
             1170  CALL_FUNCTION_2       2  '2 positional arguments'
             1172  POP_TOP          
           1174_0  COME_FROM          1124  '1124'

 L. 591      1174  LOAD_GLOBAL              pygame
             1176  LOAD_ATTR                mouse
             1178  LOAD_ATTR                get_pos
             1180  CALL_FUNCTION_0       0  '0 positional arguments'
             1182  UNPACK_SEQUENCE_2     2 
             1184  STORE_FAST               'mouse_x'
             1186  STORE_FAST               'mouse_y'

 L. 592      1188  LOAD_FAST                'mouse_x'
             1190  LOAD_FAST                'self'
             1192  LOAD_ATTR                grid_width_in_pixels
             1194  COMPARE_OP               >
             1196  POP_JUMP_IF_FALSE  1220  'to 1220'

 L. 593      1200  LOAD_FAST                'self'
             1202  LOAD_ATTR                toolbar
             1204  LOAD_ATTR                listen
             1206  LOAD_STR                 'mouse_hover'
             1208  LOAD_FAST                'mouse_x'
             1210  LOAD_FAST                'mouse_y'
             1212  BUILD_TUPLE_2         2 
             1214  LOAD_CONST               ('position',)
             1216  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1218  STORE_FAST               'toolbar_event'
           1220_0  COME_FROM          1196  '1196'

 L. 595      1220  LOAD_CONST               False
             1222  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 482

    def __listen_all(self, event: str=None, data=None):
        """ Calls listen of grid and all actors """
        self.listen(event, data)
        for actor in self._actors:
            actor.listen(event, data)

    def listen(self, event: str=None, data=None):
        """
        Überschreibe diese Methode in deiner Kind-Klasse

        :param event: Das Event, welches getriggert wurde. Mögliche Events:
            * mousedown
            * key_pressed / key - Eine taste wird gedrückt (gehalten)
            * key_down - Eine Taste wird gerade heruntergedrückt
            * button_name Falls ein Button geklickt wurde.
        :param data: Zusätzliche Infos, wie z.B. die gedrückten Tasten oder
            die Koordinaten der Maus.
        """
        pass

    def collision(self, partner1, partner2):
        """
        Überschreibe diese Methoden, wenn du Kollisionen handhaben möchtest.
        """
        pass

    def _call_collisions(self):
        """
        Wird aus update() heraus aufgerufen.
        Erstellt alle Kollisionspaare mit Hilfe von
          * self.get_all_bounding_box_collisions
        """
        colliding_actors_pairs = []
        checked = []
        for actor in self.actors:
            if actor._collision_partners:
                colliding_actors = self.get_all_collisions_for_actor(actor)
                if colliding_actors:
                    for colliding_actor in colliding_actors:
                        if actor not in checked:
                            pair, reversed = (
                             actor, colliding_actor), (colliding_actor, actor)
                            if pair not in self._current_colliding_actors_pairs:
                                if reversed not in self._current_colliding_actors_pairs:
                                    self.collision(actor, colliding_actor)
                                    self.listen('collision', pair)
                            colliding_actors_pairs.append(pair)
                        checked.append(actor)

            self._logging.debug('gamegrid.__collision__() - 1collision-actors:' + str(colliding_actors_pairs) + ', current_colliding:' + str(self._current_colliding_actors_pairs))
            self._current_colliding_actors_pairs = list(set(self._current_colliding_actors_pairs) - (set(self._current_colliding_actors_pairs) - set(colliding_actors_pairs)))
            self._current_colliding_actors_pairs = list(set(self._current_colliding_actors_pairs).union(set(colliding_actors_pairs)))
            self._logging.debug('gamegrid.__collision__() - 2collision-actors:' + str(colliding_actors_pairs) + ', current_colliding:' + str(self._current_colliding_actors_pairs))

    def get_all_collisions_for_actor(self, actor):
        """
        Gibt einen Actor zurück, dessen Bounding-Boxes mit dem angegebenen Akteur
        kollidieren.

        Parameters
        ----------
        actor Ein Actor vom angegebenen Klassennahmen, der mit dem angegebenen Actor kollidiert.
        class_name Den Klassennamen nach dem gefiltert werden soll.

        Returns
        -------

        """
        collision_actors = pygame.sprite.spritecollide(actor, actor._collision_partners, True)
        if actor in collision_actors:
            collision_actors.remove(actor)
        return collision_actors

    def get_all_bounding_box_collisions(self, actor, class_name: str=None):
        """
        Gibt alle Actors zurück, deren Bounding-Boxes mit dem angegebenen Akteur
        kollidieren.

        Parameters
        ----------
        actor
            Der Actor für den Kollisionen überprüft werden sollen.
        class_name : str
            Die Klasse nach der gefiltert werden soll.
            (z.B. Gebe nur Kollisionen mit Akteuren der Klasse "Wall" zurück.)

        Returns
        -------
        list(gamegrid.Actor)
            Alle Akeure, die mit dem aktuellen Akteur kollidieren
        """
        colliding_actors = []
        if class_name:
            pass
        for collision_partner in actor._collision_partners:
            if self.actors_are_colliding(actor, collision_partner):
                colliding_actors.append(collision_partner)

        return colliding_actors

    def actors_are_colliding(self, actor1, actor2) -> bool:
        """
        Überprüft, ob zwei Actors kollidieren

        Parameters
        ----------
        actor1 gamegrid.Actor
            Der erste Actor
        actor2 gamegrid.Actor
            Der zweite Actor

        Returns
        -------
        bool
            True, falls es eine Überschneidung gibt.

        """
        if actor1 is not actor2:
            if actor1.rect.colliderect(actor2.rect):
                self._logging.debug('gamegrid.collision_bounding_box: colliding')
                return True
            else:
                self._logging.debug('gamegrid.collision_bounding_box: not colliding')
                return False

    def __get_bounding_box_collisions__(self, actor):
        """
        .. deprecated:: 0.4.0
          `__get_bounding_box_collisions__` wird in GameGrid 0.5 ersetzt werden.
          `get_all_bounding_box_collisions` ist die (etwas mächtigere) Alternative.
        """
        for partner in actor.collision_partners:
            if self.actors_are_colliding(actor, partner):
                return partner

    def get_all_actors_at_location(self, location: tuple, class_name: str='') -> list:
        """
        Gebe alle Akteure an den angegebenen Zellenkoordinaten zurück
        .. deprecated:: 0.5.0
            Use sublass cellgrid instead

        :param location: Die Zellenkordinaten als Tupel (x,y)
        :param class_name: Den Klassennamen, nachdem gefiltert werden soll
        :return: Eine Liste aller Akteure (mit der angegebenen Klasse) an der Position.
        """
        actors_at_location = []
        for actor in self._actors:
            if actor.location == location and (class_name is '' or actor.__class__.__name__ == class_name):
                actors_at_location.append(actor)

        return actors_at_location

    def is_location_in_grid(self, location):
        """
        Gibt an, ob eine Zellenkoordinate im Grid liegt

        :param location: Die Zellenkoordinate als Tupel (x,y)
        :return: True falls Koordinate im Grid, ansonsten False
        """
        if location[0] > self._grid_columns - 1:
            return False
        else:
            if location[1] > self._grid_rows - 1:
                return False
            if location[0] < 0 or location[1] < 0:
                return False
            return True

    def update(self, no_logic: bool=False, no_drawing: bool=False):
        """ Part 1:
        For grid an all actors
        listen to events
        react with listen() method
        """
        if self.__is_setting_up__:
            no_logic = True
            no_drawing = True
        else:
            if not no_logic:
                do_act = self._GameGrid__listen()
            elif not no_logic:
                if self._running or do_act:
                    if not no_logic:
                        self._tick = self._tick + 1
                        if self._tick > 60 - self.speed:
                            self._GameGrid__act_all()
                            self._tick = 0
            else:
                self._logging.debug('gamegrid.update() - frame: ' + str(self.frame))
                if not no_logic:
                    self._call_collisions()
                if not no_drawing:
                    self.draw()
                    self._frame = self._frame + 1
                    if self._frame == 60:
                        self._frame = 0
            if not no_logic:
                self.clock.tick(60)

    def remove_actor(self, actor):
        """
        Entfernt einen Akteur aus dem Grid

        :param actor: Der zu entfernende Akteur
        :param cell: Entfernt alle Akteure an einer Zelle (actor wird dann ignoriert)
        :return:
        """
        if actor:
            self._actors.remove(actor)
            actor.__grid__ = None
            self._logging.info("Parameter actor can't be none (except cell is given)")

    @staticmethod
    def log():
        logging.basicConfig(stream=(sys.stdout), level=(logging.INFO))

    def remove_all_actors(self):
        """
        Entfernt alle Akteure aus dem Grid.
        """
        for actor in self._actors:
            self.remove_actor(actor)

    def reset(self):
        """
        Entfernt alle Akteure aus dem Grid und setzt sie an ihre Ursprungspositionen.
        """
        self.remove_all_actors()
        self._setup()

    def stop(self):
        """
        Stoppt die Ausführung (siehe auch run)
        """
        self._running = False

    def run(self):
        """
        Startet die Ausführung (equivalent zum Drücken des Run-Buttons).
        Wenn das Spiel läuft handeln die Akteure mit jedem Durchlauf der mainloop genau einmal.
        """
        self._running = True

    def show(self):
        """
        Startet das Programm.
        """
        self.update()
        while not self._GameGrid__done:
            self.update()

        pygame.quit()

    def _setup(self):
        self.__is_setting_up__ = True
        self.setup()
        self.__is_setting_up__ = False
        self.schedule_repaint(pygame.Rect(0, 0, self._resolution[0], self._resolution[1]))
        self.update(no_logic=True, no_drawing=True)

    def setup(self):
        """
        Sollte in deiner Kind-Klasse überschrieben werden.
        """
        pass

    def __pixel_to_cell(self, pos: tuple):
        """
        transforms a pixel-coordinate into a cell coordinate in grid
        :param pos: the position in pixels
        """
        column = (pos[0] - self._cell_margin) // (self.cell_size + self._cell_margin)
        row = (pos[1] - self._cell_margin) // (self.cell_size + self._cell_margin)
        return (column, row)

    def cell_rect(self, cell: tuple):
        """
        Gibt das Rechteck zurück, dass eine Zelle umschließt.
        """
        x = cell[0] * self.cell_size + cell[0] * self._cell_margin + self._cell_margin
        y = cell[1] * self.cell_size + cell[1] * self._cell_margin + self._cell_margin
        return pygame.Rect(x, y, self.cell_size, self.cell_size)

    def cell_to_pixel(self, cell: tuple):
        """
        Gibt die obere-linke Koordinate einer Zelle zurück.
        """
        x = cell[0] * self.cell_size + cell[0] * self._cell_margin + self._cell_margin
        y = cell[1] * self.cell_size + cell[1] * self._cell_margin + self._cell_margin
        return pygame.Rect(x, y, self.cell_size, self.cell_size)

    def play_sound(self, sound_path):
        """
        Spielt einen Sound

        :param sound_path: Der Pfad zum Sound relativ zum aktuellen Verzeichnis.
        """
        effect = pygame.mixer.Sound(sound_path)
        effect.play()

    def play_music(self, music_path):
        """
        Spielt eine Musik in Endlosschleife

        :param music_path: Der Pfad zur Musikdatei relativ zum aktuellen Verzeichnis.
        """
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    @property
    def type(self):
        return self._type


class DatabaseGrid(GameGrid):
    __doc__ = '\n    Ein Grid mit Datenbank-Anbindung.\n\n    Achtung: Die Funktionen müssen immer in folgender Reihenfolge ausgeführt werden:\n    connect\n    select/insert (beliebig viele)\n    commit\n    close\n    '

    def connect(self, database):
        """
        Verbindet sich zu einer sqlite Datanbank
        Parameters
        ----------
        database
            Die Datenbank, zu der sich das Programm verbinden soll

        Returns
        -------

        """
        self.connection = lite.connect(database)
        self.cursor = self.connection.cursor()

    def insert(self, table, row):
        """
        Fügt Werte in die Datenbank ein.
        Parameters
        ----------
        table : str
            Die Tabelle, in die eingefügt werden soll.
        row : dict
            Die Zeile die eingefügt werden soll als Dictionary Spaltenname : Wert

        Returns
        -------

        """
        cols = ', '.join('{}'.format(col) for col in row.keys())
        vals = ''
        for col in row.values():
            if isinstance(col, str):
                col = "'" + col + "'"
            vals = vals + str(col) + ','

        vals = vals[:-1]
        sql = 'INSERT INTO ' + table + '( ' + str(cols) + ') VALUES (' + str(vals) + ')'
        print(sql)
        self.connection.execute(sql)

    def close_connection(self):
        """
        Schließt die Verbindung zur Datenbank
        Returns
        -------

        """
        self.connection.close()

    def select_single_row(self, statement: str):
        """
        Gibt einen Datensätze einer SELECT-Abfrage als Liste ( zurück
        Parameters
        ----------
        statement: str
            Das SELECT Statement

        Returns
        -------
        list
            Der Datensatz als Liste von einzelnen Werten.
        """
        self.cursor.execute(statement)
        return self.cursor.fetchone()

    def select_all_rows(self, statement: str):
        """
        Gibt alle Datensätze einer SELECT-Abfrage als Liste (von Listen) zurück
        Parameters
        ----------
        statement: str
            Das SELECT Statement

        Returns
        -------
        list
            Die Datensätze als Liste von Listen
        """
        self.cursor.execute(statement)
        return self.cursor.fetchone()

    def commit(self):
        """
        Commited alle getätigten Änderungen

        Returns
        -------

        """
        self.connection.commit()


class PixelGrid(GameGrid):
    __doc__ = '\n    Das Pixel-Grid ist gedacht für Grids, deren Zellen genau 1 Pixel groß sind, d.h.\n    für Spiele in denen Pixelgenaue Informationen wichtig sind.\n    '

    def bounce(self, partner1, partner2):
        mirror_axis = (partner1.direction + partner2.direction) / 2
        self._logging.debug('Bouncing: actor1:' + str(partner1.direction) + ', actor2:' + str(partner2.direction) + 'mirror:' + str(mirror_axis))
        self._logging.debug('Bouncing: actor2:' + str(partner2.direction) + ', actor2:' + str(partner1.direction) + 'mirror:' + str(mirror_axis))
        self.bounce_against_line(partner1, mirror_axis)
        self.bounce_against_line(partner2, mirror_axis)

    def bounce_against_line(self, actor, line_axis):
        """
        Pralle gegen eine (gedachte) Linie mit dem angegebenen
        Winkel nach der Formel Enfallswinkel=Ausfallswinkel

        :param actor: Der Actor, der abprallt.
        :param line_axis: Der Winkel in dem die Linie steht.
            0° bezeichnet eine horizontale Linie (von links nach rechts verlaufend,
            der Winkel wird gegen den Uhrzeigersinn angegeben.

        """
        actor.direction = (line_axis * 2 - actor.direction) % 360

    def bounce_from_border(self, actor, border: str):
        """
        Pralle gegen einen Rand und ändere dabei den Winkel nach der Formel
        Einfallswinkel = Ausfallswinkel.

        :param actor: Der Actor der abprallen soll.
        :param border: Der Rand als String ("left", "right", "top", "border")

        """
        deg_mirror = 0
        if border == 'top':
            deg_mirror = 0
        else:
            if border == 'bottom':
                deg_mirror = 180
            else:
                if border == 'left':
                    deg_mirror = 90
                else:
                    if border == 'right':
                        deg_mirror = 270
        actor.direction = deg_mirror * 2 - actor.direction


class CellGrid(GameGrid):
    __doc__ = '\n    Das Cell-Grid ist gedacht für Grids, deren Zellen größer als 1 Pixel sind.\n    '

    def __init__(self, title, cell_size=32, columns=8, rows=8, margin=0, background_color=(255, 255, 255), cell_color=(0, 0, 0), img_path=None, img_action='upscale', speed=60, toolbar=False, console=False, actionbar=True):
        self._non_static_collision_actors = defaultdict(list)
        self._static_collision_actors = defaultdict(list)
        self._non_static_actors = []
        super().__init__(title, cell_size, columns, rows, margin, background_color, cell_color, img_path, img_action, speed, toolbar, console, actionbar)

    def _call_collisions(self):
        self._non_static_collision_actors.clear()
        for actor in self._non_static_actors:
            self._non_static_collision_actors[(actor.get_x(), actor.get_y())].append(actor)

        super()._call_collisions()

    def get_all_collisions_for_actor(self, actor):
        """
        Gibt einen Actor zurück, dessen Bounding-Boxes mit dem angegebenen Akteur
        kollidieren.

        Parameters
        ----------
        actor Ein Actor vom angegebenen Klassennahmen, der mit dem angegebenen Actor kollidiert.
        class_name Den Klassennamen nach dem gefiltert werden soll.

        Returns
        -------

        """
        collision_actors = self.get_all_actors_at_location(actor.location)
        if actor in collision_actors:
            collision_actors.remove(actor)
        return collision_actors

    def remove_actor(self, actor):
        if actor in self._non_static_actors:
            self._non_static_actors.remove(actor)
        if actor in self._static_collision_actors[(actor.get_x(), actor.get_y())]:
            self._static_collision_actors[(actor.get_x(), actor.get_y())].remove(actor)
        self._logging.info('Removed' + str(actor))
        super().remove_actor(actor)

    def remove_actors_from_cell(self, location):
        """
        Entfernt alle Actors aus einer Zelle
        Parameters
        ----------
        location : Die Zelle aus der der Akteur entfernt werden soll.

        Returns
        -------

        """
        for actor in self._non_static_collision_actors[(location[0], location[1])]:
            self.remove_actor(actor)

        for actor in self._static_collision_actors[(location[0], location[1])]:
            self.remove_actor(actor)

    def add_actor(self, actor, location=None):
        if actor.is_static:
            self._static_collision_actors[(actor.get_x(), actor.get_y())].append(actor)
        else:
            self._non_static_actors.append(actor)
        super().add_actor(actor, location)

    def update_actor(self, actor, attribute, value):
        if attribute == 'is_static' and value is True:
            self._static_collision_actors[(actor.get_x(), actor.get_y())].append(actor)
            if actor in self._non_static_collision_actors:
                self._non_static_collision_actors.remove(actor)
        else:
            self._non_static_actors.append(actor)
        super()._update_actor(actor, attribute, value)

    def get_all_actors_at_location(self, location: tuple, class_name: str='') -> list:
        """
        Gebe alle Akteure an den angegebenen Zellenkoordinaten zurück

        :param location: Die Zellenkordinaten als Tupel (x,y)
        :param class_name: Den Klassennamen, nachdem gefiltert werden soll
        :return: Eine Liste aller Akteure (mit der angegebenen Klasse) an der Position.
        """
        actors_at_location = []
        try:
            if self._non_static_collision_actors[(location[0], location[1])]:
                actors_at_location.extend(self._non_static_collision_actors[(location[0], location[1])])
            if self._static_collision_actors[(location[0], location[1])]:
                actors_at_location.extend(self._static_collision_actors[(location[0], location[1])])
        except:
            self.logging.info('Cellgrid: get_all_actors_at_location() : No actor at location')

        if class_name is not '':
            actors_at_location = [actor for actor in actors_at_location if actor.__class__.__name__ == class_name]
        return actors_at_location

    def get_actor_at_location(self, location, class_name) -> list:
        """
        Gibt *einen* Akteur  an der Position zurück.

        :param class_name: Der Klassenname nachdem gesucht werden soll als String
            (z.B. alle Akteure vom Typ "Wall").
        :param location: Optional kann eine andere Zellen-Koordinate als
            Tupel (x,y) angegeben werden.
        :return: Der erste Akteur vom angegegebenen Typ.
        """
        actors = self.get_all_actors_at_location(location, class_name)
        if actors:
            return actors[0]
        else:
            return

    def add_cell_image(self, img_path: str, location: tuple):
        """
        Fügt ein Bild zu einer einzelnen Zelle hinzu

        :param img_path: Der Pfad zum Bild relativ zum aktuellen Verzeichnis
        :param location: Die Zelle, die "angemalt" werden soll.
        """
        top_left = self.cell_to_pixel(location)
        cell_image = pygame.image.load(img_path).convert()
        cell_image = pygame.transform.scale(cell_image, (self.cell_size, self.cell_size))
        self._image.blit(cell_image, (top_left[0], top_left[1], self.cell_size, self.cell_size))

    @property
    def type(self):
        return 'cell'


class GUIGrid(GameGrid):
    __doc__ = '\n    Das GUI-Grid erlaubt es Pop-Up Fenster mit GUI Elementen einzublenden.\n    '

    def button_box(self, message: str, choices: list) -> str:
        """
        Zeigt ein Pop-Up mit selbst gewählten Buttons an.

        Parameters
        ----------
        message : int
            Die Nachricht, die angezeigt werden soll.
        choices : list
            Texte, die in Auswahlmöglichkeiten übersetzt werden.

        Returns
        -------
        str
            Die gewählte Antwortmöglichkeit als Text.

        """
        reply = easygui.buttonbox(message, choices=choices)
        return reply

    def integer_box(self, message: str, title='', min: int=0, max: int=sys.maxsize, image=None) -> str:
        """
        Zeigt ein Pop-Up zur Eingabe einer Zahl ein.

        Parameters
        ----------
        message : int
            Die Nachricht, die angezeigt werden soll
        title: String
            Der Fenster-Titel.
        min : int
            Der minimale Wert
        max : int
            Der maximale Wert
        image : str
            Optional: Pfad zu einem Bild.

        Returns
        -------
        int
            Der Wert, der eingegeben wurde.

        """
        reply = easygui.integerbox(message, title=title, lowerbound=min, upperbound=max, image=image)
        return reply

    def string_box(self, message: str, default='', title='', strip=False, image=None) -> str:
        """
        Zeigt ein Pop-Up zur Eingabe einer Zahl ein.

        Parameters
        ----------
        message : int
            Die Nachricht, die angezeigt werden soll.
        title: String
            Der Fenster-Titel.
        strip : bool
            Sollen Whitespaces (Leerzeichen) aus dem String herausgelöscht werden?
        image : str
            Optional: Pfad zu einem Bild.

        Returns
        -------
        str
            Der eingegebene Wert als String.
        """
        reply = easygui.enterbox(message, title=title, default=default, strip=strip, image=image)
        return reply

    def message_box(self, message):
        """
        Zeigt eine Nachrichtenbox
        Parameters
        ----------
        message
            Die Nachricht, die angezeigt werden soll.

        Returns
        -------

        """
        easygui.msgbox(message)