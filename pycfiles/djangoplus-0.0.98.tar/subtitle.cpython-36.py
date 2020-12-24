# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/tools/subtitle.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 1534 bytes
import platform

class Subtitle(object):

    @staticmethod
    def display(message, duration=4):
        import tkinter as tk
        root = tk.Tk()
        root.overrideredirect(True)
        root.wm_attributes('-topmost', True)
        root.attributes('-alpha', 0.8)
        root.configure(background='black')
        lines = list()
        break_line = False
        for i, letter in enumerate(message):
            if break_line or i and i % 50 == 0:
                if letter == ' ':
                    lines.append('\n')
                    break_line = False
                else:
                    break_line = True
            lines.append(letter)

        message = ''.join(lines)
        line_breaks = message.count('\n')
        if 'darwin' in platform.system().lower():
            font_size, width, top, right = (
             30, 82, int(root.winfo_screenwidth() / 2 - 700),
             int(root.winfo_screenheight() - [90, 120, 156][line_breaks]))
        else:
            font_size, width, top, right = (
             20, 70, int(root.winfo_screenwidth() / 2 - 525.0),
             int(root.winfo_screenheight() - [77, 110, 140][line_breaks]))
        label = tk.Label(root, text=message, font=('Helvetica', font_size), width=width, height=(2 + line_breaks))
        label.configure(foreground='white', background='black')
        label.pack(expand=(tk.YES), fill=(tk.BOTH))
        root.geometry('+{}+{}'.format(top, right))
        root.after(1000 * duration, lambda : root.destroy())
        root.mainloop()