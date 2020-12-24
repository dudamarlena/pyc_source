# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/siteconfig.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging, os, re
from django.conf import settings, global_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.translation import ugettext as _
from djblets.log import restart_logging, siteconfig as log_siteconfig
from djblets.recaptcha import siteconfig as recaptcha_siteconfig
from djblets.siteconfig.django_settings import apply_django_settings, get_django_defaults, get_django_settings_map
from djblets.siteconfig.models import SiteConfiguration
from djblets.webapi.auth.backends import reset_auth_backends
from haystack import connections
from reviewboard.accounts.backends import auth_backends
from reviewboard.accounts.privacy import recompute_privacy_consents
from reviewboard.avatars import avatar_services
from reviewboard.oauth.features import oauth2_service_feature
from reviewboard.notifications.email.message import EmailMessage
from reviewboard.search import search_backend_registry
from reviewboard.search.search_backends.whoosh import WhooshBackend
from reviewboard.signals import site_settings_loaded
storage_backend_map = {b'builtin': b'django.core.files.storage.FileSystemStorage', 
   b's3': b'storages.backends.s3boto.S3BotoStorage', 
   b'swift': b'swift.storage.SwiftStorage'}
settings_map = {b'auth_digest_file_location': b'DIGEST_FILE_LOCATION', 
   b'auth_digest_realm': b'DIGEST_REALM', 
   b'auth_ldap_anon_bind_uid': b'LDAP_ANON_BIND_UID', 
   b'auth_ldap_anon_bind_passwd': b'LDAP_ANON_BIND_PASSWD', 
   b'auth_ldap_given_name_attribute': b'LDAP_GIVEN_NAME_ATTRIBUTE', 
   b'auth_ldap_surname_attribute': b'LDAP_SURNAME_ATTRIBUTE', 
   b'auth_ldap_full_name_attribute': b'LDAP_FULL_NAME_ATTRIBUTE', 
   b'auth_ldap_email_domain': b'LDAP_EMAIL_DOMAIN', 
   b'auth_ldap_email_attribute': b'LDAP_EMAIL_ATTRIBUTE', 
   b'auth_ldap_tls': b'LDAP_TLS', 
   b'auth_ldap_base_dn': b'LDAP_BASE_DN', 
   b'auth_ldap_uid': b'LDAP_UID', 
   b'auth_ldap_uid_mask': b'LDAP_UID_MASK', 
   b'auth_ldap_uri': b'LDAP_URI', 
   b'auth_ad_domain_name': b'AD_DOMAIN_NAME', 
   b'auth_ad_use_tls': b'AD_USE_TLS', 
   b'auth_ad_find_dc_from_dns': b'AD_FIND_DC_FROM_DNS', 
   b'auth_ad_domain_controller': b'AD_DOMAIN_CONTROLLER', 
   b'auth_ad_ou_name': b'AD_OU_NAME', 
   b'auth_ad_group_name': b'AD_GROUP_NAME', 
   b'auth_ad_search_root': b'AD_SEARCH_ROOT', 
   b'auth_ad_recursion_depth': b'AD_RECURSION_DEPTH', 
   b'auth_x509_username_field': b'X509_USERNAME_FIELD', 
   b'auth_x509_custom_username_field': b'X509_CUSTOM_USERNAME_FIELD', 
   b'auth_x509_username_regex': b'X509_USERNAME_REGEX', 
   b'auth_x509_autocreate_users': b'X509_AUTOCREATE_USERS', 
   b'auth_nis_email_domain': b'NIS_EMAIL_DOMAIN', 
   b'site_domain_method': b'DOMAIN_METHOD'}
