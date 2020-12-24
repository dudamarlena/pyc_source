# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/guimain.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 17968 bytes
"""
Root-level classes defining this application's graphical user interface (GUI).
"""
from PySide2.QtCore import QCoreApplication
from betse.util.io.log import logs
from betse.util.type.types import type_check, StrOrNoneTypes
from betsee import guimetadata
from betsee.util.app import guiapp, guiappstatus, guiappwindow
from betsee.util.io import guierror

class BetseeGUI(object):
    __doc__ = '\n    Graphical user interface (GUI) for this application, doubling as both the\n    main window and root Qt widget for this application.\n\n    Attributes\n    ----------\n    _settings : QBetseeSettings\n        :class:`QSettings`-based object exposing all application-wide settings\n        via cross-platform, thread- and process-safe slots.\n    _signaler : QBetseeSignaler\n        :class:`PySide2`-based collection of all application-wide signals.\n    _sim_conf_filename : StrOrNoneTypes\n        Absolute or relative path of the initial YAML-formatted simulation\n        configuration file to be initially opened if any *or* ``None``\n        otherwise.\n    '

    @type_check
    def __init__(self, sim_conf_filename):
        """
        Initialize this graphical user interface (GUI).

        Parameters
        ----------
        sim_conf_filename : StrOrNoneTypes
            Absolute or relative path of the initial YAML-formatted simulation
            configuration file to be initially opened if any *or* ``None``
            otherwise.
        """
        super().__init__()
        self._sim_conf_filename = sim_conf_filename
        self._signaler = None
        self._settings = None

    def run(self) -> int:
        """
        Run this GUI's main event loop and display this GUI.

        Returns
        ----------
        int
            Exit status of this event loop as an unsigned byte.
        """
        guierror.install_exception_hook()
        self._make_main_window()
        return self._show_main_window()

    def _make_main_window(self) -> None:
        """
        Create but do *not* display this GUI's main window.
        """
        from betsee.gui.guimainsettings import QBetseeSettings
        from betsee.gui.guimainsignaler import QBetseeSignaler
        from betsee.gui.window.guiwindow import QBetseeMainWindow
        logs.log_info('Initiating PySide2 UI...')
        self._signaler = QBetseeSignaler()
        main_window = QBetseeMainWindow(signaler=(self._signaler),
          sim_conf_filename=(self._sim_conf_filename))
        guiappwindow.set_main_window(main_window)
        guiappstatus.show_status(QCoreApplication.translate('BetseeGUI', 'Welcome to {}'.format(guimetadata.NAME)))
        self._settings = QBetseeSettings(main_window)
        self._settings.restore_settings()
        main_window.show()

    def _show_main_window(self) -> int:
        """
        Display this GUI's previously created main window.

        Specifically, this method:

        * Run this GUI's event loop, thus displaying this window.
        * Propagates the resulting exit status to the caller.
        """
        logs.log_info('Displaying PySide2 UI...')
        gui_app = guiapp.get_app()
        return gui_app.exec_()