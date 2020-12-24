# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/project/basebrowser.py
# Compiled at: 2019-10-07 21:21:23
# Size of source mod 2**32: 37566 bytes
from noval import GetApp, _, core, constants
import os, tkinter as tk
from tkinter import messagebox, filedialog
import noval.consts as consts
from tkinter import ttk
import noval.util.utils as utils, noval.util.fileutils as fileutils, noval.util.strutils as strutils, noval.project.baseviewer as baseviewer, noval.imageutils as imageutils, noval.menu as tkmenu, noval.misc as misc, threading
from noval.project.command import ProjectAddProgressFilesCommand
from noval.python.parser.utils import py_cmp, py_sorted
import noval.terminal as terminal, noval.project.property as projectproperty, time, noval.project.document as projectdocument

class EntryPopup(tk.Entry):

    def __init__(self, parent, text, item, **kw):
        """ If relwidth is set, then width is ignored """
        tk.Entry.__init__(self, parent, **kw)
        self.item = item
        self.insert(0, text)
        self['readonlybackground'] = 'white'
        self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False
        self.focus_force()
        self.bind('<Control-a>', self.selectAll)
        self.bind('<Escape>', lambda *ignore: self.destroy())
        self.bind('<Return>', self.master.FinishLabel)
        self.selectAll()

    def selectAll(self, *ignore):
        """ Set selection on the whole text """
        self.selection_range(0, 'end')
        return 'break'


