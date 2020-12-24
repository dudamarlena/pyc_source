# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\scenes\transitions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 22508 bytes
__doc__ = 'Transitions between Scenes'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import pyglet
from pyglet.gl import *
from cocos.actions import *
import cocos.scene as scene
import cocos.director as director
from cocos.layer import ColorLayer
from cocos.sprite import Sprite
__all__ = [
 'TransitionScene',
 'RotoZoomTransition', 'JumpZoomTransition',
 'MoveInLTransition', 'MoveInRTransition',
 'MoveInBTransition', 'MoveInTTransition',
 'SlideInLTransition', 'SlideInRTransition',
 'SlideInBTransition', 'SlideInTTransition',
 'FlipX3DTransition', 'FlipY3DTransition', 'FlipAngular3DTransition',
 'ShuffleTransition',
 'TurnOffTilesTransition',
 'FadeTRTransition', 'FadeBLTransition',
 'FadeUpTransition', 'FadeDownTransition',
 'ShrinkGrowTransition',
 'CornerMoveTransition',
 'EnvelopeTransition',
 'SplitRowsTransition', 'SplitColsTransition',
 'FadeTransition',
 'ZoomTransition']

class TransitionScene(scene.Scene):
    """TransitionScene"""

    def __init__(self, dst, duration=1.25, src=None):
        """Initializes the transition

        :Parameters:
            `dst` : Scene
                Incoming scene, the one that remains visible when the transition ends.
            `duration` : float
                Duration of the transition in seconds. Default: 1.25
            `src` : Scene
                Outgoing scene. Default: current scene
        """
        super(TransitionScene, self).__init__()
        if src is None:
            src = director.scene
            if isinstance(src, TransitionScene):
                tmp = src.in_scene.get('dst')
                src.finish()
                src = tmp
        if src is dst:
            raise Exception('Incoming scene must be different from outgoing scene')
        envelope = scene.Scene()
        envelope.add(dst, name='dst')
        self.in_scene = envelope
        envelope = scene.Scene()
        envelope.add(src, name='src')
        self.out_scene = envelope
        self.duration = duration
        if not self.duration:
            self.duration = 1.25
        self.start()

    def start(self):
        """Adds the incoming scene with z=1 and the outgoing scene with z=0"""
        self.add((self.in_scene), z=1)
        self.add((self.out_scene), z=0)

    def finish(self):
        """Called when the time is over.
        Envelopes are discarded and the dst scene will be the one runned by director.
        """
        dst = self.in_scene.get('dst')
        src = self.out_scene.get('src')
        director.replace(dst)

    def hide_out_show_in(self):
        """Hides the outgoing scene and shows the incoming scene"""
        self.in_scene.visible = True
        self.out_scene.visible = False

    def hide_all(self):
        """Hides both the incoming and outgoing scenes"""
        self.in_scene.visible = False
        self.out_scene.visible = False

    def visit(self):
        glPushMatrix()
        super(TransitionScene, self).visit()
        glPopMatrix()


