# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylogo/ide.py
# Compiled at: 2007-10-14 14:35:27
import Tkinter, Pmw, threading
from pylogo import reader
from Queue import Queue, Empty
root = Pmw.initialise()

class IDE:
    __module__ = __name__

    def __init__(self, parent):
        self.incoming_history = Queue()
        self.incoming_commands = Queue()
        self.parent = parent
        self.menuBar = Pmw.MainMenuBar(parent)
        parent.configure(menu=self.menuBar)
        self.menuBar.addmenu('File', '')
        self.menuBar.addmenuitem('File', 'command', label='Exit', command=self.exit)
        self.parent.protocol('WM_DELETE_WINDOW', self.exit)
        self.menuBar.addmenu('Help', '')
        self.menuBar.addmenuitem('Help', 'command', label='About', command=self.about)
        self.pw = Pmw.PanedWidget(parent, hull_borderwidth=1, hull_relief='sunken')
        pane = self.pw.add('canvas', size=0.5)
        self.scroller = TurtleSpace(pane, canvas_width=1000, canvas_height=1000, canvas_background='white')
        self.scroller.pack(side='top', expand=1)
        pane3 = self.pw.add('history', size=0.4)
        self.history = Pmw.ScrolledText(pane3, borderframe=1, vscrollmode='static', text_width=70)
        self.history.pack(side='top', expand=1)
        pane2 = self.pw.add('entry', size=0.1)
        self.input = Pmw.EntryField(pane2, command=self.feed_input, entry_width=72)
        self.input.pack(side='top', expand=1)
        self.pw.pack(expand=1, fill='both')
        self.canvas = canvas = self.scroller.component('canvas')
        self.parent.after(100, self.idle_updates)

    def feed_input(self):
        value = self.input.getvalue() + '\n'
        self.logo_communicator.add_input(value)
        self.input.clear()
        self.update_history()
        self.update_commands()

    def idle_updates(self):
        self.update_history()
        self.update_commands()
        self.parent.after(100, self.idle_updates)

    def add_history(self, val):
        self.incoming_history.put(val)

    def update_history(self):
        history = []
        while 1:
            try:
                history.append(self.incoming_history.get_nowait())
            except Empty:
                break

        for line in history:
            if line.endswith('\n') and 0:
                line = line[:-1]
            self.history.appendtext(line)

    def exit(self):
        print 'Exiting!'
        self.parent.destroy()
        self.logo_communicator.exit()

    def about(self):
        Pmw.aboutversion('0.2')
        Pmw.aboutcopyright('Copyright Ian Bicking 2003')
        Pmw.aboutcontact('For more information:\n  http://pylogo.org')
        about = Pmw.AboutDialog(self.parent, applicationname='PyLogo')
        about.show()

    def update_commands(self):
        while 1:
            try:
                command = self.incoming_commands.get_nowait()
            except Empty:
                return

            if command == 'quit':
                self.exit()
            try:
                val = command[1](*command[2], **command[3])
            except Exception, e:
                if command[0]:
                    command[0].put([True, e])
            else:
                if command[0]:
                    command[0].put([False, val])

    def run_command(self, func, *args, **kw):
        if kw.has_key('_nowait'):
            nowait = kw['_nowait']
            del kw['_nowait']
        else:
            nowait = 0
        if nowait:
            out = None
        else:
            out = Queue(1)
        self.incoming_commands.put((out, func, args, kw))
        if out:
            (error, result) = out.get()
            if error:
                raise result
            else:
                return result
        return

    def add_command(self, func, *args, **kw):
        kw['_nowait'] = 1
        return self.run_command(func, *args, **kw)


class TurtleSpace(Pmw.ScrolledCanvas):
    __module__ = __name__

    def __init__(self, *args, **kw):
        Pmw.ScrolledCanvas.__init__(self, *args, **kw)


class LogoCommunicator:
    __module__ = __name__

    def __init__(self, app, interp):
        self.interp = interp
        self.app = app
        app.logo_communicator = self
        interp.canvas = app.canvas
        interp.app = app
        self.pending_input = Queue()
        self.pendingOutput = Queue()
        self.input_event = threading.Event()

    def start(self):
        self.logoThread = threading.Thread(target=self.interp.input_loop, args=(reader.TrackingStream(self), self))
        self.logoThread.start()

    def exit(self):
        self.add_input('bye\n')

    def add_input(self, value):
        if not value.endswith('\n'):
            value += '\n'
        self.app.add_history(value)
        self.pending_input.put(value)
        self.input_event.set()

    def readline(self):
        result = self.pending_input.get()
        return result

    def write(self, value):
        self.app.add_history(value)

    def flush(self):
        pass

    name = '<ide>'


from pylogo import interpreter

def add_command(command, *args, **kw):
    TheApp.add_command(command, *args, **kw)
    return TheApp


def get_canvas():
    return TheApp.canvas


def main():
    global TheApp
    import sys
    from pylogo import logo_turtle
    TheApp = IDE(root)
    TheApp.input.component('entry').focus_force()
    comm = LogoCommunicator(TheApp, interpreter.Logo)
    sys.stdout = comm
    interpreter.Logo.import_module(logo_turtle)
    logo_turtle.createturtle(interpreter.Logo)
    comm.start()
    root.mainloop()


if __name__ == '__main__':
    main()