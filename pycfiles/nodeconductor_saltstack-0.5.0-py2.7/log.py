# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_saltstack/sharepoint/log.py
# Compiled at: 2016-09-28 02:05:53
from nodeconductor.logging.loggers import EventLogger, event_logger
from nodeconductor_saltstack.sharepoint.models import User, SiteCollection, SharepointTenant

class SharepointTenantEventLogger(EventLogger):
    tenant = SharepointTenant

    class Meta:
        event_types = ('sharepoint_tenant_quota_update', )


class SharepointUserEventLogger(EventLogger):
    affected_user = User

    class Meta:
        event_types = ('sharepoint_user_password_reset', )


class SharepointSiteCollectionEventLogger(EventLogger):
    site_collection = SiteCollection

    class Meta:
        event_types = ('sharepoint_site_collection_quota_update', )


event_logger.register('sharepoint_user', SharepointUserEventLogger)
event_logger.register('sharepoint_site_collection', SharepointSiteCollectionEventLogger)
event_logger.register('sharepoint_tenant', SharepointTenantEventLogger)