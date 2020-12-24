# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cal/tests.py
# Compiled at: 2011-03-28 05:04:09
from datetime import datetime, timedelta
import unittest
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models as django_models
from cal import models
from cal.models import Calendar, Entry, EntryItem
from panya.models import ModelBase

class WantedContent(ModelBase):
    pass


django_models.register_models('cal', WantedContent)

class UnwantedContent(ModelBase):
    pass


django_models.register_models('cal', UnwantedContent)

class EntrySaveHandlersTestCase(unittest.TestCase):

    def setUp(self):
        content = ModelBase()
        content.save()
        self.content = content
        calendar = models.Calendar()
        calendar.save()
        self.calendar = calendar

    def test_save_handler_does_not_repeat(self):
        entry = models.Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='does_not_repeat', content=self.content)
        entry.save()
        entry.calendars.add(self.calendar)
        entry.repeat = 'daily'
        self.failUnlessRaises(Exception, models.save_handler_does_not_repeat, entry)
        entry.repeat = 'does_not_repeat'
        models.save_handler_does_not_repeat(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.get().entry, entry)
        ent = entries.get()
        self.failUnlessEqual(ent.entry, entry)
        self.failUnlessEqual(ent.start, entry.start)
        self.failUnlessEqual(ent.end, entry.end)
        self.failUnlessEqual(ent.content, entry.content)
        self.failUnlessEqual(ent.entry, entry)
        self.failUnlessEqual(list(ent.calendars.all()), list(entry.calendars.all()))
        models.save_handler_does_not_repeat(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.get().entry, entry)

    def test_save_handler_daily(self):
        entry = models.Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=self.content)
        entry.save()
        entry.calendars.add(self.calendar)
        entry.repeat = 'does_not_repeat'
        self.failUnlessRaises(Exception, models.save_handler_daily, entry)
        entry.repeat = 'daily'
        entry.repeat_until = None
        self.failUnlessRaises(Exception, models.save_handler_daily, entry)
        entry.repeat_until = (entry.start + timedelta(days=30)).date()
        models.save_handler_daily(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 31)
        starts = set()
        entries = entries.order_by('start')
        for ent in entries:
            starts.add(ent.start)
            self.failUnlessEqual(ent.duration, entry.duration)
            self.failUnlessEqual(ent.entry, entry)
            self.failUnlessEqual(ent.content, entry.content)
            self.failUnlessEqual(list(ent.calendars.all()), list(entry.calendars.all()))

        self.failUnlessEqual(len(starts), 31)
        models.save_handler_daily(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 31)
        return

    def test_save_handler_weekdays(self):
        handler = models.save_handler_weekdays
        entry = models.Entry(start=datetime(year=2000, month=1, day=1, hour=1, minute=1), end=datetime(year=2000, month=1, day=1, hour=1, minute=1) + timedelta(days=1), repeat='weekdays', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=self.content)
        entry.save()
        entry.calendars.add(self.calendar)
        entry.repeat = 'does_not_repeat'
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat = 'weekdays'
        entry.repeat_until = None
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat_until = (entry.start + timedelta(days=30)).date()
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 21)
        starts = set()
        for ent in entries:
            starts.add(ent.start)
            self.failIf(ent.start.weekday() >= 5)
            self.failUnlessEqual(ent.duration, entry.duration)
            self.failUnlessEqual(ent.entry, entry)
            self.failUnlessEqual(ent.content, entry.content)
            self.failUnlessEqual(list(ent.calendars.all()), list(entry.calendars.all()))

        self.failUnlessEqual(len(starts), 21)
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 21)
        return

    def test_save_handler_weekends(self):
        handler = models.save_handler_weekends
        entry = models.Entry(start=datetime(year=2000, month=1, day=1, hour=1, minute=1), end=datetime(year=2000, month=1, day=1, hour=1, minute=1) + timedelta(days=1), repeat='weekends', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=self.content)
        entry.save()
        entry.calendars.add(self.calendar)
        entry.repeat = 'does_not_repeat'
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat = 'weekends'
        entry.repeat_until = None
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat_until = (entry.start + timedelta(days=30)).date()
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 10)
        starts = set()
        for ent in entries:
            starts.add(ent.start)
            self.failIf(ent.start.weekday() < 5)
            self.failUnlessEqual(ent.duration, entry.duration)
            self.failUnlessEqual(ent.entry, entry)
            self.failUnlessEqual(ent.content, entry.content)
            self.failUnlessEqual(list(ent.calendars.all()), list(entry.calendars.all()))

        self.failUnlessEqual(len(starts), 10)
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 10)
        return

    def test_save_handler_weekly(self):
        handler = models.save_handler_weekly
        entry = models.Entry(start=datetime(year=2000, month=1, day=1, hour=1, minute=1), end=datetime(year=2000, month=1, day=1, hour=1, minute=1) + timedelta(days=1), repeat='weekly', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=self.content)
        entry.save()
        entry.calendars.add(self.calendar)
        entry.repeat = 'does_not_repeat'
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat = 'weekly'
        entry.repeat_until = None
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat_until = (entry.start + timedelta(days=30)).date()
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 5)
        starts = set()
        for ent in entries:
            starts.add(ent.start)
            self.failUnlessEqual(ent.start.weekday(), entry.start.weekday())
            self.failUnlessEqual(ent.duration, entry.duration)
            self.failUnlessEqual(ent.entry, entry)
            self.failUnlessEqual(ent.content, entry.content)
            self.failUnlessEqual(list(ent.calendars.all()), list(entry.calendars.all()))

        self.failUnlessEqual(len(starts), 5)
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 5)
        return

    def test_save_handler_monthly_by_day_of_month(self):
        handler = models.save_handler_monthly_by_day_of_month
        entry = models.Entry(start=datetime(year=2000, month=1, day=31, hour=1, minute=1), end=datetime(year=2000, month=2, day=1, hour=1, minute=1) + timedelta(days=1), repeat='monthly_by_day_of_month', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=self.content)
        entry.save()
        entry.calendars.add(self.calendar)
        entry.repeat = 'does_not_repeat'
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat = 'monthly_by_day_of_month'
        entry.repeat_until = None
        self.failUnlessRaises(Exception, handler, entry)
        entry.repeat_until = (entry.start + timedelta(days=366)).date()
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 7)
        starts = set()
        for ent in entries:
            starts.add(ent.start)
            self.failUnlessEqual(ent.start.day, entry.start.day)
            self.failUnlessEqual(ent.duration, entry.duration)
            self.failUnlessEqual(ent.entry, entry)
            self.failUnlessEqual(ent.content, entry.content)
            self.failUnlessEqual(list(ent.calendars.all()), list(entry.calendars.all()))

        self.failUnlessEqual(len(starts), 7)
        handler(entry)
        entries = models.EntryItem.objects.filter(entry=entry)
        self.failUnlessEqual(entries.count(), 7)
        return


class PermittedManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.web_site = Site(domain='web.address.com')
        self.web_site.save()
        settings.SITE_ID = self.web_site.id

    def test_get_query_set(self):
        unpublished_cal = Calendar(title='title', state='unpublished')
        unpublished_cal.save()
        unpublished_cal.sites.add(self.web_site)
        unpublished_cal.save()
        staging_cal = Calendar(title='title', state='staging')
        staging_cal.save()
        staging_cal.sites.add(self.web_site)
        staging_cal.save()
        published_cal = Calendar(title='title', state='published')
        published_cal.save()
        published_cal.sites.add(self.web_site)
        published_cal.save()
        unpublished_content = ModelBase(title='title', state='unpublished')
        unpublished_content.save()
        unpublished_content.sites.add(self.web_site)
        unpublished_content.save()
        staging_content = ModelBase(title='title', state='staging')
        staging_content.save()
        staging_content.sites.add(self.web_site)
        staging_content.save()
        published_content = ModelBase(title='title', state='published')
        published_content.save()
        published_content.sites.add(self.web_site)
        published_content.save()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=unpublished_content)
        entry_obj.save()
        entry_obj.calendars.add(unpublished_cal)
        entry_obj.save()
        queryset = EntryItem.permitted.all()
        self.failIf(queryset.count())
        Entry.objects.all().delete()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=published_content)
        entry_obj.save()
        entry_obj.calendars.add(unpublished_cal)
        entry_obj.save()
        queryset = EntryItem.permitted.all()
        self.failIf(queryset.count())
        Entry.objects.all().delete()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=unpublished_content)
        entry_obj.save()
        entry_obj.calendars.add(published_cal)
        entry_obj.save()
        queryset = EntryItem.permitted.all()
        self.failIf(queryset.count())
        Entry.objects.all().delete()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=staging_content)
        entry_obj.save()
        entry_obj.calendars.add(staging_cal)
        entry_obj.save()
        settings.STAGING = False
        queryset = EntryItem.permitted.all()
        self.failIf(queryset.count())
        settings.STAGING = True
        queryset = EntryItem.permitted.all()
        self.failUnless(queryset.count())
        Entry.objects.all().delete()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=published_content)
        entry_obj.save()
        entry_obj.calendars.add(published_cal)
        entry_obj.save()
        queryset = EntryItem.permitted.all()
        self.failUnless(queryset.count())
        Entry.objects.all().delete()
        mobile_site = Site(domain='mobi.address.com')
        mobile_site.save()
        published_cal_mobile = Calendar(title='title', state='published')
        published_cal_mobile.save()
        published_cal_mobile.sites.add(mobile_site)
        published_cal_mobile.save()
        published_content_mobile = ModelBase(title='title', state='published')
        published_content_mobile.save()
        published_content_mobile.sites.add(mobile_site)
        published_content_mobile.save()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=published_content_mobile)
        entry_obj.save()
        entry_obj.calendars.add(published_cal_mobile)
        entry_obj.save()
        queryset = EntryItem.permitted.all()
        self.failIf(queryset.count())

    def test_by_model(self):
        published_cal = Calendar(title='title', state='published')
        published_cal.save()
        published_cal.sites.add(self.web_site)
        published_cal.save()
        wanted_content = WantedContent(title='title', state='published')
        wanted_content.save()
        wanted_content.sites.add(self.web_site)
        wanted_content.save()
        unwanted_content = UnwantedContent(title='title', state='published')
        unwanted_content.save()
        unwanted_content.sites.add(self.web_site)
        unwanted_content.save()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=wanted_content)
        entry_obj.save()
        entry_obj.calendars.add(published_cal)
        entry_obj.save()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=unwanted_content)
        entry_obj.save()
        entry_obj.calendars.add(published_cal)
        entry_obj.save()
        queryset = EntryItem.permitted.by_model(WantedContent)
        for obj in queryset:
            self.failUnlessEqual(obj.content.class_name, 'WantedContent')

    def test_now(self):
        published_cal = Calendar(title='title', state='published')
        published_cal.save()
        published_cal.sites.add(self.web_site)
        published_cal.save()
        content = ModelBase(title='title', state='published')
        content.save()
        content.sites.add(self.web_site)
        content.save()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=content)
        entry_obj.save()
        entry_obj.calendars.add(published_cal)
        entry_obj.save()
        queryset = EntryItem.permitted.now()
        self.failUnless(queryset.count())
        for entry_item in queryset:
            self.failUnless(entry_item.start < datetime.now())
            self.failUnless(entry_item.end > datetime.now())

    def test_by_range(self):
        published_cal = Calendar(title='title', state='published')
        published_cal.save()
        published_cal.sites.add(self.web_site)
        published_cal.save()
        content = ModelBase(title='title', state='published')
        content.save()
        content.sites.add(self.web_site)
        content.save()
        start = datetime.now()
        end = start + timedelta(days=2)
        spanning_entryitem = EntryItem(entry_id=1, start=start - timedelta(days=1), end=end + timedelta(days=1), content=content)
        spanning_entryitem.save()
        spanning_entryitem.calendars.add(published_cal)
        preceding_entryitem = EntryItem(entry_id=1, start=start - timedelta(days=1), end=start, content=content)
        preceding_entryitem.save()
        preceding_entryitem.calendars.add(published_cal)
        proceding_entryitem = EntryItem(entry_id=1, start=end, end=end + timedelta(days=1), content=content)
        proceding_entryitem.save()
        proceding_entryitem.calendars.add(published_cal)
        contained_entryitem = EntryItem(entry_id=1, start=start, end=end, content=content)
        contained_entryitem.save()
        contained_entryitem.calendars.add(published_cal)
        end_contained_entryitem = EntryItem(entry_id=1, start=start - timedelta(days=1), end=end, content=content)
        end_contained_entryitem.save()
        end_contained_entryitem.calendars.add(published_cal)
        start_contained_entryitem = EntryItem(entry_id=1, start=start, end=end + timedelta(days=1), content=content)
        start_contained_entryitem.save()
        start_contained_entryitem.calendars.add(published_cal)
        result = EntryItem.permitted.by_range(start, end)
        self.failUnless(spanning_entryitem in result)
        self.failIf(preceding_entryitem in result)
        self.failIf(proceding_entryitem in result)
        self.failUnless(contained_entryitem in result)
        self.failUnless(end_contained_entryitem in result)
        self.failUnless(start_contained_entryitem in result)

    def test_by_date(self):
        published_cal = Calendar(title='title', state='published')
        published_cal.save()
        published_cal.sites.add(self.web_site)
        published_cal.save()
        content = ModelBase(title='title', state='published')
        content.save()
        content.sites.add(self.web_site)
        content.save()
        entry_obj = Entry(start=datetime.now(), end=datetime.now() + timedelta(days=1), repeat='daily', repeat_until=(datetime.now() + timedelta(days=30)).date(), content=content)
        entry_obj.save()
        entry_obj.calendars.add(published_cal)
        entry_obj.save()
        now = datetime.now()
        date = now.date()
        result = EntryItem.permitted.by_date(date)
        self.failUnlessEqual(result.count(), 1)