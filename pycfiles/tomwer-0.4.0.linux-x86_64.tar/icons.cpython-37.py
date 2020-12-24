# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/icons.py
# Compiled at: 2019-12-17 04:06:55
# Size of source mod 2**32: 12947 bytes
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
import silx.utils as silxweakref
from silx.utils.deprecation import deprecated
_logger = logging.getLogger(__name__)
_cached_icons = weakref.WeakValueDictionary()
_supported_formats = None

class AbstractAnimatedIcon(qt.QObject):
    __doc__ = 'Store an animated icon.\n\n    It provides an event containing the new icon everytime it is updated.'

    def __init__(self, parent=None):
        """Constructor

        :param qt.QObject parent: Parent of the QObject
        :raises: ValueError when name is not known
        """
        qt.QObject.__init__(self, parent)
        self._AbstractAnimatedIcon__targets = silxweakref.WeakList()
        self._AbstractAnimatedIcon__currentIcon = None

    iconChanged = qt.Signal(qt.QIcon)

    def register(self, obj):
        """Register an object to the AnimatedIcon.
        If no object are registred, the animation is paused.
        Object are stored in a weaked list.

        :param object obj: An object
        """
        if obj not in self._AbstractAnimatedIcon__targets:
            self._AbstractAnimatedIcon__targets.append(obj)
        self._updateState()

    def unregister(self, obj):
        """Remove the object from the registration.
        If no object are registred the animation is paused.

        :param object obj: A registered object
        """
        if obj in self._AbstractAnimatedIcon__targets:
            self._AbstractAnimatedIcon__targets.remove(obj)
        self._updateState()

    def hasRegistredObjects(self):
        """Returns true if any object is registred.

        :rtype: bool
        """
        return len(self._AbstractAnimatedIcon__targets)

    def isRegistered(self, obj):
        """Returns true if the object is registred in the AnimatedIcon.

        :param object obj: An object
        :rtype: bool
        """
        return obj in self._AbstractAnimatedIcon__targets

    def currentIcon(self):
        """Returns the icon of the current frame.

        :rtype: qt.QIcon
        """
        return self._AbstractAnimatedIcon__currentIcon

    def _updateState(self):
        """Update the object according to the connected objects."""
        pass

    def _setCurrentIcon(self, icon):
        """Store the current icon and emit a `iconChanged` event.

        :param qt.QIcon icon: The current icon
        """
        self._AbstractAnimatedIcon__currentIcon = icon
        self.iconChanged.emit(self._AbstractAnimatedIcon__currentIcon)


class MovieAnimatedIcon(AbstractAnimatedIcon):
    __doc__ = 'Store a looping QMovie to provide icons for each frames.\n    Provides an event with the new icon everytime the movie frame\n    is updated.'

    def __init__(self, filename, parent=None):
        """Constructor

        :param str filename: An icon name to an animated format
        :param qt.QObject parent: Parent of the QObject
        :raises: ValueError when name is not known
        """
        AbstractAnimatedIcon.__init__(self, parent)
        qfile = getQFile(filename)
        self._MovieAnimatedIcon__movie = qt.QMovie(qfile.fileName(), qt.QByteArray(), parent)
        self._MovieAnimatedIcon__movie.setCacheMode(qt.QMovie.CacheAll)
        self._MovieAnimatedIcon__movie.frameChanged.connect(self._MovieAnimatedIcon__frameChanged)
        self._MovieAnimatedIcon__cacheIcons = {}
        self._MovieAnimatedIcon__movie.jumpToFrame(0)
        self._MovieAnimatedIcon__updateIconAtFrame(0)

    def __frameChanged(self, frameId):
        """Callback everytime the QMovie frame change
        :param int frameId: Current frame id
        """
        self._MovieAnimatedIcon__updateIconAtFrame(frameId)

    def __updateIconAtFrame(self, frameId):
        """
        Update the current stored QIcon

        :param int frameId: Current frame id
        """
        if frameId in self._MovieAnimatedIcon__cacheIcons:
            icon = self._MovieAnimatedIcon__cacheIcons[frameId]
        else:
            icon = qt.QIcon(self._MovieAnimatedIcon__movie.currentPixmap())
            self._MovieAnimatedIcon__cacheIcons[frameId] = icon
        self._setCurrentIcon(icon)

    def _updateState(self):
        """Update the movie play according to internal stat of the
        AnimatedIcon."""
        self._MovieAnimatedIcon__movie.setPaused(not self.hasRegistredObjects())


