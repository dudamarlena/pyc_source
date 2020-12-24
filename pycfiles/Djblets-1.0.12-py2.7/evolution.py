# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/db/evolution.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django_evolution.mutations import BaseMutation

class FakeChangeFieldType(BaseMutation):
    """
    Changes the type of the field to a similar type.
    This is intended only when the new type is really a version of the
    old type, such as a subclass of that Field object. The two fields
    should be compatible or there could be migration issues.
    """

    def __init__(self, model_name, field_name, new_type):
        self.model_name = model_name
        self.field_name = field_name
        self.new_type = new_type

    def __repr__(self):
        return b"FakeChangeFieldType('%s', '%s', '%s')" % (
         self.model_name, self.field_name, self.new_type)

    def simulate(self, app_label, proj_sig):
        app_sig = proj_sig[app_label]
        model_sig = app_sig[self.model_name]
        field_dict = model_sig[b'fields']
        field_sig = field_dict[self.field_name]
        field_sig[b'field_type'] = self.new_type

    def mutate(self, app_label, proj_sig):
        self.simulate(app_label, proj_sig)
        return b''