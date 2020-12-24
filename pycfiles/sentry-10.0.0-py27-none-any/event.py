# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/event.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six, string, warnings, pytz
from collections import OrderedDict
from dateutil.parser import parse as parse_date
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from hashlib import md5
from semaphore.processing import StoreNormalizer
from sentry import eventtypes
from sentry.db.models import BoundedBigIntegerField, BoundedIntegerField, Model, NodeData, NodeField, sane_repr
from sentry.db.models.manager import EventManager
from sentry.interfaces.base import get_interfaces
from sentry.utils import json
from sentry.utils.cache import memoize
from sentry.utils.canonical import CanonicalKeyDict, CanonicalKeyView
from sentry.utils.safe import get_path
from sentry.utils.strings import truncatechars

class EventDict(CanonicalKeyDict):
    """
    Creating an instance of this dictionary will send the event through basic
    (Rust-based) type/schema validation called "re-normalization".

    This is used as a wrapper type for `Event.data` such that creating an event
    object (or loading it from the DB) will ensure the data fits the type
    schema.
    """

    def __init__(self, data, skip_renormalization=False, **kwargs):
        is_renormalized = isinstance(data, EventDict) or isinstance(data, NodeData) and isinstance(data.data, EventDict)
        if not skip_renormalization and not is_renormalized:
            normalizer = StoreNormalizer(is_renormalize=True, enable_trimming=False)
            data = normalizer.normalize_event(dict(data))
        CanonicalKeyDict.__init__(self, data, **kwargs)


