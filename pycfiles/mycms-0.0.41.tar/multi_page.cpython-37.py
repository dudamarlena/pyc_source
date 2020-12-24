# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/view_handlers/multi_page.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 6370 bytes
from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import OperationalError
import logging
logger = logging.getLogger('mycms.page_handlers')

class MultiPage(object):

    def __init__(self, page_object, request=None):
        self.page_object = page_object
        try:
            self.memberpageview_pagetype_obj = CMSPageTypes.objects.get(page_type='MEMBERPAGE')
        except ObjectDoesNotExist as e:
            try:
                msg = 'Could not load MEMBERPAGE view object. Going to create it.'
                logger.debug(msg)
                self.memberpageview_pagetype_obj, _ = CMSPageTypes.objects.get_or_create(page_type='MEMBERPAGE', text='MemberPage Article',
                  view_class='MemberPage',
                  view_template='MemberPage.html')
            finally:
                e = None
                del e

        except MultipleObjectsReturned as e:
            try:
                msg = 'Got more than 1 CMSMultiPageType: MULTIPAGE. Database is inconsistent. Will return the first one.'
                logger.info(msg)
                memberpageview_pagetype_obj = CMSMultiPageTypes.objects.filter(page_type='MEMBERPAGE')[0]
            finally:
                e = None
                del e

    @property
    def is_multipage(self):
        return True

    def articles(self):
        """Here we load all pages that says we are their parent."""
        obj_list = CMSEntries.objects.filter(page_type=(self.memberpageview_pagetype_obj), path__parent__id=(self.page_object.path.id))
        view_list = []
        for obj in obj_list:
            view_list.append(ViewObject(page_object=obj))

        return view_list

    def page_types(self):
        """
        Refactor me into a parent class.
        returns a list fo page_types
        """
        pagetype_objs = CMSPageTypes.objects.filter(page_type='MEMBERPAGE')
        return pagetype_objs

    def on_create(self):
        print('Created a new article {}'.format(self.page_object.title))

    @property
    def first_page_object(self):
        return self.page_object

    @property
    def member_page_objects(self):
        member_cmsentries = CMSEntries.objects.filter(path__parent=(self.page_object.path)).order_by('page_number')
        return member_cmsentries

    @property
    def first_page_object(self):
        return self.page_object.parent

    @property
    def first_page(self):
        entries = CMSEntries.objects.filter(path__parent=(self.page_object.path)).order_by('page_number')
        num_entries = len(entries)
        print(num_entries)
        if entries.count() > 0:
            return entries[0]
        return

    @property
    def has_first_page(self):
        if self.first_page == None:
            return False
        return True


class MemberPage(object):

    def __init__(self, page_object, request=None):
        self.page_object = page_object

    def on_create(self):
        """
        A new member page has been created. Append it as the last page.

        """
        print('Created a memberpage called {}'.format(self.page_object.title))
        my_parent_object = CMSEntries.objects.get(path=(self.page_object.path.parent))
        print(my_parent_object.title)
        my_siblings = CMSEntries.objects.filter(path__parent=(self.page_object.path.parent))
        for sibling in my_siblings:
            print(sibling.title)

        last_page_num = self.last_member_page_object.page_number
        self.page_object.page_number = last_page_num + 1
        self.page_object.save()

    @property
    def member_page_objects(self):
        return CMSEntries.objects.filter(path__parent=(self.page_object.path.parent)).order_by('page_number')

    @property
    def first_member_page_object(self):
        pass

    @property
    def last_member_page_object(self):
        c = self.member_page_objects.count()
        if c == 1:
            return self.member_page_objects[0]
        if c == 0:
            return
        return self.member_page_objects[(c - 1)]

    @property
    def next_page(self):
        """
        Get the next page by getting all the pages that have greater page_number than us.
        """
        next_pages = CMSEntries.objects.filter(path__parent=(self.page_object.path.parent), page_number__gt=(self.page_object.page_number)).order_by('page_number')
        num_results = len(next_pages)
        if num_results > 0:
            return next_pages[0]
        return

    @property
    def previous_page(self):
        previous_pages = CMSEntries.objects.filter(path__parent=(self.page_object.path.parent), page_number__lt=(self.page_object.page_number)).order_by('-page_number')
        num_results = len(previous_pages)
        if num_results > 0:
            return previous_pages[0]
        return

    @property
    def first_page(self):
        entries = CMSEntries.objects.filter(path__parent=(self.page_object.path.parent)).order_by('page_number')
        return entries[0]

    @property
    def is_last_page(self):
        entries = CMSEntries.objects.filter(path__parent=(self.page_object.path.parent)).order_by('-page_number')
        if entries[0] == self.page_object:
            return True
        return False

    @property
    def is_first_page(self):
        if self.page_object == self.first_page:
            return True
        return False