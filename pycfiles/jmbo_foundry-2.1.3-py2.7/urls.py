# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/urls.py
# Compiled at: 2015-11-26 05:42:33
from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from preferences import preferences
from jmbo.urls import v1_api
from foundry.models import Page
from foundry import views, forms
from foundry.api import ListingResource, LinkResource, NavbarResource, MenuResource, PageResource, BlogPostResource
admin.autodiscover()
try:
    import object_tools
    object_tools.autodiscover()
except ImportError:
    pass

v1_api.register(ListingResource())
v1_api.register(LinkResource())
v1_api.register(NavbarResource())
v1_api.register(MenuResource())
v1_api.register(PageResource())
v1_api.register(BlogPostResource())
urlpatterns = patterns('', url('^comments/post/$', 'foundry.views.post_comment', {}, name='comments-post-comment'), (
 '^favicon\\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=False)), (
 '^googlesearch/', include('googlesearch.urls')), (
 '^jmbo/', include('jmbo.urls')), (
 '^comments/', include('django.contrib.comments.urls')), (
 '^likes/', include('likes.urls')), (
 '^object-tools/', include(object_tools.tools.urls)), (
 '^ckeditor/', include('ckeditor.urls')), (
 '^contact/', include('contact.urls')), (
 '^post/', include('post.urls')), (
 '^simple-autocomplete/', include('simple_autocomplete.urls')), (
 '^jmbo-analytics/', include('jmbo_analytics.urls')), url('social-auth', include('social_auth.urls')), (
 '^admin/', include(admin.site.urls)), url('^$', TemplateView.as_view(template_name='base.html'), name='home'), url('^logo/$', TemplateView.as_view(template_name='foundry/logo.html'), name='logo'), url('^header/$', TemplateView.as_view(template_name='foundry/inclusion_tags/header.html'), name='header'), url('^footer/$', TemplateView.as_view(template_name='foundry/inclusion_tags/footer.html'), name='footer'), url('^join/$', 'foundry.views.join', {}, name='join'), url('^join-finish/$', 'foundry.views.join_finish', {}, name='join-finish'), (
 '^auth/', include('django.contrib.auth.urls')), url('^login/$', 'django.contrib.auth.views.login', {'authentication_form': forms.LoginForm}, name='login'), url('^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'), url('^password_reset/$', 'django.contrib.auth.views.password_reset', {'password_reset_form': forms.PasswordResetForm}, name='password_reset'), url('^about-us/$', views.StaticView.as_view(content=lambda : preferences.GeneralPreferences.about_us, title=_('About us')), name='about-us'), url('^terms-and-conditions/$', views.StaticView.as_view(content=lambda : preferences.GeneralPreferences.terms_and_conditions, title=_('Terms and conditions')), name='terms-and-conditions'), url('^privacy-policy/$', views.StaticView.as_view(content=lambda : preferences.GeneralPreferences.privacy_policy, title=_('Privacy policy')), name='privacy-policy'), url('^age-gateway/$', 'foundry.views.age_gateway', {}, name='age-gateway'), url('^listing/(?P<slug>[\\w-]+)/$', 'foundry.views.listing_detail', {}, name='listing-detail'), url('^listing/(?P<slug>[\\w-]+)/feed/$', 'foundry.feeds.listing_feed', {}, name='listing-feed'), url('^edit-profile/$', login_required(views.EditProfile.as_view(form_class=forms.EditProfileForm, template_name='foundry/edit_profile.html')), name='edit-profile'), url('^complete-profile/$', login_required(views.EditProfile.as_view(form_class=forms.EditProfileForm, template_name='foundry/complete_profile.html')), name='complete-profile'), url('^page/(?P<slug>[\\w-]+)/$', 'foundry.views.page_detail', {}, name='page-detail'), url('^lorem-ipsum/$', TemplateView.as_view(template_name='foundry/lorem_ipsum.html'), name='lorem-ipsum'), url('^search/$', 'foundry.views.search', {}, name='search'), url('^search-results/$', 'foundry.views.search_results', {}, name='search-results'), url('^comment-reply-form/$', 'foundry.views.comment_reply_form', {}, name='comment-reply-form'), url('^report-comment/(?P<comment_id>\\d+)/$', 'foundry.views.report_comment', {}, name='report-comment'), url('^chatroom/(?P<slug>[\\w-]+)/$', 'foundry.views.chatroom_detail', {}, name='chatroom-detail'), url('^create-blogpost/$', 'foundry.views.create_blogpost', {}, name='create-blogpost'), url('^blogposts/$', views.BlogPostObjectList.as_view(), {'limit': 300}, name='blogpost_object_list'), url('^blogpost/(?P<slug>[\\w-]+)/$', views.BlogPostObjectDetail.as_view(), {}, name='blogpost_object_detail'), url('^member-notifications/$', login_required(views.member_notifications), {}, name='member-notifications'), url('^users/(?P<username>[=@\\.\\w-]+)/$', 'foundry.views.user_detail', {}, name='user-detail'), url('^coming-soon/$', TemplateView.as_view(template_name='foundry/coming_soon.html'), name='coming-soon'), url('^fetch-new-comments-ajax/(?P<content_type_id>\\d+)/(?P<oid>\\d+)/(?P<last_comment_id>\\d+)/$', 'foundry.views.fetch_new_comments_ajax', {}, name='fetch-new-comments-ajax'), url('^test-plain-response/$', 'foundry.views.test_plain_response', {}, name='test-plain-response'), url('^test-redirect/$', 'foundry.views.test_redirect', {}, name='test-redirect'), url('^pages/$', DetailView.as_view(), {'queryset': Page.permitted.all().order_by('title')}, 'page-list'), url('^members/(?P<username>[\\w-]+)/$', 'foundry.views.member_detail', {}, name='member-detail'), url('^admin-row-create-ajax/$', 'foundry.admin_views.row_create_ajax', {}, name='admin-row-create-ajax'), url('^admin-column-create-ajax/$', 'foundry.admin_views.column_create_ajax', {}, name='admin-column-create-ajax'), url('^admin-tile-create-ajax/$', 'foundry.admin_views.tile_create_ajax', {}, name='admin-tile-create-ajax'), url('^admin-row-edit-ajax/$', 'foundry.admin_views.row_edit_ajax', {}, name='admin-row-edit-ajax'), url('^admin-column-edit-ajax/$', 'foundry.admin_views.column_edit_ajax', {}, name='admin-column-edit-ajax'), url('^admin-tile-edit-ajax/$', 'foundry.admin_views.tile_edit_ajax', {}, name='admin-tile-edit-ajax'), url('^admin-row-delete-ajax/$', 'foundry.admin_views.row_delete_ajax', {}, name='admin-row-delete-ajax'), url('^admin-column-delete-ajax/$', 'foundry.admin_views.column_delete_ajax', {}, name='admin-column-delete-ajax'), url('^admin-tile-delete-ajax/$', 'foundry.admin_views.tile_delete_ajax', {}, name='admin-tile-delete-ajax'), url('^admin-persist-sort-ajax/$', 'foundry.admin_views.persist_sort_ajax', {}, name='admin-persist-sort-ajax'), url('^admin-remove-comment/(?P<comment_id>\\d+)/$', 'foundry.admin_views.remove_comment', {}, name='admin-remove-comment'), url('^admin-allow-comment/(?P<comment_id>\\d+)/$', 'foundry.admin_views.allow_comment', {}, name='admin-allow-comment'))
