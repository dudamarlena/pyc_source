# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/pubsub_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 16184 bytes
from airflow.contrib.hooks.gcp_pubsub_hook import PubSubHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PubSubTopicCreateOperator(BaseOperator):
    __doc__ = "Create a PubSub topic.\n\n    By default, if the topic already exists, this operator will\n    not cause the DAG to fail. ::\n\n        with DAG('successful DAG') as dag:\n            (\n                dag\n                >> PubSubTopicCreateOperator(project='my-project',\n                                             topic='my_new_topic')\n                >> PubSubTopicCreateOperator(project='my-project',\n                                             topic='my_new_topic')\n            )\n\n    The operator can be configured to fail if the topic already exists. ::\n\n        with DAG('failing DAG') as dag:\n            (\n                dag\n                >> PubSubTopicCreateOperator(project='my-project',\n                                             topic='my_new_topic')\n                >> PubSubTopicCreateOperator(project='my-project',\n                                             topic='my_new_topic',\n                                             fail_if_exists=True)\n            )\n\n    Both ``project`` and ``topic`` are templated so you can use\n    variables in them.\n    "
    template_fields = ['project', 'topic']
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
    __doc__ = "Create a PubSub subscription.\n\n    By default, the subscription will be created in ``topic_project``. If\n    ``subscription_project`` is specified and the GCP credentials allow, the\n    Subscription can be created in a different project from its topic.\n\n    By default, if the subscription already exists, this operator will\n    not cause the DAG to fail. However, the topic must exist in the project. ::\n\n        with DAG('successful DAG') as dag:\n            (\n                dag\n                >> PubSubSubscriptionCreateOperator(\n                    topic_project='my-project', topic='my-topic',\n                    subscription='my-subscription')\n                >> PubSubSubscriptionCreateOperator(\n                    topic_project='my-project', topic='my-topic',\n                    subscription='my-subscription')\n            )\n\n    The operator can be configured to fail if the subscription already exists.\n    ::\n\n        with DAG('failing DAG') as dag:\n            (\n                dag\n                >> PubSubSubscriptionCreateOperator(\n                    topic_project='my-project', topic='my-topic',\n                    subscription='my-subscription')\n                >> PubSubSubscriptionCreateOperator(\n                    topic_project='my-project', topic='my-topic',\n                    subscription='my-subscription', fail_if_exists=True)\n            )\n\n    Finally, subscription is not required. If not passed, the operator will\n    generated a universally unique identifier for the subscription's name. ::\n\n        with DAG('DAG') as dag:\n            (\n                dag >> PubSubSubscriptionCreateOperator(\n                    topic_project='my-project', topic='my-topic')\n            )\n\n    ``topic_project``, ``topic``, ``subscription``, and\n    ``subscription`` are templated so you can use variables in them.\n    "
    template_fields = ['topic_project', 'topic', 'subscription',
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
    __doc__ = "Delete a PubSub topic.\n\n    By default, if the topic does not exist, this operator will\n    not cause the DAG to fail. ::\n\n        with DAG('successful DAG') as dag:\n            (\n                dag\n                >> PubSubTopicDeleteOperator(project='my-project',\n                                             topic='non_existing_topic')\n            )\n\n    The operator can be configured to fail if the topic does not exist. ::\n\n        with DAG('failing DAG') as dag:\n            (\n                dag\n                >> PubSubTopicCreateOperator(project='my-project',\n                                             topic='non_existing_topic',\n                                             fail_if_not_exists=True)\n            )\n\n    Both ``project`` and ``topic`` are templated so you can use\n    variables in them.\n    "
    template_fields = ['project', 'topic']
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
    __doc__ = "Delete a PubSub subscription.\n\n    By default, if the subscription does not exist, this operator will\n    not cause the DAG to fail. ::\n\n        with DAG('successful DAG') as dag:\n            (\n                dag\n                >> PubSubSubscriptionDeleteOperator(project='my-project',\n                                                    subscription='non-existing')\n            )\n\n    The operator can be configured to fail if the subscription already exists.\n\n    ::\n\n        with DAG('failing DAG') as dag:\n            (\n                dag\n                >> PubSubSubscriptionDeleteOperator(\n                     project='my-project', subscription='non-existing',\n                     fail_if_not_exists=True)\n            )\n\n    ``project``, and ``subscription`` are templated so you can use\n    variables in them.\n    "
    template_fields = ['project', 'subscription']
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
    __doc__ = "Publish messages to a PubSub topic.\n\n    Each Task publishes all provided messages to the same topic\n    in a single GCP project. If the topic does not exist, this\n    task will fail. ::\n\n        from base64 import b64encode as b64e\n\n        m1 = {'data': b64e('Hello, World!'),\n              'attributes': {'type': 'greeting'}\n             }\n        m2 = {'data': b64e('Knock, knock')}\n        m3 = {'attributes': {'foo': ''}}\n\n        t1 = PubSubPublishOperator(\n            project='my-project',topic='my_topic',\n            messages=[m1, m2, m3],\n            create_topic=True,\n            dag=dag)\n\n    ``project`` , ``topic``, and ``messages`` are templated so you can use\n    variables in them.\n    "
    template_fields = ['project', 'topic', 'messages']
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