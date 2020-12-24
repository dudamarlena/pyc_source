# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/incidents/tasks.py
# Compiled at: 2019-09-04 11:05:35
from __future__ import absolute_import
from uuid import uuid4
from django.core.urlresolvers import reverse
from django.db import transaction
from six.moves.urllib.parse import urlencode
from sentry import deletions
from sentry.app import locks
from sentry.auth.access import from_user
from sentry.exceptions import DeleteAborted
from sentry.incidents.models import AlertRule, AlertRuleStatus, Incident, IncidentActivity, IncidentActivityType, IncidentStatus, IncidentSuspectCommit
from sentry.snuba.query_subscription_consumer import register_subscriber
from sentry.tasks.base import instrumented_task, retry
from sentry.utils.email import MessageBuilder
from sentry.utils.http import absolute_uri
from sentry.utils.linksign import generate_signed_link
from sentry.utils.retries import TimedRetryPolicy
INCIDENTS_SNUBA_SUBSCRIPTION_TYPE = 'incidents'

@instrumented_task(name='sentry.incidents.tasks.send_subscriber_notifications', queue='incidents')
def send_subscriber_notifications(activity_id):
    from sentry.incidents.logic import get_incident_subscribers, unsubscribe_from_incident
    try:
        activity = IncidentActivity.objects.select_related('incident', 'user', 'incident__organization').get(id=activity_id)
    except IncidentActivity.DoesNotExist:
        return

    if activity.type not in (
     IncidentActivityType.COMMENT.value,
     IncidentActivityType.STATUS_CHANGE.value):
        return
    projects = list(activity.incident.projects.all())
    for subscriber in get_incident_subscribers(activity.incident).select_related('user'):
        user = subscriber.user
        access = from_user(user, activity.incident.organization)
        if not any(project for project in projects if access.has_project_access(project)):
            unsubscribe_from_incident(activity.incident, user)
        elif user != activity.user:
            msg = generate_incident_activity_email(activity, user)
            msg.send_async([user.email])


def generate_incident_activity_email(activity, user):
    incident = activity.incident
    return MessageBuilder(subject=('Activity on Incident {} (#{})').format(incident.title, incident.identifier), template='sentry/emails/incidents/activity.txt', html_template='sentry/emails/incidents/activity.html', type='incident.activity', context=build_activity_context(activity, user))


def build_activity_context(activity, user):
    if activity.type == IncidentActivityType.COMMENT.value:
        action = 'left a comment'
    else:
        action = 'changed status from %s to %s' % (
         IncidentStatus(int(activity.previous_value)).name.lower(),
         IncidentStatus(int(activity.value)).name.lower())
    incident = activity.incident
    action = '%s on incident %s (#%s)' % (action, incident.title, incident.identifier)
    return {'user_name': activity.user.name if activity.user else 'Sentry', 
       'action': action, 
       'link': absolute_uri(reverse('sentry-incident', kwargs={'organization_slug': incident.organization.slug, 'incident_id': incident.identifier})) + '?' + urlencode({'referrer': 'incident_activity_email'}), 
       'comment': activity.comment, 
       'unsubscribe_link': generate_signed_link(user, 'sentry-account-email-unsubscribe-incident', kwargs={'incident_id': incident.id})}


@instrumented_task(name='sentry.incidents.tasks.calculate_incident_suspects', queue='incidents')
def calculate_incident_suspects(incident_id):
    from sentry.incidents.logic import get_incident_suspect_commits
    lock = locks.get(('incident:suspects:{}').format(incident_id), duration=600)
    with TimedRetryPolicy(60)(lock.acquire):
        incident = Incident.objects.get(id=incident_id)
        suspect_commits = get_incident_suspect_commits(incident)
        with transaction.atomic():
            IncidentSuspectCommit.objects.filter(incident=incident).delete()
            IncidentSuspectCommit.objects.bulk_create([ IncidentSuspectCommit(incident=incident, commit_id=commit_id, order=i) for i, commit_id in enumerate(suspect_commits)
                                                      ])


@instrumented_task(name='sentry.incidents.tasks.delete_alert_rule', queue='cleanup', default_retry_delay=300, max_retries=1)
@retry(exclude=(DeleteAborted,))
def delete_alert_rule(alert_rule_id, transaction_id=None, **kwargs):
    from sentry.incidents.models import AlertRule
    try:
        instance = AlertRule.objects_with_deleted.get(id=alert_rule_id)
    except AlertRule.DoesNotExist:
        return

    if instance.status not in (
     AlertRuleStatus.DELETION_IN_PROGRESS.value,
     AlertRuleStatus.PENDING_DELETION.value):
        raise DeleteAborted
    task = deletions.get(model=AlertRule, query={'id': alert_rule_id}, transaction_id=transaction_id or uuid4().hex)
    has_more = task.chunk()
    if has_more:
        delete_alert_rule.apply_async(kwargs={'alert_rule_id': alert_rule_id, 'transaction_id': transaction_id}, countdown=15)


class AlertRuleDeletionTask(deletions.ModelDeletionTask):
    manager_name = 'objects_with_deleted'


deletions.default_manager.register(AlertRule, AlertRuleDeletionTask)

@register_subscriber(INCIDENTS_SNUBA_SUBSCRIPTION_TYPE)
def handle_snuba_query_update(subscription_update, subscription):
    """
    Handles a subscription update for a `QuerySubscription`.
    :param subscription_update: dict formatted according to schemas in
    sentry/snuba/json_schemas.py
    :param subscription: The `QuerySubscription` that this update is for
    """
    pass