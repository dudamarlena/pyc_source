# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/material_ui/flatui/layouts.py
# Compiled at: 2015-02-04 16:18:59
import sys
sys.path.append('..')
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from . import labels
from pkg_resources import resource_filename
path = resource_filename(__name__, 'layouts.kv')
Builder.load_file(path)

class ColorAnchorLayout(AnchorLayout):
    """
    Just an AnchorLayout with a background color.
    """
    background_color = ListProperty([0, 0, 0, 0])


class ColorBoxLayout(BoxLayout):
    """
    Just a BoxLayout with a background color.
    """
    background_color = ListProperty([0, 0, 0, 0])


class ColorFloatLayout(FloatLayout):
    """
    Just a FloatLayout with a background color.
    """
    background_color = ListProperty([0, 0, 0, 0])


class ColorRelativeLayout(RelativeLayout):
    """
    Just a RelativeLayout with a background color.
    """
    background_color = ListProperty([0, 0, 0, 0])


class ColorGridLayout(GridLayout):
    """
    Just a GridLayout with a background color.
    """
    background_color = ListProperty([0, 0, 0, 0])


class ColorStackLayout(StackLayout):
    """
    Just a StackLayout with a background color.
    """
    background_color = ListProperty([0, 0, 0, 0])