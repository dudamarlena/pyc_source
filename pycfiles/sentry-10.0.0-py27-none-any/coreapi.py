# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/coreapi.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import abc, base64, logging, re, six, zlib
from django.core.exceptions import SuspiciousOperation
from django.utils.crypto import constant_time_compare
from gzip import GzipFile
from six import BytesIO
from time import time
from sentry.attachments import attachment_cache
from sentry.cache import default_cache
from sentry.models import ProjectKey
from sentry.tasks.store import preprocess_event, preprocess_event_from_reprocessing
from sentry.utils import json
from sentry.utils.auth import parse_auth_header
from sentry.utils.http import origin_from_request
from sentry.utils.strings import decompress
from sentry.utils.safe import get_path
from sentry.utils.sdk import configure_scope
from sentry.utils.canonical import CANONICAL_TYPES
_dist_re = re.compile('^[a-zA-Z0-9_.-]+$')
logger = logging.getLogger('sentry.api')

class APIError(Exception):
    http_status = 400
    msg = 'Invalid request'
    name = None

    def __init__(self, msg=None, name=None):
        if msg:
            self.msg = msg
        if self.name:
            self.name = name

    def __str__(self):
        return self.msg or ''


class APIUnauthorized(APIError):
    http_status = 401
    msg = 'Unauthorized'


class APIForbidden(APIError):
    http_status = 403


class APIRateLimited(APIError):
    http_status = 429
    msg = 'Creation of this event was denied due to rate limiting'
    name = 'rate_limit'

    def __init__(self, retry_after=None):
        self.retry_after = retry_after


class Auth(object):

    def __init__(self, client=None, version=None, secret_key=None, public_key=None, is_public=False):
        self.client = client
        self.version = version
        self.secret_key = secret_key
        self.public_key = public_key
        self.is_public = is_public


class ClientContext(object):

    def __init__(self, agent=None, version=None, project_id=None, ip_address=None):
        self.agent = agent
        self.version = version
        self.project_id = project_id
        self.project = None
        self.ip_address = ip_address
        return

    def bind_project(self, project):
        self.project = project
        self.project_id = project.id
        with configure_scope() as (scope):
            scope.set_tag('project', project.id)

    def bind_auth(self, auth):
        self.agent = auth.client
        self.version = auth.version
        with configure_scope() as (scope):
            scope.set_tag('agent', self.agent)
            scope.set_tag('protocol', self.version)


class ClientApiHelper(object):

    def __init__(self, agent=None, version=None, project_id=None, ip_address=None):
        self.context = ClientContext(agent=agent, version=version, project_id=project_id, ip_address=ip_address)

    def project_key_from_auth(self, auth):
        if not auth.public_key:
            raise APIUnauthorized('Invalid api key')
        if not ProjectKey.looks_like_api_key(auth.public_key):
            raise APIUnauthorized('Invalid api key')
        try:
            pk = ProjectKey.objects.get_from_cache(public_key=auth.public_key)
        except ProjectKey.DoesNotExist:
            raise APIUnauthorized('Invalid api key')

        if not constant_time_compare(pk.secret_key, auth.secret_key or pk.secret_key):
            raise APIUnauthorized('Invalid api key')
        if not pk.is_active:
            raise APIUnauthorized('API key is disabled')
        if not pk.roles.store:
            raise APIUnauthorized('Key does not allow event storage access')
        return pk

    def project_id_from_auth(self, auth):
        return self.project_key_from_auth(auth).project_id

    def ensure_does_not_have_ip(self, data):
        env = get_path(data, 'request', 'env')
        if env:
            env.pop('REMOTE_ADDR', None)
        user = get_path(data, 'user')
        if user:
            user.pop('ip_address', None)
        sdk = get_path(data, 'sdk')
        if sdk:
            sdk.pop('client_ip', None)
        return

    def insert_data_to_database(self, data, start_time=None, from_reprocessing=False, attachments=None):
        if start_time is None:
            start_time = time()
        if isinstance(data, CANONICAL_TYPES):
            data = dict(data.items())
        cache_timeout = 3600
        cache_key = cache_key_for_event(data)
        default_cache.set(cache_key, data, cache_timeout)
        if attachments is not None:
            attachment_cache.set(cache_key, attachments, cache_timeout)
        task = from_reprocessing and preprocess_event_from_reprocessing or preprocess_event
        task.delay(cache_key=cache_key, start_time=start_time, event_id=data['event_id'])
        return


