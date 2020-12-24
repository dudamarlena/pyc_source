# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thomas/Dev/Project/django-trusts/trusts/models.py
# Compiled at: 2016-04-16 22:35:57
from __future__ import unicode_literals
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import signals, Q, options
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from trusts import ENTITY_MODEL_NAME, PERMISSION_MODEL_NAME, GROUP_MODEL_NAME, DEFAULT_SETTLOR, ALLOW_NULL_SETTLOR, ROOT_PK, utils
options.DEFAULT_NAMES += ('roles', 'permission_conditions', 'content_roles', 'content_permission_conditions')

class TrustManager(models.Manager):

    def get_or_create_settlor_default(self, settlor, defaults={}, **kwargs):
        if b'trust' in kwargs:
            raise TypeError(b'"%s" are invalid keyword arguments' % b'trust')
        if settlor is None:
            raise ValueError(b'"settlor" must has a value.')
        if settlor.is_anonymous():
            raise ValueError(b'Anonymous is not yet supported.')
        try:
            return (
             self.get(settlor=settlor, title=b'', **kwargs), False)
        except Trust.DoesNotExist:
            params = {k:v for k, v in kwargs.items() if b'__' not in k if b'__' not in k}
            params.update(defaults)
            params.update({b'title': b'', b'trust_id': ROOT_PK})
            trust = self.model(**params)
            trust.save()
            return (trust, True)

        return

    def get_root(self):
        return self.get(pk=ROOT_PK)

    def filter_by_content(self, obj):
        if isinstance(obj, models.QuerySet):
            klass = obj.model
            is_qs = True
        else:
            klass = obj.__class__
            is_qs = False
        if Content.is_content_model(klass):
            fieldlookup = Content.get_content_fieldlookup(klass)
            if fieldlookup is None:
                fieldlookup = b'%s_content' % utils.get_short_model_name_lower(klass).replace(b'.', b'_')
            filters = {}
            if is_qs:
                filters[b'%s__in' % fieldlookup] = obj
            else:
                filters[fieldlookup] = obj
            return self.filter(**filters).distinct()
        else:
            return self.none()

    def filter_by_user_perm(self, user, **kwargs):
        if b'group__user' in kwargs:
            raise TypeError(b'"%s" are invalid keyword arguments' % b'group__user')
        return self.filter((Q(groups__user=user) | Q(trustees__entity=user)), **kwargs)


class ReadonlyFieldsMixin(object):

    def __init__(self, *args, **kwargs):
        super(ReadonlyFieldsMixin, self).__init__(*args, **kwargs)
        if hasattr(self, b'_readonly_fields'):
            self._state.init_fields = {field:getattr(self, field) for field in self._readonly_fields if hasattr(self, field)}

    def clean(self):
        super(ReadonlyFieldsMixin, self).clean()
        if hasattr(self, b'_readonly_fields') and hasattr(self._state, b'init_fields'):
            for field in self._readonly_fields:
                if field in self._state.init_fields:
                    saved_value = self._state.init_fields[field]
                    if saved_value != getattr(self, field):
                        raise ValidationError(b'Field "%s" is readonly.' % b'trust')


class Content(ReadonlyFieldsMixin, models.Model):
    trust = models.ForeignKey(b'trusts.Trust', related_name=b'%(app_label)s_%(class)s_content', default=ROOT_PK, null=False, blank=False)
    _contents = {}
    _conditions = {}

    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'read')
        permission_conditions = ()

    @staticmethod
    def register_permission_condition(klass, cond_code, func):
        short_name = utils.get_short_model_name(klass)
        if short_name not in Content._conditions:
            Content._conditions[short_name] = {}
        Content._conditions[short_name][cond_code] = func

    @staticmethod
    def register_content(klass, fieldlookup=None):
        if fieldlookup is None:
            content_model_fields = [ f for f in klass._meta.fields if f.rel is not None and f.name == b'trust' ]
            if len(content_model_fields) != 1:
                raise AttributeError(b'Expect "trust" field in model %s.' % short_name)
        short_name = utils.get_short_model_name(klass)
        Content._contents[short_name] = fieldlookup
        if hasattr(klass._meta, b'permission_conditions'):
            for permcond, func in klass._meta.permission_conditions:
                Content.register_permission_condition(klass, permcond, func)

        return

    @staticmethod
    def is_content_model(klass):
        short_name = utils.get_short_model_name(klass)
        if short_name in Content._contents.keys():
            return True
        return False

    @staticmethod
    def get_content_fieldlookup(klass):
        short_name = utils.get_short_model_name(klass)
        if short_name in Content._contents.keys():
            return Content._contents[short_name]
        else:
            return

    @staticmethod
    def is_content(obj):
        if isinstance(obj, models.QuerySet):
            klass = obj.model
            is_qs = True
        else:
            klass = obj.__class__
            is_qs = False
        return Content.is_content_model(klass)

    @staticmethod
    def get_permission_condition_func(klass, cond_code):
        short_name = utils.get_short_model_name(klass)
        if short_name in Content._conditions:
            if cond_code in Content._conditions[short_name]:
                return Content._conditions[short_name][cond_code]
        return


