# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\utilities.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 14298 bytes
try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from tkinter import PhotoImage, TclError
from collections.abc import MutableSequence
import sys

class GUIZeroException(Exception):
    pass


class SystemConfig:

    def __init__(self):
        """
        Holds details about the system configuration guizero is using
        """
        self._platform = sys.platform
        if self._platform.startswith('linux'):
            self._platform = 'linux'
        elif PIL_AVAILABLE:
            self._supported_image_types = [
             'GIF', 'Animated GIF', 'BMP', 'ICO', 'PNG', 'JPG', 'TIF']
        else:
            self._supported_image_types = [
             'GIF', 'PNG']
            if self._platform == 'darwin':
                self._supported_image_types = ['GIF']
        self._tk_options = {'*Label.Font':'helvetica 12', 
         '*Label.Foreground':'black'}

    @property
    def PIL_available(self):
        """
        Returns `True` if PIL (Python Imaging Library) is available.
        """
        return PIL_AVAILABLE

    @property
    def supported_image_types(self):
        """
        Returns a list of images types supported by this system
        e.g. ('GIF', 'PNG', 'JPG')
        """
        return self._supported_image_types

    @property
    def platform(self):
        """
        Returns the current platform ("linux", "darwin", "win32")
        """
        return self._platform

    @property
    def tk_options(self):
        """
        Returns a dictionary of tk options in the format {"pattern": value}
        which will be applied when an App is created.

        The tk options can be used to modify the default behaviour of 
        tk and its widgets e.g. Change the background colour of all Buttons ::

            from guizero import system_config
            system_config.tk_options["*Button.Background"] = "green"

        """
        return self._tk_options


system_config = SystemConfig()

class GUIZeroImage:

    def __init__(self, image_source, width, height):
        """
        GUIZeroImage manages an "image" for guizero widgets, parsing its
        contents, sizing it accordingly and managing environment.

        :param string image_source:
            The source of the image, a file path, PIL or
            Tk image object.

        :param int width:
            The required width of the image, set to `None`, to keep the
            original image width

        :param int height:
            The required height of the image, set to `None`, to keep the
            original image width.
        """
        self._image_source = image_source
        self._pil_image = None
        self._tk_image = None
        self._tk_frames = []
        self._width = width
        self._height = height
        self._current_frame = 0
        self._animation = False
        self._animation_running = False
        self._setup_image()

    @property
    def image_source(self):
        """
        Returns the original source of the image, be that a file path, PIL or
        Tk image object.
        """
        return self._image_source

    @property
    def tk_image(self):
        """
        Returns the Tk PhotoImage object.
        """
        return self._tk_image

    @property
    def pil_image(self):
        """
        Returns the PIL Image object.
        """
        return self._pil_image

    @property
    def width(self):
        """
        Returns the image width.
        """
        return int(self._width)

    @property
    def height(self):
        """
        Returns the image height.
        """
        return int(self._height)

    @property
    def animation(self):
        """
        Returns `True` if the image contains more than 1 frame (i.e. is an
        animation)
        """
        return self._animation

    @property
    def tk_frames(self):
        """
        Returns a list of frames as Tk PhotoImage objects which make up this
        image.
        """
        return self._tk_frames

    def _setup_image(self):
        try:
            self._open_image_source()
            self._size_image()
            self._open_image_frames()
        except Exception as e:
            try:
                error_text = "Image import error - '{}'\n".format(e)
                error_text += 'Check the file path and image type is {}'.format('/'.join(system_config.supported_image_types))
                raise_error(error_text)
            finally:
                e = None
                del e

    def _open_image_source(self):
        if system_config.PIL_available:
            if isinstance(self._image_source, str):
                self._pil_image = Image.open(self._image_source)
                self._tk_image = ImageTk.PhotoImage(self._pil_image)
            elif Image.isImageType(self._image_source):
                self._pil_image = self._image_source
                self._tk_image = ImageTk.PhotoImage(self._pil_image)
            elif isinstance(self._image_source, (PhotoImage, ImageTk.PhotoImage)):
                self._tk_image = self._image_source
            else:
                raise Exception('Image must be a file path, PIL.Image or tkinter.PhotoImage')
        elif isinstance(self._image_source, str):
            self._tk_image = PhotoImage(file=(self._image_source))
        else:
            if isinstance(self._image_source, PhotoImage):
                self._tk_image = self._image_source
            else:
                raise Exception('Image must be a file path or tkinter.PhotoImage')

    def _size_image(self):
        if self._width is None:
            self._width = self._tk_image.width()
        else:
            if self._height is None:
                self._height = self._tk_image.height()
            if self._width != self._tk_image.width() or self._height != self._tk_image.height():
                if self._pil_image:
                    resized_image = self._pil_image.resize((self._width, self._height), Image.ANTIALIAS)
                    self._tk_image = ImageTk.PhotoImage(resized_image)
                else:
                    error_format('Image resizing - cannot scale the image as PIL is not available.')

    def _open_image_frames(self):
        if self._pil_image:
            frame_count = 0
            try:
                while True:
                    self._pil_image.seek(frame_count)
                    tk_frame = ImageTk.PhotoImage(self._pil_image.resize((self._width, self._height), Image.ANTIALIAS))
                    try:
                        delay = self._pil_image.info['duration']
                    except:
                        delay = 100

                    self._tk_frames.append((tk_frame, delay))
                    frame_count += 1

            except EOFError as e:
                try:
                    pass
                finally:
                    e = None
                    del e

            if frame_count > 1:
                self._animation = True


