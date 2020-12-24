# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_functions.py
# Compiled at: 2020-03-11 06:42:57
# Size of source mod 2**32: 1129 bytes
import tkinter as tk
from PIL import ImageTk, Image

def setbutton(parent, text, command, side=None, anchor=None, fill=None, bg=None, relief=None):
    btn = tk.Button(parent, text=text, command=command, anchor=anchor, bg=bg, relief=relief, bd=0)
    return btn


def save(subplot, save_file):
    fgr, axs = subplot
    fgr.savefig(save_file)
    axs.clear()


def display(panel, chart, name, i, subplot, action=None):
    fgr, axs = subplot
    f = panel.input.tempfile.TemporaryFile()
    fgr.savefig(f)
    plot_to_chart(f, chart)
    axs.clear()
    f.close()
    chart.name = name
    chart.i = i
    chart.bind('<Button-1>', action)


def plot_to_chart(chart_file, chart_label):
    if hasattr(chart_label, 'graph_file'):
        chart_label.graph_file.close()
    chart_label.graph_file = Image.open(chart_file)
    img = ImageTk.PhotoImage((chart_label.graph_file), master=chart_label)
    chart_label.configure(image=img)
    chart_label.graph_img = img


def fix_fname(s, i=None):
    if i is None:
        i = ''
    else:
        i = str(i)
    if '.' in s:
        l = len(s.split('.')[(-1)])
        s = s[:-l] + i + s[-l:]
    else:
        s = s + i + '.jpg'
    return s