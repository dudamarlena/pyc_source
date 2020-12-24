# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/admin.py
# Compiled at: 2016-09-16 10:02:59
from django.contrib import admin
from nodeconductor.structure import admin as structure_admin
from .models import JiraService, JiraServiceProjectLink, Project, Issue, Comment
admin.site.register(Issue, admin.ModelAdmin)
admin.site.register(Comment, admin.ModelAdmin)
admin.site.register(Project, structure_admin.ResourceAdmin)
admin.site.register(JiraService, structure_admin.ServiceAdmin)
admin.site.register(JiraServiceProjectLink, structure_admin.ServiceProjectLinkAdmin)