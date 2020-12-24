# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/app_menus.py
# Compiled at: 2019-07-16 09:35:37
from __future__ import unicode_literals
from builtins import range
import sys, tempfile, png, os, webbrowser
if sys.version_info[0] < 3:
    import Tkinter as Tk_, ttk, tkMessageBox
    from urllib import pathname2url
else:
    import tkinter as Tk_
    from tkinter import ttk
    import tkinter.messagebox as tkMessageBox
    from urllib.request import pathname2url
from snappy import filedialog, __file__ as snappy_dir
from .infodialog import about_snappy, InfoDialog
OSX_shortcuts = {b'Open...': b'Command-o', b'Save': b'Command-s', 
   b'Save as...': b'Command-Shift-s', 
   b'Cut': b'Command-x', 
   b'Copy': b'Command-c', 
   b'Paste': b'Command-v', 
   b'Close': b'Command-w', 
   b'Left': b'←', 
   b'Up': b'↑', 
   b'Right': b'→', 
   b'Down': b'↓'}
OSX_shortcut_events = {b'Open...': b'<Command-o>', b'Save': b'<Command-s>', 
   b'Save as...': b'<Command-S>', 
   b'Cut': b'<Command-x>', 
   b'Copy': b'<Command-c>', 
   b'Paste': b'<Command-v>', 
   b'Close': b'<Command-w>'}
Linux_shortcuts = {b'Open...': b'Cntl+O', b'Save': b'Cntl+S', 
   b'Save as...': b'Cntl+Shift+S', 
   b'Cut': b'Cntl+X', 
   b'Copy': b'Cntl+Shift+C', 
   b'Paste': b'Cntl+Shift+V', 
   b'Left': b'←', 
   b'Up': b'↑', 
   b'Right': b'→', 
   b'Down': b'↓'}
Linux_shortcut_events = {b'Open...': b'<Control-o>', b'Save': b'<Control-s>', 
   b'Save as...': b'<Control-S>', 
   b'Cut': b'<Control-x>', 
   b'Copy': b'<Control-C>', 
   b'Paste': b'<Control-V>'}
if sys.platform == b'darwin':
    scut = OSX_shortcuts
    scut_events = OSX_shortcut_events
elif sys.platform == b'linux2' or sys.platform == b'linux':
    scut = Linux_shortcuts
    scut_events = Linux_shortcut_events
else:
    scut = Linux_shortcuts
    scut_events = Linux_shortcut_events

def add_menu(root, menu, label, command, state=b'active'):
    accelerator = scut.get(label, b'')
    menu.add_command(label=label, accelerator=accelerator, command=command, state=state)
    if scut_events.get(label, None) and state != b'disabled':
        root.bind(scut_events[label], command)
    return


class EditMenu(Tk_.Menu):
    """Edit Menu cascade containing Cut, Copy, Paste and Delete. To use,
    provide a callback function which returns a dict specifying which
    editing functions should be enabled.  The keys should be chosen
    from the list ['Cut', 'Copy', 'Paste, 'Delete'] and the values
    should be functions to be call for the corresponding actions.  If
    a key is missing, the corresponding menu entry will be disabled.

    """
    entries = [
     b'Cut', b'Copy', b'Paste', b'Delete']

    def __init__(self, menubar, callback):
        Tk_.Menu.__init__(self, menubar, name=b'snappyedit', postcommand=self.configure)
        self.get_actions = callback
        self.add_entry(b'Cut', lambda event=None: self.actions[b'Cut']())
        self.add_entry(b'Copy', lambda event=None: self.actions[b'Copy']())
        self.add_entry(b'Paste', lambda event=None: self.actions[b'Paste']())
        self.add_entry(b'Delete', lambda event=None: self.actions[b'Delete']())
        self.actions = {}
        return

    def add_entry(self, label, command):
        accelerator = scut.get(label, b'')
        self.add_command(label=label, accelerator=accelerator, command=command, state=b'disabled')

    def configure(self):
        """Called before the menu is opened."""
        self.actions = self.get_actions()
        for entry in self.entries:
            if self.actions.get(entry, None):
                self.entryconfig(entry, state=b'normal')
            else:
                self.entryconfig(entry, state=b'disabled')

        return