class ProjectTreeCtrl(ttk.Treeview):
    BOLD_TAG = 'BoldItem'
    NORMAL_TAG = 'NormalItem'

    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        self._iconLookup = {}
        self._blankIconImage = imageutils.getBlankIcon()
        self._packageFolderImage = imageutils.getPackageFolderIcon()
        self._folderClosedImage = imageutils.getFolderClosedIcon()
        self.is_edit_state = False
        self.entryPopup = None
        self.bind('<Escape>', self.EndLabel)
        self.bind('<<TreeviewSelect>>', self.OnItemSelect)
        self.bind('<Button-1>', self.FinishLabel)

    def SelectItem(self, node):
        self.selection_set(node)
        self.focus(node)

    def BuildLookupIcon(self):
        if 0 == len(self._iconLookup):
            templates = GetApp().GetDocumentManager().GetTemplates()
            for template in templates:
                icon = template.GetIcon()
                self._iconLookup[template] = icon

    def SetItemBold(self, node, bold=True):
        if bold:
            self.item(node, tags=self.BOLD_TAG)
            self.tag_configure(self.BOLD_TAG, font=consts.TREE_VIEW_BOLD_FONT)
        else:
            self.item(node, tags=self.NORMAL_TAG)
            self.tag_configure(self.NORMAL_TAG, font=consts.TREE_VIEW_FONT)

    def GetPyData(self, node):
        if node is None:
            return
        values = self.item(node)['values']
        if type(values) == str:
            return
        return values[0]

    def SortChildren(self, node):
        children = self.get_children(node)
        ids_sorted_by_name = py_sorted(children, cmp_func=self.OnCompareItems)
        self.set_children(node, *ids_sorted_by_name)

    def GetChildrenCount(self, item):
        return len(self.get_children(item))

    def DeleteChildren(self, node):
        for child_id in self.get_children(node):
            self.delete(child_id)

    def GetRootItem(self):
        return self.GetFirstChild(None)

    def GetFirstChild(self, item):
        childs = self.get_children(item)
        if 0 == len(childs):
            return
        return childs[0]

    def OnItemSelect(self, event):
        self.FinishLabel(event)

    def EndLabel(self, event):
        if not self.is_edit_state or self.entryPopup is None:
            return
        self.entryPopup.destroy()
        self.entryPopup = None
        self.is_edit_state = False

    def FinishLabel(self, event):
        if not self.is_edit_state or self.entryPopup is None:
            return
        self.master.GetView().OnEndLabelEdit(self.entryPopup.item, self.entryPopup.get())
        self.EndLabel(event)

    def EditLabel(self, item):
        self.is_edit_state = True
        x, y, width, height = self.bbox(item)
        pady = height // 2
        text = self.item(item, 'text')
        self.entryPopup = EntryPopup(self, text, item)
        self.entryPopup.place(x=30, y=y + pady, anchor=tk.W, relwidth=1)

    def OnCompareItems(self, item1, item2):
        item1IsFolder = self.GetPyData(item1) == None
        item2IsFolder = self.GetPyData(item2) == None
        if item1IsFolder == item2IsFolder:
            return py_cmp(self.item(item1, 'text').lower(), self.item(item2, 'text').lower())
        if item1IsFolder and not item2IsFolder:
            return -1
        if not item1IsFolder and item2IsFolder:
            return 1

    def AppendFolder(self, parent, folderName):
        item = self.insert(parent, 'end', text=folderName, image=self._folderClosedImage)
        return item

    def GetIconFromName(self, filename):
        template = wx.GetApp().GetDocumentManager().FindTemplateForPath(filename)
        return self.GetTemplateIcon(template)

    def GetProjectIcon(self):
        template = GetApp().GetDocumentManager().FindTemplateForTestPath(consts.PROJECT_EXTENSION)
        project_file_image = self.GetTemplateIcon(template)
        return project_file_image

    def GetTemplateIcon(self, template):
        self.BuildLookupIcon()
        if template in self._iconLookup:
            return self._iconLookup[template]
        return self._blankIconImage

    def AppendItem(self, parent, filename, file):
        if filename == consts.DUMMY_NODE_TEXT:
            return
        template = GetApp().MainFrame.GetView(consts.PROJECT_VIEW_NAME).GetView().GetOpenDocumentTemplate(file)
        found = False
        if template is None:
            template = GetApp().GetDocumentManager().FindTemplateForPath(filename)
        file_image = self.GetTemplateIcon(template)
        item = self.insert(parent, 'end', text=filename, image=file_image, values=(file.filePath,))
        return item

    def AddFolder(self, folderPath):
        folderItems = []
        if folderPath != None:
            folderTree = folderPath.split('/')
            item = self.GetRootItem()
            for folderName in folderTree:
                found = False
                for child in self.get_children(item):
                    file = self.GetPyData(child)
                    if file:
                        pass
                    elif self.item(child, 'text') == folderName:
                        item = child
                        found = True
                        break

                if not found:
                    item = self.AppendFolder(item, folderName)
                    folderItems.append(item)

        return folderItems

    def FindItem(self, filePath, parentItem=None):
        if not parentItem:
            parentItem = self.GetRootItem()
        for child in self.get_children(parentItem):
            child_file_path = self.GetPyData(child)
            if child_file_path:
                if child_file_path == filePath:
                    return child
            else:
                result = self.FindItem(filePath, child)
                if result:
                    return result

    def FindFolder(self, folderPath):
        if folderPath != None:
            folderTree = folderPath.split('/')
            item = self.GetRootItem()
            for folderName in folderTree:
                found = False
                for child in self.get_children(item):
                    file = self.GetPyData(child)
                    if file:
                        pass
                    elif self.item(child, 'text') == folderName:
                        item = child
                        found = True
                        break

            if found:
                pass
            return item

    def FindClosestFolder(self, x, y):
        item, flags = self.HitTest((x, y))
        if item:
            file = self.GetPyData(item)
            if file:
                item = self.GetItemParent(item)
                return item
            return item

    def GetSingleSelectItem(self):
        items = self.selection()
        if not items:
            return
        return items[0]