settings_map.update(get_django_settings_map())
settings_map.update(log_siteconfig.settings_map)
settings_map.update(recaptcha_siteconfig.settings_map)
settings_map.update({b'aws_access_key_id': b'AWS_ACCESS_KEY_ID', 
   b'aws_secret_access_key': b'AWS_SECRET_ACCESS_KEY', 
   b'aws_headers': b'AWS_HEADERS', 
   b'aws_calling_format': b'AWS_CALLING_FORMAT', 
   b'aws_default_acl': b'AWS_DEFAULT_ACL', 
   b'aws_querystring_auth': b'AWS_QUERYSTRING_AUTH', 
   b'aws_querystring_active': b'AWS_QUERYSTRING_ACTIVE', 
   b'aws_querystring_expire': b'AWS_QUERYSTRING_EXPIRE', 
   b'aws_s3_secure_urls': b'AWS_S3_SECURE_URLS', 
   b'aws_s3_bucket_name': b'AWS_STORAGE_BUCKET_NAME', 
   b'swift_auth_url': b'SWIFT_AUTH_URL', 
   b'swift_username': b'SWIFT_USERNAME', 
   b'swift_key': b'SWIFT_KEY', 
   b'swift_auth_version': b'SWIFT_AUTH_VERSION', 
   b'swift_container_name': b'SWIFT_CONTAINER_NAME', 
   b'couchdb_default_server': b'COUCHDB_DEFAULT_SERVER', 
   b'couchdb_storage_options': b'COUCHDB_STORAGE_OPTIONS'})
defaults = get_django_defaults()
defaults.update(log_siteconfig.defaults)
defaults.update(recaptcha_siteconfig.defaults)
defaults.update(avatar_services.get_siteconfig_defaults())
defaults.update({b'auth_ldap_anon_bind_uid': b'', 
   b'auth_ldap_anon_bind_passwd': b'', 
   b'auth_ldap_email_domain': b'', 
   b'auth_ldap_tls': False, 
   b'auth_ldap_uid': b'uid', 
   b'auth_ldap_uid_mask': b'', 
   b'auth_ldap_uri': b'', 
   b'auth_nis_email_domain': b'', 
   b'auth_registration_show_captcha': False, 
   b'auth_require_sitewide_login': False, 
   b'auth_custom_backends': [], b'auth_enable_registration': True, 
   b'auth_x509_username_field': b'SSL_CLIENT_S_DN_CN', 
   b'auth_x509_username_regex': b'', 
   b'auth_x509_autocreate_users': False, 
   b'company': b'', 
   b'default_use_rich_text': True, 
   b'diffviewer_context_num_lines': 5, 
   b'diffviewer_include_space_patterns': [], b'diffviewer_max_diff_size': 0, 
   b'diffviewer_paginate_by': 20, 
   b'diffviewer_paginate_orphans': 10, 
   b'diffviewer_syntax_highlighting': True, 
   b'diffviewer_syntax_highlighting_threshold': 0, 
   b'diffviewer_show_trailing_whitespace': True, 
   b'mail_send_review_mail': False, 
   b'mail_send_new_user_mail': False, 
   b'mail_send_password_changed_mail': False, 
   b'mail_enable_autogenerated_header': True, 
   b'mail_from_spoofing': EmailMessage.FROM_SPOOFING_SMART, 
   b'search_enable': False, 
   b'send_support_usage_stats': True, 
   b'site_domain_method': b'http', 
   b'privacy_enable_user_consent': False, 
   b'privacy_info_html': None, 
   b'privacy_policy_url': None, 
   b'terms_of_service_url': None, 
   b'search_results_per_page': 20, 
   b'search_backend_id': WhooshBackend.search_backend_id, 
   b'search_backend_settings': {}, b'search_on_the_fly_indexing': False, 
   b'site_media_url': settings.SITE_ROOT + b'media/'})
defaults.update({b'aws_access_key_id': b'', 
   b'aws_calling_format': 2, 
   b'aws_default_acl': b'public-read', 
   b'aws_headers': {}, b'aws_querystring_active': False, 
   b'aws_querystring_auth': False, 
   b'aws_querystring_expire': 60, 
   b'aws_s3_bucket_name': b'', 
   b'aws_s3_secure_urls': False, 
   b'aws_secret_access_key': b'', 
   b'couchdb_default_server': b'', 
   b'couchdb_storage_options': {}, b'swift_auth_url': b'', 
   b'swift_auth_version': b'1', 
   b'swift_container_name': b'', 
   b'swift_key': b'', 
   b'swift_username': b''})
