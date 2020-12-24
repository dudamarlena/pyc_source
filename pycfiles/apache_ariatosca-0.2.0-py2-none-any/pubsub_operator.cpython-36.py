# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/pubsub_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 16184 bytes
from airflow.contrib.hooks.gcp_pubsub_hook import PubSubHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PubSubTopicCreateOperator(BaseOperator):
    """PubSubTopicCreateOperator"""
    template_fields = [
     'project', 'topic']
    ui_color = '#0273d4'

    @apply_defaults
    def __init__(self, project, topic, fail_if_exists=False, gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        """
        :param project: the GCP project ID where the topic will be created
        :type project: str
        :param topic: the topic to create. Do not include the
            full topic path. In other words, instead of
            ``projects/{project}/topics/{topic}``, provide only
            ``{topic}``. (templated)
        :type topic: str
        :param gcp_conn_id: The connection ID to use connecting to
            Google Cloud Platform.
        :type gcp_conn_id: str
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request
            must have domain-wide delegation enabled.
        :type delegate_to: str
        """
        (super(PubSubTopicCreateOperator, self).__init__)(*args, **kwargs)
        self.project = project
        self.topic = topic
        self.fail_if_exists = fail_if_exists
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        hook = PubSubHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        hook.create_topic((self.project), (self.topic), fail_if_exists=(self.fail_if_exists))


class PubSubSubscriptionCreateOperator(BaseOperator):
    """PubSubSubscriptionCreateOperator"""
    template_fields = [
     'topic_project', 'topic', 'subscription',
     'subscription_project']
    ui_color = '#0273d4'

    @apply_defaults
    def __init__(self, topic_project, topic, subscription=None, subscription_project=None, ack_deadline_secs=10, fail_if_exists=False, gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        """
        :param topic_project: the GCP project ID where the topic exists
        :type topic_project: str
        :param topic: the topic to create. Do not include the
            full topic path. In other words, instead of
            ``projects/{project}/topics/{topic}``, provide only
            ``{topic}``. (templated)
        :type topic: str
        :param subscription: the Pub/Sub subscription name. If empty, a random
            name will be generated using the uuid module
        :type subscription: str
        :param subscription_project: the GCP project ID where the subscription
            will be created. If empty, ``topic_project`` will be used.
        :type subscription_project: str
        :param ack_deadline_secs: Number of seconds that a subscriber has to
            acknowledge each message pulled from the subscription
        :type ack_deadline_secs: int
        :param gcp_conn_id: The connection ID to use connecting to
            Google Cloud Platform.
        :type gcp_conn_id: str
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request
            must have domain-wide delegation enabled.
        :type delegate_to: str
        """
        (super(PubSubSubscriptionCreateOperator, self).__init__)(*args, **kwargs)
        self.topic_project = topic_project
        self.topic = topic
        self.subscription = subscription
        self.subscription_project = subscription_project
        self.ack_deadline_secs = ack_deadline_secs
        self.fail_if_exists = fail_if_exists
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        hook = PubSubHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        return hook.create_subscription(self.topic_project, self.topic, self.subscription, self.subscription_project, self.ack_deadline_secs, self.fail_if_exists)


class PubSubTopicDeleteOperator(BaseOperator):
    """PubSubTopicDeleteOperator"""
    template_fields = [
     'project', 'topic']
    ui_color = '#cb4335'

    @apply_defaults
    def __init__(self, project, topic, fail_if_not_exists=False, gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        """
        :param project: the GCP project ID in which to work (templated)
        :type project: str
        :param topic: the topic to delete. Do not include the
            full topic path. In other words, instead of
            ``projects/{project}/topics/{topic}``, provide only
            ``{topic}``. (templated)
        :type topic: str
        :param fail_if_not_exists: If True and the topic does not exist, fail
            the task
        :type fail_if_not_exists: bool
        :param gcp_conn_id: The connection ID to use connecting to
            Google Cloud Platform.
        :type gcp_conn_id: str
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request
            must have domain-wide delegation enabled.
        :type delegate_to: str
        """
        (super(PubSubTopicDeleteOperator, self).__init__)(*args, **kwargs)
        self.project = project
        self.topic = topic
        self.fail_if_not_exists = fail_if_not_exists
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        hook = PubSubHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        hook.delete_topic((self.project), (self.topic), fail_if_not_exists=(self.fail_if_not_exists))


class PubSubSubscriptionDeleteOperator(BaseOperator):
    """PubSubSubscriptionDeleteOperator"""
    template_fields = [
     'project', 'subscription']
    ui_color = '#cb4335'

    @apply_defaults
    def __init__(self, project, subscription, fail_if_not_exists=False, gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        """
        :param project: the GCP project ID in which to work (templated)
        :type project: str
        :param subscription: the subscription to delete. Do not include the
            full subscription path. In other words, instead of
            ``projects/{project}/subscription/{subscription}``, provide only
            ``{subscription}``. (templated)
        :type subscription: str
        :param fail_if_not_exists: If True and the subscription does not exist,
            fail the task
        :type fail_if_not_exists: bool
        :param gcp_conn_id: The connection ID to use connecting to
            Google Cloud Platform.
        :type gcp_conn_id: str
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request
            must have domain-wide delegation enabled.
        :type delegate_to: str
        """
        (super(PubSubSubscriptionDeleteOperator, self).__init__)(*args, **kwargs)
        self.project = project
        self.subscription = subscription
        self.fail_if_not_exists = fail_if_not_exists
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        hook = PubSubHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        hook.delete_subscription((self.project), (self.subscription), fail_if_not_exists=(self.fail_if_not_exists))


class PubSubPublishOperator(BaseOperator):
    """PubSubPublishOperator"""
    template_fields = [
     'project', 'topic', 'messages']
    ui_color = '#0273d4'

    @apply_defaults
    def __init__(self, project, topic, messages, gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        """
        :param project: the GCP project ID in which to work (templated)
        :type project: str
        :param topic: the topic to which to publish. Do not include the
            full topic path. In other words, instead of
            ``projects/{project}/topics/{topic}``, provide only
            ``{topic}``. (templated)
        :type topic: str
        :param messages: a list of messages to be published to the
            topic. Each message is a dict with one or more of the
            following keys-value mappings:
            * 'data': a base64-encoded string
            * 'attributes': {'key1': 'value1', ...}
            Each message must contain at least a non-empty 'data' value
            or an attribute dict with at least one key (templated). See
            https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage
        :type messages: list
        :param gcp_conn_id: The connection ID to use connecting to
            Google Cloud Platform.
        :type gcp_conn_id: str
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request
            must have domain-wide delegation enabled.
        :type delegate_to: str
        """
        (super(PubSubPublishOperator, self).__init__)(*args, **kwargs)
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.project = project
        self.topic = topic
        self.messages = messages

    def execute(self, context):
        hook = PubSubHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        hook.publish(self.project, self.topic, self.messages)