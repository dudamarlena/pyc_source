# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/forms/DeleteEventForm.py
# Compiled at: 2016-04-19 10:47:47
"""
.. module:: DeleteEventForm
    :synopsis: A form for deleting an event or event series.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""
from flask.ext.wtf import Form
from wtforms import BooleanField

class DeleteEventForm(Form):
    """A form for deleting an event.

    :ivar delete_all: :class:`wtforms.fields.BooleanField` - True if the event
        is recurring and all events in the series should be deleted.
    """
    delete_all = BooleanField('Delete All', default=False)