class EventCommon(object):
    """
    Methods and properties common to both Event and SnubaEvent.
    """

    @classmethod
    def generate_node_id(cls, project_id, event_id):
        """
        Returns a deterministic node_id for this event based on the project_id
        and event_id which together are globally unique. The event body should
        be saved under this key in nodestore so it can be retrieved using the
        same generated id when we only have project_id and event_id.
        """
        return md5(('{}:{}').format(project_id, event_id)).hexdigest()

    @property
    def group(self):
        from sentry.models import Group
        if not self.group_id:
            return None
        else:
            if not hasattr(self, '_group_cache'):
                self._group_cache = Group.objects.get(id=self.group_id)
            return self._group_cache

    @group.setter
    def group(self, group):
        self.group_id = group.id
        self._group_cache = group

    @property
    def project(self):
        from sentry.models import Project
        if not hasattr(self, '_project_cache'):
            self._project_cache = Project.objects.get(id=self.project_id)
        return self._project_cache

    @project.setter
    def project(self, project):
        if project is None:
            self.project_id = None
        else:
            self.project_id = project.id
        self._project_cache = project
        return

    def get_interfaces(self):
        return CanonicalKeyView(get_interfaces(self.data))

    @memoize
    def interfaces(self):
        return self.get_interfaces()

    def get_interface(self, name):
        return self.interfaces.get(name)

    def get_legacy_message(self):
        return get_path(self.data, 'logentry', 'formatted') or get_path(self.data, 'logentry', 'message') or self.message

    def get_event_type(self):
        """
        Return the type of this event.

        See ``sentry.eventtypes``.
        """
        return self.data.get('type', 'default')

    def get_event_metadata(self):
        """
        Return the metadata of this event.

        See ``sentry.eventtypes``.
        """
        return self.data.get('metadata') or {}

    def get_grouping_config(self):
        """Returns the event grouping config."""
        from sentry.grouping.api import get_grouping_config_dict_for_event_data
        return get_grouping_config_dict_for_event_data(self.data, self.project)

    def get_hashes(self, force_config=None):
        """
        Returns the calculated hashes for the event.  This uses the stored
        information if available.  Grouping hashes will take into account
        fingerprinting and checksums.
        """
        if force_config is None:
            hashes = self.data.get('hashes')
            if hashes is not None:
                return hashes
        return filter(None, [ x.get_hash() for x in self.get_grouping_variants(force_config).values() ])

    def get_grouping_variants(self, force_config=None, normalize_stacktraces=False):
        """
        This is similar to `get_hashes` but will instead return the
        grouping components for each variant in a dictionary.

        If `normalize_stacktraces` is set to `True` then the event data will be
        modified for `in_app` in addition to event variants being created.  This
        means that after calling that function the event data has been modified
        in place.
        """
        from sentry.grouping.api import get_grouping_variants_for_event, load_grouping_config
        from sentry.stacktraces.processing import normalize_stacktraces_for_grouping
        if force_config is not None:
            if isinstance(force_config, six.string_types):
                stored_config = self.get_grouping_config()
                config = dict(stored_config)
                config['id'] = force_config
            else:
                config = force_config
        else:
            config = self.data.get('grouping_config')
        config = load_grouping_config(config)
        if normalize_stacktraces:
            normalize_stacktraces_for_grouping(self.data, config)
        return get_grouping_variants_for_event(self, config)

    def get_primary_hash(self):
        return self.get_hashes()[0]

    @property
    def title(self):
        et = eventtypes.get(self.get_event_type())()
        return et.get_title(self.get_event_metadata())

    @property
    def culprit(self):
        if self.group_id:
            return self.data.get('culprit') or self.group.culprit
        return self.data.get('culprit')

    @property
    def location(self):
        et = eventtypes.get(self.get_event_type())()
        return et.get_location(self.get_event_metadata())

    @property
    def real_message(self):
        return get_path(self.data, 'logentry', 'formatted') or get_path(self.data, 'logentry', 'message') or ''

    @property
    def organization(self):
        return self.project.organization

    @property
    def version(self):
        return self.data.get('version', '5')

    @property
    def ip_address(self):
        ip_address = get_path(self.data, 'user', 'ip_address')
        if ip_address:
            return ip_address
        else:
            remote_addr = get_path(self.data, 'request', 'env', 'REMOTE_ADDR')
            if remote_addr:
                return remote_addr
            return

    @property
    def tags(self):
        try:
            rv = sorted([ (t, v) for t, v in get_path(self.data, 'tags', filter=True) or () if t is not None and v is not None
                        ])
            return rv
        except ValueError:
            return []

        return

    def get_tags(self):
        return self.tags

    def get_tag(self, key):
        for t, v in self.get_tags():
            if t == key:
                return v

        return

    @property
    def release(self):
        return self.get_tag('sentry:release')

    @property
    def dist(self):
        return self.get_tag('sentry:dist')

    def get_raw_data(self):
        """Returns the internal raw event data dict."""
        return dict(self.data.items())

    @property
    def size(self):
        return len(json.dumps(dict(self.data)))

    @property
    def transaction(self):
        return self.get_tag('transaction')

    def get_email_subject(self):
        template = self.project.get_option('mail:subject_template')
        if template:
            template = EventSubjectTemplate(template)
        else:
            template = DEFAULT_SUBJECT_TEMPLATE
        return truncatechars(template.safe_substitute(EventSubjectTemplateData(self)), 128).encode('utf-8')

    def get_environment(self):
        from sentry.models import Environment
        if not hasattr(self, '_environment_cache'):
            self._environment_cache = Environment.objects.get(organization_id=self.project.organization_id, name=Environment.get_name_or_default(self.get_tag('environment')))
        return self._environment_cache

    def get_minimal_user(self):
        """
        A minimal 'User' interface object that gives us enough information
        to render a user badge.
        """
        return self.get_interface('user')

    def as_dict(self):
        """Returns the data in normalized form for external consumers."""
        data = OrderedDict()
        data['event_id'] = self.event_id
        data['project'] = self.project_id
        data['release'] = self.release
        data['dist'] = self.dist
        data['platform'] = self.platform
        data['message'] = self.real_message
        data['datetime'] = self.datetime
        data['time_spent'] = self.time_spent
        data['tags'] = [ (k.split('sentry:', 1)[(-1)], v) for k, v in self.tags ]
        for k, v in sorted(six.iteritems(self.data)):
            if k in data:
                continue
            if k == 'sdk':
                v = {v_k:v_v for v_k, v_v in six.iteritems(v) if v_k != 'client_ip' if v_k != 'client_ip'}
            data[k] = v

        if data.get('culprit') is None and self.group_id:
            data['culprit'] = self.group.culprit
        data['title'] = self.title
        data['location'] = self.location
        return data

    @property
    def level(self):
        if self.group:
            return self.group.level
        else:
            return
            return

    def get_level_display(self):
        if self.group:
            return self.group.get_level_display()
        else:
            return
            return

    @property
    def logger(self):
        warnings.warn('Event.logger is deprecated. Use Event.tags instead.', DeprecationWarning)
        return self.get_tag('logger')

    @property
    def site(self):
        warnings.warn('Event.site is deprecated. Use Event.tags instead.', DeprecationWarning)
        return self.get_tag('site')

    @property
    def server_name(self):
        warnings.warn('Event.server_name is deprecated. Use Event.tags instead.', DeprecationWarning)
        return self.get_tag('server_name')

    @property
    def checksum(self):
        warnings.warn('Event.checksum is no longer used', DeprecationWarning)
        return ''

    def error(self):
        warnings.warn('Event.error is deprecated, use Event.title', DeprecationWarning)
        return self.title

    error.short_description = _('error')

    @property
    def message_short(self):
        warnings.warn('Event.message_short is deprecated, use Event.title', DeprecationWarning)
        return self.title


