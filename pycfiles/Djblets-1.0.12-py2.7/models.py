# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/models.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import six, timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djblets.db.fields import JSONField
from djblets.webapi.managers import WebAPITokenManager
from djblets.webapi.signals import webapi_token_updated

@python_2_unicode_compatible
class BaseWebAPIToken(models.Model):
    """Base class for an access token used for authenticating with the API.

    Each token can be used to authenticate the token's owner with the API,
    without requiring a username or password to be provided. Tokens can
    be revoked, and new tokens added.

    Tokens can store policy information, which will later be used for
    restricting access to the API.
    """
    user = models.ForeignKey(User, related_name=b'webapi_tokens', on_delete=models.CASCADE)
    token = models.CharField(max_length=40, unique=True)
    time_added = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True)
    policy = JSONField(null=True)
    extra_data = JSONField(null=True)
    objects = WebAPITokenManager()

    def is_accessible_by(self, user):
        return user.is_superuser or self.user == user

    def is_mutable_by(self, user):
        return user.is_superuser or self.user == user

    def is_deletable_by(self, user):
        return user.is_superuser or self.user == user

    def __str__(self):
        return b'Web API token for %s' % self.user

    def save(self, *args, **kwargs):
        """Save the token.

        If the token is being updated, the
        :py:data:`~djblets.webapi.signals.webapi_token_updated` signal will be
        emitted.

        Args:
            *args (tuple):
                Positional arguments to pass to the superclass.

            **kwargs (dict):
                Keyword arguments to pass to the superclass.
        """
        is_new = self.pk is None
        super(BaseWebAPIToken, self).save(*args, **kwargs)
        if not is_new:
            webapi_token_updated.send(instance=self, sender=type(self))
        return

    @classmethod
    def get_root_resource(self):
        raise NotImplementedError

    @classmethod
    def validate_policy(cls, policy):
        """Validate an API policy.

        This will check to ensure that the policy is in a suitable format
        and contains the information required in a format that can be parsed.

        If a failure is found, a ValidationError will be raised describing
        the error and where it was found.
        """
        if not isinstance(policy, dict):
            raise ValidationError(_(b'The policy must be a JSON object.'))
        if not policy:
            return
        if b'resources' not in policy:
            raise ValidationError(_(b'The policy is missing a "resources" section.'))
        resources_section = policy[b'resources']
        if not isinstance(resources_section, dict):
            raise ValidationError(_(b'The policy\'s "resources" section must be a JSON object.'))
        if not resources_section:
            raise ValidationError(_(b'The policy\'s "resources" section must not be empty.'))
        if b'*' in resources_section:
            cls._validate_policy_section(resources_section, b'*', b'resources.*')
        resource_policies = [ (section_name, section) for section_name, section in six.iteritems(resources_section) if section_name != b'*'
                            ]
        if resource_policies:
            valid_policy_ids = cls._get_valid_policy_ids(cls.get_root_resource())
            for policy_id, section in resource_policies:
                if policy_id not in valid_policy_ids:
                    raise ValidationError(_(b'"%s" is not a valid resource policy ID.') % policy_id)
                for subsection_name, subsection in six.iteritems(section):
                    if not isinstance(subsection_name, six.text_type):
                        raise ValidationError(_(b'%s must be a string in "resources.%s"') % (
                         subsection_name, policy_id))
                    cls._validate_policy_section(section, subsection_name, b'resources.%s.%s' % (policy_id, subsection_name))

    @classmethod
    def _validate_policy_section(cls, parent_section, section_name, full_section_name):
        section = parent_section[section_name]
        if not isinstance(section, dict):
            raise ValidationError(_(b'The "%s" section must be a JSON object.') % full_section_name)
        if b'allow' not in section and b'block' not in section:
            raise ValidationError(_(b'The "%s" section must have "allow" and/or "block" rules.') % full_section_name)
        if b'allow' in section and not isinstance(section[b'allow'], list):
            raise ValidationError(_(b'The "%s" section\'s "allow" rule must be a list.') % full_section_name)
        if b'block' in section and not isinstance(section[b'block'], list):
            raise ValidationError(_(b'The "%s" section\'s "block" rule must be a list.') % full_section_name)

    @classmethod
    def _get_valid_policy_ids(cls, resource, result=None):
        if result is None:
            result = set()
        if hasattr(resource, b'policy_id'):
            result.add(resource.policy_id)
        for child_resource in resource.list_child_resources:
            cls._get_valid_policy_ids(child_resource, result)

        for child_resource in resource.item_child_resources:
            cls._get_valid_policy_ids(child_resource, result)

        return result

    class Meta:
        abstract = True
        verbose_name = _(b'Web API token')
        verbose_name_plural = _(b'Web API tokens')