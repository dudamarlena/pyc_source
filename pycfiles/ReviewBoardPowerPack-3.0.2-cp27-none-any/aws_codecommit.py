# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/aws_codecommit.py
# Compiled at: 2019-06-17 15:11:31
"""Hosting service for AWS CodeCommit."""
from __future__ import unicode_literals
import boto3, botocore
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from reviewboard.hostingsvcs.errors import AuthorizationError, HostingServiceError, RepositoryError
from reviewboard.hostingsvcs.forms import HostingServiceAuthForm, HostingServiceForm
from reviewboard.hostingsvcs.service import HostingService
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError
from rbpowerpack.utils.extension import get_powerpack_extension

class AWSCodeCommitAuthForm(HostingServiceAuthForm):
    """Authentication configuration form for AWS CodeCommit."""

    class Meta(object):
        labels = {b'hosting_account_username': b'AWS access key ID', 
           b'hosting_account_password': b'AWS secret access key'}
        help_texts = {b'hosting_account_username': _(b'The access key ID for an IAM user who has access to the repositories being configured. We recommend a dedicated IAM user used solely for Review Board.'), 
           b'hosting_account_password': _(b'The secret access key for an IAM user who has access to the repositories being configured. This will be stored in an encrypted format.')}


class AWSCodeCommitForm(HostingServiceForm):
    """Configuration form for AWS CodeCommit."""
    aws_codecommit_region = forms.CharField(label=_(b'AWS region'), max_length=32, required=True, widget=forms.TextInput(attrs={b'size': 20}), help_text=_(b'The AWS region (e.g., us-east-1) for your CodeCommit repository.'))
    aws_codecommit_repo_name = forms.CharField(label=_(b'Repository name'), max_length=64, required=True, widget=forms.TextInput(attrs={b'size': b'60'}), help_text=_(b'The name of the repository as configured on CodeCommit. This is the same value you would find as part of the clone URL.'))


