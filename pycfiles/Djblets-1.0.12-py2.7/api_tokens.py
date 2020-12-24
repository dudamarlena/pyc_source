# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/resources/mixins/api_tokens.py
# Compiled at: 2019-06-12 01:17:17
"""Mixins for integrating token-based authentication into an API."""
from __future__ import unicode_literals
from django.contrib import auth
from django.utils import six
from djblets.webapi.errors import PERMISSION_DENIED

class ResourceAPITokenMixin(object):
    """Augments a WebAPIResource to support API tokens.

    Any WebAPIResource subclass making use of this mixin can accept requests
    backed by an API token, and will restrict the request to that token's
    policy.

    It's recommended that all resources in a project inherit from a base
    resource that inherits both from this mixin and from WebAPIResource. The
    subclass must provide, at a minimum, a value for
    :py:attr:`api_token_model`.
    """
    api_token_model = None
    api_token_access_allowed = True

    @property
    def policy_id(self):
        """Return the ID used for access policies.

        This defaults to the name of the resource, but can be overridden
        in case the name is not specific enough or there's a conflict.
        """
        return self.name

    def call_method_view(self, request, method, view, *args, **kwargs):
        """Check token access policies and call the API method handler.

        If the client has authenticated with an API token, the token's
        access policies will be checked before invoking the API method
        handler. If the policy disallows this operation, a
        ``PERMISSION_DENIED`` error will be returned.
        """
        webapi_token = self.__get_api_token_for_request(request)
        if webapi_token:
            if not self.api_token_access_allowed:
                return PERMISSION_DENIED
            policy = webapi_token.policy
            resources_policy = policy.get(b'resources')
            if resources_policy:
                resource_id = kwargs.get(self.uri_object_key)
                if not self.is_resource_method_allowed(resources_policy, method, resource_id):
                    return PERMISSION_DENIED
        return super(ResourceAPITokenMixin, self).call_method_view(request, method, view, *args, **kwargs)

    def is_resource_method_allowed(self, resources_policy, method, resource_id):
        """Return whether a method can be performed on a resource.

        A method can be performed if a specific per-resource policy allows
        it, and the global policy also allows it.

        The per-resource policy takes precedence over the global policy.
        If, for instance, the global policy blocks and the resource policies
        allows, the method will be allowed.

        If no policies apply to this, then the default is to allow.
        """
        resource_policy = resources_policy.get(self.policy_id)
        if resource_policy:
            permission = self.__check_resource_policy(resource_policy, method, [resource_id, b'*'])
            if permission is not None:
                return permission
        if b'*' in resources_policy:
            permission = self.__check_resource_policy(resources_policy, method, [b'*'])
            if permission is not None:
                return permission
        return True

    def __check_resource_policy(self, policy, method, keys):
        """Check the policy for a specific resource and method.

        This will grab the resource policy for the given policy ID,
        and see if a given method can be performed on that resource,
        without factoring in any global policy rules.

        If the method is allowed and ``restrict_ids`` is ``True``, this will
        then check if the resource should be blocked based on the ID.

        In case of a conflict, blocked policies always trump allowed
        policies.
        """
        for key in keys:
            sub_policy = policy.get(key)
            if sub_policy:
                allowed = sub_policy.get(b'allow', [])
                blocked = sub_policy.get(b'block', [])
                if method in blocked:
                    return False
                if method in allowed:
                    return True
                if b'*' in blocked:
                    return False
                if b'*' in allowed:
                    return True

        return

    def __get_api_token_for_request(self, request):
        webapi_token = getattr(request, b'_webapi_token', None)
        if not webapi_token:
            webapi_token_id = request.session.get(b'webapi_token_id')
            if webapi_token_id:
                try:
                    webapi_token = self.api_token_model.objects.get(pk=webapi_token_id, user=request.user)
                except self.api_token_model.DoesNotExist:
                    auth.logout(request)

                request._webapi_token = webapi_token
        return webapi_token

    def _get_queryset(self, request, is_list=False, *args, **kwargs):
        """Return the queryset for the resource.

        This is a specialization of :py:meth:`WebAPIResource._get_queryset()`,
        which imposes further restrictions on the queryset results if using
        a WebAPIToken for authentication that defines a policy.

        Any items in the queryset that are denied by the policy will be
        excluded from the results.
        """
        queryset = super(ResourceAPITokenMixin, self)._get_queryset(request, is_list=is_list, *args, **kwargs)
        if is_list:
            webapi_token = self.__get_api_token_for_request(request)
            if webapi_token:
                resources_policy = webapi_token.policy.get(b'resources', {})
                resource_policy = resources_policy.get(self.policy_id)
                if resource_policy:
                    resource_ids = [ resource_id for resource_id in six.iterkeys(resource_policy) if resource_id != b'*' and not self.__check_resource_policy(resources_policy, self.policy_id, b'GET', resource_id, True)
                                   ]
                    if resource_ids:
                        queryset = queryset.exclude(**{self.model_object_key + b'__in': resource_ids})
        return queryset