class Trust(Content):
    title = models.CharField(max_length=40, null=False, blank=False, verbose_name=_(b'title'))
    settlor = models.ForeignKey(ENTITY_MODEL_NAME, default=DEFAULT_SETTLOR, null=ALLOW_NULL_SETTLOR, blank=False)
    groups = models.ManyToManyField(GROUP_MODEL_NAME, related_name=b'trusts', verbose_name=_(b'groups'), help_text=_(b'The groups this trust grants permissions to. A user willget all permissions granted to each of his/her group.'))
    _readonly_fields = ('trust', 'settlor')
    objects = TrustManager()

    class Meta:
        unique_together = ('settlor', 'title')
        default_permissions = ('add', 'change', 'delete', 'read')
        permission_conditions = ((b'own', lambda u, p, o: u == o.settlor),)

    def __str__(self):
        settlor_str = b' of %s' % str(self.settlor) if self.settlor is not None else b''
        return b'Trust[%s]: "%s"' % (self.id, self.title)


Content.register_content(Trust)

class Role(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False, unique=True, help_text=_(b"The name of the role. Corresponds to the key of model's trusts option."))
    groups = models.ManyToManyField(GROUP_MODEL_NAME, related_name=b'roles', null=False, blank=False, verbose_name=_(b'groups'))
    permissions = models.ManyToManyField(PERMISSION_MODEL_NAME, through=b'trusts.RolePermission', related_name=b'roles', null=False, blank=False, verbose_name=_(b'permissions'))

    class Meta:
        pass


class RolePermission(models.Model):
    role = models.ForeignKey(b'trusts.Role', related_name=b'rolepermissions', null=False, blank=False)
    permission = models.ForeignKey(PERMISSION_MODEL_NAME, related_name=b'rolepermissions', null=False, blank=False)
    managed = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        unique_together = ('role', 'permission')


class TrustUserPermission(models.Model):
    trust = models.ForeignKey(b'trusts.Trust', related_name=b'trustees', null=False, blank=False)
    entity = models.ForeignKey(ENTITY_MODEL_NAME, related_name=b'trustpermissions', null=False, blank=False)
    permission = models.ForeignKey(PERMISSION_MODEL_NAME, related_name=b'trustentities', null=False, blank=False)

    class Meta:
        unique_together = ('trust', 'entity', 'permission')


class Junction(ReadonlyFieldsMixin, models.Model):
    trust = models.ForeignKey(b'trusts.Trust', related_name=b'%(app_label)s_%(class)s', default=ROOT_PK, null=False, blank=False)
    _readonly_fields = ('trust', )

    class Meta:
        abstract = True
        default_permissions = ()
        content_permission_conditions = ()
        unique_together = ('content', )

    @staticmethod
    def register_junction(klass, content_model=None):
        Content.register_content(klass.get_content_model(), klass.get_fieldlookup())
        if hasattr(klass._meta, b'content_permission_conditions'):
            for permcond, func in klass._meta.content_permission_conditions:
                Content.register_permission_condition(klass, permcond, func)

    @classmethod
    def get_content_model(cls):
        content_model_fields = [ f for f in cls._meta.fields if f.rel is not None and f.name != b'trust' ]
        if len(content_model_fields) == 1:
            return content_model_fields[0].rel.to
        else:
            raise NotImplementedError(b'Juctnion\'s classmethod "get_content_model" is not implemented.')
            return

    @classmethod
    def get_fieldlookup(cls):
        return b'%s__content' % utils.get_short_model_name_lower(cls).replace(b'.', b'_')


def register_content_junction(sender, **kwargs):
    if issubclass(sender, Junction):
        Junction.register_junction(sender)
    elif issubclass(sender, Content):
        Content.register_content(sender)


signals.class_prepared.connect(register_content_junction)