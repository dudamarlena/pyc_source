# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/functional/test_model_serializer.py
# Compiled at: 2018-05-06 09:04:01
import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
django.setup()
import pytest
from tests.app.serializers import UserSerializer, CategoryHierarchySerializer
from tests.app import models

@pytest.mark.django_db
def test_simple_saved():
    user = models.User.objects.create(name='Bob')
    serializer = UserSerializer(instance=user)
    data = serializer.data
    assert data['name'] == 'Bob'
    assert data['id'] > 0


def test_simple_unsaved():
    user = models.User(name='Bob')
    serializer = UserSerializer(instance=user)
    data = serializer.data
    assert data['name'] == 'Bob'
    assert data['id'] is None
    return


@pytest.mark.django_db
def test_complex():
    user = models.User.objects.create(name='Bob')
    top_category = models.FilmCategory.objects.create(name='All')
    child_movies = models.FilmCategory.objects.create(name='Child movies', parent_category=top_category)
    cartoons = models.FilmCategory.objects.create(name='Cartoons', parent_category=child_movies)
    serious_stuff = models.FilmCategory.objects.create(name='Serious', parent_category=top_category)
    anime = models.FilmCategory.objects.create(name='Anime', parent_category=serious_stuff)
    film_1 = models.Film.objects.create(name='Mickey Mouse', year=1966, uploaded_by=user, category=cartoons)
    film_2 = models.Film.objects.create(name='Ghost in the shell', year=1989, uploaded_by=user, category=anime)
    object = models.CategoryHierarchy(top_category, categories=[
     models.CategoryHierarchy(child_movies, categories=[
      models.CategoryHierarchy(cartoons, films=[
       film_1])]),
     models.CategoryHierarchy(serious_stuff, categories=[
      models.CategoryHierarchy(anime, films=[
       film_2])])])
    serializer = CategoryHierarchySerializer(object)
    data = serializer.data
    assert data['category']['name'] == 'All'
    assert data['categories'][0]['category']['name'] == 'Child movies'
    assert data['categories'][0]['categories'][0]['films'][0]['year'] == 1966
    assert data['categories'][1]['category']['name'] == 'Serious'
    assert data['categories'][1]['categories'][0]['films'][0]['year'] == 1989