class HelpMenu(Tk_.Menu):
    """Help Menu cascade.  Always contains the main SnapPy help entry.
    Additional help entries for specific tools, such as a Dirichlet
    viewer, may be added or removed.

    """

    def __init__(self, menubar):
        Tk_.Menu.__init__(self, menubar, name=b'help')
        if sys.platform != b'darwin':
            self.add_command(label=b'SnapPy Help ...', command=self.show_SnapPy_help)
        self.add_command(label=b'Report Bugs ...', command=self.show_bugs_page)
        self.extra_commands = {}

    def show_SnapPy_help(self):
        self.show_page(b'index.html')

    def show_bugs_page(self):
        self.show_page(b'bugs.html')

    def show_page(self, page):
        path = os.path.join(os.path.dirname(snappy_dir), b'doc', page)
        if os.path.exists(path):
            url = b'file:' + pathname2url(path)
            try:
                webbrowser.open_new_tab(url)
            except webbrowser.Error:
                tkMessageBox.showwarning(b'Error', b'Failed to open the documentation file.')

        else:
            tkMessageBox.showwarning(b'Not found!', b'The file %s does not exist.' % path)

    def extra_command(self, label, command):
        self.extra_commands[label] = command

    def activate(self, labels):
        """Manage extra help entries.
        Pass the labels of the extra commands to be activated.
        """
        end = self.index(Tk_.END)
        if sys.platform == b'darwin':
            self.delete(0, self.index(Tk_.END))
        else:
            if end > 0:
                self.delete(1, self.index(Tk_.END))
            for label in labels:
                if label in self.extra_commands:
                    self.add_command(label=label, command=self.extra_commands[label])


