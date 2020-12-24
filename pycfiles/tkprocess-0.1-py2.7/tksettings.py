# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkprocess\tksettings.py
# Compiled at: 2018-06-26 14:45:24
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, os, glob, importlib, logging
try:
    from . import __pkgname__, __description__, __version__
    from .core.backwardcompat import *
    from .core.dump import plain
    from .core.settings import Settings
    from .core.tkprop import propertyDialog
except:
    from __init__ import __pkgname__, __description__, __version__
    from core.backwardcompat import *
    from core.dump import plain
    from core.settings import Settings
    from core.tkprop import propertyDialog

def import_file(filename):
    dirname, basename = os.path.split(filename)
    sys.path.insert(0, dirname)
    root, ext = os.path.splitext(basename)
    try:
        module = importlib.import_module(root)
    except Exception as e:
        module = None
        logging.exception(e)

    del sys.path[0]
    return module


class AppUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(b'tkSettings')
        self.menubar = tk.Menu(self)
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'File', menu=menu)
        menu.add_command(command=self.onLoadDefault, label=b'Load default')
        menu.add_command(command=self.onLoadFile, label=b'Load file')
        menu.add_separator()
        menu.add_command(command=self.quit, label=b'Exit')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Edit', menu=menu)
        menu.add_command(command=self.onCleanData, label=b'Clean data')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Batch import', menu=menu)
        menu.add_command(command=self.onBatch1, label=b'File to file')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Help', menu=menu)
        menu.add_command(command=self.onAbout, label=b'About')
        self.config(menu=self.menubar)
        self.frame1 = tk.Frame(self)
        button = tk.Button(self.frame1, text=b'Settings')
        button.pack()
        button.bind(b'<Button-1>', self.onShowSettings)
        button = tk.Button(self.frame1, text=b'Save test data')
        button.pack()
        button.bind(b'<Button-1>', self.onSaveTestData)
        button = tk.Button(self.frame1, text=b'Import from module')
        button.pack()
        button.bind(b'<Button-1>', self.onImportFromModule)
        button = tk.Button(self.frame1, text=b'Import from module to branch')
        button.pack()
        button.bind(b'<Button-1>', self.onImportFromModuleToBranch)
        button = tk.Button(self.frame1, text=b'Import from dir')
        button.pack()
        button.bind(b'<Button-1>', self.onImportFromDir)
        button = tk.Button(self.frame1, text=b'Import from dir to branch')
        button.pack()
        button.bind(b'<Button-1>', self.onImportFromDirToBranch)
        dFont1 = Font(family=b'Courier', size=9)
        self.text1 = tk.Text(self, font=dFont1)
        self.text1_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text1.yview)
        self.text1[b'yscrollcommand'] = self.text1_y.set
        self.status = tk.StringVar()
        label1 = tk.Label(self, textvariable=self.status, anchor=tk.W)
        self.setStatus()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=120)
        self.grid_columnconfigure(1, weight=5, minsize=400)
        self.grid_columnconfigure(2)
        self.frame1.grid(row=0, column=0, sticky=b'nwes')
        self.text1.grid(row=0, column=1, sticky=b'nwes')
        self.text1_y.grid(row=0, column=2, sticky=b'nwes')
        self.grid_rowconfigure(1)
        label1.grid(row=1, column=0, columnspan=4, sticky=b'nwes')
        self.onLoadDefault()
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def appendText(self, text=b''):
        self.text1.insert(tk.INSERT, (b'{0}\n').format(plain(text)))

    def setText(self, text=b''):
        self.text1.delete(1.0, tk.END)
        self.appendText(text)

    def setStatus(self, text=b''):
        self.status.set(text)

    def showInfo(self):
        self.setText(b'System:')
        self.appendText(self.s.get_systems())
        self.appendText(b'Settings:')
        self.appendText(self.s.get_dict())
        self.setStatus(self.s.get_filename())

    def onAbout(self, event=None):
        text = (b'{0}\n{1}\nVersion {2}\n\nPython: {3}\nBinary: {4}\n').format(__pkgname__, __description__, __version__, sys.version, sys.executable)
        showinfo(b'About', text)

    def onLoadDefault(self):
        self.s = Settings()
        self.showInfo()

    def onLoadFile(self):
        initialdir = os.path.expanduser(b'~')
        filename = askopenfilename(initialdir=initialdir, filetypes=[
         ('Config files', '*.pickle'),
         ('All files', '*.*')])
        if filename:
            self.s = Settings(filename=filename)
            self.showInfo()

    def onCleanData(self):
        response = askquestion(b'Clean data', b'Are you sure you want to permanently delete all information from the config?')
        if response == b'yes':
            self.s.clean()
            self.showInfo()

    def onBatch1(self):
        dfilename = askdirectory()
        if dfilename:
            pickles = []
            for filename in glob.glob(os.path.join(dfilename, b'*.py')):
                module = import_file(filename)
                if module:
                    basename = os.path.basename(filename)
                    root, ext = os.path.splitext(basename)
                    logging.debug(root)
                    BRANCH = Settings(root)
                    pickles.append(BRANCH.get_filename())
                    for i in dir(module):
                        if i[0] != b'_':
                            value = getattr(module, i)
                            if isinstance(value, all_types):
                                BRANCH.set(i, value)

            message = b'Processed pickles:\n' + plain(pickles) + b'\n\n' + b'Note: Empty pickles was not created!'
            showinfo(b'Info', message)
            self.setText()
            self.setStatus()

    def onShowSettings(self, event):
        propertyDialog(self.s.get_dict())

    def onSaveTestData(self, event):
        self.s.saveEnv()
        self.s.set_path(b'test_instance', b'$')
        self.s.set_path(b'test_home', b'~')
        self.s.set_path(b'test_location', b'~~', True)
        self.s.set_path(b'test_app', b'~~~', True)
        self.showInfo()

    def onImportFromModuleToBranch(self, event):
        self.onImportFromModule(event, tobranch=True)

    def onImportFromModule(self, event, tobranch=False):
        filename = askopenfilename(filetypes=[
         ('Python files', '*.py'),
         ('All files', '*.*')])
        if filename:
            module = import_file(filename)
            if module:
                if tobranch:
                    branch = module.__name__
                    BRANCH = self.s.get_group(branch)
                else:
                    BRANCH = self.s
                for i in dir(module):
                    if i[0] != b'_':
                        value = getattr(module, i)
                        if isinstance(value, dict) and isinstance(BRANCH.get(i), dict):
                            BRANCH.update(value)
                        elif isinstance(value, all_types):
                            BRANCH.set(i, value)

                self.showInfo()

    def onImportFromDirToBranch(self, event):
        self.onImportFromDir(event, tobranch=True)

    def onImportFromDir(self, event, tobranch=False):
        dfilename = askdirectory()
        if dfilename:
            basename = os.path.basename(dfilename)
            logging.debug(basename)
            ROOT = self.s
            for filename in glob.glob(os.path.join(dfilename, b'*.py')):
                module = import_file(filename)
                if module:
                    if tobranch:
                        branch = module.__name__
                        BRANCH = self.s.get_group(branch)
                    else:
                        BRANCH = self.s
                    for i in dir(module):
                        if i[0] != b'_':
                            value = getattr(module, i)
                            if isinstance(value, all_types):
                                BRANCH.set(i, value)

            self.showInfo()


def main():
    root = AppUI()
    root.mainloop()


if __name__ == b'__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()