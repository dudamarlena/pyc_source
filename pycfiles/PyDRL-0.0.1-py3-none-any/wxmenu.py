# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\traits102\wxmenu.py
# Compiled at: 2014-04-16 13:17:36
from __future__ import division
import wxPython.wx as wx, re, string
from types import StringType
TRUE = 1
FALSE = 0
DEBUG = TRUE
help_pat = re.compile('(.*){(.*)}(.*)')
options_pat = re.compile('(.*)\\[(.*)\\](.*)')
key_map = {'F1': wx.WXK_F1, 
   'F2': wx.WXK_F2, 
   'F3': wx.WXK_F3, 
   'F4': wx.WXK_F4, 
   'F5': wx.WXK_F5, 
   'F6': wx.WXK_F6, 
   'F7': wx.WXK_F7, 
   'F8': wx.WXK_F8, 
   'F9': wx.WXK_F9, 
   'F10': wx.WXK_F10, 
   'F11': wx.WXK_F11, 
   'F12': wx.WXK_F12}

class MakeMenu:
    cur_id = 1000

    def __init__(self, desc, owner, popup=FALSE, window=None):
        self.owner = owner
        if window is None:
            window = owner
        self.window = window
        self.indirect = getattr(owner, 'call_menu', None)
        self.names = {}
        self.desc = desc.split('\n')
        self.index = 0
        self.keys = []
        if popup:
            self.menu = menu = wx.wxMenu()
            self.parse(menu, -1)
        else:
            self.menu = menu = wx.wxMenuBar()
            self.parse(menu, -1)
            window.SetMenuBar(menu)
            if len(self.keys) > 0:
                window.SetAcceleratorTable(wx.wxAcceleratorTable(self.keys))
        return

    def parse(self, menu, indent):
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
                menu.AppendSeparator()
                continue
            MakeMenu.cur_id += 1
            cur_id = MakeMenu.cur_id
            help = ''
            match = help_pat.search(line)
            if match:
                help = ' ' + match.group(2).strip()
                line = match.group(1) + match.group(3)
            col = line.find(':')
            if col >= 0:
                handler = line[col + 1:].strip()
                if handler != '':
                    if self.indirect:
                        self.indirect(cur_id, handler)
                        handler = self.indirect
                    else:
                        try:
                            exec 'def handler(event,self=self.owner):\n %s\n' % handler
                        except:
                            handler = null_handler

                else:
                    try:
                        exec 'def handler(event,self=self.owner):\n%s\n' % (
                         self.get_body(indented),) in globals()
                    except:
                        handler = null_handler

                wx.EVT_MENU(self.window, cur_id, handler)
                not_checked = checked = disabled = FALSE
                line = line[:col]
                match = options_pat.search(line)
                if match:
                    line = match.group(1) + match.group(3)
                    not_checked, checked, disabled, name = option_check('~/-', match.group(2).strip())
                    if name != '':
                        self.names[name] = cur_id
                        setattr(self.owner, name, MakeMenuItem(self, cur_id))
                label = line.strip()
                col = label.find('|')
                if col >= 0:
                    key = label[col + 1:].strip()
                    label = '%s%s%s' % (label[:col].strip(), '\t', key)
                    key = key.upper()
                    flag = wx.wxACCEL_NORMAL
                    col = key.find('-')
                    if col >= 0:
                        flag = {'CTRL': wx.wxACCEL_CTRL, 'SHIFT': wx.wxACCEL_SHIFT, 'ALT': wx.wxACCEL_ALT}.get(key[:col].strip(), wx.wxACCEL_CTRL)
                        key = key[col + 1:].strip()
                    code = key_map.get(key, None)
                    if code is None:
                        code = ord(key)
                    self.keys.append(wx.wxAcceleratorEntry(flag, code, cur_id))
                menu.Append(cur_id, label, help, not_checked or checked)
                if checked:
                    menu.Check(cur_id, TRUE)
                if disabled:
                    menu.Enable(cur_id, FALSE)
                continue
            submenu = wx.wxMenu()
            label = line.strip()
            self.parse(submenu, indented)
            try:
                menu.AppendMenu(cur_id, label, submenu, help)
            except:
                menu.Append(submenu, label)

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

    def get_id(self, name):
        if type(name) is StringType:
            return self.names[name]
        return name

    def checked(self, name, check=None):
        if check is None:
            return self.menu.IsChecked(self.get_id(name))
        else:
            self.menu.Check(self.get_id(name), check)
            return

    def enabled(self, name, enable=None):
        if enable is None:
            return self.menu.IsEnabled(self.get_id(name))
        else:
            self.menu.Enable(self.get_id(name), enable)
            return

    def label(self, name, label=None):
        if label is None:
            return self.menu.GetLabel(self.get_id(name))
        else:
            self.menu.SetLabel(self.get_id(name), label)
            return


class MakeMenuItem:

    def __init__(self, menu, id):
        self.menu = menu
        self.id = id

    def checked(self, check=None):
        return self.menu.checked(self.id, check)

    def toggle(self):
        checked = not self.checked()
        self.checked(checked)
        return checked

    def enabled(self, enable=None):
        return self.menu.enabled(self.id, enable)

    def label(self, label=None):
        return self.menu.label(self.id, label)


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