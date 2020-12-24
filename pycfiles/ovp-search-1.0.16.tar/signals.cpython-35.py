# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-search/ovp_search/signals.py
# Compiled at: 2017-06-22 10:26:17
# Size of source mod 2**32: 4336 bytes
from django.db import models
from haystack import signals
from ovp_projects.models import Project, Job, Work
from ovp_organizations.models import Organization
from ovp_core.models import GoogleAddress
from ovp_users.models import User
from ovp_users.models.profile import get_profile_model

class TiedModelRealtimeSignalProcessor(signals.BaseSignalProcessor):
    __doc__ = '\n    TiedModelRealTimeSignalProcessor handles updates to a index tied to a model\n\n    We need to be able to detect changes to a model a rebuild another index,\n    such as detecting changes to GoogleAddress and updating the index\n    for projects and organizations.\n\n  '
    attach_to = [
     (
      Project, 'handle_save', 'handle_delete'),
     (
      Organization, 'handle_save', 'handle_delete'),
     (
      User, 'handle_save', 'handle_delete'),
     (
      get_profile_model(), 'handle_profile_save', 'handle_profile_delete'),
     (
      GoogleAddress, 'handle_address_save', 'handle_address_delete'),
     (
      Job, 'handle_job_and_work_save', 'handle_job_and_work_delete'),
     (
      Work, 'handle_job_and_work_save', 'handle_job_and_work_delete')]
    m2m = [
     Project.causes.through,
     Project.skills.through,
     Organization.causes.through]
    m2m_user = [
     get_profile_model().causes.through,
     get_profile_model().skills.through]

    def setup(self):
        for item in self.attach_to:
            models.signals.post_save.connect(getattr(self, item[1]), sender=item[0])
            models.signals.post_delete.connect(getattr(self, item[2]), sender=item[0])

        for item in self.m2m:
            models.signals.m2m_changed.connect(self.handle_m2m, sender=item)

        for item in self.m2m_user:
            models.signals.m2m_changed.connect(self.handle_m2m_user, sender=item)

    def teardown(self):
        for item in self.attach_to:
            models.signals.post_save.disconnect(getattr(self, item[1]), sender=item[0])
            models.signals.post_delete.disconnect(getattr(self, item[2]), sender=item[0])

        for item in self.m2m:
            models.signals.m2m_changed.disconnect(self.handle_m2m, sender=item)

        for item in self.m2m_user:
            models.signals.m2m_changed.disconnect(self.handle_m2m_user, sender=item)

    def handle_address_save(self, sender, instance, **kwargs):
        """ Custom handler for address save """
        objects = self.find_associated_with_address(instance)
        for obj in objects:
            self.handle_save(obj.__class__, obj)

    def handle_address_delete(self, sender, instance, **kwargs):
        """ Custom handler for address delete """
        objects = self.find_associated_with_address(instance)
        for obj in objects:
            self.handle_delete(obj.__class__, obj)

    def handle_job_and_work_save(self, sender, instance, **kwargs):
        """ Custom handler for job and work save """
        self.handle_save(instance.project.__class__, instance.project)

    def handle_job_and_work_delete(self, sender, instance, **kwargs):
        """ Custom handler for job and work delete """
        self.handle_delete(instance.project.__class__, instance.project)

    def handle_profile_save(self, sender, instance, **kwargs):
        """ Custom handler for user profile save """
        self.handle_save(instance.user.__class__, instance.user)

    def handle_profile_delete(self, sender, instance, **kwargs):
        """ Custom handler for user profile delete """
        try:
            self.handle_save(instance.user.__class__, instance.user)
        except get_profile_model().DoesNotExist:
            pass

    def handle_m2m(self, sender, instance, **kwargs):
        """ Handle many to many relationships """
        self.handle_save(instance.__class__, instance)

    def handle_m2m_user(self, sender, instance, **kwargs):
        """ Handle many to many relationships for user field """
        self.handle_save(instance.user.__class__, instance.user)

    def find_associated_with_address(self, instance):
        """ Returns list with projects and organizations associated with given address """
        objects = []
        objects += list(Project.objects.filter(address=instance))
        objects += list(Organization.objects.filter(address=instance))
        return objects