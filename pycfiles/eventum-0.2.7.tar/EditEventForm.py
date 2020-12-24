# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/forms/EditEventForm.py
# Compiled at: 2016-04-19 10:47:47
"""
.. module:: EditEventForm
    :synopsis: A form for editing an :class:`~app.models.Event`.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""
from eventum.forms import CreateEventForm
from eventum.forms.CreateEventForm import INVALID_SLUG
from eventum.forms.validators import UniqueEditEvent
from wtforms import StringField, BooleanField
from wtforms.validators import Regexp
from eventum.lib.regex import Regex

def EditEventForm(original, *args, **kwargs):
    """ Creates an edit form.

    Uses a function closure to pass ``original`` into the UniqueEditEvent
    validator for EditEventForm.slug

    :param Event original: the event being edited
    """

    class EditEventForm(CreateEventForm):
        """A form for editing an :class:`~app.models.Event`.

        This inherits from :class:`CreateEventForm`. Edited slugs are checked
        for uniqueness, while unedited slugs are not (they should appear once
        in the database).

        :ivar update_all: :class:`wtforms.fields.BooleanField` - True if all
            events should be modified in this update.
        :ivar slug: :class:`wtforms.fields.StringField` - Unique url fragment
            for the blog post. It may only contain letters, numbers, and dashes
            (``-``).
        """
        update_all = BooleanField('Update all', default=False)
        slug = StringField('Slug', [
         Regexp(Regex.SLUG_REGEX, message=INVALID_SLUG),
         UniqueEditEvent(original)])

    return EditEventForm(*args, **kwargs)