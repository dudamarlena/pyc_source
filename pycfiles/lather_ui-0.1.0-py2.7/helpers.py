# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lather_ui\helpers.py
# Compiled at: 2017-05-23 11:50:05
try:
    import Tkinter, tkFileDialog, tkMessageBox, Tkconstants, ScrolledText
except ImportError:
    import tkinter as Tkinter
    from tkinter import filedialog as tkFileDialog, messagebox as tkMessageBox, constants as Tkconstants, scrolledtext as ScrolledText

import subprocess, shlex, sys, os
from lxml import etree
from threading import Thread
from time import sleep

def getFilename():
    """this will get a filename using Tkinter browse dialog
    """
    file_opt = options = {}
    options['filetypes'] = [
     ('shell script', '.sh'), ('all files', '.*')]
    options['initialdir'] = os.getcwd()
    frame = Tkinter.Frame()
    options['parent'] = frame
    options['title'] = 'select a shell script source file: '
    filepath = tkFileDialog.askopenfilename(**file_opt)
    frame.destroy()
    return filepath


def writeFile(filename, content, content_header=''):
    """this writes some given content to a given filename in binary append mode
    """
    outFile = open(filename, 'ab')
    outFile.write(content_header + '\n')
    outFile.write(content + '\n')
    outFile.close()


def get_file_options():
    options = {}
    options['filetypes'] = [
     ('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = os.getcwd()
    options['parent'] = self.root
    options['title'] = 'select a jmx file: '


class RedirectText(object):
    """Helper class to redirect STD Out to a particular UI element"""

    def __init__(self, text_ctrl):
        """Constructor"""
        self.output = text_ctrl
        self.fileno = sys.stdout.fileno

    def write(self, string):
        """ write to the redirected terminal"""
        self.output.insert(Tkinter.INSERT, string + '\n')


class AbstractWindow(Tkinter.Frame):

    def userAlert(self, message):
        tkMessageBox.showinfo('Alert:', message)

    def restart(self):
        subprocess.Popen('python App.py', shell=True)
        self.root.quit()

    def hello(self):
        tkMessageBox.showinfo('INFO:', 'This feature is not implemented yet')