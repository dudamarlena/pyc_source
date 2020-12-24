# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/opsgenie_alert_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4958 bytes
from airflow.contrib.hooks.opsgenie_alert_hook import OpsgenieAlertHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class OpsgenieAlertOperator(BaseOperator):
    __doc__ = "\n    This operator allows you to post alerts to Opsgenie.\n    Accepts a connection that has an Opsgenie API key as the connection's password.\n    This operator sets the domain to conn_id.host, and if not set will default\n    to ``https://api.opsgenie.com``.\n\n    Each Opsgenie API key can be pre-configured to a team integration.\n    You can override these defaults in this operator.\n\n    :param opsgenie_conn_id: The name of the Opsgenie connection to use\n    :type opsgenie_conn_id: str\n    :param message: The Message of the Opsgenie alert (templated)\n    :type message: str\n    :param alias: Client-defined identifier of the alert (templated)\n    :type alias: str\n    :param description: Description field of the alert (templated)\n    :type description: str\n    :param responders: Teams, users, escalations and schedules that\n        the alert will be routed to send notifications.\n    :type responders: list[dict]\n    :param visibleTo: Teams and users that the alert will become visible\n        to without sending any notification.\n    :type visibleTo: list[dict]\n    :param actions: Custom actions that will be available for the alert.\n    :type actions: list[str]\n    :param tags: Tags of the alert.\n    :type tags: list[str]\n    :param details: Map of key-value pairs to use as custom properties of the alert.\n    :type details: dict\n    :param entity: Entity field of the alert that is\n        generally used to specify which domain alert is related to. (templated)\n    :type entity: str\n    :param source: Source field of the alert. Default value is\n        IP address of the incoming request.\n    :type source: str\n    :param priority: Priority level of the alert. Default value is P3. (templated)\n    :type priority: str\n    :param user: Display name of the request owner.\n    :type user: str\n    :param note: Additional note that will be added while creating the alert. (templated)\n    :type note: str\n    "
    template_fields = ('message', 'alias', 'description', 'entity', 'priority', 'note')

    @apply_defaults
    def __init__(self, message, opsgenie_conn_id='opsgenie_default', alias=None, description=None, responders=None, visibleTo=None, actions=None, tags=None, details=None, entity=None, source=None, priority=None, user=None, note=None, *args, **kwargs):
        (super(OpsgenieAlertOperator, self).__init__)(*args, **kwargs)
        self.message = message
        self.opsgenie_conn_id = opsgenie_conn_id
        self.alias = alias
        self.description = description
        self.responders = responders
        self.visibleTo = visibleTo
        self.actions = actions
        self.tags = tags
        self.details = details
        self.entity = entity
        self.source = source
        self.priority = priority
        self.user = user
        self.note = note
        self.hook = None

    def _build_opsgenie_payload(self):
        """
        Construct the Opsgenie JSON payload. All relevant parameters are combined here
        to a valid Opsgenie JSON payload.

        :return: Opsgenie payload (dict) to send
        """
        payload = {}
        for key in ('message', 'alias', 'description', 'responders', 'visibleTo', 'actions',
                    'tags', 'details', 'entity', 'source', 'priority', 'user', 'note'):
            val = getattr(self, key)
            if val:
                payload[key] = val

        return payload

    def execute(self, context):
        """
        Call the OpsgenieAlertHook to post message
        """
        self.hook = OpsgenieAlertHook(self.opsgenie_conn_id)
        self.hook.execute(self._build_opsgenie_payload())