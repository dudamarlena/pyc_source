# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/illustrations.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 5373 bytes
"""Set of icons for buttons.

Use :func:`getQIcon` to create Qt QIcon from the name identifying an icon.
"""
__authors__ = [
 'T. Vincent']
__license__ = 'MIT'
__date__ = '06/09/2017'
import os, logging, weakref
from silx.gui import qt
import tomwer.resources
_logger = logging.getLogger(__name__)
_cached_icons = weakref.WeakValueDictionary()
_supported_formats = None

def getQIcon(name):
    """Create a QIcon from its name.

    The resource name can be prefixed by the name of a resource directory. For
    example "silx:foo.png" identify the resource "foo.png" from the resource
    directory "silx".

    If no prefix are specified, the file with be returned from the silx
    resource directory with a specific path "gui/icons".

    See also :func:`silx.resources.register_resource_directory`.

    :param str name: Name of the icon, in one of the defined icons
                     in this module.
    :return: Corresponding QIcon
    :raises: ValueError when name is not known
    """
    qfile = getQFile(name)
    pixmap = qt.QPixmap(qfile.fileName())
    icon = qt.QIcon(pixmap)
    return icon


def getQPixmap(name):
    """Create a QPixmap from its name.

    The resource name can be prefixed by the name of a resource directory. For
    example "silx:foo.png" identify the resource "foo.png" from the resource
    directory "silx".

    If no prefix are specified, the file with be returned from the silx
    resource directory with a specific path "gui/icons".

    See also :func:`silx.resources.register_resource_directory`.

    :param str name: Name of the icon, in one of the defined icons
                     in this module.
    :return: Corresponding QPixmap
    :raises: ValueError when name is not known
    """
    qfile = getQFile(name)
    if qfile is None:
        raise ValueError('Not an illustration name: %s' % name)
    return qt.QPixmap(qfile.fileName())


def getQFile(name):
    """Create a QFile from an icon name. Filename is found
    according to supported Qt formats.

    The resource name can be prefixed by the name of a resource directory. For
    example "silx:foo.png" identify the resource "foo.png" from the resource
    directory "silx".

    If no prefix are specified, the file with be returned from the silx
    resource directory with a specific path "gui/icons".

    See also :func:`silx.resources.register_resource_directory`.

    :param str name: Name of the icon, in one of the defined icons
                     in this module.
    :return: Corresponding QFile
    :rtype: qt.QFile
    :raises: ValueError when name is not known
    """
    global _supported_formats
    _name = name.replace(' ', '_')
    if '.' in _name:
        return _getQFile(_name)
        if _supported_formats is None:
            _supported_formats = []
            supported_formats = qt.supportedImageFormats()
            order = ['mng', 'gif', 'svg', 'png', 'jpg']
            for format_ in order:
                if format_ in supported_formats:
                    _supported_formats.append(format_)

            if len(_supported_formats) == 0:
                _logger.error('No format supported for icons')
    else:
        _logger.debug('Format %s supported', ', '.join(_supported_formats))
    for format_ in _supported_formats:
        format_ = str(format_)
        out = _getQFile('%s.%s' % (_name, format_))
        if out and out.exists():
            return out

    raise ValueError('Not an illustration name: %s' % _name)


def getResourceFileName(name):
    return tomwer.resources._resource_filename(name,
      default_directory=(os.path.join('gui', 'illustrations')))


def _getQFile(name):
    filename = tomwer.resources._resource_filename(name,
      default_directory=(os.path.join('gui', 'illustrations')))
    qfile = qt.QFile(filename)
    if qfile.exists():
        return qfile
    return