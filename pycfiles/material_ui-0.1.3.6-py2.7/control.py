# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/material_ui/navigation/control.py
# Compiled at: 2015-03-20 19:33:33
import sys
from kivy.animation import Animation
from kivy.config import Config
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.actionbar import ActionBar, ActionItem, ActionPrevious
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import platform as PLATFORM
from material_ui.flatui.flatui import *
from material_ui.flatui.labels import *
from material_ui.flatui.popups import *
from pkg_resources import resource_filename
alphapng = resource_filename(__name__, 'alpha.png')
path = resource_filename(__name__, 'control.kv')
Builder.load_file(path)
MOBILE = PLATFORM in ('android', 'ios')

class EmptyNavigationStack(Exception):
    """
    Raised whenever you pop with an empty navigation stack.
    """

    def __init__(self):
        super(EmptyNavigationStack, self).__init__('Cannot pop view, navigation stack is empty')


class NavigationController(BoxLayout):
    r"""
    Custom layout you can use to manage navigation in your app.
    This is inspired by iOS navigation system, but much easier...

    You should put a NavigationController as root widget for your app,
    internally uses a stack to manage navigation ( accessible by using the 'stack' property ).

    You can pop\push views by using 'pop' and 'push' methods.
    """
    root_widget = ObjectProperty(None)
    stack = ListProperty([])
    background_color = ListProperty([0.93, 0.93, 0.93, 1])
    animation_duracy = NumericProperty(0.25)
    push_mode = OptionProperty('right', options=['left', 'right'])
    disable_widget = BooleanProperty(False)
    title = StringProperty('Navigation control!')
    nav_height = NumericProperty(dp(56))
    nav_color = ListProperty([0.1, 0.11, 0.11, 1])
    shadow_alpha = NumericProperty(0.065)
    font_name = StringProperty(None)
    font_size = NumericProperty(dp(22))
    text_color = ListProperty([1, 1, 1, 1])
    floating_panel = ObjectProperty(None)
    splash_image = StringProperty(alphapng)
    _push_cache = ListProperty([])
    _actionprev = ObjectProperty(None)
    _actiontext = ObjectProperty(None)
    _content = ObjectProperty(None)
    _width = NumericProperty(float(Config.get('graphics', 'width')))

    def __init__(self, **kargs):
        super(NavigationController, self).__init__(**kargs)
        self._keyboard_show = False
        self._keyboard_just_show = False
        self._has_root = False
        self._last_args = {'title': '', 'animation': None}
        self._animation = None
        self._bind_keyboard()
        return

    def pop(self, *args):
        """
        Use this to go back to the last view.
        Will eventually throw EmptyNavigationStack.
        """
        if self._animation is None:
            if len(self.stack) > 0:
                try:
                    self.root_widget.on_pop(self)
                except:
                    pass

                self._save_temp_view(0, self.root_widget)
                self._run_pop_animation()
            else:
                raise EmptyNavigationStack()
        return

    def push(self, view, **kargs):
        """
        Will append the last view to the list and show the new one.
        Keyword arguments :
            title
                Navigation bar title, default ''.
        """
        if self._animation is None:
            if 'title' not in kargs.keys():
                kargs['title'] = ''
            self._last_kargs = kargs
            x = -1 if self.push_mode == 'left' else 1
            self._save_temp_view(x, view)
            self._run_push_animation()
        return

    def _bind_keyboard(self):
        EventLoop.window.bind(on_keyboard=self._on_keyboard_show)
        EventLoop.window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_show(self, *args):
        self._keyboard_show = True

    def _on_keyboard_down(self, window, key, *args):
        if key == 27:
            if self._keyboard_show:
                self._keyboard_show = False
                EventLoop.window.release_all_keyboards()
            else:
                self.pop()
            return True
        return False

    def _run_push_animation(self):
        try:
            self._temp_view.disabled = self.disable_widget
            duracy = self.animation_duracy if self._has_root else 0
            self._animation = Animation(x=0, duration=duracy)
            self._animation.bind(on_complete=self._push_temp_view)
            self._animation.start(self._temp_view)
        except:
            pass

    def _run_pop_animation(self):
        try:
            self._temp_view.disabled = self.disable_widget
            x = self._temp_view.width * (-1 if self.push_mode == 'left' else 1)
            self._animation = Animation(x=x, duration=self.animation_duracy)
            self._animation.bind(on_complete=self._pop_temp_view)
            self._animation.start(self._temp_view)
        except:
            pass

    def _push_temp_view(self, *args):
        self._temp_view.disabled = False
        if self._has_root:
            self.content.remove_widget(self.root_widget)
        self.stack.append([self.root_widget, self._last_kargs])
        self.root_widget = self._temp_view
        self._clear_temp_view()
        self.content.add_widget(self.root_widget)
        self._has_root = True
        self._update_nav()
        self._animation = None
        try:
            self.root_widget.on_push(self)
        except:
            pass

        return

    def _pop_temp_view(self, *args):
        self._temp_view.disabled = False
        self.content.remove_widget(self.root_widget)
        self.root_widget, self._last_kargs = self.stack.pop()
        if len(self.stack) > 0:
            self._last_kargs = self.stack[(-1)][1]
        self.content.add_widget(self.root_widget)
        self._update_nav()
        self._animation = None
        return

    def _clear_temp_view(self, *args):
        try:
            self.floating_panel.remove_widget(self._temp_view)
        except:
            pass

        self._temp_view = None
        return

    def _save_temp_view(self, p, view):
        self._temp_view = view
        try:
            self._temp_view.pos = [
             self._width * p, 0]
            self.floating_panel.add_widget(self._temp_view)
        except:
            pass

    def _update_nav(self):
        self.title = self._last_kargs['title']
        has_previous = len(self.stack) > 1
        self.actionprev.text = ' < ' if has_previous else ''
        self.actionprev.disabled = not has_previous