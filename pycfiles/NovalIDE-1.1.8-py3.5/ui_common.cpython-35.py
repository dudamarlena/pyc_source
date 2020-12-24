# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/ui_common.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 13515 bytes
import tkinter as tk
from tkinter import ttk
from noval import _, GetApp
from noval.consts import DEFAUT_CONTRL_PAD_X, DEFAUT_CONTRL_PAD_Y
import noval.misc as misc, noval.ui_base as ui_base, noval.constants as constants, noval.preference as preference, noval.consts as consts

class AutomaticPanedWindow(tk.PanedWindow):
    __doc__ = '\n    Enables inserting panes according to their position_key-s.\n    Automatically adds/removes itself to/from its master AutomaticPanedWindow.\n    Fixes some style glitches.\n    '

    def __init__(self, master, position_key=None, preferred_size_in_pw=None, **kwargs):
        tk.PanedWindow.__init__(self, master, **kwargs)
        self._pane_minsize = 100
        self.position_key = position_key
        self._restoring_pane_sizes = False
        self._last_window_size = (0, 0)
        self._full_size_not_final = True
        self._configure_binding = self.bind('<Configure>', self._on_window_resize, True)
        self._update_appearance_binding = self.bind('<<ThemeChanged>>', self._update_appearance, True)
        self.bind('<B1-Motion>', self._on_mouse_dragged, True)
        self._update_appearance()
        self.preferred_size_in_pw = preferred_size_in_pw

    def insert(self, pos, child, **kw):
        kw.setdefault('minsize', self._pane_minsize)
        if pos == 'auto':
            for sibling in sorted(self.pane_widgets(), key=lambda p: p.position_key if hasattr(p, 'position_key') else 0):
                if not hasattr(sibling, 'position_key') or sibling.position_key == None or sibling.position_key > child.position_key:
                    pos = sibling
                    break
            else:
                pos = 'end'

        if isinstance(pos, tk.Widget):
            kw['before'] = pos
        self.add(child, **kw)

    def add(self, child, **kw):
        kw.setdefault('minsize', self._pane_minsize)
        tk.PanedWindow.add(self, child, **kw)
        self._update_visibility()
        self._check_restore_preferred_sizes()

    def remove(self, child):
        tk.PanedWindow.remove(self, child)
        self._update_visibility()
        self._check_restore_preferred_sizes()

    def forget(self, child):
        tk.PanedWindow.forget(self, child)
        self._update_visibility()
        self._check_restore_preferred_sizes()

    def destroy(self):
        self.unbind('<Configure>', self._configure_binding)
        self.unbind('<<ThemeChanged>>', self._update_appearance_binding)
        tk.PanedWindow.destroy(self)

    def is_visible(self):
        if not isinstance(self.master, AutomaticPanedWindow):
            return self.winfo_ismapped()
        else:
            return self in self.master.pane_widgets()

    def pane_widgets(self):
        result = []
        for pane in self.panes():
            assert not isinstance(pane, tk.Widget)
            result.append(self.nametowidget(str(pane)))

        return result

    def _on_window_resize(self, event):
        if event.width < 10 or event.height < 10:
            return
        window = self.winfo_toplevel()
        window_size = (window.winfo_width(), window.winfo_height())
        initializing = hasattr(window, 'initializing') and window.initializing
        if not initializing and not self._restoring_pane_sizes and (window_size != self._last_window_size or self._full_size_not_final):
            self._check_restore_preferred_sizes()
            self._last_window_size = window_size

    def _on_mouse_dragged(self, event):
        if event.widget == self and not self._restoring_pane_sizes:
            self._update_preferred_sizes()

    def _update_preferred_sizes(self):
        for pane in self.pane_widgets():
            if getattr(pane, 'preferred_size_in_pw', None) is not None:
                if self.cget('orient') == 'horizontal':
                    current_size = pane.winfo_width()
                else:
                    current_size = pane.winfo_height()
                if current_size > 20:
                    pane.preferred_size_in_pw = current_size

    def _check_restore_preferred_sizes(self):
        window = self.winfo_toplevel()
        if getattr(window, 'initializing', False):
            return
        try:
            self._restoring_pane_sizes = True
            self._restore_preferred_sizes()
        finally:
            self._restoring_pane_sizes = False

    def _restore_preferred_sizes(self):
        total_preferred_size = 0
        panes_without_preferred_size = []
        panes = self.pane_widgets()
        for pane in panes:
            if not hasattr(pane, 'preferred_size_in_pw'):
                return
            if pane.preferred_size_in_pw is None:
                panes_without_preferred_size.append(pane)
            else:
                total_preferred_size += pane.preferred_size_in_pw

        assert len(panes_without_preferred_size) <= 1
        size = self._get_size()
        if size is None:
            return
        leftover_size = self._get_size() - total_preferred_size
        used_size = 0
        for i, pane in enumerate(panes[:-1]):
            used_size += pane.preferred_size_in_pw or leftover_size
            self._place_sash(i, used_size)
            used_size += int(str(self.cget('sashwidth')))

    def _get_size(self):
        if self.cget('orient') == tk.HORIZONTAL:
            result = self.winfo_width()
        else:
            result = self.winfo_height()
        if result < 20:
            return
        else:
            return result

    def _place_sash(self, i, distance):
        if self.cget('orient') == tk.HORIZONTAL:
            self.sash_place(i, distance, 0)
        else:
            self.sash_place(i, 0, distance)

    def _update_visibility(self):
        if not isinstance(self.master, AutomaticPanedWindow):
            return
        if len(self.panes()) == 0 and self.is_visible():
            self.master.forget(self)
        if len(self.panes()) > 0 and not self.is_visible():
            self.master.insert('auto', self)

    def _update_appearance(self, event=None):
        self.configure(sashwidth=misc.lookup_style_option('Sash', 'sashthickness', 5))
        self.configure(background=misc.lookup_style_option('TPanedWindow', 'background'))


