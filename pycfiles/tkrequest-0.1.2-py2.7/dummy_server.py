# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkrequest\dummy_server.py
# Compiled at: 2013-08-30 08:40:17
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, threading, webbrowser
try:
    from .lib.info import __pkgname__, __description__, __version__
    from .lib.backwardcompat import *
    from .lib.dump import plain
    from .lib.settings import Settings
except:
    from lib.info import __pkgname__, __description__, __version__
    from lib.backwardcompat import *
    from lib.dump import plain
    from lib.settings import Settings

s = Settings()
s.saveEnv()

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
        self.title(b'tkDummyServer')
        self.server = None
        self.host = tk.StringVar()
        self.port = tk.StringVar()
        self.menubar = tk.Menu(self)
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'File', menu=menu)
        menu.add_command(command=self.quit, label=b'Exit')
        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=b'Help', menu=menu)
        menu.add_command(command=self.onHelpAbout, label=b'About')
        self.config(menu=self.menubar)
        line1 = tk.Frame(self)
        entry1 = tk.Entry(line1, textvariable=self.host)
        entry1.pack(side=tk.LEFT, fill=tk.X, expand=1)
        vcmd = (
         self.register(validate_port), b'%P')
        entry2 = tk.Entry(line1, textvariable=self.port, validate=b'key', validatecommand=vcmd)
        entry2.pack(side=tk.LEFT, fill=tk.X)
        self.host.set(s.get(b'server_host', b'localhost'))
        self.port.set(s.get(b'server_port', b'80'))
        button1 = tk.Button(line1, text=b'Start/stop server')
        button1.pack(side=tk.RIGHT)
        line1.pack(fill=tk.X)
        self.text = ScrolledText(self)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.status = StatusBar(self)
        self.status.pack(fill=tk.X)
        button1.bind(b'<Button-1>', self.onStartServer)
        entry1.bind(b'<KeyPress-Return>', self.onStartServer)
        entry2.bind(b'<KeyPress-Return>', self.onStartServer)
        self.bind(b'<w>', self.onOpenLink)
        self.status.setText()
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())
        return

    def onHelpAbout(self, event=None):
        text = (b'{0}\n{1}\nVersion {2}\n\nPython: {3}\nPackage: {4}\n').format(__pkgname__, __description__, __version__, sys.version, __package__)
        showinfo(b'About', text)

    def onStartServer(self, event=None):
        if self.server is None:
            host = self.host.get()
            port = self.port.get()
            port = int(port) if port else 80
            s.set(b'server_host', host)
            s.set(b'server_port', port)
            self.status.setText(b'Server started!')
            t = threading.Thread(target=self.startServer, args=(host, port))
            t.daemon = True
            t.start()
        else:
            self.status.setText()
            self.server.shutdown()
            self.server = None
        return

    def onOpenLink(self, event=None):
        host = self.host.get()
        port = self.port.get()
        if port:
            port = b':' + port
        url = b'http://' + host + port
        if event.state == 4:
            webbrowser.open(url)
        if event.state == 0:
            wtype = event.widget.winfo_class()
            if wtype not in ('Entry', 'Text', 'TCombobox'):
                webbrowser.open(url)

    def startServer(self, host, port):
        self.server = MyServer((host, port), MyHandler, self.text)
        self.server.serve_forever()


class MyServer(SocketServer.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, scrolled_text):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
        self.text = scrolled_text


class MyHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.request.send(self.data)
        text = (b'=== {0} ===\n{1}\n').format(self.client_address[0], plain(self.data))
        if self.server.text:
            self.server.text.setText(text)
        else:
            print(text)


def validate_port(value):
    if not value:
        return True
    if value.isdigit() and int(value) < 65536:
        return True
    return False


def main():
    root = AppUI()
    root.mainloop()


if __name__ == b'__main__':
    main()