# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/plugins/fileview.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 16000 bytes
from noval import GetApp, _
import os, tkinter as tk
from tkinter.messagebox import showerror
import noval.iface as iface, noval.plugin as plugin, noval.consts as consts, noval.constants as constants
from noval.ttkwidgets.treeviewframe import TreeViewFrame
from tkinter import ttk
import noval.util.utils as utils, noval.util.fileutils as fileutils, noval.util.strutils as strutils, noval.syntax.syntax as syntax, noval.menu as tkmenu
try:
    import tkSimpleDialog
except ImportError:
    import tkinter.simpledialog as tkSimpleDialog

_dummy_node_text = '...'
if utils.is_windows():
    from win32com.shell import shell, shellcon

    def GetDriveDisplayName(path):
        return shell.SHGetFileInfo(path, 0, shellcon.SHGFI_DISPLAYNAME)[1][3]


    def GetRoots():
        roots = []
        import ctypes, os
        for i in range(65, 91):
            vol = chr(i) + ':'
            if os.path.isdir(vol):
                roots.append([GetDriveDisplayName(vol), vol])

        return roots


else:

    def GetRoots():
        roots = []
        home_dir = wx.GetHomeDir()
        roots.append([_('Home directory'), home_dir])
        desktop_dir = home_dir + '/Desktop'
        roots.append([_('Desktop'), desktop_dir])
        roots.append(['/', '/'])
        return roots


def get_win_drives():
    roots = []
    import ctypes, os
    for i in range(65, 91):
        vol = chr(i) + ':'
        if os.path.isdir(vol):
            roots.append(vol)

    return roots


SAVE_OPEN_FOLDER_KEY = 'FileViewSaveFolder'
OPEN_FOLDER_KEY = 'FileViewLastFolder'