if 'banner' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^banner/', include('banner.urls')))
if 'chart' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^chart/', include('chart.urls')))
if 'competition' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^competition/', include('competition.urls')))
if 'downloads' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^downloads/', include('downloads.urls')))
if 'friends' in settings.INSTALLED_APPS:
    urlpatterns.insert(1, url('^friends/', include('friends.urls')))
if 'gallery' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', (
     '^gallery/', include('gallery.urls')), (
     '^admin/', include('gallery.admin_urls')))
if 'jmbo_calendar' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^calendar/', include('jmbo_calendar.urls')))
if 'jmbo_twitter' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', (
     '^jmbo_twitter', include('jmbo_twitter.urls')), (
     '^admin/', include('jmbo_twitter.admin_urls')))
if 'music' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^music/', include('music.urls')))
if 'poll' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^poll/', include('poll.urls')))
if 'show' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^show/', include('show.urls')))
if 'video' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', ('^video/', include('video.urls')))
if 'jmbo_sitemap' in settings.INSTALLED_APPS:
    from jmbo_sitemap import sitemaps
    from jmbo_sitemap.views import sitemap, SitemapHTMLView
    urlpatterns += patterns('', url('^sitemap\\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'), url('^sitemap/$', SitemapHTMLView.as_view(), name='html-sitemap'))
urlpatterns += patterns('', ('^api/', include(v1_api.urls)))
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('', ('r^/', include('django.contrib.flatpages.urls')))
handler500 = 'foundry.views.server_error'
if settings.DEBUG:
    urlpatterns += patterns('', (
     '^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}))