class AWSCodeCommit(HostingService):
    """Hosting service for AWS CodeCommit.

    This supports posting changes against CodeCommit repositories.

    Currently it does not support post-commit review. We're limited only by the
    lack of a commit log API.
    """
    name = b'AWS CodeCommit'
    needs_authorization = True
    supports_repositories = True
    supported_scmtools = [b'Git']
    supports_post_commit = False
    auth_form = AWSCodeCommitAuthForm
    form = AWSCodeCommitForm
    repository_fields = {b'Git': {b'path': b'https://git-codecommit.%(aws_codecommit_region)s.amazonaws.com/v1/repos/%(aws_codecommit_repo_name)s', 
                b'mirror_path': b'ssh://git-codecommit.%(aws_codecommit_region)s.amazonaws.com/v1/repos/%(aws_codecommit_repo_name)s'}}

    def __init__(self, *args, **kwargs):
        """Initialize the hosting service.

        Args:
            *args (tuple):
                Positional arguments passed to the constructor.

            **kwargs (dict):
                Keyword arguments passed to the constructor.
        """
        super(AWSCodeCommit, self).__init__(*args, **kwargs)
        self._boto_client = None
        return

    def can_user_post(self, user, repository):
        """Return whether a user can post against the given repository.

        This will check the extension's policy to ensure that the user
        is permitted to post.

        Args:
            user (django.contrib.auth.models.User):
                The user attempting to post a change.

            repository (reviewboard.scmtools.models.Repository):
                The repository being posted against.

        Returns:
            bool:
            ``True`` if the user can post a change, based on license
            settings. ``False`` if they cannot.
        """
        extension = get_powerpack_extension()
        return extension is not None and extension.policy.is_aws_codecommit_enabled(user, repository)

    def check_repository(self, aws_codecommit_region, aws_codecommit_repo_name, *args, **kwargs):
        """Check the validity of a repository.

        This performs a check against the hosting service to ensure that the
        information provided by the user represents a valid repository.

        Args:
            aws_codecommit_region (unicode):
                The region that the CodeCommit repository resides in.

            aws_codecommit_repo_name (unicode):
                The name of the CodeCommit repository.

            *args (tuple):
                Additional positional arguments passed by the caller.

            **kwargs (dict):
                Additional keyword arguments passed by the caller. This
                includes all field data from the HostingServiceForm.

        Raises:
            reviewboard.hostingsvcs.errors.HostingServiceError:
                An error occurred communicating with the hosting service.

            reviewboard.hostingsvcs.errors.RepositoryError:
                An error occurred when trying to verify the repository.
        """
        client = self._get_boto_client(aws_codecommit_region)
        try:
            client.get_repository(repositoryName=aws_codecommit_repo_name)
        except client.exceptions.RepositoryDoesNotExistException:
            raise RepositoryError(ugettext(b'The repository "%(repo_name)s" was not found in region "%(region)s".') % {b'repo_name': aws_codecommit_repo_name, 
               b'region': aws_codecommit_region})
        except Exception as e:
            raise HostingServiceError(ugettext(b'Error fetching information on the CodeCommit repository "%(repo_name)s": %(error)s') % {b'repo_name': aws_codecommit_repo_name, 
               b'error': e})

    def authorize(self, username, password, aws_codecommit_region, *args, **kwargs):
        """Authorize an account for the hosting service.

        Args:
            username (unicode):
                The AWS Access Key ID used for the account.

            password (unicode):
                The AWS Secret Access Key used for the account.

            aws_codecommit_region (unicode):
                The region that the CodeCommit repository resides in.

            *args (tuple):
                Extra unused positional arguments.

            **kwargs (dict):
                Extra keyword arguments containing values from the repository's
                configuration.

        Raises:
            reviewboard.hostingsvcs.errors.AuthorizationError:
                The credentials provided were not valid.

            reviewboard.hostingsvcs.errors.HostingServiceError:
                An error occurred communicating with the hosting service.
        """
        self.account.data[b'password'] = encrypt_password(password)
        client = self._get_boto_client(aws_codecommit_region)
        try:
            client.list_repositories()
        except Exception as e:
            del self.account.data[b'password']
            if isinstance(e, botocore.exceptions.ClientError):
                raise AuthorizationError(ugettext(b'Unable to communicate with CodeCommit using the provided credentials. Check to make sure your IAM user has access to the repository and that the region is correct.'))
            else:
                raise HostingServiceError(ugettext(b'Unexpected error authenticating with Amazon: %s') % e)

        self.account.save()

    def is_authorized(self):
        """Return whether or not the hosting service account is authorized.

        An account is authorized if it has a Secret Access Key stored in the
        account data.

        Returns:
            bool:
            True if the account has been successfully authorized.
        """
        return self.account.data.get(b'password') is not None

    def get_file(self, repository, path, revision, *args, **kwargs):
        """Retrieve a file from the repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            path (unicode):
                The path of the file to fetch.

            revision (unicode):
                The revision of the file to fetch.

            *args (tuple):
                Additional positional arguments passed by the caller.

            **kwargs (tuple):
                Additional keyword arguments passed by the caller.

        Returns:
            bytes:
            The contents of the file at the given revision.

        Raises:
            reviewboard.scmtools.errors.FileNotFoundError:
                The file did not exist at the given revision.
        """
        client = self._get_boto_client(self._get_repository_region(repository))
        repo_name = repository.extra_data[b'aws_codecommit_repo_name']
        try:
            rsp = client.get_blob(repositoryName=repo_name, blobId=revision)
        except client.exceptions.BlobIdDoesNotExistException:
            raise FileNotFoundError(path, revision=revision)

        return rsp[b'content'].encode(b'utf-8')

    def get_file_exists(self, repository, path, revision, *args, **kwargs):
        """Return whether or not a file exists at a given revision.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The repository.

            path (unicode):
                The path of the file to check for existence.

            revision (unicode):
                The revision of the file.

            *args (tuple):
                Additional positional arguments passed by the caller.

            **kwargs (tuple):
                Additional keyword arguments passed by the caller.

        Returns:
            bool:
            True if the file exists at the given revision.
        """
        try:
            repository.get_file(path, revision)
        except FileNotFoundError:
            return False

        return True

    def _get_boto_client(self, region):
        """Return a client connection for CodeCommit.

        Args:
            region (unicode):
                The AWS region for the CodeCommit repository.

        Returns:
            botocore.client.CodeCommit:
            The CodeCommit client to use for requests.
        """
        if not self._boto_client or self._boto_client.meta.region_name != region:
            self._boto_client = boto3.client(b'codecommit', region_name=region, aws_access_key_id=self.account.username, aws_secret_access_key=decrypt_password(self.account.data[b'password']))
        return self._boto_client

    def _get_repository_region(self, repository):
        """Return the AWS region for a given repository.

        Args:
            repository (reviewboard.scmtools.models.Repository):
                The configured CodeCommit repository.

        Returns:
            unicode:
            The AWS region for the repository.
        """
        return repository.extra_data[b'aws_codecommit_region']