# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/fabioformats.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 7951 bytes
"""
Provide an API to all the supported formats
"""
__author__ = 'Valentin Valls'
__contact__ = 'valentin.valls@esrf.eu'
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__date__ = '15/03/2019'
__status__ = 'stable'
__docformat__ = 'restructuredtext'
import logging
_logger = logging.getLogger(__name__)
from . import fabioimage
from .fabioutils import OrderedDict
try:
    import importlib
    importer = importlib.import_module
except ImportError:

    def importer(module_name):
        module = __import__(module_name)
        names = module_name.split('.')
        names.pop(0)
        for name in names:
            module = getattr(module, name)

        return module


_default_codecs = [
 ('edfimage', 'EdfImage'),
 ('dtrekimage', 'DtrekImage'),
 ('tifimage', 'TifImage'),
 ('marccdimage', 'MarccdImage'),
 ('mar345image', 'Mar345Image'),
 ('fit2dmaskimage', 'Fit2dMaskImage'),
 ('brukerimage', 'BrukerImage'),
 ('bruker100image', 'Bruker100Image'),
 ('pnmimage', 'PnmImage'),
 ('GEimage', 'GeImage'),
 ('OXDimage', 'OxdImage'),
 ('dm3image', 'Dm3Image'),
 ('HiPiCimage', 'HipicImage'),
 ('pilatusimage', 'PilatusImage'),
 ('fit2dspreadsheetimage', 'Fit2dSpreadsheetImage'),
 ('kcdimage', 'KcdImage'),
 ('cbfimage', 'CbfImage'),
 ('xsdimage', 'XsdImage'),
 ('binaryimage', 'BinaryImage'),
 ('pixiimage', 'PixiImage'),
 ('raxisimage', 'RaxisImage'),
 ('numpyimage', 'NumpyImage'),
 ('eigerimage', 'EigerImage'),
 ('hdf5image', 'Hdf5Image'),
 ('fit2dimage', 'Fit2dImage'),
 ('speimage', 'SpeImage'),
 ('jpegimage', 'JpegImage'),
 ('jpeg2kimage', 'Jpeg2KImage'),
 ('mpaimage', 'MpaImage'),
 ('mrcimage', 'MrcImage'),
 ('esperantoimage', 'EsperantoImage'),
 ('adscimage', 'AdscImage')]
_registry = OrderedDict()
_extension_cache = None

def register(codec_class):
    """Register a class format to the core fabio library"""
    global _extension_cache
    assert issubclass(codec_class, fabioimage.FabioImage), 'Expected subclass of FabioImage class but found %s' % type(codec_class)
    _registry[codec_class.codec_name()] = codec_class
    _extension_cache = None


def register_default_formats():
    """Register all available default image classes provided by fabio.

    If a format is already registered, it will be overwriten
    """
    for module_name, class_name in _default_codecs:
        module = importer('fabio.' + module_name)
        codec_class = getattr(module, class_name)
        if codec_class is None:
            raise RuntimeError("Class name '%s' from mudule '%s' not found" % (class_name, module_name))
        register(codec_class)


def get_all_classes():
    """Returns the list of supported codec identified by there fabio classes.

    :rtype: list"""
    return _registry.values()


def get_classes(reader=None, writer=None):
    """
    Return available codecs according to filter

    :param bool reader: True to reach codecs providing reader or False to
        provide codecs which do not provided reader. If None, reader feature is
        not filtered
    :param bool writer: True to reach codecs providing writer or False to
        provide codecs which do not provided writer. If None, writer feature is
        not filtered
    :rtype: list
    """
    formats = []
    for f in get_all_classes():
        has_reader = f.read.__module__ != fabioimage.__name__
        has_writer = f.write.__module__ != fabioimage.__name__
        include_format = True
        if reader is not None and reader != has_reader:
            include_format = False
        if writer is not None and writer != has_writer:
            include_format = False
        if include_format:
            formats.append(f)

    return formats


def get_class_by_name(format_name):
    """
    Get a format class by its name.

    :param str format_name: Format name, for example, "edfimage"
    :return: instance of the new class
    """
    if format_name in _registry:
        return _registry[format_name]
    else:
        return


def _get_extension_mapping():
    """Returns a dictionary mapping file extension to the list of supported
    formats. The result is cached, do not edit it

    :rtype: dict
    """
    global _extension_cache
    if _extension_cache is None:
        _extension_cache = {}
        for codec in get_all_classes():
            if not hasattr(codec, 'DEFAULT_EXTENSIONS'):
                pass
            else:
                for ext in codec.DEFAULT_EXTENSIONS:
                    if ext not in _extension_cache:
                        _extension_cache[ext] = []
                    _extension_cache[ext].append(codec)

    return _extension_cache


def get_classes_from_extension(extension):
    """
    Returns list of supported file format classes from a file extension

    :param str extension: File extension, for example "edf"
    :return: fabio image class
    """
    mapping = _get_extension_mapping()
    extension = extension.lower()
    if extension in mapping:
        return list(mapping[extension])
    else:
        return []


def is_extension_supported(extension):
    """
    Returns true is the extension is supported.

    :param str format_name: Format name, for example, "edfimage"
    :return: instance of the new class
    """
    mapping = _get_extension_mapping()
    extension = extension.lower()
    return extension in mapping


def factory(name):
    """Factory of image using name of the codec class.

    :param str name: name of the class to instantiate
    :return: an instance of the class
    :rtype: fabio.fabioimage.FabioImage
    """
    name = name.lower()
    obj = None
    if name in _registry:
        obj = _registry[name]()
    else:
        msg = 'FileType %s is unknown !, please check if the filename exists or select one from %s' % (
         name, _registry.keys())
        _logger.debug(msg)
        raise RuntimeError(msg)
    return obj