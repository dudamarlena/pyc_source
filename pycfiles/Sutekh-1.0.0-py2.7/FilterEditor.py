# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/FilterEditor.py
# Compiled at: 2019-12-11 16:37:48
"""Widget for editing filters."""
import gtk
from .FilterModelPanes import FilterModelPanes, add_accel_to_button

class FilterEditor(gtk.Alignment):
    """GTK component for editing Sutekh filter ASTs.

       Provides a graphical representation of the filter as nested boxes,
       which the user can extend or remove from.
       """

    def __init__(self, oAST, sFilterType, oParser, oFilterDialog):
        super(FilterEditor, self).__init__(xscale=1.0, yscale=1.0)
        self.__oParser = oParser
        self.__oFilterDialog = oFilterDialog
        self.__oPanes = FilterModelPanes(sFilterType, oFilterDialog)
        self.__sFilterType = sFilterType
        oNameLabel = gtk.Label('Filter name:')
        self.__oNameEntry = gtk.Entry()
        self.__oNameEntry.set_width_chars(30)
        oHelpButton = gtk.Button('Help')
        oHelpButton.connect('clicked', self.__show_help_dialog)
        add_accel_to_button(oHelpButton, 'F1', oFilterDialog.accel_group)
        oHBox = gtk.HBox(spacing=5)
        oHBox.pack_start(oNameLabel, expand=False)
        oHBox.pack_start(self.__oNameEntry, expand=False)
        oHBox.pack_end(oHelpButton, expand=False)
        self.__oVBox = gtk.VBox(spacing=5)
        self.__oVBox.pack_end(oHBox, expand=False)
        self.__oVBox.pack_end(gtk.HSeparator(), expand=False)
        self.__oVBox.pack_start(self.__oPanes, expand=True)
        self.add(self.__oVBox)
        self.replace_ast(oAST)

    def get_filter(self):
        """Get the actual filter for the current AST."""
        oAST = self.get_current_ast()
        if oAST is None:
            return
        else:
            return oAST.get_filter()

    def get_current_ast(self):
        """Get the current AST represented by the editor."""
        return self.__oPanes.get_ast_with_values()

    def get_current_text(self):
        """Get the current text of the filter for saving in the config
           file.

           We include any current set values for the filter when saving."""
        return self.__oPanes.get_text()

    def replace_ast(self, oAST):
        """Replace the current AST with a new one and update the GUI,
           preserving variable values if possible.

           Also used to setup the filter initially.
           """
        self.__oPanes.replace_ast(oAST)

    def set_name(self, sName):
        """Set the filter name."""
        self.__oNameEntry.set_text(sName)

    def get_name(self):
        """Get the filter name."""
        return self.__oNameEntry.get_text().strip()

    def connect_name_changed(self, fCallback):
        """Connect a callback to the name entry change signal."""
        self.__oNameEntry.connect('changed', fCallback)

    def __show_help_dialog(self, _oHelpButton):
        """Show a dialog window with the helptext from the filters."""
        oMainWindow = gtk.window_list_toplevels()[0]
        if self.__sFilterType == 'PhysicalCard':
            oMainWindow.show_card_filter_help()
        elif self.__sFilterType == 'PhysicalCardSet':
            oMainWindow.show_card_set_filter_help()
        else:
            raise RuntimeError('No help for unknown filter type %s' % self.__sFilterType)