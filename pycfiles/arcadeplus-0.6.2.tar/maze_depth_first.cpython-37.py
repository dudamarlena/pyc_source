# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\maze_depth_first.py
# Compiled at: 2020-03-29 18:05:54
# Size of source mod 2**32: 10929 bytes
__doc__ = '\nCreate a maze using a depth-first search maze generation algorithm.\nFor more information on this algorithm see:\nhttp://www.algosome.com/articles/maze-generation-depth-first.html\n...or search up some other examples.\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.maze_depth_first\n'
import random, arcadeplus, timeit, os
NATIVE_SPRITE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = NATIVE_SPRITE_SIZE * SPRITE_SCALING
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = 'Maze Depth First Example'
MOVEMENT_SPEED = 8
TILE_EMPTY = 0
TILE_CRATE = 1
MAZE_HEIGHT = 51
MAZE_WIDTH = 51
MERGE_SPRITES = True
VIEWPORT_MARGIN = 200

def _create_grid_with_cells(width, height):
    """ Create a grid with empty cells on odd row/column combinations. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(TILE_EMPTY)
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(TILE_CRATE)
            else:
                grid[row].append(TILE_CRATE)

    return grid


def make_maze_depth_first(maze_width, maze_height):
    maze = _create_grid_with_cells(maze_width, maze_height)
    w = (len(maze[0]) - 1) // 2
    h = (len(maze) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x, y):
        vis[y][x] = 1
        d = [
         (
          x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for xx, yy in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[(max(y, yy) * 2)][x * 2 + 1] = TILE_EMPTY
            if yy == y:
                maze[(y * 2 + 1)][max(x, xx) * 2] = TILE_EMPTY
            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))
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
        maze = make_maze_depth_first(MAZE_WIDTH, MAZE_HEIGHT)
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