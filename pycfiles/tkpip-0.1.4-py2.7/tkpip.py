# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkpip\tkpip.py
# Compiled at: 2017-07-31 08:19:52
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, os, re, logging
try:
    import pkg_resources, pip
except ImportError:
    os.system((b'{0} {1}').format(sys.executable, b'install_pip.py'))
    logging.warning(b'Restart required!')
    sys.exit(0)

try:
    from . import __pkgname__, __description__, __version__
    from .lib.backwardcompat import *
    from .lib.dist import *
    from .lib.dump import plain
    from .lib.listboxdata import ListBoxData
    from .lib.cache import pipcache
except:
    from __init__ import __pkgname__, __description__, __version__
    from lib.backwardcompat import *
    from lib.dist import *
    from lib.dump import plain
    from lib.listboxdata import ListBoxData
    from lib.cache import pipcache

class ScrolledText(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, relief=tk.SUNKEN)
        sbar1 = tk.Scrollbar(self, orient=tk.VERTICAL)
        sbar1.config(command=self.text.yview)
        self.text.config(yscrollcommand=sbar1.set)
        sbar2 = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        sbar2.config(command=self.text.xview)
        self.text.config(xscrollcommand=sbar2.set)
        self.text.config(wrap=tk.NONE)
        self.text.config(font=('Courier', 9, 'normal'))
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1)
        self.grid_rowconfigure(0, weight=1)
        self.text.grid(row=0, column=0, sticky=b'nwes')
        sbar1.grid(row=0, column=1, sticky=b'nwes')
        self.grid_rowconfigure(1)
        sbar2.grid(row=1, column=0, sticky=b'nwes')

    def appendText(self, text=b''):
        self.text.insert(tk.END, text)
        self.text.focus()

    def setText(self, text=b''):
        self.text.delete(1.0, tk.END)
        self.appendText(text)

    def getText(self):
        return self.text.get(b'1.0', tk.END + b'-1c')

    def bind(self, event, handler, add=None):
        self.text.bind(event, handler, add)


class StatusBar(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.labels = {}

    def setLabel(self, name=0, side=tk.LEFT, **kargs):
        label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W, **kargs)
        label.pack(side=side)
        self.labels[name] = label
        return label

    def setText(self, text=b'', name=0):
        if name in self.labels:
            label = self.labels[name]
        else:
            label = self.setLabel(name)
            self.labels[name] = label
        status = sys.executable
        if text:
            status += b' :: ' + text
        label.config(text=status)


class AppUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(b'tkPip')
        self.mode = None
        self.menubar = tk.Menu(self)
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'File', menu=menu)
        menu.add_command(command=self.onLoadSitePackages, label=b'Load site packages')
        menu.add_command(command=self.onLoadPipPackages, label=b'Load pip packages')
        menu.add_command(command=self.onLoadFile, label=b'Load pkglist from file')
        menu.add_separator()
        menu.add_command(command=self.onSaveFile, label=b'Save pkglist to file')
        menu.add_separator()
        menu.add_command(command=self.clear, label=b'Clear pkglist')
        menu.add_separator()
        menu.add_command(command=self.quit, label=b'Exit')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Dist', menu=menu)
        menu.add_command(command=self.onInstall, label=b'Install')
        menu.add_command(command=self.onUpgrade, label=b'Upgrade')
        menu.add_command(command=self.onUninstall, label=b'Uninstall')
        menu.add_separator()
        menu.add_command(command=self.onAppend, label=b'Append a package')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Debug', menu=menu)
        menu.add_command(command=self.onPypiCache, label=b'Pypi Cache')
        menu.add_command(command=self.onPrintData, label=b'Print Data')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Help', menu=menu)
        menu.add_command(command=self.onHelpAbout, label=b'About')
        self.config(menu=self.menubar)
        self.listbox = ListBoxData(self)
        sbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        sbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=sbar.set)
        self.text = ScrolledText(self)
        self.status = StatusBar(self)
        self.grid_columnconfigure(0, weight=1, minsize=160)
        self.grid_columnconfigure(1)
        self.grid_columnconfigure(2, weight=10, minsize=400)
        self.grid_rowconfigure(0, weight=1)
        self.listbox.grid(row=0, column=0, sticky=b'nwes')
        sbar.grid(row=0, column=1, sticky=b'nwes')
        self.text.grid(row=0, column=2, sticky=b'nwes')
        self.grid_rowconfigure(1)
        self.status.grid(row=1, column=0, columnspan=3, sticky=b'nwes')
        self.listbox.bind(b'<<ListboxSelect>>', self.onSelect)
        self.listbox.bind(b'<Double-Button-1>', self.onActivated)
        self.status.setText()
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        return

    def onLoadSitePackages(self):
        self.clear()
        self.mode = self.onLoadSitePackages
        distros = pkg_resources.Environment()
        items_dict = {}
        query_list = []
        for key in distros:
            query_list.append(key)
            for dist in distros[key]:
                self.append_item(items_dict, key, dist)

        self.listbox.insert_items(items_dict)
        self.status.setText(b'Updating cache...')
        pipcache.query_info(query_list, self.afterUpdate)

    def onLoadPipPackages(self):
        self.clear()
        self.mode = self.onLoadPipPackages
        distros = pip.get_installed_distributions()
        items_dict = {}
        query_list = []
        for dist in distros:
            query_list.append(dist.key)
            self.append_item(items_dict, dist.key, dist)

        self.listbox.insert_items(items_dict)
        self.status.setText(b'Updating cache...')
        pipcache.query_info(query_list, self.afterUpdate)

    def onLoadFile(self):
        self.clear()
        self.mode = self.onLoadFile
        filename = askopenfilename()
        if filename:
            items_dict = {}
            query_list = []
            with open(filename) as (f):
                distros = pkg_resources.Environment()
                for line in f:
                    line_list = line.split()
                    if line_list:
                        key = line_list[0].lower()
                        if re.match(b'^[a-z][a-z0-9]*$', key):
                            query_list.append(key)
                            dist = distros[key]
                            dist = dist[0] if dist else None
                            self.append_item(items_dict, key, dist)

            self.listbox.insert_items(items_dict)
            self.status.setText(b'Updating cache...')
            pipcache.query_info(query_list, self.afterUpdate)
        return

    def onSaveFile(self):
        filename = asksaveasfilename()
        if filename:
            with open(filename, b'w') as (f):
                for i, value, data in self.listbox:
                    if value:
                        f.write((b'{0}\n').format(value))

    def onActivated(self, event=None):
        self.status.setText(b'Processing...')
        selected, value, data = self.listbox.get_selected()
        if selected:
            key = data.get(b'key')
            if key:
                if b'[I]' in value:
                    dist_install(key)
                elif b'[U]' in value:
                    dist_upgrade(key)
        self.updateMode()

    def onInstall(self, event=None):
        self.status.setText(b'Processing...')
        selected, value, data = self.listbox.get_selected()
        if selected:
            key = data.get(b'key')
            if key:
                dist_install(key)
        self.updateMode()

    def onUpgrade(self, event=None):
        self.status.setText(b'Processing...')
        selected, value, data = self.listbox.get_selected()
        if selected:
            key = data.get(b'key')
            if key:
                dist_upgrade(key)
        self.updateMode()

    def onUninstall(self, event=None):
        self.status.setText(b'Processing...')
        selected, value, data = self.listbox.get_selected()
        if selected:
            key = data.get(b'key')
            if key:
                dist_uninstall(key, data.get(b'dist'))
        self.updateMode()

    def onAppendPkg(self, event=None):
        pkgname = self.ask_entry1.get().strip()
        self.ask.destroy()
        if pkgname:
            self.status.setText(b'Processing...')
            dist_install(pkgname)
            self.updateMode()

    def onAppend(self, event=None):
        self.ask = tk.Toplevel()
        self.ask.title(b'Enter a package name')
        self.ask_entry1 = tk.Entry(self.ask)
        self.ask_entry1[b'width'] = 50
        self.ask_entry1.pack(side=tk.LEFT)
        self.ask_entry1.pack()
        button1 = tk.Button(self.ask, text=b'Submit', command=self.onAppendPkg)
        button1.pack()
        self.ask_entry1.focus_set()

    def onPypiCache(self):
        for key, name, ver, data, urls, releases in pipcache:
            print((b'{0} [{1}]: {2} {3!r}').format(key, name, ver, releases))
            print(repr(data)[:200] + b'...')
            print(repr(urls)[:200] + b'...')

    def onPrintData(self):
        selected, value, data = self.listbox.get_selected()
        print(selected)
        for i, value, data in self.listbox:
            print(i, value)
            print(data)

    def onHelpAbout(self, event=None):
        text = (b'{0}\n{1}\nVersion {2}\n\nPython: {3}\nPackage: {4}\n').format(__pkgname__, __description__, __version__, sys.version, __package__)
        showinfo(b'About', text)

    def onSelect(self, event=None):
        selected, value, data = self.listbox.get_selected()
        if data is None:
            self.text.setText(b'No data!')
            return
        else:
            key = data.get(b'key')
            if key is None:
                self.text.setText(b'Wrong data!')
                return
            dist = data.get(b'dist')
            if dist:
                installed = dist.version
                state = b'active' if data[b'active'] else b'non-active'
                dist_dump = plain(dist)
            else:
                installed = b'<Not installed>'
                state = b'none'
                dist_dump = b'none\n'
            name, ver, data, urls, releases = pipcache.get(key)
            data_dump = plain(data)
            urls_dump = b''
            for i in urls:
                urls_dump += (b'{0}\n---\n').format(plain(i))

            text = (b'{0} [{1}] ({2})\nInstalled: {3}\nLatest:    {4} {5!r}\n\n=== Dist dump\n{6}\n=== Data dump\n{7}\n=== Urls dump\n{8}').format(key, name, state, installed, ver, releases, dist_dump, data_dump, urls_dump)
            self.text.setText(text)
            return

    def clear(self):
        self.mode = None
        self.listbox.clear()
        self.text.setText()
        return

    def updateMode(self):
        self.status.setText()
        if self.mode:
            self.mode()

    def append_item(self, items_dict, key, dist=None):
        active = dist in pkg_resources.WorkingSet() if dist else None
        data = dict(key=key, active=active, dist=dist)
        label = self.get_label(data)
        style = self.get_style(data)
        items_dict[label] = data
        items_dict[label][b'_item'] = style
        return

    def get_label(self, data):
        key = data[b'key']
        active = data[b'active']
        if active is None:
            label = (b'{0} [I]').format(key)
        else:
            label = (b'{0} {1}').format(key, data[b'dist'].version)
        return label

    def get_style(self, data):
        active = data[b'active']
        style = {}
        if active is None:
            style = dict(background=b'Lemonchiffon')
        elif active == False:
            style = dict(background=b'Gray')
        return style

    def afterUpdate(self, *args):
        for i, value, data in self.listbox:
            if value and data:
                dist = data.get(b'dist')
                if dist:
                    active = data[b'active']
                    installed = dist.version
                    name, ver, data, urls, releases = pipcache.get(dist.key)
                    if installed != ver and active != False:
                        self.listbox.setValue(i, value + b' [U]')
                        self.listbox.itemconfig(i, dict(background=b'Lightgreen'))

        self.status.setText()


def main():
    root = AppUI()
    root.mainloop()


if __name__ == b'__main__':
    logging.basicConfig(level=logging.INFO)
    main()