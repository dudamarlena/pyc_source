# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/form/simple_form.py
# Compiled at: 2013-04-11 17:47:52
from sqlalchemy.schema import Column
from sqlalchemy.types import Unicode, Date
from camelot.admin.entity_admin import EntityAdmin
from camelot.core.orm import Entity
from camelot.view import forms

class Movie(Entity):
    title = Column(Unicode(60), nullable=False)
    short_description = Column(Unicode(512))
    releasedate = Column(Date)

    class Admin(EntityAdmin):
        form_display = forms.Form(['title', 'short_description', 'releasedate'])