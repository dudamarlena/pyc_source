# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b:\forskning\papers\paneltime\paneltime\paneltime\gui\gui_script_handling.py
# Compiled at: 2020-02-21 07:39:57
# Size of source mod 2**32: 1939 bytes
import tkinter as tk, re

def edit_exe_script(window, dataset):
    if dataset is None:
        return
    else:
        editor = dataset.get_exe_editor(window.main_tabs, False)
        script = editor.widget.get('1.0', tk.END)
        exe_script = dataset.generate_exe_script(window.right_tabs.data_tree)
        m = re.search('execute\\(([\\s\\S]*?)\\)', script)
        if m is None:
            script = script + '\n\n' + exe_script
        else:
            script = script[:m.start()] + exe_script + script[m.end():]
    imprt = 'from paneltime import *'
    if imprt not in ' '.join(script.split()):
        script = imprt + '\n' + script
    editor.widget.replace_all(script)
    window.data.save()
    return script


def edit_options_script(options):
    editor = options.dataset.get_exe_editor(options.win.main_tabs, False).widget
    script = editor.get('1.0', tk.END)
    optns, search_patterns = options.get_script()
    m = re.search('execute\\(([\\s\\S]*?)\\)', script)
    if m is None:
        script = edit_exe_script(options.win, options.dataset)
    end = re.search('execute\\(([\\s\\S]*?)\\)', script).start()
    if script[end - 2:end] != '\n\n':
        script = script[:end] + '\n\n' + script[end:]
    for i in range(len(optns)):
        m = re.search(search_patterns[i], script[:end])
        if m is None:
            script = script[:end - 2] + '\n' + optns[i] + script[end - 2:]
        else:
            script = script[:m.start()] + optns[i] + script[m.end():]

    editor.replace_all(script)
    options.win.data.save()


def get_start_end(lines, identstr1, identstr2):
    start = -1
    end = -1
    for i in range(len(lines)):
        if lines[i] == identstr1[:-1]:
            if start == -1:
                start = i
        if lines[i] == identstr2[:-1] and start > -1:
            end = i
            break

    return (
     start, end)


def nicify(string):
    repl_list = [
     [
      '\n\n\n', '\n\n'], ['\n\r\n', '\n\n'], ['\n\n\r', '\n\n'], ['\r\n\n', '\n\n'], ['  ', ' ']]
    for s, r in repl_list:
        while True:
            if s in string:
                string = string.replace(s, r)
            else:
                break

    return string