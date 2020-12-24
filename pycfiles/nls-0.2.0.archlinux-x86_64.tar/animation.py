# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/loki/.virtualenvs/nls/lib/python2.7/site-packages/nls/animation.py
# Compiled at: 2016-04-23 16:47:57
from __future__ import absolute_import, print_function
from time import time
from matplotlib import animation
from matplotlib.pyplot import figure
from .pumping import GaussianRingPumping1D

class AbstractAnimation(object):
    """Animation base class that contains common method of initialization and rendering video.
    """

    def __init__(self, model, frames, step=1):
        self.elapsed_time = 0.0
        self.model = model
        self.frames = frames
        self.step = step
        self.writer = animation.writers['ffmpeg'](fps=15, metadata={'title': 'Exciton-polariton condensation.'})

    def getElapsedTime(self):
        """Get time in seconds elapsed during animation rendering.
        """
        return self.elapsed_time

    def render(self, filename):
        """Perform initialization of render, set quality and size video attributes and then call template method that
        is defined in child class.
        """
        self.elapsed_time = -time()
        dpi = 100
        fig = figure(figsize=(16, 9), dpi=dpi)
        with self.writer.saving(fig, filename, dpi):
            for frame_id in xrange(self.frames + 1):
                self.renderFrame(frame_id)
                self.writer.grab_frame()

        self.elapsed_time += time()

    def renderFrame(self, frame_id):
        """It is not a public method that renders only one frame. This method should be overrided in child classes.
        """
        raise Exception('No frame to render: frameRender() override is needed!')

    def report(self):
        """Prints in standard output report about animation rendering. Namely, it prints seconds spent, number of
        frames and step size that is used in functional animation.
        """
        message = 'Elapsed in {0} seconds with {1} frames and {2} step.'
        print(message.format(self.elapsed_time, self.frames, self.step))


class IterationIncreaseAnimation(AbstractAnimation):
    """This class represents object that provide ability to render video that frames draw solution profile in different
    number of iteration which is increasing.
    """

    def __init__(self, model, frames, step=1):
        super(IterationIncreaseAnimation, self).__init__(model, frames, step)

    def renderFrame(self, frame_id):
        solution = self.model.solve(self.step)
        solution.setInitialSolution(solution.getSolution())
        solution.visualize()


class PumpingRadiusIncreaseAnimation(AbstractAnimation):
    """This class implements animation scenario that shows solution profile with different radius of pumping profile.
    In this case spacial pumping profile is gaussian.
    """

    def __init__(self, model, frames, step=1, power=20.0, variation=3.14):
        super(PumpingRadiusIncreaseAnimation, self).__init__(model, frames, step)
        self.power = power
        self.variation = variation

    def renderFrame(self, frame_id):
        origin = frame_id * self.step
        pumping = GaussianRingPumping1D(power=self.power, radius=origin, variation=self.variation)
        self.model.solution.setPumping(pumping)
        solution = self.model.solve()
        solution.setInitialSolution(solution.getSolution())
        solution.visualize()


class PumpingPowerIncreaseAnimation(AbstractAnimation):
    """Funcational animation that is implemented by object of this type is increasing pumping power as time increase.
    Pumping model of a problem should provide ability to set pumping power.
    """

    def __init__(self, model, frames, step=0.1):
        super(PumpingPowerIncreaseAnimation, self).__init__(model, frames, step)

    def renderFrame(self, frame_id):
        self.model.solution.pumping.setPower(frame_id * self.step)
        solution = self.model.solve()
        solution.visualize()