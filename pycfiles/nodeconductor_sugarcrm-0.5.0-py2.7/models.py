# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/models.py
# Compiled at: 2016-09-28 11:51:43
from __future__ import unicode_literals
from django.db import models
from nodeconductor.core import utils as core_utils
from nodeconductor.quotas.fields import QuotaField, LimitAggregatorQuotaField, CounterQuotaField
from nodeconductor.quotas.models import QuotaModelMixin
from nodeconductor.structure import models as structure_models

class SugarCRMService(structure_models.Service):
    projects = models.ManyToManyField(structure_models.Project, related_name=b'sugarcrm_services', through=b'SugarCRMServiceProjectLink')

    class Meta:
        verbose_name = b'SugarCRM service'
        verbose_name_plural = b'SugarCRM services'
        unique_together = ('customer', 'settings')

    @classmethod
    def get_url_name(cls):
        return b'sugarcrm'


class SugarCRMServiceProjectLink(structure_models.ServiceProjectLink):
    service = models.ForeignKey(SugarCRMService)

    class Quotas(QuotaModelMixin.Quotas):
        user_limit_count = LimitAggregatorQuotaField(default_limit=50, get_children=lambda spl: CRM.objects.filter(service_project_link=spl), child_quota_name=b'user_count')
        crm_count = CounterQuotaField(target_models=lambda : [
         CRM], path_to_scope=b'service_project_link', default_limit=-1)

    class Meta(structure_models.ServiceProjectLink.Meta):
        verbose_name = b'SugarCRM service project link'
        verbose_name_plural = b'SugarCRM service project links'

    @classmethod
    def get_url_name(cls):
        return b'sugarcrm-spl'


class CRM(QuotaModelMixin, structure_models.PublishableResource, structure_models.ApplicationMixin):
    service_project_link = models.ForeignKey(SugarCRMServiceProjectLink, related_name=b'crms', on_delete=models.PROTECT)
    api_url = models.CharField(max_length=127, help_text=b'CRMs OpenStack instance access URL.')
    admin_username = models.CharField(max_length=60)
    admin_password = models.CharField(max_length=255)
    instance_url = models.URLField(blank=True, help_text=b'CRMs OpenStack instance URL in NC.')

    class Quotas(QuotaModelMixin.Quotas):
        user_count = QuotaField(default_limit=0)

    class Meta:
        verbose_name = b'CRM'
        verbose_name_plural = b'CRMs'

    @classmethod
    def get_url_name(cls):
        return b'sugarcrm-crms'

    @property
    def full_name(self):
        return b'SugarCRM Instance %s' % self.name

    def get_backend(self):
        from .backend import SugarCRMBackend
        return SugarCRMBackend(settings=self.service_project_link.service.settings, crm=self)

    def get_instance(self):
        """ Restore instance from URL """
        return core_utils.instance_from_url(self.instance_url)

    def as_dict(self):
        """ Represent instance as dict with all necessary attributes """
        return {b'name': self.name, 
           b'description': self.description, 
           b'service_project_link': self.service_project_link.pk, 
           b'admin_username': self.admin_username, 
           b'admin_password': self.admin_password, 
           b'tags': [ tag.name for tag in self.tags.all() ]}