# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/icon/icon.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides taurus-specific functions related to icons"""
__all__ = [
 'sanitizePrefix',
 'registerPathFiles',
 'registerTheme',
 'getCachedPixmap',
 'getStandardIcon',
 'getElementTypeToolTip',
 'getElementTypeSize',
 'getElementTypeIcon',
 'getElementTypeIconName',
 'getElementTypePixmap',
 'getDevStateToolTip',
 'getDevStateIcon',
 'getDevStatePixmap',
 'REGISTERED_PREFIXES']
__docformat__ = 'restructuredtext'
import os, re, sys, json
from taurus.external.qt import Qt
from taurus.core.taurusbasetypes import TaurusElementType, TaurusDevState
from taurus.core.util.log import Logger
__LOGGER = Logger(__name__)
__INITIALIZED = False
__DW = 70
__DH = 24
__DQS = Qt.QSize(__DW, __DH)
__1DQS = __DQS
__2DQS = Qt.QSize(2 * __DW, __DH)
__3DQS = Qt.QSize(3 * __DW, __DH)
__IDX_ELEM_TYPE_ICON, __IDX_ELEM_TYPE_SIZE, __IDX_ELEM_TYPE_TOOLTIP = list(range(3))
_ELEM_TYPE_MAP = {TaurusElementType.Name: (
                          'folder', __3DQS, None), 
   TaurusElementType.Device: (
                            'applications-system', Qt.QSize(210, __DH),
                            'Tango device name'), 
   TaurusElementType.DeviceAlias: (
                                 'applications-system', Qt.QSize(140, __DH),
                                 'Tango device alias'), 
   TaurusElementType.Domain: (
                            'folder', Qt.QSize(80, __DH),
                            'Tango device domain'), 
   TaurusElementType.Family: (
                            'folder', Qt.QSize(80, __DH),
                            'Tango device family'), 
   TaurusElementType.Member: (
                            'applications-system', Qt.QSize(80, __DH),
                            'Tango device member'), 
   TaurusElementType.Server: (
                            'application-x-executable', Qt.QSize(190, __DH),
                            'Tango server'), 
   TaurusElementType.ServerName: (
                                'application-x-executable',
                                Qt.QSize(80, __DH), 'Tango server name'), 
   TaurusElementType.ServerInstance: (
                                    'application-x-executable',
                                    Qt.QSize(80, __DH),
                                    'Tango server instance'), 
   TaurusElementType.DeviceClass: (
                                 'text-x-script', Qt.QSize(140, __DH),
                                 'Tango class name'), 
   TaurusElementType.Exported: (
                              'start-here', Qt.QSize(60, __DH),
                              'Alive/not alive'), 
   TaurusElementType.Host: (
                          'network-server', Qt.QSize(100, __DH),
                          'Host machine were last ran'), 
   TaurusElementType.Attribute: (
                               ':/actions/format-text-bold.svg',
                               Qt.QSize(100, __DH), 'Attribute name')}
__IDX_STATE_ICON, __IDX_STATE_TOOLTIP = list(range(2))
_STATE_MAP = {TaurusDevState.Ready: ('status:available.svg', 'Element ready'), 
   TaurusDevState.NotReady: ('status:not-available.svg', 'Element not ready'), 
   TaurusDevState.Undefined: ('status:not-known.svg', 'Element state undefined')}
REGISTERED_PREFIXES = set()

def sanitizePrefix(prefix):
    """strips any leading '/' and substitutes non alphanumeric characters by '_'
    """
    prefix = prefix.lstrip('/')
    return re.sub('[^0-9a-zA-Z]+', '_', prefix)


