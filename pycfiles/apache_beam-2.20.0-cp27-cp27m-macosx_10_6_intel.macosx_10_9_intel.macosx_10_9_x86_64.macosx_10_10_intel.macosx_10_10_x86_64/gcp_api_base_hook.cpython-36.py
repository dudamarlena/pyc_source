# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/gcp_api_base_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10897 bytes
import json, functools, httplib2, google.auth, google_auth_httplib2, google.oauth2.service_account, os, tempfile
from google.api_core.exceptions import GoogleAPICallError, AlreadyExists, RetryError
from googleapiclient.errors import HttpError
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
_DEFAULT_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )
_G_APP_CRED_ENV_VAR = 'GOOGLE_APPLICATION_CREDENTIALS'

class GoogleCloudBaseHook(BaseHook):
    """GoogleCloudBaseHook"""

    def __init__(self, gcp_conn_id='google_cloud_default', delegate_to=None):
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.extras = self.get_connection(self.gcp_conn_id).extra_dejson

    def _get_credentials(self):
        """
        Returns the Credentials object for Google API
        """
        key_path = self._get_field('key_path', False)
        keyfile_dict = self._get_field('keyfile_dict', False)
        scope = self._get_field('scope', None)
        if scope:
            scopes = [s.strip() for s in scope.split(',')]
        else:
            scopes = _DEFAULT_SCOPES
        if not key_path:
            if not keyfile_dict:
                self.log.info('Getting connection using `google.auth.default()` since no key file is defined for hook.')
                credentials, _ = google.auth.default(scopes=scopes)
        if key_path:
            if key_path.endswith('.json'):
                self.log.debug('Getting connection using JSON key file %s' % key_path)
                credentials = google.oauth2.service_account.Credentials.from_service_account_file(key_path,
                  scopes=scopes)
            else:
                if key_path.endswith('.p12'):
                    raise AirflowException('Legacy P12 key file are not supported, use a JSON key file.')
                else:
                    raise AirflowException('Unrecognised extension for key file.')
        else:
            try:
                keyfile_dict = json.loads(keyfile_dict)
                keyfile_dict['private_key'] = keyfile_dict['private_key'].replace('\\n', '\n')
                credentials = google.oauth2.service_account.Credentials.from_service_account_info(keyfile_dict,
                  scopes=scopes)
            except json.decoder.JSONDecodeError:
                raise AirflowException('Invalid key JSON.')

            if self.delegate_to:
                return credentials.with_subject(self.delegate_to)
            else:
                return credentials

    def _get_access_token(self):
        """
        Returns a valid access token from Google API Credentials
        """
        return self._get_credentials().token

    def _authorize(self):
        """
        Returns an authorized HTTP object to be used to build a Google cloud
        service hook connection.
        """
        credentials = self._get_credentials()
        http = httplib2.Http()
        authed_http = google_auth_httplib2.AuthorizedHttp(credentials,
          http=http)
        return authed_http

    def _get_field(self, f, default=None):
        """
        Fetches a field from extras, and returns it. This is some Airflow
        magic. The google_cloud_platform hook type adds custom UI elements
        to the hook page, which allow admins to specify service_account,
        key_path, etc. They get formatted as shown below.
        """
        long_f = 'extra__google_cloud_platform__{}'.format(f)
        if hasattr(self, 'extras'):
            if long_f in self.extras:
                return self.extras[long_f]
        return default

    @property
    def project_id(self):
        return self._get_field('project')

    @property
    def num_retries(self):
        """
        Returns num_retries from Connection.

        :return: the number of times each API request should be retried
        :rtype: int
        """
        return self._get_field('num_retries') or 5

    @staticmethod
    def catch_http_exception(func):
        """
        Function decorator that intercepts HTTP Errors and raises AirflowException
        with more informative message.
        """

        @functools.wraps(func)
        def wrapper_decorator(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except GoogleAPICallError as e:
                if isinstance(e, AlreadyExists):
                    raise e
                else:
                    self.log.error('The request failed:\n%s', str(e))
                    raise AirflowException(e)
            except RetryError as e:
                self.log.error('The request failed due to a retryable error and retry attempts failed.')
                raise AirflowException(e)
            except ValueError as e:
                self.log.error('The request failed, the parameters are invalid.')
                raise AirflowException(e)
            except HttpError as e:
                self.log.error('The request failed:\n%s', str(e))
                raise AirflowException(e)

        return wrapper_decorator

    @staticmethod
    def fallback_to_default_project_id(func):
        """
        Decorator that provides fallback for Google Cloud Platform project id. If
        the project is None it will be replaced with the project_id from the
        service account the Hook is authenticated with. Project id can be specified
        either via project_id kwarg or via first parameter in positional args.

        :param func: function to wrap
        :return: result of the function call
        """

        @functools.wraps(func)
        def inner_wrapper(self, *args, **kwargs):
            if len(args) > 0:
                raise AirflowException('You must use keyword arguments in this methods rather than positional')
            else:
                if 'project_id' in kwargs:
                    kwargs['project_id'] = self._get_project_id(kwargs['project_id'])
                else:
                    kwargs['project_id'] = self._get_project_id(None)
            if not kwargs['project_id']:
                raise AirflowException('The project id must be passed either as keyword project_id parameter or as project_id extra in GCP connection definition. Both are not set!')
            return func(self, *args, **kwargs)

        return inner_wrapper

    def _get_project_id(self, project_id):
        """
        In case project_id is None, overrides it with default project_id from
        the service account that is authorized.

        :param project_id: project id to
        :type project_id: str
        :return: the project_id specified or default project id if project_id is None
        """
        if project_id:
            return project_id
        else:
            return self.project_id

    class _Decorators(object):
        """GoogleCloudBaseHook._Decorators"""

        @staticmethod
        def provide_gcp_credential_file(func):
            """
            Function decorator that provides a GOOGLE_APPLICATION_CREDENTIALS
            environment variable, pointing to file path of a JSON file of service
            account key.
            """

            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                with tempfile.NamedTemporaryFile(mode='w+t') as (conf_file):
                    key_path = self._get_field('key_path', False)
                    keyfile_dict = self._get_field('keyfile_dict', False)
                    if key_path:
                        if key_path.endswith('.p12'):
                            raise AirflowException('Legacy P12 key file are not supported, use a JSON key file.')
                        os.environ[_G_APP_CRED_ENV_VAR] = key_path
                    else:
                        if keyfile_dict:
                            conf_file.write(keyfile_dict)
                            conf_file.flush()
                            os.environ[_G_APP_CRED_ENV_VAR] = conf_file.name
                    return func(self, *args, **kwargs)

            return wrapper