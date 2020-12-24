# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-search/ovp_search/search_indexes.py
# Compiled at: 2017-06-21 15:43:52
# Size of source mod 2**32: 3696 bytes
from haystack import indexes
from django.db.models import Q
from ovp_projects.models import Project, Work, Job
from ovp_organizations.models import Organization
from ovp_core.models import GoogleAddress
from ovp_users.models import User
from ovp_users.models.profile import get_profile_model

class CausesMixin:

    def prepare_causes(self, obj):
        return [cause.id for cause in obj.causes.all()]


class SkillsMixin:

    def prepare_skills(self, obj):
        return [skill.id for skill in obj.skills.all()]


class AddressComponentsMixin:

    def prepare_address_components(self, obj):
        types = []
        if obj.address and type(obj.address) == GoogleAddress:
            for component in obj.address.address_components.all():
                for component_type in component.types.all():
                    types.append('{}-{}'.format(component.long_name, component_type.name))

        return types


class ProjectIndex(indexes.SearchIndex, indexes.Indexable, SkillsMixin, CausesMixin, AddressComponentsMixin):
    name = indexes.EdgeNgramField(model_attr='name')
    causes = indexes.MultiValueField(faceted=True)
    text = indexes.CharField(document=True, use_template=True)
    skills = indexes.MultiValueField(faceted=True)
    highlighted = indexes.BooleanField(model_attr='highlighted')
    can_be_done_remotely = indexes.BooleanField(faceted=True)
    published = indexes.BooleanField(model_attr='published')
    deleted = indexes.BooleanField(model_attr='deleted')
    closed = indexes.BooleanField(model_attr='closed')
    address_components = indexes.MultiValueField(faceted=True)

    def prepare_can_be_done_remotely(self, obj):
        can_be_done_remotely = False
        try:
            can_be_done_remotely = obj.work.can_be_done_remotely
        except Work.DoesNotExist:
            pass

        try:
            can_be_done_remotely = obj.job.can_be_done_remotely
        except Job.DoesNotExist:
            pass

        return can_be_done_remotely

    def get_model(self):
        return Project

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(closed=False, deleted=False)


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable, CausesMixin, AddressComponentsMixin):
    name = indexes.EdgeNgramField(model_attr='name')
    causes = indexes.MultiValueField(faceted=True)
    text = indexes.CharField(document=True, use_template=True)
    highlighted = indexes.BooleanField(model_attr='highlighted')
    address_components = indexes.MultiValueField(faceted=True)
    published = indexes.BooleanField(model_attr='published')

    def get_model(self):
        return Organization

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(deleted=False)


class UserIndex(indexes.SearchIndex, indexes.Indexable, AddressComponentsMixin):
    name = indexes.EdgeNgramField(model_attr='name')
    text = indexes.CharField(document=True)
    causes = indexes.MultiValueField(faceted=True)
    skills = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects

    def prepare_causes(self, obj):
        try:
            if obj.profile:
                return [cause.id for cause in obj.profile.causes.all()]
        except get_profile_model().DoesNotExist:
            return []

    def prepare_skills(self, obj):
        try:
            if obj.profile:
                return [skill.id for skill in obj.profile.skills.all()]
        except get_profile_model().DoesNotExist:
            return []