_original_webapi_auth_backends = settings.WEB_API_AUTH_BACKENDS

def load_site_config(full_reload=False):
    """Load stored site configuration settings.

    This populates the Django settings object with any keys that need to be
    there.
    """
    global _original_webapi_auth_backends

    def apply_setting(settings_key, db_key, default=None):
        """Apply the given siteconfig value to the Django settings object."""
        db_value = siteconfig.settings.get(db_key)
        if db_value:
            setattr(settings, settings_key, db_value)
        elif default:
            setattr(settings, settings_key, default)

    def update_haystack_settings():
        """Update the haystack settings in site config."""
        search_backend_id = siteconfig.get(b'search_backend_id') or defaults[b'search_backend_id']
        search_backend = search_backend_registry.get_search_backend(search_backend_id)
        if not search_backend:
            raise ImproperlyConfigured(_(b'The search engine "%s" could not be found. If this is provided by an extension, you will have to make sure that extension is enabled.' % search_backend_id))
        apply_setting(b'HAYSTACK_CONNECTIONS', None, {b'default': search_backend.configuration})
        connections.connections_info = settings.HAYSTACK_CONNECTIONS
        connections._connections = {}
        return

    dirty = False
    try:
        siteconfig = SiteConfiguration.objects.get_current()
    except SiteConfiguration.DoesNotExist:
        raise ImproperlyConfigured(b'The site configuration entry does not exist in the database. Re-run `./manage.py` syncdb to fix this.')
    except Exception as e:
        logging.error(b'Could not load siteconfig: %s' % e)
        return

    if not siteconfig.get_defaults():
        siteconfig.add_defaults(defaults)
    mail_default_from = siteconfig.settings.get(b'mail_default_from', global_settings.DEFAULT_FROM_EMAIL)
    if not mail_default_from or mail_default_from == global_settings.DEFAULT_FROM_EMAIL:
        domain = siteconfig.site.domain.split(b':')[0]
        siteconfig.set(b'mail_default_from', b'noreply@' + domain)
    site_static_root = siteconfig.settings.get(b'site_static_root', b'')
    site_media_root = siteconfig.settings.get(b'site_media_root')
    if site_static_root == b'' or site_static_root == site_media_root:
        siteconfig.set(b'site_static_root', settings.STATIC_ROOT)
    site_static_url = siteconfig.settings.get(b'site_static_url', b'')
    site_media_url = siteconfig.settings.get(b'site_media_url')
    if site_static_url == b'' or site_static_url == site_media_url:
        siteconfig.set(b'site_static_url', settings.STATIC_URL)
    apply_django_settings(siteconfig, settings_map)
    if full_reload and not getattr(settings, b'RUNNING_TEST', False):
        restart_logging()
    update_haystack_settings()
    apply_setting(b'ADMINS', None, (
     (
      siteconfig.get(b'site_admin_name', b''),
      siteconfig.get(b'site_admin_email', b'')),))
    apply_setting(b'MANAGERS', None, settings.ADMINS)
    apply_setting(b'ADMIN_MEDIA_PREFIX', None, settings.STATIC_URL + b'admin/')
    auth_backend_id = siteconfig.settings.get(b'auth_backend', b'builtin')
    builtin_backend_obj = auth_backends.get(b'backend_id', b'builtin')
    builtin_backend = b'%s.%s' % (builtin_backend_obj.__module__,
     builtin_backend_obj.__name__)
    if auth_backend_id == b'custom':
        custom_backends = siteconfig.settings.get(b'auth_custom_backends')
        if isinstance(custom_backends, six.string_types):
            custom_backends = (
             custom_backends,)
        elif isinstance(custom_backends, list):
            custom_backends = tuple(custom_backends)
        settings.AUTHENTICATION_BACKENDS = custom_backends
        if builtin_backend not in custom_backends:
            settings.AUTHENTICATION_BACKENDS += (builtin_backend,)
    else:
        backend = auth_backends.get(b'backend_id', auth_backend_id)
        if backend and backend is not builtin_backend_obj:
            settings.AUTHENTICATION_BACKENDS = (b'%s.%s' % (backend.__module__, backend.__name__),
             builtin_backend)
        else:
            settings.AUTHENTICATION_BACKENDS = (
             builtin_backend,)
        if auth_backend_id == b'ldap':
            if not hasattr(settings, b'LDAP_UID'):
                if hasattr(settings, b'LDAP_UID_MASK'):
                    m = re.search(b'([a-zA-Z][a-zA-Z0-9-]+)=%s', settings.LDAP_UID_MASK)
                    if m:
                        settings.LDAP_UID = m.group(1)
                    else:
                        settings.LDAP_UID = b'uid'
                else:
                    settings.LDAP_UID = b'uid'
                settings.LDAP_UID_MASK = None
                siteconfig.set(b'auth_ldap_uid', settings.LDAP_UID)
                siteconfig.set(b'auth_ldap_uid_mask', settings.LDAP_UID_MASK)
                dirty = True
        settings.AUTHENTICATION_BACKENDS += ('reviewboard.webapi.auth_backends.TokenAuthBackend', )
        settings.WEB_API_AUTH_BACKENDS = _original_webapi_auth_backends
        reset_auth_backends()
        if oauth2_service_feature.is_enabled():
            settings.AUTHENTICATION_BACKENDS += ('reviewboard.webapi.auth_backends.OAuth2TokenAuthBackend', )
            settings.WEB_API_AUTH_BACKENDS += ('djblets.webapi.auth.backends.oauth2_tokens.WebAPIOAuth2TokenAuthBackend', )
        storage_backend = siteconfig.settings.get(b'storage_backend', b'builtin')
        if storage_backend in storage_backend_map:
            settings.DEFAULT_FILE_STORAGE = storage_backend_map[storage_backend]
        else:
            settings.DEFAULT_FILE_STORAGE = storage_backend_map[b'builtin']
        settings.AWS_QUERYSTRING_AUTH = siteconfig.get(b'aws_querystring_auth')
        settings.AWS_ACCESS_KEY_ID = six.text_type(siteconfig.get(b'aws_access_key_id'))
        settings.AWS_SECRET_ACCESS_KEY = six.text_type(siteconfig.get(b'aws_secret_access_key'))
        settings.AWS_STORAGE_BUCKET_NAME = six.text_type(siteconfig.get(b'aws_s3_bucket_name'))
        try:
            settings.AWS_CALLING_FORMAT = int(siteconfig.get(b'aws_calling_format'))
        except ValueError:
            settings.AWS_CALLING_FORMAT = 0

        settings.SWIFT_AUTH_URL = six.text_type(siteconfig.get(b'swift_auth_url'))
        settings.SWIFT_USERNAME = six.text_type(siteconfig.get(b'swift_username'))
        settings.SWIFT_KEY = six.text_type(siteconfig.get(b'swift_key'))
        try:
            settings.SWIFT_AUTH_VERSION = int(siteconfig.get(b'swift_auth_version'))
        except:
            settings.SWIFT_AUTH_VERSION = 1

    settings.SWIFT_CONTAINER_NAME = six.text_type(siteconfig.get(b'swift_container_name'))
    if siteconfig.settings.get(b'site_domain_method', b'http') == b'https':
        os.environ[b'HTTPS'] = b'on'
    else:
        os.environ[b'HTTPS'] = b'off'
    if avatar_services.migrate_settings(siteconfig):
        dirty = True
    if dirty:
        siteconfig.save()
    recompute_privacy_consents()
    site_settings_loaded.send(sender=None)
    return siteconfig