# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/prototype/admin.py
# Compiled at: 2014-06-19 10:55:29
from models import PropertyEquivalence
from models import ProtoTable
from django.contrib import admin
from actions import doModelPrototype, doModelGraph, doExportPrototype, doExportProtoJson
from models import Project, Model, Property, Relationship

class MyModelAdmin(admin.ModelAdmin):
    actions = [
     doModelPrototype, doModelGraph, doExportPrototype, doExportProtoJson]


admin.site.register(Model, MyModelAdmin)
from actions import doEntityPrototype
from models import Entity

class MyEntityAdmin(admin.ModelAdmin):
    actions = [
     doEntityPrototype]


admin.site.register(Entity, MyEntityAdmin)
from actions import doImportSchema, doImportOMS

class MyProjectAdmin(admin.ModelAdmin):
    actions = [
     doImportSchema, doImportOMS]


admin.site.register(Project, MyProjectAdmin)
from models import Diagram, DiagramEntity

class MyDiagramAdmin(admin.ModelAdmin):
    actions = [
     doModelGraph]


admin.site.register(Diagram, MyDiagramAdmin)
admin.site.register(Property)
admin.site.register(Relationship)
admin.site.register(ProtoTable)