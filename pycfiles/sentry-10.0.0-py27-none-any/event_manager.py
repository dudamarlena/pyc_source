# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/event_manager.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import time, jsonschema, logging, six
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from django.db import connection, IntegrityError, router, transaction
from django.db.models import Func
from django.utils import timezone
from django.utils.encoding import force_text
from sentry import buffer, eventtypes, eventstream, features, tagstore, tsdb
from sentry.constants import DEFAULT_STORE_NORMALIZER_ARGS, LOG_LEVELS, LOG_LEVELS_MAP, MAX_TAG_VALUE_LENGTH, MAX_SECS_IN_FUTURE, MAX_SECS_IN_PAST
from sentry.message_filters import should_filter_event
from sentry.grouping.api import get_grouping_config_dict_for_project, get_grouping_config_dict_for_event_data, load_grouping_config, apply_server_fingerprinting, get_fingerprinting_config_for_project, GroupingConfigNotFound
from sentry.coreapi import APIError, APIForbidden, decompress_gzip, decompress_deflate, decode_and_decompress_data, decode_data, safely_load_json_string
from sentry.interfaces.base import get_interface
from sentry.models import Activity, Environment, Event, EventDict, EventError, EventUser, Group, GroupEnvironment, GroupHash, GroupLink, GroupRelease, GroupResolution, GroupStatus, Project, Release, ReleaseEnvironment, ReleaseProject, ReleaseProjectEnvironment, UserReport, Organization
from sentry.plugins import plugins
from sentry.signals import event_discarded, event_saved, first_event_received
from sentry.tasks.integrations import kick_off_status_syncs
from sentry.utils import metrics
from sentry.utils.canonical import CanonicalKeyDict
from sentry.utils.data_filters import is_valid_ip, is_valid_release, is_valid_error_message, FilterStatKeys
from sentry.utils.dates import to_timestamp
from sentry.utils.db import is_postgres
from sentry.utils.safe import safe_execute, trim, get_path, setdefault_path
from sentry.stacktraces.processing import normalize_stacktraces_for_grouping
from sentry.culprit import generate_culprit
logger = logging.getLogger('sentry.events')
SECURITY_REPORT_INTERFACES = ('csp', 'hpkp', 'expectct', 'expectstaple')

def pop_tag(data, key):
    data['tags'] = [ kv for kv in data['tags'] if kv is None or kv[0] != key ]
    return


def set_tag(data, key, value):
    pop_tag(data, key)
    data['tags'].append((key, trim(value, MAX_TAG_VALUE_LENGTH)))


def get_tag(data, key):
    for k, v in get_path(data, 'tags', filter=True):
        if k == key:
            return v


def count_limit(count):
    for amount, sample_rate in settings.SENTRY_SAMPLE_RATES:
        if count <= amount:
            return sample_rate

    return settings.SENTRY_MAX_SAMPLE_RATE


def time_limit(silence):
    for amount, sample_rate in settings.SENTRY_SAMPLE_TIMES:
        if silence >= amount:
            return sample_rate

    return settings.SENTRY_MAX_SAMPLE_TIME


def validate_and_set_timestamp(data, timestamp):
    """
    Helper function for event processors/enhancers to avoid setting broken timestamps.

    If we set a too old or too new timestamp then this affects event retention
    and search.
    """
    if timestamp:
        current = time.time()
        if current - MAX_SECS_IN_PAST > timestamp:
            data.setdefault('errors', []).append({'type': EventError.PAST_TIMESTAMP, 'name': 'timestamp', 'value': timestamp})
        elif timestamp > current + MAX_SECS_IN_FUTURE:
            data.setdefault('errors', []).append({'type': EventError.FUTURE_TIMESTAMP, 'name': 'timestamp', 'value': timestamp})
        else:
            data['timestamp'] = float(timestamp)


def parse_client_as_sdk(value):
    if not value:
        return {}
    try:
        name, version = value.split('/', 1)
    except ValueError:
        try:
            name, version = value.split(' ', 1)
        except ValueError:
            return {}

    return {'name': name, 'version': version}


if not settings.SENTRY_SAMPLE_DATA:

    def should_sample(current_datetime, last_seen, times_seen):
        return False


else:

    def should_sample(current_datetime, last_seen, times_seen):
        silence = current_datetime - last_seen
        if times_seen % count_limit(times_seen) == 0:
            return False
        if times_seen % time_limit(silence) == 0:
            return False
        return True


