# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\maze_recursive.py
# Compiled at: 2020-03-29 18:05:57
# Size of source mod 2**32: 12513 bytes
__doc__ = '\nCreate a maze using a recursive division method.\n\nFor more information on the algorithm, see "Recursive Division Method"\nat https://en.wikipedia.org/wiki/Maze_generation_algorithm\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.maze_recursive\n'
import random, arcadeplus, timeit, os
NATIVE_SPRITE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = NATIVE_SPRITE_SIZE * SPRITE_SCALING
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = 'Maze Recursive Example'
MOVEMENT_SPEED = 8
TILE_EMPTY = 0
TILE_CRATE = 1
MAZE_HEIGHT = 51
MAZE_WIDTH = 51
VIEWPORT_MARGIN = 200
MERGE_SPRITES = True

def create_empty_grid(width, height, default_value=TILE_EMPTY):
    """ Create an empty grid. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            grid[row].append(default_value)

    return grid


def create_outside_walls(maze):
    """ Create outside border walls."""
    for row in range(len(maze)):
        maze[row][0] = TILE_CRATE
        maze[row][len(maze[row]) - 1] = TILE_CRATE

    for column in range(1, len(maze[0]) - 1):
        maze[0][column] = TILE_CRATE
        maze[(len(maze) - 1)][column] = TILE_CRATE


def make_maze_recursive_call(maze, top, bottom, left, right):
    """
    Recursive function to divide up the maze in four sections
    and create three gaps.
    Walls can only go on even numbered rows/columns.
    Gaps can only go on odd numbered rows/columns.
    Maze must have an ODD number of rows and columns.
    """
    start_range = bottom + 2
    end_range = top - 1
    y = random.randrange(start_range, end_range, 2)
    for column in range(left + 1, right):
        maze[y][column] = TILE_CRATE

    start_range = left + 2
    end_range = right - 1
    x = random.randrange(start_range, end_range, 2)
    for row in range(bottom + 1, top):
        maze[row][x] = TILE_CRATE

    wall = random.randrange(4)
    if wall != 0:
        gap = random.randrange(left + 1, x, 2)
        maze[y][gap] = TILE_EMPTY
    if wall != 1:
        gap = random.randrange(x + 1, right, 2)
        maze[y][gap] = TILE_EMPTY
    if wall != 2:
        gap = random.randrange(bottom + 1, y, 2)
        maze[gap][x] = TILE_EMPTY
    if wall != 3:
        gap = random.randrange(y + 1, top, 2)
        maze[gap][x] = TILE_EMPTY
    if top > y + 3:
        if x > left + 3:
            make_maze_recursive_call(maze, top, y, left, x)
    if top > y + 3:
        if x + 3 < right:
            make_maze_recursive_call(maze, top, y, x, right)
    if bottom + 3 < y:
        if x + 3 < right:
            make_maze_recursive_call(maze, y, bottom, x, right)
    if bottom + 3 < y:
        if x > left + 3:
            make_maze_recursive_call(maze, y, bottom, left, x)


def make_maze_recursion(maze_width, maze_height):
    """ Make the maze by recursively splitting it into four rooms. """
    maze = create_empty_grid(maze_width, maze_height)
    create_outside_walls(maze)
    make_maze_recursive_call(maze, maze_height - 1, 0, 0, maze_width - 1)
    return maze


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None
        self.wall_list = None
        self.score = 0
        self.player_sprite = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.processing_time = 0
        self.draw_time = 0

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.player_list = arcadeplus.SpriteList()
        self.wall_list = arcadeplus.SpriteList()
        self.score = 0
        maze = make_maze_recursion(MAZE_WIDTH, MAZE_HEIGHT)
        if not MERGE_SPRITES:
            for row in range(MAZE_HEIGHT):
                for column in range(MAZE_WIDTH):
                    if maze[row][column] == 1:
                        wall = arcadeplus.Sprite(':resources:images/tiles/grassCenter.png', SPRITE_SCALING)
                        wall.center_x = column * SPRITE_SIZE + SPRITE_SIZE / 2
                        wall.center_y = row * SPRITE_SIZE + SPRITE_SIZE / 2
                        self.wall_list.append(wall)

        else:
            for row in range(MAZE_HEIGHT):
                column = 0
                while column < len(maze):
                    while column < len(maze) and maze[row][column] == 0:
                        column += 1

                    start_column = column
                    while column < len(maze) and maze[row][column] == 1:
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
            self.player_sprite.center_x = random.randrange(MAZE_WIDTH * SPRITE_SIZE)
            self.player_sprite.center_y = random.randrange(MAZE_HEIGHT * SPRITE_SIZE)
            walls_hit = arcadeplus.check_for_collision_with_list(self.player_sprite, self.wall_list)
            if len(walls_hit) == 0:
                placed = True

        self.physics_engine = arcadeplus.PhysicsEngineSimple(self.player_sprite, self.wall_list)
        arcadeplus.set_background_color(arcadeplus.color.AMAZON)
        self.view_left = 0
        self.view_bottom = 0
        print(f"Total wall blocks: {len(self.wall_list)}")

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        draw_start_time = timeit.default_timer()
        self.wall_list.draw()
        self.player_list.draw()
        sprite_count = len(self.wall_list)
        output = f"Sprite Count: {sprite_count}"
        arcadeplus.draw_text(output, self.view_left + 20, SCREEN_HEIGHT - 20 + self.view_bottom, arcadeplus.color.WHITE, 16)
        output = f"Drawing time: {self.draw_time:.3f}"
        arcadeplus.draw_text(output, self.view_left + 20, SCREEN_HEIGHT - 40 + self.view_bottom, arcadeplus.color.WHITE, 16)
        output = f"Processing time: {self.processing_time:.3f}"
        arcadeplus.draw_text(output, self.view_left + 20, SCREEN_HEIGHT - 60 + self.view_bottom, arcadeplus.color.WHITE, 16)
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

    def on_update(self, delta_time):
        """ Movement and game logic """
        start_time = timeit.default_timer()
        self.physics_engine.update()
        changed = False
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True
        if changed:
            arcadeplus.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)
        self.processing_time = timeit.default_timer() - start_time


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()