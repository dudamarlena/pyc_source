# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\pymunk_box_stacks.py
# Compiled at: 2020-03-29 18:07:10
# Size of source mod 2**32: 7825 bytes
__doc__ = '\nUse Pymunk physics engine.\n\nFor more info on Pymunk see:\nhttp://www.pymunk.org/en/latest/\n\nTo install pymunk:\npip install pymunk\n\nArtwork from http://kenney.nl\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.pymunk_box_stacks\n\nClick and drag with the mouse to move the boxes.\n'
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
    """MyGame"""

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
        for row in range(10):
            for column in range(10):
                size = 32
                mass = 1.0
                x = 500 + column * 32
                y = floor_height + size / 2 + row * size
                moment = pymunk.moment_for_box(mass, (size, size))
                body = pymunk.Body(mass, moment)
                body.position = pymunk.Vec2d(x, y)
                shape = pymunk.Poly.create_box(body, (size, size))
                shape.elasticity = 0.2
                shape.friction = 0.9
                self.space.add(body, shape)
                sprite = BoxSprite(shape, ':resources:images/tiles/boxCrate_double.png', width=size, height=size)
                self.sprite_list.append(sprite)

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
            body.velocity = (2000, 0)
            shape = pymunk.Circle(body, radius, pymunk.Vec2d(0, 0))
            shape.friction = 0.3
            self.space.add(body, shape)
            sprite = CircleSprite(shape, ':resources:images/items/coinGold.png')
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
                sprite.remove_from_sprite_lists()

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