def plugin_is_regression(group, event):
    project = event.project
    for plugin in plugins.for_project(project):
        result = safe_execute(plugin.is_regression, group, event, version=1, _with_transaction=False)
        if result is not None:
            return result

    return True


def has_pending_commit_resolution(group):
    return GroupLink.objects.filter(group_id=group.id, linked_type=GroupLink.LinkedType.commit, relationship=GroupLink.Relationship.resolves).extra(where=[
     'NOT EXISTS(SELECT 1 FROM sentry_releasecommit where commit_id = sentry_grouplink.linked_id)']).exists()


class HashDiscarded(Exception):
    pass


class ScoreClause(Func):

    def __init__(self, group=None, last_seen=None, times_seen=None, *args, **kwargs):
        self.group = group
        self.last_seen = last_seen
        self.times_seen = times_seen
        if hasattr(self.times_seen, 'rhs'):
            self.times_seen = self.times_seen.rhs.value
        super(ScoreClause, self).__init__(*args, **kwargs)

    def __int__(self):
        if self.group:
            return self.group.get_score()
        return 0

    def as_sql(self, compiler, connection, function=None, template=None):
        db = getattr(connection, 'alias', 'default')
        has_values = self.last_seen is not None and self.times_seen is not None
        if is_postgres(db):
            if has_values:
                sql = 'log(times_seen + %d) * 600 + %d' % (
                 self.times_seen,
                 to_timestamp(self.last_seen))
            else:
                sql = 'log(times_seen) * 600 + last_seen::abstime::int'
        else:
            sql = int(self)
        return (sql, [])


def add_meta_errors(errors, meta):
    for field_meta in meta:
        original_value = field_meta.get().get('val')
        for i, (err_type, err_data) in enumerate(field_meta.iter_errors()):
            error = dict(err_data)
            error['type'] = err_type
            if field_meta.path:
                error['name'] = field_meta.path
            if i == 0 and original_value is not None:
                error['value'] = original_value
            errors.append(error)

    return


def _decode_event(data, content_encoding):
    if isinstance(data, six.binary_type):
        if content_encoding == 'gzip':
            data = decompress_gzip(data)
        elif content_encoding == 'deflate':
            data = decompress_deflate(data)
        elif data[0] != '{':
            data = decode_and_decompress_data(data)
        else:
            data = decode_data(data)
    if isinstance(data, six.text_type):
        data = safely_load_json_string(data)
    return CanonicalKeyDict(data)


