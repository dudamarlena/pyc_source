# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/log.py
# Compiled at: 2016-12-16 07:39:01
from nodeconductor.logging.loggers import EventLogger, event_logger
from nodeconductor_paas_oracle.models import Deployment

class OracleDeploymentEventLogger(EventLogger):
    deployment = Deployment
    jira_issue_key = basestring

    class Meta:
        nullable_fields = [
         'jira_issue_key']
        event_types = ('oracle_deployment_resize_requested', 'oracle_deployment_resize_succeeded',
                       'oracle_deployment_start_requested', 'oracle_deployment_start_succeeded',
                       'oracle_deployment_restart_requested', 'oracle_deployment_restart_succeeded',
                       'oracle_deployment_stop_requested', 'oracle_deployment_stop_succeeded',
                       'oracle_deployment_support_requested', 'oracle_deployment_report_updated')


event_logger.register('oracle_deployment', OracleDeploymentEventLogger)