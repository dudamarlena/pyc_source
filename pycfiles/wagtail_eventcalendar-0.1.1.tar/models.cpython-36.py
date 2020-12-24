# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/eventcalendar/base/wagtail_eventcalendar/wagtail_eventcalendar/models.py
# Compiled at: 2018-10-04 05:06:05
# Size of source mod 2**32: 15997 bytes
from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.models import Page
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from .managers import CategoryManager
from modelcluster.fields import ParentalKey
from wagtailgmaps.edit_handlers import MapFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
import json
from django.shortcuts import render
from django.utils import timezone
from wagtail.search import index
from icalendar import Calendar, Event, vText
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
import pytz, django.http
from typing import Union

class EventCalendar(RoutablePageMixin, Page):
    __doc__ = '\n    Base calendar class which actually displays the calendar.\n    '
    description = RichTextField(blank=True, help_text=(_('Description of the calendar')), verbose_name=(_('Description')))
    default_image = models.ForeignKey('wagtailimages.Image', null=True,
      blank=True,
      on_delete=(models.SET_NULL),
      related_name='+',
      verbose_name=(_('Default Image')),
      help_text=(_('Default image to be used for calendar entries')))
    content_panels = Page.content_panels + [
     FieldPanel('description'),
     ImageChooserPanel('default_image')]
    subpage_types = [
     'wagtail_eventcalendar.EventCalPage']
    search_fields = Page.search_fields + [
     index.SearchField('description')]

    class Meta:
        verbose_name = _('Calendar Root Page')

    @route('^events/$')
    def getEvents(self, request):
        """
        Route that returns the events. Is accessed by fullcalender as the api to call

        :param request: Django request
        :return: JSON of the events ard their details
        """

        def filterForPeriod(request: django.http.HttpRequest) -> models.QuerySet:
            """
            Filter for the specific time frame being queried by FullCalendar

            :param request: Django request
            :return: Queryset of EventCalPage objects
            """
            events = EventCalPage.objects.filter(start_dt__range=[request.GET['start'], request.GET['end']]).live()
            return events

        if request.is_ajax():
            result = [{'title':event.title,  'start':event.start_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),  'end':event.end_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),  'url':event.url} for event in filterForPeriod(request)]
            json_output = json.dumps(result)
            return HttpResponse(json_output)
        else:
            return super(EventCalendar, self).serve(request)

    @route('^category/(?P<category>[\\w\\-]+)/$')
    def viewByCategory(self, request: django.http.HttpRequest, **kwargs) -> django.http.HttpResponse:
        """
        View calendar by a specific category

        :param request: Django request
        :param kwargs: Django request kwargs
        :return: HttpResponse that shows a calendar filtered by a category
        """
        return render(request, 'eventcalendar/event_calendar_category.html', {'self':self, 
         'page':self,  'category':kwargs['category']})

    @route('^category/(?P<category>[\\w\\-]+)/events/$')
    def getEventsByCategory(self, request: django.http.HttpRequest, **kwargs: dict) -> django.http.HttpResponse:
        """
        Gets the events for a specific category for a specific timeframe. Is accessed by fullcalender.js

        :param request: Django request
        :param kwargs: Django request kwargs
        :return: HttpResponse
        """
        categ = kwargs['category']

        def filterForPeriod(request: django.http.HttpRequest, categ: str) -> django.http.HttpResponse:
            """
            Filters for a period taking into account the specific category

            :param request:
            :param categ:
            :return:
            """
            events = EventCalPage.objects.filter(start_dt__range=[request.GET['start'], request.GET['end']]).live()
            events = events.filter(categories__name__iexact=categ)
            return events

        if request.is_ajax():
            result = [{'title':event.title,  'start':event.start_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),  'end':event.end_dt.astimezone(pytz.timezone(request.GET['timezone'])).isoformat(),  'url':event.url} for event in filterForPeriod(request, categ)]
            json_output = json.dumps(result)
            return HttpResponse(json_output)
        else:
            return render(request, 'eventcalendar/event_calendar_category.html', {'self':self, 
             'page':self,  'category':kwargs['category']})

    @route('^ical/$')
    def icalView(self, request: django.http.HttpRequest, *args, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that produces the ical files requested by clients.

        :param request: Django request
        :param args: Django request args
        :param kwargs: Django request kwargs
        :return: HttpResponse containing an ical file
        """
        cal = Calendar()
        cal.add('prodid', '-//Calendar Event event//mxm.dk//')
        cal.add('version', '2.0')
        for entry in EventCalPage.objects.live():
            event = Event()
            event.add('summary', entry.title)
            event.add('dtstart', entry.start_dt)
            event.add('dtend', entry.end_dt)
            event.add('dtstamp', timezone.now())
            event.add('uid', str(entry.pk))
            event['location'] = vText(entry.location)
            cal.add_component(event)

        return HttpResponse((cal.to_ical()), content_type='text/calendar')

    @route('^category/(?P<category>[\\w\\-]+)/ical/$')
    def icalViewCategory(self, request: django.http.HttpRequest, *args, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that produces the ical files requested by clients, but filtered for a specific category

        :param request: Django HttpRequest
        :param args: Django request args
        :param kwargs: Django request kwargs
        :return: HttpResponse containing an ical file
        """
        cal = Calendar()
        cal.add('prodid', '-//Calendar Event event//mxm.dk//')
        cal.add('version', '2.0')
        print(kwargs['category'])
        for entry in EventCalPage.objects.filter(categories__name__iexact=(kwargs['category'])).live():
            event = Event()
            event.add('summary', entry.title)
            event.add('dtstart', entry.start_dt)
            event.add('dtend', entry.end_dt)
            event.add('dtstamp', timezone.now())
            event.add('uid', str(entry.pk))
            event['location'] = vText(entry.location)
            cal.add_component(event)

        return HttpResponse((cal.to_ical()), content_type='text/calendar')

    @property
    def get_categories(self) -> models.QuerySet:
        """
        Gets the calendar categories that currently exist

        :return: Returns a Queryset of Category objects
        """
        return Category.objects.all()

    @property
    def get_url(self) -> str:
        """
        Gets the url of the calendar page

        :return: Url of the calendar page
        """
        return self.url


class EventCalPage(RoutablePageMixin, Page):
    __doc__ = '\n    Calendar entry/ an even base model.\n    '
    categories = models.ManyToManyField('wagtail_eventcalendar.Category', through='wagtail_eventcalendar.CategoryEventPage', blank=True, help_text=(_('Categories this event belongs to')),
      verbose_name=(_('Categories')))
    description = RichTextField(blank=True, help_text=(_('Description of event')), verbose_name=(_('Description')))
    image = models.ForeignKey('wagtailimages.Image', null=True,
      blank=True,
      on_delete=(models.SET_NULL),
      related_name='+',
      verbose_name=(_('Image')))
    start_dt = models.DateTimeField(help_text=(_('Starting time of event')), verbose_name=(_('Start of Event')))
    end_dt = models.DateTimeField(help_text=(_('End time of event. Does not need to be same day.')), verbose_name=(_('End of Event')))
    location = models.CharField(max_length=255, blank=True, help_text=(_('Location of event')), verbose_name=(_('Location')))
    problem_status = models.BooleanField(default=False, help_text=(_('Whether there is a problem with the event')), verbose_name=(_('Problem Status')))
    problem_text = models.TextField(blank=True, null=True, help_text=(_('Text that describes the problem. Keep brief.')), verbose_name=(_('Problem Description')))
    content_panels = Page.content_panels + [
     FieldPanel('description'),
     ImageChooserPanel('image'),
     FieldPanel('start_dt'),
     FieldPanel('end_dt'),
     MapFieldPanel('location'),
     MultiFieldPanel([
      InlinePanel('event_categories', label=(_('Categories')))])]
    settings_panels = Page.settings_panels + [
     FieldPanel('problem_status'),
     FieldPanel('problem_text')]
    parent_page_types = [
     'wagtail_eventcalendar.EventCalendar']
    search_fields = Page.search_fields + [
     index.SearchField('description'),
     index.RelatedFields('categories', [
      index.SearchField('name'),
      index.SearchField('description')])]

    class Meta:
        verbose_name = _('Calendar Event')

    def clean(self):
        """
        Checks that the end date and time occurs after the start date and date
        """
        if self.start_dt > self.end_dt:
            raise ValidationError(_('Start date and time must be before end date and time'))

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = EventCalendar.objects.live()[0].default_image
        super(EventCalPage, self).save()

    @property
    def get_categories(self) -> models.QuerySet:
        """
        Gets all the event categories.

        :return: Queryset containing the Categories objects
        """
        return Category.objects.all()

    @property
    def get_status_text(self) -> Union[(str, bool)]:
        """
        Shows the status text of a calender entry/event

        :return: Str if the event is finished, or begun but not yet completed else false.
        """
        if self.end_dt < timezone.now():
            return _('Event Finished')
        else:
            if self.problem_status:
                return self.problem_text
            if self.start_dt < timezone.now() < self.end_dt:
                return _('Event has begun')
            return False

    @route('^ical/$')
    def icalView(self, request: django.http.HttpRequest, *args, **kwargs: dict) -> django.http.HttpResponse:
        """
        Route that returns an ical file for a specific event.

        :param request: Django HttpRequest
        :param args: Normal request args
        :param kwargs: Normal request kwargs
        :return: ical file as part of HttpResponse with only the details of a specific event
        """
        cal = Calendar()
        cal.add('prodid', '-//Calendar Event event//mxm.dk//')
        cal.add('version', '2.0')
        event = Event()
        event.add('summary', self.title)
        event.add('dtstart', self.start_dt)
        event.add('dtend', self.end_dt)
        event.add('dtstamp', timezone.now())
        event.add('uid', str(self.pk))
        event['location'] = vText(self.location)
        cal.add_component(event)
        return HttpResponse((cal.to_ical()), content_type='text/calendar')


class Category(models.Model):
    __doc__ = '\n    Category to which an event belongs\n    '
    name = models.CharField(max_length=80, unique=True, verbose_name=(_('Category name')))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey('self',
      blank=True,
      null=True,
      related_name='children',
      verbose_name=(_('Parent category')),
      on_delete=(models.SET_NULL))
    description = models.CharField(max_length=500, blank=True, verbose_name=(_('Description')))
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        """
        Ensures that there are no circular references when it comes to nested categories.
        """
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_('Parent category cannot be self.'))
            if parent.parent:
                if parent.parent == self:
                    raise ValidationError(_('Cannot have circular Parents.'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return (super(Category, self).save)(*args, **kwargs)

    class Meta:
        ordering = [
         'name']
        verbose_name = _('Event Category')
        verbose_name_plural = _('Event Categories')


class CategoryEventPage(models.Model):
    __doc__ = 'Internally used model. Ignore.'
    category = models.ForeignKey(Category, related_name='+', verbose_name=(_('Category')), on_delete=(models.CASCADE))
    page = ParentalKey('EventCalPage', related_name='event_categories')
    panels = [
     FieldPanel('category')]

    def __str__(self):
        return str(self.category)