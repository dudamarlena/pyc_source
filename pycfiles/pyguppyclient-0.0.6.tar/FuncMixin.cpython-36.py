# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\source\Tools\FuncMixin.py
# Compiled at: 2019-04-13 14:49:35
# Size of source mod 2**32: 846 bytes
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QStackedWidget, QWidget

def fm_returnTo(self: QWidget, toIndex: int, stackedWidget=None):
    """用于页面跳转"""
    if stackedWidget is None:
        if hasattr(self, 'stackedWidget'):
            stackedWidget = self.stackedWidget
        else:
            return
    else:
        stackedWidget.setCurrentIndex(toIndex)


class FuncMixin(QObject):

    def __init__(self, *a, **kw):
        (super().__init__)(*a, **kw)
        all_fm = [(func[0], func[1]) for k, func in enumerate(globals().items()) if func[0].find('fm') != -1]
        for f in all_fm:
            funcName, func = f
            setattr(self, funcName, func)