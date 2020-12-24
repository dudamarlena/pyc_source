# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/ide.py
# Compiled at: 2019-10-17 01:45:10
# Size of source mod 2**32: 46980 bytes
"""
    尽量少在文件头部导入太多模块,会导致程序启动很慢
"""
import tkinter as tk
from noval import core, imageutils, consts, _, Locale
import noval.python.parser.utils as parserutils
from dummy.userdb import UserDataDb
from noval.util import utils
import noval.util.strutils as strutils, noval.constants as constants
from pkg_resources import resource_filename
import sys, noval.util.logger as logger, os, noval.misc as misc, tkinter.font as tk_font
from tkinter import ttk
from noval.syntax import synglob, syntax
from noval.util import record
import noval.menu as tkmenu, noval.syntax.lang as lang, noval.preference as preference
from tkinter import messagebox
import subprocess, noval.docposition as docposition, noval.ui_utils as ui_utils, traceback, noval.ttkwidgets.messagedialog as messagedialog, noval.util.fileutils as fileutils, noval.logview as logview

class IDEApplication(core.App):

    def __init__(self):
        self._event_handlers = {}
        core.App.__init__(self)

    def OnInit(self):
        args = sys.argv
        if strutils.isInArgs('debug', args):
            self.SetAppName(consts.DEBUG_APPLICATION_NAME)
            self.SetDebug(True)
            self.SetSingleInstance(False)
        else:
            self.SetAppName(consts.APPLICATION_NAME)
            self.SetDebug(False)
            self.SetSingleInstance(True)
        import noval.boot_common
        logger.initLogging(self.GetDebug())
        if not core.App.OnInit(self):
            return False
        from noval.editor import text as texteditor
        import noval.colorfont as colorfont, noval.docoption as docoption, noval.generalopt as generalopt, noval.project.debugger as basedebugger, noval.project.baseviewer as baseprojectviewer, noval.project.document as projectdocument
        from noval.editor import imageviewer
        tk.Tk.report_callback_exception = self._on_tk_exception
        self._open_project_path = None
        self.frame = None
        self._pluginmgr = None
        self._debugger_class = basedebugger.Debugger
        self._debugger_view_class = basedebugger.DebugView
        self.project_template_class = baseprojectviewer.ProjectTemplate
        self.project_document_class = projectdocument.ProjectDocument
        self.project_view_class = baseprojectviewer.ProjectView
        self._config = utils.Config(self.GetAppName())
        self._init_scaling()
        self._init_theming()
        self.geometry('{0}x{1}+{2}+{3}'.format(max(utils.profile_get_int(consts.FRAME_WIDTH_KEY), 320), max(utils.profile_get_int(consts.FRAME_HEIGHT_KEY), 240), min(max(utils.profile_get_int(consts.FRAME_LEFT_LOC_KEY), 0), self.winfo_screenwidth() - 200), min(max(utils.profile_get_int(consts.FRAME_TOP_LOC_KEY), 0), self.winfo_screenheight() - 200)))
        if utils.profile_get_int(consts.FRAME_MAXIMIZED_KEY, True):
            self.MaxmizeWindow()
        lang_id = utils.profile_get_int(consts.LANGUANGE_ID_KEY, utils.get_lang_config())
        if Locale.IsAvailable(lang_id):
            self.locale = Locale(lang_id)
            self.locale.AddCatalogLookupPathPrefix(os.path.join(utils.get_app_path(), 'locale'))
            ibRet = self.locale.AddCatalog(consts.APPLICATION_NAME.lower())
            ibRet = self.locale.AddCatalog('wxstd')
            self.locale.AddCatalog('wxstock')
        else:
            utils.get_logger().error('lang id %d is not available', lang_id)
        docManager = core.DocManager()
        self.SetDocumentManager(docManager)
        defaultTemplate = core.DocTemplate(docManager, _('All Files'), '*.*', os.getcwd(), '.txt', 'Text Document', _('Text Editor'), texteditor.TextDocument, texteditor.TextView, core.TEMPLATE_INVISIBLE, icon=imageutils.getBlankIcon())
        docManager.AssociateTemplate(defaultTemplate)
        imageTemplate = core.DocTemplate(docManager, _('Image File'), '*.bmp;*.ico;*.gif;*.jpg;*.jpeg;*.png', os.getcwd(), '.png', 'Image Document', _('Image Viewer'), imageviewer.ImageDocument, imageviewer.ImageView, core.TEMPLATE_NO_CREATE, icon=imageutils.get_image_file_icon())
        docManager.AssociateTemplate(imageTemplate)
        try:
            ui_utils.check_chardet_version()
        except RuntimeError as e:
            messagebox.showerror(self.GetAppName(), str(e), parent=self)
            return False

        self.CreateLexerTemplates()
        self.LoadLexerTemplates()
        self.SetDefaultIcon(imageutils.get_default_icon())
        self._InitFonts()
        self._default_command_ids = []
        self._InitMenu()
        self._InitMainFrame()
        self._InitCommands()
        preference.PreferenceManager().AddOptionsPanelClass(preference.ENVIRONMENT_OPTION_NAME, preference.GENERAL_ITEM_NAME, generalopt.GeneralOptionPanel)
        preference.PreferenceManager().AddOptionsPanelClass(preference.ENVIRONMENT_OPTION_NAME, preference.PROJECT_ITEM_NAME, baseprojectviewer.ProjectOptionsPanel)
        preference.PreferenceManager().AddOptionsPanelClass(preference.ENVIRONMENT_OPTION_NAME, preference.TEXT_ITEM_NAME, texteditor.TextOptionsPanel)
        preference.PreferenceManager().AddOptionsPanelClass(preference.ENVIRONMENT_OPTION_NAME, 'Document', docoption.DocumentOptionsPanel)
        preference.PreferenceManager().AddOptionsPanelClass(preference.ENVIRONMENT_OPTION_NAME, preference.FONTS_CORLORS_ITEM_NAME, colorfont.ColorFontOptionsPanel)
        self.InitPlugins()
        self.OpenCommandLineArgs()
        self.SetCurrentProject()
        self.initializing = False
        self.after(500, self.InitTkDnd)
        self.bind('TextInsert', self.EventTextChange, True)
        self.bind('TextDelete', self.EventTextChange, True)
        self.bind('<<UpdateAppearance>>', self.EventTextChange, True)
        self.bind('<FocusIn>', self._on_focus_in, True)
        return True

    @utils.compute_run_time
    def InitPlugins(self):
        self.LoadDefaultPlugins()
        self.MainFrame.InitPlugins()
        self.MainFrame.GetProjectView()._InitCommands()
        self.InitThemeMenu()
        self.load_themes()

    def _on_tk_exception(self, exc, val, tb):
        sys.last_type = exc
        sys.last_value = val
        sys.last_traceback = tb
        self.report_exception()

    def report_exception(self, title='Internal error'):
        utils.get_logger().exception(title)
        if utils.is_py2():
            tk._default_root = self
        if tk._default_root and utils.profile_get_int('RedirectTkException', True if self.GetDebug() else False):
            typ, value, _ = sys.exc_info()
            assert typ is not None
            msg = traceback.format_exc()
            dlg = messagedialog.ScrolledMessageDialog(self, title, msg)
            dlg.ShowModal()

    def LoadDefaultPlugins(self):
        """
            默认插件在consts.DEFAULT_PLUGINS中指定
        """
        pass

    def AppendDefaultCommand(self, command_id):
        self._default_command_ids.append(command_id)

    def InitTkDnd(self):
        """
            初始化文件拖拽
        """
        core.App.InitTkDnd(self)
        if self.dnd is not None:
            self.event_generate('InitTkDnd')
        self.event_generate('<<AppInitialized>>')

    def _on_focus_in(self, event):
        """
            主界面在前台显示时,检查文本是否在外部改变
        """
        openDocs = self.GetDocumentManager().GetDocuments()
        for doc in openDocs:
            if isinstance(doc, self.project_document_class):
                view = self.MainFrame.GetProjectView(False).GetView()
            else:
                view = doc.GetFirstView()
            if hasattr(view, '_is_external_changed') and view._is_external_changed and utils.profile_get_int('CheckFileModify', True):
                view.check_for_external_changes()

    def EventTextChange(self, event):
        """
            文本改变时重新对代码着色,同时更改代码大纲显示内容
        """
        if hasattr(event, 'text_widget'):
            text = event.text_widget
        else:
            text = event.widget
        is_syntax_color_ctrl = hasattr(text, 'GetColorClass')
        if not hasattr(text, 'syntax_colorer'):
            if is_syntax_color_ctrl:
                class_ = text.GetColorClass()
                text.syntax_colorer = class_(text)
        if is_syntax_color_ctrl:
            text.syntax_colorer.schedule_update(event, use_coloring=utils.profile_get_int('TextHighlightSyntax', True))
            text.tag_remove('motion', '1.0', 'end')
            text.tag_add('motion', '1.0', 'end')
        if isinstance(text.master.master, core.DocTabbedChildFrame):
            self.MainFrame.GetView(consts.OUTLINE_VIEW_NAME)._update_frame_contents()

    def CreateLexerTemplates(self):
        synglob.LexerFactory().CreateLexerTemplates(self.GetDocumentManager())

    def LoadLexerTemplates(self):
        synglob.LexerFactory().LoadLexerTemplates(self.GetDocumentManager())

    def CreateProjectTemplate(self):
        template_class, document_class, view_class = self.GetProjectTemplateClassData()
        projectTemplate = template_class(self.GetDocumentManager(), _('Project File'), '*%s' % consts.PROJECT_EXTENSION, os.getcwd(), consts.PROJECT_EXTENSION, 'Project Document', _('Project Viewer'), document_class, view_class, icon=imageutils.getProjectIcon())
        self.GetDocumentManager().AssociateTemplate(projectTemplate)

    def GetDefaultLangId(self):
        return lang.ID_LANG_TXT

    @property
    def MainFrame(self):
        return self.frame

    def GotoView(self, file_path, lineNum=-1, colno=-1, trace_track=True, load_outline=True):
        docs = self.GetDocumentManager().CreateDocument(file_path, core.DOC_SILENT | core.DOC_OPEN_ONCE)
        if docs == []:
            return
        foundView = docs[0].GetFirstView()
        if foundView:
            foundView.GetFrame().SetFocus()
            foundView.Activate()
            if not hasattr(foundView, 'GotoLine'):
                return
            if colno == -1:
                foundView.GotoLine(lineNum)
            else:
                if trace_track:
                    foundView.GotoPos(lineNum, colno)
                else:
                    foundView.GetCtrl().GotoPos(lineNum, colno)
                return
            if self.MainFrame.GetOutlineView().IsValidViewType(foundView) and load_outline:
                self.MainFrame.GetOutlineView().LoadOutLine(foundView, lineNum=lineNum)

    @property
    def OpenProjectPath(self):
        return self._open_project_path

    def GetPluginManager(self):
        """Returns the plugin manager used by this application
        @return: Apps plugin manager
        @see: L{plugin}

        """
        return self._pluginmgr

    def SetPluginManager(self, pluginmgr):
        self._pluginmgr = pluginmgr

    def AddMessageCatalog(self, name, path):
        """
            添加翻译文件的查找路径,在插件中使用,如果插件需要翻译,可以在egg文件里面添加翻译文件在egg文件里面的相对路径
        """
        if self.locale is not None:
            path = resource_filename(path, 'locale')
            self.locale.AddCatalogLookupPathPrefix(path)
            self.locale.AddCatalog(name)

    def _InitMenu(self):
        self.option_add('*tearOff', tk.FALSE)
        if utils.profile_get_int('USE_CUSTOM_MENUBAR', False):
            self._menu_bar = tkmenu.ThemeMenuBar(self)
            self._menu_bar.grid(row=0, column=0, sticky='nsew')
        else:
            self._menu_bar = tkmenu.DefaultMenuBar(self)
            self.config(menu=self._menu_bar)
        self._menu_bar.GetFileMenu()
        self._menu_bar.GetEditMenu()
        self._menu_bar.GetViewMenu()
        self._menu_bar.GetFormatMenu()
        self._menu_bar.GetProjectMenu()
        self._menu_bar.GetRunMenu()
        self._menu_bar.GetToolsMenu()
        self._menu_bar.GetHelpMenu()

    @property
    def Menubar(self):
        return self._menu_bar

    def AddCommand(self, command_id, main_menu_name, command_label, handler, accelerator=None, image=None, include_in_toolbar=False, add_separator=False, kind=consts.NORMAL_MENU_ITEM_KIND, variable=None, tester=None, default_tester=False, default_command=False, skip_sequence_binding=False, extra_sequences=[], **extra_args):
        main_menu = self._menu_bar.GetMenu(main_menu_name)
        self.AddMenuCommand(command_id, main_menu, command_label, handler, accelerator, image, include_in_toolbar, add_separator, kind, variable, tester, default_tester, default_command, skip_sequence_binding, extra_sequences, **extra_args)

    def InsertCommand(self, refer_item_id, command_id, main_menu_name, command_label, handler, accelerator=None, image=None, add_separator=False, kind=consts.NORMAL_MENU_ITEM_KIND, variable=None, tester=None, pos='after'):
        if image is not None and type(image) == str:
            image = self.GetImage(image)
        main_menu = self._menu_bar.GetMenu(main_menu_name)
        accelerator = self.AddAcceleratorCommand(command_id, accelerator, handler, tester)
        if pos == 'after':
            menu_item = main_menu.InsertAfter(refer_item_id, command_id, command_label, handler=handler, img=image, accelerator=accelerator, kind=kind, variable=variable, tester=tester)
        elif pos == 'before':
            menu_item = main_menu.InsertBefore(refer_item_id, command_id, command_label, handler=handler, img=image, accelerator=accelerator, kind=kind, variable=variable, tester=tester)
        return menu_item

    def AddAcceleratorCommand(self, command_id, accelerator, handler, tester, bell_when_denied=True, skip_sequence_binding=False, extra_sequences=[]):

        def dispatch(event=None):
            if not tester or tester():
                denied = False
                handler()
            else:
                denied = True
                utils.get_logger().debug('Command %d execution denied', command_id)
            if bell_when_denied:
                self.bell()

        accelerator, sequence = self._menu_bar.keybinder.GetBinding(command_id, accelerator)
        if sequence is not None and not skip_sequence_binding:
            self.bind_all(sequence, dispatch, True)
        for extra_sequence in extra_sequences:
            self.bind_all(extra_sequence, dispatch, True)

        return accelerator

    def AddMenuCommand(self, command_id, menu, command_label, handler, accelerator=None, image=None, include_in_toolbar=False, add_separator=False, kind=consts.NORMAL_MENU_ITEM_KIND, variable=None, tester=None, default_tester=False, default_command=False, skip_sequence_binding=False, extra_sequences=[], **extra_args):
        """
            tester表示菜单状态更新的回调函数,返回bool值
            default_command表示菜单是否在文本编辑区为空白时(即没有一个文本编辑窗口),菜单状态为灰选
        """
        if image is not None and type(image) == str:
            image = self.GetImage(image)
        if tester is None and default_tester:
            if default_command:
                self.AppendDefaultCommand(command_id)
            tester = lambda : self.UpdateUI(command_id)
        if add_separator:
            sep_location = extra_args.pop('separator_location', 'bottom')
        accelerator = self.AddAcceleratorCommand(command_id, accelerator, handler, tester, skip_sequence_binding=skip_sequence_binding, extra_sequences=extra_sequences)
        if add_separator and sep_location == 'top':
            menu.add_separator()
        menu.Append(command_id, command_label, handler=handler, img=image, accelerator=accelerator, kind=kind, variable=variable, tester=tester, **extra_args)
        if add_separator and sep_location == 'bottom':
            menu.add_separator()
        if include_in_toolbar:
            self.MainFrame.AddToolbarButton(command_id, image, command_label, handler, accelerator, tester=tester)

    def UpdateUI(self, command_id):
        if command_id in [constants.ID_RUN, constants.ID_DEBUG] and self.MainFrame.GetProjectView(False).GetCurrentProject() is not None:
            return True
        current_editor = self.MainFrame.GetNotebook().get_current_editor()
        if command_id in self._default_command_ids and current_editor is None:
            return False
        active_view = current_editor.GetView()
        assert active_view is not None
        return active_view.UpdateUI(command_id)

    def _InitCommands(self):
        self.AddCommand(constants.ID_NEW, _('&File'), _('&New...'), self.OnNew, image='toolbar/new.png', include_in_toolbar=True)
        self.AddCommand(constants.ID_OPEN, _('&File'), _('&Open...'), self.OnOpen, image='toolbar/open.png', include_in_toolbar=True)
        self.AddCommand(constants.ID_CLOSE, _('&File'), _('&Close'), self.OnClose, default_tester=True, default_command=True)
        self.AddCommand(constants.ID_CLOSE_ALL, _('&File'), _('&Close A&ll'), self.OnCloseAll, add_separator=True, default_tester=True, default_command=True)
        self.AddCommand(constants.ID_SAVE, _('&File'), _('&Save...'), self.OnFileSave, image='toolbar/save.png', include_in_toolbar=True, default_tester=True, default_command=True)
        self.AddCommand(constants.ID_SAVEAS, _('&File'), _('Save &As...'), self.OnFileSaveAs, default_tester=True, default_command=True)
        self.AddCommand(constants.ID_SAVEALL, _('&File'), _('Save All'), self.OnFileSaveAll, image='toolbar/saveall.png', include_in_toolbar=True, add_separator=True, tester=self.MainFrame.GetNotebook().SaveAllFilesEnabled)
        self.AddCommand(constants.ID_EXIT, _('&File'), _('E&xit'), self.Quit, image='exit.png')
        self.GetDocumentManager().FileHistoryUseMenu(self._menu_bar.GetFileMenu())
        self.GetDocumentManager().FileHistoryAddFilesToMenu()
        self.MainFrame._InitCommands()
        self.AddCommand(constants.ID_SHOW_FULLSCREEN, _('&View'), _('Show FullScreen'), self.ShowFullScreen, image='monitor.png')
        self.AddCommand(constants.ID_RUN, _('&Run'), _('&Start Running'), self.Run, image='toolbar/run.png', include_in_toolbar=True, default_tester=True, default_command=True)
        self.AddCommand(constants.ID_DEBUG, _('&Run'), _('&Start Debugging'), self.Debug, image='toolbar/debug.png', include_in_toolbar=True, default_tester=True, default_command=True)
        self.AddCommand(constants.ID_OPEN_TERMINAL, _('&Tools'), _('&Open terminator...'), self.OpenTerminator, image='cmd.png')
        self.AddCommand(constants.ID_GOTO_OFFICIAL_WEB, _('&Help'), _('&Visit NovalIDE Website'), self.GotoWebsite)
        self.AddCommand(constants.ID_FEEDBACK, _('&Help'), _('Feedback'), self.Feedback)

    def Run(self):
        """
            在终端中运行程序
        """
        self.GetDebugger().Run()

    def Debug(self):
        """
            在程序调试窗口中运行程序
        """
        self.GetDebugger().Debug()

    def OpenTerminator(self, filename=None):
        if filename:
            if os.path.isdir(filename):
                cwd = filename
            else:
                cwd = os.path.dirname(filename)
        else:
            cwd = os.getcwd()
        if utils.is_windows():
            subprocess.Popen('start cmd.exe', shell=True, cwd=cwd)
        else:
            subprocess.Popen('gnome-terminal', shell=True, cwd=cwd)

    def GetImage(self, file_name):
        return imageutils.load_image('', file_name, self._scaling_factor)

    def _InitMainFrame(self):
        import noval.frame as frame
        self.frame = frame.DocTabbedParentFrame(self, None, None, -1, self.GetAppName(), tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        if self.GetDebug():
            self.MainFrame.AddView('Logs', logview.LogView, _('Logs'), 's', default_position_key=3)

    @misc.update_toolbar
    def OnOpen(self):
        self.GetDocumentManager().CreateDocument('', core.DEFAULT_DOCMAN_FLAGS)

    def OnNew(self):
        self.GetDocumentManager().CreateDocument('', core.DOC_NEW)

    @misc.update_toolbar
    def OnClose(self):
        self.MainFrame.CloseDoc()

    @misc.update_toolbar
    def OnCloseAll(self):
        self.MainFrame.CloseAllDocs()

    @misc.update_toolbar
    def OnFileSave(self):
        """
        Saves the current document by calling wxDocument.Save for the current
        document.
        """
        doc = self.GetDocumentManager().GetCurrentDocument()
        if not doc:
            return
        doc.Save()

    @misc.update_toolbar
    def OnFileSaveAs(self):
        """
        Calls wxDocument.SaveAs for the current document.
        """
        doc = self.GetDocumentManager().GetCurrentDocument()
        if not doc:
            return
        self.SaveAsDocument(doc)

    def SaveAsDocument(self, doc):
        """
            另存为文件
        """
        old_filename = doc.GetFilename()
        if not doc.SaveAs():
            return
        new_filename = doc.GetFilename()
        if doc.IsWatched and not parserutils.ComparePath(new_filename, old_filename):
            doc.FileWatcher.RemoveFile(old_filename)

    @misc.update_toolbar
    def OnFileSaveAll(self):
        """
        Saves all of the currently open documents.
        """
        docs = self.GetDocumentManager().GetDocuments()
        for doc in docs:
            doc.Save()

    def GetDefaultEditorFamily(self):
        default_editor_family = consts.DEFAULT_FONT_FAMILY
        families = tk_font.families()
        for family in ['Consolas', 'Ubuntu Mono', 'Menlo', 'DejaVu Sans Mono']:
            if family in families:
                default_editor_family = family
                break

        return default_editor_family

    def _InitFonts(self):
        default_editor_family = self.GetDefaultEditorFamily()
        default_io_family = consts.DEFAULT_FONT_FAMILY
        default_font = tk_font.nametofont('TkDefaultFont')
        if utils.is_linux():
            heading_font = tk_font.nametofont('TkHeadingFont')
            heading_font.configure(weight='normal')
            caption_font = tk_font.nametofont('TkCaptionFont')
            caption_font.configure(weight='normal', size=default_font.cget('size'))
        self._fonts = [
         tk_font.Font(name='IOFont', family=utils.profile_get(consts.IO_FONT_FAMILY_KEY, default_io_family)),
         tk_font.Font(name='EditorFont', family=utils.profile_get(consts.EDITOR_FONT_FAMILY_KEY, default_editor_family)),
         tk_font.Font(name='SmallEditorFont', family=utils.profile_get(consts.EDITOR_FONT_FAMILY_KEY, default_editor_family)),
         tk_font.Font(name='BoldEditorFont', family=utils.profile_get(consts.EDITOR_FONT_FAMILY_KEY, default_editor_family), weight='bold'),
         tk_font.Font(name='ItalicEditorFont', family=utils.profile_get(consts.EDITOR_FONT_FAMILY_KEY, default_editor_family), slant='italic'),
         tk_font.Font(name='BoldItalicEditorFont', family=utils.profile_get(consts.EDITOR_FONT_FAMILY_KEY, default_editor_family), weight='bold', slant='italic'),
         tk_font.Font(name=consts.TREE_VIEW_FONT, family=default_font.cget('family'), size=default_font.cget('size')),
         tk_font.Font(name='TreeviewBoldFont', family=default_font.cget('family'), size=default_font.cget('size'), weight='bold'),
         tk_font.Font(name='BoldTkDefaultFont', family=default_font.cget('family'), size=default_font.cget('size'), weight='bold'),
         tk_font.Font(name='ItalicTkDefaultFont', family=default_font.cget('family'), size=default_font.cget('size'), slant='italic'),
         tk_font.Font(name='UnderlineTkDefaultFont', family=default_font.cget('family'), size=default_font.cget('size'), underline=1)]
        self.UpdateFonts()

    def UpdateFonts(self):
        default_editor_family = self.GetDefaultEditorFamily()
        editor_font_size = self._guard_font_size(utils.profile_get_int(consts.EDITOR_FONT_SIZE_KEY, consts.DEFAULT_FONT_SIZE))
        editor_font_family = utils.profile_get(consts.EDITOR_FONT_FAMILY_KEY, default_editor_family)
        io_font_family = utils.profile_get(consts.IO_FONT_FAMILY_KEY, default_editor_family)
        tk_font.nametofont('IOFont').configure(family=io_font_family, size=min(editor_font_size - 2, int(editor_font_size * 0.8 + 3)))
        tk_font.nametofont('EditorFont').configure(family=editor_font_family, size=editor_font_size)
        tk_font.nametofont('SmallEditorFont').configure(family=editor_font_family, size=editor_font_size - 2)
        tk_font.nametofont('BoldEditorFont').configure(family=editor_font_family, size=editor_font_size)
        tk_font.nametofont('ItalicEditorFont').configure(family=editor_font_family, size=editor_font_size)
        tk_font.nametofont('BoldItalicEditorFont').configure(family=editor_font_family, size=editor_font_size)
        style = ttk.Style()
        treeview_font_size = int(consts.DEFAULT_FONT_SIZE * 0.7 + 2)
        rowheight = int(self.scale_base(16)) - 1
        tk_font.nametofont(consts.TREE_VIEW_FONT).configure(size=treeview_font_size)
        tk_font.nametofont(consts.TREE_VIEW_BOLD_FONT).configure(size=treeview_font_size)
        style.configure('Treeview', rowheight=rowheight)

    def _guard_font_size(self, size):
        MIN_SIZE = 4
        MAX_SIZE = 200
        if size < MIN_SIZE:
            return MIN_SIZE
        else:
            if size > MAX_SIZE:
                return MAX_SIZE
            return size

    def AllowClose(self):
        if not self.GetDebuggerClass().CloseDebugger():
            return False
        if not self.MainFrame.CloseWindows():
            return False
        if not self.GetDocumentManager().Clear(force=False):
            return False
        return True

    def SaveLayout(self):
        utils.profile_set(consts.FRAME_MAXIMIZED_KEY, misc.get_zoomed(self))
        if not misc.get_zoomed(self):
            utils.profile_set(consts.FRAME_TOP_LOC_KEY, self.winfo_y())
            utils.profile_set(consts.FRAME_LEFT_LOC_KEY, self.winfo_x())
            utils.profile_set(consts.FRAME_WIDTH_KEY, self.winfo_width())
            utils.profile_set(consts.FRAME_HEIGHT_KEY, self.winfo_height())
        self.MainFrame.SaveLayout()

    def Quit(self):
        self.update_idletasks()
        UserDataDb().RecordEnd()
        self.SaveLayout()
        docposition.DocMgr.WriteBook()
        self._pluginmgr.WritePluginConfig()
        core.App.Quit(self)

    @misc.update_toolbar
    def OpenMRUFile(self, n):
        """
        Opens the appropriate file when it is selected from the file history
        menu.
        """
        filename = self._docManager.GetHistoryFile(n)
        if filename and os.path.exists(filename):
            self._docManager.CreateDocument(filename, core.DOC_SILENT)
        else:
            self._docManager.RemoveFileFromHistory(n)
            msgTitle = self.GetAppName()
        if not msgTitle:
            msgTitle = _('File Error')
        if filename:
            messagebox.showerror(msgTitle, _("The file '%s' doesn't exist and couldn't be opened!") % filename)

    def event_generate(self, sequence, event=None, **kwargs):
        """Uses custom event handling when sequence doesn't start with <.
        In this case arbitrary attributes can be added to the event.
        Otherwise forwards the call to Tk's event_generate"""
        if sequence.startswith('<'):
            assert event is None
            tk.Tk.event_generate(self, sequence, **kwargs)
        elif sequence in self._event_handlers:
            if event is None:
                event = AppEvent(sequence, **kwargs)
            else:
                event.update(kwargs)
            for handler in sorted(self._event_handlers[sequence].copy(), key=str):
                try:
                    handler(event)
                except Exception:
                    utils.get_logger().exception("Problem when handling '" + sequence + "'")

        self.MainFrame.UpdateToolbar()

    def bind(self, sequence, func, add=None):
        """Uses custom event handling when sequence doesn't start with <.
        Otherwise forwards the call to Tk's bind"""
        if not add:
            logging.warning('Workbench.bind({}, ..., add={}) -- did you really want to replace existing bindings?'.format(sequence, add))
        if sequence.startswith('<'):
            tk.Tk.bind(self, sequence, func, add)
        else:
            if sequence not in self._event_handlers or not add:
                self._event_handlers[sequence] = set()
            self._event_handlers[sequence].add(func)

    def SetCurrentProject(self):
        self.MainFrame.GetProjectView().SetCurrentProject()

    def add_ui_theme(self, name, parent, settings, images={}):
        if name in self._ui_themes:
            utils.get_logger().warn("Overwriting theme '%s'", name)
        self._ui_themes[name] = (parent, settings, images)
        if parent is not None:
            pass

    def _init_theming(self):
        self._style = ttk.Style()
        self._ui_themes = {}
        self._syntax_themes = {}
        default_ui_theme = 'xpnative' if utils.is_windows() else 'clam'
        self.theme_value = tk.StringVar()
        self.theme_value.set(default_ui_theme)

    def load_themes(self):
        default_ui_theme = self.theme_value.get()
        self.theme_value.set(utils.profile_get('APPLICATION_LOOK', default_ui_theme))
        self._apply_ui_theme(self.theme_value.get())

    def _register_ui_theme_as_tk_theme(self, name):
        total_settings = []
        total_images = {}
        temp_name = name
        while True:
            parent, settings, images = self._ui_themes[temp_name]
            total_settings.insert(0, settings)
            for img_name in images:
                total_images.setdefault(img_name, images[img_name])

            if parent is not None:
                temp_name = parent
            else:
                break

        assert temp_name in self._style.theme_names()
        self._style.theme_create(name, temp_name)
        self.MainFrame.GetNotebook().images.append(imageutils.load_image('img_close', 'tab-close.gif'))
        self.MainFrame.GetNotebook().images.append(imageutils.load_image('img_close_active', 'tab-close-active.gif'))
        for settings in total_settings:
            if callable(settings):
                settings = settings()
            if isinstance(settings, dict):
                self._style.theme_settings(name, settings)
            else:
                for subsettings in settings:
                    self._style.theme_settings(name, subsettings)

    def _apply_ui_theme(self, name):
        self._current_theme_name = name
        if name not in self._style.theme_names():
            self._register_ui_theme_as_tk_theme(name)
        self._style.theme_use(name)
        utils.profile_set('APPLICATION_LOOK', name)
        for setting in [
         'background',
         'foreground',
         'selectBackground',
         'selectForeground']:
            value = self._style.lookup('Listbox', setting)
            if value:
                self.option_add('*TCombobox*Listbox.' + setting, value)
                self.option_add('*Listbox.' + setting, value)

        text_opts = self._style.configure('Text')
        if text_opts:
            for key in text_opts:
                self.option_add('*Text.' + key, text_opts[key])

        for menu_data in self.Menubar._menus:
            menu = menu_data[2]
            menu.configure(misc.get_style_configuration('Menu'))

        self.UpdateFonts()

    def get_usable_ui_theme_names(self):
        return sorted([name for name in self._ui_themes if self._ui_themes[name][0] is not None])

    def InitThemeMenu(self):
        theme_names = self.get_usable_ui_theme_names()
        if len(theme_names):
            view_menu = self.Menubar.GetMenu(_('&View'))
            theme_menu = tkmenu.PopupMenu()
            view_menu.AppendMenu(constants.ID_VIEW_APPLICAITON_LOOK, _('&Application Look'), theme_menu)
            for name in theme_names:

                def apply_theme(name=name):
                    self._apply_ui_theme(name)

                self.AddMenuCommand(name, theme_menu, command_label=name, handler=apply_theme, kind=consts.RADIO_MENU_ITEM_KIND, variable=self.theme_value, value=name)

    def Feedback(self):
        fileutils.startfile('https://gitee.com/wekay/NovalIDE/issues')

    def GotoWebsite(self):
        fileutils.startfile(UserDataDb.HOST_SERVER_ADDR)

    def OnOptions(self):
        preference_dlg = preference.PreferenceDialog(self, selection=utils.profile_get('PrefereceOptionName', ''))
        preference_dlg.ShowModal()

    def ShowFullScreen(self):
        if not self.IsFullScreen:
            ui_utils.GetFullscreenDialog().Show()
            if utils.profile_get_int('HideMenubarFullScreen', False):
                self.ShowMenubar(False)
        else:
            ui_utils.GetFullscreenDialog().CloseDialog()

    def ShowMenubar(self, show=True):
        if show:
            if isinstance(self._menu_bar, tkmenu.ThemeMenuBar):
                self._menu_bar.grid(row=0, column=0, sticky='nsew')
            else:
                self.config(menu=self._menu_bar)
        else:
            if isinstance(self._menu_bar, tkmenu.ThemeMenuBar):
                self._menu_bar.grid_forget()
            else:
                self.config(menu='')
                self.update()

    def GetDefaultTextDocumentType(self):
        """
            默认新建文本文档类型
        """
        return syntax.SyntaxThemeManager().GetLexer(self.GetDefaultLangId()).GetDocTypeName()

    def GetDebugviewClass(self):
        return self._debugger_view_class

    def GetDebuggerClass(self):
        return self._debugger_class

    def GetDebugger(self):
        debugger = self.GetDebuggerClass()()
        current_project = self.MainFrame.GetProjectView(False).GetCurrentProject()
        debugger.SetCurrentProject(current_project)
        return debugger

    def GetProjectTemplateClassData(self):
        """
            返回项目实际的模板类,文档类,以及视图类
        """
        return (
         self.project_template_class, self.project_document_class, self.project_view_class)

    def _init_scaling(self):
        self._default_scaling_factor = self.tk.call('tk', 'scaling')
        if self._default_scaling_factor > 10:
            self._default_scaling_factor = 1.33
        scaling = utils.profile_get('UI_SCALING_FACTOR', 'default')
        if scaling in ('default', 'auto'):
            self._scaling_factor = self._default_scaling_factor
        else:
            self._scaling_factor = float(scaling)
        self.tk.call('tk', 'scaling', self._scaling_factor)
        font_scaling_mode = 'default'
        if utils.is_linux() and font_scaling_mode in ('default', 'extra') and scaling not in ('default',
                                                                                              'auto'):
            for name in tk_font.names():
                f = tk_font.nametofont(name)
                orig_size = f.cget('size')
                if orig_size < 0:
                    orig_size = -orig_size / self._default_scaling_factor
                scaled_size = round(orig_size * (self._scaling_factor / self._default_scaling_factor))
                if utils.is_py2():
                    scaled_size = int(scaled_size)
                f.configure(size=scaled_size)

    def scale_base(self, value):
        if isinstance(value, (int, float)):
            result = int(self._scaling_factor * value)
            if result == 0 and value > 0:
                return 1
            else:
                return result
        else:
            raise NotImplementedError('Only numeric dimensions supported at the moment')


class AppEvent(record.Record):

    def __init__(self, sequence, **kwargs):
        record.Record.__init__(self, **kwargs)
        self.sequence = sequence