class EventManager(object):
    """
    Handles normalization in both the store endpoint and the save task. The
    intention is to swap this class out with a reimplementation in Rust.
    """

    def __init__(self, data, version='5', project=None, grouping_config=None, client_ip=None, user_agent=None, auth=None, key=None, content_encoding=None, is_renormalize=False, remove_other=None, project_config=None):
        self._data = _decode_event(data, content_encoding=content_encoding)
        self.version = version
        self._project = project
        if grouping_config is None and project_config is not None:
            config = project_config.config
            grouping_config = config.get('grouping_config')
        if grouping_config is None and project is not None:
            grouping_config = get_grouping_config_dict_for_project(self._project)
        self._grouping_config = grouping_config
        self._client_ip = client_ip
        self._user_agent = user_agent
        self._auth = auth
        self._key = key
        self._is_renormalize = is_renormalize
        self._remove_other = remove_other
        self._normalized = False
        self.project_config = project_config
        return

    def process_csp_report(self):
        """Only called from the CSP report endpoint."""
        data = self._data
        try:
            interface = get_interface(data.pop('interface'))
            report = data.pop('report')
        except KeyError:
            raise APIForbidden('No report or interface data')

        try:
            instance = report if isinstance(report, interface) else interface.from_raw(report)
        except jsonschema.ValidationError as e:
            raise APIError('Invalid security report: %s' % str(e).splitlines()[0])

        def clean(d):
            return dict(filter(lambda x: x[1], d.items()))

        data.update({'logger': 'csp', 
           'message': instance.get_message(), 
           'culprit': instance.get_culprit(), 
           instance.path: instance.to_json(), 
           'tags': instance.get_tags(), 
           'errors': [], 'user': {'ip_address': self._client_ip}, 'request': {'url': instance.get_origin(), 
                       'headers': clean({'User-Agent': self._user_agent, 'Referer': instance.get_referrer()})}})
        self._data = data

    def normalize(self):
        with metrics.timer('events.store.normalize.duration'):
            self._normalize_impl()
        metrics.timing('events.store.normalize.errors', len(self._data.get('errors') or ()))

    def _normalize_impl(self):
        if self._normalized:
            raise RuntimeError('Already normalized')
        self._normalized = True
        from semaphore.processing import StoreNormalizer
        rust_normalizer = StoreNormalizer(project_id=(self._project.id if self._project else None), client_ip=self._client_ip, client=(self._auth.client if self._auth else None), key_id=(six.text_type(self._key.id) if self._key else None), grouping_config=self._grouping_config, protocol_version=(six.text_type(self.version) if self.version is not None else None), is_renormalize=self._is_renormalize, remove_other=self._remove_other, normalize_user_agent=True, **DEFAULT_STORE_NORMALIZER_ARGS)
        self._data = CanonicalKeyDict(rust_normalizer.normalize_event(dict(self._data)))
        return

    def should_filter(self):
        """
        returns (result: bool, reason: string or None)
        Result is True if an event should be filtered
        The reason for filtering is passed along as a string
        so that we can store it in metrics
        """
        for name in SECURITY_REPORT_INTERFACES:
            if name in self._data:
                interface = get_interface(name)
                if interface.to_python(self._data[name]).should_filter(self._project):
                    return (True, FilterStatKeys.INVALID_CSP)

        if self._client_ip and not is_valid_ip(self.project_config, self._client_ip):
            return (True, FilterStatKeys.IP_ADDRESS)
        else:
            release = self._data.get('release')
            if release and not is_valid_release(self.project_config, release):
                return (True, FilterStatKeys.RELEASE_VERSION)
            error_message = get_path(self._data, 'logentry', 'formatted') or get_path(self._data, 'logentry', 'message') or ''
            if error_message and not is_valid_error_message(self.project_config, error_message):
                return (True, FilterStatKeys.ERROR_MESSAGE)
            for exc in get_path(self._data, 'exception', 'values', filter=True, default=[]):
                message = (': ').join(filter(None, map(exc.get, ['type', 'value'])))
                if message and not is_valid_error_message(self.project_config, message):
                    return (True, FilterStatKeys.ERROR_MESSAGE)

            return should_filter_event(self.project_config, self._data)

    def get_data(self):
        return self._data

    def _get_event_instance(self, project_id=None):
        data = self._data
        event_id = data.get('event_id')
        platform = data.get('platform')
        recorded_timestamp = data.get('timestamp')
        date = datetime.fromtimestamp(recorded_timestamp)
        date = date.replace(tzinfo=timezone.utc)
        time_spent = data.get('time_spent')
        data['node_id'] = Event.generate_node_id(project_id, event_id)
        return Event(project_id=project_id or self._project.id, event_id=event_id, data=EventDict(data, skip_renormalization=True), time_spent=time_spent, datetime=date, platform=platform)

    def get_culprit(self):
        """Helper to calculate the default culprit"""
        return force_text(self._data.get('culprit') or self._data.get('transaction') or generate_culprit(self._data) or '')

    def get_event_type(self):
        """Returns the event type."""
        return eventtypes.get(self._data.get('type', 'default'))()

    def materialize_metadata(self):
        """Returns the materialized metadata to be merged with group or
        event data.  This currently produces the keys `type`, `metadata`,
        `title` and `location`.  This should most likely also produce
        `culprit` here.
        """
        event_type = self.get_event_type()
        event_metadata = event_type.get_metadata(self._data)
        return {'type': event_type.key, 
           'metadata': event_metadata, 
           'title': event_type.get_title(event_metadata), 
           'location': event_type.get_location(event_metadata)}

    def get_search_message(self, event_metadata=None, culprit=None):
        """This generates the internal event.message attribute which is used
        for search purposes.  It adds a bunch of data from the metadata and
        the culprit.
        """
        if event_metadata is None:
            event_metadata = self.get_event_type().get_metadata(self._data)
        if culprit is None:
            culprit = self.get_culprit()
        data = self._data
        message = ''
        if data.get('logentry'):
            message += data['logentry'].get('formatted') or data['logentry'].get('message') or ''
        if event_metadata:
            for value in six.itervalues(event_metadata):
                value_u = force_text(value, errors='replace')
                if value_u not in message:
                    message = ('{} {}').format(message, value_u)

        if culprit and culprit not in message:
            culprit_u = force_text(culprit, errors='replace')
            message = ('{} {}').format(message, culprit_u)
        return trim(message.strip(), settings.SENTRY_MAX_MESSAGE_LENGTH)

    def save(self, project_id, raw=False, assume_normalized=False):
        if not self._normalized:
            if not assume_normalized:
                self.normalize()
            self._normalized = True
        data = self._data
        project = Project.objects.get_from_cache(id=project_id)
        project._organization_cache = Organization.objects.get_from_cache(id=project.organization_id)
        try:
            event = Event.objects.get(project_id=project.id, event_id=data['event_id'])
        except Event.DoesNotExist:
            pass
        else:
            event._project_cache = project
            logger.info('duplicate.found', exc_info=True, extra={'event_uuid': data['event_id'], 
               'project_id': project.id, 
               'model': Event.__name__})
            return event

        culprit = self.get_culprit()
        level = data.get('level')
        if level is not None and isinstance(level, six.integer_types):
            level = LOG_LEVELS[level]
        transaction_name = data.get('transaction')
        logger_name = data.get('logger')
        release = data.get('release')
        dist = data.get('dist')
        environment = data.get('environment')
        recorded_timestamp = data.get('timestamp')
        event = self._get_event_instance(project_id=project_id)
        self._data = data = event.data.data
        event._project_cache = project
        date = event.datetime
        platform = event.platform
        event_id = event.event_id
        if transaction_name:
            transaction_name = force_text(transaction_name)
        if event.get_event_type() == 'transaction':
            issueless_event = True
        else:
            issueless_event = False
        setdefault_path(data, 'tags', value=[])
        set_tag(data, 'level', level)
        if logger_name:
            set_tag(data, 'logger', logger_name)
        if environment:
            set_tag(data, 'environment', environment)
        if transaction_name:
            set_tag(data, 'transaction', transaction_name)
        if release:
            pop_tag(data, 'release')
            release = Release.get_or_create(project=project, version=release, date_added=date)
            set_tag(data, 'sentry:release', release.version)
        if dist and release:
            dist = release.add_dist(dist, date)
            pop_tag(data, 'dist')
            set_tag(data, 'sentry:dist', dist.name)
        else:
            dist = None
        event_user = self._get_event_user(project, data)
        if event_user:
            pop_tag(data, 'user')
            set_tag(data, 'sentry:user', event_user.tag_value)
        grouping_config = load_grouping_config(get_grouping_config_dict_for_event_data(data, project))
        normalize_stacktraces_for_grouping(data, grouping_config)
        for plugin in plugins.for_project(project, version=None):
            added_tags = safe_execute(plugin.get_tags, event, _with_transaction=False)
            if added_tags:
                for key, value in added_tags:
                    if get_tag(data, key) is None:
                        set_tag(data, key, value)

        for path, iface in six.iteritems(event.interfaces):
            for k, v in iface.iter_tags():
                set_tag(data, k, v)

            if iface.ephemeral:
                data.pop(iface.path, None)

        data['fingerprint'] = data.get('fingerprint') or ['{{ default }}']
        apply_server_fingerprinting(data, get_fingerprinting_config_for_project(project))
        try:
            hashes = event.get_hashes()
        except GroupingConfigNotFound:
            data['grouping_config'] = get_grouping_config_dict_for_project(project)
            hashes = event.get_hashes()

        data['hashes'] = hashes
        materialized_metadata = self.materialize_metadata()
        event_metadata = materialized_metadata['metadata']
        data.update(materialized_metadata)
        data['culprit'] = culprit
        event.message = self.get_search_message(event_metadata, culprit)
        received_timestamp = event.data.get('received') or float(event.datetime.strftime('%s'))
        if not issueless_event:
            group_metadata = dict(materialized_metadata)
            group_metadata['last_received'] = received_timestamp
            kwargs = {'platform': platform, 
               'message': event.message, 
               'culprit': culprit, 
               'logger': logger_name, 
               'level': LOG_LEVELS_MAP.get(level), 
               'last_seen': date, 
               'first_seen': date, 
               'active_at': date, 
               'data': group_metadata}
            if release:
                kwargs['first_release'] = release
            try:
                group, is_new, is_regression, is_sample = self._save_aggregate(event=event, hashes=hashes, release=release, **kwargs)
            except HashDiscarded:
                event_discarded.send_robust(project=project, sender=EventManager)
                metrics.incr('events.discarded', skip_internal=True, tags={'organization_id': project.organization_id, 'platform': platform})
                raise
            else:
                event_saved.send_robust(project=project, event_size=event.size, sender=EventManager)

            event.group = group
        else:
            group = None
            is_new = False
            is_regression = False
            is_sample = False
            event_saved.send_robust(project=project, event_size=event.size, sender=EventManager)
        event.data.bind_ref(event)
        environment = Environment.get_or_create(project=project, name=environment)
        if group:
            group_environment, is_new_group_environment = GroupEnvironment.get_or_create(group_id=group.id, environment_id=environment.id, defaults={'first_release': release if release else None})
        else:
            is_new_group_environment = False
        if release:
            ReleaseEnvironment.get_or_create(project=project, release=release, environment=environment, datetime=date)
            ReleaseProjectEnvironment.get_or_create(project=project, release=release, environment=environment, datetime=date)
            if group:
                grouprelease = GroupRelease.get_or_create(group=group, release=release, environment=environment, datetime=date)
        counters = [(tsdb.models.project, project.id)]
        if group:
            counters.append((tsdb.models.group, group.id))
        if release:
            counters.append((tsdb.models.release, release.id))
        tsdb.incr_multi(counters, timestamp=event.datetime, environment_id=environment.id)
        frequencies = []
        if group:
            frequencies.append((
             tsdb.models.frequent_environments_by_group, {group.id: {environment.id: 1}}))
            if release:
                frequencies.append((
                 tsdb.models.frequent_releases_by_group, {group.id: {grouprelease.id: 1}}))
        if frequencies:
            tsdb.record_frequency_multi(frequencies, timestamp=event.datetime)
        if group:
            UserReport.objects.filter(project=project, event_id=event_id).update(group=group, environment=environment)
        if not is_sample:
            try:
                with transaction.atomic(using=router.db_for_write(Event)):
                    event.save()
            except IntegrityError:
                logger.info('duplicate.found', exc_info=True, extra={'event_uuid': event_id, 
                   'project_id': project.id, 
                   'group_id': group.id if group else None, 
                   'model': Event.__name__})
                return event

            tagstore.delay_index_event_tags(organization_id=project.organization_id, project_id=project.id, group_id=group.id if group else None, environment_id=environment.id, event_id=event.id, tags=event.tags, date_added=event.datetime)
        if event_user:
            counters = [(tsdb.models.users_affected_by_project, project.id, (event_user.tag_value,))]
            if group:
                counters.append((
                 tsdb.models.users_affected_by_group, group.id, (event_user.tag_value,)))
            tsdb.record_multi(counters, timestamp=event.datetime, environment_id=environment.id)
        if release:
            if is_new:
                buffer.incr(ReleaseProject, {'new_groups': 1}, {'release_id': release.id, 'project_id': project.id})
            if is_new_group_environment:
                buffer.incr(ReleaseProjectEnvironment, {'new_issues_count': 1}, {'project_id': project.id, 
                   'release_id': release.id, 
                   'environment_id': environment.id})
        if group:
            safe_execute(Group.objects.add_tags, group, environment, event.get_tags(), _with_transaction=False)
        if not raw:
            if not project.first_event:
                project.update(first_event=date)
                first_event_received.send_robust(project=project, event=event, sender=Project)
        eventstream.insert(group=group, event=event, is_new=is_new, is_sample=is_sample, is_regression=is_regression, is_new_group_environment=is_new_group_environment, primary_hash=hashes[0], skip_consume=raw)
        metrics.timing('events.latency', received_timestamp - recorded_timestamp, tags={'project_id': project.id})
        metrics.timing('events.size.data.post_save', event.size, tags={'project_id': project.id})
        return event

    def _get_event_user(self, project, data):
        user_data = data.get('user')
        if not user_data:
            return
        else:
            euser = EventUser(project_id=project.id, ident=user_data.get('id'), email=user_data.get('email'), username=user_data.get('username'), ip_address=user_data.get('ip_address'), name=user_data.get('name'))
            euser.set_hash()
            if not euser.hash:
                return
            cache_key = ('euserid:1:{}:{}').format(project.id, euser.hash)
            euser_id = cache.get(cache_key)
            if euser_id is None:
                try:
                    with transaction.atomic(using=router.db_for_write(EventUser)):
                        euser.save()
                except IntegrityError:
                    try:
                        euser = EventUser.objects.get(project_id=project.id, hash=euser.hash)
                    except EventUser.DoesNotExist:
                        e_userid = -1
                    else:
                        if euser.name != (user_data.get('name') or euser.name):
                            euser.update(name=user_data['name'])
                        e_userid = euser.id

                    cache.set(cache_key, e_userid, 3600)

            return euser

    def _find_hashes(self, project, hash_list):
        return map(lambda hash: GroupHash.objects.get_or_create(project=project, hash=hash)[0], hash_list)

    def _save_aggregate(self, event, hashes, release, **kwargs):
        project = event.project
        all_hashes = self._find_hashes(project, hashes)
        existing_group_id = None
        for h in all_hashes:
            if h.group_id is not None:
                existing_group_id = h.group_id
                break
            if h.group_tombstone_id is not None:
                raise HashDiscarded('Matches group tombstone %s' % h.group_tombstone_id)

        if existing_group_id is None:
            first_release = kwargs.pop('first_release', None)
            with transaction.atomic():
                short_id = project.next_short_id()
                group, group_is_new = Group.objects.create(project=project, short_id=short_id, first_release_id=(Release.objects.filter(id=first_release.id).values_list('id', flat=True).first() if first_release else None), **kwargs), True
            metrics.incr('group.created', skip_internal=True, tags={'platform': event.platform or 'unknown'})
        else:
            group = Group.objects.get(id=existing_group_id)
            group_is_new = False
        is_new = False
        new_hashes = [ h for h in all_hashes if h.group_id is None ]
        if new_hashes:
            GroupHash.objects.filter(id__in=[ h.id for h in new_hashes ]).exclude(state=GroupHash.State.LOCKED_IN_MIGRATION).update(group=group)
            if group_is_new and len(new_hashes) == len(all_hashes):
                is_new = True
        can_sample = features.has('projects:sample-events', project=project) and should_sample(event.data.get('received') or float(event.datetime.strftime('%s')), group.data.get('last_received') or float(group.last_seen.strftime('%s')), group.times_seen)
        if not is_new:
            is_regression = self._process_existing_aggregate(group=group, event=event, data=kwargs, release=release)
        else:
            is_regression = False
        if is_new or is_regression:
            is_sample = False
        else:
            is_sample = can_sample
        return (group, is_new, is_regression, is_sample)

    def _handle_regression(self, group, event, release):
        if not group.is_resolved():
            return
        if GroupResolution.has_resolution(group, release):
            return
        if has_pending_commit_resolution(group):
            return
        if not plugin_is_regression(group, event):
            return
        date = max(event.datetime, group.last_seen)
        is_regression = bool(Group.objects.filter(id=group.id, status__in=[
         GroupStatus.RESOLVED, GroupStatus.UNRESOLVED]).exclude(active_at__gte=date - timedelta(seconds=5)).update(active_at=date, last_seen=date, status=GroupStatus.UNRESOLVED))
        group.active_at = date
        group.status = GroupStatus.UNRESOLVED
        if is_regression and release:
            try:
                resolution = GroupResolution.objects.get(group=group)
            except GroupResolution.DoesNotExist:
                affected = False
            else:
                cursor = connection.cursor()
                cursor.execute('DELETE FROM sentry_groupresolution WHERE id = %s', [resolution.id])
                affected = cursor.rowcount > 0

            if affected:
                try:
                    activity = Activity.objects.filter(group=group, type=Activity.SET_RESOLVED_IN_RELEASE, ident=resolution.id).order_by('-datetime')[0]
                except IndexError:
                    pass
                else:
                    activity.update(data={'version': release.version})

        if is_regression:
            activity = Activity.objects.create(project=group.project, group=group, type=Activity.SET_REGRESSION, data={'version': release.version if release else ''})
            activity.send_notification()
            kick_off_status_syncs.apply_async(kwargs={'project_id': group.project_id, 'group_id': group.id})
        return is_regression

    def _process_existing_aggregate(self, group, event, data, release):
        date = max(event.datetime, group.last_seen)
        extra = {'last_seen': date, 'score': ScoreClause(group), 'data': data['data']}
        if event.message and event.message != group.message:
            extra['message'] = event.message
        if group.level != data['level']:
            extra['level'] = data['level']
        if group.culprit != data['culprit']:
            extra['culprit'] = data['culprit']
        is_regression = self._handle_regression(group, event, release)
        group.last_seen = extra['last_seen']
        update_kwargs = {'times_seen': 1}
        buffer.incr(Group, update_kwargs, {'id': group.id}, extra)
        return is_regression