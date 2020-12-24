# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/urls.py
# Compiled at: 2019-04-03 22:56:33
# Size of source mod 2**32: 3805 bytes
from django.conf.urls import include, url
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sitemaps.views import sitemap
from django.apps import apps
from cms.sitemaps import CMSSitemap
from dynamic_preferences.views import PreferenceFormView
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.forms import GlobalPreferenceForm
from danceschool.core.sitemaps import EventSitemap
urlpatterns = [
 url('^settings/global/$', (user_passes_test(lambda u: u.is_superuser)(PreferenceFormView.as_view(registry=global_preferences_registry,
   form_class=GlobalPreferenceForm,
   template_name='dynamic_preferences/form_danceschool.html'))),
   name='dynamic_preferences.global'),
 url('^settings/global/(?P<section>[\\w\\ ]+)$', (user_passes_test(lambda u: u.is_superuser)(PreferenceFormView.as_view(registry=global_preferences_registry,
   form_class=GlobalPreferenceForm,
   template_name='dynamic_preferences/form_danceschool.html'))),
   name='dynamic_preferences.global.section'),
 url('^filer/', include('filer.urls')),
 url('^', include('filer.server.urls')),
 url('^filebrowser_filer/', include('ckeditor_filebrowser_filer.urls')),
 url('^sitemap\\.xml$', sitemap,
   {'sitemaps': {'event':EventSitemap,  'page':CMSSitemap}},
   name='django.contrib.sitemaps.views.sitemap'),
 url('^accounts/', include('allauth.urls')),
 url('^', include('djangocms_forms.urls')),
 url('^', include('danceschool.core.urls')),
 url('^register/', include('danceschool.core.urls_registration'))]
if apps.is_installed('danceschool.banlist'):
    urlpatterns.append(url('^banlist/', include('danceschool.banlist.urls')))
if apps.is_installed('danceschool.discounts'):
    urlpatterns.append(url('^discounts/', include('danceschool.discounts.urls')))
if apps.is_installed('danceschool.financial'):
    urlpatterns.append(url('^financial/', include('danceschool.financial.urls')))
if apps.is_installed('danceschool.guestlist'):
    urlpatterns.append(url('^guest-list/', include('danceschool.guestlist.urls')))
if apps.is_installed('danceschool.prerequisites'):
    urlpatterns.append(url('^prerequisites/', include('danceschool.prerequisites.urls')))
if apps.is_installed('danceschool.private_events'):
    urlpatterns.append(url('^private-events/', include('danceschool.private_events.urls')))
if apps.is_installed('danceschool.private_lessons'):
    urlpatterns.append(url('^private-lessons/', include('danceschool.private_lessons.urls')))
if apps.is_installed('danceschool.vouchers'):
    urlpatterns.append(url('^vouchers/', include('danceschool.vouchers.urls')))
if apps.is_installed('danceschool.payments.payatdoor'):
    urlpatterns.append(url('^payatdoor/', include('danceschool.payments.payatdoor.urls')))
if apps.is_installed('danceschool.payments.paypal'):
    urlpatterns.append(url('^paypal/', include('danceschool.payments.paypal.urls')))
if apps.is_installed('danceschool.payments.stripe'):
    urlpatterns.append(url('^stripe/', include('danceschool.payments.stripe.urls')))
if apps.is_installed('danceschool.payments.square'):
    urlpatterns.append(url('^square/', include('danceschool.payments.square.urls')))