# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_sugarcrm/log.py
# Compiled at: 2016-09-28 11:51:43
from nodeconductor.logging.loggers import EventLogger, event_logger
from .models import CRM

class SugarCRMUserEventLogger(EventLogger):
    user_name = basestring
    crm = CRM

    class Meta:
        event_types = ('sugarcrm_user_creation_succeeded', 'sugarcrm_user_update_succeeded',
                       'sugarcrm_user_deletion_succeeded', 'sugarcrm_user_activation_succeeded',
                       'sugarcrm_user_deactivation_succeeded', 'sugarcrm_user_password_reset')


event_logger.register('sugarcrm_user', SugarCRMUserEventLogger)