class SnubaEvent(EventCommon):
    """
        An event backed by data stored in snuba.

        This is a readonly event and does not support event creation or save.
        The basic event data is fetched from snuba, and the event body is
        fetched from nodestore and bound to the data property in the same way
        as a regular Event.
    """
    minimal_columns = [
     'event_id', 'group_id', 'project_id', 'timestamp']
    selected_columns = minimal_columns + [
     'culprit',
     'location',
     'message',
     'platform',
     'title',
     'type',
     'tags.key',
     'tags.value',
     'email',
     'ip_address',
     'user_id',
     'username']
    __repr__ = sane_repr('project_id', 'group_id')

    def __init__(self, snuba_values):
        """
            When initializing a SnubaEvent, think about the attributes you
            might need to access on it. If you only need a few properties, and
            they are all available in snuba, then you should use
            `SnubaEvent.selected_colums` (or a subset depending on your needs)
            But if you know you are going to need the entire event body anyway
            (which requires a nodestore lookup) you may as well just initialize
            the event with `SnubaEvent.minimal_colums` and let the rest of of
            the attributes come from nodestore.
        """
        assert all(k in snuba_values for k in SnubaEvent.minimal_columns)
        self.snuba_data = snuba_values
        node_id = SnubaEvent.generate_node_id(self.snuba_data['project_id'], self.snuba_data['event_id'])
        self.data = NodeData(None, node_id, data=None, wrapper=EventDict)
        return

    def __getattr__(self, name):
        """
        Depending on what snuba data this event was initialized with, we may
        have the data available to return, or we may have to look in the
        `data` dict (which would force a nodestore load). All unresolved
        self.foo type accesses will come through here.
        """
        if name in ('_project_cache', '_group_cache', '_environment_cache'):
            raise AttributeError()
        if name in self.snuba_data:
            return self.snuba_data[name]
        else:
            return self.data[name]

    @property
    def tags(self):
        """
        Override of tags property that uses tags from snuba rather than
        the nodestore event body. This might be useful for implementing
        tag deletions without having to rewrite nodestore blobs.
        """
        if 'tags.key' in self.snuba_data and 'tags.value' in self.snuba_data:
            keys = getattr(self, 'tags.key')
            values = getattr(self, 'tags.value')
            if keys and values and len(keys) == len(values):
                return sorted(zip(keys, values))
            return []
        else:
            return super(SnubaEvent, self).tags

    def get_minimal_user(self):
        from sentry.interfaces.user import User
        return User.to_python({'id': self.user_id, 
           'email': self.email, 
           'username': self.username, 
           'ip_address': self.ip_address})

    def get_event_type(self):
        if 'type' in self.snuba_data:
            return self.snuba_data['type']
        return super(SnubaEvent, self).get_event_type()

    @property
    def ip_address(self):
        if 'ip_address' in self.snuba_data:
            return self.snuba_data['ip_address']
        return super(SnubaEvent, self).ip_address

    @property
    def title(self):
        if 'title' in self.snuba_data:
            return self.snuba_data['title']
        return super(SnubaEvent, self).title

    @property
    def culprit(self):
        if 'culprit' in self.snuba_data:
            return self.snuba_data['culprit']
        return super(SnubaEvent, self).culprit

    @property
    def location(self):
        if 'location' in self.snuba_data:
            return self.snuba_data['location']
        return super(SnubaEvent, self).location

    @property
    def datetime(self):
        """
        Reconstruct the datetime of this event from the snuba timestamp
        """
        return parse_date(self.timestamp).replace(tzinfo=pytz.utc)

    @property
    def time_spent(self):
        return

    @property
    def message(self):
        if 'message' in self.snuba_data:
            return self.snuba_data['message']
        return self.data.get('message')

    @property
    def platform(self):
        if 'platform' in self.snuba_data:
            return self.snuba_data['platform']
        return self.data.get('platform')

    @property
    def id(self):
        return self.event_id

    def save(self):
        raise NotImplementedError


