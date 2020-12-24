# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/hostingsvcs/tests/test_aws_codecommit.py
# Compiled at: 2019-06-17 15:11:31
"""Unit test for rbpowerpack.hostingsvcs.aws_codecommit."""
from __future__ import unicode_literals
from botocore.exceptions import ClientError
from djblets.testing.decorators import add_fixtures
from reviewboard.hostingsvcs.errors import AuthorizationError, HostingServiceError, RepositoryError
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.hostingsvcs.service import get_hosting_service, register_hosting_service, unregister_hosting_service
from reviewboard.scmtools.crypto_utils import decrypt_password, encrypt_password
from reviewboard.scmtools.errors import FileNotFoundError
from rbpowerpack.hostingsvcs.aws_codecommit import AWSCodeCommit
from rbpowerpack.hostingsvcs.tests.testcases import ServiceTests

class DummyCodeCommitClient(object):

    class exceptions:

        class BlobIdDoesNotExistException(ClientError):
            pass

        class RepositoryDoesNotExistException(ClientError):
            pass

    def get_blob(self, repositoryName, blobId):
        pass

    def get_repository(self, repositoryName):
        pass

    def list_repositories(self):
        pass


class AWSCodeCommitTests(ServiceTests):
    """Unit tests for the AWSCodeCommit hosting service."""
    service_name = b'aws-codecommit'

    def setUp(self):
        register_hosting_service(self.service_name, AWSCodeCommit)
        self.service_class = get_hosting_service(self.service_name)
        self.boto_client = DummyCodeCommitClient()
        super(AWSCodeCommitTests, self).setUp()

    def tearDown(self):
        super(AWSCodeCommitTests, self).tearDown()
        unregister_hosting_service(self.service_name)

    def test_service_support(self):
        """Testing AWSCodeCommit service support capabilities"""
        self.assertTrue(self.service_class.supports_repositories)
        self.assertFalse(self.service_class.supports_bug_trackers)
        self.assertFalse(self.service_class.supports_post_commit)

    def test_field_values(self):
        """Testing AWSCodeCommit repository form values"""
        fields = self._get_repository_fields(b'Git', fields={b'aws_codecommit_region': b'us-east-1', 
           b'aws_codecommit_repo_name': b'myrepo'})
        self.assertEqual(fields[b'path'], b'https://git-codecommit.us-east-1.amazonaws.com/v1/repos/myrepo')
        self.assertEqual(fields[b'mirror_path'], b'ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/myrepo')

    def test_authorize(self):
        """Testing AWSCodeCommit.authorize"""
        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        self.assertFalse(account.is_authorized)
        service = account.service
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.list_repositories)
        service.authorize(username=b'ABCDEF12345', password=b'ZZ9PZA', aws_codecommit_region=b'us-east-1')
        self.assertTrue(account.is_authorized)
        self.assertTrue(self.boto_client.list_repositories.called)
        account = HostingServiceAccount.objects.get(pk=account.pk)
        self.assertIn(b'password', account.data)
        self.assertEqual(decrypt_password(account.data[b'password']), b'ZZ9PZA')

    def test_authorize_with_client_error(self):
        """Testing AWSCodeCommit.authorize with ClientError"""

        def list_repositories(*args):
            raise ClientError({}, b'ListRepositories')

        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        self.assertFalse(account.is_authorized)
        service = account.service
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.list_repositories, call_fake=list_repositories)
        expected_message = b'Unable to communicate with CodeCommit using the provided credentials. Check to make sure your IAM user has access to the repository and that the region is correct.'
        with self.assertRaisesMessage(AuthorizationError, expected_message):
            service.authorize(username=b'ABCDEF12345', password=b'ZZ9PZA', aws_codecommit_region=b'us-east-1')
        self.assertFalse(account.is_authorized)
        self.assertTrue(self.boto_client.list_repositories.called)
        self.assertNotIn(b'password', account.data)

    def test_authorize_with_exception(self):
        """Testing AWSCodeCommit.authorize with Exception"""

        def list_repositories(*args):
            raise Exception(b'oh no!')

        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        self.assertFalse(account.is_authorized)
        service = account.service
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.list_repositories, call_fake=list_repositories)
        expected_message = b'Unexpected error authenticating with Amazon: oh no!'
        with self.assertRaisesMessage(HostingServiceError, expected_message):
            service.authorize(username=b'ABCDEF12345', password=b'ZZ9PZA', aws_codecommit_region=b'us-east-1')
        self.assertFalse(account.is_authorized)
        self.assertTrue(self.boto_client.list_repositories.called)
        self.assertNotIn(b'password', account.data)

    def test_check_repository(self):
        """Testing AWSCodeCommit.check_repository"""
        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        account.data[b'password'] = encrypt_password(b'ZZ9PZA')
        service = account.service
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.get_repository)
        service.check_repository(aws_codecommit_region=b'us-east-1', aws_codecommit_repo_name=b'myrepo')
        self.assertTrue(self.boto_client.get_repository.called_with(repositoryName=b'myrepo'))

    def test_check_repository_with_repo_does_not_exist(self):
        """Testing AWSCodeCommit.check_repository with invalid repository"""

        def get_repository(cls, repositoryName):
            raise self.boto_client.exceptions.RepositoryDoesNotExistException({}, b'GetRepository')

        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        account.data[b'password'] = encrypt_password(b'ZZ9PZA')
        service = account.service
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.get_repository, call_fake=get_repository)
        expected_message = b'The repository "myrepo" was not found in region "us-east-1".'
        with self.assertRaisesMessage(RepositoryError, expected_message):
            service.check_repository(aws_codecommit_region=b'us-east-1', aws_codecommit_repo_name=b'myrepo')

    def test_check_repository_with_exception(self):
        """Testing AWSCodeCommit.check_repository with unexpected exception"""

        def get_repository(cls, repositoryName):
            raise Exception(b'oh no!')

        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        account.data[b'password'] = encrypt_password(b'ZZ9PZA')
        service = account.service
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.get_repository, call_fake=get_repository)
        expected_message = b'Error fetching information on the CodeCommit repository "myrepo": oh no!'
        with self.assertRaisesMessage(HostingServiceError, expected_message):
            service.check_repository(aws_codecommit_region=b'us-east-1', aws_codecommit_repo_name=b'myrepo')

    @add_fixtures([b'test_scmtools'])
    def test_get_file(self):
        """Testing AWSCodeCommit.get_file"""
        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        account.data[b'password'] = encrypt_password(b'ZZ9PZA')
        service = account.service
        repository = self.create_repository(hosting_account=account)
        repository.extra_data.update({b'aws_codecommit_repo_name': b'myrepo', 
           b'aws_codecommit_region': b'us-east-1'})
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.get_blob, call_fake=lambda *args, **kwargs: {b'content': b'This is a test, and here is some unicode: ⊜'})
        content = service.get_file(repository=repository, path=b'/path', revision=b'abc123')
        self.assertIsInstance(content, bytes)
        self.assertEqual(content, b'This is a test, and here is some unicode: ⊜')

    @add_fixtures([b'test_scmtools'])
    def test_get_file_with_not_found(self):
        """Testing AWSCodeCommit.get_file with file not found"""

        def get_file(cls, repositoryName, blobId):
            raise self.boto_client.exceptions.BlobIdDoesNotExistException({}, b'GetBlob')

        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        account.data[b'password'] = encrypt_password(b'ZZ9PZA')
        service = account.service
        repository = self.create_repository(hosting_account=account)
        repository.extra_data.update({b'aws_codecommit_repo_name': b'myrepo', 
           b'aws_codecommit_region': b'us-east-1'})
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.get_blob, call_fake=get_file)
        with self.assertRaises(FileNotFoundError) as (cm):
            service.get_file(repository=repository, path=b'/path', revision=b'abc123')
            self.assertEqual(cm.exception.path, b'/path')
            self.assertEqual(cm.exception.revision, b'abc123')

    @add_fixtures([b'test_scmtools'])
    def test_get_file_exists_with_exists(self):
        """Testing AWSCodeCommit.get_file_exists with file exists"""
        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        account.data[b'password'] = encrypt_password(b'ZZ9PZA')
        service = account.service
        repository = self.create_repository(hosting_account=account)
        repository.extra_data.update({b'aws_codecommit_repo_name': b'myrepo', 
           b'aws_codecommit_region': b'us-east-1'})
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.get_blob, call_fake=lambda *args, **kwargs: {b'content': b'This is a test'})
        self.assertTrue(service.get_file_exists(repository=repository, path=b'/path', revision=b'abc123'))

    @add_fixtures([b'test_scmtools'])
    def test_get_file_exists_with_not_exists(self):
        """Testing AWSCodeCommit.get_file_exists with file doesn't exist"""

        def get_file(cls, repositoryName, blobId):
            raise self.boto_client.exceptions.BlobIdDoesNotExistException({}, b'GetBlob')

        account = HostingServiceAccount(service_name=self.service_name, username=b'ABCDEF12345')
        account.data[b'password'] = encrypt_password(b'ZZ9PZA')
        service = account.service
        repository = self.create_repository(hosting_account=account)
        repository.extra_data.update({b'aws_codecommit_repo_name': b'myrepo', 
           b'aws_codecommit_region': b'us-east-1'})
        self.spy_on(service._get_boto_client, call_fake=lambda *args, **kwargs: self.boto_client)
        self.spy_on(self.boto_client.get_blob, call_fake=get_file)
        self.assertFalse(service.get_file_exists(repository=repository, path=b'/path', revision=b'abc123'))