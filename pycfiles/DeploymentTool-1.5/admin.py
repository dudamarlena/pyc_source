# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\hasil_development\Deployment\Deployment\Deploymentapp\admin.py
# Compiled at: 2014-10-02 05:40:58
from django.contrib import admin
from Deploymentapp.models import Hosts, Users, Task, Commands

class AdministratorHosts(admin.ModelAdmin):
    list_display = ('idhosts', 'hostname', 'basepath')


admin.site.register(Hosts, AdministratorHosts)

class AdministratorUsers(admin.ModelAdmin):
    list_display = ('iduser', 'usersname')


admin.site.register(Users, AdministratorUsers)

class AdministratorTask(admin.ModelAdmin):
    list_display = ('idtask', 'author', 'taskname', 'status')


admin.site.register(Task, AdministratorTask)

class AdministratorCommands(admin.ModelAdmin):
    list_display = ('idtasks', 'commandname', 'parameter1', 'parameter2')


admin.site.register(Commands, AdministratorCommands)