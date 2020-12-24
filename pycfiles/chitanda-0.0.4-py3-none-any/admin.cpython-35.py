# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/api/admin.py
# Compiled at: 2017-04-03 16:34:20
# Size of source mod 2**32: 1213 bytes
from django.contrib import admin
import chisubmit.backend.api.models as models

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')


class GraderAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'dropped')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'name', 'deadline', 'course')


class RubricComponentAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'description', 'points')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('course', 'team_id')


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('team', 'assignment')


admin.site.register(models.Course)
admin.site.register(models.Instructor, InstructorAdmin)
admin.site.register(models.Grader, GraderAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.RubricComponent, RubricComponentAdmin)
admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Registration, RegistrationAdmin)
admin.site.register(models.Submission)
admin.site.register(models.Grade)