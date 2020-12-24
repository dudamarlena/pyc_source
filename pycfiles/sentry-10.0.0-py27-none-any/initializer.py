# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/initializer.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import click, os, six
from django.conf import settings
from sentry.utils import warnings
from sentry.utils.sdk import configure_sdk
from sentry.utils.warnings import DeprecatedSettingWarning

def register_plugins(settings):
    from pkg_resources import iter_entry_points
    from sentry.plugins import plugins
    for ep in iter_entry_points('sentry.plugins'):
        try:
            plugin = ep.load()
        except Exception:
            import traceback
            click.echo('Failed to load plugin %r:\n%s' % (ep.name, traceback.format_exc()), err=True)
        else:
            plugins.register(plugin)

    for plugin in plugins.all(version=None):
        init_plugin(plugin)

    from sentry import integrations
    from sentry.utils.imports import import_string
    for integration_path in settings.SENTRY_DEFAULT_INTEGRATIONS:
        try:
            integration_cls = import_string(integration_path)
        except Exception:
            import traceback
            click.echo('Failed to load integration %r:\n%s' % (integration_path, traceback.format_exc()), err=True)
        else:
            integrations.register(integration_cls)

    for integration in integrations.all():
        try:
            integration.setup()
        except AttributeError:
            pass

    return


def init_plugin(plugin):
    from sentry.plugins import bindings
    plugin.setup(bindings)
    if hasattr(plugin, 'get_custom_contexts'):
        from sentry.interfaces.contexts import contexttype
        for cls in plugin.get_custom_contexts() or ():
            contexttype(cls)

    if hasattr(plugin, 'get_cron_schedule') and plugin.is_enabled():
        schedules = plugin.get_cron_schedule()
        if schedules:
            settings.CELERYBEAT_SCHEDULE.update(schedules)
    if hasattr(plugin, 'get_worker_imports') and plugin.is_enabled():
        imports = plugin.get_worker_imports()
        if imports:
            settings.CELERY_IMPORTS += tuple(imports)
    if hasattr(plugin, 'get_worker_queues') and plugin.is_enabled():
        from kombu import Queue
        for queue in plugin.get_worker_queues():
            try:
                name, routing_key = queue
            except ValueError:
                name = routing_key = queue

            q = Queue(name, routing_key=routing_key)
            q.durable = False
            settings.CELERY_QUEUES.append(q)


def initialize_receivers():
    import sentry.receivers


def get_asset_version(settings):
    path = os.path.join(settings.STATIC_ROOT, 'version')
    try:
        with open(path) as (fp):
            return fp.read().strip()
    except IOError:
        from time import time
        return int(time())


options_mapper = {'system.secret-key': 'SECRET_KEY', 
   'mail.backend': 'EMAIL_BACKEND', 
   'mail.host': 'EMAIL_HOST', 
   'mail.port': 'EMAIL_PORT', 
   'mail.username': 'EMAIL_HOST_USER', 
   'mail.password': 'EMAIL_HOST_PASSWORD', 
   'mail.use-tls': 'EMAIL_USE_TLS', 
   'mail.from': 'SERVER_EMAIL', 
   'mail.subject-prefix': 'EMAIL_SUBJECT_PREFIX'}

