# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/recipes/urls.py
# Compiled at: 2012-11-19 10:50:40
from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from senpilic.recipes.models import Recipe
from senpilic.recipes.views import RecipeSearch, RecipeForm
urlpatterns = patterns('', url('^$', ListView.as_view(model=Recipe, template_name='recipes/index.html'), name='recipes_index'), url('^search/$', RecipeSearch.as_view(template_name='recipes/index.html'), name='recipes_search'), url('^create/$', RecipeForm.as_view(template_name='recipes/form.html'), name='recipes_form'), url('^(?P<slug>[-\\w]+)/$', DetailView.as_view(model=Recipe, template_name='recipes/recipe.html'), name='recipes_recipe'))