# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\boards\board.py
# Compiled at: 2020-02-16 10:02:27
# Size of source mod 2**32: 41789 bytes
import inspect, os
from collections import defaultdict
from inspect import signature
from typing import Union
import pygame
from deprecated import deprecated
import miniworldmaker.app as app
from miniworldmaker.appearances import background
from miniworldmaker.board_positions import board_position
from miniworldmaker.board_positions import board_rect
from miniworldmaker.containers import container
import miniworldmaker.physics as physics
import miniworldmaker.physics as physicsengine
import miniworldmaker.tokens as tkn
from miniworldmaker.tools import db_manager

class MetaBoard(type):

    def __call__(cls, *args, **kwargs):
        instance = (super().__call__)(*args, **kwargs)
        return instance


class Board(container.Container, metaclass=MetaBoard):
    __doc__ = 'Base Class for Boards.\n\n    You can create a custom board by inherit one of Boars subclasses.\n\n    Examples:\n\n        A pixel-board in follow_the_mouse.py:\n\n        >>>  class MyBoard(PixelBoard):\n        >>>\n        >>>  def on_setup(self):\n        >>>    self.add_image(path="images/stone.jpg")\n        >>>    Robot(position=(50, 50))\n        >>>\n        >>>\n        >>>  board = MyBoard(800, 600)\n        A tiled-board in basicframework1.py:\n\n        >>> class MyBoard(TiledBoard):\n        >>>\n        >>>   def on_setup(self):\n        >>>     self.add_image(path="images/soccer_green.jpg")\n        >>>     self.player = Player(position=(3, 4))\n        >>>     self.speed = 10\n        >>>     stone = self.add_background(("images/stone.png"))\n        >>>     stone.is_textured = True\n        >>>     stone.is_scaled_to_tile = True\n        >>>\n        >>>\n        >>>  board = MyBoard(columns=20, rows=8, tile_size=42, tile_margin=0)\n    Args:\n        columns: columns of new board (default: 40)\n        rows: rows of new board (default:40)\n\n    '
    registered_collision_handlers_for_tokens = defaultdict(list)
    token_class_ids = defaultdict()
    token_classes = defaultdict()
    token_class_id_counter = 0
    subclasses = None
    begin_prefix = 'on_touching_'
    separate_prefix = 'on_separation_from_'

    def __init__(self, columns=40, rows=40, tile_size=1, tile_margin=0, background_image=None):
        super().__init__()
        pygame.init()
        self.registered_events = {
         'all'}
        self.is_running = True
        self.sound_effects = {}
        self.physics_property = physicsengine.PhysicsProperty
        self._is_setup = False
        if not hasattr(self, '_fps'):
            self._fps = 60
        else:
            self._tokens = pygame.sprite.LayeredDirty()
            self._key_pressed = False
            self._animated = False
            self._grid = []
            self._orientation = 0
            self._repaint_all = 1
            if type(columns) != int or type(rows) != int:
                if type(columns) == tuple and type(columns[0]) == int and type(columns[0]) == int:
                    columns, rows = columns[0], columns[1]
                else:
                    raise TypeError('ERROR: columns and rows should be int values but types are', str(type(columns)), 'and', str(type(rows)))
        self._columns, self._rows, self._tile_size, self._tile_margin = (
         columns, rows, tile_size, tile_margin)
        self._grid = []
        for row in range(self.rows):
            self._grid.append([])
            for column in range(self.columns):
                self._grid[row].append(0)

        self.background = None
        self.backgrounds = []
        self._update_background()
        self._image = pygame.Surface((1, 1))
        self.surface = pygame.Surface((1, 1))
        self.frame = 0
        self.speed = 1
        self.clock = pygame.time.Clock()
        self._Board__last_update = pygame.time.get_ticks()
        self._app = app.App('MiniWorldMaker')
        self._app.add_container(self, 'top_left')
        app.App.board = self
        self.registered_event_handlers = dict()
        self.tokens_with_eventhandler = defaultdict(list)
        self.tokens_with_collisionhandler = defaultdict(list)
        if background_image is not None:
            self.add_background(background_image)
        self.dirty = 1
        self.timed_objects = []
        self._repaint_all = 1
        self._executed_events = set()
        self.window.send_event_to_containers('setup', self)

    @classmethod
    def from_db(cls, file):
        """
        Loads a sqlite db file.

        Args:
            file:

        Returns:

        """
        db = db_manager.DBManager(file)
        data = db.select_single_row('SELECT rows, columns, tile_size, tile_margin, board_class FROM Board')
        board = cls()
        board.rows = data[0]
        board.columns = data[1]
        board._tile_size = data[2]
        board._tile_margin = data[3]
        data = db.select_all_rows('SELECT token_id, column, row, token_class FROM token')
        if data:
            for tokens in data:
                token_class_name = tokens[3]
                token_class = tkn.Token
                class_list = tkn.Token.all_subclasses()
                for cls_obj in class_list:
                    if cls_obj.__name__ == token_class_name:
                        token_class = cls_obj

                token_class(position=(tokens[1], tokens[2]))

        board.window.send_event_to_containers('Loaded from db', board)
        return board

    @classmethod
    def all_subclasses(cls):

        def rec_all_subs(base_cls):
            if cls.subclasses is None:
                return set(base_cls.__subclasses__()).union([s for c in base_cls.__subclasses__() for s in rec_all_subs(c)])
            return cls.subclasses

        return rec_all_subs(cls)

    def __str__(self):
        return '{0} with {1} columns and {2} rows'.format(self.__class__.__name__, self.columns, self.rows)

    def _act_all(self):
        for token in self.tokens:
            if token.board:
                self._handle_act_event(token)

        method = self._get_method(self, 'act')
        if method:
            method()

    @property
    def container_width(self) -> int:
        """
        Gets the width of the container

        Returns:
            The width of the container (in pixels on a PixelGrid; in Tiles on a TiledGrid)

        """
        if self._repaint_all:
            self._container_width = self.columns * self.tile_size + (self.columns + 1) * self.tile_margin
        return self._container_width

    @property
    def container_height(self) -> int:
        """
        Gets the height of the container

        Returns:
            The height of the container (in pixels on a PixelGrid; in Tiles on a TiledGrid)

        """
        if self._repaint_all:
            self._container_height = self.rows * self.tile_size + (self.rows + 1) * self.tile_margin
        return self._container_height

    @property
    def fps(self) -> int:
        """
        The world speed. The world speed is counted in fps (frames per second).

        """
        return self._fps

    @fps.setter
    def fps(self, value: int):
        self._fps = value

    @property
    def width(self) -> int:
        """
        See container_width
        """
        return self.container_width

    @property
    def height(self) -> int:
        """
        See container_height
        """
        return self.container_height

    @property
    def window(self) -> app.App:
        """
        Gets the parent window

        Returns:
            The window

        """
        return self._window

    @property
    def rows(self) -> int:
        """
        The number of rows
        """
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def columns(self) -> int:
        """
        The number of columns
        """
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def tile_size(self) -> int:
        """
        The number of columns
        """
        return self._tile_size

    @tile_size.setter
    def tile_size(self, value):
        self._tile_size = value
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def tile_margin(self) -> int:
        """
        The number of columns
        """
        return self._tile_margin

    @tile_margin.setter
    def tile_margin(self, value):
        self._tile_margin = value
        self.window.dirty = 1
        self._repaint_all = 1

    @property
    def tokens(self) -> pygame.sprite.LayeredDirty:
        """
        A list of all tokens registered to the grid.
        """
        return self._tokens

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def add_image(self, path: str) -> background.Background:
        """
        Adds image to current background.
        If no background is created yet, a new background will be created with this image.

        Args:
            path: The path to the image as relative path

        Returns:
            The index of the image.

        Examples:
            >>> class MyBoard(Board):
            >>>
            >>>     def __init__(self):
            >>>         super().__init__(columns=400, rows=200)
            >>>         self.add_image(path="images/stone.jpg")
            Creates Board with file stone.jpg in folder images as background

        """
        if self.background is None:
            self.add_background(path)
            image = self.background.image
            self.window._display_update()
            self.window.window_surface.blit(image, self.rect)
        else:
            image = self.background.add_image(path)
        return image

    def add_background(self, source: Union[(str, tuple)]) -> background.Background:
        """
        Adds a new background to the board

        Args:
            source: The path to the first image of the background or a color

        Returns:

        """
        new_background = background.Background(self)
        if type(source) == str:
            new_background.add_image(source)
        else:
            if type(source) == tuple:
                new_background.fill(source)
        if self.background is None:
            self.background = new_background
            self._update_all_costumes()
            self._update_background()
            new_background.orientation = self.background.orientation
        self.backgrounds.append(new_background)
        return new_background

    def add_to_board(self, token, position: board_position.BoardPosition):
        """
        Adds an actor to the board.
        Is called in __init__-Method if position is set.

        Args:
            board: The board, the actor should be added
            position: The position on the board where the actor should be added.
        """
        self.tokens.add(token)
        token.dirty = 1
        if token.init != 1:
            raise UnboundLocalError('super().__init__() was not called')
        self._register_physics_collision_handler(token)
        self._add_board_connector(token, position)

    def _add_board_connector(self, token, position):
        raise Exception("You can't use class Board - You must use a specific class e.g. PixelBoard, TiledBoard or PhysicsBoard")

    def blit_surface_to_window_surface(self):
        self.window.window_surface.blit(self.surface, self.rect)

    def get_colors_at_position(self, position: Union[(tuple, board_position.BoardPosition)]):
        if type(position) == tuple:
            position = board_position.BoardPosition(position[0], position[1])
        return position.color()

    def get_colors_at_line(self, line: list):
        """
        Gets all colors in a line. A line is a list of board_positions

        Args:
            line: the line

        Returns: A list of all colors found at the line

        """
        colors = []
        for pos in line:
            if type(pos) == tuple:
                pos = board_position.BoardPosition.from_tuple(pos)
            color_at_pos = pos.color()
            if color_at_pos not in colors:
                colors.append(color_at_pos)

        return colors

    def get_color_at_rect(self, rect: board_rect.BoardRect, directions=None) -> list:
        return rect.colors()

    def get_tokens_by_pixel(self, pixel: tuple) -> list:
        """Gets all tokens by Pixel.

        Args:
            pixel: the pixel-coordinates

        Returns:
            A list of tokens

        Examples:
            >>> position = board.get_mouse_position()
            >>> tokens = board.get_tokens_by_pixel(position)

        """
        return [token for token in self.tokens if token.rect.collidepoint(pixel)]

    def get_tokens_at_rect(self, rect: pygame.Rect, singleitem=False, exclude=None, token_type=None) -> Union[(
 tkn.Token, list)]:
        """
        Gets all Tokens which are colliding with a given rect.

        Args:
            rect: The rect
            singleitem: Should the method return a single token (faster) or all tokens at rect (slower)
            exclude: Exclude a token
            token_type: Filter return values by token type

        Returns: A single token or a list of tokens at rect

        """
        pass

    @property
    def image(self) -> pygame.Surface:
        """
        The current displayed image
        """
        if self.background:
            self._image = self.background.image
        return self._image

    def remove_tokens_from_rect(self, rect: Union[(tuple, pygame.Rect)], token=None, exclude=None):
        """Removes all tokens in an area

        Args:
            rect: A rectangle or a tuple (which is automated converted to a rectangle with tile_size
            token: The class of the tokens which should be removed
            exclude: A token which should not be removed e.g. the actor itself

        Returns: all tokens in the area
        """
        if type(rect) == tuple:
            rect = pygame.Rect(rect[0], rect[1], 1, 1)
        tokens = self.get_tokens_at_rect(rect)
        if token is not None:
            [token.remove() for token in Board.filter_actor_list(tokens, token)]

    def switch_board(self, Board, size: tuple=None):
        if size is None:
            size = self.size
        self.window.send_event_to_containers('switch_board', [self, Board, size])

    def reset(self):
        """Resets the board
        Creates a new board with init-function - recreates all tokens and actors on the board.

        Examples:

            Restarts flappy the bird game after collision with pipe:

            >>> def on_sensing_collision_with_pipe(self, other, info):
            >>>    self.board.is_running = False
            >>>    self.board.reset()
        """
        self.window.send_event_to_containers('reset', self)

    @deprecated(version='1.0.44', reason='Use _handle_reset_event instead')
    def _reset(self, event, data):
        self._handle_reset_event(event, data)

    def repaint(self):
        if self.background:
            if self._repaint_all:
                self.background.call_all_actions()
                self.surface = pygame.Surface((self.container_width, self.container_height))
                self.surface.blit(self.image, self.surface.get_rect())
            self.tokens.clear(self.surface, self.image)
            repaint_rects = self.tokens.draw(self.surface)
            self.window.repaint_areas.extend(repaint_rects)
            if self._repaint_all:
                self.window.repaint_areas.append(self.rect)
                self._repaint_all = False

    def reset(self):
        """Resets the board
        Creates a new board with init-function - recreates all tokens and actors on the board.

        Examples:

            Restarts flappy the bird game after collision with pipe:

            >>> def on_sensing_collision_with_pipe(self, other, info):
            >>>    self.board.is_running = False
            >>>    self.board.reset()
        """
        self.window.send_event_to_containers('reset', self)

    def run(self, fullscreen=False):
        """
        The method show() should always called at the end of your program.
        It starts the mainloop.

        Examples:
            >>> my_board = Board() # or a subclass of Board
            >>> my_board.show()

        """
        if not self._is_setup:
            if hasattr(self, 'setup'):
                if callable(getattr(self, 'setup')):
                    self.window.send_event_to_containers('setup', self)
            if hasattr(self, 'on_setup'):
                if callable(getattr(self, 'on_setup')):
                    self.window.send_event_to_containers('setup', self)
        self.window.run((self.image), full_screen=fullscreen)

    @deprecated(version='1.0.44', reason='You should use board.run()')
    def show(self, fullscreen=False):
        """
        The method show() should always called at the end of your program.
        It starts the mainloop.

        Examples:
            >>> my_board = Board() # or a subclass of Board
            >>> my_board.show()

        """
        self.run(fullscreen)

    def switch_background(self, index=-1) -> background.Background:
        """Switches the background

        Args:
            index: The index of the new costume. If index=-1, the next costume will be selected

        Returns: The new costume

        """
        if index == -1:
            index = self.backgrounds.index(self.background)
            if index < len(self.backgrounds) - 1:
                index += 1
            else:
                index = 0
        else:
            index = index
        self.background = self.backgrounds[index]
        self.background.dirty = 1
        self.background.changed_all()
        self.background_changed = 1
        self._repaint_all = 1
        [token.set_dirty() for token in self.tokens]
        return self.background

    def update(self):
        if self.is_running:
            if self.frame % self.speed == 0:
                self._act_all()
                self._handle_all_collisions()
            self._update_all_costumes()
            self._update_background()
            self._tick_timed_objects()
            if physicsengine.PhysicsProperty.count > 0:
                physics_tokens = [token for token in self.tokens if token.physics if token.physics.started]
                physics.PhysicsProperty.simulation(physics_tokens)
        self.frame = self.frame + 1
        self.clock.tick(self.fps)
        self._executed_events.clear()

    def _update_all_costumes(self):
        [token.costume.update() for token in self.tokens]

    def _update_background(self):
        if self.background:
            self.background.update()

    def _tick_timed_objects(self):
        [obj.tick() for obj in self.timed_objects]

    def handle_event(self, event, data=None):
        """
        Event handling

        Args:
            event (str): The event which was thrown, e.g. "key_up", "act", "reset", ...
            data: The data of the event (e.g. ["S","s"], (155,3), ...
        """
        if event not in self._executed_events:
            self._executed_events.add(event)
            from miniworldmaker.tokens import token
            token_classes = token.Token.all_subclasses()
            token_classes.add(token.Token)
            all_objects = list(self.tokens.sprites())
            all_objects.append(self)
            for a_object in all_objects:
                if event in ('reset', ):
                    self._handle_reset_event()
                if event in ('setup', ):
                    self._handle_setup_event()
                if event in ('switch_board', ):
                    (self._handle_switch_board_event)(*data)
                if event in ('key_down', 'key_pressed', 'key_down', 'key_up'):
                    self._handle_key_event(a_object, event, data)
                if event in ('mouse_left', 'mouse_right', 'mouse_motion'):
                    self._handle_mouse_event(a_object, event, data)
                if event in ('clicked_left', 'clicked_right'):
                    self._handle_mouse_token_event(event, data)
                if event in ('message', ):
                    self._handle_message_event(a_object, event, data)
                if event in ('button_pressed', ):
                    self._handle_button_event(a_object, event, data)

            if event in self.registered_event_handlers.keys():
                if data is None:
                    self.registered_event_handlers[event]()
                else:
                    try:
                        self.registered_event_handlers[event](self, data)
                    except TypeError:
                        raise TypeError('Wrong number of arguments for ', str(self.registered_event_handlers[event]), ' with Arguments ', data)

            self.get_event(event, data)

    def _get_method(self, a_object, name):
        """
        If a (token-)object has method this returns the method by a given name
        """
        if hasattr(a_object, name):
            if callable(getattr(a_object, name)):
                _method = getattr(a_object, name)
                _bound_method = _method.__get__(a_object, a_object.__class__)
                return _bound_method
            return
        else:
            return

    def _call_method(self, receiver, method, args):
        sig = signature(method)
        if issubclass(receiver.__class__, tkn.Token):
            if not receiver.board:
                return
        elif args == None:
            method()
        else:
            if len(sig.parameters) == len(args):
                method(*args)
            else:
                info = inspect.getframeinfo(inspect.currentframe())
                raise Exception('Wrong number of arguments for ' + str(method) + ' in , got ' + str(len(args)) + ' but should be ' + str(len(sig.parameters)) + '; File:' + str(info.filename), '; Method: ' + str(method))

    def _handle_key_event(self, receiver, event, data):
        method = self._get_method(receiver, 'on_' + str(event))
        if method:
            self._call_method(receiver, method, [data])
        for key in data:
            if key == key.lower():
                method = self._get_method(receiver, 'on_' + event + '_' + key)
                if method:
                    self._call_method(receiver, method, None)

    def _handle_mouse_event(self, receiver, event, data):
        method_name = 'on_' + event
        method = self._get_method(receiver, method_name)
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)

    def _handle_mouse_token_event(self, event, data):
        token = data[0]
        position = data[1]
        method_name = 'on_' + event
        method = self._get_method(token, method_name)
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)
        tokens = self.get_tokens_by_pixel(position)
        for token in tokens:
            method = self._get_method(token, method_name)
            if method:
                self._call_method(token, method, [position])

    def _handle_setup_event(self):
        if not self._is_setup:
            if hasattr(self, 'setup'):
                if callable(getattr(self, 'setup')):
                    self.setup()
                    self._is_setup = True
            if hasattr(self, 'on_setup'):
                if callable(getattr(self, 'on_setup')):
                    self.on_setup()
                    self._is_setup = True
        return self

    def _handle_reset_event(self):
        self.window.event_queue.clear()
        for token in self.tokens:
            token.remove()

        self.window.board = self.__class__(self.width, self.height)
        self.window.board.run()
        board = self.window.board
        board.event_queue.clear()
        del self
        return board

    def _handle_switch_board_event(self, old_board, Board, size: tuple):
        self.window.event_queue.clear()
        for token in self.tokens:
            token.remove()

        self.window.board = Board(size[0], size[1])
        board = self.window.board
        board.run()
        board.event_queue.clear()
        del self
        return board

    def _handle_act_event(self, receiver):
        method = self._get_method(receiver, 'act')
        if method:
            sig = signature(method)
            if len(sig.parameters) == 0:
                method()
            else:
                raise Exception('Wrong number of arguments for act-Method (should be: 0)')

    def _handle_button_event(self, receiver, event, data):
        method = self._get_method(receiver, 'on_button_pressed')
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)

    def _handle_message_event(self, receiver, event, data):
        method = self._get_method(receiver, 'on_message')
        if method:
            sig = signature(method)
            if len(sig.parameters) == 1:
                method(data)

    def _handle_all_collisions(self):
        for token in self.tokens:
            self._handle_collision_with_tokens(token)
            self._handle_collision_with_borders(token)
            self._handle_on_board(token)

    def _handle_collision_with_tokens(self, token):
        members = dir(token)
        found_tokens = []
        for token_type in [member[11:] for member in members if member.startswith('on_sensing_')]:
            tokens_for_token_type = token.sensing_tokens(token_type=(token_type.capitalize()))
            for found_token in tokens_for_token_type:
                if found_token not in found_tokens:
                    found_tokens.append(found_token)

        if found_tokens:
            for other_token in found_tokens:
                parents = inspect.getmro(other_token.__class__)
                other_and_parents = list(parents)
                if other_and_parents:
                    for other_class in other_and_parents:
                        method_name = ('on_sensing_' + str(other_class.__name__)).lower()
                        method = self._get_method(token, method_name)
                        if method:
                            self._call_method(token, method, [other_token])

    def _handle_collision_with_borders(self, token):
        border_methods_dict = {'on_sensing_left_border':self._get_method(token, 'on_sensing_left_border'), 
         'on_sensing_right_border':self._get_method(token, 'on_sensing_right_border'), 
         'on_sensing_bottom_border':self._get_method(token, 'on_sensing_bottom_border'), 
         'on_sensing_top_border':self._get_method(token, 'on_sensing_top_border')}
        on_sensing_borders = self._get_method(token, 'on_sensing_borders')
        if on_sensing_borders or [method for method in border_methods_dict.values() if method is not None]:
            sensed_borders = token.sensing_borders()
            if sensed_borders:
                if on_sensing_borders:
                    self._call_method(token, on_sensing_borders, [sensed_borders])
                for key in border_methods_dict.keys():
                    if border_methods_dict[key]:
                        for border in sensed_borders:
                            if border in key:
                                self._call_method(token, border_methods_dict[key], None)

    def _handle_on_board(self, a_object):
        on_board_handler = self._get_method(a_object, 'on_sensing_on_board'.lower())
        not_on_board_handler = self._get_method(a_object, 'on_sensing_not_on_board'.lower())
        if on_board_handler or not_on_board_handler:
            is_on_board = a_object.sensing_on_board()
            if is_on_board:
                if on_board_handler:
                    on_board_handler()
        elif not_on_board_handler:
            not_on_board_handler()

    def save_to_db(self, file):
        """
        Saves the current board an all actors to database.
        The file is stored as db file and can be opened with sqlite.

        Args:
            file: The file as relative location

        Returns:

        """
        if os.path.exists(file):
            os.remove(file)
        db = db_manager.DBManager(file)
        query_actors = '     CREATE TABLE `token` (\n                        `token_id`\t\t\tINTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\n                        `column`\t\tINTEGER,\n                        `row`\t\t\tINTEGER,\n                        `token_class`\tTEXT,\n                        `parent_class`  TEXT\n                        );\n                        '
        query_board = '     CREATE TABLE `board` (\n                        `tile_size`\t\tINTEGER,\n                        `rows`\t\t\tINTEGER,\n                        `columns`\t\tINTEGER,\n                        `tile_margin`\tINTEGER,\n                        `board_class`\tTEXT\n                        );\n                        '
        cur = db.cursor
        cur.execute(query_actors)
        cur.execute(query_board)
        db.commit()
        for token in self.tokens:
            token_dict = {'column':token.position[0], 
             'row':token.position[1], 
             'token_class':token.__class__.__name__}
            db.insert(table='token', row=token_dict)

        board_dict = {'rows':self.rows, 
         'columns':self.columns, 
         'tile_margin':self.tile_margin, 
         'tile_size':self.tile_size, 
         'board_class':self.__class__.__name__}
        db.insert(table='board', row=board_dict)
        db.commit()
        db.close_connection()
        self.window.send_event_to_containers('Saved to db', file)

    def play_sound(self, path: str):
        if path.endswith('mp3'):
            path = path[:-4] + 'wav'
        elif path in self.sound_effects.keys():
            self.sound_effects[path].play()
        else:
            effect = self.register_sound(path)
            effect.play()

    def play_music(self, path: str):
        """
        plays a music by path

        Args:
            path: The path to the music

        Returns:

        """
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def find_colors(self, rect, color, threshold=(20, 20, 20, 20)):
        return self.background.count_pixels_by_color(rect, color, threshold)

    def get_mouse_position(self) -> Union[(board_position.BoardPosition, None)]:
        """
        Gets the current mouse_position

        Returns:
            Returns the mouse position if mouse is on board. Returns "None" otherwise

        Examples:
            This example shows you how to use the mouse_position

            >>> def act(self):
            >>>     mouse = self.board.get_mouse_position()
            >>>     if mouse:
            >>>         self.point_towards_position(mouse)

        """
        pos = board_position.BoardPosition.from_pixel(pygame.mouse.get_pos())
        clicked_container = self.window.get_container_by_pixel(pos[0], pos[1])
        if clicked_container == self:
            return pos
        return

    def get_board_position_from_pixel(self, pixel):
        return board_position.BoardPosition.from_pixel(pixel)

    def _update_event_handling(self):
        self.tokens_with_eventhandler.clear()
        for token in self.tokens:
            for event_handler in self.registered_event_handlers_for_tokens[token.__class__].keys():
                self.tokens_with_eventhandler[event_handler].append(token)

    def is_position_on_board--- This code section failed: ---

 L. 963         0  LOAD_GLOBAL              type
                2  LOAD_FAST                'position'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_GLOBAL              tuple
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    32  'to 32'

 L. 964        12  LOAD_GLOBAL              board_position
               14  LOAD_METHOD              BoardPosition
               16  LOAD_FAST                'position'
               18  LOAD_CONST               0
               20  BINARY_SUBSCR    
               22  LOAD_FAST                'position'
               24  LOAD_CONST               1
               26  BINARY_SUBSCR    
               28  CALL_METHOD_2         2  '2 positional arguments'
               30  STORE_FAST               'position'
             32_0  COME_FROM            10  '10'

 L. 965        32  LOAD_GLOBAL              type
               34  LOAD_FAST                'position'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  LOAD_GLOBAL              board_position
               40  LOAD_ATTR                BoardPosition
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 966        46  LOAD_FAST                'position'
               48  LOAD_METHOD              to_rect
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  STORE_FAST               'position'
             54_0  COME_FROM            44  '44'

 L. 968        54  LOAD_FAST                'position'
               56  LOAD_ATTR                topleft
               58  LOAD_CONST               0
               60  BINARY_SUBSCR    

 L. 969        62  LOAD_FAST                'position'
               64  LOAD_ATTR                topleft
               66  LOAD_CONST               1
               68  BINARY_SUBSCR    

 L. 970        70  LOAD_FAST                'position'
               72  LOAD_ATTR                right

 L. 971        74  LOAD_FAST                'position'
               76  LOAD_ATTR                top
               78  BUILD_TUPLE_4         4 
               80  UNPACK_SEQUENCE_4     4 
               82  STORE_FAST               'top_left_x'
               84  STORE_FAST               'top_left_y'
               86  STORE_FAST               'right'
               88  STORE_FAST               'top'

 L. 972        90  LOAD_FAST                'top_left_x'
               92  LOAD_CONST               0
               94  COMPARE_OP               <
               96  POP_JUMP_IF_TRUE    130  'to 130'
               98  LOAD_FAST                'top_left_y'
              100  LOAD_CONST               0
              102  COMPARE_OP               <
              104  POP_JUMP_IF_TRUE    130  'to 130'
              106  LOAD_FAST                'position'
              108  LOAD_ATTR                right
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                width
              114  COMPARE_OP               >=
              116  POP_JUMP_IF_TRUE    130  'to 130'
              118  LOAD_FAST                'position'
              120  LOAD_ATTR                bottom
              122  LOAD_FAST                'self'
              124  LOAD_ATTR                height
              126  COMPARE_OP               >=
              128  POP_JUMP_IF_FALSE   134  'to 134'
            130_0  COME_FROM           116  '116'
            130_1  COME_FROM           104  '104'
            130_2  COME_FROM            96  '96'

 L. 973       130  LOAD_CONST               False
              132  RETURN_VALUE     
            134_0  COME_FROM           128  '128'

 L. 975       134  LOAD_CONST               True
              136  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 134

    def register_sound(self, path) -> pygame.mixer.Sound:
        """
        Registers a sound effect to board-sound effects library
        Args:
            path: The path to sound

        Returns: the sound

        """
        try:
            effect = pygame.mixer.Sound(path)
            self.sound_effects[path] = effect
            return effect
        except pygame.error:
            raise FileExistsError("File '{0}' does not exist. Check your path to the sound.".format(path))

    @staticmethod
    def _get_token_class_by_name(name):
        return Board.token_classes.get(name, None)

    @staticmethod
    def _update_token_subclasses():
        """
        Returns a dict with class_name->class
        updat
        Returns:

        """
        token_subclasses = tkn.Token.all_subclasses()
        for cls in token_subclasses:
            Board.token_classes[cls.__name__] = cls
            if cls not in Board.token_class_ids:
                cls.class_id = Board.token_class_id_counter
                Board.token_class_ids[cls] = Board.token_class_id_counter
                Board.token_class_id_counter += 1

        return Board.token_classes

    def _register_physics_collision_handler(self, token):
        Board._update_token_subclasses()
        method_list = [func for func in dir(token.__class__) if callable(getattr(token.__class__, func)) and (func.startswith(Board.begin_prefix) or func.startswith(Board.separate_prefix))]
        for method_name in method_list:
            if method_name.startswith(Board.begin_prefix):
                other_class_name = method_name[len(Board.begin_prefix):].capitalize()
            else:
                if method_name.startswith(Board.separate_prefix):
                    other_class_name = method_name[len(Board.separate_prefix):].capitalize()
            other_class = Board._get_token_class_by_name(other_class_name)
            if other_class is not None:
                child_classes = other_class.all_subclasses()
                for child_class in child_classes:
                    self.add_physics_collision_handler(token, child_class, method_name)

                self.add_physics_collision_handler(token, other_class, method_name)

    def add_physics_collision_handler(self, token, other_class, method):
        handler = physics.PhysicsProperty.space.add_collision_handler(token.__class__.class_id, other_class.class_id)
        handler.data['method'] = getattr(token, method)
        if method.startswith(Board.begin_prefix):
            handler.data['type'] = 'begin'
            handler.begin = self._physics_collision_handler
        else:
            if method.startswith(Board.separate_prefix):
                handler.data['type'] = 'separate'
                handler.separate = self._physics_collision_handler

    def _physics_collision_handler(self, arbiter, space, data):
        rvalue = None
        collision = dict()
        other_class = str(arbiter.shapes[1].token.__class__.__name__).lower()
        rvalue = self.pass_physics_collision_to_tokens(arbiter, space, data)
        if data['type'] == 'begin':
            method = 'on_touching_' + other_class
            method = self._get_method(arbiter.shapes[0].token, method)
            if method:
                if callable(method):
                    rvalue = method(arbiter.shapes[1].token, collision)
        if data['type'] == 'separate':
            method = 'on_separation_from_' + other_class
            method = self._get_method(arbiter.shapes[0].token, method)
            if method:
                if callable(method):
                    rvalue = method(arbiter.shapes[1].token, collision)
        if rvalue is None:
            return True
        return rvalue

    def pass_physics_collision_to_tokens(self, arbiter, space, data):
        collision = ()
        token = arbiter.shapes[0].token
        method_list = [func for func in dir(token.__class__) if callable(getattr(token.__class__, func)) and (func.startswith(Board.begin_prefix) or func.startswith(Board.separate_prefix))]
        for method_name in method_list:
            if method_name.startswith(Board.begin_prefix):
                registered_class_name = method_name[len(Board.begin_prefix):].capitalize()
            else:
                if method_name.startswith(Board.separate_prefix):
                    registered_class_name = method_name[len(Board.separate_prefix):].capitalize()
            registered_class = Board._get_token_class_by_name(registered_class_name)
            if registered_class is not None:
                child_classes_of_registered = registered_class.all_subclasses().union()
                if child_classes_of_registered is not None:
                    registered_classes = child_classes_of_registered.union({registered_class})
                else:
                    registered_classes = child_classes_of_registered = {
                     registered_class}
                other = arbiter.shapes[1].token
                other_class = arbiter.shapes[1].token.__class__
                other_class_name = other_class.__name__.lower()
                if other_class in registered_classes:
                    if data['type'] == 'begin':
                        method_name = str(Board.begin_prefix + registered_class_name).lower()
                    if data['type'] == 'separate':
                        method_name = str(Board.separate_prefix + registered_class_name).lower()
                    method = self._get_method(token, method_name)
                    if method:
                        self._call_method(token, method, [other, collision])

    def add_event_handler_for_class(self, subcls, event, handler):
        handler = getattr(subcls, 'on_' + event, None)
        if callable(handler):
            self.registered_event_handlers_for_tokens[subcls][event] = handler

    def register(self, method):
        bound_method = method.__get__(self, self.__class__)
        setattr(self, method.__name__, bound_method)
        return bound_method

    def send_message(self, message):
        self.window.send_event_to_containers('message', message)