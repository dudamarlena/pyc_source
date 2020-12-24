# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/provider.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 20925 bytes
__doc__ = '\nThis class encapsulates the provider-specific header differences.\n'
import os
from boto.compat import six
from datetime import datetime
import boto
from boto import config
from boto.compat import expanduser
from boto.pyami.config import Config
from boto.gs.acl import ACL
from boto.gs.acl import CannedACLStrings as CannedGSACLStrings
from boto.s3.acl import CannedACLStrings as CannedS3ACLStrings
from boto.s3.acl import Policy
HEADER_PREFIX_KEY = 'header_prefix'
METADATA_PREFIX_KEY = 'metadata_prefix'
AWS_HEADER_PREFIX = 'x-amz-'
GOOG_HEADER_PREFIX = 'x-goog-'
ACL_HEADER_KEY = 'acl-header'
AUTH_HEADER_KEY = 'auth-header'
COPY_SOURCE_HEADER_KEY = 'copy-source-header'
COPY_SOURCE_VERSION_ID_HEADER_KEY = 'copy-source-version-id-header'
COPY_SOURCE_RANGE_HEADER_KEY = 'copy-source-range-header'
DELETE_MARKER_HEADER_KEY = 'delete-marker-header'
DATE_HEADER_KEY = 'date-header'
METADATA_DIRECTIVE_HEADER_KEY = 'metadata-directive-header'
RESUMABLE_UPLOAD_HEADER_KEY = 'resumable-upload-header'
SECURITY_TOKEN_HEADER_KEY = 'security-token-header'
STORAGE_CLASS_HEADER_KEY = 'storage-class'
MFA_HEADER_KEY = 'mfa-header'
SERVER_SIDE_ENCRYPTION_KEY = 'server-side-encryption-header'
VERSION_ID_HEADER_KEY = 'version-id-header'
RESTORE_HEADER_KEY = 'restore-header'
STORAGE_COPY_ERROR = 'StorageCopyError'
STORAGE_CREATE_ERROR = 'StorageCreateError'
STORAGE_DATA_ERROR = 'StorageDataError'
STORAGE_PERMISSIONS_ERROR = 'StoragePermissionsError'
STORAGE_RESPONSE_ERROR = 'StorageResponseError'
NO_CREDENTIALS_PROVIDED = object()

class ProfileNotFoundError(ValueError):
    pass


