# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Compose/GUI/TextOutputGUI.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.UI.Tk.TkWindow import TkWindow
from Kamaelia.Support.Tk.Scrolling import ScrollingMenu
from Axon.Ipc import producerFinished, shutdownMicroprocess
import Tkinter

class TextOutputGUI(TkWindow):

    def __init__(self, title):
        self.title = title
        self.allreceived = True
        super(TextOutputGUI, self).__init__()

    def setupWindow(self):
        self.textbox = Tkinter.Text(self.window, cnf={'state': Tkinter.DISABLED})
        self.window.title(self.title)
        self.textbox.grid(row=0, column=0, sticky=Tkinter.N + Tkinter.E + Tkinter.W + Tkinter.S)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.protocol('WM_DELETE_WINDOW', self.handleCloseWindowRequest)

    def main(self):
        while not self.isDestroyed():
            if self.dataReady('inbox'):
                self.textbox.config(state=Tkinter.NORMAL)
                if self.allreceived:
                    self.allreceived = False
                    self.textbox.delete(1.0, Tkinter.END)
                while self.dataReady('inbox'):
                    data = self.recv('inbox')
                    if data == None:
                        self.allreceived = True
                    else:
                        self.textbox.insert(Tkinter.END, data)

                self.textbox.config(state=Tkinter.DISABLED)
            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, shutdownMicroprocess) or isinstance(msg, producerFinished):
                    self.send(msg, 'signal')
                    self.window.destroy()

            self.tkupdate()
            yield 1

        return

    def handleCloseWindowRequest(self):
        self.send(shutdownMicroprocess(self), 'signal')
        self.window.destroy()


if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    import Axon, time

    class Source(Axon.Component.component):
        """A simple data source"""

        def __init__(self, data=None):
            super(Source, self).__init__()
            if data == None:
                data = []
            self.data = data
            return

        def main(self):
            for item in iter(self.data):
                self.send(item, 'outbox')
                yield 1


    class TimedPassthrough(Axon.ThreadedComponent.threadedcomponent):

        def __init__(self, delay=1):
            super(TimedPassthrough, self).__init__()
            self.delay = delay

        def main(self):
            while 1:
                time.sleep(self.delay)
                if self.dataReady('inbox'):
                    data = self.recv('inbox')
                    self.send(data, 'outbox')


    Pipeline(Source(['H\n', None,
     'Hel\n', None,
     'Hello \n', None,
     'Hello Wo\n', None,
     'Hello World\n']), TimedPassthrough(0.1), TextOutputGUI('Basic Display')).run()