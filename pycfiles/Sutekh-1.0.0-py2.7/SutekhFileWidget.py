# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/SutekhFileWidget.py
# Compiled at: 2019-12-11 16:37:48
"""FileChooserWidget and FileChooserDialog wrapper for Sutekh

   Provides base class for the file widgets and dialogs used in Sutekh -
   ensures set_name is called consistently, and updates the global working
   directory as appropriate
   """
import gtk

def _changed_dir(oFileChooser, oParentWin):
    """Update parent's working dir when the folder changes."""
    if oFileChooser.get_mapped():
        oParentWin.set_working_dir(oFileChooser.get_current_folder())


def add_filter(oFileChooser, sFilterName, aFilterPatterns):
    """Add  filter to the widget, using the list of patterns in
       aFilterPatterns"""
    oFilter = gtk.FileFilter()
    oFilter.set_name(sFilterName)
    for sPattern in aFilterPatterns:
        oFilter.add_pattern(sPattern)

    oFileChooser.add_filter(oFilter)
    oFileChooser.set_filter(oFilter)
    return oFilter


def _mapped(oFileWidget, oParent):
    """Update the dialogs working dir when the widget is shown.

       We need this since the working dir will often change between
       button/dialog creation, and the dialog being popped up.
       """
    sWorkingDir = oParent.get_working_dir()
    if sWorkingDir:
        oFileWidget.set_current_folder(sWorkingDir)


class SutekhFileDialog(gtk.FileChooserDialog):
    """Wrapper for the gtk.FileChooseDialog which updates the
       working dir of Sutekh."""

    def __init__(self, oParent, sTitle, oAction=gtk.FILE_CHOOSER_ACTION_OPEN, oButtons=None):
        super(SutekhFileDialog, self).__init__(sTitle, oParent, oAction, oButtons)
        self.set_name('Sutekh.dialog')
        self.connect('current-folder-changed', _changed_dir, oParent)
        self.connect('show', _mapped, oParent)
        self._oAllFilter = add_filter(self, 'All Files', ['*'])

    def add_filter_with_pattern(self, sName, aFilterPatterns):
        """Add a filter named sName to this widget, using the patterns
           in aFilterPatterns."""
        return add_filter(self, sName, aFilterPatterns)

    def default_filter(self):
        """Set the filter to be the default all files filter"""
        self.set_filter(self._oAllFilter)


class SutekhFileWidget(gtk.FileChooserWidget):
    """Wrapper for the gtk.FileChooseWidget which updates the
       working dir of Sutekh."""

    def __init__(self, oParent, oAction=gtk.FILE_CHOOSER_ACTION_OPEN):
        super(SutekhFileWidget, self).__init__(oAction)
        sWorkingDir = oParent.get_working_dir()
        if sWorkingDir:
            self.set_current_folder(sWorkingDir)
        self.connect('current-folder-changed', _changed_dir, oParent)
        self.connect('show', _mapped, oParent)
        self._oAllFilter = add_filter(self, 'All Files', ['*'])

    def add_filter_with_pattern(self, sName, aFilterPatterns):
        """Add a filter named sName to this widget, using the patterns
           in aFilterPatterns."""
        add_filter(self, sName, aFilterPatterns)

    def default_filter(self):
        """Set the filter to be the default all files filter"""
        self.set_filter(self._oAllFilter)


class SutekhFileButton(gtk.FileChooserButton):
    """Wrapper class for gtk.FileChooserButton which updates the
       working directory."""

    def __init__(self, oParent, sTitle):
        self.oDialog = SutekhFileDialog(oParent, sTitle, oButtons=(gtk.STOCK_OK, gtk.RESPONSE_OK,
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        super(SutekhFileButton, self).__init__(self.oDialog)
        sWorkingDir = oParent.get_working_dir()
        if sWorkingDir:
            self.set_current_folder(sWorkingDir)

    def add_filter_with_pattern(self, sName, aFilterPatterns):
        """Add a filter named sName to this widget, using the patterns
           in aFilterPatterns."""
        add_filter(self.oDialog, sName, aFilterPatterns)

    def default_filter(self):
        """Set the filter to be the default all files filter"""
        self.oDialog.default_filter()


class SimpleFileDialog(SutekhFileDialog):
    """A simple file dialog, which just returns the file name"""

    def __init__(self, oParent, sTitle, oAction):
        super(SimpleFileDialog, self).__init__(oParent, sTitle, oAction, (
         gtk.STOCK_OK, gtk.RESPONSE_OK,
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        self.connect('response', self.button_response)
        self.set_local_only(True)
        self.set_select_multiple(False)
        self.sName = None
        return

    def button_response(self, _oWidget, iResponse):
        """Handle button press events"""
        if iResponse == gtk.RESPONSE_OK:
            self.sName = self.get_filename()
        self.destroy()

    def get_name(self):
        """Return the name to the caller."""
        return self.sName


class ImportDialog(SimpleFileDialog):
    """Prompt the user for a file name to import"""

    def __init__(self, sTitle, oParent):
        super(ImportDialog, self).__init__(oParent, sTitle, gtk.FILE_CHOOSER_ACTION_OPEN)


class ExportDialog(SimpleFileDialog):
    """Prompt the user for a filename to export to"""

    def __init__(self, sTitle, oParent, sDefaultFileName=None):
        super(ExportDialog, self).__init__(oParent, sTitle, gtk.FILE_CHOOSER_ACTION_SAVE)
        self.set_do_overwrite_confirmation(True)
        if sDefaultFileName:
            self.set_current_name(sDefaultFileName)


class ZipFileDialog(SimpleFileDialog):
    """Prompt the user for a zip file name"""

    def __init__(self, oParent, sTitle, oAction):
        super(ZipFileDialog, self).__init__(oParent, sTitle, oAction)
        self.add_filter_with_pattern('Zip Files', ['*.zip', '*.ZIP'])