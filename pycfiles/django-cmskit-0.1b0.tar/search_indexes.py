# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/recipes/search_indexes.py
# Compiled at: 2012-10-09 11:51:15
import datetime
from haystack.indexes import *
from haystack import site
from senpilic.recipes.models import Recipe
from cms_search.search_helpers.indexes import MultiLanguageIndex

class RecipeIndex(MultiLanguageIndex):
    title = CharField(model_attr='title')
    url = CharField(stored=True)
    text = CharField(document=True, use_template=True, template_name='search/recipes/recipe_index.txt')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Recipe.objects.published().select_related()

    def prepare_url(self, obj):
        try:
            return obj.get_absolute_url()
        except:
            pass

    class HaystackTrans:
        fields = ('url', )


site.register(Recipe, RecipeIndex)