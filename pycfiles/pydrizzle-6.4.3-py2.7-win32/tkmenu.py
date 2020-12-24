# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\tkmenu.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import Tkinter as tk, re, string
from types import StringType
TRUE = 1
FALSE = 0
DEBUG = TRUE
help_pat = re.compile('(.*){(.*)}(.*)')
options_pat = re.compile('(.*)\\[(.*)\\](.*)')

class MakeMenu:

    def __init__(self, desc, owner, popup=FALSE, window=None):
        self.owner = owner
        if window is None:
            window = owner
        self.window = window
        self.desc = desc.split('\n')
        self.index = 0
        self.menus = []
        if popup:
            self.menu = menu = tk.Menu(window, tearoff=FALSE)
            self.parse(menu, -1)
        else:
            self.menubar = tk.Frame(window, relief=tk.RAISED, borderwidth=1)
            self.parse(None, -1)
            self.menubar.tk_menuBar(*self.menus)
        return

    def parse(self, menu, indent):
        cur_id = 0
        while TRUE:
            if self.index >= len(self.desc):
                return
            dline = self.desc[self.index]
            line = dline.lstrip()
            indented = len(dline) - len(line)
            if indented <= indent:
                return
            self.index += 1
            if line == '' or line[0:1] == '#':
                continue
            if line[0:1] == '-':
                menu.add_separator()
                cur_id += 1
                continue
            help = ''
            match = help_pat.search(line)
            if match:
                help = ' ' + match.group(2).strip()
                line = match.group(1) + match.group(3)
            col = line.find(':')
            if col >= 0:
                handler = line[col + 1:].strip()
                if handler != '':
                    try:
                        exec 'def handler(event=None,self=self.owner):\n %s\n' % handler
                    except:
                        handler = null_handler

                else:
                    try:
                        exec 'def handler(event=None,self=self.owner):\n%s\n' % (
                         self.get_body(indented),) in globals()
                    except:
                        handler = null_handler

                not_checked = checked = disabled = FALSE
                line = line[:col]
                match = options_pat.search(line)
                if match:
                    line = match.group(1) + match.group(3)
                    not_checked, checked, disabled, name = option_check('~/-', match.group(2).strip())
                    check_var = None
                    if not_checked or checked:
                        check_var = tk.IntVar()
                        check_var.set(checked)
                    if name != '':
                        setattr(self.owner, name, MakeMenuItem(menu, cur_id, check_var))
                label = line.strip().replace('&', '')
                col = label.find('|')
                if col >= 0:
                    key_name = label[col + 1:].strip()
                    label = label[:col].strip()
                    self.window.bind(self.binding_for(key_name), handler)
                if checked or not_checked:
                    menu.add_checkbutton(label=label, command=handler, variable=check_var)
                else:
                    menu.add_command(label=label, command=handler)
                if col >= 0:
                    menu.entryconfig(cur_id, accelerator=key_name)
                if disabled:
                    menu.entryconfig(cur_id, state=tk.DISABLED)
                cur_id += 1
                continue
            label = line.strip().replace('&', '')
            if menu is None:
                menubar = tk.Menubutton(self.menubar, text=label)
                self.menus.append(menubar)
                menubar.pack(side=tk.LEFT)
                menubar['menu'] = submenu = tk.Menu(menubar, tearoff=FALSE)
            else:
                submenu = tk.Menu(menu, tearoff=FALSE)
                menu.add_cascade(label=label, menu=submenu)
            self.parse(submenu, indented)
            cur_id += 1

        return

    def get_body(self, indent):
        result = []
        while self.index < len(self.desc):
            line = self.desc[self.index]
            if len(line) - len(line.lstrip()) <= indent:
                break
            result.append(line)
            self.index += 1

        result = string.join(result, '\n').rstrip()
        if result != '':
            return result
        return '  pass'

    def binding_for(self, key_name):
        key_name = key_name.replace('Ctrl-', 'Control-')
        if key_name[-2:-1] == '-':
            key_name = key_name[:-1] + key_name[(-1)].lower()
        return '<%s>' % key_name


class MakeMenuItem:

    def __init__(self, menu, id, var):
        self.menu = menu
        self.id = id
        self.var = var

    def checked(self, check=None):
        if check is not None:
            self.var.set(check)
            return check
        else:
            return self.var.get()

    def toggle(self):
        checked = not self.checked()
        self.checked(checked)
        return checked

    def enabled(self, enable=None):
        if enable is not None:
            self.menu.entryconfig(self.id, state=(
             tk.DISABLED, tk.NORMAL)[enable])
            return enable
        else:
            return self.menu.entrycget(self.id, 'state') == tk.NORMAL

    def label(self, label=None):
        if label is not None:
            self.menu.entryconfig(self.id, label=label)
            return label
        else:
            return self.menu.entrycget(self.id, 'label')


def option_check(test, string):
    result = []
    for char in test:
        col = string.find(char)
        result.append(col >= 0)
        if col >= 0:
            string = string[:col] + string[col + 1:]

    return result + [string.strip()]


def null_handler(event):
    print 'null_handler invoked'