class BaseFileBrowser(TreeViewFrame):

    def __init__(self, master, show_hidden_files=False):
        TreeViewFrame.__init__(self, master, ['#0', 'kind', 'path'], displaycolumns=(0, ))
        self.default_extentsion = '.' + syntax.SyntaxThemeManager().GetLexer(GetApp().GetDefaultLangId()).GetDefaultExt()
        self.show_hidden_files = show_hidden_files
        self.tree['show'] = ('tree', )
        wb = GetApp()
        self.folder_icon = wb.GetImage('files/folder.gif')
        self.python_file_icon = wb.GetImage('files/python-file.gif')
        self.text_file_icon = wb.GetImage('files/text-file.gif')
        self.generic_file_icon = wb.GetImage('files/generic-file.gif')
        self.hard_drive_icon = wb.GetImage('files/hard-drive.gif')
        self.tree.column('#0', width=500, anchor=tk.W)
        self.tree.set('', 'kind', 'root')
        self.tree.set('', 'path', '')
        self.refresh_tree()
        self.tree.bind('<<TreeviewOpen>>', self.on_open_node)
        self.open_initial_folder()

    def open_initial_folder(self):
        if utils.profile_get_int(SAVE_OPEN_FOLDER_KEY, True):
            path = utils.profile_get(OPEN_FOLDER_KEY)
            if path:
                self.open_path_in_browser(path, True)

    def save_current_folder(self):
        path = self.get_selected_path()
        if not path:
            return
        if os.path.isfile(path):
            path = os.path.dirname(path)
        utils.profile_set(OPEN_FOLDER_KEY, path)

    def on_open_node(self, event):
        node_id = self.get_selected_node()
        if node_id:
            self.refresh_tree(node_id, True)

    def get_selected_node(self):
        nodes = self.tree.selection()
        assert len(nodes) <= 1
        if len(nodes) == 1:
            return nodes[0]
        else:
            return

    def get_selected_path(self):
        node_id = self.get_selected_node()
        if node_id:
            return self.tree.set(node_id, 'path')
        else:
            return

    def open_path_in_browser(self, path, see=True):

        def split(path):
            head, tail = os.path.split(path)
            if head == '' and tail == '':
                return []
            else:
                if head == path or tail == path:
                    return [path]
                if head == '':
                    return [tail]
                if tail == '':
                    return split(head)
                return split(head) + [tail]

        parts = split(path)
        current_node_id = ''
        current_path = ''
        while parts != []:
            current_path = os.path.join(current_path, parts.pop(0))
            for child_id in self.tree.get_children(current_node_id):
                child_path = self.tree.set(child_id, 'path')
                if child_path == current_path:
                    self.tree.item(child_id, open=True)
                    self.refresh_tree(child_id)
                    current_node_id = child_id
                    break

        if see and current_node_id:
            self.tree.selection_set(current_node_id)
            self.tree.focus(current_node_id)
            if self.tree.set(current_node_id, 'kind') == 'file':
                self.tree.see(self.tree.parent(current_node_id))
        else:
            self.tree.see(current_node_id)

    def refresh_tree(self, node_id='', opening=None):
        path = self.tree.set(node_id, 'path')
        if os.path.isfile(path):
            self.tree.set_children(node_id)
            self.tree.item(node_id, open=False)
        else:
            if node_id == '' or self.tree.item(node_id, 'open') or opening == True:
                if path != '' and not path.endswith(os.sep):
                    path += os.sep
                fs_children_names = self.listdir(path, self.show_hidden_files)
                tree_children_ids = self.tree.get_children(node_id)
                children = {}
                for child_id in tree_children_ids:
                    name = self.tree.item(child_id, 'text')
                    if name in fs_children_names:
                        children[name] = child_id

                for name in fs_children_names:
                    if name not in children:
                        children[name] = self.tree.insert(node_id, 'end')
                        self.tree.set(children[name], 'path', os.path.join(path, name))

                def file_order(name):
                    return (
                     os.path.isfile(os.path.join(path, name)), name.upper())

                ids_sorted_by_name = list(map(lambda key: children[key], sorted(children.keys(), key=file_order)))
                self.tree.set_children(node_id, *ids_sorted_by_name)
                for child_id in ids_sorted_by_name:
                    self.update_node_format(child_id)
                    self.refresh_tree(child_id)

            else:
                children_ids = self.tree.get_children(node_id)
        if len(children_ids) == 0:
            self.tree.insert(node_id, 'end', text=_dummy_node_text)

    def update_node_format(self, node_id):
        assert node_id != ''
        path = self.tree.set(node_id, 'path')
        if os.path.isdir(path) or path.endswith(':') or path.endswith(':\\'):
            self.tree.set(node_id, 'kind', 'dir')
            if path.endswith(':') or path.endswith(':\\'):
                img = self.hard_drive_icon
            else:
                img = self.folder_icon
        else:
            self.tree.set(node_id, 'kind', 'file')
            if path.lower().endswith('.py'):
                img = self.python_file_icon
            else:
                if path.lower().endswith('.txt') or path.lower().endswith('.csv'):
                    img = self.text_file_icon
                else:
                    img = self.generic_file_icon
                text = os.path.basename(path)
                if text == '':
                    if utils.is_windows():
                        if utils.is_py2():
                            name = GetDriveDisplayName(path).decode(utils.get_default_encoding())
                        elif utils.is_py3_plus():
                            name = GetDriveDisplayName(path)
                        text = name
                    else:
                        text = path.strip(os.sep)
        self.tree.item(node_id, text=' ' + text, image=img)
        self.tree.set(node_id, 'path', path)

    def listdir(self, path='', include_hidden_files=False):
        key = str.upper
        if path == '' and utils.is_windows():
            drives = get_win_drives()
            result = [drive + '\\' for drive in drives]
        else:
            if path == '':
                first_level = True
                path = '/'
            else:
                first_level = False
            result = [x for x in self.ListDir(path) if include_hidden_files or not fileutils.is_file_path_hidden(os.path.join(path, x))]
        if first_level:
            result = ['/' + x for x in result]
        if utils.is_py2():
            key = unicode.upper
        return sorted(result, key=key)

    def ListDir(self, path):
        for x in os.listdir(path):
            if utils.is_py2():
                try:
                    yield x.decode(utils.get_default_encoding())
                except:
                    yield x.decode('utf-8')

            else:
                yield x


