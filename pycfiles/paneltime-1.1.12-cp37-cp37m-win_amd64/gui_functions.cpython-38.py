# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \\ad.uit.no\uit\data\esi000data\dokumenter\forskning\papers\paneltime\paneltime\paneltime\gui\gui_functions.py
# Compiled at: 2020-01-08 06:45:13
# Size of source mod 2**32: 1074 bytes
import tkinter as tk
from PIL import ImageTk, Image

def setbutton(parent, text, command, side=None, anchor=None, fill=None, bg=None):
    btn = tk.Button(parent, text=text, command=command, anchor=anchor, bg=bg)
    return btn


def save(subplot, save_file):
    fgr, axs = subplot
    fgr.savefig(save_file)
    axs.clear()


def display(panel, chart, name, i, subplot, action):
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
    img = ImageTk.PhotoImage(chart_label.graph_file)
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