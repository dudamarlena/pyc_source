# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\pymunk_apples.py
# Compiled at: 2020-03-29 18:07:07
# Size of source mod 2**32: 6924 bytes
"""
Use Pymunk physics engine.

For more info on Pymunk see:
http://www.pymunk.org/en/latest/

To install pymunk:
pip install pymunk

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.pymunk_box_stacks

Click and drag with the mouse to move the boxes.
"""
import arcadeplus, pymunk, timeit, math, os
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Pymunk test'

class PhysicsSprite(arcadeplus.Sprite):

    def __init__(self, pymunk_shape, filename):
        super().__init__(filename, center_x=(pymunk_shape.body.position.x), center_y=(pymunk_shape.body.position.y))
        self.pymunk_shape = pymunk_shape


class CircleSprite(PhysicsSprite):

    def __init__(self, pymunk_shape, filename):
        super().__init__(pymunk_shape, filename)
        self.width = pymunk_shape.radius * 2
        self.height = pymunk_shape.radius * 2


class BoxSprite(PhysicsSprite):

    def __init__(self, pymunk_shape, filename, width, height):
        super().__init__(pymunk_shape, filename)
        self.width = width
        self.height = height


class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        arcadeplus.set_background_color(arcadeplus.color.DARK_SLATE_GRAY)
        self.space = pymunk.Space()
        self.space.iterations = 35
        self.space.gravity = (0.0, -900.0)
        self.sprite_list = arcadeplus.SpriteList()
        self.static_lines = []
        self.shape_being_dragged = None
        self.last_mouse_position = (0, 0)
        self.draw_time = 0
        self.processing_time = 0
        floor_height = 80
        body = pymunk.Body(body_type=(pymunk.Body.STATIC))
        shape = pymunk.Segment(body, [0, floor_height], [SCREEN_WIDTH, floor_height], 0.0)
        shape.friction = 10
        self.space.add(shape)
        self.static_lines.append(shape)

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        draw_start_time = timeit.default_timer()
        self.sprite_list.draw()
        for line in self.static_lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            arcadeplus.draw_line(pv1.x, pv1.y, pv2.x, pv2.y, arcadeplus.color.WHITE, 2)

        output = f"Processing time: {self.processing_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 20, arcadeplus.color.WHITE, 12)
        output = f"Drawing time: {self.draw_time:.3f}"
        arcadeplus.draw_text(output, 20, SCREEN_HEIGHT - 40, arcadeplus.color.WHITE, 12)
        self.draw_time = timeit.default_timer() - draw_start_time

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcadeplus.MOUSE_BUTTON_LEFT:
            self.last_mouse_position = (
             x, y)
            shape_list = self.space.point_query((x, y), 1, pymunk.ShapeFilter())
            if len(shape_list) > 0:
                self.shape_being_dragged = shape_list[0]
        elif button == arcadeplus.MOUSE_BUTTON_RIGHT:
            mass = 60
            radius = 10
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.position = (x, y)
            body.velocity = (0, 0)
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)
            sprite = CircleSprite(shape, 'images/coin_01.png')
            self.sprite_list.append(sprite)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcadeplus.MOUSE_BUTTON_LEFT:
            self.shape_being_dragged = None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.shape_being_dragged is not None:
            self.last_mouse_position = (x, y)
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = (dx * 20, dy * 20)

    def on_update(self, delta_time):
        start_time = timeit.default_timer()
        for sprite in self.sprite_list:
            if sprite.pymunk_shape.body.position.y < 0:
                self.space.remove(sprite.pymunk_shape, sprite.pymunk_shape.body)
                sprite.kill()

        self.space.step(0.016666666666666666)
        if self.shape_being_dragged is not None:
            self.shape_being_dragged.shape.body.position = self.last_mouse_position
            self.shape_being_dragged.shape.body.velocity = (0, 0)
        for sprite in self.sprite_list:
            sprite.center_x = sprite.pymunk_shape.body.position.x
            sprite.center_y = sprite.pymunk_shape.body.position.y
            sprite.angle = math.degrees(sprite.pymunk_shape.body.angle)

        self.processing_time = timeit.default_timer() - start_time


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcadeplus.run()


if __name__ == '__main__':
    main()