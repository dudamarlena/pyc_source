# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/file_series.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 28551 bytes
"""

Authors:
........

* Henning O. Sorensen & Erik Knudsen
  Center for Fundamental Research: Metal Structures in Four Dimensions
  Risoe National Laboratory
  Frederiksborgvej 399
  DK-4000 Roskilde
  email:erik.knudsen@risoe.dk
* Jon Wright, ESRF

"""
from __future__ import absolute_import, print_function, with_statement, division
import logging, sys, os.path, collections
logger = logging.getLogger(__name__)
import fabio
from .fabioutils import FilenameObject, next_filename
from .openimage import openimage
from .fabioimage import FabioImage
from .utils import deprecation

def new_file_series0(first_object, first=None, last=None, step=1):
    """
    Created from a fabio image
    first and last are file numbers

    """
    im = first_object
    nimages = 0
    if None in (first, last):
        step = 0
        total = 1
    else:
        total = last - first
    yield im
    while nimages < total:
        nimages += step
        try:
            newim = im.next()
            im = newim
        except Exception as error:
            logger.warning('Got a problem here: %s', error)
            logger.debug('Backtrace', exc_info=True)
            try:
                im.filename = next_filename(im.filename)
            except Exception as error:
                logger.warning('Got another problem here: %s', error)
                im.filename = next_filename(im.sequencefilename)

            yield

        yield im


def new_file_series(first_object, nimages=0, step=1, traceback=False):
    """
    A generator function that creates a file series starting from a fabioimage.
    Iterates through all images in a file (if more than 1), then proceeds to
    the next file as determined by fabio.next_filename.

    :param first_object: the starting fabioimage, which will be the first one yielded
        in the sequence
    :param nimages:  the maximum number of images to consider
        step: step size, will yield the first and every step'th image until nimages
        is reached.  (e.g. nimages = 5, step = 2 will yield 3 images (0, 2, 4)
    :param traceback: if True causes it to print a traceback in the event as a
        logging error. Otherwise the exception is logged as a debug message.
        the exception as it chooses
    :param yields: the next fabioimage in the series.
        In the event there is an exception, it yields the sys.exec_info for the
        exception instead.  sys.exec_info is a tuple:
        ( exceptionType, exceptionValue, exceptionTraceback )
        from which all the exception information can be obtained.

    Suggested usage:

    .. code-block:: python

        for obj in new_file_series( ... ):
            if not isinstance(obj, fabio.fabioimage.FabioImage):
                # In case of problem (missing images, non readable files, etc)
                # obj contains the result of exc_info
                traceback.print_exception(obj[0], obj[1], obj[2])
    """
    im = first_object
    nprocessed = 0
    abort = False
    if nimages > 0:
        yield im
        nprocessed += 1
    while nprocessed < nimages:
        try:
            newim = im.next()
            im = newim
            retVal = im
        except Exception as ex:
            retVal = sys.exc_info()
            logger.warning('Got a problem here: next() failed %s', ex)
            if traceback:
                logger.error('Backtrace', exc_info=True)
            else:
                logger.debug('Backtrace', exc_info=True)
            try:
                im.filename = next_filename(im.filename)
            except Exception as ex:
                logger.warning('Got another problem here: next_filename(im.filename) %s', ex)

        if nprocessed % step == 0:
            yield retVal
            retVal = None
            if abort:
                break
            nprocessed += 1


