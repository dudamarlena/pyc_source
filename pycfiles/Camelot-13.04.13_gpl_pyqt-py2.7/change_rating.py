# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/change_rating.py
# Compiled at: 2013-04-11 17:47:52
"""Example code for attaching actions to camelot views
"""
from camelot.admin.action import Action, Mode
from camelot.admin.object_admin import ObjectAdmin
from camelot.view.action_steps import ChangeObject, FlushSession, UpdateProgress
from camelot.view.controls import delegates
from camelot.core.utils import ugettext_lazy as _

class Options(object):
    """A python object in which we store the change in rating
    """

    def __init__(self):
        self.only_selected = True
        self.change = 1

    class Admin(ObjectAdmin):
        verbose_name = _('Change rating options')
        form_display = ['change', 'only_selected']
        form_size = (100, 100)
        field_attributes = {'only_selected': {'delegate': delegates.BoolDelegate, 'editable': True}, 
           'change': {'delegate': delegates.IntegerDelegate, 'editable': True}}


class ChangeRatingAction(Action):
    """Action to print a list of movies"""
    verbose_name = _('Change Rating')

    def model_run(self, model_context):
        options = Options()
        yield ChangeObject(options)
        if options.only_selected:
            iterator = model_context.get_selection()
        else:
            iterator = model_context.get_collection()
        for movie in iterator:
            yield UpdateProgress(text='Change %s' % unicode(movie))
            movie.rating = min(5, max(0, (movie.rating or 0) + options.change))

        yield FlushSession(model_context.session)