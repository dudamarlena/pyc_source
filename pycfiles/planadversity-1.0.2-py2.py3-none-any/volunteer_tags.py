# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/templatetags/volunteer_tags.py
# Compiled at: 2014-06-10 15:49:30
from django.template.base import Library
from volunteers.models import VolunteerApplication, Organization, Project
register = Library()

@register.assignment_tag(takes_context=True)
def application_status(context, opp, user):
    try:
        app = VolunteerApplication.objects.get(user=user, opportunity=opp)
    except:
        app = None

    if app:
        return app.status
    else:
        return
        return


@register.assignment_tag(takes_context=True)
def manager_of(context, org, user):
    try:
        organization = Organization.objects.get(slug=org.slug, managers=user)
    except:
        organization = None

    if organization:
        return True
    else:
        return False
        return


@register.assignment_tag(takes_context=True)
def lead_volunteer_of(context, project, user):
    try:
        proj = Project.objects.get(slug=project.slug, lead_volunteers=user)
    except:
        proj = None

    if proj:
        return True
    else:
        return False
        return