def registerPathFiles(pathfilenames):
    """
    Use given .path files to update Qt's search path
    Each path file contains a json-encoded list of (prefix,path) tuples.
    This function will call Qt.QDir.addSearchPath with each of the tuples
    from the path files (prefix values will be sanitized first, and relative
    path values will be made relative to the dir containing the .path file)

    :param pathfilenames: (list<str>) list of .path file names
    """
    for filename in pathfilenames:
        try:
            pathmap = json.load(open(filename))
        except Exception as e:
            __LOGGER.error('Error registering "%s": %r', filename, e)
            pathmap = []

        base_dir = os.path.abspath(os.path.dirname(filename))
        for prefix, path in pathmap:
            prefix = sanitizePrefix(prefix)
            path = os.path.join(base_dir, path)
            Qt.QDir.addSearchPath(prefix, path)
            REGISTERED_PREFIXES.add(prefix)


def registerTheme(name='Tango', path='', force=False):
    """Use bundled them if OS does not define a theme (non-X11 systems)

    :param name: (str) icon theme name (default=Tango)
    :param path: (str) path to dir containing the theme (absolute or relative
                 to dir of taurus.qt.qtgui.icon). Default = ''
    :param force: (bool) Force to set path even if a theme is already set
    """
    if force or not sys.platform.startswith('linux'):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base_dir, path)
        Qt.QIcon.setThemeSearchPaths([path])
        Qt.QIcon.setThemeName(name)
        __LOGGER.info('Setting %s icon theme (from %s)', name, path)


def getCachedPixmap(key, size=None):
    """Returns a PyQt4.QtGui.QPixmap object for the given key and size.
    The key argument supports QDir's searchPath prefixes (see
    :meth:`QDir.setSearchPaths`).

    :param key: (str) the pixmap key., e.g.: 'status:folder-open.svg'
    :param size: (int) the pixmap size in pixels (will get a square pixmap).
                If None is passed it will return the original size

    :return: (PyQt4.QtGui.QPixmap)"""
    name = key
    if size is not None:
        key += '_%sx%s' % (size, size)
    pm = Qt.QPixmapCache.find(key)
    if pm is None:
        pm = Qt.QPixmap(name)
        if size is not None:
            pm = pm.scaled(size, size, Qt.Qt.KeepAspectRatio, Qt.Qt.SmoothTransformation)
        Qt.QPixmapCache.insert(key, pm)
    return Qt.QPixmap(pm)


def getStandardIcon(key, widget=None):
    """Returns a PyQt4.QtGui.QIcon object for the given key. Key should be a
    QStyle.StandardPixmap enumeration member. The widget argument is optional
    and can also be used to aid the determination of the icon.

    :param key: (QStyle.StandardPixmap) a standard pixmap which can follow some
                existing GUI style or guideline
    :param widget: (Qt.QWidget) the widget argument (optional) can also be used
                   to aid the determination of the icon.

    :return: (PyQt4.QtGui.QIcon)"""
    styleOption = None
    if widget is not None:
        styleOption = Qt.QStyleOption()
        styleOption.initFrom(widget)
    style = Qt.QApplication.instance().style()
    return style.standardIcon(key, styleOption, widget)


def getElementTypeToolTip(elemType):
    data = _ELEM_TYPE_MAP.get(elemType)
    if data is None:
        return
    else:
        return data[__IDX_ELEM_TYPE_TOOLTIP]


def getElementTypeSize(elemType):
    data = _ELEM_TYPE_MAP.get(elemType)
    if data is None:
        return
    else:
        return data[__IDX_ELEM_TYPE_SIZE]


def getElementTypeIconName(elemType):
    """Gets an icon name string for the given
    :class:`taurus.core.taurusbasetypes.TaurusElementType`.

    If an icon name cannot be found for elemType, None is returned.

    :param elemType: (TaurusElementType) the taurus element type

    :return: (str) a string representing the icon name for the given
             :class:`taurus.core.taurusbasetypes.TaurusElementType`"""
    if elemType is None:
        return
    else:
        data = _ELEM_TYPE_MAP.get(elemType)
        if data is None:
            return
        return data[__IDX_ELEM_TYPE_ICON]