class BaseProjectbrowser(ttk.Frame):

    def __init__(self, master, columns=[
 '#0', 'kind', 'path'], displaycolumns='#all', show_scrollbar=True, borderwidth=0, relief='flat', **tree_kw):
        ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief)
        self._mapToProject = dict()
        GetApp().bind('ShowView', self.Show, True)
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style=None)
        if show_scrollbar:
            self.vert_scrollbar.grid(row=1, column=1, sticky=tk.NSEW)
        self.project_combox = ttk.Combobox(self)
        self.project_combox.bind('<<ComboboxSelected>>', self.ProjectSelect)
        self.project_combox.grid(row=0, column=0, sticky=tk.NSEW)
        self.project_combox.state(['readonly'])
        self.tree = self.GetProjectTreectrl(**tree_kw)
        self.tree.column('#0', anchor=tk.W, stretch=True)
        self.tree['show'] = ('tree', )
        self.tree.grid(row=1, column=0, sticky=tk.NSEW)
        self.vert_scrollbar['command'] = self.tree.yview
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.tree.bind('<Double-Button-1>', self.on_double_click, '+')
        self.tree.bind('<Return>', self.OnEnter)
        self.tree.bind('<<TreeviewOpen>>', self.OpenTreeItem)
        self._is_loading = False
        view = self.CreateView()
        self.SetView(view)
        self.GetView().AddProjectRoot(_('Projects'))
        GetApp().bind('InitTkDnd', self.SetDropTarget, True)
        self.tree.bind('<3>', self.on_secondary_click, True)
        self.tree.bind('<<TreeviewSelect>>', self._on_select, True)

    def SetDropTarget(self, event):
        if GetApp().dnd is not None and utils.profile_get_int('ALLOW_DROP_OPENFILE', True):
            GetApp().dnd.bindtarget(self, baseviewer.ProjectFileDropTarget(self.GetView()), 'text/uri-list')

    def GetProjectTreectrl(self, **tree_kw):
        return ProjectTreeCtrl(self, yscrollcommand=self.vert_scrollbar.set, **tree_kw)

    def _on_select(self, event):
        GetApp().GetDocumentManager().ActivateView(self.GetView())

    def _clear_tree(self):
        for child_id in self.tree.get_children():
            self.tree.delete(child_id)

    def clear(self):
        self._clear_tree()

    def GetItemFile(self, item):
        file_path = self.GetView()._GetItemFilePath(item)
        if not file_path:
            return
        return self.GetView().GetDocument().GetModel().FindFile(file_path)

    def OnEnter(self, event):
        if self.tree.is_edit_state:
            self.tree.FinishLabel(event)
            return
        self.OpenSelection()

    def on_double_click(self, event):
        self.OpenSelection()

    def OpenSelection(self):
        selections = self.tree.selection()
        if not selections:
            return
        doc = None
        try:
            item = selections[0]
            filepath = self.GetView()._GetItemFilePath(item)
            file_template = None
            if filepath:
                filepath = fileutils.opj(filepath)
                if not os.path.exists(filepath):
                    msgTitle = GetApp().GetAppName()
                    if not msgTitle:
                        msgTitle = _('File Not Found')
                    ret = messagebox.askyesno(msgTitle, _("The file '%s' was not found in '%s'.\n\nWould you like to browse for the file?") % (
                     fileutils.get_filename_from_path(filepath), fileutils.get_filepath_from_path(filepath)), parent=self)
                    if not ret:
                        return
                    newpath = filedialog.askopenfilename(master=self, initialdir=os.getcwd(), title=_('Choose a file'), initialfile=fileutils.get_filename_from_path(filepath))
                    if newpath:
                        self.GetView().GetDocument().UpdateFilePath(filepath, newpath)
                        filepath = newpath
                    else:
                        return
                else:
                    project_file = self.GetItemFile(item)
                    file_template = self.GetView().GetOpenDocumentTemplate(project_file)
                if file_template:
                    doc = GetApp().GetDocumentManager().CreateTemplateDocument(file_template, filepath, wx.lib.docview.DOC_SILENT | wx.lib.docview.DOC_OPEN_ONCE)
                else:
                    docs = GetApp().GetDocumentManager().CreateDocument(filepath, core.DOC_SILENT | core.DOC_OPEN_ONCE)
                if not docs and filepath.endswith(consts.PROJECT_EXTENSION):
                    self.SetProject(filepath)
            elif docs:
                baseviewer.AddProjectMapping(docs[0])
        except IOError as e:
            msgTitle = wx.GetApp().GetAppName()
            if not msgTitle:
                msgTitle = _('File Error')
            wx.MessageBox("Could not open '%s'." % wx.lib.docview.FileNameFromPath(filepath), msgTitle, wx.OK | wx.ICON_EXCLAMATION, self.GetFrame())

    def GetView(self):
        return self._view

    def CreateView(self):
        return baseviewer.ProjectView(self)

    def SetView(self, view):
        self._view = view

    def AddProject(self, name):
        if type(self.project_combox['values']) == str:
            self.project_combox['values'] = [
             name]
            return 0
        else:
            self.project_combox['values'] = self.project_combox['values'] + (name,)
            return len(self.project_combox['values']) - 1

    def LoadSavedProjects(self):
        self._is_loading = True
        openedDocs = False
        if utils.profile_get_int(consts.PROJECT_DOCS_SAVED_KEY, True):
            docList = utils.profile_get(consts.PROJECT_SAVE_DOCS_KEY, [])
            doc = None
            for fileName in docList:
                if isinstance(fileName, str) and strutils.get_file_extension(fileName) == consts.PROJECT_SHORT_EXTENSION:
                    if utils.is_py2():
                        fileName = fileName.decode('utf-8')
                    if os.path.exists(fileName):
                        doc = GetApp().GetDocumentManager().CreateDocument(fileName, core.DOC_SILENT | core.DOC_OPEN_ONCE)
                    if doc:
                        openedDocs = True

        self._is_loading = False
        return openedDocs

    def SetCurrentProject(self):
        open_project_path = GetApp().OpenProjectPath
        if open_project_path is not None:
            self.GetView().SetProject(open_project_path)
        else:
            currProject = utils.profile_get(consts.CURRENT_PROJECT_KEY)
            docList = [document.GetFilename() for document in self.GetView().Documents]
        if currProject in docList:
            self.GetView().SetProject(currProject)

    @property
    def IsLoading(self):
        return self._is_loading

    def SetFocus(self):
        self.focus_set()
        self.tree.focus_set()

    def ProjectSelect(self, event):
        self.GetView().ProjectSelect()

    def Show(self, event):
        if event.get('view_name') != consts.PROJECT_VIEW_NAME:
            utils.get_logger().info('project view could not handler view %s showview event', event.get('view_name'))
            return
        project = self.GetView().GetDocument()
        if not project:
            self.LoadSavedProjects()

    def OpenTreeItem(self, event):
        if self.GetView().GetDocument() == None:
            return
        self.GetView().SaveFolderState()

    def FindProjectFromMapping(self, key):
        """ 从对照表中快速查找文档对应的项目"""
        return self._mapToProject.get(key, None)

    def AddProjectMapping(self, key, projectDoc=None):
        """ 设置文档或者其他对象对应的项目
        """
        if not projectDoc:
            projectDoc = self.GetCurrentProject()
        self._mapToProject[key] = projectDoc

    def RemoveProjectMapping(self, key):
        """ Remove mapping from model or document to project.  """
        if key in self._mapToProject:
            del self._mapToProject[key]

    def GetCurrentProject(self):
        view = self.GetView()
        if view:
            return view.GetDocument()

    def FindProjectByFile(self, filename):
        """查找包含文件的所有项目文档,当前项目文档放在第一位"""
        retval = []
        for document in GetApp().GetDocumentManager().GetDocuments():
            if document.GetDocumentTemplate().GetDocumentType() == projectdocument.ProjectDocument:
                if document.GetFilename() == filename:
                    retval.append(document)
                elif document.IsFileInProject(filename):
                    retval.append(document)

        currProject = self.GetCurrentProject()
        if currProject and currProject in retval:
            retval.remove(currProject)
            retval.insert(0, currProject)
        return retval

    def _InitCommands(self):
        GetApp().AddCommand(constants.ID_NEW_PROJECT, _('&Project'), _('New Project'), self.NewProject, image='project/new.png')
        GetApp().AddCommand(constants.ID_OPEN_PROJECT, _('&Project'), _('Open Project'), self.OpenProject, image='project/open.png')
        GetApp().AddCommand(constants.ID_CLOSE_PROJECT, _('&Project'), _('Close Project'), self.CloseProject, tester=lambda : self.GetView().UpdateUI(constants.ID_CLOSE_PROJECT))
        GetApp().AddCommand(constants.ID_SAVE_PROJECT, _('&Project'), _('Save Project'), self.SaveProject, image='project/save.png', tester=lambda : self.GetView().UpdateUI(constants.ID_SAVE_PROJECT))
        GetApp().AddCommand(constants.ID_DELETE_PROJECT, _('&Project'), _('Delete Project'), self.DeleteProject, image='project/trash.png', tester=lambda : self.GetView().UpdateUI(constants.ID_DELETE_PROJECT))
        GetApp().AddCommand(constants.ID_CLEAN_PROJECT, _('&Project'), _('Clean Project'), self.CleanProject, tester=lambda : self.GetView().UpdateUI(constants.ID_CLEAN_PROJECT))
        GetApp().AddCommand(constants.ID_ARCHIVE_PROJECT, _('&Project'), _('Archive Project'), self.ArchiveProject, image='project/archive.png', add_separator=True, tester=lambda : self.GetView().UpdateUI(constants.ID_ARCHIVE_PROJECT))
        GetApp().AddCommand(constants.ID_IMPORT_FILES, _('&Project'), _('Import Files...'), image=GetApp().GetImage('project/import.png'), tester=lambda : self.GetView().UpdateUI(constants.ID_IMPORT_FILES), handler=lambda : self.ProcessEvent(constants.ID_IMPORT_FILES))
        GetApp().AddCommand(constants.ID_ADD_FILES_TO_PROJECT, _('&Project'), _('Add &Files to Project...'), handler=lambda : self.ProcessEvent(constants.ID_ADD_FILES_TO_PROJECT), tester=lambda : self.GetView().UpdateUI(constants.ID_ADD_FILES_TO_PROJECT))
        GetApp().AddCommand(constants.ID_ADD_DIR_FILES_TO_PROJECT, _('&Project'), _('Add Directory Files to Project...'), handler=lambda : self.ProcessEvent(constants.ID_ADD_DIR_FILES_TO_PROJECT), tester=lambda : self.GetView().UpdateUI(constants.ID_ADD_DIR_FILES_TO_PROJECT))
        GetApp().AddCommand(constants.ID_ADD_CURRENT_FILE_TO_PROJECT, _('&Project'), _('&Add Active File to Project...'), handler=lambda : self.ProcessEvent(constants.ID_ADD_CURRENT_FILE_TO_PROJECT), add_separator=True, tester=lambda : self.GetView().UpdateUI(constants.ID_ADD_CURRENT_FILE_TO_PROJECT))
        GetApp().AddCommand(constants.ID_ADD_NEW_FILE, _('&Project'), _('New File'), image=GetApp().GetImage('project/new_file.png'), handler=lambda : self.ProcessEvent(constants.ID_ADD_NEW_FILE), tester=lambda : self.GetView().UpdateUI(constants.ID_ADD_NEW_FILE))
        GetApp().AddCommand(constants.ID_ADD_FOLDER, _('&Project'), _('New Folder'), image=GetApp().GetImage('project/folder.png'), handler=lambda : self.ProcessEvent(constants.ID_ADD_FOLDER), add_separator=True, tester=lambda : self.GetView().UpdateUI(constants.ID_ADD_FOLDER))
        GetApp().AddCommand(constants.ID_PROPERTIES, _('&Project'), _('Project Properties'), self.OnProjectProperties, image=GetApp().GetImage('project/properties.png'), tester=lambda : self.GetView().UpdateUI(constants.ID_PROPERTIES))
        GetApp().AddCommand(constants.ID_OPEN_FOLDER_PATH, _('&Project'), _('Open Project Path in Explorer'), handler=self.OpenProjectPath, tester=lambda : self.GetView().UpdateUI(constants.ID_OPEN_FOLDER_PATH))

    def NewProject(self):
        """
            新建项目
        """
        template = GetApp().GetDocumentManager().FindTemplateForTestPath(consts.PROJECT_EXTENSION)
        template.CreateDocument('', flags=core.DOC_NEW)

    def OpenProject(self):
        """
            打开项目
        """
        template = GetApp().GetDocumentManager().FindTemplateForTestPath(consts.PROJECT_EXTENSION)
        descrs = [
         strutils.get_template_filter(template)]
        project_path = filedialog.askopenfilename(master=GetApp(), filetypes=descrs)
        if not project_path:
            return
        project_path = fileutils.opj(project_path)
        self.GetView().OpenProject(project_path)

    @misc.update_toolbar
    def CloseProject(self):
        self.GetView().CloseProject()

    @misc.update_toolbar
    def SaveProject(self):
        self.GetView().SaveProject()

    @misc.update_toolbar
    def DeleteProject(self):
        self.GetView().DeleteProject()

    def ArchiveProject(self):
        self.GetView().ArchiveProject()

    def CleanProject(self):
        self.GetView().CleanProject()

    def GetFilesFromCurrentProject(self):
        view = self.GetView()
        if view:
            project = view.GetDocument()
            if project:
                pass
            return project.GetFiles()

    def on_secondary_click(self, event):
        items = self.tree.selection()
        if not items:
            return
        if self.GetView()._HasFilesSelected():
            menu = self.GetPopupFileMenu(items[0])
        else:
            if not self.tree.parent(items[0]):
                menu = self.GetPopupProjectMenu(items[0])
            else:
                menu = self.GetPopupFolderMenu(items[0])
        menu['postcommand'] = lambda : menu._update_menu()
        menu.tk_popup(event.x_root, event.y_root)

    def GetPopupFileMenu(self, item):
        menu = tkmenu.PopupMenu(self, **misc.get_style_configuration('Menu'))
        menu.Append(constants.ID_OPEN_SELECTION, _('&Open'), handler=lambda : self.ProcessEvent(constants.ID_OPEN_SELECTION))
        common_item_ids = [None, consts.ID_UNDO, consts.ID_REDO, consts.ID_CUT, consts.ID_COPY, consts.ID_PASTE, consts.ID_CLEAR, None, consts.ID_SELECTALL]
        self.GetCommonItemsMenu(menu, common_item_ids)
        menu.Append(constants.ID_RENAME, _('&Rename'), handler=lambda : self.ProcessEvent(constants.ID_RENAME))
        menu.Append(constants.ID_REMOVE_FROM_PROJECT, _('Remove from Project'), handler=lambda : self.ProcessEvent(constants.ID_REMOVE_FROM_PROJECT))
        GetApp().event_generate(constants.PROJECTVIEW_POPUP_FILE_MENU_EVT, menu=menu, item=item)
        self.AppendFileFoderCommonMenu(menu)
        return menu

    def AppendFileFoderCommonMenu(self, menu):
        menu.add_separator()
        menu.Append(constants.ID_PROPERTIES, _('&Properties'), handler=lambda : self.ProcessEvent(constants.ID_PROPERTIES))
        menu.Append(constants.ID_OPEN_FOLDER_PATH, _('Open Path in Explorer'), handler=lambda : self.ProcessEvent(constants.ID_OPEN_FOLDER_PATH))
        menu.Append(constants.ID_OPEN_TERMINAL_PATH, _('Open Command Prompt here...'), handler=lambda : self.ProcessEvent(constants.ID_OPEN_TERMINAL_PATH))
        menu.Append(constants.ID_COPY_PATH, _('Copy Full Path'), handler=lambda : self.ProcessEvent(constants.ID_COPY_PATH))

    def GetPopupFolderMenu(self, item):
        menu = tkmenu.PopupMenu(self, **misc.get_style_configuration('Menu'))
        menu['postcommand'] = lambda : menu._update_menu()
        common_item_ids = self.GetPopupFolderItemIds()
        self.GetCommonItemsMenu(menu, common_item_ids, is_folder=True)
        menu.Append(constants.ID_RENAME, _('&Rename'), handler=lambda : self.ProcessEvent(constants.ID_RENAME))
        menu.Append(constants.ID_REMOVE_FROM_PROJECT, _('Remove from Project'), handler=lambda : self.ProcessEvent(constants.ID_REMOVE_FROM_PROJECT))
        GetApp().event_generate(constants.PROJECTVIEW_POPUP_FOLDER_MENU_EVT, menu=menu, item=item)
        self.AppendFileFoderCommonMenu(menu)
        return menu

    def GetPopupFolderItemIds(self):
        folder_item_ids = [
         constants.ID_IMPORT_FILES, constants.ID_ADD_FILES_TO_PROJECT, constants.ID_ADD_DIR_FILES_TO_PROJECT, None, constants.ID_ADD_NEW_FILE, constants.ID_ADD_FOLDER,
         None, consts.ID_UNDO, consts.ID_REDO, consts.ID_CUT, consts.ID_COPY, consts.ID_PASTE, consts.ID_CLEAR, None, consts.ID_SELECTALL]
        return folder_item_ids

    def GetPopupProjectMenu(self, item):
        menu = tkmenu.PopupMenu(self, **misc.get_style_configuration('Menu'))
        menu['postcommand'] = lambda : menu._update_menu()
        common_item_ids = self.GetPopupProjectItemIds()
        self.GetCommonItemsMenu(menu, common_item_ids)
        if self.GetCurrentProject() is not None:
            menu.Append(constants.ID_RENAME, _('&Rename'), handler=lambda : self.ProcessEvent(constants.ID_RENAME))
            menu.Append(constants.ID_OPEN_TERMINAL_PATH, _('Open Command Prompt here...'), handler=lambda : self.ProcessEvent(constants.ID_OPEN_TERMINAL_PATH))
            menu.Append(constants.ID_COPY_PATH, _('Copy Full Path'), handler=lambda : self.ProcessEvent(constants.ID_COPY_PATH))
        GetApp().event_generate(constants.PROJECTVIEW_POPUP_ROOT_MENU_EVT, menu=menu, item=item)
        return menu

    def GetPopupProjectItemIds(self):
        project_item_ids = [
         constants.ID_NEW_PROJECT, constants.ID_OPEN_PROJECT]
        if self.GetCurrentProject() is not None:
            project_item_ids.extend([constants.ID_CLOSE_PROJECT, constants.ID_SAVE_PROJECT, constants.ID_DELETE_PROJECT,
             constants.ID_CLEAN_PROJECT, constants.ID_ARCHIVE_PROJECT])
            project_item_ids.extend([None, constants.ID_IMPORT_FILES, constants.ID_ADD_FILES_TO_PROJECT,
             constants.ID_ADD_DIR_FILES_TO_PROJECT, None, constants.ID_ADD_NEW_FILE, constants.ID_ADD_FOLDER])
            project_item_ids.extend([None, constants.ID_PROPERTIES, constants.ID_OPEN_FOLDER_PATH])
        return project_item_ids

    def GetCommonItemsMenu(self, menu, menu_item_ids, is_folder=False):
        for item_id in menu_item_ids:
            if item_id == None:
                menu.add_separator()
                continue
                menu_item = GetApp().Menubar.FindItemById(item_id)
                if menu_item is None:
                    pass
                else:
                    handler = GetApp().Menubar.GetMenuhandler(_('&Project'), item_id)
                    extra = {}
                    if item_id in [consts.ID_UNDO, consts.ID_REDO]:
                        extra.update(dict(tester=lambda : False))
                    else:
                        if item_id in [consts.ID_CLEAR, consts.ID_SELECTALL]:
                            extra.update(dict(tester=None))
                        else:
                            if item_id == consts.ID_PASTE:
                                extra.update(dict(tester=self.GetView().CanPaste))
                            else:
                                if item_id in [consts.ID_CUT, consts.ID_COPY]:
                                    if is_folder:
                                        extra.update(dict(tester=lambda : False))
                                else:
                                    extra.update(dict(tester=None))
                        if handler == None:

                            def common_handler(id=item_id):
                                self.ProcessEvent(id)

                            handler = common_handler
                    menu.AppendMenuItem(menu_item, handler=handler, **extra)

    def ProcessEvent(self, id):
        view = self.GetView()
        if id == constants.ID_ADD_FILES_TO_PROJECT:
            view.OnAddFileToProject()
            return True
        else:
            if id == constants.ID_ADD_DIR_FILES_TO_PROJECT:
                view.OnAddDirToProject()
                return True
            if id == constants.ID_ADD_CURRENT_FILE_TO_PROJECT:
                view.OnAddCurrentFileToProject()
                return True
            if id == constants.ID_ADD_NEW_FILE:
                view.OnAddNewFile()
                return True
            if id == constants.ID_ADD_FOLDER:
                view.OnAddFolder()
                return True
            if id == constants.ID_RENAME:
                view.OnRename()
                return True
            if id == constants.ID_CLEAR:
                view.DeleteFromProject()
                return True
            if id == constants.ID_DELETE_PROJECT:
                self.OnDeleteProject(event)
                return True
            if id == constants.ID_CUT:
                view.OnCut()
                return True
            if id == constants.ID_COPY:
                view.OnCopy()
                return True
            if id == constants.ID_PASTE:
                view.OnPaste()
                return True
            if id == constants.ID_REMOVE_FROM_PROJECT:
                view.RemoveFromProject()
                return True
            if id == constants.ID_SELECTALL:
                self.OnSelectAll(event)
                return True
            if id == constants.ID_OPEN_SELECTION:
                self.OpenSelection()
                return True
            if id == constants.ID_PROPERTIES:
                self.OnProperties()
                return True
            if id == constants.ID_IMPORT_FILES:
                view.ImportFilesToProject()
                return True
            if id == constants.ID_OPEN_FOLDER_PATH:
                self.OpenFolderPath()
                return True
            if id == constants.ID_OPEN_TERMINAL_PATH:
                self.OpenPromptPath()
                return True
            if id == constants.ID_COPY_PATH:
                self.CopyPath()
                return True
            return False

    def OnProperties(self):
        projectproperty.PropertiesService().ShowPropertyDialog(self.tree.GetSingleSelectItem())

    def OnProjectProperties(self, item_name=None):
        projectproperty.PropertiesService().ShowPropertyDialog(self.tree.GetRootItem(), option_name=item_name)

    def OpenProjectPath(self):
        document = self.GetCurrentProject()
        fileutils.safe_open_file_directory(document.GetFilename())

    def OpenFolderPath(self):
        document = self.GetCurrentProject()
        project_path = os.path.dirname(document.GetFilename())
        item = self.tree.GetSingleSelectItem()
        filePath = self.GetItemPath(item)
        fileutils.safe_open_file_directory(filePath)

    def OpenPromptPath(self):
        item = self.tree.GetSingleSelectItem()
        filePath = self.GetItemPath(item)
        GetApp().OpenTerminator(filename=filePath)

    def CopyPath(self):
        document = self.GetCurrentProject()
        item = self.tree.GetSingleSelectItem()
        filePath = self.GetItemPath(item)
        utils.CopyToClipboard(filePath)

    def GetItemPath(self, item):
        if self.GetView()._IsItemFile(item):
            filePath = self.GetView()._GetItemFilePath(item)
        else:
            document = self.GetCurrentProject()
            project_path = os.path.dirname(document.GetFilename())
            filePath = fileutils.opj(os.path.join(project_path, self.GetView()._GetItemFolderPath(item)))
        return filePath

    def StartCopyFilesToProject(self, progress_ui, file_list, src_path, dest_path, que):
        self.copy_thread = threading.Thread(target=self.CopyFilesToProject, args=(progress_ui, file_list, src_path, dest_path, que))
        self.copy_thread.start()

    def BuildFileList(self, file_list):
        return file_list

    def CopyFilesToProject(self, progress_ui, file_list, src_path, dest_path, que):
        utils.get_logger().info('start import total %d files to path %s', len(file_list), dest_path)
        start_time = time.time()
        files_dict = self.BuildFileMaps(file_list)
        copy_file_count = 0
        for dir_path in files_dict:
            self.tree.item(self.tree.GetRootItem(), open=True)
            if progress_ui.is_cancel:
                break
            file_path_list = files_dict[dir_path]
            self.BuildFileList(file_path_list)
            folder_path = dir_path.replace(src_path, '').replace(os.sep, '/').lstrip('/').rstrip('/')
            paths = dest_path.split(os.sep)
            if len(paths) > 1:
                dest_folder_path = '/'.join(paths[1:])
                if folder_path != '':
                    dest_folder_path += '/' + folder_path
            else:
                dest_folder_path = folder_path
            self.GetView().GetDocument().GetCommandProcessor().Submit(ProjectAddProgressFilesCommand(progress_ui, self.GetView().GetDocument(), file_path_list, que, folderPath=dest_folder_path, range_value=copy_file_count))
            copy_file_count += len(file_path_list)

        que.put((None, None))
        end_time = time.time()
        utils.get_logger().info('success import total %d files,elapse %d seconds', copy_file_count, int(end_time - start_time))

    def BuildFileMaps(self, file_list):
        d = {}
        for file_path in file_list:
            dir_path = os.path.dirname(file_path)
            if dir_path not in d:
                d[dir_path] = [
                 file_path]
            else:
                d[dir_path].append(file_path)

        return d

    def SaveProjectConfig(self):
        self.GetView().WriteProjectConfig()

    def GetOpenProjects(self):
        return self.GetView().Documents