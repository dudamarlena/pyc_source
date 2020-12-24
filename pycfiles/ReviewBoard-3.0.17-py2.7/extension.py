# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/extension.py
# Compiled at: 2020-02-11 04:03:57
"""Review Board's extension resource."""
from djblets.extensions.resources import ExtensionResource as DjbletsExtensionResource
from djblets.util.decorators import augment_method_from
from reviewboard.extensions.base import get_extension_manager
from reviewboard.webapi.base import RBResourceMixin
from reviewboard.webapi.decorators import webapi_check_local_site, webapi_check_login_required

class ExtensionResource(RBResourceMixin, DjbletsExtensionResource):
    """Review Board's extension resource.

    This resource special-cases the one in Djblets to provide API token and
    OAuth token access.
    """

    @webapi_check_login_required
    @webapi_check_local_site
    @augment_method_from(DjbletsExtensionResource)
    def get(self, *args, **kwargs):
        pass

    @webapi_check_login_required
    @webapi_check_local_site
    @augment_method_from(DjbletsExtensionResource)
    def get_list(self, *args, **kwargs):
        pass

    @webapi_check_local_site
    @augment_method_from(DjbletsExtensionResource)
    def update(self, *args, **kwargs):
        pass

    def has_modify_permissions(self, request, extension, *args, **kwargs):
        """Return whether the user has access to modify this extension.

        Args:
            request (django.http.HttpRequest):
                The request.

            extension (reviewboard.extensions.base.Extension):
                The extension being modified.

            *args (tuple, unused):
                Additional positional arguments.

            **kwargs (dict, unused):
                Additional keyword arguments.

        Returns:
            bool:
            True, always. Individual permissions checks will be done via the
            :py:func:`djblets.webapi.decorators.webapi_permission_required`
            decorator.
        """
        return True


extension_resource = ExtensionResource(get_extension_manager())