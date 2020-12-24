# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/forms.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 6168 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from airflow.models import Connection
from airflow.utils import timezone
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget, BS3TextAreaFieldWidget, BS3PasswordFieldWidget, Select2Widget, DateTimePickerWidget
from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import IntegerField, SelectField, TextAreaField, PasswordField, StringField, DateTimeField, BooleanField

class DateTimeForm(FlaskForm):
    execution_date = DateTimeField('Execution date',
      widget=(DateTimePickerWidget()))


class DateTimeWithNumRunsForm(FlaskForm):
    base_date = DateTimeField('Anchor date',
      widget=(DateTimePickerWidget()), default=(timezone.utcnow()))
    num_runs = SelectField('Number of runs', default=25, choices=((5, '5'), (25, '25'),
                                                                  (50, '50'), (100, '100'),
                                                                  (365, '365')))


class DateTimeWithNumRunsWithDagRunsForm(DateTimeWithNumRunsForm):
    execution_date = SelectField('DAG run')


class DagRunForm(DynamicForm):
    dag_id = StringField((lazy_gettext('Dag Id')),
      validators=[
     validators.DataRequired()],
      widget=(BS3TextFieldWidget()))
    start_date = DateTimeField((lazy_gettext('Start Date')),
      widget=(DateTimePickerWidget()))
    end_date = DateTimeField((lazy_gettext('End Date')),
      widget=(DateTimePickerWidget()))
    run_id = StringField((lazy_gettext('Run Id')),
      validators=[
     validators.DataRequired()],
      widget=(BS3TextFieldWidget()))
    state = SelectField((lazy_gettext('State')),
      choices=(('success', 'success'), ('running', 'running'), ('failed', 'failed')),
      widget=(Select2Widget()))
    execution_date = DateTimeField((lazy_gettext('Execution Date')),
      widget=(DateTimePickerWidget()))
    external_trigger = BooleanField(lazy_gettext('External Trigger'))

    def populate_obj(self, item):
        super(DagRunForm, self).populate_obj(item)
        item.execution_date = timezone.make_aware(item.execution_date)


class ConnectionForm(DynamicForm):
    conn_id = StringField((lazy_gettext('Conn Id')),
      validators=[
     validators.DataRequired()],
      widget=(BS3TextFieldWidget()))
    conn_type = SelectField((lazy_gettext('Conn Type')),
      choices=(Connection._types),
      widget=(Select2Widget()))
    host = StringField((lazy_gettext('Host')),
      widget=(BS3TextFieldWidget()))
    schema = StringField((lazy_gettext('Schema')),
      widget=(BS3TextFieldWidget()))
    login = StringField((lazy_gettext('Login')),
      widget=(BS3TextFieldWidget()))
    password = PasswordField((lazy_gettext('Password')),
      widget=(BS3PasswordFieldWidget()))
    port = IntegerField((lazy_gettext('Port')),
      validators=[
     validators.Optional()],
      widget=(BS3TextFieldWidget()))
    extra = TextAreaField((lazy_gettext('Extra')),
      widget=(BS3TextAreaFieldWidget()))
    extra__jdbc__drv_path = StringField((lazy_gettext('Driver Path')),
      widget=(BS3TextFieldWidget()))
    extra__jdbc__drv_clsname = StringField((lazy_gettext('Driver Class')),
      widget=(BS3TextFieldWidget()))
    extra__google_cloud_platform__project = StringField((lazy_gettext('Project Id')),
      widget=(BS3TextFieldWidget()))
    extra__google_cloud_platform__key_path = StringField((lazy_gettext('Keyfile Path')),
      widget=(BS3TextFieldWidget()))
    extra__google_cloud_platform__keyfile_dict = PasswordField((lazy_gettext('Keyfile JSON')),
      widget=(BS3PasswordFieldWidget()))
    extra__google_cloud_platform__scope = StringField((lazy_gettext('Scopes (comma separated)')),
      widget=(BS3TextFieldWidget()))
    extra__google_cloud_platform__num_retries = IntegerField((lazy_gettext('Number of Retries')),
      validators=[
     validators.NumberRange(min=0)],
      widget=(BS3TextFieldWidget()),
      default=5)
    extra__grpc__auth_type = StringField((lazy_gettext('Grpc Auth Type')),
      widget=(BS3TextFieldWidget()))
    extra__grpc__credential_pem_file = StringField((lazy_gettext('Credential Keyfile Path')),
      widget=(BS3TextFieldWidget()))
    extra__grpc__scopes = StringField((lazy_gettext('Scopes (comma separated)')),
      widget=(BS3TextFieldWidget()))