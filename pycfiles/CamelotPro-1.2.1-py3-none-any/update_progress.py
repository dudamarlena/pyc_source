# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action_steps/update_progress.py
# Compiled at: 2013-04-11 17:47:52
from camelot.admin.action import ActionStep
from camelot.core.exception import CancelRequest

class UpdateProgress(ActionStep):
    """
Inform the user about the progress the application is making
while executing an action.  This ActionStep is not blocking.  So it can
be used inside transactions and will result in a minimum of delay when
yielded.  Each time an object is yielded, the progress dialog will be
updated.

.. image:: /_static/controls/progress_dialog.png

:param value: the current step
:param maximum: the maximum number of steps that will be executed. set it
    to 0 to display a busy indicator instead of a progres bar
:param text: the text to be displayed inside the progres bar
:param detail: the text to be displayed below the progres bar, this text is
    appended to the text already there
:param clear_details: clear the details text already there before putting 
    the new detail text.
"""
    blocking = False

    def __init__(self, value=0, maximum=0, text=None, detail=None, clear_details=False):
        super(UpdateProgress, self).__init__()
        self._value = value
        self._maximum = maximum
        self._text = text
        self._detail = detail
        self._clear_details = clear_details

    def __unicode__(self):
        return ('Update Progress {0._value:03d}/{0._maximum:03d} {0._text}').format(self)

    def gui_run(self, gui_context):
        """This method will update the progress dialog, if such dialog exists
        within the GuiContext
        
        :param gui_context: a :class:`camelot.admin.action.GuiContext` instance
        """
        progress_dialog = gui_context.progress_dialog
        if progress_dialog:
            if progress_dialog.wasCanceled():
                progress_dialog.reset()
                raise CancelRequest()
            progress_dialog.setMaximum(self._maximum)
            progress_dialog.setValue(self._value)
            if self._text != None:
                progress_dialog.setLabelText(unicode(self._text))
        return