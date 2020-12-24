# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/urls.py
# Compiled at: 2019-08-23 05:13:18
from __future__ import absolute_import
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.http import HttpResponse
from django.views.generic import RedirectView
from sentry.web import api
from sentry.web.frontend import accounts, generic
from sentry.web.frontend.auth_login import AuthLoginView
from sentry.web.frontend.twofactor import TwoFactorAuthView, u2f_appid
from sentry.web.frontend.auth_logout import AuthLogoutView
from sentry.web.frontend.auth_organization_login import AuthOrganizationLoginView
from sentry.web.frontend.auth_provider_login import AuthProviderLoginView
from sentry.web.frontend.auth_close import AuthCloseView
from sentry.web.frontend.error_page_embed import ErrorPageEmbedView
from sentry.web.frontend.group_event_json import GroupEventJsonView
from sentry.web.frontend.group_plugin_action import GroupPluginActionView
from sentry.web.frontend.group_tag_export import GroupTagExportView
from sentry.web.frontend.home import HomeView
from sentry.web.frontend.pipeline_advancer import PipelineAdvancerView
from sentry.web.frontend.mailgun_inbound_webhook import MailgunInboundWebhookView
from sentry.web.frontend.oauth_authorize import OAuthAuthorizeView
from sentry.web.frontend.oauth_token import OAuthTokenView
from sentry.auth.providers.saml2 import SAML2AcceptACSView, SAML2SLSView, SAML2MetadataView
from sentry.web.frontend.organization_avatar import OrganizationAvatarPhotoView
from sentry.web.frontend.organization_auth_settings import OrganizationAuthSettingsView
from sentry.web.frontend.organization_integration_setup import OrganizationIntegrationSetupView
from sentry.web.frontend.out import OutView
from sentry.web.frontend.project_avatar import ProjectAvatarPhotoView
from sentry.web.frontend.react_page import GenericReactPageView, ReactPageView
from sentry.web.frontend.reactivate_account import ReactivateAccountView
from sentry.web.frontend.release_webhook import ReleaseWebhookView
from sentry.web.frontend.restore_organization import RestoreOrganizationView
from sentry.web.frontend.team_avatar import TeamAvatarPhotoView
from sentry.web.frontend.account_identity import AccountIdentityAssociateView
from sentry.web.frontend.sudo import SudoView
from sentry.web.frontend.unsubscribe_issue_notifications import UnsubscribeIssueNotificationsView
from sentry.web.frontend.unsubscribe_incident_notifications import UnsubscribeIncidentNotificationsView
from sentry.web.frontend.user_avatar import UserAvatarPhotoView
from sentry.web.frontend.setup_wizard import SetupWizardView
from sentry.web.frontend.vsts_extension_configuration import VstsExtensionConfigurationView
from sentry.web.frontend.js_sdk_loader import JavaScriptSdkLoader
from sentry.web.frontend.project_event import ProjectEventRedirect
__all__ = ('urlpatterns', )

def init_all_applications():
    """
    Forces import of all applications to ensure code is registered.
    """
    from django.db.models import get_apps, get_models
    for app in get_apps():
        try:
            get_models(app)
        except Exception:
            continue


init_all_applications()
generic_react_page_view = GenericReactPageView.as_view()
react_page_view = ReactPageView.as_view()
urlpatterns = patterns('')
if getattr(settings, 'DEBUG_VIEWS', settings.DEBUG):
    from sentry.web.debug_urls import urlpatterns as debug_urls
    urlpatterns += debug_urls
if settings.DEBUG:
    urlpatterns += patterns('', url('^_static/[^/]+/[^/]+/images/favicon\\.ico$', generic.dev_favicon, name='sentry-dev-favicon'))
