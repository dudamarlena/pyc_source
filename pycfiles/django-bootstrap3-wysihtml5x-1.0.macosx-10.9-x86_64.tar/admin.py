# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/bootstrap3_wysihtml5x/admin.py
# Compiled at: 2014-10-27 10:01:28
from bootstrap3_wysihtml5x.fields import Wysihtml5TextField
from bootstrap3_wysihtml5x.widgets import Wysihtml5TextareaWidget

class AdminWysihtml5TextFieldMixin(object):
    """Mixin for ModelAdmin subclasses to provide custom widget for ``Wysihtml5TextField`` fields."""

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, Wysihtml5TextField):
            return db_field.formfield(widget=Wysihtml5TextareaWidget)
        sup = super(AdminWysihtml5TextFieldMixin, self)
        return sup.formfield_for_dbfield(db_field, **kwargs)