# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\procedural_caves_cellular.py
# Compiled at: 2020-03-29 18:07:04
# Size of source mod 2**32: 11763 bytes
__doc__ = '\nThis example procedurally develops a random cave based on cellular automata.\n\nFor more information, see:\nhttps://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.procedural_caves_cellular\n'
import random, arcadeplus, timeit, os
SPRITE_SCALING = 0.125
SPRITE_SIZE = 128 * SPRITE_SCALING
GRID_WIDTH = 400
GRID_HEIGHT = 300
CHANCE_TO_START_ALIVE = 0.4
DEATH_LIMIT = 3
BIRTH_LIMIT = 4
NUMBER_OF_STEPS = 4
MOVEMENT_SPEED = 5
VIEWPORT_MARGIN = 300
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = 'Procedural Caves Cellular Automata Example'
MERGE_SPRITES = False

def create_grid(width, height):
    """ Create a two-dimensional grid of specified size. """
    return [[0 for _x in range(width)] for _y in range(height)]


def initialize_grid(grid):
    """ Randomly set grid locations to on/off based on chance. """
    height = len(grid)
    width = len(grid[0])
    for row in range(height):
        for column in range(width):
            if random.random() <= CHANCE_TO_START_ALIVE:
                grid[row][column] = 1


def count_alive_neighbors(grid, x, y):
    """ Count neighbors that are alive. """
    height = len(grid)
    width = len(grid[0])
    alive_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = x + i
            neighbor_y = y + j
            if i == 0 and j == 0:
                continue
            elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= height or neighbor_x >= width:
                alive_count += 1
            elif grid[neighbor_y][neighbor_x] == 1:
                alive_count += 1

    return alive_count


def do_simulation_step(old_grid):
    """ Run a step of the cellular automaton. """
    height = len(old_grid)
    width = len(old_grid[0])
    new_grid = create_grid(width, height)
    for x in range(width):
        for y in range(height):
            alive_neighbors = count_alive_neighbors(old_grid, x, y)
            if old_grid[y][x] == 1:
                if alive_neighbors < DEATH_LIMIT:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            elif alive_neighbors > BIRTH_LIMIT:
                new_grid[y][x] = 1
            else:
                new_grid[y][x] = 0

    return new_grid


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.grid = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.view_bottom = 0
        self.view_left = 0
        self.draw_time = 0
        self.processing_time = 0
        self.physics_engine = None
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def setup(self):
        self.wall_list = arcadeplus.SpriteList(use_spatial_hash=True)
        self.player_list = arcadeplus.SpriteList()
        self.grid = create_grid(GRID_WIDTH, GRID_HEIGHT)
        initialize_grid(self.grid)
        for step in range(NUMBER_OF_STEPS):
            self.grid = do_simulation_step(self.grid)

        if not MERGE_SPRITES:
            for row in range(GRID_HEIGHT):
                for column in range(GRID_WIDTH):
                    if self.grid[row][column] == 1:
                        wall = arcadeplus.Sprite(':resources:images/tiles/grassCenter.png', SPRITE_SCALING)
                        wall.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                        wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                        self.wall_list.append(wall)

        else:
            for row in range(GRID_HEIGHT):
                column = 0
                while column < GRID_WIDTH:
                    while column < GRID_WIDTH and self.grid[row][column] == 0:
                        column += 1

                    start_column = column
                    while column < GRID_WIDTH and self.grid[row][column] == 1:
                        column += 1

                    end_column = column - 1
                    column_count = end_column - start_column + 1
                    column_mid = (start_column + end_column) / 2
                    wall = arcadeplus.Sprite(':resources:images/tiles/grassCenter.png', SPRITE_SCALING, repeat_count_x=column_count)
                    wall.center_x = column_mid * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.width = SPRITE_SIZE * column_count
                    self.wall_list.append(wall)

        self.player_sprite = arcadeplus.Sprite(':resources:images/animated_characters/female_person/femalePerson_idle.png', SPRITE_SCALING)
        self.player_list.append(self.player_sprite)
        placed = False
        while not placed:
            max_x = GRID_WIDTH * SPRITE_SIZE
            max_y = GRID_HEIGHT * SPRITE_SIZE
            self.player_sprite.center_x = random.randrange(max_x)
            self.player_sprite.center_y = random.randrange(max_y)
            walls_hit = arcadeplus.check_for_collision_with_list(self.player_sprite, self.wall_list)
            if len(walls_hit) == 0:
                placed = True

        self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        """ Render the screen. """
        draw_start_time = timeit.default_timer()
        arcadeplus.start_render()
        self.wall_list.draw()
        self.player_list.draw()
        sprite_count = len(self.wall_list)
        output = f"Sprite Count: {sprite_count}"
        arcadeplus.draw_text(output, self.view_left + 20, self.height - 20 + self.view_bottom, arcadeplus.color.WHITE, 16)
        output = f"Drawing time: {self.draw_time:.3f}"
        arcadeplus.draw_text(output, self.view_left + 20, self.height - 40 + self.view_bottom, arcadeplus.color.WHITE, 16)
        output = f"Processing time: {self.processing_time:.3f}"
        arcadeplus.draw_text(output, self.view_left + 20, self.height - 60 + self.view_bottom, arcadeplus.color.WHITE, 16)
        self.draw_time = timeit.default_timer() - draw_start_time

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

    def on_resize(self, width, height):
        arcadeplus.set_viewport(self.view_left, self.width + self.view_left, self.view_bottom, self.height + self.view_bottom)

    def on_update(self, delta_time):
        """ Movement and game logic """
        start_time = timeit.default_timer()
        self.physics_engine.update()
        changed = False
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True
        right_bndry = self.view_left + WINDOW_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True
        top_bndry = self.view_bottom + WINDOW_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True
        if changed:
            arcadeplus.set_viewport(self.view_left, self.width + self.view_left, self.view_bottom, self.height + self.view_bottom)
        self.processing_time = timeit.default_timer() - start_time


def main():
    game = MyGame()
    game.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()