def bootstrap_options(settings, config=None):
    """
    Quickly bootstrap options that come in from a config file
    and convert options into Django settings that are
    required to even initialize the rest of the app.
    """
    from sentry.options import load_defaults
    load_defaults()
    options = {}
    if config is not None:
        from sentry.utils.yaml import safe_load
        from yaml.parser import ParserError
        from yaml.scanner import ScannerError
        try:
            with open(config, 'rb') as (fp):
                options = safe_load(fp)
        except IOError:
            pass
        except (AttributeError, ParserError, ScannerError) as e:
            from .importer import ConfigurationError
            raise ConfigurationError('Malformed config.yml file: %s' % six.text_type(e))

        if options is None:
            options = {}
        elif not isinstance(options, dict):
            from .importer import ConfigurationError
            raise ConfigurationError('Malformed config.yml file')
    from sentry.conf.server import DEAD
    for k, v in six.iteritems(options_mapper):
        if getattr(settings, v, DEAD) is not DEAD and k not in options:
            warnings.warn(DeprecatedSettingWarning(options_mapper[k], "SENTRY_OPTIONS['%s']" % k))
            options[k] = getattr(settings, v)

    for k, v in six.iteritems(options):
        settings.SENTRY_OPTIONS[k] = v

    for o in (settings.SENTRY_DEFAULT_OPTIONS, settings.SENTRY_OPTIONS):
        for k, v in six.iteritems(o):
            if k in options_mapper:
                if k == 'mail.backend':
                    try:
                        v = settings.SENTRY_EMAIL_BACKEND_ALIASES[v]
                    except KeyError:
                        pass

                setattr(settings, options_mapper[k], v)

    return


def configure_structlog():
    """
    Make structlog comply with all of our options.
    """
    from django.conf import settings
    import logging, structlog
    from sentry import options
    from sentry.logging import LoggingFormat
    WrappedDictClass = structlog.threadlocal.wrap_dict(dict)
    kwargs = {'context_class': WrappedDictClass, 
       'wrapper_class': structlog.stdlib.BoundLogger, 
       'cache_logger_on_first_use': True, 
       'processors': [
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.format_exc_info,
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.UnicodeDecoder()]}
    fmt_from_env = os.environ.get('SENTRY_LOG_FORMAT')
    if fmt_from_env:
        settings.SENTRY_OPTIONS['system.logging-format'] = fmt_from_env.lower()
    fmt = options.get('system.logging-format')
    if fmt == LoggingFormat.HUMAN:
        from sentry.logging.handlers import HumanRenderer
        kwargs['processors'].extend([
         structlog.processors.ExceptionPrettyPrinter(), HumanRenderer()])
    elif fmt == LoggingFormat.MACHINE:
        from sentry.logging.handlers import JSONRenderer
        kwargs['processors'].append(JSONRenderer())
    structlog.configure(**kwargs)
    lvl = os.environ.get('SENTRY_LOG_LEVEL')
    if lvl and lvl not in logging._levelNames:
        raise AttributeError('%s is not a valid logging level.' % lvl)
    settings.LOGGING['root'].update({'level': lvl or settings.LOGGING['default_level']})
    if lvl:
        for logger in settings.LOGGING['overridable']:
            try:
                settings.LOGGING['loggers'][logger].update({'level': lvl})
            except KeyError:
                raise KeyError('%s is not a defined logger.' % logger)

    logging.config.dictConfig(settings.LOGGING)


