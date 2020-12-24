# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lather_ui\lather_ui.py
# Compiled at: 2017-05-23 11:50:05
from __future__ import unicode_literals, print_function, division, absolute_import
try:
    import Tkinter, tkFileDialog, tkMessageBox, Tkconstants, ScrolledText
except ImportError:
    import tkinter as Tkinter
    from tkinter import filedialog as tkFileDialog, messagebox as tkMessageBox, constants as Tkconstants, scrolledtext as ScrolledText

import logging, sys, os
from .lather_client import SudsClientWrapper
from .helpers import AbstractWindow, RedirectText

class XMLFormWindow(AbstractWindow):

    def __init__(self, callback, method):
        self.root = Tkinter.Toplevel()
        self.frame = Tkinter.Frame(self.root)
        self.callback = callback
        self.method = method
        self.param_stringVars = {}
        self.param_infos = {}
        self.method_signature = None
        return

    def buildForm(self, method_signature):
        method_params = method_signature[b'params']
        self.method_signature = method_signature
        print(b'BUILDING FORM....', end=b'')
        print(method_signature)
        frame = Tkinter.Frame(self.root)
        for param_key in method_params:
            param = param_key.split(b' ')
            if param[0].split(b':')[0] == b'xs':
                Tkinter.Label(frame, text=param_key).pack()
                self.param_stringVars[param_key] = Tkinter.StringVar()
                Tkinter.Entry(frame, textvariable=self.param_stringVars[param_key], width=60).pack()
            else:
                Tkinter.Label(frame, text=(b'This is a complex element... not yet supported. type is {}').format(param_key)).pack()
            frame.pack()

        Tkinter.Button(frame, text=b'SUBMIT', command=self.submitForm).pack()

    def pack_StringVarToStrings(self, param_stringVars):
        """ get raw string types from StrinVars """
        packed_params = {}
        for param_key in param_stringVars.keys():
            packed_params[param_key] = param_stringVars[param_key].get()

        return packed_params

    def pack_removeEmptyStrings(self, param_stringVars):
        """ Remove Empty Parameters from the Dictionary """
        packed_params = {}
        for param_key in param_stringVars.keys():
            if self.param_stringVars[param_key].get() is not b'':
                packed_params[param_key] = self.param_stringVars[param_key]

        return packed_params

    def submitForm(self):
        call_params = {}
        call_params = self.pack_removeEmptyStrings(self.param_stringVars)
        call_params = self.pack_StringVarToStrings(call_params)
        self.callback(self.method, call_params)
        self.root.destroy()


