# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/forms/CreateProfileForm.py
# Compiled at: 2016-04-19 10:47:47
"""
.. module:: CreateProfileForm
    :synopsis: A form for completing a user's profile.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""
from flask.ext.wtf import Form
from wtforms import StringField, HiddenField
from wtforms.validators import URL, Email, Required
EMAIL_ERROR = 'Please provide a valid email address.'

class CreateProfileForm(Form):
    """A form for completing a :class:`~app.models.User` profile after they
    login to Eventum for the first time.

    :ivar email: :class:`wtforms.fields.StringField` - The user's email
        address.
    :ivar name: :class:`wtforms.fields.StringField` - The user's name.
    :ivar next: :class:`wtforms.fields.HiddenField` - The URL that they should
        be redirected to after completing their profile.
    """
    name = StringField('Full Name')
    email = StringField('Email Address', [Email(message=EMAIL_ERROR),
     Required(message=EMAIL_ERROR)])
    next = HiddenField('hidden', [URL(require_tld=False)])