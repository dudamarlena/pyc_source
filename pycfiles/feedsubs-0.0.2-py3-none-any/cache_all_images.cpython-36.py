# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/management/commands/cache_all_images.py
# Compiled at: 2018-09-30 10:27:19
# Size of source mod 2**32: 918 bytes
from django.core.management.base import BaseCommand
from ... import models, tasks
from ...html_processing import find_images_in_article

class Command(BaseCommand):
    help = 'Cache images found in all articles'

    def add_arguments(self, parser):
        parser.add_argument('--queue',
          dest='queue',
          help='Queue to consume')

    def handle(self, *args, **options):
        chunk_size = 200
        images_uris = set()
        articles_iter = models.Article.objects.select_related('feed').iterator(chunk_size=chunk_size)
        for i, article in enumerate(articles_iter, 1):
            images_uris.update(find_images_in_article(article.content, article.feed.uri))
            if i % chunk_size == 0:
                tasks.cache_images(images_uris)
                images_uris = set()