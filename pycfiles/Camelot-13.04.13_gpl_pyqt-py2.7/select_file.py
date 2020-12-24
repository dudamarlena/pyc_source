# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action_steps/select_file.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from camelot.admin.action import ActionStep
from camelot.view.action_runner import hide_progress_dialog
from camelot.core.exception import CancelRequest

class SelectFile(ActionStep):
    """Select one or more files to open or to process.
    
    :param file_name_filter: Filter on the names of the files that can
        be selected, such as 'All files (*)'.  
        See :class:`QtGui.QFileDialog` for more documentation.
    
    .. attribute:: single
    
        defaults to :const:`True`, set to :const:`False` if selection
        of multiple files is allowed

    .. attribute:: existing
    
        defaults to :const:`True`, set to :const:`False` if non existing
        files are allowed (to save something)
        
    The :keyword:`yield` statement of :class:`SelectFile` returns a list
    of selected file names.  This list has only one element when single is
    set to :const:`True`.  Raises a 
    :class:`camelot.core.exception.CancelRequest` when no file was selected.
    
    .. image:: /_static/actionsteps/select_file.png
    
    This action step stores its last location into the :class:`QtCore.QSettings` 
    and uses it as the initial location the next time it is invoked.
    """

    def __init__(self, file_name_filter=''):
        self.file_name_filter = file_name_filter
        self.single = True
        self.existing = True

    def render(self, directory=None):
        """create the file dialog widget. this method is used to unit test
        the action step.

        :param directory: the directory in which to open the dialog, None to
            use the default
        """
        dialog = QtGui.QFileDialog(filter=self.file_name_filter, directory=None or '')
        if self.existing == False:
            file_mode = QtGui.QFileDialog.AnyFile
        elif self.single == True:
            file_mode = QtGui.QFileDialog.ExistingFile
        else:
            file_mode = QtGui.QFileDialog.ExistingFiles
        dialog.setFileMode(file_mode)
        return dialog

    def gui_run(self, gui_context):
        settings = QtCore.QSettings()
        directory = settings.value('datasource').toString()
        dialog = self.render(directory)
        with hide_progress_dialog(gui_context):
            if dialog.exec_() == QtGui.QDialog.Rejected:
                raise CancelRequest()
            file_names = [ unicode(fn) for fn in dialog.selectedFiles() ]
            if file_names:
                settings.setValue('datasource', QtCore.QVariant(file_names[0]))
            return file_names