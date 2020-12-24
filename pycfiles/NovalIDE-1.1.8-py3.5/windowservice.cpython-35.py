# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/plugins/windowservice.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 10084 bytes
from noval import GetApp, _
import noval.iface as iface, noval.plugin as plugin, tkinter as tk
from tkinter import ttk, messagebox
import noval.preference as preference
from noval.util import utils
import noval.ui_utils as ui_utils, noval.consts as consts
MAX_WINDOW_MENU_NUM_ITEMS = 30

class WindowsOptionPanel(ui_utils.CommonOptionPanel):
    __doc__ = '\n    '

    def __init__(self, parent):
        ui_utils.CommonOptionPanel.__init__(self, parent)
        self._loadLayoutCheckVar = tk.IntVar(value=utils.profile_get_int('LoadLastPerspective', True))
        loadLayoutCheckBox = ttk.Checkbutton(self.panel, text=_('Load the last window layout at start up'), variable=self._loadLayoutCheckVar)
        loadLayoutCheckBox.pack(fill=tk.X)
        self._hideMenubarCheckVar = tk.IntVar(value=utils.profile_get_int('HideMenubarFullScreen', False))
        hideMenubarCheckBox = ttk.Checkbutton(self.panel, text=_('Hide menubar When full screen display'), variable=self._hideMenubarCheckVar)
        hideMenubarCheckBox.pack(fill=tk.X)
        self._useCustommenubarCheckVar = tk.IntVar(value=utils.profile_get_int('USE_CUSTOM_MENUBAR', False))
        useCustommenubarCheckBox = ttk.Checkbutton(self.panel, text=_('Use custom menubar'), variable=self._useCustommenubarCheckVar)
        useCustommenubarCheckBox.pack(fill=tk.X)
        row = ttk.Frame(self.panel)
        self._scaling_label = ttk.Label(row, text=_('UI scaling factor:'))
        self._scaling_label.pack(fill=tk.X, side=tk.LEFT)
        self._scaleVar = tk.StringVar(value=utils.profile_get('UI_SCALING_FACTOR', ''))
        scalings = sorted({0.5, 0.75, 1.0, 1.25, 1.33, 1.5, 2.0, 2.5, 3.0, 4.0})
        combobox = ttk.Combobox(row, exportselection=False, textvariable=self._scaleVar, state='readonly', height=15, values=tuple(scalings))
        combobox.pack(fill=tk.X, side=tk.LEFT)
        row.pack(fill=tk.X)
        clear_window_layout_btn = ttk.Button(self.panel, text=_('Clear Window layout configuration information'), command=self.ClearWindowLayoutConfiguration)
        clear_window_layout_btn.pack(anchor=tk.W, pady=consts.DEFAUT_HALF_CONTRL_PAD_Y)

    def OnOK(self, optionsDialog):
        if utils.profile_get('UI_SCALING_FACTOR', '') != self._scaleVar.get():
            messagebox.showinfo(GetApp().GetAppName(), _('Scale changes will not appear until the application is restarted.'), parent=self)
        if utils.profile_get_int('USE_CUSTOM_MENUBAR', 0) != self._useCustommenubarCheckVar.get():
            messagebox.showinfo(GetApp().GetAppName(), _('Menubar changes will not appear until the application is restarted.'), parent=self)
        utils.profile_set('LoadLastPerspective', self._loadLayoutCheckVar.get())
        utils.profile_set('HideMenubarFullScreen', self._hideMenubarCheckVar.get())
        utils.profile_set('USE_CUSTOM_MENUBAR', self._useCustommenubarCheckVar.get())
        scale = self._scaleVar.get()
        if not scale:
            scale = 'default'
        utils.profile_set('UI_SCALING_FACTOR', scale)
        return True

    def ClearWindowLayoutConfiguration(self):
        config = GetApp().GetConfig()
        config.DeleteEntry('DefaultPerspective')
        config.DeleteEntry('LastPerspective')
        messagebox.showinfo(GetApp().GetAppName(), _('Already Clear Window layout configuration information'))


class WindowServiceLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        preference.PreferenceManager().AddOptionsPanelClass('Misc', 'Appearance', WindowsOptionPanel)