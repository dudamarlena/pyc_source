# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/artpacker/packer/simple.py
# Compiled at: 2012-05-29 14:05:03
import os
from artpacker.artpacker import SpriteSheet

class PackNode(object):
    """
    Creates an area which can recursively pack other areas of smaller sizes into itself.
    """

    def __init__(self, area):
        if len(area) == 2:
            area = (
             0, 0, area[0], area[1])
        self.area = area

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, str(self.area))

    def get_width(self):
        return self.area[2] - self.area[0]

    width = property(fget=get_width)

    def get_height(self):
        return self.area[3] - self.area[1]

    height = property(fget=get_height)

    def insert(self, area):
        if hasattr(self, 'child'):
            a = self.child[0].insert(area)
            if a is None:
                return self.child[1].insert(area)
            return a
        area = PackNode(area)
        if area.width <= self.width and area.height <= self.height:
            self.child = [
             None, None]
            self.child[0] = PackNode((self.area[0] + area.width, self.area[1], self.area[2], self.area[1] + area.height))
            self.child[1] = PackNode((self.area[0], self.area[1] + area.height, self.area[2], self.area[3]))
            return PackNode((self.area[0], self.area[1], self.area[0] + area.width, self.area[1] + area.height))
        else:
            return


class SimplePacker:

    def __init__(self, max_width, max_height):
        self.max_width = max_width
        self.max_height = max_height

    def pack(self, images):
        result = SpriteSheet()
        source_images = sorted(images, key=lambda item: item['area'], reverse=True)
        output_size = self.adjust_max_size(source_images)
        tree = PackNode(output_size)
        missed_images = []
        for image in source_images:
            position = tree.insert(image['size'])
            if position is None:
                missed_images.append(image)
            else:
                result.size = (
                 max(result.size[0], position.area[2]), max(result.size[1], position.area[3]))
                result.add_sprite(image, position.area)

        return (
         result, missed_images)

    def adjust_max_size(self, images):
        max_width = max(self.max_width, max(map(lambda a: a['width'], images)))
        max_height = max(self.max_height, max(map(lambda a: a['height'], images)))
        return (max_width, max_height)