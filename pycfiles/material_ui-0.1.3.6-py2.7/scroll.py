# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/material_ui/flatui/scroll.py
# Compiled at: 2015-03-13 15:10:54
__version__ = '1.0.0'
import pdb, sys, traceback
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.graphics.context_instructions import PopMatrix, PushMatrix, Rotate
from kivy.graphics.instructions import *
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.metrics import dp, sp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from pkg_resources import resource_filename
path = resource_filename(__name__, 'scroll.kv')
Builder.load_file(path)
spinner_image_default = resource_filename(__name__, 'spinner.png')

class _RefreshScrollEffect(DampedScrollEffect):
    """
    This class is simply based on DampedScrollEffect.
    If you need any documentation please look at kivy.effects.dampedscrolleffect.
    """
    min_scroll_to_reload = NumericProperty(-dp(100))

    def on_overscroll(self, scrollview, overscroll):
        if overscroll < self.min_scroll_to_reload:
            scroll_view = self.target_widget.parent
            scroll_view._did_overscroll = True
            return True
        else:
            return False


class RefreshableScrollView(ScrollView):
    """
    This is a very simple subclass of ScrollView.
    When the user does overscroll the view, a 'ReloadSpinner' is shown.
    You will need to call 'reload_done' once you've dove your loading.
    A ReloadSpinner widget will be added to the root_layout (you can choose ReloadSpinner class to use).
    """
    on_start_reload = ObjectProperty(None)
    spinner_class = StringProperty('LollipopSpinner')
    spinner_image = StringProperty(spinner_image_default)
    spinner_diameter = NumericProperty(dp(38))
    spinner_duracy = NumericProperty(0.2)
    root_layout = ObjectProperty(None)
    spinner_speed = NumericProperty(12)
    spinner_shadow_alpha = NumericProperty(0.05)
    reload_spinner = ObjectProperty(None)

    def __init__(self, **kargs):
        super(RefreshableScrollView, self).__init__(**kargs)
        self.effect_cls = _RefreshScrollEffect
        self._reloading = False
        self._did_overscroll = False

    def on_touch_up(self, *args):
        if self._did_overscroll and not self._reloading:
            if self.on_start_reload:
                self.on_start_reload()
            self.reload_spinner = self._spinner_class()(root_layout=self.root_layout, spinner_image=self.spinner_image, shadow_alpha=self.spinner_shadow_alpha, diameter=self.spinner_diameter, duracy=self.spinner_duracy, speed=self.spinner_speed)
            self.reload_spinner.start()
            self._reloading = True
            self._did_overscroll = False
            return True
        return super(RefreshableScrollView, self).on_touch_up(*args)

    def reload_done(self, *args):
        self._reloading = False
        if self.reload_spinner:
            self.reload_spinner.stop()

    def _spinner_class(self):
        return eval(self.spinner_class)


class ReloadSpinner(Widget):
    """
    Override this class if you want a custom spinner.
    There are fiew thigs to now :
        - Canvas is centered in the spinner center!
        - You need to PopMatrix when you're done drawing content
    See scroll.kv for more informations.
    """
    spinner_image = StringProperty('spinner.png')
    shadow_alpha = NumericProperty(0.05)
    root_layout = ObjectProperty(None)
    diameter = NumericProperty(dp(48))
    duracy = NumericProperty(0.2)
    speed = NumericProperty(6)
    angle = NumericProperty(0)
    on_update_animation = ObjectProperty(None)

    def __init__(self, **kargs):
        super(ReloadSpinner, self).__init__(**kargs)

    def update_animation(self, *args):
        self.angle += self.speed
        if self.angle >= 360:
            self.angle = 0
        if self.on_update_animation:
            self.on_update_animation(self, *args)

    def start(self):
        self.pos = (self.root_layout.width / 2 - self.width / 2,
         self.root_layout.height + self.height - dp(56))
        animation = Animation(y=self.root_layout.height - 2 * self.height, duration=self.duracy)
        animation.start(self)
        self.angle = 0
        self._hex = 0
        self._color = (0, 0, 0, 1)
        self.root_layout.add_widget(self)
        Clock.schedule_interval(self.update_animation, 0.04)

    def stop(self):
        animation = Animation(y=self.root_layout.height - 2 * self.height, duration=self.duracy)
        animation.bind(on_complete=self._remove_animation_done)
        animation.start(self)

    def _remove_animation_done(self, *args):
        self.root_layout.remove_widget(self)
        Clock.unschedule(self.update_animation)


class ImageSpinner(ReloadSpinner):
    """
    Based on the default spinner, kv lang provides image rendering.
    """
    pass


class LollipopSpinner(ReloadSpinner):
    """
    Based on the android gmail app spinner.
    """
    color = ListProperty([0, 0, 0, 1])
    angle2 = NumericProperty(0)
    colors = ListProperty([[0.051, 0.635, 0.376, 1], [0.867, 0.314, 0.267, 1], [0.227, 0.494, 0.953, 1], [0.969, 0.773, 0.253, 1]])

    def __init__(self, **kargs):
        self._current_color = 0
        self.color = self.colors[self._current_color]
        super(LollipopSpinner, self).__init__(**kargs)
        self.speed = 12
        self.on_update_animation = self.update_angle2
        self.angle2 = 0

    def update_angle2(self, *args):
        self.angle2 -= self.speed
        if abs(self.angle2) == 360:
            self.angle2 = 0
        if self.angle == self.angle2 == 0:
            self._current_color += 1
            if self._current_color == len(self.colors):
                self._current_color = 0
            self.color = self.colors[self._current_color]