# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/forms.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 2044 bytes
from django.db import DatabaseError
from django.forms import ModelForm, Field, ValidationError, BooleanField, CharField
from django.forms.widgets import CheckboxInput, Select
from explorer.app_settings import EXPLORER_DEFAULT_CONNECTION, EXPLORER_CONNECTIONS
from explorer.models import Query, MSG_FAILED_BLACKLIST

class SqlField(Field):

    def validate(self, value):
        """
        Ensure that the SQL passes the blacklist.

        :param value: The SQL for this Query model.
        """
        query = Query(sql=value)
        passes_blacklist, failing_words = query.passes_blacklist()
        error = MSG_FAILED_BLACKLIST % ', '.join(failing_words) if not passes_blacklist else None
        if error:
            raise ValidationError(error,
              code='InvalidSql')


class QueryForm(ModelForm):
    sql = SqlField()
    snapshot = BooleanField(widget=CheckboxInput, required=False)
    connection = CharField(widget=Select, required=False)

    def __init__(self, *args, **kwargs):
        (super(QueryForm, self).__init__)(*args, **kwargs)
        self.fields['connection'].widget.choices = self.connections
        if not self.instance.connection:
            self.initial['connection'] = EXPLORER_DEFAULT_CONNECTION
        self.fields['connection'].widget.attrs['class'] = 'form-control'

    def clean(self):
        if self.instance:
            if self.data.get('created_by_user', None):
                self.cleaned_data['created_by_user'] = self.instance.created_by_user
        return super(QueryForm, self).clean()

    @property
    def created_by_user_email(self):
        if self.instance.created_by_user:
            return self.instance.created_by_user.email
        else:
            return '--'

    @property
    def created_at_time(self):
        return self.instance.created_at.strftime('%Y-%m-%d')

    @property
    def connections(self):
        return [(v, k) for k, v in EXPLORER_CONNECTIONS.items()]

    class Meta:
        model = Query
        fields = ['title', 'sql', 'description', 'snapshot', 'connection']