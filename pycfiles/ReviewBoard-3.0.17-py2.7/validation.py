# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/validation.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from djblets.util.decorators import augment_method_from
from djblets.webapi.resources.root import RootResource as DjbletsRootResource
from reviewboard.webapi.decorators import webapi_check_local_site, webapi_check_login_required
from reviewboard.webapi.base import RBResourceMixin
from reviewboard.webapi.resources import resources

class ValidationResource(RBResourceMixin, DjbletsRootResource):
    """Links to validation resources."""
    added_in = b'2.0'
    name = b'validation'

    def __init__(self, *args, **kwargs):
        super(ValidationResource, self).__init__([
         resources.validate_diff], include_uri_templates=False, *args, **kwargs)

    @webapi_check_login_required
    @webapi_check_local_site
    @augment_method_from(DjbletsRootResource)
    def get(self, request, *args, **kwargs):
        """Retrieves links to all the validation resources."""
        pass


validation_resource = ValidationResource()