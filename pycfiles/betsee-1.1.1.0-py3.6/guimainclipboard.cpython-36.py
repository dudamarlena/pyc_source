# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/gui/window/guimainclipboard.py
# Compiled at: 2019-01-16 01:51:29
# Size of source mod 2**32: 17005 bytes
"""
High-level application clipboard functionality.
"""
from PySide2.QtCore import QCoreApplication, QObject, Slot
from PySide2.QtWidgets import QWidget
from betsee.util.app import guiapp
from betse.util.io.log import logs
from betse.util.type.types import type_check
from betsee.guiexception import BetseePySideClipboardException
from betsee.gui.window.guimainwindow import QBetseeMainWindow
from betsee.util.io import guiclipboard
from betsee.util.io.key import guifocus
from betsee.util.type.guitype import QWidgetOrNoneTypes
from betsee.util.widget.abc.guicontrolabc import QBetseeControllerABC

class QBetseeMainClipboard(QBetseeControllerABC):
    __doc__ = "\n    High-level **clipboarder** (i.e., :mod:`PySide2`-based object encapsulating\n    all application clipboard state).\n\n    This state includes:\n\n    * Whether or not an application widget capable of receiving the interactive\n      keyboard input focus is currently focused.\n    * Whether or not the platform-specific system clipboard's plaintext buffer\n      is currently empty (i.e., contains the empty string).\n\n    Attributes\n    ----------\n    _widget_focused_if_any : QWidgetOrNoneTypes\n        Widget currently receiving the interactive keyboard input focus if any\n        *or* ``None`` otherwise. Ideally, the\n        :func:`betsee.util.io.key.guifocus.get_widget_focused` getter would be\n        called as needed to query for this widget rather than classifying this\n        widget. Sadly, that getter appears to raise spurious exceptions on\n        attempting to query for this widget when a toolbar button (notably, the\n        copy, cut, or paste buttons) is clicked. Why? Presumably due to Qt\n        subtleties in which the currently focused widget is temporarily\n        defocused when a toolbar button is clicked -- regardless of that\n        button's focus policy. In short, Qt issues.\n\n    Attributes (Actions)\n    ----------\n    _action_copy : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_copy` action.\n    _action_cut : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_cut` action.\n    _action_paste : QAction\n        Alias of the :attr:`QBetseeMainWindow.action_paste` action.\n    "

    @type_check
    def __init__(self, *args, **kwargs):
        """
        Initialize this clipboarder.
        """
        (super().__init__)(*args, **kwargs)
        self._action_copy = None
        self._action_cut = None
        self._action_paste = None
        self._widget_focused_if_any = None

    @type_check
    def init(self, main_window):
        """
        Initialize this clipboarder, owned by the passed main window widget.

        This method connects all relevant signals and slots of *all* widgets
        (including the main window, top-level widgets of that window, and leaf
        widgets distributed throughout this application) whose internal state
        pertains to the high-level state of the system clipboard.

        To avoid circular references, this method is guaranteed to *not* retain
        references to this main window on returning. References to child widgets
        (e.g., actions) of this window may be retained, however.

        Parameters
        ----------
        main_window : QBetseeMainWindow
            Initialized application-specific parent :class:`QMainWindow` widget
            against which to initialize this object.
        """
        super().init(main_window)
        logs.log_debug('Sanitizing system clipboard state...')
        self._action_copy = main_window.action_copy
        self._action_cut = main_window.action_cut
        self._action_paste = main_window.action_paste
        self._action_copy.triggered.connect(self._copy_widget_focused_selection_to_clipboard)
        self._action_cut.triggered.connect(self._cut_widget_focused_selection_to_clipboard)
        self._action_paste.triggered.connect(self._paste_clipboard_to_widget_focused_selection)
        gui_app = guiapp.get_app()
        clipboard = guiclipboard.get_clipboard()
        gui_app.focusChanged.connect(self._widget_focus_set)
        clipboard.dataChanged.connect(self._clipboard_text_set)
        self._widget_focus_set(None, None)

    @Slot()
    def _clipboard_text_set(self) -> None:
        """
        Slot signalled when any text is copied or cut into the system
        clipboard's plaintext buffer by any application in the current windowing
        session (including the current application).

        Caveats
        ----------
        The slot is signalled in a somewhat deferred manner on macOS. To quote
        the documentation for the :attr:`QClipboard.dataChanged` signal:

             On macOS and with Qt version 4.3 or higher, clipboard changes made
             by other applications will only be detected when the application is
             activated.
        """
        widget_focused_if_any = guifocus.get_widget_focused_or_none()
        self._widget_focus_set(widget_focused_if_any, widget_focused_if_any)

    @Slot(QWidget, QWidget)
    def _widget_focus_set(self, widget_focused_old: QWidgetOrNoneTypes, widget_focused_new: QWidgetOrNoneTypes) -> None:
        """
        Slot signalled when an application widget loses and/or gains interactive
        keyboard input focus (e.g., due to the tab-key being pressed, this
        widget being clicked, or this main window being made active).

        The slot is signalled *after* both widgets have been notified of this
        :class:`QFocusEvent`.

        Parameters
        ----------
        widget_focused_old : QWidgetOrNoneTypes
            Previously focused widget if any *or* ``None`` otherwise.
        widget_focused_new : QWidgetOrNoneTypes
            Previously focused widget if any *or* ``None`` otherwise.
        """
        try:
            self._widget_focused_if_any = widget_focused_new
            is_widget_focused_clipboardable = self._is_widget_focused_clipboardable()
            self._action_copy.setEnabled(is_widget_focused_clipboardable)
            self._action_cut.setEnabled(is_widget_focused_clipboardable)
            self._action_paste.setEnabled(is_widget_focused_clipboardable and guiclipboard.is_clipboard_text())
        except:
            gui_app = guiapp.get_app()
            gui_app.focusChanged.disconnect(self._widget_focus_set)
            raise

    @Slot()
    def _copy_widget_focused_selection_to_clipboard(self) -> None:
        """
        Slot invoked in response to a user-driven request to copy the
        currently focused widget's **current selection** (i.e., currently
        selected subset of this widget's value(s)) to the system clipboard,
        silently replacing the prior contents if any.
        """
        self._die_unless_widget_focused_clipboardable()
        logs.log_debug('Copying widget "%s" selection to clipboard...', self._widget_focused_if_any.obj_name)
        self._widget_focused_if_any.copy_selection_to_clipboard()

    @Slot()
    def _cut_widget_focused_selection_to_clipboard(self) -> None:
        """
        Slot invoked in response to a user-driven request to **cut** (i.e., copy
        and then remove as a single atomic operation) the currently focused
        widget's **current selection** (i.e., currently selected subset of this
        widget's value(s)) to the clipboard's plaintext buffer, silently
        replacing the prior contents if any.
        """
        self._die_unless_widget_focused_clipboardable()
        logs.log_debug('Cutting widget "%s" selection to clipboard...', self._widget_focused_if_any.obj_name)
        self._widget_focused_if_any.cut_selection_to_clipboard()

    @Slot()
    def _paste_clipboard_to_widget_focused_selection(self) -> None:
        """
        Slot invoked in response to a user-driven request to paste the contents
        of the system clipboard over the currently focused widget's **current
        selection** (i.e., currently selected subset of this widget's value(s)),
        silently replacing the prior selection if any.
        """
        self._die_unless_widget_focused_clipboardable()
        logs.log_debug('Pasting clipboard over widget "%s" selection...', self._widget_focused_if_any.obj_name)
        self._widget_focused_if_any.paste_clipboard_to_selection()

    def _die_unless_widget_focused_clipboardable(self) -> None:
        """
        Raise an exception unless an application-specific widget transparently
        supporting copying, cutting, and pasting into and from the system
        clipboard is currently focused.

        Raises
        ----------
        BetseePySideFocusException
            If *no* widget is currently focused.
        BetseePySideClipboardException
            If a widget is currently focused but this widget is *not* an
            application-specific editable widget supporting clipboard operation.
        """
        if not self._is_widget_focused_clipboardable():
            raise BetseePySideClipboardException(QCoreApplication.translate('QBetseeMainClipboard', 'Focused widget "{0}" not clipboardable (i.e., not an instance of "QBetseeEditWidgetMixin" whose "is_clipboardable" property is True).'.format(self._widget_focused_if_any)))

    @type_check
    def _is_widget_focused_clipboardable(self) -> bool:
        """
        ``True`` only if the currently focused widget (if any) is an
        application-specific editable widget transparently supporting copying,
        cutting, and pasting into and from the system clipboard.

        Returns
        ----------
        bool
            ``True`` only if this widget is an application-specific
            clipboardable widget.
        """
        from betsee.util.widget.abc.guiclipboardabc import QBetseeClipboardWidgetMixin
        return isinstance(self._widget_focused_if_any, QBetseeClipboardWidgetMixin)