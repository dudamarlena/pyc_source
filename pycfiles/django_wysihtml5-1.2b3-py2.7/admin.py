# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/wysihtml5/admin.py
# Compiled at: 2014-01-19 03:33:05
from wysihtml5.fields import Wysihtml5TextField
from wysihtml5.widgets import Wysihtml5TextareaWidget

class AdminWysihtml5TextFieldMixin(object):
    """Mixin for ModelAdmin subclasses to provide custom widget for ``Wysihtml5TextField`` fields."""

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, Wysihtml5TextField):
            return db_field.formfield(widget=Wysihtml5TextareaWidget)
        sup = super(AdminWysihtml5TextFieldMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)