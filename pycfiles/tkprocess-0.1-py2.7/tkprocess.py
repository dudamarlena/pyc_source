# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkprocess\tkprocess.py
# Compiled at: 2018-06-26 15:47:21
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, os, subprocess, time
from threading import Event, Thread
from . import __pkgname__, __description__, __version__
from .core.backwardcompat import *
from .core.settings import Settings
py_version = sys.version_info[:2]
PY2 = py_version[0] == 2
if PY2:
    from Queue import Queue
    getcwd = os.getcwdu
else:
    from queue import Queue
    getcwd = os.getcwd
q = Queue()
s = Settings()
s.saveEnv()

def call_repeatedly(interval, func, *args):
    stopped = Event()

    def loop():
        while not stopped.wait(interval):
            func(*args)

    Thread(target=loop).start()
    return stopped.set


def do_stuff(stopped, status):
    while True:
        cmd, text = q.get()
        text.setText()
        start = text.text.index(tk.CURRENT)
        text.appendText(cmd)
        stop = text.text.index(tk.CURRENT)
        text.text.tag_add(b'highlighted', start, stop)
        text.appendText(b'\n')
        run_command_0(stopped, cmd, text, status)
        q.task_done()


def do_print(pipe, text):
    for line in iter(pipe.readline, b''):
        if line:
            text.appendText(line)


def run_command_0(stopped, cmd, text, status):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    t = time.time()
    th1 = Thread(target=do_print, args=(process.stdout, text))
    th1.setDaemon(True)
    th1.start()
    th2 = Thread(target=do_print, args=(process.stderr, text))
    th2.setDaemon(True)
    th2.start()
    status.running = True
    while status.running:
        sec = time.time() - t
        rc = process.poll()
        if rc is None:
            status.update_status((b'Running {0:.2f} sec...').format(sec))
        else:
            status.update_status((b'Finished in {0:.2f} sec with code: {1}').format(sec, rc))
            status.running = False
        if stopped.isSet():
            status.update_status((b'Released after {0:.2f} sec ').format(sec))
            status.running = False
            stopped.clear()
        time.sleep(1)

    return


class ScrolledText(tk.Frame):

    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, relief=tk.SUNKEN)
        self.text.pack(fill=tk.BOTH, side=tk.LEFT, expand=tk.YES)
        sbar = tk.Scrollbar(self)
        sbar.pack(fill=tk.Y, side=tk.RIGHT)
        sbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=sbar.set)
        self.text.config(font=('Courier', 9, 'normal'))
        self.text.tag_config(b'highlighted', background=b'green', foreground=b'blue')

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
        self.running = False

    def setLabel(self, name=0, side=tk.LEFT, **kargs):
        label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W, **kargs)
        label.pack(side=side)
        self.labels[name] = label
        return label

    def setText(self, text=b'', name=0, side=tk.LEFT, **kargs):
        if name in self.labels:
            label = self.labels[name]
        else:
            label = self.setLabel(name, side, **kargs)
        label.config(text=text)

    def update_cwd(self):
        self.setText(getcwd(), 0)

    def update_time(self, **kargs):
        self.setText(time.strftime(b'%H:%M:%S'), 1, **kargs)

    def update_status(self, text, **kargs):
        self.setText(text, 2, **kargs)


class AppUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(b'tkProcess')
        self.cmd = tk.StringVar()
        self.menubar = tk.Menu(self)
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'File', menu=menu)
        menu.add_command(command=self.onClosing, label=b'Exit')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Help', menu=menu)
        menu.add_command(command=self.onAbout, label=b'About')
        self.config(menu=self.menubar)
        line1 = tk.Frame(self)
        self.entry = ttk.Combobox(line1, textvariable=self.cmd)
        cmds = s.get(b'cmds', [b'dir'])
        self.setEntry(cmds)
        self.entry.current(0)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.button1 = tk.Button(line1, text=b'Exec')
        self.button1.pack(side=tk.RIGHT)
        line1.pack(fill=tk.X)
        self.text = ScrolledText(self)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.status = StatusBar(self)
        self.status.pack(fill=tk.X)
        self.status.update_cwd()
        self.status.update_time(side=tk.RIGHT)
        self.status.update_status(b'Idle', side=tk.RIGHT)
        self.button1.bind(b'<Button-1>', self.onExec)
        self.entry.bind(b'<KeyPress-Return>', self.onExec)
        self.cancel_future_calls = call_repeatedly(1, self.status.update_time)
        self.stopped = Event()
        self.worker = Thread(target=do_stuff, args=(self.stopped, self.status))
        self.worker.setDaemon(True)
        self.worker.start()
        self.protocol(b'WM_DELETE_WINDOW', self.onClosing)
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def onAbout(self, event=None):
        text = (b'{0}\n{1}\nVersion {2}\n\nPython: {3}\nBinary: {4}\n').format(__pkgname__, __description__, __version__, sys.version, sys.executable)
        showinfo(b'About', text)

    def onExec(self, event=None):
        if self.status.running:
            if askokcancel(b'Release', b'Do you want to release the process?\nThe process will stay running in background!'):
                if self.status.running:
                    self.stopped.set()
        else:
            cmd = self.cmd.get()
            cmds = s.insert(b'cmds', 0, cmd, 2)
            self.setEntry(cmds)
            q.put((cmd, self.text))

    def onClosing(self, event=None):
        if askokcancel(b'Quit', b'Do you want to quit?'):
            self.cancel_future_calls()
            self.destroy()

    def setEntry(self, values_list=[]):
        self.entry[b'values'] = values_list


def main():
    root = AppUI()
    root.mainloop()