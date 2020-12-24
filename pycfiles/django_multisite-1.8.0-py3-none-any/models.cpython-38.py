# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/models.py
# Compiled at: 2020-05-07 16:45:29
# Size of source mod 2**32: 11089 bytes
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
    import django.utils.translation as _
else:
    import django.utils.translation as _
_site_domain = Site._meta.get_field('domain')
use_framework_for_site_cache()

class AliasManager(models.Manager):
    __doc__ = 'Manager for all Aliases.'

    def get_queryset(self):
        return super(AliasManager, self).get_queryset().select_related('site')

    def resolve--- This code section failed: ---

 L.  50         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _expand_netloc
                4  LOAD_FAST                'host'
                6  LOAD_FAST                'port'
                8  LOAD_CONST               ('host', 'port')
               10  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               12  STORE_FAST               'domains'

 L.  51        14  LOAD_GLOBAL              reduce
               16  LOAD_GLOBAL              operator
               18  LOAD_ATTR                or_
               20  LOAD_GENEXPR             '<code_object <genexpr>>'
               22  LOAD_STR                 'AliasManager.resolve.<locals>.<genexpr>'
               24  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               26  LOAD_FAST                'domains'
               28  GET_ITER         
               30  CALL_FUNCTION_1       1  ''
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'q'

 L.  52        36  LOAD_GLOBAL              dict
               38  LOAD_GENEXPR             '<code_object <genexpr>>'
               40  LOAD_STR                 'AliasManager.resolve.<locals>.<genexpr>'
               42  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               44  LOAD_FAST                'self'
               46  LOAD_METHOD              get_queryset
               48  CALL_METHOD_0         0  ''
               50  LOAD_METHOD              filter
               52  LOAD_FAST                'q'
               54  CALL_METHOD_1         1  ''
               56  GET_ITER         
               58  CALL_FUNCTION_1       1  ''
               60  CALL_FUNCTION_1       1  ''
               62  STORE_FAST               'aliases'

 L.  53        64  LOAD_FAST                'domains'
               66  GET_ITER         
               68  FOR_ITER            110  'to 110'
               70  STORE_FAST               'domain'

 L.  54        72  SETUP_FINALLY        88  'to 88'

 L.  55        74  LOAD_FAST                'aliases'
               76  LOAD_FAST                'domain'
               78  BINARY_SUBSCR    
               80  POP_BLOCK        
               82  ROT_TWO          
               84  POP_TOP          
               86  RETURN_VALUE     
             88_0  COME_FROM_FINALLY    72  '72'

 L.  56        88  DUP_TOP          
               90  LOAD_GLOBAL              KeyError
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   106  'to 106'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L.  57       102  POP_EXCEPT       
              104  JUMP_BACK            68  'to 68'
            106_0  COME_FROM            94  '94'
              106  END_FINALLY      
              108  JUMP_BACK            68  'to 68'

