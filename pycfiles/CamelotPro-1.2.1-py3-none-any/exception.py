# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/exception.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = 'Functions and widget to represent exceptions to the user'
from PyQt4 import QtGui
from camelot.core.utils import ugettext as _
from camelot.core.exception import UserException

def register_exception(logger, text, exception):
    """Log an exception and return a serialized form of the exception with 
    exception information in a  user readable format, to be used when displaying 
    an exception message box.
    
    that serialized form can be fed to the model_thread_exception_message_box 
    function.
    
    :return: a tuple with exception information
    """
    if isinstance(exception, UserException):
        return (
         exception.title,
         exception.text,
         exception.icon,
         exception.resolution,
         exception.detail)
    else:
        logger.error(text, exc_info=exception)
        title = _('Exception')
        text = _('An unexpected event occurred')
        icon = None
        resolution = unicode(exception)[:1000]
        import traceback, cStringIO
        sio = cStringIO.StringIO()
        traceback.print_exc(file=sio)
        detail = sio.getvalue()
        sio.close()
        return (
         title, text, icon, resolution, detail)


class ExceptionDialog(QtGui.QMessageBox):
    """Dialog to display an exception to the user

    .. image:: /_static/controls/user_exception.png 
    """

    def __init__(self, exception_info):
        """Dialog to display a serialized exception, as returned
        by :func:`register_exception`

        :param exception_info: a tuple containing exception information
        """
        title, text, icon, resolution, detail = exception_info
        super(ExceptionDialog, self).__init__(QtGui.QMessageBox.Warning, unicode(title), unicode(text))
        self.setInformativeText(unicode(resolution or ''))
        self.setDetailedText(unicode(detail or ''))


def model_thread_exception_message_box(exception_info):
    """Display an exception that occurred in the model thread in a message box,
    use this function as the exception argument in the model thread's post function
    to represent the exception to the user
    
    :param exception_info: a tuple containing exception information
    """
    dialog = ExceptionDialog(exception_info)
    dialog.exec_()