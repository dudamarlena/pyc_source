# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/emails.py
# Compiled at: 2017-04-12 11:57:10
# Size of source mod 2**32: 2836 bytes
from ovp_core.emails import BaseMail
from django.utils.translation import ugettext_lazy as _
from ovp_core.helpers import get_settings

class ProjectMail(BaseMail):
    __doc__ = '\n  This class is responsible for firing emails for Project related actions\n\n  Context should always include a project instance.\n  '

    def __init__(self, project, async_mail=None):
        super(ProjectMail, self).__init__(project.owner.email, async_mail, project.owner.locale)

    def sendProjectCreated(self, context={}):
        """
    Sent when user creates a project
    """
        return self.sendEmail('projectCreated', 'Project created', context)

    def sendProjectPublished(self, context):
        """
    Sent when project is published
    """
        return self.sendEmail('projectPublished', 'Project published', context)

    def sendProjectClosed(self, context):
        """
    Sent when project gets closed
    """
        return self.sendEmail('projectClosed', 'Project closed', context)


class ApplyMail(BaseMail):
    __doc__ = '\n  This class is responsible for firing emails for apply related actions\n  '

    def __init__(self, apply, async_mail=None, locale=None):
        self.apply = apply
        self.async = async_mail
        locale = locale or apply.user and apply.user.locale
        super(ApplyMail, self).__init__(apply.email, async_mail, locale)

    def sendAppliedToVolunteer(self, context={}):
        """
    Sent to user when he applies to a project
    """
        return self.sendEmail('volunteerApplied-ToVolunteer', 'Applied to project', context)

    def sendAppliedToOwner(self, context={}):
        """
    Sent to project owner when user applies to a project
    """
        super(ApplyMail, self).__init__(self.apply.project.owner.email, self.async, self.apply.project.owner.locale)
        return self.sendEmail('volunteerApplied-ToOwner', 'New volunteer', context)

    def sendUnappliedToVolunteer(self, context={}):
        """
    Sent to user when he unapplies from a project
    """
        return self.sendEmail('volunteerUnapplied-ToVolunteer', 'Unapplied from project', context)

    def sendUnappliedToOwner(self, context={}):
        """
    Sent to project owner when user unapplies from a project
    """
        super(ApplyMail, self).__init__(self.apply.project.owner.email, self.async, self.apply.project.owner.locale)
        return self.sendEmail('volunteerUnapplied-ToOwner', 'Volunteer unapplied from project', context)


class ProjectAdminMail(BaseMail):
    __doc__ = '\n  This class is responsible for firing emails for Project related actions\n  '

    def __init__(self, project, async_mail=None):
        s = get_settings()
        email = s.get('ADMIN_MAIL', None)
        super(ProjectAdminMail, self).__init__(email, async_mail)

    def sendProjectCreated(self, context={}):
        """
    Sent when user creates a project
    """
        return self.sendEmail('projectCreatedToAdmin', 'Project created', context)