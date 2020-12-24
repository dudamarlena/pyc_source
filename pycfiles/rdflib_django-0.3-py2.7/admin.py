# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/rdflib_django/admin.py
# Compiled at: 2012-10-25 06:19:50
"""
Defines admin options for this RDFlib implementation.
"""
from django.contrib import admin
from rdflib_django import models, forms

class NamedGraphAdmin(admin.ModelAdmin):
    """
    Admin module for named graphs.
    """
    list_display = ('identifier', )
    ordering = ('identifier', )
    search_fields = ('identifier', )


class NamespaceAdmin(admin.ModelAdmin):
    """
    Admin module for managing namespaces.
    """
    list_display = ('prefix', 'uri', 'fixed')
    ordering = ('-fixed', 'prefix')
    search_fields = ('prefix', 'uri')
    form = forms.NamespaceForm

    def get_actions(self, request):
        return []

    def has_delete_permission(self, request, obj=None):
        """
        Default namespaces cannot be deleted.
        """
        if obj is not None and obj.fixed:
            return False
        else:
            return super(NamespaceAdmin, self).has_delete_permission(request, obj)


admin.site.register(models.NamedGraph, NamedGraphAdmin)
admin.site.register(models.NamespaceModel, NamespaceAdmin)
admin.site.register(models.URIStatement)
admin.site.register(models.LiteralStatement)