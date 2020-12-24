# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/material_ui/demo.py
# Compiled at: 2015-03-01 17:04:59
__version__ = '1.0.0'
import sys
sys.path.append('..')
import traceback
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from demo.forms import Screen1
from navigation.control import *
Builder.load_file('demo/commons.kv')

class TestApp(App):

    def build(self):
        self.nav = NavigationController(push_mode='left', font_name='font/Roboto-Regular.ttf')
        Screen1(shared_navigation_controller=self.nav).push()
        return self.nav


if __name__ == '__main__':
    TestApp().run()