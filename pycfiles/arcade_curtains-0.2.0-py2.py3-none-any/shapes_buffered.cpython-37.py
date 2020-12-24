# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\shapes_buffered.py
# Compiled at: 2020-03-29 18:08:19
# Size of source mod 2**32: 4429 bytes
__doc__ = '\nThis simple animation example shows how to use classes to animate\nmultiple objects on the screen at the same time.\n\nBecause this is redraws the shapes from scratch each frame, this is SLOW\nand inefficient.\n\nUsing buffered drawing commands (Vertex Buffer Objects) is a bit more complex,\nbut faster.\n\nAlso, any Sprite class put in a SpriteList and drawn with the SpriteList will\nbe drawn using Vertex Buffer Objects for better performance.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.shapes\n'
import arcadeplus, random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Shapes!'
RECT_WIDTH = 50
RECT_HEIGHT = 50
NUMBER_OF_SHAPES = 200

class Shape:

    def __init__(self, x, y, width, height, angle, delta_x, delta_y, delta_angle, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle
        self.color = color
        self.shape_list = None

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle

    def draw(self):
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y
        self.shape_list.angle = self.angle
        self.shape_list.draw()


class Ellipse(Shape):

    def __init__(self, x, y, width, height, angle, delta_x, delta_y, delta_angle, color):
        super().__init__(x, y, width, height, angle, delta_x, delta_y, delta_angle, color)
        shape = arcadeplus.create_ellipse_filled(self.x, self.y, self.width, self.height, self.color, self.angle)
        self.shape_list = arcadeplus.ShapeElementList()
        self.shape_list.append(shape)


class Rectangle(Shape):

    def __init__(self, x, y, width, height, angle, delta_x, delta_y, delta_angle, color):
        super().__init__(x, y, width, height, angle, delta_x, delta_y, delta_angle, color)
        shape = arcadeplus.create_rectangle_filled(self.x, self.y, self.width, self.height, self.color, self.angle)
        self.shape_list = arcadeplus.ShapeElementList()
        self.shape_list.append(shape)


class MyGame(arcadeplus.Window):
    """MyGame"""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []
        for i in range(NUMBER_OF_SHAPES):
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            width = random.randrange(10, 30)
            height = random.randrange(10, 30)
            angle = random.randrange(0, 360)
            d_x = random.randrange(-3, 4)
            d_y = random.randrange(-3, 4)
            d_angle = random.randrange(-3, 4)
            red = random.randrange(256)
            green = random.randrange(256)
            blue = random.randrange(256)
            alpha = random.randrange(256)
            shape_type = random.randrange(2)
            if shape_type == 0:
                shape = Rectangle(x, y, width, height, angle, d_x, d_y, d_angle, (red, green, blue, alpha))
            else:
                shape = Ellipse(x, y, width, height, angle, d_x, d_y, d_angle, (red, green, blue, alpha))
            self.shape_list.append(shape)

    def on_update(self, dt):
        """ Move everything """
        for shape in self.shape_list:
            shape.move()

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        for shape in self.shape_list:
            shape.draw()


def main():
    window = MyGame()
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()