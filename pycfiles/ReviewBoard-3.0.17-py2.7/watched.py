# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/watched.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_login_required
from reviewboard.webapi.resources import resources

class WatchedResource(WebAPIResource):
    """
    Links to all Watched Items resources for the user.

    This is more of a linking resource rather than a data resource, much like
    the root resource is. The sole purpose of this resource is for easy
    navigation to the more specific Watched Items resources.
    """
    name = b'watched'
    singleton = True
    list_child_resources = [
     resources.watched_review_group,
     resources.watched_review_request]

    @webapi_check_login_required
    def get_list(self, request, *args, **kwargs):
        """Retrieves the list of Watched Items resources.

        Unlike most resources, the result of this resource is just a list of
        links, rather than any kind of data. It exists in order to index the
        more specific Watched Review Groups and Watched Review Requests
        resources.
        """
        return super(WatchedResource, self).get_list(request, *args, **kwargs)


watched_resource = WatchedResource()