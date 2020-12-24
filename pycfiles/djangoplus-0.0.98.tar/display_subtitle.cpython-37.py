# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/tools/management/commands/display_subtitle.py
# Compiled at: 2018-10-05 12:52:37
# Size of source mod 2**32: 445 bytes
from djangoplus.tools.subtitle import Subtitle
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('words', nargs='*', default=None)

    def handle(self, *args, **options):
        words = options.pop('words')
        Subtitle.display(' '.join(words).replace('\\n', '\n'))