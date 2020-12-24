# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/profile/task.py
# Compiled at: 2013-06-04 03:20:20
from datetime import datetime
from zope.dublincore.interfaces import IZopeDublinCore
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.principalannotation.interfaces import IPrincipalAnnotationUtility
from ztfy.sendit.app.interfaces import ISenditApplication
from ztfy.sendit.profile.interfaces import IProfilesCleanerTask
from zope.component import queryUtility, getUtility
from zope.interface import implements
from zope.security.proxy import removeSecurityProxy
from ztfy.scheduler.task import BaseTask
from ztfy.sendit.profile import SENDIT_USER_PROFILE
from ztfy.utils.timezone import tztime
from ztfy.utils.traversing import getParent

class ProfilesCleanerTask(BaseTask):
    """Profiles cleaning task
    
    This task is automatically deleting non-activated profiles
    """
    implements(IProfilesCleanerTask)

    def run(self, report):
        count = 0
        principal_annotations = queryUtility(IPrincipalAnnotationUtility)
        if principal_annotations is None:
            raise Exception('No principal annotations utility found')
        principal_annotations = removeSecurityProxy(principal_annotations)
        app = getParent(self, ISenditApplication)
        auth_plugin = getUtility(IAuthenticatorPlugin, app.external_auth_plugin)
        prefix_length = len(auth_plugin.prefix)
        for principal_id, annotations in principal_annotations.annotations.items():
            if auth_plugin.principalInfo(principal_id) is None:
                continue
            profile = annotations.get(SENDIT_USER_PROFILE)
            if profile is not None and not profile.activated:
                created = IZopeDublinCore(profile).created
                if (tztime(datetime.utcnow()) - tztime(created)).days > app.confirmation_delay:
                    report.write(' - deleting profile %s (created on %s)\n' % (annotations.__name__,
                     tztime(created).strftime('%Y-%m-%d')))
                    del annotations[SENDIT_USER_PROFILE]
                    if not annotations.data:
                        del principal_annotations.annotations[principal_id]
                    del auth_plugin[principal_id[prefix_length:]]
                    count += 1

        if count > 0:
            report.write('--------------------\n')
            report.write('%d profile(s) deleted' % count)
        return