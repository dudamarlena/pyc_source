# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Compose/GUI/ArgumentsPanel.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.UI.Tk.TkWindow import TkWindow
from Kamaelia.Support.Tk.Scrolling import ScrollingMenu
from Axon.Ipc import producerFinished, shutdownMicroprocess
import Tkinter, pprint

class ArgumentsPanel(Tkinter.Frame):

    def __init__(self, parent, theclass):
        Tkinter.Frame.__init__(self, parent)
        self.theclass = theclass
        row = 0
        if self.theclass['classdoc']:
            self.classdoclabel = Tkinter.Label(self, text=self.theclass['classdoc'], justify='left')
            self.classdoclabel['font'] = (' ').join(self.classdoclabel['font'].split(' ')[0:2])
            self.classdoclabel.grid(row=row, column=0, columnspan=2, sticky=Tkinter.N + Tkinter.E + Tkinter.W + Tkinter.S, padx=4, pady=4)
            row += 1
        if self.theclass['initdoc']:
            self.initdoclabel = Tkinter.Label(self, text=self.theclass['initdoc'], justify='left')
            self.initdoclabel['font'] = (' ').join(self.initdoclabel['font'].split(' ')[0:2])
            self.initdoclabel.grid(row=row, column=0, columnspan=2, sticky=Tkinter.N + Tkinter.E + Tkinter.W + Tkinter.S, padx=4, pady=4)
            row += 1
        self.label = Tkinter.Label(self, text='ARGUMENTS:')
        self.label.grid(row=row, column=0, columnspan=2, sticky=Tkinter.W + Tkinter.S, padx=4, pady=4)
        row += 1
        self.args = []
        for arg in self.theclass['args']['std']:
            arglabel = Tkinter.Label(self, text=arg[0])
            arglabel.grid(row=row, column=0, sticky=Tkinter.E)
            svar = Tkinter.StringVar()
            argfield = Tkinter.Entry(self, bg='white', textvariable=svar, takefocus=1)
            default = ''
            if len(arg) >= 2:
                default = arg[1]
                svar.set(default)
            argfield.grid(row=row, column=1, sticky=Tkinter.W)
            self.args.append((arg[0], svar, default))
            row += 1

        for argname in ['*', '**']:
            if self.theclass['args'][argname]:
                arglabel = Tkinter.Label(self, text=argname)
                arglabel.grid(row=row, column=0, sticky=Tkinter.E)
                arglabel = None
                svar = Tkinter.StringVar()
                argfield = Tkinter.Entry(self, bg='white', textvariable=svar, takefocus=1)
                argfield.grid(row=row, column=1, sticky=Tkinter.W)
                self.args.append((argname, svar, ''))
                row += 1

        return

    def getDef(self):
        return {'name': self.theclass['class'], 'module': self.theclass['module'], 
           'instantiation': self.getInstantiation(), 
           'configuration': self.getConfiguration()}

    def getConfiguration(self):
        """Return the instantiation string"""
        argstr = ''
        prefix = ''
        SEQUENTIALARGS = []
        TUPLEARGS = None
        DICTARGS = None
        for (argname, svar, default) in self.args:
            unspecified = False
            value = None
            text = svar.get().strip()
            default = default.strip()
            if argname != '*':
                if argname != '**' and (default == '' or text != default):
                    if not text:
                        unspecified = True
                    value = text
                SEQUENTIALARGS.append([argname, unspecified, value, default])
            elif text:
                if argname == '*':
                    TUPLEARGS = text
                if argname == '**':
                    DICTARGS = text

        return {'args': SEQUENTIALARGS, 'tupleargs': TUPLEARGS, 
           'dictargs': DICTARGS, 
           'theclass': self.theclass['theclass']}

    def getInstantiation(self):
        """Return the instantiation string"""
        argstr = ''
        prefix = ''
        for (argname, svar, default) in self.args:
            text = svar.get().strip()
            default = default.strip()
            if argname != '*' and argname != '**':
                if argname[0] == '[' and argname[(-1)] == ']':
                    if text:
                        argname = argname[1:-1]
                        argstr = argstr + prefix + argname + ' = ' + text
                        prefix = ', '
                elif default == '' or text != default:
                    if not text:
                        text = '<<unspecified>>'
                    argstr = argstr + prefix + argname + ' = ' + text
                    prefix = ', '
            elif text:
                argstr = argstr + prefix + text
                prefix = ', '

        return argstr