def initialize_app(config, skip_service_validation=False):
    settings = config['settings']
    bootstrap_options(settings, config['options'])
    configure_structlog()
    if 'south' in settings.INSTALLED_APPS:
        fix_south(settings)
    apply_legacy_settings(settings)
    if settings.CELERY_ALWAYS_EAGER and not settings.DEBUG:
        warnings.warn('Sentry is configured to run asynchronous tasks in-process. This is not recommended within production environments. See https://docs.sentry.io/on-premise/server/queue/ for more information.')
    if settings.SENTRY_SINGLE_ORGANIZATION:
        settings.SENTRY_FEATURES['organizations:create'] = False
    if not hasattr(settings, 'SUDO_COOKIE_SECURE'):
        settings.SUDO_COOKIE_SECURE = getattr(settings, 'SESSION_COOKIE_SECURE', False)
    if not hasattr(settings, 'SUDO_COOKIE_DOMAIN'):
        settings.SUDO_COOKIE_DOMAIN = getattr(settings, 'SESSION_COOKIE_DOMAIN', None)
    if not hasattr(settings, 'SUDO_COOKIE_PATH'):
        settings.SUDO_COOKIE_PATH = getattr(settings, 'SESSION_COOKIE_PATH', '/')
    if not hasattr(settings, 'CSRF_COOKIE_SECURE'):
        settings.CSRF_COOKIE_SECURE = getattr(settings, 'SESSION_COOKIE_SECURE', False)
    if not hasattr(settings, 'CSRF_COOKIE_DOMAIN'):
        settings.CSRF_COOKIE_DOMAIN = getattr(settings, 'SESSION_COOKIE_DOMAIN', None)
    if not hasattr(settings, 'CSRF_COOKIE_PATH'):
        settings.CSRF_COOKIE_PATH = getattr(settings, 'SESSION_COOKIE_PATH', '/')
    settings.CACHES['default']['VERSION'] = settings.CACHE_VERSION
    settings.ASSET_VERSION = get_asset_version(settings)
    settings.STATIC_URL = settings.STATIC_URL.format(version=settings.ASSET_VERSION)
    if getattr(settings, 'SENTRY_DEBUGGER', None) is None:
        settings.SENTRY_DEBUGGER = settings.DEBUG
    import django
    if hasattr(django, 'setup'):
        django.setup()
    bind_cache_to_option_store()
    register_plugins(settings)
    initialize_receivers()
    validate_options(settings)
    validate_snuba()
    configure_sdk()
    setup_services(validate=not skip_service_validation)
    from django.utils import timezone
    from sentry.app import env
    from sentry.runner.settings import get_sentry_conf
    env.data['config'] = get_sentry_conf()
    env.data['start_date'] = timezone.now()
    return


def setup_services(validate=True):
    from sentry import analytics, buffer, digests, newsletter, nodestore, quotas, ratelimits, search, tagstore, tsdb
    from .importer import ConfigurationError
    from sentry.utils.settings import reraise_as
    service_list = (
     analytics,
     buffer,
     digests,
     newsletter,
     nodestore,
     quotas,
     ratelimits,
     search,
     tagstore,
     tsdb)
    for service in service_list:
        if validate:
            try:
                service.validate()
            except AttributeError as exc:
                reraise_as(ConfigurationError(('{} service failed to call validate()\n{}').format(service.__name__, six.text_type(exc))))

        try:
            service.setup()
        except AttributeError as exc:
            if not hasattr(service, 'setup') or not callable(service.setup):
                reraise_as(ConfigurationError(('{} service failed to call setup()\n{}').format(service.__name__, six.text_type(exc))))
            raise


def validate_options(settings):
    from sentry.options import default_manager
    default_manager.validate(settings.SENTRY_OPTIONS, warn=True)


def fix_south(settings):
    settings.SOUTH_DATABASE_ADAPTERS = {}
    for key, value in six.iteritems(settings.DATABASES):
        if value['ENGINE'] != 'sentry.db.postgres':
            continue
        settings.SOUTH_DATABASE_ADAPTERS[key] = 'south.db.postgresql_psycopg2'


def bind_cache_to_option_store():
    from django.core.cache import cache as default_cache
    from sentry.options import default_store
    default_store.cache = default_cache


def show_big_error(message):
    if isinstance(message, six.string_types):
        lines = message.strip().splitlines()
    else:
        lines = message
    maxline = max(map(len, lines))
    click.echo('', err=True)
    click.secho('!!!%s!!!' % ('!' * min(maxline, 80),), err=True, fg='red')
    click.secho('!! %s !!' % ('').center(maxline), err=True, fg='red')
    for line in lines:
        click.secho('!! %s !!' % line.center(maxline), err=True, fg='red')

    click.secho('!! %s !!' % ('').center(maxline), err=True, fg='red')
    click.secho('!!!%s!!!' % ('!' * min(maxline, 80),), err=True, fg='red')
    click.echo('', err=True)


