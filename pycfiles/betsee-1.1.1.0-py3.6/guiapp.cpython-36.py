# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/app/guiapp.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 16530 bytes
"""
Submodule both instantiating and initializing the :class:`QApplication`
singleton for this application.
"""
import logging
from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QApplication, qApp
from betsee import guimetadata
from betsee.guiexception import BetseePySideApplicationException
_IS_INITTED = False

def die_unless_initted() -> None:
    """
    Raise an exception unless the :func:`init` function has been called and
    hence instantiated the :class:`QApplication` singleton for this
    application.

    For safety, this function additionally raises an exception if the
    :func:`init` function has been called but the :class:`QApplication`
    singleton instantiated by that function no longer exists.

    Raises
    ----------
    BetseePySideApplicationException
        If either:
        * The :func:`init` function has yet to be called.
        * The :class:`QApplication` singleton has yet to be instantiated.
    """
    global _IS_INITTED
    if not _IS_INITTED:
        raise BetseePySideApplicationException(QCoreApplication.translate('guiapp', 'betsee.util.app.guiapp.init() has yet to be called.'))
    if qApp is None:
        raise BetseePySideApplicationException(QCoreApplication.translate('guiapp', '"QApplication" singleton uninstantiated (e.g., as betsee.util.app.guiapp.init() has yet to be called).'))


def get_app() -> QApplication:
    """
    Initialized :class:`QApplication` singleton for this application if
    instantiated by a prior call to the :func:`init` function *or* raise an
    exception otherwise (i.e., if that function has yet to be called).

    Contrary to nomenclature, the :class:`QApplication` class confusingly
    subclasses the :class:`QGuiApplication` base class in a manner optimized
    for widgets. Ergo, the former is *always* preferable to the latter.

    Design
    ----------
    This function does *not* implicitly call the :func:`init` function if the
    :class:`QApplication` singleton has yet to be instantiated. While
    non-intuitive and arguably inconvenient, this is intentional. Implicitly
    calling that function would technically be trivial but invite subtle (and
    hence non-debuggable) issues; in particular, the order in which the
    :func:`init` and :func:`betse.lib.libs.reinit` methods are called is very
    significant and hence must *not* be left up to non-deterministic chance.

    Caveats (Exceptions)
    ----------
    Avoid directly accessing the low-level :attr:`PySide2.QtWidgets.qApp`
    global, which this higher-level function wraps. Since that global is
    typically ``None`` prior to the first call to the :func:`init` function,
    directly accessing that global sufficiently early in runtime may raise
    non-human-readable exceptions *or* induce low-level segmentation faults
    from Qt itself resembling:

        QWidget: Must construct a QApplication before a QWidget
        [1]    30475 abort      betsee -v

    In contrast, this function *always* raises human-readable exceptions.

    Caveats (Attributes)
    ----------
    Avoid attempting to add application-specific instance variables to the
    low-level :attr:`PySide2.QtWidgets.qApp` global returned by this function,
    as that global silently ignores all such attempts. While this constraint
    could technically be circumvented by globally persisting the
    :class:`QApplication` singleton created by the :func:`init` function as a
    module-scoped Python singleton, doing so would incur subtle issues of its
    own -- including complications in both garbage collection and accidental
    collision with standard Qt attributes.

    Returns
    ----------
    QApplication
        Initialized :class:`QApplication` singleton for this application.

    Raises
    ----------
    BetseePySideApplicationException
        If either:
        * The :func:`init` function has yet to be called.
        * The :class:`QApplication` singleton has yet to be instantiated.
    """
    die_unless_initted()
    return qApp


def init() -> None:
    """
    Instantiate and initialize the :class:`QApplication` singleton for this
    application (i.e., the :attr:`PySide2.QApplication.qApp` instance) if this
    function has not already been called *or* silently reduce to a noop
    otherwise (i.e., if this function has already been called).
    """
    global _IS_INITTED
    if _IS_INITTED:
        return
    _deinit_qt_app()
    _init_qt()
    _init_qt_app()
    _IS_INITTED = True


def _deinit_qt_app() -> None:
    """
    Destroy the existing :class:`QApplication` singleton with a non-fatal
    warning if such a singleton has been previously initialized elsewhere *or*
    silently reduce to a noop otherwise.

    While this condition should arguably constitute a fatal error inducing a
    raised exception, various versions of PySide2 appear to erroneously
    initialize this singleton on first importation without our explicit
    consent. There isn't much we can do about it; this is the next best thing.

    If this singleton is _not_ explicitly destroyed, PySide2 raises the
    following exception on attempting to re-initialize another such singleton:

        RuntimeError: Please destroy the QApplication singleton before creating
        a new QApplication instance.
    """
    app_prior = QCoreApplication.instance()
    if app_prior is not None:
        logging.warning('Destroying erroneously instantiated Qt application singleton...')
        app_prior.quit()


def _init_qt() -> None:
    """
    Initialize static attributes of the :class:`QApplication` class or
    subclasses thereof (e.g., :class:`QCoreApplication`,
    :class:`QGuiApplication`) *before* the singleton instance of this class is
    defined.

    Technically, some of these attributes (e.g.,
    :attr:`Qt.AA_UseHighDpiPixmaps`) are safely definable at any time. Since
    others (e.g. ,:attr:`Qt.AA_EnableHighDpiScaling`) are *not*, all such
    attributes are preemptively defined here for both simplicity and safety.

    These attributes pertain to the :class:`QApplication` singleton rather than
    this singleton's :class:`QMainWindow` instance implemented by the
    XML-formatted UI file exported by Qt Creator; thus, these attributes
    *cannot* be specified by this file but *must* instead be manually
    implemented in Python.
    """
    from betsee.util.io import guisettings
    _init_qt_metadata()
    _init_qt_dpi()
    guisettings.init()


def _init_qt_metadata() -> None:
    """
    Initialize all static attributes of the :class:`QCoreApplication` class
    signifying application-wide core properties (e.g., name, version).
    """
    logging.debug('Initializing static Qt attributes...')
    QGuiApplication.setApplicationDisplayName(guimetadata.NAME)
    QCoreApplication.setApplicationName(guimetadata.NAME)
    QCoreApplication.setApplicationVersion(guimetadata.VERSION)
    QCoreApplication.setOrganizationName(guimetadata.ORG_NAME)
    QCoreApplication.setOrganizationDomain(guimetadata.ORG_DOMAIN_NAME)


def _init_qt_dpi() -> None:
    """
    Initialize all static attributes of the :class:`QApplication` class
    pertaining to dots per inch (DPI) and, specifically, high-DPI displays.

    See Also
    ----------
    https://blog.qt.io/blog/2016/01/26/high-dpi-support-in-qt-5-6
        *High-DPI Support in Qt 5.6,* article colloquially describing the
        attributes initialized by this method.
    """
    try:
        from betse.util.os import displays
        if not displays.is_dpi_scaling():
            logging.debug('Initializing high-DPI scaling emulation...')
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    except ImportError as exception:
        logging.error(str(exception))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)


def _init_qt_app() -> QApplication:
    """
    Instantiate and return the :class:`QApplication` singleton for this
    application.
    """
    logging.debug('Instantiating Qt application singleton...')
    gui_app = QApplication([])
    return gui_app