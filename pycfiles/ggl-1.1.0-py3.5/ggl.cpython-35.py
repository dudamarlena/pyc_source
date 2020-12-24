# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ggl/ggl.py
# Compiled at: 2016-11-12 21:02:31
# Size of source mod 2**32: 495 bytes
import sys, tkinter, urllib.parse, webbrowser

def get_clipboard_text():
    tk = tkinter.Tk()
    tk.withdraw()
    return tk.clipboard_get()


def search_by_google(text):
    url = 'http://www.google.com/#q=' + urllib.parse.quote(text)
    webbrowser.open_new_tab(url)


def main():
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = get_clipboard_text()
    search_by_google(text)