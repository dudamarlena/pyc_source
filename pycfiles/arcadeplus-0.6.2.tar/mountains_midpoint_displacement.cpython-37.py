# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\mountains_midpoint_displacement.py
# Compiled at: 2020-03-29 18:06:00
# Size of source mod 2**32: 6842 bytes
__doc__ = '\nMountains Midpoint Displacement\n\nCreate a random mountain range.\nOriginal idea and some code from:\nhttps://bitesofcode.wordpress.com/2016/12/23/landscape-generation-using-midpoint-displacement/\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.mountains_midpoint_displacement\n'
import arcadeplus, random, bisect
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = 'Mountains Midpoint Displacement Example'

def midpoint_displacement(start, end, roughness, vertical_displacement=None, num_of_iterations=16):
    """
    Given a straight line segment specified by a starting point and an endpoint
    in the form of [starting_point_x, starting_point_y] and [endpoint_x, endpoint_y],
    a roughness value > 0, an initial vertical displacement and a number of
    iterations > 0 applies the  midpoint algorithm to the specified segment and
    returns the obtained list of points in the form
    points = [[x_0, y_0],[x_1, y_1],...,[x_n, y_n]]
    """
    if vertical_displacement is None:
        vertical_displacement = (start[1] + end[1]) / 2
    points = [
     start, end]
    iteration = 1
    while iteration <= num_of_iterations:
        points_tup = tuple(points)
        for i in range(len(points_tup) - 1):
            midpoint = list(map(lambda x: (points_tup[i][x] + points_tup[(i + 1)][x]) / 2, [
             0, 1]))
            midpoint[1] += random.choice([-vertical_displacement,
             vertical_displacement])
            bisect.insort(points, midpoint)

        vertical_displacement *= 2 ** (-roughness)
        iteration += 1

    return points


def fix_points(points):
    last_y = None
    last_x = None
    new_list = []
    for point in points:
        x = int(point[0])
        y = int(point[1])
        if not last_y is None:
            if y != last_y:
                if last_y is None:
                    last_x = x
                    last_y = y
            x1 = last_x
            x2 = x
            y1 = last_y
            y2 = y
            new_list.append((x1, 0))
            new_list.append((x1, y1))
            new_list.append((x2, y2))
            new_list.append((x2, 0))
            last_x = x
            last_y = y

    x1 = last_x
    x2 = SCREEN_WIDTH
    y1 = last_y
    y2 = last_y
    new_list.append((x1, 0))
    new_list.append((x1, y1))
    new_list.append((x2, y2))
    new_list.append((x2, 0))
    return new_list


def create_mountain_range(start, end, roughness, vertical_displacement, num_of_iterations, color_start):
    shape_list = arcadeplus.ShapeElementList()
    layer_1 = midpoint_displacement(start, end, roughness, vertical_displacement, num_of_iterations)
    layer_1 = fix_points(layer_1)
    color_list = [
     color_start] * len(layer_1)
    lines = arcadeplus.create_rectangles_filled_with_colors(layer_1, color_list)
    shape_list.append(lines)
    return shape_list


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.mountains = None
        arcadeplus.set_background_color(arcadeplus.color.WHITE)

    def setup(self):
        """
        This, and any function with the arcadeplus.decorator.init decorator,
        is run automatically on start-up.
        """
        self.mountains = []
        background = arcadeplus.ShapeElementList()
        color1 = (195, 157, 224)
        color2 = (240, 203, 163)
        points = ((0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT))
        colors = (color1, color1, color2, color2)
        rect = arcadeplus.create_rectangle_filled_with_colors(points, colors)
        background.append(rect)
        self.mountains.append(background)
        layer_4 = create_mountain_range([0, 350], [SCREEN_WIDTH, 320], 1.1, 250, 8, (158,
                                                                                     98,
                                                                                     204))
        self.mountains.append(layer_4)
        layer_3 = create_mountain_range([0, 270], [SCREEN_WIDTH, 190], 1.1, 120, 9, (130,
                                                                                     79,
                                                                                     138))
        self.mountains.append(layer_3)
        layer_2 = create_mountain_range([0, 180], [SCREEN_WIDTH, 80], 1.2, 30, 12, (68,
                                                                                    28,
                                                                                    99))
        self.mountains.append(layer_2)
        layer_1 = create_mountain_range([250, 0], [SCREEN_WIDTH, 200], 1.4, 20, 12, (49,
                                                                                     7,
                                                                                     82))
        self.mountains.append(layer_1)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        for mountain_range in self.mountains:
            mountain_range.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()