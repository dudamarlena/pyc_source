# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/digests/notifications.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import functools, itertools, logging, six
from collections import OrderedDict, defaultdict, namedtuple
from six.moves import reduce
from sentry.app import tsdb
from sentry.digests import Record
from sentry.models import Project, Group, GroupStatus, Rule
from sentry.utils.dates import to_timestamp
logger = logging.getLogger('sentry.digests')
Notification = namedtuple('Notification', 'event rules')

def split_key(key):
    from sentry.plugins import plugins
    plugin_slug, _, project_id = key.split(':', 2)
    return (plugins.get(plugin_slug), Project.objects.get(pk=project_id))


def unsplit_key(plugin, project):
    return ('{plugin.slug}:p:{project.id}').format(plugin=plugin, project=project)


def strip_for_serialization(instance):
    cls = type(instance)
    return cls(**{field.attname:getattr(instance, field.attname) for field in cls._meta.fields})


def event_to_record(event, rules):
    if not rules:
        logger.warning('Creating record for %r that does not contain any rules!', event)
    return Record(event.event_id, Notification(strip_for_serialization(event), [ rule.id for rule in rules ]), to_timestamp(event.datetime))


def fetch_state(project, records):
    start = records[(-1)].datetime
    end = records[0].datetime
    groups = Group.objects.in_bulk(record.value.event.group_id for record in records)
    return {'project': project, 
       'groups': groups, 
       'rules': Rule.objects.in_bulk(itertools.chain.from_iterable(record.value.rules for record in records)), 
       'event_counts': tsdb.get_sums(tsdb.models.group, groups.keys(), start, end), 
       'user_counts': tsdb.get_distinct_counts_totals(tsdb.models.users_affected_by_group, groups.keys(), start, end)}


def attach_state(project, groups, rules, event_counts, user_counts):
    for id, group in six.iteritems(groups):
        assert group.project_id == project.id, 'Group must belong to Project'
        group.project = project

    for id, rule in six.iteritems(rules):
        assert rule.project_id == project.id, 'Rule must belong to Project'
        rule.project = project

    for id, event_count in six.iteritems(event_counts):
        groups[id].event_count = event_count

    for id, user_count in six.iteritems(user_counts):
        groups[id].user_count = user_count

    return {'project': project, 'groups': groups, 'rules': rules}


class Pipeline(object):

    def __init__(self):
        self.operations = []

    def __call__(self, sequence):
        return reduce(lambda x, operation: operation(x), self.operations, sequence)

    def apply(self, function):

        def operation(sequence):
            result = function(sequence)
            logger.debug('%r applied to %s items.', function, len(sequence))
            return result

        self.operations.append(operation)
        return self

    def filter(self, function):

        def operation(sequence):
            result = [ s for s in sequence if function(s) ]
            logger.debug('%r filtered %s items to %s.', function, len(sequence), len(result))
            return result

        self.operations.append(operation)
        return self

    def map(self, function):

        def operation(sequence):
            result = [ function(s) for s in sequence ]
            logger.debug('%r applied to %s items.', function, len(sequence))
            return result

        self.operations.append(operation)
        return self

    def reduce(self, function, initializer):

        def operation(sequence):
            result = reduce(function, sequence, initializer(sequence))
            logger.debug('%r reduced %s items to %s.', function, len(sequence), len(result))
            return result

        self.operations.append(operation)
        return self


def rewrite_record(record, project, groups, rules):
    event = record.value.event
    group = groups.get(event.group_id)
    if group is not None:
        event.group = group
    else:
        logger.debug('%r could not be associated with a group.', record)
        return
    return Record(record.key, Notification(event, filter(None, [ rules.get(id) for id in record.value.rules ])), record.timestamp)


def group_records(groups, record):
    group = record.value.event.group
    rules = record.value.rules
    if not rules:
        logger.debug('%r has no associated rules, and will not be added to any groups.', record)
    for rule in rules:
        groups[rule][group].append(record)

    return groups


def sort_group_contents(rules):
    for key, groups in six.iteritems(rules):
        rules[key] = OrderedDict(sorted(groups.items(), key=lambda x: (
         x[0].event_count, x[0].user_count), reverse=True))

    return rules


def sort_rule_groups(rules):
    return OrderedDict(sorted(rules.items(), key=lambda x: len(x[1]), reverse=True))


def build_digest(project, records, state=None):
    records = list(records)
    if not records:
        return
    else:
        if state is None:
            state = fetch_state(project, records)
        state = attach_state(**state)

        def check_group_state(record):
            return record.value.event.group.get_status() == GroupStatus.UNRESOLVED

        pipeline = Pipeline().map(functools.partial(rewrite_record, **state)).filter(bool).filter(check_group_state).reduce(group_records, lambda sequence: defaultdict(lambda : defaultdict(list))).apply(sort_group_contents).apply(sort_rule_groups)
        return pipeline(records)