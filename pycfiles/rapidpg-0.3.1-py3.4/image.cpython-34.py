# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rapidpg\loader\image.py
# Compiled at: 2014-06-30 19:20:37
# Size of source mod 2**32: 4577 bytes
from os import listdir
from os.path import join, isfile, splitext, abspath
from pygame.image import load

class ImageLoader:
    __doc__ = '\n    Convenient class for loading images using relative path painless\n    '
    decimal_set = {str(x) for x in range(10)}

    def __init__(self, origin):
        """
        Create a loader pointing at the *origin*. Any loading is relative to the *origin*
        Paths passed to the methods of this object are lists where each element is either
        a directory name or a file name. ``([dir1,dir2,file.txt])``

        :param origin: path string
        """
        self.origin = origin

    @staticmethod
    def is_decimal(s):
        """
        check if all characters in the string are in '0' to '9', and there is
        more than 1 character

        :rtype: bool
        """
        if len(s) is 0:
            return False
        for c in s:
            if c not in ImageLoader.decimal_set:
                return False

        return True

    def load_image(self, path, convert_alpha=False):
        """
        Load an image file

        :param path: Path to the image in list format
        :param convert_alpha: *boolean* convert surfaces with convert_alpha()
        :return: surface
        """
        if convert_alpha:
            return load(self.get_path(path)).convert_alpha()
        return load(self.get_path(path)).convert()

    def load_all(self, path, convert_alpha=False, raw=False):
        """
        Load all files in a directory. Assume they are all images.

        :param path: Path to a directory
        :param convert_alpha: *boolean* convert surfaces with convert_alpha()
        :return: Dict mapping the striped filename to its surface
        """
        result = dict()
        dir_path = self.get_path(path)
        for name in listdir(dir_path):
            file_path = join(dir_path, name)
            if isfile(file_path):
                striped = splitext(name)[0]
                if convert_alpha:
                    result[striped] = load(file_path).convert_alpha()
                    continue
                if raw:
                    result[striped] = load(file_path)
                    continue
                result[striped] = load(file_path).convert()
                continue

        return result

    def load_all_frames(self, path, convert_alpha=False):
        """
        Load all files that have purely numerical name in a directory, assume
        they are images. Return a list of surface in the order of the
        numerical values.

        :param path: Path relative to the origin in list format
            pointing to a directory
        :return: a list of surfaces
        """
        to_load = []
        for name in listdir(self.get_path(path)):
            as_list = name.split('.')
            if len(as_list) <= 2 and ImageLoader.is_decimal(as_list[0]) and isfile(self.get_path(path + [name])):
                to_load.append(name)
                continue

        to_load.sort(key=lambda name: name.split('.')[0])
        return [self.load_image(path + [x], convert_alpha) for x in to_load]

    def load_frames(self, path, frames, convert_alpha=False):
        """
        Load a sequence of image named 1.ext...*frames*.ext from *path*
        *ext* must be consistent

        :param path: Path in list format pointing to a directory
        :param frames: Number of frames to load
        :param convert_alpha: whether surfaces are converted with convert_alpha()
        :return: a list of surfaces
        """
        dir_path = self.get_path(path)
        extension = ''
        for name in listdir(dir_path):
            file = join(dir_path, name)
            if isfile(file):
                striped, file_ext = splitext(name)
                if striped == '1':
                    extension = file_ext
                    break
                else:
                    continue

        surfs = []
        for c in range(1, frames + 1):
            file = join(dir_path, str(c) + extension)
            if convert_alpha:
                surfs.append(load(file).convert_alpha())
                continue
            surfs.append(load(file).convert())

        return surfs

    def get_path(self, path):
        """
        Returns a path string relative to the origin

        :param path: a path in list format
        :return: path string
        """
        return abspath(join(self.origin, *path))