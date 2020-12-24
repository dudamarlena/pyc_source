# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\texture_transform.py
# Compiled at: 2020-03-29 18:11:19
# Size of source mod 2**32: 3540 bytes
"""
Sprites with texture transformations

Artwork from http://kenney.nl

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sprite_texture_transform
"""
import arcadeplus
from arcadeplus import Matrix3x3
import math, os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHIP_SPEED = 5
ASPECT = SCREEN_HEIGHT / SCREEN_WIDTH
SCREEN_TITLE = 'Texture transformations'

class MyGame(arcadeplus.Window):
    __doc__ = ' Main application class. '

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.ship = None
        self.camera_x = 0
        self.t = 0
        self.stars = None
        self.xy_square = None

    def setup(self):
        """ Setup """
        self.ship = arcadeplus.Sprite(':resources:images/space_shooter/playerShip1_orange.png', 0.5)
        self.ship.center_x = SCREEN_WIDTH / 2
        self.ship.center_y = SCREEN_HEIGHT / 2
        self.ship.angle = 270
        self.stars = arcadeplus.load_texture(':resources:images/backgrounds/stars.png')
        self.xy_square = arcadeplus.load_texture(':resources:images/test_textures/xy_square.png')
        arcadeplus.set_background_color(arcadeplus.color.BLACK)

    def on_update(self, delta_time: float):
        """ Update """
        self.ship.update()
        self.camera_x += 2
        self.t += delta_time * 60

    def on_draw(self):
        """
        Render the screen.
        """
        arcadeplus.start_render()
        for z in (300, 200, 150, 100):
            opacity = int(math.exp(-z / 1000) * 255)
            angle = z
            scale = 150 / z
            translate = scale / 500
            self.stars.draw_transformed(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, opacity, Matrix3x3().rotate(angle).scale(scale * ASPECT, scale).translate(-self.camera_x * translate, 0))

        self.ship.draw()
        for i, pair in enumerate([
         [
          'identity', Matrix3x3()],
         [
          'rotate(30)', Matrix3x3().rotate(30)],
         [
          'scale(0.8, 0.5)', Matrix3x3().scale(0.8, 0.5)],
         [
          'translate(0.3, 0.1)', Matrix3x3().translate(0.3, 0.1)],
         [
          'rotate(10).\nscale(0.33, 0.33)', Matrix3x3().rotate(10).scale(0.7, 0.7)],
         [
          'scale(-1, 1)', Matrix3x3().scale(-1, 1)],
         [
          'shear(0.3, 0.1)', Matrix3x3().shear(0.3, 0.1)],
         [
          f"rotate({int(self.t) % 360})", Matrix3x3().rotate(self.t)]]):
            x = 80 + 180 * (i % 4)
            y = 420 - i // 4 * 320
            arcadeplus.draw_text(pair[0], x, y - 20 - pair[0].count('\n') * 10, arcadeplus.color.WHITE, 10)
            self.xy_square.draw_transformed(x, y, 100, 100, 0, 255, pair[1])


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcadeplus.run()


if __name__ == '__main__':
    main()