# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/janrain/middleware.py
# Compiled at: 2013-06-20 04:08:17
import re
from django.core.urlresolvers import reverse
from django.conf import settings
from preferences import preferences
from foundry.models import Member
from janrain.models import JanrainProfile
from janrain.models import STATUS_DIRTY, STATUS_SYNCED
PATHS = (
 reverse('complete-profile'), reverse('edit-profile'))

class JanrainMiddleware:

    def process_request(self, request):
        if request.META['PATH_INFO'] in PATHS:
            user = getattr(request, 'user', None)
            if user is not None and user.is_authenticated():
                janrain_profile = user.janrainprofile_set.all()[0]
                if request.META['REQUEST_METHOD'] == 'POST':
                    janrain_profile.status = STATUS_DIRTY
                    print 'status set to dirty'
                    janrain_profile.save()
                if request.META['REQUEST_METHOD'] == 'GET':
                    janrain_profile.status = STATUS_DIRTY
                    print 'Will sync now'
                    janrain_profile.status = STATUS_SYNCED
                    janrain_profile.save()
        return