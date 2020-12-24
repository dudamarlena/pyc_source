# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/philip/vms/vagrant/django-rest-framework-chain/rest_framework_chain/tests.py
# Compiled at: 2013-12-11 23:31:42
# Size of source mod 2**32: 5237 bytes
from __future__ import unicode_literals
from django.db import models
from django.test import TestCase
from django.contrib.auth.models import User
import django_filters
from .filters import RelatedFilter, AllLookupsFilter
from .filterset import ChainedFilterSet

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User)


class NoteFilterWithAll(ChainedFilterSet):
    title = AllLookupsFilter(name='title')

    class Meta:
        model = Note


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(name='username')
    email = django_filters.CharFilter(name='email')

    class Meta:
        model = User


class UserFilterWithAll(ChainedFilterSet):
    username = AllLookupsFilter(name='username')
    email = django_filters.CharFilter(name='email')

    class Meta:
        model = User


class NoteFilterWithRelated(ChainedFilterSet):
    title = django_filters.CharFilter(name='title')
    author = RelatedFilter(UserFilter, name='author')

    class Meta:
        model = Note


class NoteFilterWithRelatedAll(ChainedFilterSet):
    title = django_filters.CharFilter(name='title')
    author = RelatedFilter(UserFilterWithAll, name='author')

    class Meta:
        model = Note


class TestAllLookupsFilter(TestCase):

    def setUp(self):
        user1 = User(username='user1', email='user1@example.org')
        user1.save()
        user2 = User(username='user2', email='user2@example.org')
        user2.save()
        n = Note(title='Test 1', content='Test content 1', author=user1)
        n.save()
        n = Note(title='Test 2', content='Test content 2', author=user1)
        n.save()
        n = Note(title='Hello Test 3', content='Test content 3', author=user1)
        n.save()
        n = Note(title='Hello Test 4', content='Test content 4', author=user2)
        n.save()

    def test_alllookupsfilter(self):
        GET = {'title__iendswith': '2'}
        f = NoteFilterWithAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 1)
        note = list(f)[0]
        self.assertEqual(note.title, 'Test 2')
        GET = {'title__contains': 'Test'}
        f = NoteFilterWithAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 4)
        GET = {'title': 'Hello Test 3'}
        f = NoteFilterWithAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 1)
        note = list(f)[0]
        self.assertEqual(note.title, 'Hello Test 3')

    def test_relatedfilter(self):
        GET = {'author': User.objects.get(username='user2').pk}
        f = NoteFilterWithRelated(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 1)
        note = list(f)[0]
        self.assertEqual(note.title, 'Hello Test 4')
        GET = {'author__username': 'user2'}
        f = NoteFilterWithRelated(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 1)
        note = list(f)[0]
        self.assertEqual(note.title, 'Hello Test 4')

    def test_relatedfilter_combined_with_alllookups(self):
        GET = {'author': User.objects.get(username='user2').pk}
        f = NoteFilterWithRelatedAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 1)
        note = list(f)[0]
        self.assertEqual(note.title, 'Hello Test 4')
        GET = {'author__username': 'user2'}
        f = NoteFilterWithRelatedAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 1)
        note = list(f)[0]
        self.assertEqual(note.title, 'Hello Test 4')
        GET = {'author__username__endswith': '2'}
        f = NoteFilterWithRelatedAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 1)
        note = list(f)[0]
        self.assertEqual(note.title, 'Hello Test 4')
        GET = {'author__username__endswith': '1'}
        f = NoteFilterWithRelatedAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 3)
        GET = {'author__username__contains': 'user'}
        f = NoteFilterWithRelatedAll(GET, queryset=Note.objects.all())
        self.assertEqual(len(list(f)), 4)