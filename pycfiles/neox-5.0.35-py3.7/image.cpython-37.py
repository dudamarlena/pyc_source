# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/image.py
# Compiled at: 2020-02-26 23:29:02
# Size of source mod 2**32: 2170 bytes
from PyQt5.QtWidgets import QLabel, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QPixmap
__all__ = [
 'Image']

class Image(QLabel):

    def __init__(self, obj=None, name='', default_img=None, scaled_rate=None):
        if not obj:
            obj = QWidget()
        super(Image, self).__init__(obj)
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        self.parent = obj
        self.setObjectName('img_' + name)
        if default_img:
            self.pixmap = QPixmap()
            self.pixmap.load(default_img)
            img_width, img_height = self.pixmap.width(), self.pixmap.height()
            scaled_rate = False
            if screen_width <= 1024:
                scaled_rate = 0.5
            else:
                if screen_width <= 1366:
                    scaled_rate = 0.75
            if scaled_rate:
                new_width = img_width * scaled_rate
                new_height = img_height * scaled_rate
                self.pixmap = self.pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(self.pixmap)

    def set_image(self, img, kind=None):
        self.pixmap = QPixmap()
        if img:
            if kind == 'bytes':
                ba = QByteArray.fromBase64(img)
                self.pixmap.loadFromData(ba)
            else:
                self.pixmap.loadFromData(img.data)
            self.setPixmap(self.pixmap)

    def load_image(self, pathfile):
        self.pixmap = QPixmap()
        self.pixmap.load(pathfile)
        self.setPixmap(self.pixmap)

    def activate(self):
        self.free_center()
        self.parent.show()

    def free_center(self):
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        size = self.pixmap.size()
        print(('image size', size.width(), size.height()))
        self.parent.setGeometry(screen_width / 2 - size.width() / 2, screen_height / 2 - size.height() / 2, size.width(), size.height())