@six.add_metaclass(abc.ABCMeta)
class AbstractAuthHelper(object):

    @abc.abstractmethod
    def auth_from_request(cls, request):
        pass

    @abc.abstractmethod
    def origin_from_request(cls, request):
        pass


class ClientAuthHelper(AbstractAuthHelper):

    @classmethod
    def auth_from_request(cls, request):
        result = {k:request.GET[k] for k in six.iterkeys(request.GET) if k[:7] == 'sentry_'}
        if request.META.get('HTTP_X_SENTRY_AUTH', '')[:7].lower() == 'sentry ':
            if result:
                raise SuspiciousOperation('Multiple authentication payloads were detected.')
            result = parse_auth_header(request.META['HTTP_X_SENTRY_AUTH'])
        elif request.META.get('HTTP_AUTHORIZATION', '')[:7].lower() == 'sentry ':
            if result:
                raise SuspiciousOperation('Multiple authentication payloads were detected.')
            result = parse_auth_header(request.META['HTTP_AUTHORIZATION'])
        if not result:
            raise APIUnauthorized('Unable to find authentication information')
        origin = cls.origin_from_request(request)
        auth = Auth(client=result.get('sentry_client'), version=six.text_type(result.get('sentry_version')), secret_key=result.get('sentry_secret'), public_key=result.get('sentry_key'), is_public=bool(origin))
        if not auth.client:
            auth.client = request.META.get('HTTP_USER_AGENT')
            if isinstance(auth.client, bytes):
                auth.client = auth.client.decode('latin1')
        return auth

    @classmethod
    def origin_from_request(cls, request):
        """
        Returns either the Origin or Referer value from the request headers.
        """
        if request.META.get('HTTP_ORIGIN') == 'null':
            return 'null'
        return origin_from_request(request)


class MinidumpAuthHelper(AbstractAuthHelper):

    @classmethod
    def origin_from_request(cls, request):
        return

    @classmethod
    def auth_from_request(cls, request):
        key = request.GET.get('sentry_key')
        if not key:
            raise APIUnauthorized('Unable to find authentication information')
        auth = Auth(public_key=key, client='sentry-minidump', is_public=False)
        return auth


class SecurityAuthHelper(AbstractAuthHelper):

    @classmethod
    def origin_from_request(cls, request):
        return

    @classmethod
    def auth_from_request(cls, request):
        key = request.GET.get('sentry_key')
        if not key:
            raise APIUnauthorized('Unable to find authentication information')
        auth = Auth(public_key=key, is_public=True)
        auth.client = request.META.get('HTTP_USER_AGENT')
        return auth


def cache_key_for_event(data):
    return ('e:{1}:{0}').format(data['project'], data['event_id'])


def decompress_deflate(encoded_data):
    try:
        return zlib.decompress(encoded_data).decode('utf-8')
    except Exception as e:
        logger.debug(six.text_type(e), exc_info=True)
        raise APIError('Bad data decoding request (%s, %s)' % (type(e).__name__, e))


def decompress_gzip(encoded_data):
    try:
        fp = BytesIO(encoded_data)
        try:
            f = GzipFile(fileobj=fp)
            return f.read().decode('utf-8')
        finally:
            f.close()

    except Exception as e:
        logger.debug(six.text_type(e), exc_info=True)
        raise APIError('Bad data decoding request (%s, %s)' % (type(e).__name__, e))


def decode_and_decompress_data(encoded_data):
    try:
        try:
            return decompress(encoded_data).decode('utf-8')
        except zlib.error:
            return base64.b64decode(encoded_data).decode('utf-8')

    except Exception as e:
        logger.debug(six.text_type(e), exc_info=True)
        raise APIError('Bad data decoding request (%s, %s)' % (type(e).__name__, e))


def decode_data(encoded_data):
    try:
        return encoded_data.decode('utf-8')
    except UnicodeDecodeError as e:
        logger.debug(six.text_type(e), exc_info=True)
        raise APIError('Bad data decoding request (%s, %s)' % (type(e).__name__, e))


def safely_load_json_string(json_string):
    try:
        if isinstance(json_string, six.binary_type):
            json_string = json_string.decode('utf-8')
        obj = json.loads(json_string)
        assert isinstance(obj, dict)
    except Exception as e:
        logger.debug(six.text_type(e), exc_info=True)
        raise APIError('Bad data reconstructing object (%s, %s)' % (type(e).__name__, e))

    return obj