class Provider(object):
    CredentialMap = {'aws': ('aws_access_key_id', 'aws_secret_access_key', 'aws_security_token', 'aws_profile'), 
     'google': ('gs_access_key_id', 'gs_secret_access_key', None, None)}
    AclClassMap = {'aws': Policy, 
     'google': ACL}
    CannedAclsMap = {'aws': CannedS3ACLStrings, 
     'google': CannedGSACLStrings}
    HostKeyMap = {'aws': 's3', 
     'google': 'gs'}
    ChunkedTransferSupport = {'aws': False, 
     'google': True}
    MetadataServiceSupport = {'aws': True, 
     'google': False}
    HeaderInfoMap = {'aws': {HEADER_PREFIX_KEY: AWS_HEADER_PREFIX, 
             METADATA_PREFIX_KEY: AWS_HEADER_PREFIX + 'meta-', 
             ACL_HEADER_KEY: AWS_HEADER_PREFIX + 'acl', 
             AUTH_HEADER_KEY: 'AWS', 
             COPY_SOURCE_HEADER_KEY: AWS_HEADER_PREFIX + 'copy-source', 
             COPY_SOURCE_VERSION_ID_HEADER_KEY: AWS_HEADER_PREFIX + 'copy-source-version-id', 
             COPY_SOURCE_RANGE_HEADER_KEY: AWS_HEADER_PREFIX + 'copy-source-range', 
             DATE_HEADER_KEY: AWS_HEADER_PREFIX + 'date', 
             DELETE_MARKER_HEADER_KEY: AWS_HEADER_PREFIX + 'delete-marker', 
             METADATA_DIRECTIVE_HEADER_KEY: AWS_HEADER_PREFIX + 'metadata-directive', 
             RESUMABLE_UPLOAD_HEADER_KEY: None, 
             SECURITY_TOKEN_HEADER_KEY: AWS_HEADER_PREFIX + 'security-token', 
             SERVER_SIDE_ENCRYPTION_KEY: AWS_HEADER_PREFIX + 'server-side-encryption', 
             VERSION_ID_HEADER_KEY: AWS_HEADER_PREFIX + 'version-id', 
             STORAGE_CLASS_HEADER_KEY: AWS_HEADER_PREFIX + 'storage-class', 
             MFA_HEADER_KEY: AWS_HEADER_PREFIX + 'mfa', 
             RESTORE_HEADER_KEY: AWS_HEADER_PREFIX + 'restore'}, 
     'google': {HEADER_PREFIX_KEY: GOOG_HEADER_PREFIX, 
                METADATA_PREFIX_KEY: GOOG_HEADER_PREFIX + 'meta-', 
                ACL_HEADER_KEY: GOOG_HEADER_PREFIX + 'acl', 
                AUTH_HEADER_KEY: 'GOOG1', 
                COPY_SOURCE_HEADER_KEY: GOOG_HEADER_PREFIX + 'copy-source', 
                COPY_SOURCE_VERSION_ID_HEADER_KEY: GOOG_HEADER_PREFIX + 'copy-source-version-id', 
                COPY_SOURCE_RANGE_HEADER_KEY: None, 
                DATE_HEADER_KEY: GOOG_HEADER_PREFIX + 'date', 
                DELETE_MARKER_HEADER_KEY: GOOG_HEADER_PREFIX + 'delete-marker', 
                METADATA_DIRECTIVE_HEADER_KEY: GOOG_HEADER_PREFIX + 'metadata-directive', 
                RESUMABLE_UPLOAD_HEADER_KEY: GOOG_HEADER_PREFIX + 'resumable', 
                SECURITY_TOKEN_HEADER_KEY: GOOG_HEADER_PREFIX + 'security-token', 
                SERVER_SIDE_ENCRYPTION_KEY: None, 
                VERSION_ID_HEADER_KEY: GOOG_HEADER_PREFIX + 'version-id', 
                STORAGE_CLASS_HEADER_KEY: None, 
                MFA_HEADER_KEY: None, 
                RESTORE_HEADER_KEY: None}}
    ErrorMap = {'aws': {STORAGE_COPY_ERROR: boto.exception.S3CopyError, 
             STORAGE_CREATE_ERROR: boto.exception.S3CreateError, 
             STORAGE_DATA_ERROR: boto.exception.S3DataError, 
             STORAGE_PERMISSIONS_ERROR: boto.exception.S3PermissionsError, 
             STORAGE_RESPONSE_ERROR: boto.exception.S3ResponseError}, 
     'google': {STORAGE_COPY_ERROR: boto.exception.GSCopyError, 
                STORAGE_CREATE_ERROR: boto.exception.GSCreateError, 
                STORAGE_DATA_ERROR: boto.exception.GSDataError, 
                STORAGE_PERMISSIONS_ERROR: boto.exception.GSPermissionsError, 
                STORAGE_RESPONSE_ERROR: boto.exception.GSResponseError}}

    def __init__(self, name, access_key=None, secret_key=None, security_token=None, profile_name=None):
        self.host = None
        self.port = None
        self.host_header = None
        self.access_key = access_key
        self.secret_key = secret_key
        self.security_token = security_token
        self.profile_name = profile_name
        self.name = name
        self.acl_class = self.AclClassMap[self.name]
        self.canned_acls = self.CannedAclsMap[self.name]
        self._credential_expiry_time = None
        shared_path = os.path.join(expanduser('~'), '.' + name, 'credentials')
        self.shared_credentials = Config(do_load=False)
        if os.path.isfile(shared_path):
            self.shared_credentials.load_from_path(shared_path)
        self.get_credentials(access_key, secret_key, security_token, profile_name)
        self.configure_headers()
        self.configure_errors()
        host_opt_name = '%s_host' % self.HostKeyMap[self.name]
        if config.has_option('Credentials', host_opt_name):
            self.host = config.get('Credentials', host_opt_name)
        port_opt_name = '%s_port' % self.HostKeyMap[self.name]
        if config.has_option('Credentials', port_opt_name):
            self.port = config.getint('Credentials', port_opt_name)
        host_header_opt_name = '%s_host_header' % self.HostKeyMap[self.name]
        if config.has_option('Credentials', host_header_opt_name):
            self.host_header = config.get('Credentials', host_header_opt_name)

    def get_access_key(self):
        if self._credentials_need_refresh():
            self._populate_keys_from_metadata_server()
        return self._access_key

    def set_access_key(self, value):
        self._access_key = value

    access_key = property(get_access_key, set_access_key)

    def get_secret_key(self):
        if self._credentials_need_refresh():
            self._populate_keys_from_metadata_server()
        return self._secret_key

    def set_secret_key(self, value):
        self._secret_key = value

    secret_key = property(get_secret_key, set_secret_key)

    def get_security_token(self):
        if self._credentials_need_refresh():
            self._populate_keys_from_metadata_server()
        return self._security_token

    def set_security_token(self, value):
        self._security_token = value

    security_token = property(get_security_token, set_security_token)

    def _credentials_need_refresh(self):
        if self._credential_expiry_time is None:
            return False
        else:
            delta = self._credential_expiry_time - datetime.utcnow()
            seconds_left = (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 1000000) / 1000000
            if seconds_left < 300:
                boto.log.debug('Credentials need to be refreshed.')
                return True
            return False

    def get_credentials(self, access_key=None, secret_key=None, security_token=None, profile_name=None):
        access_key_name, secret_key_name, security_token_name, profile_name_name = self.CredentialMap[self.name]
        if profile_name is None and profile_name_name is not None and profile_name_name.upper() in os.environ:
            profile_name = os.environ[profile_name_name.upper()]
        shared = self.shared_credentials
        if access_key is not None:
            self.access_key = access_key
            boto.log.debug('Using access key provided by client.')
        else:
            if access_key_name.upper() in os.environ:
                self.access_key = os.environ[access_key_name.upper()]
                boto.log.debug('Using access key found in environment variable.')
            else:
                if profile_name is not None:
                    if shared.has_option(profile_name, access_key_name):
                        self.access_key = shared.get(profile_name, access_key_name)
                        boto.log.debug('Using access key found in shared credential file for profile %s.' % profile_name)
                    else:
                        if config.has_option('profile %s' % profile_name, access_key_name):
                            self.access_key = config.get('profile %s' % profile_name, access_key_name)
                            boto.log.debug('Using access key found in config file: profile %s.' % profile_name)
                        else:
                            raise ProfileNotFoundError('Profile "%s" not found!' % profile_name)
                else:
                    if shared.has_option('default', access_key_name):
                        self.access_key = shared.get('default', access_key_name)
                        boto.log.debug('Using access key found in shared credential file.')
                    else:
                        if config.has_option('Credentials', access_key_name):
                            self.access_key = config.get('Credentials', access_key_name)
                            boto.log.debug('Using access key found in config file.')
                        if secret_key is not None:
                            self.secret_key = secret_key
                            boto.log.debug('Using secret key provided by client.')
                        else:
                            if secret_key_name.upper() in os.environ:
                                self.secret_key = os.environ[secret_key_name.upper()]
                                boto.log.debug('Using secret key found in environment variable.')
                            else:
                                if profile_name is not None:
                                    if shared.has_option(profile_name, secret_key_name):
                                        self.secret_key = shared.get(profile_name, secret_key_name)
                                        boto.log.debug('Using secret key found in shared credential file for profile %s.' % profile_name)
                                    else:
                                        if config.has_option('profile %s' % profile_name, secret_key_name):
                                            self.secret_key = config.get('profile %s' % profile_name, secret_key_name)
                                            boto.log.debug('Using secret key found in config file: profile %s.' % profile_name)
                                        else:
                                            raise ProfileNotFoundError('Profile "%s" not found!' % profile_name)
                                else:
                                    if shared.has_option('default', secret_key_name):
                                        self.secret_key = shared.get('default', secret_key_name)
                                        boto.log.debug('Using secret key found in shared credential file.')
                                    else:
                                        if config.has_option('Credentials', secret_key_name):
                                            self.secret_key = config.get('Credentials', secret_key_name)
                                            boto.log.debug('Using secret key found in config file.')
                                        elif config.has_option('Credentials', 'keyring'):
                                            keyring_name = config.get('Credentials', 'keyring')
                                            try:
                                                import keyring
                                            except ImportError:
                                                boto.log.error('The keyring module could not be imported. For keyring support, install the keyring module.')
                                                raise

                                            self.secret_key = keyring.get_password(keyring_name, self.access_key)
                                            boto.log.debug('Using secret key found in keyring.')
                if security_token is not None:
                    self.security_token = security_token
                    boto.log.debug('Using security token provided by client.')
                elif security_token_name is not None and access_key is None and secret_key is None:
                    if security_token_name.upper() in os.environ:
                        self.security_token = os.environ[security_token_name.upper()]
                        boto.log.debug('Using security token found in environment variable.')
                    else:
                        if shared.has_option(profile_name or 'default', security_token_name):
                            self.security_token = shared.get(profile_name or 'default', security_token_name)
                            boto.log.debug('Using security token found in shared credential file.')
                        else:
                            if profile_name is not None:
                                if config.has_option('profile %s' % profile_name, security_token_name):
                                    boto.log.debug('config has option')
                                    self.security_token = config.get('profile %s' % profile_name, security_token_name)
                                    boto.log.debug('Using security token found in config file: profile %s.' % profile_name)
                            elif config.has_option('Credentials', security_token_name):
                                self.security_token = config.get('Credentials', security_token_name)
                                boto.log.debug('Using security token found in config file.')
        if (self._access_key is None or self._secret_key is None) and self.MetadataServiceSupport[self.name]:
            self._populate_keys_from_metadata_server()
        self._secret_key = self._convert_key_to_str(self._secret_key)

    def _populate_keys_from_metadata_server(self):
        boto.log.debug('Retrieving credentials from metadata server.')
        from boto.utils import get_instance_metadata
        timeout = config.getfloat('Boto', 'metadata_service_timeout', 1.0)
        attempts = config.getint('Boto', 'metadata_service_num_attempts', 1)
        metadata = get_instance_metadata(timeout=timeout, num_retries=attempts, data='meta-data/iam/security-credentials/')
        if metadata:
            security = list(metadata.values())[0]
            self._access_key = security['AccessKeyId']
            self._secret_key = self._convert_key_to_str(security['SecretAccessKey'])
            self._security_token = security['Token']
            expires_at = security['Expiration']
            self._credential_expiry_time = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M:%SZ')
            boto.log.debug('Retrieved credentials will expire in %s at: %s', self._credential_expiry_time - datetime.now(), expires_at)

    def _convert_key_to_str(self, key):
        if isinstance(key, six.text_type):
            return str(key)
        return key

    def configure_headers(self):
        header_info_map = self.HeaderInfoMap[self.name]
        self.metadata_prefix = header_info_map[METADATA_PREFIX_KEY]
        self.header_prefix = header_info_map[HEADER_PREFIX_KEY]
        self.acl_header = header_info_map[ACL_HEADER_KEY]
        self.auth_header = header_info_map[AUTH_HEADER_KEY]
        self.copy_source_header = header_info_map[COPY_SOURCE_HEADER_KEY]
        self.copy_source_version_id = header_info_map[COPY_SOURCE_VERSION_ID_HEADER_KEY]
        self.copy_source_range_header = header_info_map[COPY_SOURCE_RANGE_HEADER_KEY]
        self.date_header = header_info_map[DATE_HEADER_KEY]
        self.delete_marker = header_info_map[DELETE_MARKER_HEADER_KEY]
        self.metadata_directive_header = header_info_map[METADATA_DIRECTIVE_HEADER_KEY]
        self.security_token_header = header_info_map[SECURITY_TOKEN_HEADER_KEY]
        self.resumable_upload_header = header_info_map[RESUMABLE_UPLOAD_HEADER_KEY]
        self.server_side_encryption_header = header_info_map[SERVER_SIDE_ENCRYPTION_KEY]
        self.storage_class_header = header_info_map[STORAGE_CLASS_HEADER_KEY]
        self.version_id = header_info_map[VERSION_ID_HEADER_KEY]
        self.mfa_header = header_info_map[MFA_HEADER_KEY]
        self.restore_header = header_info_map[RESTORE_HEADER_KEY]

    def configure_errors(self):
        error_map = self.ErrorMap[self.name]
        self.storage_copy_error = error_map[STORAGE_COPY_ERROR]
        self.storage_create_error = error_map[STORAGE_CREATE_ERROR]
        self.storage_data_error = error_map[STORAGE_DATA_ERROR]
        self.storage_permissions_error = error_map[STORAGE_PERMISSIONS_ERROR]
        self.storage_response_error = error_map[STORAGE_RESPONSE_ERROR]

    def get_provider_name(self):
        return self.HostKeyMap[self.name]

    def supports_chunked_transfer(self):
        return self.ChunkedTransferSupport[self.name]


def get_default():
    return Provider('aws')