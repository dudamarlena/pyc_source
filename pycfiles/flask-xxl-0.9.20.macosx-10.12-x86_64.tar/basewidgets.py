# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kyle/flask-cms/venv/lib/python2.7/site-packages/flask_xxl/basewidgets.py
# Compiled at: 2017-03-10 19:05:13


class Widget(object):

    def render(self):
        raise NotImplementedError

    def __call__(self):
        return self.render()


class ModelWidget(Widget):
    _model = None