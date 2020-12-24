# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superhero/admin.py
# Compiled at: 2015-05-05 00:01:33
from django.contrib import admin
from django.utils.translation import ugettext as _
from jmbo.admin import ModelBaseAdmin
from superhero.forms import ImportForm
from superhero.models import Superhero

class SuperheroAdmin(ModelBaseAdmin):
    form = ImportForm

    def get_fieldsets(self, request, obj=None):
        result = super(SuperheroAdmin, self).get_fieldsets(request, obj=obj)
        result += ([_('Import'), {'fields': ('files', )}],)
        result = list(result)
        return (result[0], result[2], result[3], result[7])


admin.site.register(Superhero, SuperheroAdmin)