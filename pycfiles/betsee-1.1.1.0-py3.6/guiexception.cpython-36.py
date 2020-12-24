# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/guiexception.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 18083 bytes
"""
Application-specific exception hierarchy.
"""
from abc import ABCMeta

class BetseeException(Exception, metaclass=ABCMeta):
    __doc__ = '\n    Abstract base class of all application-specific exceptions.\n\n    Attributes\n    ----------\n    title : str\n        Human-readable title associated with this exception, typically\n        constrained to at most two to three words.\n    synopsis : str\n        Human-readable synopsis tersely describing this exception, typically\n        constrained to a single sentence.\n    exegesis : optional[str]\n        Human-readable explanation fully detailing this exception if any,\n        typically spanning multiple sentences, *or* ``None`` otherwise (i.e.,\n        if no such explanation is defined).\n    '

    def __init__(self, synopsis, title=None, exegesis=None):
        """
        Initialize this exception.

        Parameters
        ----------
        synopsis : str
            Human-readable synopsis tersely describing this exception,
            typically constrained to a single sentence.
        title : optional[str]
            Human-readable title associated with this exception, typically
            constrained to at most two to three words. Defaults to ``None``, in
            which case the title defaults to the translated string returned by
            the :meth:`_title_default` property.
        exegesis : optional[str]
            Human-readable explanation fully detailing this exception,
            typically spanning multiple sentences. Defaults to ``None``, in
            which case no such explanation is defined.
        """
        if not isinstance(synopsis, str):
            raise AssertionError('"{}" not a string.'.format(synopsis))
        elif not isinstance(title, (str, type(None))):
            raise AssertionError('"{}" neither a string nor "None".'.format(title))
        else:
            assert isinstance(exegesis, (str, type(None))), '"{}" neither a string nor "None".'.format(exegesis)
            super().__init__(synopsis + (' ' + exegesis if exegesis is not None else ''))
            if title is None:
                try:
                    title = self._title_default
                except ImportError as exception:
                    title = str(exception)

        self.title = title
        self.synopsis = synopsis
        self.exegesis = exegesis

    @property
    def _title_default(self) -> str:
        """
        Default human-readable title associated with *all* exceptions of this
        type for which no ``title`` parameter is passed at instantiation time.
        """
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseeException', 'Horrible Error')


class BetseeCacheException(BetseeException):
    __doc__ = '\n    General-purpose exception applicable to user-specific caching, including\n    dynamic generation of pure-Python modules imported at runtime.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseeCacheException', 'Cache Error')


class BetseeLibException(BetseeException):
    __doc__ = '\n    General-purpose exception applicable to all optional and mandatory\n    third-party dependencies, including :mod:`PySide2`.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideException', 'Dependency Error')


class BetseeSimConfException(BetseeException):
    __doc__ = '\n    General-purpose exception applicable to simulation configuration state\n    handling (e.g., whether a simulation configuration is currently open).\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseeSimConfException', 'Simulation Configuration Error')


class BetseePySideException(BetseeLibException):
    __doc__ = "\n    General-purpose exception applicable to :mod:`PySide2`, this application's\n    principal third-party dependency.\n    "

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideException', 'PySide2 Error')


class BetseePySideClipboardException(BetseePySideException):
    __doc__ = '\n    General-purpose exception applicable to all interaction with the\n    platform-specific system clipboard.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideClipboardException', 'Clipboard Error')


class BetseePySideFocusException(BetseePySideException):
    __doc__ = '\n    General-purpose exception applicable to all handling of interactive\n    keyboard input focus for widgets.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideFocusException', 'Widget Focus Error')


class BetseePySideSettingsException(BetseePySideException):
    __doc__ = '\n    General-purpose exception applicable to all interaction with the\n    platform-specific backing store of application settings.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideSettingsException', 'Settings Error')


class BetseePySideThreadException(BetseePySideException):
    __doc__ = '\n    :class:`PySide2.QtCore.QThread`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideThreadException', 'Thread Error')


