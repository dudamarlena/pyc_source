# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpwrussell/Checkout/OME/webtagging/tagsearch/omero_webtagging_tagsearch/forms.py
# Compiled at: 2020-01-12 13:54:38
# Size of source mod 2**32: 423 bytes
from django.forms import Form, MultipleChoiceField, BooleanField

class TagSearchForm(Form):
    selectedTags = MultipleChoiceField()
    results_preview = BooleanField()

    def __init__(self, tags, conn=None, *args, **kwargs):
        (super(TagSearchForm, self).__init__)(*args, **kwargs)
        self.fields['selectedTags'].choices = tags
        self.conn = conn