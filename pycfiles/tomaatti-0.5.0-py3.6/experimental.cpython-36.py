# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/internal/experimental.py
# Compiled at: 2018-06-19 09:05:36
# Size of source mod 2**32: 2236 bytes


class ScreenOverlay(object):

    @staticmethod
    def is_coposite_manager_running():
        from subprocess import Popen, PIPE
        child = Popen(['pgrep', 'xcompmgr'], stdout=PIPE)
        child.communicate()
        if 0 == child.returncode:
            return True
        else:
            return False

    def __init__(self):
        self._tkinter_root = None
        self._overlay_canvas = None

    def show_overlay(self, text_to_show):
        from tkinter import Canvas, Tk
        self._tkinter_root = Tk()
        self._screen_width = self._tkinter_root.winfo_screenwidth()
        self._screen_height = self._tkinter_root.winfo_screenheight()
        self._overlay_canvas = Canvas(width=(self._screen_width), height=(self._screen_height), highlightthickness=0)
        self._overlay_canvas.configure(background='black')
        self._overlay_canvas.master.overrideredirect(True)
        self._overlay_canvas.master.geometry('+0+0')
        self._overlay_canvas.master.lift()
        self._overlay_canvas.master.wm_attributes('-topmost', True)
        self._overlay_canvas.master.wm_attributes('-fullscreen', True)
        self._overlay_canvas.master.wm_attributes('-zoomed', False)
        self._overlay_canvas.master.wm_attributes('-alpha', 0.7)
        self._overlay_canvas.create_rectangle(0, 0, (self._screen_width), (self._screen_height), fill='black')
        self._overlay_canvas.bind('<Button-1>', self._close_callback)
        self._overlay_canvas.pack()
        self._text = self._overlay_canvas.create_text(0, 0, fill='white', font='Roboto 30 bold', text=text_to_show)
        self._overlay_canvas.move(self._text, self._screen_width / 2, self._screen_height / 2)
        self._overlay_canvas.mainloop()

    def _close_callback(self, event):
        self._tkinter_root.destroy()