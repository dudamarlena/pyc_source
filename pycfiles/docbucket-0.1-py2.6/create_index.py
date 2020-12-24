# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/docbucket/management/commands/create_index.py
# Compiled at: 2010-12-14 16:12:04
from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
from docbucket.models import WHOOSH_SCHEMA
from whoosh import index
from whoosh.filedb.filestore import FileStorage
import os

class Command(NoArgsCommand):
    help = 'Create the index of search engine'

    def handle_noargs(self, *args, **options):
        if not os.path.exists(settings.WHOOSH_INDEX):
            os.mkdir(settings.WHOOSH_INDEX)
            ix = index.create_in(settings.WHOOSH_INDEX, WHOOSH_SCHEMA)