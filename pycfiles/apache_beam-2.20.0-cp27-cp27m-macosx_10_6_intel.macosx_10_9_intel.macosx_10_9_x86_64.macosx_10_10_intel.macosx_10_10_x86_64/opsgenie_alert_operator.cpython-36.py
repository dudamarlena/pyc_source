# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/opsgenie_alert_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4958 bytes
from airflow.contrib.hooks.opsgenie_alert_hook import OpsgenieAlertHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class OpsgenieAlertOperator(BaseOperator):
    """OpsgenieAlertOperator"""
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