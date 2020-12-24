# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\particle_stress.py
# Compiled at: 2020-03-29 18:06:37
# Size of source mod 2**32: 2069 bytes
__doc__ = '\nParticle system stress test\n\nRun a particle system that spawns, updates, draws and reaps many particles every frame for performance testing.\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.particle_stress\n'
import os, arcadeplus
from arcadeplus.examples.frametime_plotter import FrametimePlotter
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Particle stress test'
TEXTURE = ':resources:images/pinball/pool_cue_ball.png'

def make_emitter():
    return arcadeplus.Emitter(center_xy=(
     SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
      emit_controller=(arcadeplus.EmitterIntervalWithTime(0.0004, 15.0)),
      particle_factory=(lambda emitter: arcadeplus.LifetimeParticle(filename_or_texture=TEXTURE,
      change_xy=(arcadeplus.rand_in_circle((0.0, 0.0), 5.0)),
      lifetime=1.0,
      scale=0.5,
      alpha=128)))


class MyGame(arcadeplus.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.emitter = make_emitter()
        arcadeplus.set_background_color(arcadeplus.color.BLACK)
        self.frametime_plotter = FrametimePlotter()

    def on_update(self, delta_time):
        self.emitter.update()
        if self.emitter.can_reap():
            arcadeplus.close_window()
        self.frametime_plotter.end_frame(delta_time)

    def on_draw(self):
        arcadeplus.start_render()
        self.emitter.draw()


if __name__ == '__main__':
    app = MyGame()
    arcadeplus.run()
    app.frametime_plotter.show()