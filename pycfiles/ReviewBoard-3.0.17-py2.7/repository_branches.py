# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/repository_branches.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from djblets.webapi.decorators import webapi_response_errors
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.hostingsvcs.errors import HostingServiceError
from reviewboard.scmtools.errors import SCMError
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_login_required, webapi_check_local_site
from reviewboard.webapi.errors import REPO_INFO_ERROR, REPO_NOT_IMPLEMENTED
from reviewboard.webapi.resources import resources

class RepositoryBranchesResource(WebAPIResource):
    """Provides information on the branches in a repository.

    Data on branches will not be available for all types of repositories.
    """
    added_in = b'2.0'
    name = b'branches'
    policy_id = b'repository_branches'
    singleton = True
    allowed_methods = ('GET', )
    mimetype_item_resource_name = b'repository-branches'
    fields = {b'id': {b'type': six.text_type, 
               b'description': b'The ID of the branch. This is specific to the type of repository.'}, 
       b'name': {b'type': six.text_type, 
                 b'description': b'The name of the branch.'}, 
       b'commit': {b'type': six.text_type, 
                   b'description': b'The revision identifier of the commit.\n\nThe format depends on the repository type (it may be a number, SHA-1 hash, or some other type). This should be treated as a relatively opaque value, but can be used as the ``start`` parameter to the :ref:`webapi2.0-repository-commits-resource`.'}, 
       b'default': {b'type': bool, 
                    b'description': b'If set, this branch is considered the "tip" of the repository. It would represent "master" for Git repositories, "trunk" for Subversion, etc.\n\nThis will be ``true`` for exactly one of the results only. All others will be ``false``.'}}

    @webapi_check_local_site
    @webapi_check_login_required
    @webapi_response_errors(DOES_NOT_EXIST, REPO_INFO_ERROR, REPO_NOT_IMPLEMENTED)
    def get(self, request, *args, **kwargs):
        """Retrieves an array of the branches in a repository."""
        try:
            repository = resources.repository.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        try:
            branches = []
            for branch in repository.get_branches():
                branches.append({b'id': branch.id, 
                   b'name': branch.name, 
                   b'commit': branch.commit, 
                   b'default': branch.default})

            return (
             200,
             {self.item_result_key: branches})
        except (HostingServiceError, SCMError) as e:
            return REPO_INFO_ERROR.with_message(six.text_type(e))
        except NotImplementedError:
            return REPO_NOT_IMPLEMENTED


repository_branches_resource = RepositoryBranchesResource()