urlpatterns += patterns('', url('^api/store/$', api.StoreView.as_view(), name='sentry-api-store'), url('^api/(?P<project_id>[\\w_-]+)/store/$', api.StoreView.as_view(), name='sentry-api-store'), url('^api/(?P<project_id>[\\w_-]+)/minidump/?$', api.MinidumpView.as_view(), name='sentry-api-minidump'), url('^api/(?P<project_id>[\\w_-]+)/events/(?P<event_id>[\\w-]+)/attachments/$', api.EventAttachmentStoreView.as_view(), name='sentry-api-event-attachment'), url('^api/(?P<project_id>[\\w_-]+)/unreal/(?P<sentry_key>\\w+)/$', api.UnrealView.as_view(), name='sentry-api-unreal'), url('^api/(?P<project_id>\\d+)/security/$', api.SecurityReportView.as_view(), name='sentry-api-security-report'), url('^api/(?P<project_id>\\d+)/csp-report/$', api.SecurityReportView.as_view(), name='sentry-api-csp-report'), url('^api/(?P<project_id>[\\w_-]+)/crossdomain\\.xml$', api.crossdomain_xml, name='sentry-api-crossdomain-xml'), url('^api/store/schema$', api.StoreSchemaView.as_view(), name='sentry-api-store-schema'), url('^api/client-config/?$', api.ClientConfigView.as_view(), name='sentry-api-client-config'), url('^_static/(?:(?P<version>\\d{10}|[a-f0-9]{32,40})/)?(?P<module>[^/]+)/(?P<path>.*)$', generic.static_media, name='sentry-media'), url('^js-sdk-loader/(?P<public_key>[^/\\.]+)(?:(?P<minified>\\.min))?\\.js$', JavaScriptSdkLoader.as_view(), name='sentry-js-sdk-loader'), url('^api/0/', include('sentry.api.urls')), url('^api/hooks/mailgun/inbound/', MailgunInboundWebhookView.as_view(), name='sentry-mailgun-inbound-hook'), url('^api/hooks/release/(?P<plugin_id>[^/]+)/(?P<project_id>[^/]+)/(?P<signature>[^/]+)/', ReleaseWebhookView.as_view(), name='sentry-release-hook'), url('^api/embed/error-page/$', ErrorPageEmbedView.as_view(), name='sentry-error-page-embed'), url('^oauth/', include([
 url('^authorize/$', OAuthAuthorizeView.as_view()),
 url('^token/$', OAuthTokenView.as_view())])), url('^saml/', include([
 url('^acs/(?P<organization_slug>[^/]+)/$', SAML2AcceptACSView.as_view(), name='sentry-auth-organization-saml-acs'),
 url('^sls/(?P<organization_slug>[^/]+)/$', SAML2SLSView.as_view(), name='sentry-auth-organization-saml-sls'),
 url('^metadata/(?P<organization_slug>[^/]+)/$', SAML2MetadataView.as_view(), name='sentry-auth-organization-saml-metadata')])), url('^auth/', include([
 url('^login/$', AuthLoginView.as_view(), name='sentry-login'),
 url('^login/(?P<organization_slug>[^/]+)/$', AuthOrganizationLoginView.as_view(), name='sentry-auth-organization'),
 url('^link/(?P<organization_slug>[^/]+)/$', AuthOrganizationLoginView.as_view(), name='sentry-auth-link-identity'),
 url('^2fa/$', TwoFactorAuthView.as_view(), name='sentry-2fa-dialog'),
 url('^2fa/u2fappid\\.json$', u2f_appid, name='sentry-u2f-app-id'),
 url('^sso/$', AuthProviderLoginView.as_view(), name='sentry-auth-sso'),
 url('^logout/$', AuthLogoutView.as_view(), name='sentry-logout'),
 url('^reactivate/$', ReactivateAccountView.as_view(), name='sentry-reactivate-account'),
 url('^register/$', AuthLoginView.as_view(), name='sentry-register'),
 url('^close/$', AuthCloseView.as_view(), name='sentry-auth-close')])), url('^login-redirect/$', accounts.login_redirect, name='sentry-login-redirect'), url('^account/', include([
 url('^sudo/$', SudoView.as_view(), name='sentry-sudo'),
 url('^confirm-email/$', accounts.start_confirm_email, name='sentry-account-confirm-email-send'),
 url('^authorizations/$', RedirectView.as_view(pattern_name='sentry-account-settings-authorizations', permanent=False)),
 url('^confirm-email/(?P<user_id>[\\d]+)/(?P<hash>[0-9a-zA-Z]+)/$', accounts.confirm_email, name='sentry-account-confirm-email'),
 url('^recover/$', accounts.recover, name='sentry-account-recover'),
 url('^recover/confirm/(?P<user_id>[\\d]+)/(?P<hash>[0-9a-zA-Z]+)/$', accounts.recover_confirm, name='sentry-account-recover-confirm'),
 url('^password/confirm/(?P<user_id>[\\d]+)/(?P<hash>[0-9a-zA-Z]+)/$', accounts.set_password_confirm, name='sentry-account-set-password-confirm'),
 url('^settings/$', RedirectView.as_view(pattern_name='sentry-account-settings', permanent=False)),
 url('^settings/2fa/', RedirectView.as_view(pattern_name='sentry-account-settings-security', permanent=False)),
 url('^settings/avatar/$', RedirectView.as_view(pattern_name='sentry-account-settings-avatar', permanent=False)),
 url('^settings/appearance/$', RedirectView.as_view(pattern_name='sentry-account-settings-appearance', permanent=False)),
 url('^settings/identities/$', RedirectView.as_view(pattern_name='sentry-account-settings-identities', permanent=False)),
 url('^settings/subscriptions/$', RedirectView.as_view(pattern_name='sentry-account-settings-subscriptions', permanent=False)),
 url('^settings/identities/(?P<identity_id>[^\\/]+)/disconnect/$', accounts.disconnect_identity, name='sentry-account-disconnect-identity'),
 url('^settings/identities/associate/(?P<organization_slug>[^\\/]+)/(?P<provider_key>[^\\/]+)/(?P<external_id>[^\\/]+)/$', AccountIdentityAssociateView.as_view(), name='sentry-account-associate-identity'),
 url('^settings/security/', RedirectView.as_view(pattern_name='sentry-account-settings-security', permanent=False)),
 url('^settings/emails/$', RedirectView.as_view(pattern_name='sentry-account-settings-emails', permanent=False)),
 url('^settings/wizard/(?P<wizard_hash>[^\\/]+)/$', SetupWizardView.as_view(), name='sentry-project-wizard-fetch'),
 url('^settings/notifications/unsubscribe/(?P<project_id>\\d+)/$', accounts.email_unsubscribe_project),
 url('^settings/notifications/', RedirectView.as_view(pattern_name='sentry-account-settings-notifications', permanent=False)),
 url('^notifications/unsubscribe/(?P<project_id>\\d+)/$', accounts.email_unsubscribe_project, name='sentry-account-email-unsubscribe-project'),
 url('^notifications/unsubscribe/issue/(?P<issue_id>\\d+)/$', UnsubscribeIssueNotificationsView.as_view(), name='sentry-account-email-unsubscribe-issue'),
 url('^notifications/unsubscribe/incident/(?P<incident_id>\\d+)/$', UnsubscribeIncidentNotificationsView.as_view(), name='sentry-account-email-unsubscribe-incident'),
 url('^remove/$', RedirectView.as_view(pattern_name='sentry-remove-account', permanent=False)),
 url('^settings/social/', include('social_auth.urls')),
 url('^', generic_react_page_view)])), url('^onboarding/', generic_react_page_view), url('^manage/', react_page_view, name='sentry-admin-overview'), url('^docs/?$', RedirectView.as_view(url='https://docs.sentry.io/hosted/', permanent=False), name='sentry-docs-redirect'), url('^docs/api/?$', RedirectView.as_view(url='https://docs.sentry.io/hosted/api/', permanent=False), name='sentry-api-docs-redirect'), url('^api/$', RedirectView.as_view(pattern_name='sentry-api', permanent=False)), url('^api/applications/$', RedirectView.as_view(pattern_name='sentry-api-applications', permanent=False)), url('^api/new-token/$', RedirectView.as_view(pattern_name='sentry-api-new-auth-token', permanent=False)), url('^api/[^0]+/', RedirectView.as_view(pattern_name='sentry-api', permanent=False)), url('^out/$', OutView.as_view()), url('^accept-transfer/$', react_page_view, name='sentry-accept-project-transfer'), url('^accept/(?P<member_id>\\d+)/(?P<token>\\w+)/$', GenericReactPageView.as_view(auth_required=False), name='sentry-accept-invite'), url('^settings/', include([
 url('^account/$', generic_react_page_view, name='sentry-account-settings'),
 url('^account/$', generic_react_page_view, name='sentry-account-settings-appearance'),
 url('^account/authorizations/$', generic_react_page_view, name='sentry-account-settings-authorizations'),
 url('^account/security/', generic_react_page_view, name='sentry-account-settings-security'),
 url('^account/avatar/$', generic_react_page_view, name='sentry-account-settings-avatar'),
 url('^account/identities/$', generic_react_page_view, name='sentry-account-settings-identities'),
 url('^account/subscriptions/$', generic_react_page_view, name='sentry-account-settings-subscriptions'),
 url('^account/notifications/', generic_react_page_view, name='sentry-account-settings-notifications'),
 url('^account/emails/$', generic_react_page_view, name='sentry-account-settings-emails'),
 url('^account/api/applications/$', generic_react_page_view, name='sentry-api-applications'),
 url('^account/api/auth-tokens/new-token/$', generic_react_page_view, name='sentry-api-new-auth-token'),
 url('^account/api/', generic_react_page_view, name='sentry-api'),
 url('^account/close-account/$', generic_react_page_view, name='sentry-remove-account'),
 url('^account/', generic_react_page_view),
 url('^(?P<organization_slug>[\\w_-]+)/members/$', react_page_view, name='sentry-organization-members'),
 url('^(?P<organization_slug>[\\w_-]+)/members/new/$', react_page_view, name='sentry-create-organization-member'),
 url('^(?P<organization_slug>[\\w_-]+)/members/(?P<member_id>\\d+)/$', react_page_view, name='sentry-organization-member-settings'),
 url('^', react_page_view)])), url('^extensions/external-install/(?P<provider_id>\\w+)/(?P<installation_id>\\w+)/$', react_page_view, name='integration-installation'), url('^(?P<organization_slug>[\\w_-]+)/$', react_page_view, name='sentry-organization-home'), url('^organizations/', include([
 url('^new/$', generic_react_page_view),
 url('^(?P<organization_slug>[\\w_-]+)/$', react_page_view, name='sentry-organization-index'),
 url('^(?P<organization_slug>[\\w_-]+)/issues/$', react_page_view, name='sentry-organization-issue-list'),
 url('^(?P<organization_slug>[\\w_-]+)/issues/(?P<group_id>\\d+)/$', react_page_view, name='sentry-organization-issue'),
 url('^(?P<organization_slug>[\\w_-]+)/issues/(?P<issue_id>\\d+)/$', react_page_view, name='sentry-organization-issue-detail'),
 url('^(?P<organization_slug>[\\w_-]+)/issues/(?P<group_id>\\d+)/events/(?P<event_id_or_latest>[\\w-]+)/$', react_page_view, name='sentry-organization-event-detail'),
 url('^(?P<organization_slug>[\\w_-]+)/issues/(?P<group_id>\\d+)/events/(?P<event_id_or_latest>[\\w-]+)/json/$', GroupEventJsonView.as_view(), name='sentry-group-event-json'),
 url('^(?P<organization_slug>[\\w_-]+)/projects/(?P<project_slug>[\\w_-]+)/events/(?P<client_event_id>[\\w_-]+)/$', ProjectEventRedirect.as_view(), name='sentry-project-event-redirect'),
 url('^(?P<organization_slug>[\\w_-]+)/api-keys/$', react_page_view, name='sentry-organization-api-keys'),
 url('^(?P<organization_slug>[\\w_-]+)/api-keys/(?P<key_id>[\\w_-]+)/$', react_page_view, name='sentry-organization-api-key-settings'),
 url('^(?P<organization_slug>[\\w_-]+)/auth/$', react_page_view, name='sentry-organization-auth-settings'),
 url('^(?P<organization_slug>[\\w_-]+)/auth/configure/$', OrganizationAuthSettingsView.as_view(), name='sentry-organization-auth-provider-settings'),
 url('^(?P<organization_slug>[\\w_-]+)/integrations/(?P<provider_id>[\\w_-]+)/setup/$', OrganizationIntegrationSetupView.as_view(), name='sentry-organization-integrations-setup'),
 url('^(?P<organization_slug>[\\w_-]+)/members/$', RedirectView.as_view(pattern_name='sentry-organization-members', permanent=False), name='sentry-organization-members-old'),
 url('^(?P<organization_slug>[\\w_-]+)/members/new/$', RedirectView.as_view(pattern_name='sentry-create-organization-member', permanent=False), name='sentry-create-organization-member-old'),
 url('^(?P<organization_slug>[\\w_-]+)/members/(?P<member_id>\\d+)/$', RedirectView.as_view(pattern_name='sentry-organization-member-settings', permanent=False), name='sentry-organization-member-settings-old'),
 url('^(?P<organization_slug>[\\w_-]+)/stats/$', react_page_view, name='sentry-organization-stats'),
 url('^(?P<organization_slug>[\\w_-]+)/restore/$', RestoreOrganizationView.as_view(), name='sentry-restore-organization'),
 url('^(?P<organization_slug>[\\w_-]+)/settings/', react_page_view)])), url('^(?P<organization_slug>[\\w_-]+)/(?P<project_slug>[\\w_-]+)/settings/$', RedirectView.as_view(pattern_name='sentry-manage-project', permanent=False)), url('^settings/(?P<organization_slug>[\\w_-]+)/projects/(?P<project_slug>[\\w_-]+)/$', react_page_view, name='sentry-manage-project'), url('^avatar/(?P<avatar_id>[^\\/]+)/$', UserAvatarPhotoView.as_view(), name='sentry-user-avatar-url'), url('^organization-avatar/(?P<avatar_id>[^\\/]+)/$', OrganizationAvatarPhotoView.as_view(), name='sentry-organization-avatar-url'), url('^project-avatar/(?P<avatar_id>[^\\/]+)/$', ProjectAvatarPhotoView.as_view(), name='sentry-project-avatar-url'), url('^team-avatar/(?P<avatar_id>[^\\/]+)/$', TeamAvatarPhotoView.as_view(), name='sentry-team-avatar-url'), url('^extensions/vsts/configure/$', VstsExtensionConfigurationView.as_view(), name='vsts-extension-configuration'), url('^$', HomeView.as_view(), name='sentry'), url('^robots\\.txt$', api.robots_txt, name='sentry-api-robots-txt'), url('favicon\\.ico$', lambda r: HttpResponse(status=404)), url('^crossdomain\\.xml$', lambda r: HttpResponse(status=404)), url('^extensions/', include([
 url('^(?P<provider_id>[\\w_-]+)/setup/$', PipelineAdvancerView.as_view(), name='sentry-extension-setup'),
 url('^cloudflare/', include('sentry.integrations.cloudflare.urls')),
 url('^jira/', include('sentry.integrations.jira.urls')),
 url('^jira-server/', include('sentry.integrations.jira_server.urls')),
 url('^slack/', include('sentry.integrations.slack.urls')),
 url('^github/', include('sentry.integrations.github.urls')),
 url('^github-enterprise/', include('sentry.integrations.github_enterprise.urls')),
 url('^gitlab/', include('sentry.integrations.gitlab.urls')),
 url('^vsts/', include('sentry.integrations.vsts.urls')),
 url('^bitbucket/', include('sentry.integrations.bitbucket.urls'))])), url('^plugins/', include('sentry.plugins.base.urls')), url('^share/(?:group|issue)/(?P<share_id>[\\w_-]+)/$', GenericReactPageView.as_view(auth_required=False), name='sentry-group-shared'), url('^(?P<organization_slug>[\\w_-]+)/issues/(?P<short_id>[\\w_-]+)/$', react_page_view, name='sentry-short-id'), url('^(?P<organization_slug>[\\w_-]+)/(?P<project_id>[\\w_-]+)/issues/(?P<group_id>\\d+)/$', react_page_view, name='sentry-group'), url('^(?P<organization_slug>[\\w_-]+)/(?P<project_slug>[\\w_-]+)/issues/(?P<group_id>\\d+)/events/(?P<event_id>[\\w-]+)/$', react_page_view, name='sentry-group-event'), url('^(?P<organization_slug>[\\w_-]+)/(?P<project_id>[\\w_-]+)/$', react_page_view, name='sentry-stream'), url('^organizations/(?P<organization_slug>[\\w_-]+)/incidents/(?P<incident_id>\\d+)/$', react_page_view, name='sentry-incident'), url('^(?P<organization_slug>[\\w_-]+)/(?P<project_slug>[\\w_-]+)/issues/(?P<group_id>\\d+)/tags/(?P<key>[^\\/]+)/export/$', GroupTagExportView.as_view(), name='sentry-group-tag-export'), url('^(?P<organization_slug>[\\w_-]+)/(?P<project_slug>[\\w_-]+)/issues/(?P<group_id>\\d+)/actions/(?P<slug>[\\w_-]+)/', GroupPluginActionView.as_view(), name='sentry-group-plugin-action'), url('^(?P<organization_slug>[\\w_-]+)/(?P<project_slug>[\\w_-]+)/events/(?P<client_event_id>[\\w_-]+)/$', ProjectEventRedirect.as_view(), name='sentry-project-event-redirect'), url('/$', react_page_view))