Parse error at or near `ROT_TWO' instruction at offset 82

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
            raise ValueError('Invalid host: %s' % host)
        try:
            validate_ipv4_address(host)
            bits = [host]
        except ValidationError:
            bits = host.split('.')
        else:
            result = []
            for i in range(0, len(bits) + 1):
                if i == 0:
                    host = '.'.join(bits[i:])
                else:
                    host = '.'.join(['*'] + bits[i:])
                if port:
                    result.append('%s:%s' % (host, port))
                result.append(host)
            else:
                return result


class CanonicalAliasManager(models.Manager):
    __doc__ = 'Manager for Alias objects where is_canonical is True.'

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
        aliases = (self.get_queryset().filter)(*args, **kwargs)
        for alias in aliases.select_related('site'):
            domain = alias.site.domain
            if domain and alias.domain != domain:
                alias.domain = domain
                alias.save()

    def sync_missing(self):
        """Create missing canonical Alias objects based on Site.domain."""
        aliases = self.get_queryset()
        try:
            sites = self.model._meta.get_field('site').remote_field.model
        except AttributeError:
            sites = self.model._meta.get_field('site').rel.to
        else:
            for site in sites.objects.exclude(aliases__in=aliases):
                Alias.sync(site=site)

    def sync_all(self):
        """Create or sync canonical Alias objects from all Site objects."""
        self.sync_many()
        self.sync_missing()


class NotCanonicalAliasManager(models.Manager):
    __doc__ = 'Manager for Aliases where is_canonical is None.'

    def get_queryset(self):
        qset = super(NotCanonicalAliasManager, self).get_queryset()
        return qset.filter(is_canonical__isnull=True)


def validate_true_or_none(value):
    """Raises ValidationError if value is not True or None."""
    if value not in (True, None):
        raise ValidationError('%r must be True or None' % value)


@python_2_unicode_compatible
class Alias(models.Model):
    __doc__ = "\n    Model for domain-name aliases for Site objects.\n\n    Domain names must be unique in the format of: 'hostname[:port].'\n    Each Site object that has a domain must have an ``is_canonical``\n    Alias.\n    "
    domain = type(_site_domain)((_('domain name')),
      max_length=(_site_domain.max_length),
      unique=True,
      help_text=(_('Either "domain" or "domain:port"')))
    site = models.ForeignKey(Site,
      related_name='aliases', on_delete=(models.CASCADE))
    is_canonical = models.NullBooleanField((_('is canonical?')),
      default=None,
      editable=False,
      validators=[
     validate_true_or_none],
      help_text=(_('Does this domain name match the one in site?')))
    redirect_to_canonical = models.BooleanField((_('redirect to canonical?')),
      default=True,
      help_text=(_('Should this domain name redirect to the one in site?')))
    objects = AliasManager()
    canonical = CanonicalAliasManager()
    aliases = NotCanonicalAliasManager()

    class Meta:
        unique_together = [
         ('is_canonical', 'site')]
        verbose_name_plural = _('aliases')

    def __str__(self):
        return '%s -> %s' % (self.domain, self.site.domain)

    def __repr__(self):
        return '<Alias: %s>' % str(self)

    def save_base(self, *args, **kwargs):
        self.full_clean()
        if self.is_canonical:
            if self.domain != self.site.domain:
                raise ValidationError({'domain': ['Does not match %r' % self.site]})
        (super(Alias, self).save_base)(*args, **kwargs)

    def validate_unique(self, exclude=None):
        errors = {}
        try:
            super(Alias, self).validate_unique(exclude=exclude)
        except ValidationError as e:
            try:
                errors = e.update_error_dict(errors)
            finally:
                e = None
                del e

        else:
            if exclude is not None:
                if 'domain' not in exclude:
                    field_name = 'domain'
                    field_error = self.unique_error_message(self.__class__, (
                     field_name,))
                    if field_name not in errors or str(field_error) not in [str(err) for err in errors[field_name]]:
                        qset = (self.__class__.objects.filter)(**{field_name + '__iexact': getattr(self, field_name)})
                        if self.pk is not None:
                            qset = qset.exclude(pk=(self.pk))
                        if qset.exists():
                            errors.setdefault(field_name, []).append(field_error)
            if errors:
                raise ValidationError(errors)

    @classmethod
    def _sync_blank_domain(cls, site):
        """Delete associated Alias object for ``site``, if domain is blank."""
        if site.domain:
            raise ValueError('%r has a domain' % site)
        try:
            alias = cls.objects.get(site=site)
        except cls.DoesNotExist:
            pass
        else:
            if not alias.is_canonical:
                raise cls.MultipleObjectsReturned('Other %s still exist for %r' % (
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
            alias, created = cls.objects.get_or_create(site=site,
              is_canonical=True,
              defaults={'domain': domain})
            if not created:
                if alias.domain != domain:
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
            original = sender.objects.get(pk=(instance.pk))
        except sender.DoesNotExist:
            return
        else:
            if original.domain != instance.domain:
                cls.sync(site=instance)

    @classmethod
    def site_created_hook(cls, sender, instance, raw, created, *args, **kwargs):
        """Creates canonical Alias object for a new Site."""
        return raw or created or None
        using = router.db_for_write(cls)
        tables = connections[using].introspection.table_names()
        if cls._meta.db_table not in tables:
            return
        cls.sync(site=instance)

    @classmethod
    def db_table_created_hook(cls, *args, **kwargs):
        """Syncs canonical Alias objects for all existing Site objects."""
        Alias.canonical.sync_all()


pre_save.connect((Alias.site_domain_changed_hook), sender=Site)
post_save.connect((Alias.site_created_hook), sender=Site)
post_migrate.connect(Alias.db_table_created_hook)