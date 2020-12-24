# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/BasicFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Base class for Sutekh Frames"""
import gtk, gobject
from .MessageBus import MessageBus, DATABASE_MSG

class BasicFrame(gtk.Frame):
    """The basic, blank frame for sutekh.

       Provides a default frame, and drag-n-drop handlind for
       sawpping the frames. Also provides gtkrc handling for
       setting the active hint.
       """
    aDragTargets = [
     (
      'STRING', gtk.TARGET_SAME_APP, 0),
     (
      'text/plain', gtk.TARGET_SAME_APP, 0)]
    _cModelType = None

    def __init__(self, oMainWindow):
        super(BasicFrame, self).__init__()
        self._oMainWindow = oMainWindow
        self._aPlugins = []
        self.set_name('blank frame')
        self._iId = 0
        self._oTitle = gtk.EventBox()
        self._oTitleLabel = gtk.Label('Blank Frame')
        self._oTitleLabel.set_name('frame_title')
        self._oTitle.add(self._oTitleLabel)
        self._oTitle.set_name('frame_title')
        self._oView = gtk.TextView()
        self._oView.set_editable(False)
        self._oView.set_cursor_visible(False)
        self._bNeedReload = False
        self._oTitle.drag_source_set(gtk.gdk.BUTTON1_MASK | gtk.gdk.BUTTON3_MASK, self.aDragTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        self._oTitle.drag_dest_set(gtk.DEST_DEFAULT_ALL, self.aDragTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        self._oTitle.connect('drag-data-received', self.drag_drop_handler)
        self._oTitle.connect('drag-data-get', self.create_drag_data)
        self._oTitle.connect('button-press-event', self.minimize_to_toolbar)
        self._oTitle.connect_after('drag_begin', self.make_drag_icon)
        self.set_drag_handler(self._oView)
        self.set_drop_handler(self._oView)
        self.set_unique_id()

    title = property(fget=lambda self: self._oTitleLabel.get_text(), doc='Frame Title')
    name = property(fget=lambda self: self._oTitleLabel.get_text(), doc='Frame Name')
    type = property(fget=lambda self: 'Blank Frame', doc='Frame Type')
    view = property(fget=lambda self: self._oView, doc='Associated View Object')
    menu = property(fget=lambda self: None, doc="Frame's menu")
    plugins = property(fget=lambda self: self._aPlugins, doc='Plugins enabled for this frame.')
    pane_id = property(fget=lambda self: self._iId, doc='ID number for this pane (should be unique)')
    config_frame_id = property(fget=lambda self: 'pane%s' % (self._iId,), doc='Config frame id for this pane')

    def set_unique_id(self):
        """Set a unique id for this pane"""
        self._iId = max(self._oMainWindow.get_pane_ids() + [0]) + 1

    def init_plugins(self):
        """Loop through the plugins, and enable those appropriate for us."""
        oPluginMgr = self._oMainWindow.plugin_manager
        for cPlugin in oPluginMgr.get_plugins_for(self._cModelType):
            self._aPlugins.append(cPlugin(self._oController.view, self._oController.view.get_model(), self._cModelType))

    def set_title(self, sTitle):
        """Set the title of the pane to sTitle"""
        self._oTitleLabel.set_markup(gobject.markup_escape_text(sTitle))

    def set_id(self, iNewId):
        """Set the id of the pane to the correct value"""
        self._iId = iNewId

    def set_drop_handler(self, oWidget):
        """Setup the frame drop handler on the widget"""
        oWidget.drag_dest_set(gtk.DEST_DEFAULT_ALL, self.aDragTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        oWidget.connect('drag-data-received', self.drag_drop_handler)
        oWidget.connect('drag-motion', self.drag_motion)

    def set_drag_handler(self, oWidget):
        """Enable dragging of the frame via given widget"""
        oWidget.drag_source_set(gtk.gdk.BUTTON1_MASK | gtk.gdk.BUTTON3_MASK, self.aDragTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        oWidget.connect('drag-data-get', self.create_drag_data)
        oWidget.connect_after('drag_begin', self.make_drag_icon)

    def set_focus_handler(self, oFunc):
        """Set the button press handler for the frame"""
        self.connect('button-press-event', self.call_focus, oFunc)
        self.view.connect('button-press-event', self.call_focus, oFunc)
        self.view.connect('focus-in-event', oFunc, self)

    def do_swap(self, aData):
        """Swap this pane with the relevant pane"""
        oOtherFrame = self._oMainWindow.find_pane_by_id(int(aData[1]))
        if oOtherFrame:
            self._oMainWindow.swap_frames(self, oOtherFrame)
            return True
        return False

    def do_dragged_card_set(self, aData):
        """Replace this pane with the relevant card set"""
        if self.is_card_set(aData[1]):
            return False
        self._oMainWindow.replace_with_physical_card_set(aData[1], self)
        return True

    def is_card_set(self, _sSetName):
        """Returns true if we're a copy of the given card set"""
        return False

    def get_menu_name(self):
        """Return the key into the menu dictionary in the main window"""
        return

    def frame_setup(self):
        """Hook called when the frame is added to the window.

           Used for subscribing to signals and so forth."""
        MessageBus.subscribe(DATABASE_MSG, 'update_to_new_db', self.update_to_new_db)

    def cleanup(self, _bQuit=False):
        """Hook for cleanup actions when the frame is removed."""
        MessageBus.unsubscribe(DATABASE_MSG, 'update_to_new_db', self.update_to_new_db)
        for oPlugin in self._aPlugins:
            oPlugin.cleanup()

        self._aPlugins = []
        if self.menu and hasattr(self.menu, 'cleanup'):
            self.menu.cleanup()

    def reload(self):
        """Reload frame contents"""
        pass

    def do_queued_reload(self):
        """Do a deferred reload if one was set earlier"""
        self._bNeedReload = False

    def queue_reload(self):
        """Queue a reload for later - needed so reloads can happen after
           database update signals."""
        self._bNeedReload = True
        self._oMainWindow.queue_reload()

    def update_to_new_db(self):
        """Re-associate internal data against the database.

           Needed for re-reading WW cardlists and such.
           By default, just reload.
           """
        self.reload()

    def close_frame(self):
        """Close the frame"""
        self._oMainWindow.config_file.clear_frame_profile(self.config_frame_id)
        self._oMainWindow.remove_frame(self)
        self.destroy()

    def add_parts(self):
        """Add the basic widgets (title, & placeholder) to the frame."""
        oMbox = gtk.VBox(False, 2)
        oMbox.pack_start(self._oTitle, False, False)
        oMbox.pack_start(self._oView, True, True)
        self.add(oMbox)
        self.show_all()

    def set_focussed_title(self):
        """Set the title to the correct style when focussed."""
        oCurStyle = self._oTitleLabel.rc_get_style()
        self._oTitleLabel.set_name('selected_title')
        oDefaultSutekhStyle = gtk.rc_get_style_by_paths(self._oTitleLabel.get_settings(), self.path() + '.', self.class_path(), self._oTitleLabel)
        oSpecificStyle = self._oTitleLabel.rc_get_style()
        if oSpecificStyle == oDefaultSutekhStyle or oDefaultSutekhStyle is None:
            oMap = self._oTitleLabel.get_colormap()
            sColour = 'purple'
            if oMap.alloc_color(sColour).pixel == oCurStyle.fg[gtk.STATE_NORMAL].pixel:
                sColour = 'green'
            sStyleInfo = '\n            style "internal_sutekh_hlstyle" {\n                fg[NORMAL] = "%(colour)s"\n                }\n            widget "%(path)s" style "internal_sutekh_hlstyle"\n            ' % {'colour': sColour, 'path': self._oTitleLabel.path()}
            gtk.rc_parse_string(sStyleInfo)
        self._oTitle.set_name('selected_title')
        return

    def set_unfocussed_title(self):
        """Set the title back to the default, unfocussed style."""
        self._oTitleLabel.set_name('frame_title')
        self._oTitle.set_name('frame_title')

    def close_menu_item(self, _oMenuWidget):
        """Handle close requests from the menu."""
        self.close_frame()

    def call_focus(self, _oWidget, oEvent, oFocusFunc):
        """Call MultiPaneWindow focus handler for button events"""
        oFocusFunc(self, oEvent, self)
        return False

    def drag_drop_handler(self, _oWindow, oDragContext, _iXPos, _iYPos, oSelectionData, _oInfo, oTime):
        """Handle panes being dragged onto this one.

           Allows panes to be sapped by dragging 'n dropping."""
        bDragRes = True
        if not oSelectionData and oSelectionData.format != 8:
            bDragRes = False
        else:
            aData = oSelectionData.data.splitlines()
            if aData[0] == 'Basic Pane:':
                if not self.do_swap(aData):
                    bDragRes = False
            elif aData[0] == 'Card Set:':
                if not self.do_dragged_card_set(aData):
                    bDragRes = False
            else:
                bDragRes = False
        oDragContext.finish(bDragRes, False, oTime)

    def create_drag_data(self, _oBtn, _oContext, oSelectionData, _oInfo, _oTime):
        """Fill in the needed data for drag-n-drop code"""
        sData = 'Basic Pane:\n%s' % self.pane_id
        oSelectionData.set(oSelectionData.target, 8, sData)

    def drag_motion(self, _oWidget, oDrag_context, _iXPos, _iYPos, _oTimestamp):
        """Show proper icon during drag-n-drop actions."""
        if 'STRING' in oDrag_context.targets:
            oDrag_context.drag_status(gtk.gdk.ACTION_COPY)
            return True
        return False

    def minimize_to_toolbar(self, _oWidget, oEvent):
        """Minimize the frame to the toolbar on double-click."""
        if oEvent.type == gtk.gdk._2BUTTON_PRESS:
            self._oMainWindow.minimize_to_toolbar(self)

    def make_drag_icon(self, oWidget, _oDragContext):
        """Create an icon for dragging the pane from the titlebar"""
        oDrawable = self._oTitleLabel.get_snapshot(None)
        oWidget.drag_source_set_icon(oDrawable.get_colormap(), oDrawable)
        return