class WindowMenu(Tk_.Menu):
    """Emulates the behavior of the Apple Window menu. Windows register when they open
    by calling the class method register.  They unregister when they close.  The class
    maintains a list of all openwindows.  Objects of this class use the postcommand to
    construct a menu containing an entry for each registered window.  Participating
    windows should be subclasses of WindowMenu.

    In OS X we use the system Window menu instead of this one.
    """
    windows = []

    def __init__(self, menubar):
        Tk_.Menu.__init__(self, menubar, name=b'window', postcommand=self.build_entries)

    @classmethod
    def register(cls, window):
        cls.windows.append(window)

    @classmethod
    def unregister(cls, window):
        try:
            cls.windows.remove(window)
        except ValueError:
            pass

    def build_entries(self):
        if sys.platform == b'darwin':
            return
        self.delete(0, self.index(Tk_.END))
        for object in self.windows:
            self.add_command(label=object.menu_title, command=object.bring_to_front)

    def bring_to_front(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()


def togl_save_image(self):
    savefile = filedialog.asksaveasfile(parent=self.window, mode=b'wb', title=b'Save Image As PNG Image File', defaultextension=b'.png', filetypes=[
     ('PNG image files', '*.png *.PNG', ''),
     ('All files', '')])
    self.widget.redraw()
    if savefile:
        ppm_file = tempfile.mktemp() + b'.ppm'
        PI = Tk_.PhotoImage()
        self.widget.tk.call(self.widget._w, b'takephoto', PI.name)
        PI.write(ppm_file, format=b'ppm')
        infile = open(ppm_file, b'rb')
        format, width, height, depth, maxval = png.read_pnm_header(infile, ('P5', 'P6',
                                                                            'P7'))
        greyscale = depth <= 2
        pamalpha = depth in (2, 4)
        supported = [ 2 ** x - 1 for x in range(1, 17) ]
        mi = supported.index(maxval)
        bitdepth = mi + 1
        writer = png.Writer(width, height, greyscale=greyscale, bitdepth=bitdepth, alpha=pamalpha)
        writer.convert_pnm(infile, savefile)
        savefile.close()
        infile.close()
        os.remove(ppm_file)


def browser_menus(self):
    """Menus for the browser window.  Used as Browser.build_menus.
    Creates a menubar attribute for the browser.

    """
    window = self.window
    self.menubar = menubar = Tk_.Menu(window)
    Python_menu = Tk_.Menu(menubar, name=b'apple')
    Python_menu.add_command(label=b'About SnapPy ...', command=lambda : about_snappy(window))
    Python_menu.add_separator()
    Python_menu.add_command(label=b'SnapPy Preferences ...', state=b'disabled')
    Python_menu.add_separator()
    if sys.platform in ('linux2', 'linux') and self.main_window is not None:
        Python_menu.add_command(label=b'Quit SnapPy', command=self.main_window.close)
    menubar.add_cascade(label=b'SnapPy', menu=Python_menu)
    File_menu = Tk_.Menu(menubar, name=b'file')
    add_menu(window, File_menu, b'Open...', None, b'disabled')
    add_menu(window, File_menu, b'Save as...', self.save)
    Export_menu = Tk_.Menu(File_menu, name=b'export')
    File_menu.add_cascade(label=b'Export as STL...', menu=Export_menu)
    add_menu(window, Export_menu, b'Export STL', self.dirichlet_viewer.export_stl)
    add_menu(window, Export_menu, b'Export Cutout STL', self.dirichlet_viewer.export_cutout_stl)
    File_menu.add_separator()
    add_menu(window, File_menu, b'Close', self.close)
    menubar.add_cascade(label=b'File', menu=File_menu)
    menubar.add_cascade(label=b'Edit ', menu=EditMenu(menubar, self.edit_actions))
    if sys.platform == b'darwin':
        menubar.add_cascade(label=b'View', menu=Tk_.Menu(menubar, name=b'view'))
    menubar.add_cascade(label=b'Window', menu=WindowMenu(menubar))
    help_menu = HelpMenu(menubar)

    def dirichlet_help():
        InfoDialog(window, b'Viewer Help', self.dirichlet_viewer.widget.help_text)

    help_menu.extra_command(label=b'Polyhedron Viewer Help ...', command=dirichlet_help)

    def horoball_help():
        InfoDialog(window, b'Viewer Help', self.horoball_viewer.widget.help_text)

    help_menu.extra_command(label=b'Horoball Viewer Help ...', command=horoball_help)
    menubar.add_cascade(label=b'Help', menu=help_menu)
    return


def plink_menus(self):
    """Menus for the SnapPyLinkEditor."""
    self.menubar = menubar = Tk_.Menu(self.window)
    Python_menu = Tk_.Menu(menubar, name=b'apple')
    Python_menu.add_command(label=b'About PLink...', command=self.about)
    Python_menu.add_separator()
    Python_menu.add_command(label=b'Preferences...', state=b'disabled')
    Python_menu.add_separator()
    if sys.platform in ('linux2', 'linux') and self.main_window is not None:
        Python_menu.add_command(label=b'Quit SnapPy', command=self.main_window.close)
    menubar.add_cascade(label=b'SnapPy', menu=Python_menu)
    File_menu = Tk_.Menu(menubar, name=b'file')
    add_menu(self.window, File_menu, b'Open...', self.load)
    add_menu(self.window, File_menu, b'Save as...', self.save)
    self.build_save_image_menu(menubar, File_menu)
    File_menu.add_separator()
    if self.callback:
        add_menu(self.window, File_menu, b'Close', self.done)
    else:
        add_menu(self.window, File_menu, b'Exit', self.done)
    menubar.add_cascade(label=b'File', menu=File_menu)
    Edit_menu = Tk_.Menu(menubar, name=b'snappyedit')
    add_menu(self.window, Edit_menu, b'Cut', None, state=b'disabled')
    add_menu(self.window, Edit_menu, b'Copy', None, state=b'disabled')
    add_menu(self.window, Edit_menu, b'Paste', None, state=b'disabled')
    add_menu(self.window, Edit_menu, b'Delete', None, state=b'disabled')
    menubar.add_cascade(label=b'Edit ', menu=Edit_menu)
    self._add_info_menu()
    self._add_tools_menu()
    self._add_style_menu()
    menubar.add_cascade(label=b'Window', menu=WindowMenu(menubar))
    Help_menu = Tk_.Menu(menubar, name=b'help')
    menubar.add_cascade(label=b'Help', menu=HelpMenu(menubar))
    Help_menu.add_command(label=b'PLink Help ...', command=self.howto)
    self.window.config(menu=menubar)
    return


def dirichlet_menus(self):
    """Menus for the standalone Dirichlet viewer."""
    self.menubar = menubar = Tk_.Menu(self.window)
    Python_menu = Tk_.Menu(menubar, name=b'apple')
    Python_menu.add_command(label=b'About SnapPy ...', command=lambda : about_snappy(self.window))
    Python_menu.add_separator()
    Python_menu.add_command(label=b'SnapPy Preferences ...', state=b'disabled')
    Python_menu.add_separator()
    if sys.platform in ('linux2', 'linux') and self.main_window is not None:
        Python_menu.add_command(label=b'Quit SnapPy', command=self.main_window.close)
    menubar.add_cascade(label=b'SnapPy', menu=Python_menu)
    File_menu = Tk_.Menu(menubar, name=b'file')
    add_menu(self.window, File_menu, b'Open...', None, b'disabled')
    add_menu(self.window, File_menu, b'Save as...', None, b'disabled')
    File_menu.add_command(label=b'Save Image...', command=self.save_image)
    Export_menu = Tk_.Menu(File_menu, name=b'export')
    File_menu.add_cascade(label=b'Export as STL...', menu=Export_menu)
    Export_menu.add_command(label=b'Export STL', command=self.export_stl)
    Export_menu.add_command(label=b'Export Cutout STL', command=self.export_cutout_stl)
    File_menu.add_separator()
    add_menu(self.window, File_menu, b'Close', command=self.close)
    menubar.add_cascade(label=b'File', menu=File_menu)
    menubar.add_cascade(label=b'Edit ', menu=EditMenu(menubar, self.edit_actions))
    menubar.add_cascade(label=b'Window', menu=WindowMenu(menubar))
    help_menu = HelpMenu(menubar)
    help_menu.extra_command(label=b'Polyhedron Viewer Help ...', command=self.widget.help)
    help_menu.activate(b'PolyhedronViewer Help ...')
    self.menubar.add_cascade(label=b'Help', menu=help_menu)
    return


def horoball_menus(self):
    """Menus for the standalone Horoball viewer."""
    self.menubar = menubar = Tk_.Menu(self.window)
    Python_menu = Tk_.Menu(menubar, name=b'apple')
    Python_menu.add_command(label=b'About SnapPy ...', command=lambda : about_snappy(self.window))
    Python_menu.add_separator()
    Python_menu.add_command(label=b'SnapPy Preferences ...', state=b'disabled')
    Python_menu.add_separator()
    if sys.platform in ('linux2', 'linux') and self.main_window is not None:
        Python_menu.add_command(label=b'Quit SnapPy', command=self.main_window.close)
    menubar.add_cascade(label=b'SnapPy', menu=Python_menu)
    File_menu = Tk_.Menu(menubar, name=b'file')
    File_menu.add_command(label=b'Open...', accelerator=scut[b'Open...'], state=b'disabled')
    File_menu.add_command(label=b'Save as...', accelerator=scut[b'Save as...'], state=b'disabled')
    Print_menu = Tk_.Menu(menubar, name=b'print')
    File_menu.add_command(label=b'Save Image...', command=self.save_image)
    File_menu.add_separator()
    File_menu.add_command(label=b'Close', command=self.close)
    menubar.add_cascade(label=b'File', menu=File_menu)
    menubar.add_cascade(label=b'Edit ', menu=EditMenu(menubar, self.edit_actions))
    menubar.add_cascade(label=b'Window', menu=WindowMenu(menubar))
    help_menu = HelpMenu(menubar)
    help_menu.extra_command(label=b'Horoball Viewer Help ...', command=self.widget.help)
    help_menu.activate(b'HoroballViewer Help ...')
    self.menubar.add_cascade(label=b'Help', menu=help_menu)
    return