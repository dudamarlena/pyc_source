# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notetool/app/main.py
# Compiled at: 2020-02-26 03:43:36
# Size of source mod 2**32: 426 bytes
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):

    def build(self):
        """
        实现父类的build()方法
        把build()方法实现为返回一个控件实例(这个控件的实例也就是你整个应用的根控件)
        :return:
        """
        return Label(text='Hello World!')


MyApp().run()