# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/image/codecs/quicktime.py
# Compiled at: 2009-02-07 06:48:49
"""
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: pil.py 163 2006-11-13 04:15:46Z Alex.Holkner $'
import sys
from ctypes import *
from pyglet.gl import *
from pyglet.image import *
from pyglet.image.codecs import *
from pyglet.window.carbon import carbon, quicktime, _oscheck
from pyglet.window.carbon.constants import _name
from pyglet.window.carbon.types import *
Handle = POINTER(POINTER(c_byte))
GWorldPtr = c_void_p
carbon.NewHandle.restype = Handle
HandleDataHandlerSubType = _name('hndl')
PointerDataHandlerSubType = _name('ptr ')
kDataHCanRead = 1
kDataRefExtensionFileName = _name('fnam')
kDataRefExtensionMIMEType = _name('mime')
ComponentInstance = c_void_p
k1MonochromePixelFormat = 1
k2IndexedPixelFormat = 2
k4IndexedPixelFormat = 4
k8IndexedPixelFormat = 8
k16BE555PixelFormat = 16
k24RGBPixelFormat = 24
k32ARGBPixelFormat = 32
k32BGRAPixelFormat = _name('BGRA')
k1IndexedGrayPixelFormat = 33
k2IndexedGrayPixelFormat = 34
k4IndexedGrayPixelFormat = 36
k8IndexedGrayPixelFormat = 40
kNativeEndianPixMap = 256
newMovieActive = 1
noErr = 0
movieTrackMediaType = 1
movieTrackCharacteristic = 2
movieTrackEnabledOnly = 4
VisualMediaCharacteristic = _name('eyes')
nextTimeMediaSample = 1

class PointerDataRefRecord(Structure):
    _fields_ = [
     (
      'data', c_void_p),
     (
      'dataLength', c_long)]


def Str255(value):
    return create_string_buffer(chr(len(value)) + value)


class QuickTimeImageDecoder(ImageDecoder):

    def get_file_extensions(self):
        return [
         '.bmp', '.cur', '.gif', '.ico', '.jpg', '.jpeg', '.pcx', '.png',
         '.tga', '.tif', '.tiff', '.xbm', '.xpm']

    def get_animation_file_extensions(self):
        return [
         '.gif']

    def _get_data_ref(self, file, filename):
        self._data_hold = data = create_string_buffer(file.read())
        dataref = carbon.NewHandle(sizeof(PointerDataRefRecord))
        datarec = cast(dataref, POINTER(POINTER(PointerDataRefRecord))).contents.contents
        datarec.data = addressof(data)
        datarec.dataLength = len(data)
        self._data_handler_holder = data_handler = ComponentInstance()
        r = quicktime.OpenADataHandler(dataref, PointerDataHandlerSubType, None, 0, None, kDataHCanRead, byref(data_handler))
        _oscheck(r)
        extension_handle = Handle()
        self._filename_hold = filename = Str255(filename)
        r = carbon.PtrToHand(filename, byref(extension_handle), len(filename))
        r = quicktime.DataHSetDataRefExtension(data_handler, extension_handle, kDataRefExtensionFileName)
        _oscheck(r)
        quicktime.DisposeHandle(extension_handle)
        quicktime.DisposeHandle(dataref)
        dataref = c_void_p()
        r = quicktime.DataHGetDataRef(data_handler, byref(dataref))
        _oscheck(r)
        quicktime.CloseComponent(data_handler)
        return dataref

    def _get_formats(self):
        if sys.byteorder == 'big':
            format = 'ARGB'
            qtformat = k32ARGBPixelFormat
        else:
            format = 'BGRA'
            qtformat = k32BGRAPixelFormat
        return (
         format, qtformat)

    def decode(self, file, filename):
        dataref = self._get_data_ref(file, filename)
        importer = ComponentInstance()
        quicktime.GetGraphicsImporterForDataRef(dataref, PointerDataHandlerSubType, byref(importer))
        if not importer:
            raise ImageDecodeException(filename or file)
        rect = Rect()
        quicktime.GraphicsImportGetNaturalBounds(importer, byref(rect))
        width = rect.right
        height = rect.bottom
        (format, qtformat) = self._get_formats()
        buffer = (c_byte * (width * height * len(format)))()
        world = GWorldPtr()
        quicktime.QTNewGWorldFromPtr(byref(world), qtformat, byref(rect), c_void_p(), c_void_p(), 0, buffer, len(format) * width)
        quicktime.GraphicsImportSetGWorld(importer, world, c_void_p())
        result = quicktime.GraphicsImportDraw(importer)
        quicktime.DisposeGWorld(world)
        if result != 0:
            raise ImageDecodeException(filename or file)
        pitch = len(format) * width
        return ImageData(width, height, format, buffer, -pitch)

    def decode_animation(self, file, filename):
        quicktime.EnterMovies()
        data_ref = self._get_data_ref(file, filename)
        if not data_ref:
            raise ImageDecodeException(filename or file)
        movie = c_void_p()
        id = c_short()
        result = quicktime.NewMovieFromDataRef(byref(movie), newMovieActive, 0, data_ref, PointerDataHandlerSubType)
        if not movie:
            raise ImageDecodeException(filename or file)
        quicktime.GoToBeginningOfMovie(movie)
        time_scale = float(quicktime.GetMovieTimeScale(movie))
        (format, qtformat) = self._get_formats()
        rect = Rect()
        quicktime.GetMovieBox(movie, byref(rect))
        width = rect.right
        height = rect.bottom
        pitch = len(format) * width
        buffer = (c_byte * (width * height * len(format)))()
        world = GWorldPtr()
        quicktime.QTNewGWorldFromPtr(byref(world), qtformat, byref(rect), c_void_p(), c_void_p(), 0, buffer, len(format) * width)
        quicktime.SetGWorld(world, 0)
        quicktime.SetMovieGWorld(movie, world, 0)
        visual = quicktime.GetMovieIndTrackType(movie, 1, VisualMediaCharacteristic, movieTrackCharacteristic)
        if not visual:
            raise ImageDecodeException('No video track')
        time = 0
        interesting_time = c_int()
        quicktime.GetTrackNextInterestingTime(visual, nextTimeMediaSample, time, 1, byref(interesting_time), None)
        duration = interesting_time.value / time_scale
        frames = []
        while time >= 0:
            result = quicktime.GetMoviesError()
            if result == noErr:
                result = quicktime.UpdateMovie(movie)
            if result == noErr:
                quicktime.MoviesTask(movie, 0)
                result = quicktime.GetMoviesError()
            _oscheck(result)
            buffer_copy = (c_byte * len(buffer))()
            memmove(buffer_copy, buffer, len(buffer))
            image = ImageData(width, height, format, buffer_copy, -pitch)
            frames.append(AnimationFrame(image, duration))
            interesting_time = c_int()
            duration = c_int()
            quicktime.GetTrackNextInterestingTime(visual, nextTimeMediaSample, time, 1, byref(interesting_time), byref(duration))
            quicktime.SetMovieTimeValue(movie, interesting_time)
            time = interesting_time.value
            duration = duration.value / time_scale
            if duration <= 0.01:
                duration = 0.1

        quicktime.DisposeMovie(movie)
        carbon.DisposeHandle(data_ref)
        quicktime.ExitMovies()
        return Animation(frames)


def get_decoders():
    return [
     QuickTimeImageDecoder()]


def get_encoders():
    return []