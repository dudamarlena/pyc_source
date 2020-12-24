# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Wallpoppy/bg.py
# Compiled at: 2018-12-24 18:50:24
# Size of source mod 2**32: 6001 bytes
import os, pydbus, random, argparse
from gi.repository import GLib
parser = argparse.ArgumentParser(description='Set X11 root window BG using a file or folder and feh.')
parser.add_argument('src', metavar='path', help='Source file or folder.')
parser.add_argument('-r', '--random', action='store_true', help='Randomize image order.')
parser.add_argument('-t', '--time', metavar='SECONDS', type=int, default=3600, help='Time between changes.')
parser.add_argument('-s', '--style', choices=['center', 'fill', 'max', 'scale', 'tile'], default='fill', help='In which style fill the background.\nPreserved ratio:\n* center: Keep the image in the center using the image resolution.\n* fill  : Zoom the image until no corner is left untouched.\n* max   : Zoom the image until it touches a corner.\n* tile  : Repeat the image over the background.\nBy ratio:\n* scale : Stretch and/or shrink the image until it fits.')

class controlBus(object):
    __doc__ = "\n\t\t<node>\n\t\t\t<interface name='moe.hattshire.bg.control'>\n\t\t\t\t<signal name='BackgroundChanged'>\n\t\t\t\t\t<arg type='s' name='file' direction='out' />\n\t\t\t\t</signal>\n\n\t\t\t\t<method name='next'>\n\t\t\t\t\t<arg type='b' name='response' direction='out' />\n\t\t\t\t</method>\n\t\t\t\t<method name='previous'>\n\t\t\t\t\t<arg type='b' name='response' direction='out' />\n\t\t\t\t</method>\n\n\t\t\t\t<method name='addFile'>\n\t\t\t\t\t<arg type='s' name='file' direction='in' />\n\t\t\t\t\t<arg type='b' name='response' direction='out' />\n\t\t\t\t</method>\n\t\t\t\t<method name='addFileNext'>\n\t\t\t\t\t<arg type='s' name='file' direction='in' />\n\t\t\t\t\t<arg type='b' name='response' direction='out' />\n\t\t\t\t</method>\n\n\t\t\t\t<method name='removeFile'>\n\t\t\t\t\t<arg type='s' name='file' direction='in' />\n\t\t\t\t\t<arg type='b' name='response' direction='out' />\n\t\t\t\t</method>\n\n\t\t\t\t<property name='currentBackgroundFile' type='s' access='read'>\n\t\t\t\t\t<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />\n\t\t\t\t</property>\n\t\t\t\t<property name='previousBackgroundFile' type='s' access='read'>\n\t\t\t\t\t<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />\n\t\t\t\t</property>\n\t\t\t\t<property name='nextBackgroundFile' type='s' access='read'>\n\t\t\t\t\t<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />\n\t\t\t\t</property>\n\n\t\t\t\t<property name='fileList' type='s' access='read'>\n\t\t\t\t\t<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />\n\t\t\t\t</property>\n\n\t\t\t\t<property name='imageAvailable' type='b' access='read'>\n\t\t\t\t\t<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />\n\t\t\t\t</property>\n\n\t\t\t\t<property name='random' type='b' access='readwrite'>\n\t\t\t\t\t<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />\n\t\t\t\t</property>\n\n\t\t\t\t<property name='delay' type='i' access='readwrite'>\n\t\t\t\t\t<annotation name='org.freedesktop.DBus.Property.EmitsChangedSignal' value='true' />\n\t\t\t\t</property>\n\t\t\t</interface>\n\t\t</node>\n\t"
    PropertiesChanged = pydbus.generic.signal()
    BackgroundChanged = pydbus.generic.signal()
    ext_list = [
     'gif', 'png', 'tiff', 'jpeg', 'jpg']

    def __init__(self):
        args = parser.parse_args()
        self._controlBus__random = args.random
        source_name = os.path.expanduser(args.src)
        self._controlBus__image_list = []
        self._controlBus__delay = args.time
        self._controlBus__style = '--bg-%s' % args.style
        self.addFile(source_name)
        self.next()
        self._controlBus__timeout_handle = GLib.timeout_add(self._controlBus__delay * 1000, self.next)

    def next(self):
        if self.imageAvailable:
            image = self._controlBus__getImage(position=0)
            self._controlBus__setBackground(image)
            if self.random:
                if len(self._controlBus__image_list) > 1:
                    self._controlBus__randomNext()
            return True
        return False

    def previous(self):
        self._controlBus__swap(-1, 0)
        self._controlBus__setBackground(self._controlBus__image_list[(-1)])
        return True

    def addFile(self, file):
        if os.path.isdir(file):
            file_list = os.listdir(file)
            for folder_file in file_list:
                file_ext = folder_file.split(os.extsep)[(-1)]
                if file_ext not in self.ext_list:
                    continue
                self._controlBus__image_list.append(os.path.join(file, folder_file))

        else:
            if os.path.exists(file):
                self._controlBus__image_list.append(file)
            else:
                return False
        return True

    def addFileNext(self, file):
        if os.path.isdir(file):
            file_list = os.listdir(file)
            for folder_file in file_list:
                file_ext = folder_file.split(os.extsep)[(-1)]
                if file_ext not in self.ext_list:
                    continue
                self._controlBus__image_list.insert(0, os.path.join(file, folder_file))

        else:
            if os.path.exists(file):
                self._controlBus__image_list.append(0, file)
            else:
                return False
        return True

    def removeFile(self, file):
        if file in self._controlBus__image_list:
            self._controlBus__image_list.remove(file)
            return True
        return False

    @property
    def currentBackgroundFile(self):
        return self._controlBus__image_list[(-1)]

    @property
    def nextBackgroundFile(self):
        return self._controlBus__image_list[0]

    @property
    def previousBackgroundFile(self):
        return self._controlBus__image_list[(-2)]

    @property
    def imageAvailable(self, value=None):
        return len(self._controlBus__image_list) > 1

    @property
    def fileList(self):
        return str(self._controlBus__image_list)

    @property
    def random(self):
        return self._controlBus__random

    @property
    def delay(self):
        return self._controlBus__delay

    def __getImage(self, position):
        return self._controlBus__swap(position, -1)

    def __setBackground(self, image):
        os.system("feh %s '%s'" % (self._controlBus__style, image))

    def __randomNext(self):
        pos = random.randint(0, len(self._controlBus__image_list) - 2)
        self._controlBus__swap(pos, 0)

    def __swap(self, fromPosition, toPosition):
        image = self._controlBus__image_list.pop(fromPosition)
        if toPosition < 0:
            if toPosition == -1:
                self._controlBus__image_list.append(image)
            else:
                self._controlBus__image_list.insert(toPosition + 1, image)
        else:
            self._controlBus__image_list.insert(toPosition, image)
        return image