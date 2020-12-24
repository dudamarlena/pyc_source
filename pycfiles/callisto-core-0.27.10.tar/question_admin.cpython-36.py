# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/wizard_builder/admin/question_admin.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 406 bytes
import nested_admin
from django import forms
from .. import fields
from .inlines import ChoiceInline

class QuestionAdminForm(forms.ModelForm):
    type = forms.ChoiceField(choices=(fields.get_field_options()))


class FormQuestionAdmin(nested_admin.NestedModelAdmin):
    form = QuestionAdminForm
    search_fields = ['short_str', 'type', 'page']
    list_filter = ['sites']
    inlines = [ChoiceInline]