# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-organizations/ovp_organizations/models.py
# Compiled at: 2017-06-22 12:25:06
# Size of source mod 2**32: 4812 bytes
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from ovp_core.helpers import get_address_model
from ovp_organizations.emails import OrganizationMail
from ovp_organizations.emails import OrganizationAdminMail
from django.utils.translation import ugettext_lazy as _
ORGANIZATION_TYPES = (
 (
  0, _('Organization')),
 (
  1, _('School')),
 (
  2, _('Company')),
 (
  3, _('Group of volunteers')))

class Organization(models.Model):
    owner = models.ForeignKey('ovp_users.User', verbose_name=_('owner'))
    address = models.OneToOneField(get_address_model(), blank=True, null=True, verbose_name=_('address'))
    image = models.ForeignKey('ovp_uploads.UploadedImage', blank=True, null=True, verbose_name=_('image'))
    cover = models.ForeignKey('ovp_uploads.UploadedImage', blank=True, null=True, related_name='+', verbose_name=_('cover'))
    causes = models.ManyToManyField('ovp_core.Cause', verbose_name=_('causes'), blank=True)
    members = models.ManyToManyField('ovp_users.User', verbose_name=_('members'), related_name='organizations_member')
    slug = models.SlugField(_('Slug'), max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=150)
    website = models.URLField(_('Website'), blank=True, null=True, default=None)
    facebook_page = models.CharField(_('Facebook'), max_length=255, blank=True, null=True, default=None)
    type = models.PositiveSmallIntegerField(_('Type'), choices=ORGANIZATION_TYPES, default=0)
    details = models.TextField(_('Details'), max_length=3000, blank=True, null=True, default=None)
    description = models.CharField(_('Short description'), max_length=160, blank=True, null=True)
    hidden_address = models.BooleanField(_('Hidden address'), default=False)
    contact_name = models.CharField(_('Responsible name'), max_length=150, blank=True, null=True)
    contact_email = models.EmailField(_('Responsible email'), max_length=150, blank=True, null=True)
    contact_phone = models.CharField(_('Responsible phone'), max_length=150, blank=True, null=True)
    highlighted = models.BooleanField(_('Highlighted'), default=False, blank=False)
    published = models.BooleanField(_('Published'), default=False)
    published_date = models.DateTimeField(_('Published date'), blank=True, null=True)
    deleted = models.BooleanField(_('Deleted'), default=False)
    deleted_date = models.DateTimeField(_('Deleted date'), blank=True, null=True)
    created_date = models.DateTimeField(_('Created date'), auto_now_add=True)
    modified_date = models.DateTimeField(_('Modified date'), auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Organization, self).__init__(*args, **kwargs)
        self._Organization__orig_deleted = self.deleted
        self._Organization__orig_published = self.published

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.published = False
        self.save()

    def mailing(self):
        return OrganizationMail(self)

    def admin_mailing(self):
        return OrganizationAdminMail(self)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            if not self._Organization__orig_published and self.published:
                self.published_date = timezone.now()
                self.mailing().sendOrganizationPublished()
            if not self._Organization__orig_deleted and self.deleted:
                self.deleted_date = timezone.now()
        else:
            self.slug = self.generate_slug()
            self.mailing().sendOrganizationCreated()
            try:
                self.admin_mailing().sendOrganizationCreated()
            except:
                pass

            if not self.description and self.details:
                if len(self.details) > 100:
                    self.description = self.details[0:100]
            else:
                self.description = self.details
        return super(Organization, self).save(*args, **kwargs)

    def generate_slug(self):
        if self.name:
            slug = slugify(self.name)[0:99]
            append = ''
            i = 0
            query = Organization.objects.filter(slug=slug + append)
            while query.count() > 0:
                i += 1
                append = '-' + str(i)
                query = Organization.objects.filter(slug=slug + append)

            return slug + append

    class Meta:
        app_label = 'ovp_organizations'
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')


class OrganizationInvite(models.Model):
    organization = models.ForeignKey('ovp_organizations.Organization')
    invitator = models.ForeignKey('ovp_users.User', related_name='has_invited')
    invited = models.ForeignKey('ovp_users.User', related_name='been_invited')

    class Meta:
        app_label = 'ovp_organizations'
        verbose_name = _('organization_invite')