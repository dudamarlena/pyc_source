# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\math\Rectangle.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 906 bytes


class Rectangle:
    height: int
    width: int
    x: int
    y: int

    def __init__(self, *args, **kwargs):
        if args:
            if len(args) == 4:
                self.x, self.y, self.width, self.height = args
        elif kwargs:
            self.__dict__.update(kwargs)

    def round(rect):
        return Rectangle(round(rect.x), round(rect.y), round(rect.width), round(rect.height))

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def location(self):
        return (self.x, self.y)