# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sprite_rooms.py
# Compiled at: 2020-03-29 18:10:53
# Size of source mod 2**32: 8890 bytes
__doc__ = '\nSprite move between different rooms.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sprite_rooms\n'
import arcadeplus, os
SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
SCREEN_WIDTH = SPRITE_SIZE * 14
SCREEN_HEIGHT = SPRITE_SIZE * 10
SCREEN_TITLE = 'Sprite Rooms Example'
MOVEMENT_SPEED = 5

class Room:
    """Room"""

    def __init__(self):
        self.wall_list = None
        self.background = None


def setup_room_1():
    """
    Create and return room 1.
    If your program gets large, you may want to separate this into different
    files.
    """
    room = Room()
    room.wall_list = arcadeplus.SpriteList()
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if y != SPRITE_SIZE * 4:
                if y != SPRITE_SIZE * 5 or :
                    wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
    wall.left = 7 * SPRITE_SIZE
    wall.bottom = 5 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcadeplus.load_texture(':resources:images/backgrounds/abstract_1.jpg')
    return room


def setup_room_2():
    """
    Create and return room 2.
    """
    room = Room()
    room.wall_list = arcadeplus.SpriteList()
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if y != SPRITE_SIZE * 4:
                if y != SPRITE_SIZE * 5 or :
                    wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
                    wall.left = x
                    wall.bottom = y
                    room.wall_list.append(wall)

    wall = arcadeplus.Sprite(':resources:images/tiles/boxCrate_double.png', SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcadeplus.load_texture(':resources:images/backgrounds/abstract_2.jpg')
    return room


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.current_room = 0
        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcadeplus.SpriteList()
        self.player_list.append(self.player_sprite)
        self.rooms = []
        room = setup_room_1()
        self.rooms.append(room)
        room = setup_room_2()
        self.rooms.append(room)
        self.current_room = 0
        self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        scale = SCREEN_WIDTH / self.rooms[self.current_room].background.width
        arcadeplus.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)
        self.rooms[self.current_room].wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcadeplus.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcadeplus.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcadeplus.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcadeplus.key.UP or key == arcadeplus.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcadeplus.key.LEFT or key == arcadeplus.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0:
            if self.current_room == 1:
                self.current_room = 0
                self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)
                self.player_sprite.center_x = SCREEN_WIDTH


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()