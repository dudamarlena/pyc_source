# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/agent/storagepoolusage.py
# Compiled at: 2016-06-13 14:11:03
"""
Storage pool usage operations.
"""
from vsm import context
from vsm import db
from vsm import utils
from vsm import exception
from vsm.openstack.common import timeutils
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import log as logging
from vsm.openstack.common.db import exception as db_exc
LOG = logging.getLogger(__name__)

def get_all(contxt):
    """get all non-deleted storage pool usage as a dict"""
    if contxt is None:
        contxt = context.get_admin_context()
    try:
        uses = db.get_storage_pool_usage(contxt)
        return uses
    except db_exc.DBError as e:
        LOG.exception(_('DB Error on getting Storage Pool Usage %s' % e))
        raise exception.StoragePoolUsageFailure()

    return


def create(contxt, pool_list):
    """create storage pool usages"""
    return db.storage_pool_usage_create(contxt, pool_list)


def update(contxt, vsmapp_id, attach_status=None, is_terminate=False):
    """update storage pool usage"""
    if contxt is None:
        contxt = context.get_admin_context()
    if not vsmapp_id:
        raise exception.StoragePoolUsageInvalid()
    is_terminate = utils.bool_from_str(is_terminate)
    kargs = {'attach_status': attach_status, 
       'terminate_at': timeutils.utcnow() if is_terminate else None}
    try:
        return db.storage_pool_usage_update(contxt, vsmapp_id, kargs)
    except db_exc.DBError as e:
        LOG.exception(_('DB Error on updating new storage pool usage %s' % e))
        raise exception.StoragePoolUsageFailure()

    return


def destroy(contxt, id):
    if contxt is None:
        contxt = context.get_admin_context()
    id = utils.int_from_str(id)
    try:
        db.destroy_storage_pool_usage(contxt, id)
    except db_exc.DBError as e:
        LOG.exception(_('DB Error on deleting Pool Usages %s' % e))
        raise exception.StoragePoolUsageFailure()

    return