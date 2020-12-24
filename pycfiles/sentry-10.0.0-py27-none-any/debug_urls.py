# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/debug_urls.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
import sentry.web.frontend.debug.mail
from sentry.web.frontend.debug.debug_assigned_email import DebugAssignedEmailView, DebugSelfAssignedEmailView, DebugSelfAssignedTeamEmailView
from sentry.web.frontend.debug.debug_trigger_error import DebugTriggerErrorView
from sentry.web.frontend.debug.debug_error_embed import DebugErrorPageEmbedView
from sentry.web.frontend.debug.debug_incident_activity_email import DebugIncidentActivityEmailView
from sentry.web.frontend.debug.debug_invalid_identity_email import DebugInvalidIdentityEmailView
from sentry.web.frontend.debug.debug_mfa_added_email import DebugMfaAddedEmailView
from sentry.web.frontend.debug.debug_mfa_removed_email import DebugMfaRemovedEmailView
from sentry.web.frontend.debug.debug_new_release_email import DebugNewReleaseEmailView
from sentry.web.frontend.debug.debug_new_user_feedback_email import DebugNewUserFeedbackEmailView
from sentry.web.frontend.debug.debug_note_email import DebugNoteEmailView
from sentry.web.frontend.debug.debug_password_changed_email import DebugPasswordChangedEmailView
from sentry.web.frontend.debug.debug_recovery_codes_regenerated_email import DebugRecoveryCodesRegeneratedEmailView
from sentry.web.frontend.debug.debug_regression_email import DebugRegressionEmailView, DebugRegressionReleaseEmailView
from sentry.web.frontend.debug.debug_resolved_email import DebugResolvedEmailView
from sentry.web.frontend.debug.debug_resolved_in_release_email import DebugResolvedInReleaseEmailView, DebugResolvedInReleaseUpcomingEmailView
from sentry.web.frontend.debug.debug_unable_to_delete_repository import DebugUnableToDeleteRepository
from sentry.web.frontend.debug.debug_unable_to_fetch_commits_email import DebugUnableToFetchCommitsEmailView
from sentry.web.frontend.debug.debug_unassigned_email import DebugUnassignedEmailView
from sentry.web.frontend.debug.debug_new_processing_issues_email import DebugNewProcessingIssuesEmailView, DebugNewProcessingIssuesNoReprocessingEmailView
from sentry.web.frontend.debug.debug_sso_link_email import DebugSsoLinkedEmailView, DebugSsoUnlinkedEmailView, DebugSsoUnlinkedNoPasswordEmailView
from sentry.web.frontend.debug.debug_setup_2fa_email import DebugSetup2faEmailView
from sentry.web.frontend.debug import debug_auth_views
from sentry.web.frontend.debug.debug_oauth_authorize import DebugOAuthAuthorizeView, DebugOAuthAuthorizeErrorView
urlpatterns = patterns('', url('^debug/mail/alert/$', sentry.web.frontend.debug.mail.alert), url('^debug/mail/note/$', DebugNoteEmailView.as_view()), url('^debug/mail/new-release/$', DebugNewReleaseEmailView.as_view()), url('^debug/mail/new-user-feedback/$', DebugNewUserFeedbackEmailView.as_view()), url('^debug/mail/assigned/$', DebugAssignedEmailView.as_view()), url('^debug/mail/assigned/self/$', DebugSelfAssignedEmailView.as_view()), url('^debug/mail/assigned/team/$', DebugSelfAssignedTeamEmailView.as_view()), url('^debug/mail/digest/$', sentry.web.frontend.debug.mail.digest), url('^debug/mail/report/$', sentry.web.frontend.debug.mail.report), url('^debug/mail/regression/$', DebugRegressionEmailView.as_view()), url('^debug/mail/regression/release/$', DebugRegressionReleaseEmailView.as_view()), url('^debug/mail/resolved/$', DebugResolvedEmailView.as_view()), url('^debug/mail/resolved-in-release/$', DebugResolvedInReleaseEmailView.as_view()), url('^debug/mail/resolved-in-release/upcoming/$', DebugResolvedInReleaseUpcomingEmailView.as_view()), url('^debug/mail/request-access/$', sentry.web.frontend.debug.mail.request_access), url('^debug/mail/access-approved/$', sentry.web.frontend.debug.mail.access_approved), url('^debug/mail/invitation/$', sentry.web.frontend.debug.mail.invitation), url('^debug/mail/invalid-identity/$', DebugInvalidIdentityEmailView.as_view()), url('^debug/mail/confirm-email/$', sentry.web.frontend.debug.mail.confirm_email), url('^debug/mail/recover-account/$', sentry.web.frontend.debug.mail.recover_account), url('^debug/mail/unable-to-delete-repo/$', DebugUnableToDeleteRepository.as_view()), url('^debug/mail/unable-to-fetch-commits/$', DebugUnableToFetchCommitsEmailView.as_view()), url('^debug/mail/unassigned/$', DebugUnassignedEmailView.as_view()), url('^debug/mail/org-delete-confirm/$', sentry.web.frontend.debug.mail.org_delete_confirm), url('^debug/mail/mfa-removed/$', DebugMfaRemovedEmailView.as_view()), url('^debug/mail/mfa-added/$', DebugMfaAddedEmailView.as_view()), url('^debug/mail/recovery-codes-regenerated/$', DebugRecoveryCodesRegeneratedEmailView.as_view()), url('^debug/mail/password-changed/$', DebugPasswordChangedEmailView.as_view()), url('^debug/mail/new-processing-issues/$', DebugNewProcessingIssuesEmailView.as_view()), url('^debug/mail/new-processing-issues-no-reprocessing/$', DebugNewProcessingIssuesNoReprocessingEmailView.as_view()), url('^debug/mail/sso-linked/$', DebugSsoLinkedEmailView.as_view()), url('^debug/mail/sso-unlinked/$', DebugSsoUnlinkedEmailView.as_view()), url('^debug/mail/sso-unlinked/no-password$', DebugSsoUnlinkedNoPasswordEmailView.as_view()), url('^debug/mail/incident-activity$', DebugIncidentActivityEmailView.as_view()), url('^debug/mail/setup-2fa/$', DebugSetup2faEmailView.as_view()), url('^debug/embed/error-page/$', DebugErrorPageEmbedView.as_view()), url('^debug/trigger-error/$', DebugTriggerErrorView.as_view()), url('^debug/auth-confirm-identity/$', debug_auth_views.DebugAuthConfirmIdentity.as_view()), url('^debug/auth-confirm-link/$', debug_auth_views.DebugAuthConfirmLink.as_view()), url('^debug/sudo/$', TemplateView.as_view(template_name='sentry/account/sudo.html')), url('^debug/oauth/authorize/$', DebugOAuthAuthorizeView.as_view()), url('^debug/oauth/authorize/error/$', DebugOAuthAuthorizeErrorView.as_view()))