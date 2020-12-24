# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-preferences/preferences/tests/test_all.py
# Compiled at: 2018-12-20 02:32:17
# Size of source mod 2**32: 6804 bytes
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template import RequestContext, Template
from django.test import TestCase
from django.test.client import RequestFactory
from preferences import context_processors, preferences
from preferences.admin import PreferencesAdmin
from preferences.tests.models import MyPreferences

class AdminTestCase(TestCase):

    def test_changelist_view(self):
        request = RequestFactory().get('/')
        request.user = User.objects.create(username='name', password='pass', is_superuser=True)
        admin_obj = PreferencesAdmin(MyPreferences, admin.site)
        response = admin_obj.changelist_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/tests/mypreferences/%s/change/' % MyPreferences.objects.all()[0].id)
        obj = MyPreferences.objects.create()
        response = admin_obj.changelist_view(request)
        response.render()
        self.failUnless('changelist-form' in response.content.decode('utf-8'), 'Should display listing if multiple preferences objects are available.')


class ContextProcessorsTestCase(TestCase):

    def test_preferences_cp(self):
        request = RequestFactory().get('/')
        context = context_processors.preferences_cp(request)
        my_preferences = context['preferences']
        my_preferences = my_preferences.MyPreferences
        self.failUnless(isinstance(my_preferences, MyPreferences), '%s should be instance of MyPreferences.' % my_preferences)
        context_instance = RequestContext(request)
        t = Template('{% if preferences %}{{ preferences }}{% endif %}')
        self.failUnless(t.render(context_instance), 'preferences should be available in template context.')
        t = Template('{% if preferences.MyPreferences %}{{ preferences.MyPreferences }}{% endif %}')
        self.failUnless(t.render(context_instance), 'MyPreferences should be available as part of preferences var in template context.')


class ModelsTestCase(TestCase):

    def test_preferences_class_prepared(self):
        """
        Regardless of what happens in the background, after startup and model
        preparation the preferences.preferences object should have members for
        each of the various preferences models. When accessing the member the
        appropriate object for the current site should be returned (or
        unassociated with a site if not using sites).
        """
        my_preferences = preferences.MyPreferences
        self.failIf(my_preferences.sites.all(), 'Without SITE_ID should not have any preferences with sites.')
        settings.SITE_ID = 1
        current_site = Site.objects.get_current()
        my_preferences = preferences.MyPreferences
        self.failUnlessEqual(current_site, my_preferences.sites.get(), 'With SITE_ID should have preferences for current site.')
        settings.SITE_ID = 2
        second_site, created = Site.objects.get_or_create(id=2)
        my_preferences = preferences.MyPreferences
        self.failUnlessEqual(second_site, my_preferences.sites.get(), 'With SITE_ID should have preferences for current site.')

    def test_site_cleanup(self):
        """
        There should only ever be a single preferences object per site. Thus on
        many to many changes pre-existing preferences should be cleared of
        sites already associated with current preferences object.
        """
        site1 = Site.objects.create(domain='testserver')
        site2 = Site.objects.create(domain='another')
        site1_preferences = MyPreferences.objects.create()
        site1_preferences.sites.add(site1)
        self.failUnlessEqual(site1_preferences.sites.get(), site1)
        more_site1_preferences = MyPreferences.objects.create()
        more_site1_preferences.sites.add(site1)
        self.failIf(site1 in site1_preferences.sites.all())
        more_site1_preferences.sites.add(site2)
        self.failIf(site1 not in more_site1_preferences.sites.all() or site2 not in more_site1_preferences.sites.all())
        some_more_preferences = MyPreferences.objects.create()
        some_more_preferences.sites.add(site1)
        some_more_preferences.sites.add(site2)
        self.failIf(site1 in more_site1_preferences.sites.all() or site2 in more_site1_preferences.sites.all())
        self.failUnlessEqual(MyPreferences.objects.filter(sites__in=[site1, site2]).distinct().get(), some_more_preferences)


class SingletonManagerTestCase(TestCase):

    def test_get_queryset(self):
        self.failIf(MyPreferences.singleton.get().sites.all(), 'Without                 SITE_ID should not have any preferences with sites.')
        settings.SITE_ID = 1
        current_site = Site.objects.get_current()
        obj = MyPreferences.singleton.get()
        self.failUnlessEqual(current_site, obj.sites.get(), 'With SITE_ID                 should have preferences for current site.')
        settings.SITE_ID = 2
        second_site, created = Site.objects.get_or_create(id=2)
        obj = MyPreferences.singleton.get()
        self.failUnlessEqual(second_site, obj.sites.get(), 'With SITE_ID                 should have preferences for current site.')