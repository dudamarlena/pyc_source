# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/guisimconf.py
# Compiled at: 2019-09-27 02:43:45
# Size of source mod 2**32: 33395 bytes
"""
High-level **simulation configurator** (i.e., :mod:`PySide2`-based object
both displaying *and* modifying external YAML-formatted simulation
configuration files) functionality.
"""
from PySide2.QtCore import QCoreApplication, Signal, Slot
from PySide2.QtWidgets import QMessageBox
from betse.science.parameters import Parameters
from betse.util.app.meta import appmetaone
from betse.util.io.log import logs
from betse.util.path import pathnames
from betse.util.path.dirs import DirOverwritePolicy
from betse.util.type.types import type_check, StrOrNoneTypes
from betsee.guiexception import BetseeSimConfException
from betsee.gui.window.guiwindow import QBetseeMainWindow
from betsee.util.app import guiappstatus
from betsee.util.io import guimessage
from betsee.util.path import guifile
from betsee.util.widget.abc.control.guictlabc import QBetseeControllerABC

class QBetseeSimConf(QBetseeControllerABC):
    __doc__ = '\n    High-level **simulation configurator** (i.e., :mod:`PySide2`-based object\n    both displaying *and* modifying external YAML-formatted simulation\n    configuration files).\n\n    This configurator maintains all state required to manage these files,\n    including:\n\n    * Whether or not a simulation configuration is currently open.\n    * Whether or not an open simulation configuration has unsaved changes.\n\n    Attributes (Public)\n    ----------\n    p : Parameters\n        High-level simulation configuration encapsulating a low-level\n        dictionary parsed from an even lower-level YAML-formatted file. Since\n        this object is guaranteed to be a **singleton** (i.e., remain the same\n        object for the lifetime of this application), external callers are\n        encouraged to retain references to this singleton with the\n        :class:`QBetseeMainWindow` parameter passed to their respective\n        ``init()`` methods (e.g., ``self._p = main_window.sim_conf.p``).\n    undo_stack : QBetseeSimConfUndoStack\n        Undo stack for the currently open simulation configuration if any *or*\n        the empty undo stack otherwise.\n\n    Attributes (Private: Non-widgets)\n    ----------\n    _is_dirty : bool\n        ``True`` only if a simulation configuration is currently open *and*\n        this configuration is **dirty** (i.e., has unsaved changes).\n\n    Attributes (Private: Widgets)\n    ----------\n    _action_make_sim : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_make_sim` action.\n    _action_open_sim : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_open_sim` action.\n    _action_close_sim : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_close_sim` action.\n    _action_save_sim : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_save_sim` action.\n    _action_save_sim_as : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_save_sim_as` action.\n    _sim_conf_changed_signal : QSignal\n        Alias of the :attr:`QBetseeMainWindow.sim_conf_changed_signal` signal.\n    _sim_conf_stack : QBetseeSimConfStackedWidget\n        Alias of the :attr:`QBetseeMainWindow.sim_conf_stack` widget.\n    _sim_conf_tree : QBetseeSimConfTreeWidget\n        Alias of the :attr:`QBetseeMainWindow.sim_conf_tree` widget.\n    _sim_conf_tree_frame : QFrame\n        Alias of the :attr:`QBetseeMainWindow.sim_conf_tree_frame` widget.\n    _sim_tab : QBetseeSimmerTabWidget\n        Alias of the :attr:`QBetseeMainWindow.sim_tab` widget.\n    '

    @type_check
    def __init__(self, *args, **kwargs):
        """
        Initialize this configurator.
        """
        from betsee.gui.simconf.guisimconfundo import QBetseeSimConfUndoStack
        (super().__init__)(*args, **kwargs)
        self._is_dirty = False
        self._action_make_sim = None
        self._action_open_sim = None
        self._action_close_sim = None
        self._action_save_sim = None
        self._action_save_sim_as = None
        self._sim_conf_stack = None
        self._sim_conf_tree = None
        self._sim_conf_tree_frame = None
        self._sim_tab = None
        self.p = Parameters()
        self.undo_stack = QBetseeSimConfUndoStack(self)

    @type_check
    def init(self, main_window):
        """
        Finalize this configurator's initialization, owned by the passed main
        window widget.

        This method connects all relevant signals and slots of *all* widgets
        (including the main window, top-level widgets of that window, and leaf
        widgets distributed throughout this application) whose internal state
        pertains to the high-level state of this simulation configuration.

        Specifically:

        * When any such widget's content (e.g., editable text, selectable item)
          is modified, widgets elsewhere are notified of this simulation
          configuration modification via the
          :attr:`set_dirty_signal` signal.

        To avoid circular references, this method is guaranteed to *not* retain
        references to this main window on returning. References to child
        widgets (e.g., actions) of this window may be retained, however.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this object.
        """
        super().init(main_window)
        logs.log_debug('Sanitizing simulation configuration state...')
        self._init_widgets(main_window)
        self._init_connections(main_window)

    @type_check
    def _init_widgets(self, main_window: QBetseeMainWindow) -> None:
        """
        Create all widgets owned directly by this object *and* initialize all
        other widgets (not necessarily owned by this object) whose internal
        state pertains to the high-level state of this simulation
        configuration.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow`
            widget.
        """
        self._action_make_sim = main_window.action_make_sim
        self._action_open_sim = main_window.action_open_sim
        self._action_close_sim = main_window.action_close_sim
        self._action_save_sim = main_window.action_save_sim
        self._action_save_sim_as = main_window.action_save_sim_as
        self._sim_conf_stack = main_window.sim_conf_stack
        self._sim_conf_tree = main_window.sim_conf_tree
        self._sim_conf_tree_frame = main_window.sim_conf_tree_frame
        self._sim_tab = main_window.sim_tab
        self.undo_stack.init(main_window=main_window)

    @type_check
    def _init_connections(self, main_window: QBetseeMainWindow) -> None:
        """
        Connect all relevant signals and slots of *all* widgets (including the
        main window, top-level widgets of that window, and leaf widgets
        distributed throughout this application) whose internal state pertains
        to the high-level state of this simulation configuration.
        """
        self._action_make_sim.triggered.connect(self._make_sim)
        self._action_open_sim.triggered.connect(self._open_sim)
        self._action_close_sim.triggered.connect(self._close_sim)
        self._action_save_sim.triggered.connect(self._save_sim)
        self._action_save_sim_as.triggered.connect(self._save_sim_as)
        self.set_filename_signal.connect(self._on_filename_set)
        self.set_dirty_signal.connect(self._on_dirty_set)
        self.set_dirty_signal.connect(main_window.set_sim_conf_dirty)

    @property
    def is_open(self) -> bool:
        """
        ``True`` only if a simulation configuration file is currently open.
        """
        return self.p.is_loaded

    @property
    def is_dirty(self) -> bool:
        """
        ``True`` only if a simulation configuration is currently open *and*
        this configuration is **dirty** (i.e., has unsaved changes).
        """
        return self._is_dirty

    @is_dirty.setter
    @type_check
    def is_dirty(self, is_dirty: bool) -> None:
        """
        Set whether or not the current simulation configuration is **dirty**
        (i.e., open and with unsaved changes).

        Parameters
        -----------
        is_dirty : bool
            ``True`` only if this configuration is dirty.
        """
        self.set_dirty_signal.emit(is_dirty)

    @property
    def dirname(self) -> StrOrNoneTypes:
        """
        Absolute path of the directory containing the currently open
        simulation configuration file if any *or* ``None`` otherwise.
        """
        return self.p.conf_dirname

    @property
    def filename(self) -> StrOrNoneTypes:
        """
        Absolute path of the currently open simulation configuration file if
        any *or* ``None`` otherwise.
        """
        return self.p.conf_filename

    def die_unless_open(self) -> bool:
        """
        Raise an exception unless a simulation configuration file is currently
        open.
        """
        if not self.is_open:
            raise BetseeSimConfException(QCoreApplication.translate('QBetseeSimConf', 'No simulation configuration currently open.'))

    set_filename_signal = Signal(str)
    set_dirty_signal = Signal(bool)

    @Slot(str)
    def _on_filename_set(self, filename: str) -> None:
        """
        Slot signalled on the opening of a new simulation configuration *and*
        closing of an open simulation configuration.

        Parameters
        ----------
        filename : str
            Either:

            * If the user opened a new simulation configuration file, the
              non-empty absolute filename of that file.
            * If the user closed an open simulation configuration file, the
              empty string.
        """
        self.is_dirty = False

    @Slot(bool)
    def _on_dirty_set(self, is_dirty: bool) -> None:
        """
        Slot signalled on each change of the **dirty state** (i.e., existence
        of unsaved in-memory changes) of the currently open simulation
        configuration if any.

        This slot internally updates the state (e.g., enabled or disabled,
        displayed or hidden) of all widgets owned or otherwise associated with
        this object.

        Parameters
        ----------
        is_dirty : bool
            ``True`` only if a simulation configuration is currently open *and*
            this configuration is **dirty** (i.e., has unsaved changes).

        Raises
        ----------
        BetseeSimConfException
            If ``is_dirty`` is ``True`` while no simulation configuration file
            is currently open (i.e., :meth:`is_open` is ``False``).
        """
        logs.log_debug('Setting application dirty bit to "%r"...', is_dirty)
        if is_dirty:
            self.die_unless_open()
        self._is_dirty = is_dirty
        self._action_close_sim.setEnabled(self.p.is_loaded)
        self._action_save_sim_as.setEnabled(self.p.is_loaded)
        self._action_save_sim.setEnabled(self.p.is_loaded and is_dirty)
        self._sim_conf_stack.setEnabled(self.p.is_loaded)
        self._sim_conf_tree_frame.setEnabled(self.p.is_loaded)
        self._sim_tab.setEnabled(self.p.is_loaded)
        if not self.p.is_loaded:
            self.undo_stack.clear()

    @Slot()
    def _make_sim(self) -> None:
        """
        Slot invoked on the user requesting that the currently open simulation
        configuration if any be closed and a new simulation configuration with
        default settings be both created and opened.
        """
        conf_default_filename = appmetaone.get_app_meta().betse_sim_conf_default_filename
        conf_default_basename = pathnames.get_basename(conf_default_filename)
        conf_filename = guifile.select_file_yaml_save(dialog_title=(QCoreApplication.translate('QBetseeSimConf', 'New Simulation Configuration')),
          init_pathname=conf_default_basename)
        if conf_filename is None:
            return
        self._close_sim()
        self.p.copy_default(trg_conf_filename=conf_filename,
          is_conf_file_overwritable=True,
          conf_subdir_overwrite_policy=(DirOverwritePolicy.OVERWRITE))
        self._handle_load()
        guiappstatus.show_status(QCoreApplication.translate('QBetseeSimConf', 'Simulation created.'))

    @Slot()
    def _open_sim(self) -> None:
        """
        Slot invoked on the user requesting that the currently open simulation
        configuration if any be closed and an existing external simulation
        configuration be opened.
        """
        conf_filename = guifile.select_file_yaml_read(dialog_title=(QCoreApplication.translate('QBetseeSimConf', 'Open Simulation Configuration')))
        if conf_filename is None:
            return
        self._close_sim()
        self.load(conf_filename)
        guiappstatus.show_status(QCoreApplication.translate('QBetseeSimConf', 'Simulation opened.'))

    @Slot()
    def _close_sim(self) -> None:
        """
        Slot invoked on the user attempting to close the currently open
        simulation configuration.

        If this configuration is dirty (i.e., has unsaved changes), the user
        will be interactively prompted to save this changes *before* this
        configuration is closed and these changes irrevocably lost.
        """
        if not self.save_if_dirty():
            return
        self.unload()
        guiappstatus.show_status(QCoreApplication.translate('QBetseeSimConf', 'Simulation closed.'))

    @Slot()
    def _save_sim(self) -> None:
        """
        Slot invoked on the user requesting all unsaved changes to the
        currently open simulation configuration be written to the external
        YAML-formatted file underlying this configuration, overwriting the
        contents of this file.
        """
        self.p.save_inplace()
        self.set_dirty_signal.emit(False)
        guiappstatus.show_status(QCoreApplication.translate('QBetseeSimConf', 'Simulation saved.'))

    @Slot()
    def _save_sim_as(self) -> None:
        """
        Slot invoked on the user requesting the currently open simulation
        configuration be written to an arbitrary external YAML-formatted file.
        """
        conf_filename = guifile.select_file_yaml_save(dialog_title=(QCoreApplication.translate('QBetseeSimConf', 'Save Simulation Configuration As...')),
          init_pathname=(self.p.conf_basename))
        if conf_filename is None:
            return
        self.p.save(conf_filename=conf_filename,
          is_conf_file_overwritable=True,
          conf_subdir_overwrite_policy=(DirOverwritePolicy.OVERWRITE))
        self.set_filename_signal.emit(conf_filename)
        guiappstatus.show_status(QCoreApplication.translate('QBetseeSimConf', 'Simulation saved.'))

    @type_check
    def load(self, conf_filename: str) -> None:
        """
        Deserialize the YAML-formatted simulation configuration file with the
        passed filename into a high-level :class:`Parameters` object *and*
        signal all connected slots of this event.

        Design
        ----------
        Although low-level, this method is publicly accessible to permit the
        :class:`QBetseeMainWindow` class to handle the equally low-level
        ``--sim-conf-number`` command-line option.

        Note that, to avoid conflicts and confusion with ``open`` methods
        declared throughout the Qt API (e.g., :meth:`QDialog.open`,
        :meth:`QFile.open`), this method is intentionally *not* named ``open``.

        Parameters
        ----------
        conf_filename : str
            Absolute filename of this file.
        """
        self.p.load(conf_filename)
        self._handle_load()

    def _handle_load(self) -> None:
        """
        Update relevant Qt objects in response to a recent deserialization
        (i.e., loading) of a YAML-formatted simulation configuration file.

        Specifically, this method (in order):

        #. Signals all interested slots of this event.
        #. Focuses the top-level tree widget.
        """
        self.set_filename_signal.emit(self.filename)
        self._sim_conf_tree.setFocus()

    def unload(self) -> None:
        """
        Deassociate the high-level :class:`Parameters` object from its formerly
        deserialized YAML-formatted simulation configuration file (if any)
        *and* signal all connected slots of this event.

        Design
        ----------
        Although low-level, this method is publicly accessible to permit the
        :class:`QBetseeMainWindow` class to handle the equally low-level
        ``--sim-conf-number`` command-line option.

        Note that, to avoid conflicts and confusion with ``close`` methods
        declared throughout the Qt API (e.g., :meth:`QDialog.close`,
        :meth:`QBuffer.close`), this method is intentionally *not* named
        ``close``.
        """
        self.p.unload()
        self.set_filename_signal.emit('')

    def save_if_dirty(self) -> bool:
        """
        Write all unsaved changes for the currently open simulation
        configuration to the external YAML-formatted file underlying this
        configuration if such a configuration is open, if this configuration is
        dirty (i.e., has unsaved changes), and if the user interactively
        confirms the overwriting of the existing contents of this file.

        Design
        ----------
        Although low-level, this method is publicly accessible to permit the
        :class:`QBetseeMainWindow` class to handle unsaved changes on window
        closure events.

        This method should typically be called immediately *before* the
        currently open simulation configuration (if any) is closed, preventing
        unsaved changes from being irrevocably lost.

        Returns
        ----------
        bool
            Either:

            * ``False`` only if a configuration is open, this configuration is
              dirty, and the user cancels the dialog prompting for
              confirmation.  In this case, the caller should ideally abort the
              current operation (e.g., closure of either the current window or
              simulation configuration).
            * ``True`` in *all* other cases.
        """
        if not self._is_dirty:
            return True
        else:
            button_clicked = guimessage.show_warning(title=(QCoreApplication.translate('QBetseeSimConf', 'Unsaved Simulation Configuration')),
              synopsis=(QCoreApplication.translate('QBetseeSimConf', 'The currently open simulation configuration has unsaved changes.')),
              exegesis=(QCoreApplication.translate('QBetseeSimConf', 'Would you like to save these changes?')),
              buttons=(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel),
              button_default=(QMessageBox.Save))
            if button_clicked == QMessageBox.Cancel:
                return False
            if button_clicked == QMessageBox.Save:
                self.p.save_inplace()
            return True