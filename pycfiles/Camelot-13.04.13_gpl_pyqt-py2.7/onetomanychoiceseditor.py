# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/onetomanychoiceseditor.py
# Compiled at: 2013-04-11 17:47:52
from camelot.view.model_thread import post
from choiceseditor import ChoicesEditor
no_choice = [
 (None, '')]

class OneToManyChoicesEditor(ChoicesEditor):

    def __init__(self, parent, target=None, nullable=True, field_name='onetomanychoices', **kwargs):
        super(OneToManyChoicesEditor, self).__init__(parent, **kwargs)
        self.setObjectName(field_name)
        assert target != None
        self._target = target
        self._nullable = nullable
        post(self.get_choices, self.set_choices)
        return

    def get_choices(self):
        choices = [ (o, unicode(o)) for o in self._target.query.all() ]
        if self._nullable:
            return no_choice + choices
        else:
            return choices + no_choice

    def set_field_attributes(self, editable=True, **kwargs):
        """Makes sure choices are not reset when changing the
        field attributes"""
        self.setEnabled(editable != False)

    def set_value(self, value):
        post(lambda : value, super(OneToManyChoicesEditor, self).set_value)