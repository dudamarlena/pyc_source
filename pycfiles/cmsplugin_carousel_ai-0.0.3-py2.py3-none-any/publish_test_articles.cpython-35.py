# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/management/commands/publish_test_articles.py
# Compiled at: 2017-08-31 05:41:42
# Size of source mod 2**32: 1759 bytes
import random
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

class Command(BaseCommand):
    help = 'Creates published test articles with fake data.'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--lang', action='store', dest='language', default=settings.LANGUAGE_CODE, help='Language to be used.')
        parser.add_argument('-n', '--number', action='store', dest='number_of_articles', default=15, help='Number of articles to be created.')

    def handle(self, *args, **options):
        try:
            from cmsplugin_articles_ai.factories import CategoryFactory, TaggedArticleFactory
        except ImportError as e:
            self.stderr.write('Factories could not be imported. Please see README.')
            raise

        language = options['language']
        number_of_articles = int(options['number_of_articles'])
        print('Creating few test categories')
        categories = []
        for number in range(3):
            category = CategoryFactory()
            categories.append(category)
            print('  %s. category: %s' % (number + 1, category.title))

        translation.activate(language)
        print('Publishing articles with language: %s' % language)
        for number, _ in enumerate(range(number_of_articles)):
            article = TaggedArticleFactory(category=random.choice(categories))
            print('  %s. article: %s' % (number + 1, article.title))

        translation.deactivate()