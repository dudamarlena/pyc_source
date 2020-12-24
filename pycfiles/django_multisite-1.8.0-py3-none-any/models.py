# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/models.py
# Compiled at: 2020-05-07 16:45:29
from __future__ import unicode_literals
from __future__ import absolute_import
import django, operator
from functools import reduce
from six import python_2_unicode_compatible
from six.moves import range
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address
from django.db import connections, models, router
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import post_migrate
from .hacks import use_framework_for_site_cache
if django.VERSION < (2, ):
    from django.utils.translation import ugettext_lazy as _
else:
    from django.utils.translation import gettext_lazy as _
_site_domain = Site._meta.get_field(b'domain')
use_framework_for_site_cache()

class AliasManager(models.Manager):
    """Manager for all Aliases."""

    def get_queryset(self):
        return super(AliasManager, self).get_queryset().select_related(b'site')

    def resolve(self, host, port=None):
        """
        Returns the Alias that best matches ``host`` and ``port``, or None.

        ``host`` is a hostname like ``'example.com'``.
        ``port`` is a port number like 8000, or None.

        Attempts to first match by 'host:port' against
        Alias.domain. If that fails, it will try to match the bare
        'host' with no port number.

        All comparisons are done case-insensitively.
        """
        domains = self._expand_netloc(host=host, port=port)
        q = reduce(operator.or_, (Q(domain__iexact=d) for d in domains))
        aliases = dict((a.domain, a) for a in self.get_queryset().filter(q))
        for domain in domains:
            try:
                return aliases[domain]
            except KeyError:
                pass

    @classmethod
    def _expand_netloc(cls, host, port=None):
        """
        Returns a list of possible domain expansions for ``host`` and ``port``.

        ``host`` is a hostname like ``'example.com'``.
        ``port`` is a port number like 8000, or None.

        Expansions are ordered from highest to lowest preference and may
        include wildcards. Examples::

        >>> AliasManager._expand_netloc('www.example.com')
        ['www.example.com', '*.example.com', '*.com', '*']

        >>> AliasManager._expand_netloc('www.example.com', 80)
        ['www.example.com:80', 'www.example.com',
         '*.example.com:80', '*.example.com',
         '*.com:80', '*.com',
         '*:80', '*']
        """
        if not host:
            raise ValueError(b'Invalid host: %s' % host)
        try:
            validate_ipv4_address(host)
            bits = [host]
        except ValidationError:
            bits = host.split(b'.')

        result = []
        for i in range(0, len(bits) + 1):
            if i == 0:
                host = (b'.').join(bits[i:])
            else:
                host = (b'.').join([b'*'] + bits[i:])
            if port:
                result.append(b'%s:%s' % (host, port))
            result.append(host)

        return result


class CanonicalAliasManager(models.Manager):
    """Manager for Alias objects where is_canonical is True."""

    def get_queryset(self):
        qset = super(CanonicalAliasManager, self).get_queryset()
        return qset.filter(is_canonical=True)

    def sync_many(self, *args, **kwargs):
        """
        Synchronize canonical Alias objects based on Site.domain.

        You can pass Q-objects or filter arguments to update a subset of
        Alias objects::

            Alias.canonical.sync_many(site__domain='example.com')
        """
        aliases = self.get_queryset().filter(*args, **kwargs)
        for alias in aliases.select_related(b'site'):
            domain = alias.site.domain
            if domain and alias.domain != domain:
                alias.domain = domain
                alias.save()

    def sync_missing(self):
        """Create missing canonical Alias objects based on Site.domain."""
        aliases = self.get_queryset()
        try:
            sites = self.model._meta.get_field(b'site').remote_field.model
        except AttributeError:
            sites = self.model._meta.get_field(b'site').rel.to

        for site in sites.objects.exclude(aliases__in=aliases):
            Alias.sync(site=site)

    def sync_all(self):
        """Create or sync canonical Alias objects from all Site objects."""
        self.sync_many()
        self.sync_missing()


class NotCanonicalAliasManager(models.Manager):
    """Manager for Aliases where is_canonical is None."""

    def get_queryset(self):
        qset = super(NotCanonicalAliasManager, self).get_queryset()
        return qset.filter(is_canonical__isnull=True)


def validate_true_or_none(value):
    """Raises ValidationError if value is not True or None."""
    if value not in (True, None):
        raise ValidationError(b'%r must be True or None' % value)
    return