class MultiImageAnimatedIcon(AbstractAnimatedIcon):
    __doc__ = 'Store a looping QMovie to provide icons for each frames.\n    Provides an event with the new icon everytime the movie frame\n    is updated.'

    def __init__(self, filename, parent=None):
        """Constructor

        :param str filename: An icon name to an animated format
        :param qt.QObject parent: Parent of the QObject
        :raises: ValueError when name is not known
        """
        AbstractAnimatedIcon.__init__(self, parent)
        self._MultiImageAnimatedIcon__frames = []
        for i in range(100):
            try:
                pixmap = getQPixmap('%s/%02d' % (filename, i))
            except ValueError:
                break

            icon = qt.QIcon(pixmap)
            self._MultiImageAnimatedIcon__frames.append(icon)

        if len(self._MultiImageAnimatedIcon__frames) == 0:
            raise ValueError("Animated icon '%s' do not exists" % filename)
        self._MultiImageAnimatedIcon__frameId = -1
        self._MultiImageAnimatedIcon__timer = qt.QTimer(self)
        self._MultiImageAnimatedIcon__timer.timeout.connect(self._MultiImageAnimatedIcon__increaseFrame)
        self._MultiImageAnimatedIcon__updateIconAtFrame(0)

    def __increaseFrame(self):
        """Callback called every timer timeout to change the current frame of
        the animation
        """
        frameId = (self._MultiImageAnimatedIcon__frameId + 1) % len(self._MultiImageAnimatedIcon__frames)
        self._MultiImageAnimatedIcon__updateIconAtFrame(frameId)

    def __updateIconAtFrame(self, frameId):
        """
        Update the current stored QIcon

        :param int frameId: Current frame id
        """
        self._MultiImageAnimatedIcon__frameId = frameId
        icon = self._MultiImageAnimatedIcon__frames[frameId]
        self._setCurrentIcon(icon)

    def _updateState(self):
        """Update the object to wake up or sleep it according to its use."""
        if self.hasRegistredObjects():
            self._MultiImageAnimatedIcon__timer.isActive() or self._MultiImageAnimatedIcon__timer.start(100)
        else:
            if self._MultiImageAnimatedIcon__timer.isActive():
                self._MultiImageAnimatedIcon__timer.stop()


class AnimatedIcon(MovieAnimatedIcon):
    __doc__ = 'Store a looping QMovie to provide icons for each frames.\n    Provides an event with the new icon everytime the movie frame\n    is updated.\n\n    It may not be available anymore for the silx release 0.6.\n\n    .. deprecated:: 0.5\n       Use :class:`MovieAnimatedIcon` instead.\n    '

    @deprecated
    def __init__(self, filename, parent=None):
        MovieAnimatedIcon.__init__(self, filename, parent=parent)


def getWaitIcon():
    """Returns a cached version of the waiting AbstractAnimatedIcon.

    :rtype: AbstractAnimatedIcon
    """
    return getAnimatedIcon('process-working')


def getAnimatedIcon(name):
    """Create an AbstractAnimatedIcon from a resource name.

    The resource name can be prefixed by the name of a resource directory. For
    example "silx:foo.png" identify the resource "foo.png" from the resource
    directory "silx".

    If no prefix are specified, the file with be returned from the silx
    resource directory with a specific path "gui/icons".

    See also :func:`silx.resources.register_resource_directory`.

    Try to load a mng or a gif file, then try to load a multi-image animated
    icon.

    In Qt5 mng or gif are not used, because the transparency is not very well
    managed.

    :param str name: Name of the icon, in one of the defined icons
                     in this module.
    :return: Corresponding AbstractAnimatedIcon
    :raises: ValueError when name is not known
    """
    key = name + '__anim'
    if key not in _cached_icons:
        qtMajorVersion = int(qt.qVersion().split('.')[0])
        icon = None
        if qtMajorVersion != 5:
            try:
                icon = MovieAnimatedIcon(name)
            except ValueError:
                icon = None

        if icon is None:
            try:
                icon = MultiImageAnimatedIcon(name)
            except ValueError:
                icon = None

        if icon is None:
            raise ValueError('Not an animated icon name: %s', name)
        _cached_icons[key] = icon
    else:
        icon = _cached_icons[key]
    return icon


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
    if name not in _cached_icons:
        qfile = getQFile(name)
        pixmap = qt.QPixmap(qfile.fileName())
        icon = qt.QIcon(pixmap)
        _cached_icons[name] = icon
    else:
        icon = _cached_icons[name]
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
    if _supported_formats is None:
        _supported_formats = []
        supported_formats = qt.supportedImageFormats()
        order = ['svg', 'png', 'jpg']
        for format_ in order:
            if format_ in supported_formats:
                _supported_formats.append(format_)

        if len(_supported_formats) == 0:
            _logger.error('No format supported for icons')
        else:
            _logger.debug('Format %s supported', ', '.join(_supported_formats))
    for format_ in _supported_formats:
        format_ = str(format_)
        filename = tomwer.resources._resource_filename(('%s.%s' % (name, format_)), default_directory=(os.path.join('gui', 'icons')))
        qfile = qt.QFile(filename)
        if qfile.exists():
            return qfile
            if os.path.exists(filename):
                mess = filename + ' exists, but is not supported by qt'
                _logger.warning(mess)

    raise ValueError('Not an icon name: %s' % name)