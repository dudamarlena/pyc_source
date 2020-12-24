# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_theme.py
# Compiled at: 2012-07-29 09:43:20
"""
Provide an interface for creating icon themes for Editra. This will allow for
themes to be created, installed, and managed as plugins, which means that they
can be installed as single file instead of dozens of individual image files.

@summary: Editra's theme interface and implementation

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_theme.py 72247 2012-07-28 22:32:37Z CJP $'
__revision__ = '$Revision: 72247 $'
import os, wx, ed_glob, util, plugin
from profiler import Profile_Get, Profile_Set
import syntax.synglob as synglob
from syntax.syntax import SYNTAX_IDS

class ThemeI(plugin.Interface):
    """Interface for defining an icon theme in Editra
    When a icon theme is active Editra's ArtProvider will ask the active
    theme that implements this interface to give it a bitmap. The requests
    for bitmaps will be numerical ID values that come from ed_glob. These
    ID's are associated with different objects in the interface. The names
    are descriptive of the object they represent, for reference however
    see the implementation of the two main themes (Tango and Nuovo).

    @see: L{ed_glob}
    @see: L{syntax.synglob}

    """

    def GetName(self):
        """Return the name of this theme. This is used to identify the
        theme when the provider looks for resources based on user preferences

        @return: name string

        """
        pass

    def GetMenuBitmap(self, bmp_id):
        """Get the menu bitmap associated with the object id
        If this theme does not have a resource to provide for this
        object return a wx.NullBitmap.

        @return: 16x16 pixel bitmap

        """
        return wx.NullBitmap

    def GetFileBitmap(self, bmp_id):
        """Get the filetype bitmap associated with the object id, the
        valid object ids are defined in the module syntax.synglob and
        are used to request images for menu's and page tabs. The theme
        implimenting this interface should at least be able to
        provide an image for plain text files and return that for any
        unmapped types.

        If this theme does not have a resource to provide for this
        object return a wx.NullBitmap.

        @return: 16x16 pixel bitmap

        """
        return wx.NullBitmap

    def GetOtherBitmap(self, bmp_id):
        """Get the bitmap from the 'other' icon resources. Valid id's are
        identified by a mapping in the ART dictionary.
        
        If this theme does not have a resource to provide for this
        object return a wx.NullBitmap.

        @return: wx.Bitmap

        """
        return wx.NullBitmap

    def GetToolbarBitmap(self, bmp_id):
        """Get the toolbar bitmap associated with the object id. The
        toolbar icons must be returned as a 32x32 pixel bitmap any
        scaling that is needed will be handled by the art provider that
        requests the resource.

        If this theme does not have a resource to provide for this
        object return a wx.NullBitmap.

        @return: 32x32 pixel bitmap

        """
        return wx.NullBitmap


class BitmapProvider(plugin.Plugin):
    """Plugin that fetches requested icons from the current active theme.

    """
    observers = plugin.ExtensionPoint(ThemeI)

    def __GetCurrentProvider(self):
        """Gets the provider of the current theme resources
        @return: ThemeI object

        """
        theme = Profile_Get('ICONS', 'str', '')
        for prov in self.observers:
            if theme == prov.GetName():
                return prov

        if theme.lower() != 'default':
            Profile_Set('ICONS', 'Default')
        return

    def _GetTango(self, bmp_id, client):
        """Try to get the icon from the default tango theme"""
        theme = None
        bmp = wx.NullBitmap
        for prov in self.observers:
            if prov.GetName() == TangoTheme.name:
                theme = prov
                break
        else:
            return bmp

        if client == wx.ART_TOOLBAR:
            bmp = theme.GetToolbarBitmap(bmp_id)
        elif client == wx.ART_MENU:
            bmp = theme.GetMenuBitmap(bmp_id)
        elif client == wx.ART_OTHER:
            bmp = theme.GetOtherBitmap(bmp_id)
        return bmp

    def GetThemes(self):
        """Gets a list of the installed and activated themes
        @return: list of strings

        """
        return [ name.GetName() for name in self.observers ]

    def GetBitmap(self, bmp_id, client):
        """Gets a 16x16 or 32x32 pixel bitmap depending on client value.
        May return a NullBitmap if no suitable bitmap can be
        found.

        @param bmp_id: id of bitmap to lookup
        @param client: wxART_MENU, wxART_TOOLBAR
        @see: L{ed_glob}

        """
        prov = self.__GetCurrentProvider()
        if prov is not None:
            if client == wx.ART_MENU:
                bmp = prov.GetMenuBitmap(bmp_id)
            elif client == wx.ART_OTHER:
                if hasattr(prov, 'GetOtherBitmap'):
                    bmp = prov.GetOtherBitmap(bmp_id)
                else:
                    bmp = wx.NullBitmap
            else:
                bmp = prov.GetToolbarBitmap(bmp_id)
            if bmp.IsOk():
                return bmp
        bmp = self._GetTango(bmp_id, client)
        if bmp.IsOk():
            return bmp
        else:
            return wx.NullBitmap


ART = {ed_glob.ID_ABOUT: 'about.png', ed_glob.ID_ADD: 'add.png', 
   ed_glob.ID_ADD_BM: 'bmark_add.png', 
   ed_glob.ID_ADVANCED: 'advanced.png', 
   ed_glob.ID_BACKWARD: 'backward.png', 
   ed_glob.ID_BIN_FILE: 'bin_file.png', 
   ed_glob.ID_CDROM: 'cdrom.png', 
   ed_glob.ID_CONTACT: 'mail.png', 
   ed_glob.ID_COPY: 'copy.png', 
   ed_glob.ID_COMPUTER: 'computer.png', 
   ed_glob.ID_CUT: 'cut.png', 
   ed_glob.ID_DELETE: 'delete.png', 
   ed_glob.ID_DELETE_ALL: 'delete_all.png', 
   ed_glob.ID_DOCPROP: 'doc_props.png', 
   ed_glob.ID_DOCUMENTATION: 'docs.png', 
   ed_glob.ID_DOWN: 'down.png', 
   ed_glob.ID_EXIT: 'quit.png', 
   ed_glob.ID_FILE: 'file.png', 
   ed_glob.ID_FIND: 'find.png', 
   ed_glob.ID_FIND_REPLACE: 'findr.png', 
   ed_glob.ID_FIND_RESULTS: 'find.png', 
   ed_glob.ID_FLOPPY: 'floppy.png', 
   ed_glob.ID_FOLDER: 'folder.png', 
   ed_glob.ID_FONT: 'font.png', 
   ed_glob.ID_FORWARD: 'forward.png', 
   ed_glob.ID_HARDDISK: 'harddisk.png', 
   ed_glob.ID_HOMEPAGE: 'web.png', 
   ed_glob.ID_HTML_GEN: 'html_gen.png', 
   ed_glob.ID_INDENT: 'indent.png', 
   ed_glob.ID_LOGGER: 'log.png', 
   ed_glob.ID_NEW: 'new.png', 
   ed_glob.ID_NEW_FOLDER: 'newfolder.png', 
   ed_glob.ID_NEW_WINDOW: 'newwin.png', 
   ed_glob.ID_NEXT_MARK: 'bmark_next.png', 
   ed_glob.ID_NEXT_POS: 'forward.png', 
   ed_glob.ID_OPEN: 'open.png', 
   ed_glob.ID_PACKAGE: 'package.png', 
   ed_glob.ID_PASTE: 'paste.png', 
   ed_glob.ID_PLUGMGR: 'plugin.png', 
   ed_glob.ID_PRE_MARK: 'bmark_pre.png', 
   ed_glob.ID_PRE_POS: 'backward.png', 
   ed_glob.ID_PREF: 'pref.png', 
   ed_glob.ID_PRINT: 'print.png', 
   ed_glob.ID_PRINT_PRE: 'printpre.png', 
   ed_glob.ID_PYSHELL: 'pyshell.png', 
   ed_glob.ID_REDO: 'redo.png', 
   ed_glob.ID_REFRESH: 'refresh.png', 
   ed_glob.ID_REMOVE: 'remove.png', 
   ed_glob.ID_RTF_GEN: 'rtf_gen.png', 
   ed_glob.ID_SAVE: 'save.png', 
   ed_glob.ID_SAVEALL: 'saveall.png', 
   ed_glob.ID_SAVEAS: 'saveas.png', 
   ed_glob.ID_SELECTALL: 'selectall.png', 
   ed_glob.ID_STOP: 'stop.png', 
   ed_glob.ID_STYLE_EDIT: 'style_edit.png', 
   ed_glob.ID_TEX_GEN: 'tex_gen.png', 
   ed_glob.ID_THEME: 'theme.png', 
   ed_glob.ID_UNDO: 'undo.png', 
   ed_glob.ID_UNINDENT: 'outdent.png', 
   ed_glob.ID_UP: 'up.png', 
   ed_glob.ID_USB: 'usb.png', 
   ed_glob.ID_WEB: 'web.png', 
   ed_glob.ID_ZOOM_IN: 'zoomi.png', 
   ed_glob.ID_ZOOM_OUT: 'zoomo.png', 
   ed_glob.ID_ZOOM_NORMAL: 'zoomd.png', 
   ed_glob.ID_READONLY: 'readonly.png', 
   ed_glob.ID_CLASS_TYPE: 'class.png', 
   ed_glob.ID_FUNCT_TYPE: 'function.png', 
   ed_glob.ID_ELEM_TYPE: 'element.png', 
   ed_glob.ID_VARIABLE_TYPE: 'variable.png', 
   ed_glob.ID_ATTR_TYPE: 'attribute.png', 
   ed_glob.ID_PROPERTY_TYPE: 'property.png', 
   ed_glob.ID_METHOD_TYPE: 'method.png'}
MIME_ART = {synglob.ID_LANG_ADA: 'ada.png', synglob.ID_LANG_BASH: 'shell.png', 
   synglob.ID_LANG_BOO: 'boo.png', 
   synglob.ID_LANG_BOURNE: 'shell.png', 
   synglob.ID_LANG_C: 'c.png', 
   synglob.ID_LANG_CPP: 'cpp.png', 
   synglob.ID_LANG_CSH: 'shell.png', 
   synglob.ID_LANG_CSS: 'css.png', 
   synglob.ID_LANG_DIFF: 'diff.png', 
   synglob.ID_LANG_HTML: 'html.png', 
   synglob.ID_LANG_JAVA: 'java.png', 
   synglob.ID_LANG_KSH: 'shell.png', 
   synglob.ID_LANG_LATEX: 'tex.png', 
   synglob.ID_LANG_MAKE: 'makefile.png', 
   synglob.ID_LANG_PASCAL: 'pascal.png', 
   synglob.ID_LANG_PERL: 'perl.png', 
   synglob.ID_LANG_PHP: 'php.png', 
   synglob.ID_LANG_PS: 'postscript.png', 
   synglob.ID_LANG_PYTHON: 'python.png', 
   synglob.ID_LANG_RUBY: 'ruby.png', 
   synglob.ID_LANG_TCL: 'tcl.png', 
   synglob.ID_LANG_TEX: 'tex.png', 
   synglob.ID_LANG_TXT: 'text.png', 
   synglob.ID_LANG_XML: 'xml.png'}

class TangoTheme(plugin.Plugin):
    """Represents the Tango Icon theme for Editra"""
    plugin.Implements(ThemeI)
    name = 'Tango'

    def __GetArtPath(self, client, mime=False):
        """Gets the path of the resource directory to get
        the bitmaps from.
        @param client: wx.ART_MENU/wx.ART_TOOLBAR
        @keyword mime: is this a filetype icon lookup
        @return: path of art resource
        @rtype: string

        """
        clients = {wx.ART_MENU: 'menu', wx.ART_TOOLBAR: 'toolbar', 
           wx.ART_OTHER: 'other'}
        if ed_glob.CONFIG['THEME_DIR'] == '':
            theme = util.ResolvConfigDir(os.path.join('pixmaps', 'theme'))
            ed_glob.CONFIG['THEME_DIR'] = theme
        if mime:
            path = os.path.join(ed_glob.CONFIG['THEME_DIR'], self.GetName(), 'mime')
        else:
            path = os.path.join(ed_glob.CONFIG['THEME_DIR'], self.GetName(), clients.get(client, 'menu'))
        path += os.sep
        if os.path.exists(path):
            return path
        else:
            return
            return

    def GetName(self):
        """Get the name of this theme
        @return: string

        """
        return TangoTheme.name

    def GetMenuBitmap(self, bmp_id):
        """Get a menu bitmap
        @param bmp_id: Id of bitmap to look for

        """
        if bmp_id in ART:
            path = self.__GetArtPath(wx.ART_MENU, mime=False)
            if path is not None:
                path = path + ART[bmp_id]
                if os.path.exists(path):
                    return wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        else:
            return self.GetFileBitmap(bmp_id)
        return wx.NullBitmap

    def GetFileBitmap(self, bmp_id):
        """Get a mime type bitmap from the theme
        @param bmp_id: Id of filetype bitmap to look up
        @see: L{syntax.synglob}

        """
        path = self.__GetArtPath(wx.ART_MENU, mime=True)
        if path is not None and bmp_id in SYNTAX_IDS:
            if bmp_id in MIME_ART:
                req = path + MIME_ART[bmp_id]
                if os.path.exists(req):
                    return wx.Bitmap(req, wx.BITMAP_TYPE_PNG)
            bkup = path + MIME_ART[synglob.ID_LANG_TXT]
            if os.path.exists(bkup):
                return wx.Bitmap(bkup, wx.BITMAP_TYPE_PNG)
        return wx.NullBitmap

    def GetOtherBitmap(self, bmp_id):
        """Get a other catagory bitmap.
        @param bmp_id: Id of art resource

        """
        if bmp_id in ART:
            path = self.__GetArtPath(wx.ART_OTHER, mime=False)
            if path is not None:
                path = path + ART[bmp_id]
                if os.path.exists(path):
                    return wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        return wx.NullBitmap

    def GetToolbarBitmap(self, bmp_id):
        """Get a toolbar bitmap
        @param bmp_id: Id of bitmap to look for
        @return: wx.NullBitmap or a 32x32 bitmap

        """
        if bmp_id in ART:
            path = self.__GetArtPath(wx.ART_TOOLBAR, mime=False)
            if path is not None:
                path = path + ART[bmp_id]
                if os.path.exists(path):
                    return wx.Bitmap(path, wx.BITMAP_TYPE_PNG)
        return wx.NullBitmap