class MainWindow(Tkinter.Tk):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.soap_client = None
        self.file_opt = options = {}
        self.frame = Tkinter.Frame(self)
        self.frame.pack()
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.current_url = Tkinter.StringVar()
        self.current_url.set(b'http://www.webservicex.com/globalweather.asmx?WSDL')
        button_style = {b'fill': Tkconstants.BOTH, b'padx': 5, b'pady': 5}
        self.buttonFrame = leftFrame = Tkinter.Frame()
        self.disposableFrame = disposableFrame = Tkinter.Frame()
        self.generate_Type_lbl = Tkinter.Label(disposableFrame, text=b'GENERATE TYPES:')
        self.generate_Type_lbl.pack()
        leftFrame.pack(side=b'left', fill=b'y')
        self.topFrame = topFrame = Tkinter.Frame()
        self.url_field = Tkinter.Entry(topFrame, textvariable=self.current_url, width=180)
        self.url_field.pack(side=b'left', fill=b'both')
        self.get_wsdl_btn = Tkinter.Button(topFrame, text=b'Get WSDL', command=self.get_wsdl).pack(side=b'left')
        topFrame.pack(fill=b'both')
        self.middleFrame = middleFrame = Tkinter.Frame()
        self.console_left = ScrolledText.ScrolledText(middleFrame)
        self.console_left.pack(side=b'left', fill=b'y')
        self.re_left = RedirectText(self.console_left)
        self.console_right = ScrolledText.ScrolledText(middleFrame)
        self.console_right.pack(side=b'right', fill=b'y')
        self.re_right = RedirectText(self.console_right)
        middleFrame.pack()
        self.bottomFrame = bottomFrame = Tkinter.Frame()
        self.console_bottom = ScrolledText.ScrolledText(bottomFrame)
        self.console_bottom.pack(side=b'left', fill=b'both', expand=True)
        self.re_bottom = RedirectText(self.console_bottom)
        sys.stdout = self.re_bottom
        bottomFrame.pack(fill=b'both')
        self.re_left.write(b'LEFT CONSOLE')
        self.re_right.write(b'RIGHT CONSOLE')
        self.re_bottom.write(b'BOTTOM CONSOLE')
        options[b'filetypes'] = [
         ('all files', '.*'), ('text files', '.txt')]
        options[b'initialdir'] = os.getcwd()
        options[b'parent'] = self
        options[b'title'] = b'select a file: '
        menubar = Tkinter.Menu(self)
        filemenu = Tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label=b'', command=self.hello)
        filemenu.add_command(label=b'Save', command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label=b'Exit', command=self.quit)
        menubar.add_cascade(label=b'File', menu=filemenu)
        runMenu = Tkinter.Menu(menubar, tearoff=0)
        runMenu.add_command(label=b'Jmeter GUI', command=self.hello)
        runMenu.add_command(label=b'JMX Test via Console', command=self.hello)
        runMenu.add_command(label=b'run Selected JMX', command=self.hello)
        menubar.add_cascade(label=b'Run...', menu=runMenu)
        plugin_menu = Tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(labe=b'Plugins', menu=plugin_menu)
        self.config(menu=menubar)
        self.title(b'SUDS UI v0.0.01-SNAPSHOT - SoapUI Alternative in Python/Legacy Python')
        return

    def hello(self):
        tkMessageBox.showinfo(b'INFO:', b'This feature is not implemented yet')

    def run(self):
        self.mainloop()

    def get_wsdl(self):
        url = self.current_url.get()
        self.soap_client = SudsClientWrapper(url)
        self.build_operation_buttons()

    def build_operation_buttons(self):
        self.disposableFrame.destroy()
        self.disposableFrame = disposableFrame = Tkinter.Frame(self.buttonFrame)
        self.generate_Type_lbl = Tkinter.Label(disposableFrame, text=b'GENERATE TYPES:')
        self.generate_Type_lbl.pack()
        disposableFrame.pack(side=b'left', fill=b'y')
        services = self.soap_client.auto_discovered_services
        print(services)
        for s in services.keys():
            Tkinter.Label(disposableFrame, text=s).pack()
            for p in services[s][b'ports'].keys():
                Tkinter.Label(disposableFrame, text=p).pack()
                for m in services[s][b'ports'][p][b'methods'].keys():
                    print(b'Creating button with parameters for createMessage: ', end=b'')
                    print(s, p, m)
                    Tkinter.Button(self.disposableFrame, text=m, command=self.mk_button_callback(s, p, m)).pack()

    def mk_button_callback(self, s, p, m):

        def createMessage():
            print(b'Requesting: ', end=b'')
            print(s, p, m)
            sig = self.soap_client.getMethodSignature(s, p, m)
            form = XMLFormWindow(self.XMLFormCallback, m)
            form.buildForm(sig)
            form.root.mainloop()

        return createMessage

    def XMLFormCallback(self, method, parameters):
        try:
            self.soap_client.sendCall(method, parameters)
        except Exception:
            logging.exception()

        self.re_left.write(str(self.soap_client.getXMLRequest()))
        self.re_right.write(str(self.soap_client.getXMLResponse()))


def main():
    MainWindow().run()


if __name__ == b'__main__':
    main()