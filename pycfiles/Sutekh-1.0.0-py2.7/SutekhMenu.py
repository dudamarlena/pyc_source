# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/SutekhMenu.py
# Compiled at: 2019-12-11 16:37:48
"""Base class for the menus"""
import gtk

class SutekhMenu(gtk.MenuBar):
    """Base class for Menus

       This provides useful methods for handling accelerators.
       """

    def __init__(self, oMainWindow):
        super(SutekhMenu, self).__init__()
        self._dMenuLabels = {}
        self._dMenus = {}
        self._oAccelGroup = gtk.AccelGroup()
        self._oMainWindow = oMainWindow
        self._bAccelActive = False

    def activate_accels(self):
        """Add the accelerator group for this menu from the main window"""
        if self._bAccelActive:
            return
        self._oMainWindow.add_accel_group(self._oAccelGroup)
        self._bAccelActive = True
        for oMenuLabel, sMarkup in self._dMenuLabels.iteritems():
            oMenuLabel.set_use_underline(True)
            oMenuLabel.set_label(sMarkup)

    def remove_accels(self):
        """Remove the accelerator group for this menu from the main window"""
        if not self._bAccelActive:
            return
        self._oMainWindow.remove_accel_group(self._oAccelGroup)
        self._bAccelActive = False
        for oMenuLabel in self._dMenuLabels:
            oMenuLabel.set_text(oMenuLabel.get_text())

    def _add_accel(self, oMenuItem, sAccelKey):
        """Parse a accelerator description & add it to the menu item"""
        iKeyVal, iMod = gtk.accelerator_parse(sAccelKey)
        if iKeyVal != 0:
            oMenuItem.add_accelerator('activate', self._oAccelGroup, iKeyVal, iMod, gtk.ACCEL_VISIBLE)

    def create_menu_item(self, sName, oMenu, fAction, sAccelKey=None):
        """Utiltiy function for creatng menu items.

           Create a menu item, connect it to fAction (if not None), and
           add an accelerator if specified."""
        oMenuItem = gtk.MenuItem(sName)
        if oMenu is not None:
            oMenu.add(oMenuItem)
        if fAction:
            oMenuItem.connect('activate', fAction)
        if sAccelKey:
            self._add_accel(oMenuItem, sAccelKey)
        return oMenuItem

    def create_check_menu_item(self, sName, oMenu, fAction, bState=False, sAccelKey=None):
        """Utiltiy function for creatng check menu items.

           Create a check menu item, connect it to fAction (if not None), and
           add an accelerator if specified."""
        oMenuItem = gtk.CheckMenuItem(sName)
        oMenu.add(oMenuItem)
        oMenuItem.set_inconsistent(False)
        oMenuItem.set_active(bState)
        if fAction:
            oMenuItem.connect('toggled', fAction)
        if sAccelKey:
            self._add_accel(oMenuItem, sAccelKey)
        return oMenuItem

    def create_menu_item_with_submenu(self, oTopLevelMenu, sName):
        """Create a MenuItem and a submenu, returning the menu_item"""
        oMenuItem = gtk.MenuItem(sName)
        oMenuLabel = oMenuItem.get_child()
        self._dMenuLabels[oMenuLabel] = oMenuLabel.get_label()
        sStrippedName = oMenuItem.get_child().get_text()
        oMenuLabel.set_text(sStrippedName)
        oMenu = gtk.Menu()
        self._dMenus[sStrippedName] = oMenu
        oMenuItem.set_submenu(oMenu)
        oTopLevelMenu.add(oMenuItem)
        return oMenuItem

    def create_submenu(self, oMenu, sName):
        """Create a submenu of oMenu, and add it to the menu dictionary,
           returning the submenu"""
        oMenuItem = self.create_menu_item_with_submenu(oMenu, sName)
        return oMenuItem.get_submenu()

    def add_plugins_to_menus(self, oPluginWindow):
        """Add the plugins for oPluginWindow to the current menus."""
        oMenuItem = self.create_menu_item_with_submenu(self, 'Other')
        oMenu = oMenuItem.get_submenu()
        for oPlugin in oPluginWindow.plugins:
            oPlugin.add_to_menu(self._dMenus, oMenu)

        if not oMenu.get_children():
            self.remove(oMenuItem)
            del self._dMenus['Other']
        else:
            self.sort_menu(oMenu)

    @staticmethod
    def sort_menu(oMenu):
        """Sort the entries of a sub-menu by the menu text"""

        def get_name(oWidget):
            """Get the text label from an menu item by descending the
               children"""
            if isinstance(oWidget, gtk.Label):
                return oWidget.get_text()
            else:
                if not hasattr(oWidget, 'get_children'):
                    return
                for oChild in oWidget.get_children():
                    sName = get_name(oChild)
                    if sName:
                        return sName

                return

        aItems = [ (get_name(x), x) for x in oMenu.get_children() ]
        aItems.sort()
        for iPos, (_sText, oItem) in enumerate(aItems):
            oMenu.reorder_child(oItem, iPos)