class BetseePySideThreadWorkerException(BetseePySideThreadException):
    __doc__ = '\n    Multithreaded worker object-specific exception, where "worker" implies any\n    :class:`QObject`- or :class:`QRunnable`-derived object isolated in whole or\n    part to a secondary application thread.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideThreadWorkerException', 'Thread Worker Error')


class BetseePySideThreadWorkerStopException(BetseePySideThreadWorkerException):
    __doc__ = '\n    Multithreaded worker object-specific exception internally raised by the\n    ``_halt_work_if_requested`` methods and caught by the ``start`` methods\n    defined on these objects.\n\n    This exception is intended exclusively for private use by the\n    aforementioned methods as a crude (albeit sufficient) means of facilitating\n    superclass-subclass intercommunication.\n    '


class BetseePySideWidgetException(BetseePySideException):
    __doc__ = '\n    General-purpose exception applicable to :mod:`PySide2` widgets.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideWidgetException', 'Widget Error')


class BetseePySideApplicationException(BetseePySideWidgetException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QApplication`-specific exception pertaining to\n    the application singleton for this... application.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideApplicationException', 'Singleton Error')


class BetseePySideMenuException(BetseePySideWidgetException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QMenu`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideMenuException', 'Menu Error')


class BetseePySideMessageBoxException(BetseePySideWidgetException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QMessageBox`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideMessageBoxException', 'Message Box Error')


class BetseePySideSpinBoxException(BetseePySideWidgetException):
    __doc__ = '\n    General-purpose exception applicable to all concrete\n    :class:`PySide2.QtWidgets.QAbstractSpinBox` widgets (e.g.,\n    :class:`PySide2.QtWidgets.QDoubleSpinBox` widgets).\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideSpinBoxException', 'Spin Box Error')


class BetseePySideWindowException(BetseePySideWidgetException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QMainWindow`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideWindowException', 'Window Error')


class BetseePySideEditWidgetException(BetseePySideException):
    __doc__ = '\n    General-purpose exception applicable to application-specific editable\n    widgets (i.e., instances of the\n    :mod:`betsee.util.widget.mixin.guiwdgmixin.QBetseeObjectMixin` superclass).\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideEditWidgetException', 'Editable Widget Error')


class BetseePySideWidgetEnumException(BetseePySideWidgetException):
    __doc__ = '\n    General-purpose exception applicable to mutually exclusive :mod:`PySide2`\n    widgets typically converted to and from lower-level enumeration members.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideWidgetEnumException', 'Enumerable Widget Error')


class BetseePySideComboBoxException(BetseePySideWidgetEnumException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QComboBox`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideComboBoxException', 'Combo Box Error')


class BetseePySideRadioButtonException(BetseePySideWidgetEnumException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QRadioButton`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideRadioButtonException', 'Radio Button Error')


class BetseePySideStackedWidgetException(BetseePySideWidgetException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QStackedWidget`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideStackedWidgetException', 'Stacked Widget Error')


class BetseePySideTreeWidgetException(BetseePySideWidgetException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QTreeWidget`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideTreeWidgetException', 'Tree Widget Error')


class BetseePySideTreeWidgetItemException(BetseePySideWidgetException):
    __doc__ = '\n    :class:`PySide2.QtWidgets.QTreeWidgetItem`-specific exception.\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseePySideTreeWidgetItemException', 'Tree Widget Item Error')


class BetseeSimmerException(BetseePySideException):
    __doc__ = '\n    General-purpose exception applicable to the **simulator** (i.e.,\n    :mod:`PySide2`-based object both displaying *and* controlling the execution\n    of simulation phases).\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseeSimmerException', 'Simulator Error')


class BetseeSimmerBetseException(BetseeSimmerException):
    __doc__ = '\n    General-purpose exception intended to encapsulate *all* low-level\n    exceptions raised by BETSE simulations (e.g., computational instabilities).\n    '

    @property
    def _title_default(self) -> str:
        from PySide2.QtCore import QCoreApplication
        return QCoreApplication.translate('BetseeSimmerBetseException', 'BETSE Error')