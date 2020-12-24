# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/restore_organization.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import logging, six
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from sentry.api import client
from sentry.models import AuditLogEntryEvent, Organization, OrganizationStatus
from sentry.web.frontend.base import OrganizationView
from sentry.web.helpers import render_to_response
ERR_MESSAGES = {OrganizationStatus.VISIBLE: _('Deletion already canceled.'), 
   OrganizationStatus.DELETION_IN_PROGRESS: _('Deletion cannot be canceled, already in progress')}
MSG_RESTORE_SUCCESS = _('Organization restored successfully.')
delete_logger = logging.getLogger('sentry.deletions.ui')

class RestoreOrganizationView(OrganizationView):
    required_scope = 'org:admin'
    sudo_required = True

    def get_active_organization(self, request, organization_slug):
        organizations = Organization.objects.get_for_user(user=request.user, only_visible=False)
        try:
            return six.next(o for o in organizations if o.slug == organization_slug)
        except StopIteration:
            return

        return

    def get(self, request, organization):
        if organization.status == OrganizationStatus.VISIBLE:
            return self.redirect(organization.get_url())
        context = {'deleting_organization': organization, 
           'pending_deletion': organization.status == OrganizationStatus.PENDING_DELETION}
        return render_to_response('sentry/restore-organization.html', context, self.request)

    def post(self, request, organization):
        deletion_statuses = [
         OrganizationStatus.PENDING_DELETION,
         OrganizationStatus.DELETION_IN_PROGRESS]
        if organization.status not in deletion_statuses:
            messages.add_message(request, messages.ERROR, ERR_MESSAGES[organization.status])
            return self.redirect(reverse('sentry'))
        updated = Organization.objects.filter(id=organization.id, status__in=deletion_statuses).update(status=OrganizationStatus.VISIBLE)
        if updated:
            client.put(('/organizations/{}/').format(organization.slug), data={'cancelDeletion': True}, request=request)
            messages.add_message(request, messages.SUCCESS, MSG_RESTORE_SUCCESS)
            if organization.status == OrganizationStatus.PENDING_DELETION:
                self.create_audit_entry(request=request, organization=organization, target_object=organization.id, event=AuditLogEntryEvent.ORG_RESTORE, data=organization.get_audit_log_data())
        return self.redirect(organization.get_url())