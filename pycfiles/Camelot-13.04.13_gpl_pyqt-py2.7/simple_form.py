# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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