class file_series(list):
    __doc__ = '\n    Represents a series of files to iterate\n    has an idea of a current position to do next and prev\n\n    You also get from the list python superclass:\n       append\n       count\n       extend\n       insert\n       pop\n       remove\n       reverse\n       sort\n    '

    def __init__(self, list_of_strings):
        """
        Constructor:

        :param list_of_strings: arg should be a list of strings which are filenames

        """
        super(file_series, self).__init__(list_of_strings)
        self._current = 0

    def first(self):
        """
        First image in series

        """
        return self[0]

    def last(self):
        """
        Last in series

        """
        return self[(-1)]

    def previous(self):
        """
        Prev in a sequence

        """
        self._current -= 1
        return self[self._current]

    def current(self):
        """Current position in a sequence

        """
        return self[self._current]

    def next(self):
        """
        Next in a sequence

        """
        self._current += 1
        return self[self._current]

    def jump(self, num):
        """
        Goto a position in sequence

        """
        assert num < len(self) and num >= 0, 'num out of range'
        self._current = num
        return self[self._current]

    def len(self):
        """
        Number of files

        """
        return len(self)

    def first_image(self):
        """
        First image in a sequence

        :return: fabioimage

        """
        return openimage(self.first())

    def last_image(self):
        """
        Last image in a sequence

        :return: fabioimage

        """
        return openimage(self.last())

    def next_image(self):
        """
        Return the next image

        :return: fabioimage

        """
        return openimage(self.next())

    def previous_image(self):
        """
        Return the previous image

        :return: fabioimage

        """
        return openimage(self.previous())

    def jump_image(self, num):
        """
        Jump to and read image

        :return: fabioimage

        """
        return openimage(self.jump(num))

    def current_image(self):
        """
        Current image in sequence

        :return: fabioimage

        """
        return openimage(self.current())

    def first_object(self):
        """
        First image in a sequence

        :return: file_object
        """
        return FilenameObject(self.first())

    def last_object(self):
        """
        Last image in a sequence

        :return: file_object

        """
        return FilenameObject(self.last())

    def next_object(self):
        """
        Return the next image

        :return: file_object

        """
        return FilenameObject(self.next())

    def previous_object(self):
        """
        Return the previous image

        :return: file_object

        """
        return FilenameObject(self.previous())

    def jump_object(self, num):
        """
        Jump to and read image

        :return: file_object

        """
        return FilenameObject(self.jump(num))

    def current_object(self):
        """
        Current image in sequence

        :return: file_object

        """
        return FilenameObject(self.current())


class numbered_file_series(file_series):
    __doc__ = '\n    mydata0001.edf = "mydata" + 0001 + ".edf"\n    mydata0002.edf = "mydata" + 0002 + ".edf"\n    mydata0003.edf = "mydata" + 0003 + ".edf"\n    '

    def __init__(self, stem, first, last, extension, digits=4, padding='Y', step=1):
        """
        Constructor

        :param stem: first part of the name
        :param step: in case of every nth file
        :param padding: possibility for specifying that numbers are not padded with zeroes up to digits

        """
        if padding == 'Y':
            fmt = '%s%0' + str(digits) + 'd%s'
        else:
            fmt = '%s%i%s'
        strings = [fmt % (stem, i, extension) for i in range(first, last + 1, step)]
        super(numbered_file_series, self).__init__(strings)


class filename_series(object):
    __doc__ = 'Iterator through a list of files indexed by a number.\n\n    Supports `next`, `prevous` and jump accessors.\n\n    :param Union[str,FilenameObject] filename: The first filename of the\n        iteration.\n    '

    def __init__(self, filename):
        """ create from a filename (String)"""
        if isinstance(filename, FilenameObject):
            self.obj = filename
        else:
            self.obj = FilenameObject(filename=filename)

    def next(self):
        """ increment number """
        self.obj.num += 1
        return self.obj.tostring()

    def previous(self):
        """ decrement number """
        self.obj.num -= 1
        return self.obj.tostring()

    def current(self):
        """ return current filename string"""
        return self.obj.tostring()

    def jump(self, num):
        """ jump to a specific number """
        self.obj.num = num
        return self.obj.tostring()

    def next_image(self):
        """ returns the next image as a fabioimage """
        return openimage(self.next())

    def prev_image(self):
        """ returns the previos image as a fabioimage """
        return openimage(self.previous())

    def current_image(self):
        """ returns the current image as a fabioimage"""
        return openimage(self.current())

    def jump_image(self, num):
        """ returns the image number as a fabioimage"""
        return openimage(self.jump(num))

    def next_object(self):
        """ returns the next filename as a fabio.FilenameObject"""
        self.obj.num += 1
        return self.obj

    def previous_object(self):
        """ returns the previous filename as a fabio.FilenameObject"""
        self.obj.num -= 1
        return self.obj

    def current_object(self):
        """ returns the current filename as a fabio.FilenameObject"""
        return self.obj

    def jump_object(self, num):
        """ returns the filename num as a fabio.FilenameObject"""
        self.obj.num = num
        return self.obj


_FileDescription = collections.namedtuple('_FileDescription', [
 'filename', 'file_number', 'first_frame_number', 'nframes'])

def _filename_series_adapter(series):
    """Adapter to list all available files from a `filename_series` class.

    Without the adaptater `filename_series` will not list the first element,
    and will loop to the infinite.
    """
    assert isinstance(series, filename_series)
    filename = series.current()
    if not os.path.exists(filename):
        return
    yield filename
    if series.obj.num is None:
        return
    while True:
        filename = series.next()
        if not os.path.exists(filename):
            return
        yield filename


