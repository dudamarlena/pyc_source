# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/simconf/guisimconfundo.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 15444 bytes
"""
:mod:`PySide2`-based object encapsulating simulation configuration state.
"""
from PySide2.QtCore import QCoreApplication, QSize
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QUndoCommand, QUndoStack
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.guiexception import BetseePySideMenuException
from betsee.gui.window.guiwindow import QBetseeMainWindow
from betsee.util.widget.abc.guiundocmdabc import QBetseeWidgetUndoCommandABC

class QBetseeSimConfUndoStack(QUndoStack):
    __doc__ = '\n    :class:`QUndoStack`-based stack of all :class:`QBetseeUndoCommandSimConf`\n    instances signifying user-driven simulation configuration modifications and\n    the capacity to undo those modifications.\n\n    Attributes\n    ----------\n    _sim_conf : QBetseeSimConf\n        High-level state of the currently open simulation configuration, which\n        depends on the state of this low-level simulation configuration widget.\n\n    Attributes (Actions)\n    ----------\n    _redo_action : QAction\n        Redo action synchronized with the contents of this stack.\n    _undo_action : QAction\n        Undo action synchronized with the contents of this stack.\n    '

    def __init__(self, *args, **kwargs):
        """
        Initialize this undo stack.
        """
        (super().__init__)(*args, **kwargs)
        self._sim_conf = None
        self._redo_action = None
        self._undo_action = None

    @type_check
    def init(self, main_window: QBetseeMainWindow) -> None:
        """
        Finalize the initialization of this undo stack, owned by the passed
        main window.

        To avoid circular references, this method is guaranteed to *not* retain
        a reference to this main window on returning. References to child
        widgets (e.g., actions) of this window may be retained, however.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this object.
        """
        logs.log_debug('Initializing simulation configuration undo stack...')
        self._sim_conf = main_window.sim_conf
        self._init_actions()
        self._init_menu_edit(main_window)
        self._init_toolbar(main_window)

    @type_check
    def _init_actions(self) -> None:
        """
        Create all actions and icons associated with this undo stack.

        Design
        ----------
        To synchronize the state and text of these actions with the contents of
        this undo stack, this method creates these actions by calling the
        :meth:`createUndoAction` and :meth:`createRedoAction` methods. Since Qt
        Designer lacks support for doing so, this method does so manually.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific :class:`QMainWindow` widget.
        sim_config: QBetseeSimConf
            Direct parent object against which to initialize this object.
        """
        redo_icon = QIcon()
        redo_icon.addFile(':/icon/open_iconic/action-redo.svg', QSize(), QIcon.Normal, QIcon.Off)
        undo_icon = QIcon()
        undo_icon.addFile(':/icon/open_iconic/action-undo.svg', QSize(), QIcon.Normal, QIcon.Off)
        self._redo_action = self.createRedoAction(self, QCoreApplication.translate('QBetseeSimConfUndoStack', '&Redo'))
        self._redo_action.setIcon(redo_icon)
        self._redo_action.setObjectName('action_redo')
        self._redo_action.setShortcuts(QKeySequence.Redo)
        self._undo_action = self.createUndoAction(self, QCoreApplication.translate('QBetseeSimConfUndoStack', '&Undo'))
        self._undo_action.setIcon(undo_icon)
        self._undo_action.setObjectName('action_undo')
        self._undo_action.setShortcuts(QKeySequence.Undo)

    @type_check
    def _init_menu_edit(self, main_window: QBetseeMainWindow) -> None:
        """
        Create all items of the ``Edit`` menu requiring actions previously
        created by the :meth:`_init_actions` method.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific :class:`QMainWindow` widget.
        """
        menu_edit_actions = main_window.menu_edit.actions()
        first_separator = 0
        if menu_edit_actions:
            first_separator = menu_edit_actions[0]
            if not first_separator.isSeparator():
                raise BetseePySideMenuException(QCoreApplication.translate('QBetseeSimConfUndoStack', 'First "Edit" menu action "{0}" not a separator.'.format(first_separator.text())))
        main_window.menu_edit.insertAction(first_separator, self._undo_action)
        main_window.menu_edit.insertAction(first_separator, self._redo_action)

    @type_check
    def _init_toolbar(self, main_window: QBetseeMainWindow) -> None:
        """
        Create all buttons of the main toolbar requiring actions previously
        created by the :meth:`_init_actions` method.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific :class:`QMainWindow` widget.
        """
        tool_bar_actions = main_window.toolbar.actions()
        for first_separator in tool_bar_actions:
            if first_separator.isSeparator():
                main_window.toolbar.insertSeparator(first_separator)
                break
        else:
            first_separator = 0

        main_window.toolbar.insertAction(first_separator, self._undo_action)
        main_window.toolbar.insertAction(first_separator, self._redo_action)

    @type_check
    def push_undo_cmd_if_safe(self, undo_cmd: QBetseeWidgetUndoCommandABC) -> None:
        """
        Push the passed widget-specific undo command onto this undo stack.

        This method is intended to be called *only* by the
        :meth:`betsee.util.widget.mixin.guiwdgmixin.QBetseeEditWidgetMixin._push_undo_cmd_if_safe`
        method, which pushes undo commands from each editable widget onto this
        stack in a hopefully safe manner.

        Parameters
        ----------
        undo_cmd : QBetseeWidgetUndoCommandABC
            Widget-specific undo command to be pushed onto this stack.
        """
        if self._sim_conf.is_open:
            self.push(undo_cmd)
        else:
            logs.log_debug('Ignoring undo command "%s" push request (i.e., simulation configuration not open).', undo_cmd.actionText())

    def push(self, undo_cmd):
        logs.log_debug('Pushing undo command "%s" onto stack...', undo_cmd.actionText())
        try:
            super().push(undo_cmd)
        except OverflowError:
            logs.log_warning('Harmless overflow from editable widget "%s" undo command push request detected...', undo_cmd._widget.obj_name)