class AutomaticNotebook(ui_base.ClosableNotebook):
    __doc__ = '\n    Enables inserting views according to their position keys.\n    Remember its own position key. Automatically updates its visibility.\n    '

    def __init__(self, master, position_key, preferred_size_in_pw=None, style='ButtonNotebook.TNotebook'):
        ui_base.ClosableNotebook.__init__(self, master, style=style, padding=0)
        self.position_key = position_key
        self.preferred_size_in_pw = preferred_size_in_pw

    def add(self, child, **kw):
        super().add(child, **kw)
        self._update_visibility()

    def insert(self, pos, child, **kw):
        if pos == 'auto':
            for sibling in map(self.nametowidget, self.tabs()):
                if not hasattr(sibling, 'position_key') or sibling.position_key == None or sibling.position_key > child.position_key:
                    pos = sibling
                    break
            else:
                pos = 'end'

        ui_base.ClosableNotebook.insert(self, pos, child, **kw)
        self._update_visibility()

    def hide(self, tab_id):
        ui_base.ClosableNotebook.hide(self, tab_id)
        self._update_visibility()

    def forget(self, tab_id):
        if tab_id in self.tabs() or tab_id in self.winfo_children():
            ui_base.ClosableNotebook.forget(self, tab_id)
        self._update_visibility()

    def is_visible(self):
        return self in self.master.pane_widgets()

    def get_visible_child(self):
        for child in self.winfo_children():
            if str(child) == str(self.select()):
                return child

    def _update_visibility(self):
        if not isinstance(self.master, AutomaticPanedWindow):
            return
        if len(self.tabs()) == 0 and self.is_visible():
            self.master.remove(self)
        if len(self.tabs()) > 0 and not self.is_visible():
            self.master.insert('auto', self)


class AutoScrollbar(ui_base.SafeScrollbar):

    def __init__(self, master=None, **kw):
        ui_base.SafeScrollbar.__init__(self, master=master, **kw)

    def set(self, first, last):
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.grid_remove()
        elif float(first) > 0.001 or float(last) < 0.009:
            self.grid()
        ttk.Scrollbar.set(self, first, last)

    def pack(self, **kw):
        raise tk.TclError('cannot use pack with this widget')


class PromptmessageBox(ui_base.CommonModaldialog):

    def __init__(self, master, title, msg):
        ui_base.CommonModaldialog.__init__(self, master, takefocus=1)
        self.title(title)
        self.label_ctrl = ttk.Label(self.main_frame, text=msg)
        self.label_ctrl.pack(fill='x', padx=(consts.DEFAUT_CONTRL_PAD_X, consts.DEFAUT_CONTRL_PAD_X), pady=(consts.DEFAUT_CONTRL_PAD_Y, 0))
        bottom_page = ttk.Frame(self.main_frame)
        ttk.Label(bottom_page).pack(side=tk.LEFT, fill='x', expand=1)
        btnYes = ttk.Button(bottom_page, text=_('Yes'), command=self.OnYes, default=tk.ACTIVE)
        btnYes.pack(side=tk.LEFT, fill='x')
        btnNo = ttk.Button(bottom_page, text=_('No'), command=self.OnNo)
        btnNo.pack(side=tk.LEFT, fill='x', padx=(consts.DEFAUT_CONTRL_PAD_X, 0))
        btnYesAll = ttk.Button(bottom_page, text=_('YestoAll'), command=self.OnYestoAll)
        btnYesAll.pack(side=tk.LEFT, fill='x', padx=(consts.DEFAUT_CONTRL_PAD_X, 0))
        btnNoAll = ttk.Button(bottom_page, text=_('NotoAll'), command=self.OnNotoAll)
        btnNoAll.pack(side=tk.LEFT, fill='x', padx=(consts.DEFAUT_CONTRL_PAD_X, 0))
        bottom_page.pack(fill='x', padx=consts.DEFAUT_CONTRL_PAD_X, pady=consts.DEFAUT_CONTRL_PAD_Y)
        self.status = -1

    def OnYes(self):
        self.status = constants.ID_YES
        self.destroy()

    def OnNo(self):
        self.status = constants.ID_NO
        self.destroy()

    def OnYestoAll(self):
        self.status = constants.ID_YESTOALL
        self.destroy()

    def OnNotoAll(self):
        self.status = constants.ID_NOTOALL
        self.destroy()


def ShowInterpreterConfigurationPage():
    interpreter_changed = False
    preference_dlg = preference.PreferenceDialog(GetApp().GetTopWindow(), selection=preference.GetOptionName(preference.INTERPRETER_OPTION_NAME, preference.INTERPRETER_CONFIGURATIONS_ITEM_NAME))
    if preference_dlg.ShowModal() == constants.ID_OK:
        GetApp().AddInterpreters()
        interpreter_changed = True
    else:
        GetApp().SetCurrentInterpreter()
    return interpreter_changed