# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nbi/forms.py
# Compiled at: 2019-12-19 09:45:12
# Size of source mod 2**32: 1698 bytes
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Regexp, Optional
from projects.forms import MultiCheckboxField
from nbi.conf import config

class NBIProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    activities = StringField('Activities', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    area = MultiCheckboxField('Area', validators=[DataRequired()], choices=[
     ('1', 'Project'),
     ('2', 'Bachelor'),
     ('3', 'Masters')])
    image = FileField('Project Image', validators=[
     FileRequired(),
     FileAllowed(['jpg', 'png'], 'Only JPG and PNG images are allowed')])
    tags = StringField('Tags', validators=[
     DataRequired(),
     Regexp('' + config.get('NBI', 'tags_regex'), message=config.get('NBI', 'tags_regex_msg'))])


class NBIProjectSearchForm(FlaskForm):
    name = StringField('Name', validators=[Optional()], default=None)
    activities = StringField('Activities', validators=[Optional()], default=None)
    contact = StringField('Contact', validators=[Optional()], default=None)
    area = StringField('Area', validators=[Optional()], default=None)
    tags = StringField('Tags', validators=[
     Optional(),
     Regexp('' + config.get('NBI', 'tags_regex'), message=config.get('NBI', 'tags_regex_msg'))], default=None)