def apply_legacy_settings(settings):
    from sentry import options
    if hasattr(settings, 'SENTRY_USE_QUEUE'):
        warnings.warn(DeprecatedSettingWarning('SENTRY_USE_QUEUE', 'CELERY_ALWAYS_EAGER', 'https://docs.sentry.io/on-premise/server/queue/'))
        settings.CELERY_ALWAYS_EAGER = not settings.SENTRY_USE_QUEUE
    for old, new in (
     ('SENTRY_ADMIN_EMAIL', 'system.admin-email'),
     ('SENTRY_URL_PREFIX', 'system.url-prefix'),
     ('SENTRY_SYSTEM_MAX_EVENTS_PER_MINUTE', 'system.rate-limit'),
     ('SENTRY_ENABLE_EMAIL_REPLIES', 'mail.enable-replies'),
     ('SENTRY_SMTP_HOSTNAME', 'mail.reply-hostname'),
     ('MAILGUN_API_KEY', 'mail.mailgun-api-key'),
     ('SENTRY_FILESTORE', 'filestore.backend'),
     ('SENTRY_FILESTORE_OPTIONS', 'filestore.options'),
     ('GOOGLE_CLIENT_ID', 'auth-google.client-id'),
     ('GOOGLE_CLIENT_SECRET', 'auth-google.client-secret')):
        if new not in settings.SENTRY_OPTIONS and hasattr(settings, old):
            warnings.warn(DeprecatedSettingWarning(old, "SENTRY_OPTIONS['%s']" % new))
            settings.SENTRY_OPTIONS[new] = getattr(settings, old)

    if hasattr(settings, 'SENTRY_REDIS_OPTIONS'):
        if 'redis.clusters' in settings.SENTRY_OPTIONS:
            raise Exception("Cannot specify both SENTRY_OPTIONS['redis.clusters'] option and SENTRY_REDIS_OPTIONS setting.")
        else:
            warnings.warn(DeprecatedSettingWarning('SENTRY_REDIS_OPTIONS', 'SENTRY_OPTIONS["redis.clusters"]', removed_in_version='8.5'))
            settings.SENTRY_OPTIONS['redis.clusters'] = {'default': settings.SENTRY_REDIS_OPTIONS}
    else:
        settings.SENTRY_REDIS_OPTIONS = options.get('redis.clusters')['default']
    if not hasattr(settings, 'SENTRY_URL_PREFIX'):
        url_prefix = options.get('system.url-prefix', silent=True)
        if not url_prefix:
            url_prefix = 'http://sentry.example.com'
        settings.SENTRY_URL_PREFIX = url_prefix
    if settings.TIME_ZONE != 'UTC':
        show_big_error('TIME_ZONE should be set to UTC')
    if not settings.ALLOWED_HOSTS:
        settings.ALLOWED_HOSTS = [
         '*']
    if hasattr(settings, 'SENTRY_ALLOW_REGISTRATION'):
        warnings.warn(DeprecatedSettingWarning('SENTRY_ALLOW_REGISTRATION', 'SENTRY_FEATURES["auth:register"]'))
        settings.SENTRY_FEATURES['auth:register'] = settings.SENTRY_ALLOW_REGISTRATION
    settings.DEFAULT_FROM_EMAIL = settings.SENTRY_OPTIONS.get('mail.from', settings.SENTRY_DEFAULT_OPTIONS.get('mail.from'))
    if not settings.SENTRY_OPTIONS.get('system.secret-key'):
        from .importer import ConfigurationError
        raise ConfigurationError("`system.secret-key` MUST be set. Use 'sentry config generate-secret-key' to get one.")


def skip_migration_if_applied(settings, app_name, table_name, name='0001_initial'):
    from south.migration import Migrations
    from sentry.utils.db import table_exists
    import types
    if app_name not in settings.INSTALLED_APPS:
        return
    migration = Migrations(app_name)[name]

    def skip_if_table_exists(original):

        def wrapped(self):
            if table_exists(table_name):
                return lambda x=None: None
            else:
                return original()

        wrapped.__name__ = original.__name__
        return wrapped

    migration.forwards = types.MethodType(skip_if_table_exists(migration.forwards), migration)


def on_configure(config):
    """
    Executes after settings are full installed and configured.

    At this point we can force import on various things such as models
    as all of settings should be correctly configured.
    """
    settings = config['settings']
    if 'south' in settings.INSTALLED_APPS:
        skip_migration_if_applied(settings, 'social_auth', 'social_auth_association')


