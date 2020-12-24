# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/templatetags/rbadmintags.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django import template
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.context import RequestContext
from djblets.siteconfig.models import SiteConfiguration
from reviewboard import get_version_string
from reviewboard.admin.cache_stats import get_has_cache_stats
from reviewboard.hostingsvcs.models import HostingServiceAccount
from reviewboard.notifications.models import WebHookTarget
from reviewboard.oauth.models import Application
from reviewboard.reviews.models import DefaultReviewer, Group
from reviewboard.scmtools.models import Repository
from reviewboard.site.urlresolvers import local_site_reverse
register = template.Library()

@register.inclusion_tag(b'admin/subnav_item.html', takes_context=True)
def admin_subnav(context, url_name, name, icon=b''):
    """Return an <li> containing a link to the desired setting tab."""
    request = context.get(b'request')
    url = local_site_reverse(url_name, request=request)
    return RequestContext(request, {b'url': url, 
       b'name': name, 
       b'current': url == request.path, 
       b'icon': icon})


@register.simple_tag(takes_context=True)
def admin_widget(context, widget):
    """Render a widget with the given information.

    The widget will be created and returned as HTML. Any states in the
    database will be loaded into the rendered widget.
    """
    request = context.get(b'request')
    siteconfig = SiteConfiguration.objects.get(site=Site.objects.get_current())
    widget_states = siteconfig.get(b'widget_settings')
    if widget_states:
        widget.collapsed = widget_states.get(widget.name, b'0') != b'0'
    else:
        widget.collapsed = False
    return widget.render(request)


@register.inclusion_tag(b'admin/widgets/w-actions.html', takes_context=True)
def admin_actions(context):
    """Render the admin sidebar.

    This includes the configuration links and setting indicators.
    """
    request = context.get(b'request')
    request_context = {b'count_users': User.objects.count(), 
       b'count_review_groups': Group.objects.count(), 
       b'count_default_reviewers': DefaultReviewer.objects.count(), 
       b'count_oauth_applications': Application.objects.count(), 
       b'count_repository': Repository.objects.accessible(request.user, visible_only=False).count(), 
       b'count_webhooks': WebHookTarget.objects.count(), 
       b'count_hosting_accounts': HostingServiceAccount.objects.count(), 
       b'has_cache_stats': get_has_cache_stats(), 
       b'version': get_version_string()}
    return RequestContext(request, request_context)