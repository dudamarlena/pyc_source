# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/pubsub_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4319 bytes
from airflow.contrib.hooks.gcp_pubsub_hook import PubSubHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class PubSubPullSensor(BaseSensorOperator):
    """PubSubPullSensor"""
    template_fields = [
     'project', 'subscription']
    ui_color = '#ff7f50'

    @apply_defaults
    def __init__(self, project, subscription, max_messages=5, return_immediately=False, ack_messages=False, gcp_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        """
        :param project: the GCP project ID for the subscription (templated)
        :type project: str
        :param subscription: the Pub/Sub subscription name. Do not include the
            full subscription path.
        :type subscription: str
        :param max_messages: The maximum number of messages to retrieve per
            PubSub pull request
        :type max_messages: int
        :param return_immediately: If True, instruct the PubSub API to return
            immediately if no messages are available for delivery.
        :type return_immediately: bool
        :param ack_messages: If True, each message will be acknowledged
            immediately rather than by any downstream tasks
        :type ack_messages: bool
        :param gcp_conn_id: The connection ID to use connecting to
            Google Cloud Platform.
        :type gcp_conn_id: str
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request
            must have domain-wide delegation enabled.
        :type delegate_to: str
        """
        (super(PubSubPullSensor, self).__init__)(*args, **kwargs)
        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.project = project
        self.subscription = subscription
        self.max_messages = max_messages
        self.return_immediately = return_immediately
        self.ack_messages = ack_messages
        self._messages = None

    def execute(self, context):
        super(PubSubPullSensor, self).execute(context)
        return self._messages

    def poke(self, context):
        hook = PubSubHook(gcp_conn_id=(self.gcp_conn_id), delegate_to=(self.delegate_to))
        self._messages = hook.pull(self.project, self.subscription, self.max_messages, self.return_immediately)
        if self._messages:
            if self.ack_messages:
                if self.ack_messages:
                    ack_ids = [m['ackId'] for m in self._messages if m.get('ackId')]
                    hook.acknowledge(self.project, self.subscription, ack_ids)
        return self._messages