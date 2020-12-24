# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/progress_dialog.py
# Compiled at: 2013-04-11 17:47:52
"""Functions and classes to use a progress dialog in combination with
a model thread"""
import logging
from camelot.core.utils import ugettext as _
from camelot.view.art import Icon
from PyQt4 import QtGui, QtCore
LOGGER = logging.getLogger('camelot.view.controls.progress_dialog')

class ProgressDialog(QtGui.QProgressDialog):
    """
A Progress Dialog to be used in combination with a post to the model thread:
    
to display a progress dialog until my_function has finished::

    d = ProgressDialog()
    post(my_function, d.finished, d.exception)
    d.exec_()
    
.. image:: /_static/controls/progress_dialog.png
    """
    progress_icon = Icon('tango/32x32/actions/appointment-new.png')

    def __init__(self, name, icon=progress_icon):
        QtGui.QProgressDialog.__init__(self, QtCore.QString(), _('Cancel'), 0, 0)
        label = QtGui.QLabel(unicode(name))
        self.setLabel(label)
        self.setWindowTitle(_('Please wait'))
        self.show()

    @QtCore.pyqtSlot(bool)
    @QtCore.pyqtSlot()
    def finished(self, success=True):
        self.close()

    @QtCore.pyqtSlot(object)
    def exception(self, exception_info):
        from camelot.view.controls.exception import model_thread_exception_message_box
        model_thread_exception_message_box(exception_info)
        self.finished(False)

    @QtCore.pyqtSlot(object)
    def exit(self, return_code):
        """Stop the application event loop, with the given return code"""
        LOGGER.info('exit application with code %s' % return_code)
        QtGui.QApplication.exit(int(return_code))