@python_2_unicode_compatible
class Alias(models.Model):
    """
    Model for domain-name aliases for Site objects.

    Domain names must be unique in the format of: 'hostname[:port].'
    Each Site object that has a domain must have an ``is_canonical``
    Alias.
    """
    domain = type(_site_domain)(_(b'domain name'), max_length=_site_domain.max_length, unique=True, help_text=_(b'Either "domain" or "domain:port"'))
    site = models.ForeignKey(Site, related_name=b'aliases', on_delete=models.CASCADE)
    is_canonical = models.NullBooleanField(_(b'is canonical?'), default=None, editable=False, validators=[
     validate_true_or_none], help_text=_(b'Does this domain name match the one in site?'))
    redirect_to_canonical = models.BooleanField(_(b'redirect to canonical?'), default=True, help_text=_(b'Should this domain name redirect to the one in site?'))
    objects = AliasManager()
    canonical = CanonicalAliasManager()
    aliases = NotCanonicalAliasManager()

    class Meta:
        unique_together = [
         ('is_canonical', 'site')]
        verbose_name_plural = _(b'aliases')

    def __str__(self):
        return b'%s -> %s' % (self.domain, self.site.domain)

    def __repr__(self):
        return b'<Alias: %s>' % str(self)

    def save_base(self, *args, **kwargs):
        self.full_clean()
        if self.is_canonical and self.domain != self.site.domain:
            raise ValidationError({b'domain': [b'Does not match %r' % self.site]})
        super(Alias, self).save_base(*args, **kwargs)

    def validate_unique(self, exclude=None):
        errors = {}
        try:
            super(Alias, self).validate_unique(exclude=exclude)
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if exclude is not None and b'domain' not in exclude:
            field_name = b'domain'
            field_error = self.unique_error_message(self.__class__, (
             field_name,))
            if field_name not in errors or str(field_error) not in [ str(err) for err in errors[field_name] ]:
                qset = self.__class__.objects.filter(**{field_name + b'__iexact': getattr(self, field_name)})
                if self.pk is not None:
                    qset = qset.exclude(pk=self.pk)
                if qset.exists():
                    errors.setdefault(field_name, []).append(field_error)
        if errors:
            raise ValidationError(errors)
        return

    @classmethod
    def _sync_blank_domain(cls, site):
        """Delete associated Alias object for ``site``, if domain is blank."""
        if site.domain:
            raise ValueError(b'%r has a domain' % site)
        try:
            alias = cls.objects.get(site=site)
        except cls.DoesNotExist:
            pass
        else:
            if not alias.is_canonical:
                raise cls.MultipleObjectsReturned(b'Other %s still exist for %r' % (
                 cls._meta.verbose_name_plural.capitalize(), site))
            alias.delete()

    @classmethod
    def sync(cls, site, force_insert=False):
        """
        Create or synchronize Alias object from ``site``.

        If `force_insert`, forces creation of Alias object.
        """
        domain = site.domain
        if not domain:
            cls._sync_blank_domain(site)
            return
        if force_insert:
            alias = cls.objects.create(site=site, is_canonical=True, domain=domain)
        else:
            alias, created = cls.objects.get_or_create(site=site, is_canonical=True, defaults={b'domain': domain})
            if not created and alias.domain != domain:
                alias.site = site
                alias.domain = domain
                alias.save()
        return alias

    @classmethod
    def site_domain_changed_hook(cls, sender, instance, raw, *args, **kwargs):
        """Updates canonical Alias object if Site.domain has changed."""
        if raw or instance.pk is None:
            return
        try:
            original = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        if original.domain != instance.domain:
            cls.sync(site=instance)
        return

    @classmethod
    def site_created_hook(cls, sender, instance, raw, created, *args, **kwargs):
        """Creates canonical Alias object for a new Site."""
        if raw or not created:
            return
        using = router.db_for_write(cls)
        tables = connections[using].introspection.table_names()
        if cls._meta.db_table not in tables:
            return
        cls.sync(site=instance)

    @classmethod
    def db_table_created_hook(cls, *args, **kwargs):
        """Syncs canonical Alias objects for all existing Site objects."""
        Alias.canonical.sync_all()


pre_save.connect(Alias.site_domain_changed_hook, sender=Site)
post_save.connect(Alias.site_created_hook, sender=Site)
post_migrate.connect(Alias.db_table_created_hook)