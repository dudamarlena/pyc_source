# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/pubsub_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4319 bytes
from airflow.contrib.hooks.gcp_pubsub_hook import PubSubHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class PubSubPullSensor(BaseSensorOperator):
    __doc__ = "Pulls messages from a PubSub subscription and passes them through XCom.\n\n    This sensor operator will pull up to ``max_messages`` messages from the\n    specified PubSub subscription. When the subscription returns messages,\n    the poke method's criteria will be fulfilled and the messages will be\n    returned from the operator and passed through XCom for downstream tasks.\n\n    If ``ack_messages`` is set to True, messages will be immediately\n    acknowledged before being returned, otherwise, downstream tasks will be\n    responsible for acknowledging them.\n\n    ``project`` and ``subscription`` are templated so you can use\n    variables in them.\n    "
    template_fields = ['project', 'subscription']
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