def getElementTypeIcon(elemType, fallback=None):
    """Gets a PyQt4.QtGui.QIcon object for the given
    :class:`taurus.core.taurusbasetypes.TaurusElementType`.

    If an icon cannot be found for the given TaurusElementType,
    fallback is returned.

    :param elemType: (TaurusElementType) the taurus element type
    :param fallback: (PyQt4.QtGui.QIcon) the fallback icon. Default is None.

    :return: (PyQt4.QtGui.QIcon)"""
    themeIconName = getElementTypeIconName(elemType)
    icon = Qt.QIcon.fromTheme(themeIconName)
    if icon.isNull() and fallback is not None:
        icon = fallback
    return icon


def getElementTypePixmap(elemType, size=None):
    """Gets a PyQt4.QtGui.QPixmap object for the given
    :class:`taurus.core.taurusbasetypes.TaurusElementType`.

    :param elemType: (TaurusElementType) the taurus element type
    :param size: (int) the pixmap size in pixels (will get a square pixmap).
                 Default is None meaning it will return the original size.

    :return: (PyQt4.QtGui.QPixmap or None)"""
    if elemType is None:
        return
    else:
        data = _ELEM_TYPE_MAP.get(elemType)
        if data is None:
            return
        themeKey = data[__IDX_ELEM_TYPE_ICON]
        return Qt.QIcon.fromTheme(themeKey, size).pixmap(size, size)


def getDevStateToolTip(state):
    data = _STATE_MAP.get(state)
    if data is None:
        return
    else:
        return data[__IDX_STATE_TOOLTIP]


def getDevStateIcon(state, fallback=None):
    """Gets a PyQt4.QtGui.QIcon object for the given
    :class:`taurus.core.taurusbasetypes.TaurusDevState`.

    If an icon cannot be found for the given state, fallback is returned.

    :param state: (TaurusDevState) the taurus device state
    :param fallback: (PyQt4.QtGui.QIcon) the fallback icon. Default is None.

    :return: (PyQt4.QtGui.QIcon or None)"""
    if state is None:
        return
    else:
        data = _STATE_MAP.get(state)
        if data is None:
            return
        name = data[__IDX_STATE_ICON]
        icon = Qt.QIcon(name)
        if icon.isNull() and fallback is not None:
            icon = fallback
        return icon


def getDevStatePixmap(state, size=None):
    """Gets a PyQt4.QtGui.QPixmap object for the given
    :class:`taurus.core.taurusbasetypes.TaurusDevState`.

    :param state: (TaurusDevState) the taurus software device state
    :param size: (int) the pixmap size in pixels (will get a square pixmap).
                 Default is None meaning it will return the original size.

    :return: (PyQt4.QtGui.QPixmap or None)
    """
    if state is None:
        return
    else:
        data = _STATE_MAP.get(state)
        if data is None:
            return
        name = data[__IDX_STATE_ICON]
        return getCachedPixmap(name, size)


if __name__ == '__main__':
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None)
    icons = [
     Qt.QIcon('NONEXISTENT/PATH'),
     Qt.QIcon(':/actions/edit-cut.svg'),
     Qt.QIcon(os.path.abspath('Tango/scalable/actions/edit-cut.svg')),
     Qt.QIcon('Tango/scalable/actions/edit-cut.svg'),
     Qt.QIcon('actions:edit-cut.svg'),
     Qt.QIcon('apps:preferences-system-session.svg'),
     Qt.QIcon('designer:devs_tree.png'),
     Qt.QIcon('actions:process-stop.svg'),
     Qt.QIcon('actions:add.svg'),
     Qt.QIcon('actions:stop.svg'),
     Qt.QIcon('logos:taurus.svg'),
     Qt.QIcon.fromTheme('computer')]
    w = Qt.QWidget()
    l = Qt.QVBoxLayout()
    w.setLayout(l)
    for icon in icons:
        button = Qt.QPushButton(icon, 'kk')
        l.addWidget(button)

    w.show()
    sys.exit(app.exec_())