class FileSeries(FabioImage):
    __doc__ = 'Provide a `FabioImage` abstracting a file series.\n\n    This abstraction provide the set of the filenames as the container of\n    frames.\n\n    .. code-block:: python\n\n        # Sequencial access through all the frames\n        with FileSeries(filenames) as serie:\n            for frame in serie.frames():\n                frame.data\n                frame.header\n                frame.index                    # index inside the file series\n                frame.file_index               # index inside the file (edf, tif)\n                frame.file_container.filename  # name of the source file\n\n        # Random access to frames\n        with FileSeries(filenames) as serie:\n            frame = serie.get_frame(200)\n            frame = serie.get_frame(201)\n            frame = serie.get_frame(10)\n            frame = serie.get_frame(2)\n\n    Files of the series can be set using a list of filenames, an iterator or a\n    generator. It also supports a file series described using\n    :class:`filename_series` or :class:`file_series` objects.\n\n    .. code-block:: python\n\n        # Iterate known files\n        filenames = ["foo.edf", "bar.tif"]\n        serie = FileSeries(filenames=filenames)\n\n        # Iterate all images from foobar_0001.edf to 0003\n        filenames = numbered_file_series("foobar_", 1, 3, ".edf", digits=4)\n        serie = FileSeries(filenames=filenames)\n\n        # Iterate all images from foobar_0000.edf to the last consecutive number found\n        filenames = filename_series("foobar_0000.edf")\n        serie = FileSeries(filenames=filenames)\n\n    Options are provided to optimize a non-sequencial access by providing the\n    amount of frames stored per files. This options (`single_frame`, `fixed_frames` and\n    `fixed_frame_number`) can be used if we know an a priori on the way frames\n    are stored in the files (the exact same amount of frames par file).\n\n    .. code-block:: python\n\n        # Each files contains a single frame\n        serie = FileSeries(filenames=filenames, single_frame=True)\n\n        # Each files contains a fixed amout of frames.  This value is\n        # automatically found\n        serie = FileSeries(filenames=filenames, fixed_frames=True)\n\n        # Each files contains 100 frames (the last one could contain less)\n        serie = FileSeries(filenames=filenames, fixed_frame_number=100)\n    '
    DEFAULT_EXTENSIONS = []

    def __init__(self, filenames, single_frame=None, fixed_frames=None, fixed_frame_number=None):
        """
        Constructor

        :param Union[Generator,Iterator,List] filenames: Ordered list of filenames
            to process as a file series. It also can be a generator, and
            iterator, or `filename_series` or `file_series` objects.
        :param Union[Bool,None] single_frame: If True, all files are supposed to
            contain only one frame.
        :param Union[Bool,None] fixed_frames: If True, all files are supposed to
            contain the same amount of frames (this fixed amount will be reached
            from the first file of the serie).
        :param Union[Integer,None] fixed_frame_number: If set, all files are
            supposed to contain the same amount of frames (sepecified by this
            argument)
        """
        if isinstance(filenames, filename_series):
            filenames = _filename_series_adapter(filenames)
        if isinstance(filenames, list):
            self._FileSeries__filenames = filenames
            self._FileSeries__filename_generator = None
        else:
            self._FileSeries__filenames = []
            self._FileSeries__filename_generator = filenames
        self._FileSeries__current_fabio_file_index = -1
        self._FileSeries__current_fabio_file = None
        self._FileSeries__file_descriptions = None
        self._FileSeries__current_file_description = None
        if single_frame is not None:
            self._FileSeries__fixed_frames = True
            self._FileSeries__fixed_frame_number = 1
        else:
            if fixed_frame_number is not None:
                self._FileSeries__fixed_frames = True
                self._FileSeries__fixed_frame_number = int(fixed_frame_number)
            else:
                if fixed_frames is not None and fixed_frames:
                    self._FileSeries__fixed_frames = bool(fixed_frames)
                    self._FileSeries__fixed_frame_number = None
                else:
                    self._FileSeries__fixed_frames = False
                    self._FileSeries__fixed_frame_number = None
                    self._FileSeries__file_descriptions = []
        self._FileSeries__nframes = None
        self.use_edf_shortcut = True

    def close(self):
        """Close any IO handler openned."""
        if self._FileSeries__current_fabio_file is not None:
            self._FileSeries__current_fabio_file.close()
        self._FileSeries__current_fabio_file_index = -1
        self._FileSeries__current_fabio_file = None

    def __iter_filenames(self):
        """Returns an iterator throug all filenames of the file series."""
        for filename in self._FileSeries__filenames:
            yield filename

        if self._FileSeries__filename_generator is not None:
            for filename in self._FileSeries__filename_generator:
                self._FileSeries__filenames.append(filename)
                yield filename

            self._FileSeries__filename_generator = None

    def frames(self):
        """Returns an iterator throug all frames of all filenames of this
        file series."""
        import fabio.edfimage
        nframe = 0
        for filename in self._FileSeries__iter_filenames():
            if self.use_edf_shortcut:
                info = FilenameObject(filename=filename)
                if fabio.edfimage.EdfImage in info.codec_classes:
                    frames = fabio.edfimage.EdfImage.lazy_iterator(filename)
                    for frame in frames:
                        frame._set_container(self, nframe)
                        yield frame
                        nframe += 1

                continue
                with fabio.open(filename) as (image):
                    if image.nframes == 0:
                        pass
                    else:
                        if image.nframes == 1:
                            yield image
                        else:
                            for frame_num in range(image.nframes):
                                frame = image.get_frame(frame_num)
                                frame._set_container(self, nframe)
                                yield frame
                                nframe += 1

        self._FileSeries__nframes = nframe

    def __load_all_filenames(self):
        """Load all filenames using the generator.

        It is needed to know the number of frames.

        .. note:: If the generator do not have endding, it will result an
            infinite loop.
        """
        if self._FileSeries__filename_generator is not None:
            for next_filename in self._FileSeries__filename_generator:
                self._FileSeries__filenames.append(next_filename)

            self._FileSeries__filename_generator = None

    def __get_filename(self, file_number):
        """Returns the filename from it's file position.

        :param int file_number: Position of the file in the file series
        :rtype: str
        :raise IndexError: It the requested position is out of the available
            number of files
        """
        if file_number < len(self._FileSeries__filenames):
            filename = self._FileSeries__filenames[file_number]
        else:
            if self._FileSeries__filename_generator is not None:
                amount = file_number - len(self._FileSeries__filenames) + 1
                try:
                    for _ in range(amount):
                        next_filename = next(self._FileSeries__filename_generator)
                        self._FileSeries__filenames.append(next_filename)

                except StopIteration:
                    self._FileSeries__filename_generator = None

                if file_number < len(self._FileSeries__filenames):
                    filename = self._FileSeries__filenames[file_number]
                else:
                    raise IndexError("File number '%s' is not reachable" % file_number)
            else:
                raise IndexError('File number %s is not reachable' % file_number)
        return filename

    def __get_file(self, file_number):
        """Returns the opennned FabioImage from it's file position.

        :param int file_number: Position of the file in the file series
        :rtype: FabioImage
        :raise IndexError: It the requested position is out of the available
            number of files
        """
        if self._FileSeries__current_fabio_file_index == file_number:
            return self._FileSeries__current_fabio_file
        filename = self._FileSeries__get_filename(file_number)
        if self._FileSeries__current_fabio_file is not None:
            self._FileSeries__current_fabio_file.close()
        self._FileSeries__current_fabio_file_index = file_number
        self._FileSeries__current_fabio_file = fabio.open(filename)
        return self._FileSeries__current_fabio_file

    def __iter_file_descriptions(self):
        """Iter all file descriptions.

        Use a cached structure which grows according to the requestes.
        """
        assert self._FileSeries__file_descriptions is not None
        for description in self._FileSeries__file_descriptions:
            yield description

        if len(self._FileSeries__file_descriptions) > 0:
            description = self._FileSeries__file_descriptions[(-1)]
            last_frame_number = description.first_frame_number + description.nframes
        else:
            last_frame_number = 0
        while True:
            file_number = len(self._FileSeries__file_descriptions)
            try:
                filename = self._FileSeries__get_filename(file_number)
            except IndexError:
                break

            fabiofile = self._FileSeries__get_file(file_number)
            first_frame = last_frame_number
            nframes = fabiofile.nframes
            description = _FileDescription(filename, file_number, first_frame, nframes)
            self._FileSeries__file_descriptions.append(description)
            yield description
            last_frame_number = first_frame + nframes

    def __find_file_description(self, frame_number):
        """Returns a file description from a cached list of stored descriptions.

        :param int frame_number: A frame number
        :rtype: _FileDescription
        """
        assert self._FileSeries__file_descriptions is not None
        if self._FileSeries__current_file_description is not None:
            description = self._FileSeries__current_file_description
            last_frame_number = description.first_frame_number + description.nframes
            if description.first_frame_number <= frame_number < last_frame_number:
                pass
            return description
        for description in self._FileSeries__iter_file_descriptions():
            last_frame_number = description.first_frame_number + description.nframes
            if description.first_frame_number <= frame_number < last_frame_number:
                self._FileSeries__current_file_description = description
                return description

        raise IndexError('Frame %s is out of range' % frame_number)

    def __get_file_description(self, frame_number):
        """Returns file description at the frame number.

        :rtype: _FileDescription
        """
        if not self._FileSeries__fixed_frames:
            description = self._FileSeries__find_file_description(frame_number)
            return description
        if self._FileSeries__fixed_frame_number is None:
            fabiofile = self._FileSeries__get_file(0)
            self._FileSeries__fixed_frame_number = fabiofile.nframes
        file_number = frame_number // self._FileSeries__fixed_frame_number
        try:
            filename = self._FileSeries__get_filename(file_number)
        except IndexError:
            raise IndexError('Frame %s is out of range' % frame_number)

        first_frame = frame_number - frame_number % self._FileSeries__fixed_frame_number
        nframes = self._FileSeries__fixed_frame_number
        return _FileDescription(filename, file_number, first_frame, nframes)

    def _get_frame(self, num):
        """Returns the frame numbered `num` in the series as a fabioimage.

        :param int num: The number of the requested frame
        :rtype: FabioFrame
        """
        if num < 0:
            raise IndexError('Frame %s is out of range' % num)
        description = self._FileSeries__get_file_description(num)
        fileimage = self._FileSeries__get_file(description.file_number)
        local_frame = num - description.first_frame_number
        if not 0 <= local_frame < description.nframes:
            msg = "Index '%d' (local index '%d' from '%s') is out of range"
            raise IndexError(msg % (num, local_frame, description.filename))
        try:
            frame = fileimage._get_frame(local_frame)
        except IndexError:
            logger.debug('Backtrace', exc_info=True)
            msg = "Index '%d' (local index '%d' from '%s') is out of range"
            raise IndexError(msg % (num, local_frame, description.filename))

        frame._set_container(self, num)
        return frame

    @deprecation.deprecated(reason='Replaced by get_frame.', deprecated_since='0.10.0beta')
    def getframe(self, num):
        return self.get_frame(num)

    @property
    def nframes(self):
        """Returns the number of available frames in the full file series.

        :rtype: int
        """
        if self._FileSeries__nframes is not None:
            return self._FileSeries__nframes
        if not self._FileSeries__fixed_frames:
            for _ in self._FileSeries__iter_file_descriptions():
                pass

            if len(self._FileSeries__file_descriptions) == 0:
                self._FileSeries__nframes = 0
                return self._FileSeries__nframes
            description = self._FileSeries__file_descriptions[(-1)]
            self._FileSeries__nframes = description.first_frame_number + description.nframes
            return self._FileSeries__nframes
        if self._FileSeries__fixed_frame_number is None:
            try:
                fabiofile = self._FileSeries__get_file(0)
            except IndexError:
                self._FileSeries__nframes = 0
                return self._FileSeries__nframes

            self._FileSeries__fixed_frame_number = fabiofile.nframes
        self._FileSeries__load_all_filenames()
        if len(self._FileSeries__filenames) == 0:
            self._FileSeries__nframes = 0
            return self._FileSeries__nframes
        file_number = len(self._FileSeries__filenames) - 1
        fabiofile = self._FileSeries__get_file(file_number)
        nframes = self._FileSeries__fixed_frame_number * (len(self._FileSeries__filenames) - 1) + fabiofile.nframes
        self._FileSeries__nframes = nframes
        return nframes

    @property
    def data(self):
        raise NotImplementedError('Not implemented. Use serie.frames() or serie.get_frame(int)')

    @property
    def header(self):
        raise NotImplementedError('Not implemented. Use serie.frames() or serie.get_frame(int)')

    @property
    def shape(self):
        raise NotImplementedError('Not implemented. Use serie.frames() or serie.get_frame(int)')

    @property
    def dtype(self):
        raise NotImplementedError('Not implemented. Use serie.frames() or serie.get_frame(int)')