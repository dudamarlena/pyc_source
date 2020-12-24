# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/resource/taurus_resource_utils.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides widgets that display the database in a tree format"""
__all__ = [
 'getPixmap',
 'getIcon',
 'getThemePixmap',
 'getThemeIcon',
 'getThemeMembers',
 'getStandardIcon',
 'getElementTypeToolTip',
 'getElementTypeSize',
 'getElementTypeIcon',
 'getElementTypeIconName',
 'getElementTypePixmap',
 'getDevStateToolTip',
 'getDevStateIcon',
 'getDevStatePixmap']
__docformat__ = 'restructuredtext'
import os
from taurus.external.qt import Qt
from taurus.core.util.log import deprecated, taurus4_deprecation, deprecation_decorator
from taurus.qt.qtgui.icon import *

@deprecation_decorator(alt='QIcon.hasThemeIcon to test individual names', rel='4.0')
def getThemeMembers():
    """Returns the current icon theme elements

    .. note:: Since its depredation, it returns an empty dict (there is no
    reasonable way of introspecting the list of available icon names).
    Alternatively Just test a given name using

    :return: the current icon theme elements in a dictionary where each key is
             a group name and the value is a sequence of theme icon name.
    :rtype: dict<str,seq<str>>"""
    return {}


def getPixmap(key, size=None):
    if key.startswith(':'):
        head, tail = os.path.split(key[1:])
        prefix = sanitizePrefix(head or 'logos')
        alt = 'getCachedPixmap("%s:%s [, size]")' % (prefix, tail)
        ret = getCachedPixmap('%s:%s' % (prefix, tail), size)
    deprecated(dep='getPixmap("%s" [, size])' % key, alt=alt, rel='4.0')
    return ret


def getIcon(key):
    """Returns a PyQt4.QtGui.QIcon object for the given key. It supports QDir's
    searchPath prefixes (see :meth:`QDir.setSearchPaths`).
    Note that taurus.qt.qtgui.resource already sets several search paths based
    on .path files

    :param key: (str) the pixmap file name. (optionally with a prefix)

    :return: (PyQt4.QtGui.QIcon) a PyQt4.QtGui.QIcon for the given key"""
    if key.startswith(':'):
        head, tail = os.path.split(key[1:])
        prefix = sanitizePrefix(head or 'logos')
        alt = 'Qt.QIcon("%s:%s")' % (prefix, tail)
        ret = Qt.QIcon('%s:%s' % (prefix, tail))
    elif not Qt.QFile.exists(key) and Qt.QIcon.hasThemeIcon(key):
        alt = 'QIcon.fromTheme("%s")' % key
        ret = Qt.QIcon.fromTheme(key)
    else:
        alt = 'QIcon("%s")' % key
        ret = Qt.QIcon(key)
    deprecated(dep='getIcon("%s")' % key, alt=alt, rel='4.0')
    return ret


@deprecation_decorator(alt='QIcon.fromTheme(key).pixmap(size, size)', rel='4.0')
def getThemePixmap(key, size=48):
    """Returns a PyQt4.QtGui.QPixmap object for the given key and size.
    Key should be a valid theme icon key. See :meth:`PyQt4.QIcon.fromTheme`.

    Note that if the OS does not define a theme, taurus.qt.qtgui.resource will
    use the bundled 'Tango' icons theme. See:
    `Tango Icon Library <http://tango.freedesktop.org/Tango_Icon_Library>`_.

    If the key cannot be found, it will return a null content Pixmap.

    :param key: (str) a string with the pixmap theme key (ex.: 'folder_open')
    :param size: (int) the pixmap size in pixels (will get a square pixmap).
                 Default size=48

    :return: (PyQt4.QtGui.QPixmap)
    """
    return Qt.QIcon.fromTheme(key).pixmap(size, size)


@deprecation_decorator(alt='QIcon.fromTheme', rel='4.0')
def getThemeIcon(key):
    """Returns the theme icon corresponding to the given key.
    Key should be a valid theme icon key. See :meth:`PyQt4.QIcon.fromTheme`.

    Note that if the OS does not define a theme, taurus.qt.qtgui.resource will
    use the bundled 'Tango' icons theme. See:
    `Tango Icon Library <http://tango.freedesktop.org/Tango_Icon_Library>`_.

    :param key: (str) a string with the icon theme key (e.g.: 'folder_open')

    :return: (PyQt4.QtGui.QIcon) a PyQt4.QtGui.QIcon for the given theme key
    """
    return Qt.QIcon.fromTheme(key)


@taurus4_deprecation(alt='getDevStateToolTip')
def getSWDevHealthToolTip(state):
    return getDevStateToolTip(state)


@taurus4_deprecation(alt='getDevStateIcon')
def getSWDevHealthIcon(state, fallback=None):
    return getDevStateIcon(state, fallback=fallback)


@taurus4_deprecation(alt='getDevStatePixmap')
def getSWDevHealthPixmap(state, fallback=None):
    return getDevStatePixmap(state, fallback=fallback)


if __name__ == '__main__':
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None)
    themekey = 'computer'
    b = Qt.QIcon.fromTheme(themekey)
    icons = [
     getIcon('actions:edit-cut.svg'),
     getIcon(':/actions/edit-cut.svg'),
     getIcon(':/apps/preferences-system-session.svg'),
     getIcon(':/designer/devs_tree.png'),
     getIcon(':/actions/process-stop.svg'),
     getIcon(':/actions/add.svg'),
     getIcon(':/actions/stop.svg'),
     getIcon(':taurus.svg'),
     getIcon('computer'),
     getThemeIcon('computer')]
    w = Qt.QWidget()
    l = Qt.QVBoxLayout()
    w.setLayout(l)
    for icon in icons:
        button = Qt.QPushButton(icon, 'kk')
        l.addWidget(button)

    w.show()
    sys.exit(app.exec_())