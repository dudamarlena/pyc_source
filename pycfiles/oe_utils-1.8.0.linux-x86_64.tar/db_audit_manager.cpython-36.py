# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/data/db_audit_manager.py
# Compiled at: 2020-02-12 07:50:31
# Size of source mod 2**32: 637 bytes
import logging
from oe_utils.data.data_managers import AuditManager
log = logging.getLogger(__name__)

def audit_manager(request):
    """
    Initialize and return the audit manager.

    The request must contain a method `request.db` to retrieve the current session.

    :param request: `pyramid.request.Request`
    :return: the audit manager
    """
    session = request.db
    return AuditManager(session)


def includeme(config):
    """
    Configure a `request.audit_managers` method to retrieve the audit manager.

    :param config:
    """
    config.add_request_method(audit_manager, reify=True)