class MainFileBrowser(BaseFileBrowser):

    def __init__(self, master, show_hidden_files=False):
        BaseFileBrowser.__init__(self, master, show_hidden_files)
        self.menu = tkmenu.PopupMenu(tk._default_root)
        self.menu.Append(constants.ID_REFRESH_PATH, _('&Refresh'), handler=self.RefreshPath)
        self.menu.Append(constants.ID_OPEN_CMD_PATH, _('Open Command Prompt here...'), handler=self.OpenPathInterminal)
        self.menu.Append(constants.ID_COPY_FULLPATH, _('Open Path in Explorer'), handler=self.OpenPathInexplower)
        self.menu.Append(constants.ID_ADD_FOLDER, _('&Create new folder'), handler=self.create_new_folder)
        self.menu.Append(constants.ID_CREATE_NEW_FILE, _('&Create new file'), handler=self.create_new_file)
        self.tree.bind('<3>', self.on_secondary_click, True)
        self.tree.bind('<Double-Button-1>', self.on_double_click, '+')

    def RefreshPath(self, node_id=None):
        selected_path = self.get_selected_path()
        node_id = self.get_selected_node()
        if not os.path.exists(selected_path):
            node_id = self.tree.parent(node_id)
        for child_id in self.tree.get_children(node_id):
            self.tree.delete(child_id)

        try:
            self.refresh_tree(node_id, True)
        except Exception as e:
            showerror(_('Error'), e)

    def OpenPathInexplower(self):
        selected_path = self.get_selected_path()
        fileutils.safe_open_file_directory(selected_path)

    def OpenPathInterminal(self):
        selected_path = self.get_selected_path()
        if os.path.isfile(selected_path):
            selected_path = os.path.dirname(selected_path)
        try:
            fileutils.open_path_in_terminator(selected_path)
        except RuntimeError as e:
            showerror(_('Error'), e)

    def create_new_file(self):
        selected_path = self.get_selected_path()
        if not selected_path:
            return
        if os.path.isdir(selected_path):
            parent_path = selected_path
        else:
            parent_path = os.path.dirname(selected_path)
        initial_name = self.get_proposed_new_file_name(parent_path, self.default_extentsion)
        name = tkSimpleDialog.askstring('File name', 'Provide filename', initialvalue=initial_name)
        if not name:
            return
        path = os.path.join(parent_path, name)
        if os.path.exists(path):
            showerror('Error', "The file '" + path + "' already exists", parent=GetApp())
            return
        open(path, 'w').close()
        self.open_path_in_browser(path, True)
        GetApp().GotoView(path)

    def create_new_folder(self):
        selected_path = self.get_selected_path()
        if not selected_path:
            return
        if os.path.isdir(selected_path):
            parent_path = selected_path
        else:
            parent_path = os.path.dirname(selected_path)
        initial_name = self.get_proposed_new_file_name(parent_path, '', 'newfoler')
        name = tkSimpleDialog.askstring(_('New folder'), 'Provide folder name', initialvalue=initial_name)
        if not name:
            return
        path = os.path.join(parent_path, name)
        try:
            os.mkdir(path)
        except Exception as e:
            showerror(_('Error'), str(e))
            return

        self.open_path_in_browser(path, True)

    def get_proposed_new_file_name(self, folder, extension, base='new_file'):
        if os.path.exists(os.path.join(folder, base + extension)):
            i = 2
            while True:
                name = base + '_' + str(i) + extension
                path = os.path.join(folder, name)
                if os.path.exists(path):
                    i += 1
                else:
                    return name

        else:
            return base + extension

    def on_secondary_click(self, event):
        node_id = self.tree.identify_row(event.y)
        if node_id:
            self.tree.selection_set(node_id)
            self.tree.focus(node_id)
            self.menu.tk_popup(event.x_root, event.y_root)

    def on_double_click(self, event):
        path = self.get_selected_path()
        if os.path.isfile(path):
            ext = strutils.get_file_extension(path)
            if utils.is_ext_supportable(ext):
                if utils.is_windows():
                    GetApp().GotoView(path, 0)
                else:
                    GetApp().GotoView(path, 0)
            else:
                try:
                    fileutils.start_file(path)
                except:
                    pass

            self.save_current_folder()
        elif os.path.isdir(path):
            self.refresh_tree(self.get_selected_node(), True)


class FileViewLoader(plugin.Plugin):
    plugin.Implements(iface.CommonPluginI)

    def Load(self):
        GetApp().MainFrame.AddView(consts.FILE_VIEW_NAME, MainFileBrowser, _('File View'), 'nw', default_position_key='B')