class RotoZoomTransition(TransitionScene):
    """RotoZoomTransition"""

    def __init__(self, *args, **kwargs):
        (super(RotoZoomTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        self.in_scene.scale = 0.001
        self.out_scene.scale = 1.0
        self.in_scene.transform_anchor = (
         width // 2, height // 2)
        self.out_scene.transform_anchor = (width // 2, height // 2)
        rotozoom = (ScaleBy(0.001, duration=(self.duration / 2.0)) | Rotate(720, duration=(self.duration / 2.0))) + Delay(self.duration / 2.0)
        self.out_scene.do(rotozoom)
        self.in_scene.do(Reverse(rotozoom) + CallFunc(self.finish))


class JumpZoomTransition(TransitionScene):
    """JumpZoomTransition"""

    def __init__(self, *args, **kwargs):
        (super(JumpZoomTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        self.in_scene.scale = 0.5
        self.in_scene.position = (width, 0)
        self.in_scene.transform_anchor = (width // 2, height // 2)
        self.out_scene.transform_anchor = (width // 2, height // 2)
        jump = JumpBy((-width, 0), (width // 4), 2, duration=(self.duration / 4.0))
        scalein = ScaleTo(1, duration=(self.duration / 4.0))
        scaleout = ScaleTo(0.5, duration=(self.duration / 4.0))
        jumpzoomout = scaleout + jump
        jumpzoomin = jump + scalein
        delay = Delay(self.duration / 2.0)
        self.out_scene.do(jumpzoomout)
        self.in_scene.do(delay + jumpzoomin + CallFunc(self.finish))


class MoveInLTransition(TransitionScene):
    """MoveInLTransition"""

    def __init__(self, *args, **kwargs):
        (super(MoveInLTransition, self).__init__)(*args, **kwargs)
        self.init()
        a = self.get_action()
        self.in_scene.do(Accelerate(a, 0.5) + CallFunc(self.finish))

    def init(self):
        width, height = director.get_window_size()
        self.in_scene.position = (-width, 0)

    def get_action(self):
        return MoveTo((0, 0), duration=(self.duration))


class MoveInRTransition(MoveInLTransition):
    """MoveInRTransition"""

    def init(self):
        width, height = director.get_window_size()
        self.in_scene.position = (width, 0)

    def get_action(self):
        return MoveTo((0, 0), duration=(self.duration))


class MoveInTTransition(MoveInLTransition):
    """MoveInTTransition"""

    def init(self):
        width, height = director.get_window_size()
        self.in_scene.position = (0, height)

    def get_action(self):
        return MoveTo((0, 0), duration=(self.duration))


class MoveInBTransition(MoveInLTransition):
    """MoveInBTransition"""

    def init(self):
        width, height = director.get_window_size()
        self.in_scene.position = (0, -height)

    def get_action(self):
        return MoveTo((0, 0), duration=(self.duration))


class SlideInLTransition(TransitionScene):
    """SlideInLTransition"""

    def __init__(self, *args, **kwargs):
        (super(SlideInLTransition, self).__init__)(*args, **kwargs)
        self.width, self.height = director.get_window_size()
        self.init()
        move = self.get_action()
        self.in_scene.do(Accelerate(move, 0.5))
        self.out_scene.do(Accelerate(move, 0.5) + CallFunc(self.finish))

    def init(self):
        self.in_scene.position = (
         -self.width, 0)

    def get_action(self):
        return MoveBy((self.width, 0), duration=(self.duration))


class SlideInRTransition(SlideInLTransition):
    """SlideInRTransition"""

    def init(self):
        self.in_scene.position = (
         self.width, 0)

    def get_action(self):
        return MoveBy((-self.width, 0), duration=(self.duration))


class SlideInTTransition(SlideInLTransition):
    """SlideInTTransition"""

    def init(self):
        self.in_scene.position = (
         0, self.height)

    def get_action(self):
        return MoveBy((0, -self.height), duration=(self.duration))


class SlideInBTransition(SlideInLTransition):
    """SlideInBTransition"""

    def init(self):
        self.in_scene.position = (
         0, -self.height)

    def get_action(self):
        return MoveBy((0, self.height), duration=(self.duration))


class FlipX3DTransition(TransitionScene):
    """FlipX3DTransition"""

    def __init__(self, *args, **kwargs):
        (super(FlipX3DTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        turnongrid = Waves3D(amplitude=0, duration=0, grid=(1, 1), waves=2)
        flip90 = OrbitCamera(angle_x=0, delta_z=90, duration=(self.duration / 2.0))
        flipback90 = OrbitCamera(angle_x=0, angle_z=90, delta_z=90, duration=(self.duration / 2.0))
        self.in_scene.visible = False
        flip = turnongrid + flip90 + CallFunc(self.hide_all) + FlipX3D(duration=0) + CallFunc(self.hide_out_show_in) + flipback90
        self.do(flip + CallFunc(self.finish) + StopGrid())


class FlipY3DTransition(TransitionScene):
    """FlipY3DTransition"""

    def __init__(self, *args, **kwargs):
        (super(FlipY3DTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        turnongrid = Waves3D(amplitude=0, duration=0, grid=(1, 1), waves=2)
        flip90 = OrbitCamera(angle_x=90, delta_z=(-90), duration=(self.duration / 2.0))
        flipback90 = OrbitCamera(angle_x=90, angle_z=90, delta_z=90, duration=(self.duration / 2.0))
        self.in_scene.visible = False
        flip = turnongrid + flip90 + CallFunc(self.hide_all) + FlipX3D(duration=0) + CallFunc(self.hide_out_show_in) + flipback90
        self.do(flip + CallFunc(self.finish) + StopGrid())


class FlipAngular3DTransition(TransitionScene):
    """FlipAngular3DTransition"""

    def __init__(self, *args, **kwargs):
        (super(FlipAngular3DTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        turnongrid = Waves3D(amplitude=0, duration=0, grid=(1, 1), waves=2)
        flip90 = OrbitCamera(angle_x=45, delta_z=90, duration=(self.duration / 2.0))
        flipback90 = OrbitCamera(angle_x=45, angle_z=90, delta_z=90, duration=(self.duration / 2.0))
        self.in_scene.visible = False
        flip = turnongrid + flip90 + CallFunc(self.hide_all) + FlipX3D(duration=0) + CallFunc(self.hide_out_show_in) + flipback90
        self.do(flip + CallFunc(self.finish) + StopGrid())


class ShuffleTransition(TransitionScene):
    """ShuffleTransition"""

    def __init__(self, *args, **kwargs):
        (super(ShuffleTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        aspect = width / height
        x, y = int(12 * aspect), 12
        shuffle = ShuffleTiles(grid=(x, y), duration=(self.duration / 2.0), seed=15)
        self.in_scene.visible = False
        self.do(shuffle + CallFunc(self.hide_out_show_in) + Reverse(shuffle) + CallFunc(self.finish) + StopGrid())


class ShrinkGrowTransition(TransitionScene):
    """ShrinkGrowTransition"""

    def __init__(self, *args, **kwargs):
        (super(ShrinkGrowTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        self.in_scene.scale = 0.001
        self.out_scene.scale = 1
        self.in_scene.transform_anchor = (
         2 * width / 3.0, height / 2.0)
        self.out_scene.transform_anchor = (width / 3.0, height / 2.0)
        scale_out = ScaleTo(0.01, duration=(self.duration))
        scale_in = ScaleTo(1.0, duration=(self.duration))
        self.in_scene.do(Accelerate(scale_in, 0.5))
        self.out_scene.do(Accelerate(scale_out, 0.5) + CallFunc(self.finish))


class CornerMoveTransition(TransitionScene):
    """CornerMoveTransition"""

    def __init__(self, *args, **kwargs):
        (super(CornerMoveTransition, self).__init__)(*args, **kwargs)
        self.out_scene.do(MoveCornerUp(duration=(self.duration)) + CallFunc(self.finish) + StopGrid())

    def start(self):
        self.add((self.in_scene), z=0)
        self.add((self.out_scene), z=1)


class EnvelopeTransition(TransitionScene):
    """EnvelopeTransition"""

    def __init__(self, *args, **kwargs):
        (super(EnvelopeTransition, self).__init__)(*args, **kwargs)
        self.in_scene.visible = False
        move = QuadMoveBy(delta0=(320, 240), delta1=(-630, 0), delta2=(-320, -240),
          delta3=(630, 0),
          duration=(self.duration / 2.0))
        self.do(move + CallFunc(self.hide_out_show_in) + Reverse(move) + CallFunc(self.finish) + StopGrid())


class FadeTRTransition(TransitionScene):
    """FadeTRTransition"""

    def __init__(self, *args, **kwargs):
        (super(FadeTRTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        aspect = width / height
        x, y = int(12 * aspect), 12
        a = self.get_action(x, y)
        self.out_scene.do(a + CallFunc(self.finish) + StopGrid())

    def start(self):
        self.add((self.in_scene), z=0)
        self.add((self.out_scene), z=1)

    def get_action(self, x, y):
        return FadeOutTRTiles(grid=(x, y), duration=(self.duration))


class FadeBLTransition(FadeTRTransition):
    """FadeBLTransition"""

    def get_action(self, x, y):
        return FadeOutBLTiles(grid=(x, y), duration=(self.duration))


class FadeUpTransition(FadeTRTransition):
    """FadeUpTransition"""

    def get_action(self, x, y):
        return FadeOutUpTiles(grid=(x, y), duration=(self.duration))


class FadeDownTransition(FadeTRTransition):
    """FadeDownTransition"""

    def get_action(self, x, y):
        return FadeOutDownTiles(grid=(x, y), duration=(self.duration))


class TurnOffTilesTransition(TransitionScene):
    """TurnOffTilesTransition"""

    def __init__(self, *args, **kwargs):
        (super(TurnOffTilesTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        aspect = width / height
        x, y = int(12 * aspect), 12
        a = TurnOffTiles(grid=(x, y), duration=(self.duration))
        self.out_scene.do(a + CallFunc(self.finish) + StopGrid())

    def start(self):
        self.add((self.in_scene), z=0)
        self.add((self.out_scene), z=1)


class FadeTransition(TransitionScene):
    """FadeTransition"""

    def __init__(self, *args, **kwargs):
        color = kwargs.pop('color', (0, 0, 0)) + (0, )
        (super(FadeTransition, self).__init__)(*args, **kwargs)
        self.fadelayer = ColorLayer(*color)
        self.in_scene.visible = False
        self.add((self.fadelayer), z=2)

    def on_enter(self):
        super(FadeTransition, self).on_enter()
        self.fadelayer.do(FadeIn(duration=(self.duration / 2.0)) + CallFunc(self.hide_out_show_in) + FadeOut(duration=(self.duration / 2.0)) + CallFunc(self.finish))

    def on_exit(self):
        super(FadeTransition, self).on_exit()
        self.remove(self.fadelayer)


class SplitColsTransition(TransitionScene):
    """SplitColsTransition"""

    def __init__(self, *args, **kwargs):
        (super(SplitColsTransition, self).__init__)(*args, **kwargs)
        width, height = director.get_window_size()
        self.in_scene.visible = False
        flip_a = self.get_action()
        flip = flip_a + CallFunc(self.hide_out_show_in) + Reverse(flip_a)
        self.do(AccelDeccel(flip) + CallFunc(self.finish) + StopGrid())

    def get_action(self):
        return SplitCols(cols=3, duration=(self.duration / 2.0))


class SplitRowsTransition(SplitColsTransition):
    """SplitRowsTransition"""

    def get_action(self):
        return SplitRows(rows=3, duration=(self.duration / 2.0))


class ZoomTransition(TransitionScene):
    """ZoomTransition"""

    def __init__(self, *args, **kwargs):
        if 'src' in kwargs or len(args) == 3:
            raise Exception("ZoomTransition does not accept 'src' parameter.")
        (super(ZoomTransition, self).__init__)(*args, **kwargs)
        self.out_scene.visit()

    def start(self):
        screensprite = self._create_out_screenshot()
        zoom = ScaleBy(2, self.duration) | FadeOut(self.duration)
        restore = CallFunc(self.finish)
        screensprite.do(zoom + restore)
        self.add(screensprite, z=1)
        self.add((self.in_scene), z=0)

    def finish(self):
        dst = self.in_scene.get('dst')
        director.replace(dst)

    def _create_out_screenshot(self):
        buffer = pyglet.image.BufferManager()
        image = buffer.get_color_buffer()
        width, height = director.window.width, director.window.height
        actual_width, actual_height = director.get_window_size()
        out = Sprite(image)
        out.position = (actual_width // 2, actual_height // 2)
        out.scale = max(actual_width / width, actual_height / height)
        return out