# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/guimainsettings.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 10506 bytes
"""
Low-level :mod:`QSettings`-based application-wide slottable settings classes.
"""
from PySide2.QtCore import QObject, Slot
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.gui.window.guiwindow import QBetseeMainWindow
from betsee.util.io import guisettings

class QBetseeSettings(QObject):
    __doc__ = "\n    :class:`QSettings`-driven object exposing *all* application-wide settings\n    with cross-platform, thread- and process-safe slots permitting external\n    callers to request restoration and storage of these settings to and from an\n    on-disk backing store (e.g., application- and user-specific dotfile).\n\n    Attributes\n    ----------\n    _main_window : QBetseeMainWindow\n        Main window for this application.\n\n    See Also\n    ----------\n    :class:`betsee.gui.guimainsignaler.QBetseeSignaler`\n        Sibling class, whose signals are connected to this object's slots.\n    "

    @type_check
    def __init__(self, main_window, *args, **kwargs):
        """
        Initialize this slotter, connecting each slot to the corresponding
        signal of the :class:`QBetseeSettingsSignaler` instance owned by the
        passed main window widget.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this object.
        """
        (super().__init__)(*args, **kwargs)
        self._main_window = main_window
        signaler = self._main_window.signaler
        signaler.restore_settings_signal.connect(self.restore_settings)
        signaler.store_settings_signal.connect(self.store_settings)

    @Slot()
    def restore_settings(self) -> None:
        """
        Read and restore application-wide settings previously written to a
        user-specific dotfile by the most recent execution of this application
        if any *or* reduce to a noop otherwise.
        """
        logs.log_info('Restoring application settings...')
        settings = guisettings.get_settings()
        settings.beginGroup('main_window')
        if settings.contains('position'):
            main_window_position = settings.value('position')
            logs.log_debug('Restoring window position %r...', main_window_position)
            self._main_window.move(main_window_position)
        else:
            self._main_window.move(0, 0)
        if settings.contains('size'):
            main_window_size = settings.value('size')
            logs.log_debug('Restoring window size %r...', main_window_size)
            self._main_window.resize(main_window_size)
        else:
            self._main_window.resize_max()
        settings.endGroup()

    @Slot()
    def store_settings(self) -> None:
        """
        Write application-wide settings to a user-specific dotfile, which the
        next execution of this application will read and restore on startup.
        """
        logs.log_info('Storing application settings...')
        settings = guisettings.get_settings()
        settings.beginGroup('main_window')
        main_window_is_full_screen = self._main_window.isFullScreen()
        main_window_position = self._main_window.pos()
        main_window_size = self._main_window.size()
        logs.log_debug('Storing window full-screen state "%r"...', main_window_is_full_screen)
        logs.log_debug('Storing window position %r...', main_window_position)
        logs.log_debug('Storing window size %r...', main_window_size)
        settings.setValue('is_full_screen', main_window_is_full_screen)
        settings.setValue('position', main_window_position)
        settings.setValue('size', main_window_size)
        settings.endGroup()