class Event(EventCommon, Model):
    """
    An event backed by data stored in postgres.

    """
    __core__ = False
    group_id = BoundedBigIntegerField(blank=True, null=True)
    event_id = models.CharField(max_length=32, null=True, db_column='message_id')
    project_id = BoundedBigIntegerField(blank=True, null=True)
    message = models.TextField()
    platform = models.CharField(max_length=64, null=True)
    datetime = models.DateTimeField(default=timezone.now, db_index=True)
    time_spent = BoundedIntegerField(null=True)
    data = NodeField(blank=True, null=True, ref_func=lambda x: x.project_id or x.project.id, ref_version=2, wrapper=EventDict)
    objects = EventManager()

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_message'
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        unique_together = (('project_id', 'event_id'), )
        index_together = (('group_id', 'datetime'), )

    __repr__ = sane_repr('project_id', 'group_id')

    def __getstate__(self):
        state = Model.__getstate__(self)
        state.pop('_project_cache', None)
        state.pop('_environment_cache', None)
        state.pop('_group_cache', None)
        state.pop('interfaces', None)
        return state


class EventSubjectTemplate(string.Template):
    idpattern = '(tag:)?[_a-z][_a-z0-9]*'


class EventSubjectTemplateData(object):
    tag_aliases = {'release': 'sentry:release', 'dist': 'sentry:dist', 'user': 'sentry:user'}

    def __init__(self, event):
        self.event = event

    def __getitem__(self, name):
        if name.startswith('tag:'):
            name = name[4:]
            value = self.event.get_tag(self.tag_aliases.get(name, name))
            if value is None:
                raise KeyError
            return six.text_type(value)
        else:
            if name == 'project':
                return self.event.project.get_full_name()
            if name == 'projectID':
                return self.event.project.slug
            if name == 'shortID' and self.event.group_id:
                return self.event.group.qualified_short_id
            if name == 'orgID':
                return self.event.organization.slug
            if name == 'title':
                return self.event.title
            raise KeyError
            return


DEFAULT_SUBJECT_TEMPLATE = EventSubjectTemplate('$shortID - $title')