class AnimationPlayer:

    def __init__(self, master, guizero_image, update_image_callback):
        """
        AnimationPlayer manages the playing of a animated gif for guizero
        widgets.

        :param Widget master:
            The widget which is displaying the animation.

        :param GUIZeroImage guizero_image:
            The image object which contains the animation.

        :param function update_image_callback:
            A function which should be called when the Image needs updating.
            The function will be called and passed a reference to the next
            Tk PhotoImage object in the animation.
        """
        self._master = master
        self._guizero_image = guizero_image
        self._update_image_callback = update_image_callback
        self._current_frame = 0
        self._running = False
        self.start()

    @property
    def running(self):
        """
        Returns `True` if the animation is running
        """
        return self._running

    def start(self):
        """
        Starts the animation.
        """
        if not self._running:
            self._running = True
            self._show_frame()

    def stop(self):
        """
        Stops the animation
        """
        self._running = False

    def _show_frame(self):
        if self.running:
            frame_data = self._guizero_image.tk_frames[self._current_frame]
            frame = frame_data[0]
            delay = frame_data[1]
            self._update_image_callback(frame)
            self._current_frame += 1
            if self._current_frame == len(self._guizero_image.tk_frames):
                self._current_frame = 0
            self._master.after(delay, self._show_frame)


class TriggeredList(MutableSequence):

    def __init__(self, iterable=(), on_change=None):
        """
        A list which will call a callback when a value is changed.

        Used to hold a widgets grid reference.  
        """
        self._list = list(iterable)
        self._on_change = on_change

    def __getitem__(self, key):
        return self._list.__getitem__(key)

    def __setitem__(self, key, item):
        self._list.__setitem__(key, item)
        self._changed()

    def __delitem__(self, key):
        self._list.__delitem__(key)
        self._changed()

    def __len__(self):
        return self._list.__len__()

    def insert(self, index, item):
        self._list.insert(index, item)
        self._changed()

    def _changed(self):
        if self._on_change is not None:
            self._on_change()

    def __str__(self):
        data = '['
        for item in self._list:
            data = data + str(item) + ', '

        data = data[:-2] + ']'
        return data


def with_args(func_name, *args):
    return lambda : func_name(*args)


def no_args_expected(func_name):
    args = getfullargspec(func_name).args
    if len(args) > 0:
        if args[0] == 'self':
            return len(args) - 1
        return len(args)
    else:
        return 0


def error_format(message):
    print('------------------------------------------------------------')
    print('*** GUIZERO WARNING ***')
    print(message)
    print('------------------------------------------------------------')


def raise_error(message):
    error_message = '\n------------------------------------------------------------\n'
    error_message += '*** GUIZERO ERROR ***\n'
    error_message += message + '\n'
    error_message += '------------------------------------------------------------\n'
    raise GUIZeroException(error_message)


def deprecated(message):
    print('*** DEPRECATED: ' + message)


def convert_color(color):
    """
    Converts a color from "color", (255, 255, 255) or "#ffffff" into a color tk 
    should understand.
    """
    if color is not None:
        if isinstance(color, str):
            color = color.strip()
            if color[0] == '#':
                if len(color) != 7:
                    raise ValueError('{} is not a valid # color, it must be in the format #ffffff.'.format(color))
                else:
                    hex_colors = (
                     color[1:3], color[3:5], color[5:7])
                    for hex_color in hex_colors:
                        try:
                            int_color = int(hex_color, 16)
                        except:
                            raise ValueError('{} is not a valid value, it must be hex 00 - ff'.format(hex_color))

                        if not 0 <= int_color <= 255:
                            raise ValueError('{} is not a valid color value, it must be 00 - ff'.format(hex_color))

        else:
            try:
                no_of_colors = len(color)
            except:
                raise ValueError('A color must be a list or tuple of 3 values (red, green, blue)')

            if no_of_colors != 3:
                raise ValueError('A color must contain 3 values (red, green, blue)')
            for c in color:
                if not 0 <= c <= 255:
                    raise ValueError('{} is not a valid color value, it must be 0 - 255')

            color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
    return color