def validate_snuba():
    """
    Make sure everything related to Snuba is in sync.

    This covers a few cases:

    * When you have features related to Snuba, you must also
      have Snuba fully configured correctly to continue.
    * If you have Snuba specific search/tagstore/tsdb backends,
      you must also have a Snuba compatible eventstream backend
      otherwise no data will be written into Snuba.
    * If you only have Snuba related eventstream, yell that you
      probably want the other backends otherwise things are weird.
    """
    if not settings.DEBUG:
        return
    has_any_snuba_required_backends = settings.SENTRY_SEARCH == 'sentry.search.snuba.SnubaSearchBackend' or settings.SENTRY_TAGSTORE == 'sentry.tagstore.snuba.SnubaCompatibilityTagStorage' or settings.SENTRY_TSDB in ('sentry.tsdb.redissnuba.RedisSnubaTSDB',
                                                                                                                                                                                                                         'sentry.utils.services.ServiceDelegator')
    has_all_snuba_required_backends = settings.SENTRY_SEARCH == 'sentry.search.snuba.SnubaSearchBackend' and settings.SENTRY_TAGSTORE == 'sentry.tagstore.snuba.SnubaCompatibilityTagStorage' and settings.SENTRY_TSDB in ('sentry.tsdb.redissnuba.RedisSnubaTSDB',
                                                                                                                                                                                                                           'sentry.utils.services.ServiceDelegator')
    eventstream_is_snuba = settings.SENTRY_EVENTSTREAM == 'sentry.eventstream.snuba.SnubaEventStream' or settings.SENTRY_EVENTSTREAM == 'sentry.eventstream.kafka.KafkaEventStream'
    if has_all_snuba_required_backends and eventstream_is_snuba:
        return
    from sentry.features import requires_snuba as snuba_features
    snuba_enabled_features = set()
    for feature in snuba_features:
        if settings.SENTRY_FEATURES.get(feature, False):
            snuba_enabled_features.add(feature)

    if snuba_enabled_features and not eventstream_is_snuba:
        from .importer import ConfigurationError
        show_big_error("\nYou have features enabled which require Snuba,\nbut you don't have any Snuba compatible configuration.\n\nFeatures you have enabled:\n%s\n\nSee: https://github.com/getsentry/snuba#sentry--snuba\n" % ('\n').join(snuba_enabled_features))
        raise ConfigurationError('Cannot continue without Snuba configured.')
    if has_any_snuba_required_backends and not eventstream_is_snuba:
        from .importer import ConfigurationError
        show_big_error('\nIt appears that you are requiring Snuba,\nbut your SENTRY_EVENTSTREAM is not compatible.\n\nCurrent settings:\n\nSENTRY_SEARCH = %r\nSENTRY_TAGSTORE = %r\nSENTRY_TSDB = %r\nSENTRY_EVENTSTREAM = %r\n\nSee: https://github.com/getsentry/snuba#sentry--snuba' % (
         settings.SENTRY_SEARCH,
         settings.SENTRY_TAGSTORE,
         settings.SENTRY_TSDB,
         settings.SENTRY_EVENTSTREAM))
        raise ConfigurationError('Cannot continue without Snuba configured correctly.')
    if eventstream_is_snuba and not has_all_snuba_required_backends:
        show_big_error('\nYou are using a Snuba compatible eventstream\nwithout configuring search/tagstore/tsdb also to use Snuba.\nThis is probably not what you want.\n\nCurrent settings:\n\nSENTRY_SEARCH = %r\nSENTRY_TAGSTORE = %r\nSENTRY_TSDB = %r\nSENTRY_EVENTSTREAM = %r\n\nSee: https://github.com/getsentry/snuba#sentry--snuba' % (
         settings.SENTRY_SEARCH,
         settings.SENTRY_TAGSTORE,
         settings.SENTRY_TSDB,
         settings.SENTRY_EVENTSTREAM))