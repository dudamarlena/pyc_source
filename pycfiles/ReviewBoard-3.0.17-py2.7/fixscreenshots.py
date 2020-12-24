# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/management/commands/fixscreenshots.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import os
from django.core.management.base import NoArgsCommand
from reviewboard.reviews.models import Screenshot

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        prefix = os.path.join(b'images', b'uploaded')
        new_prefix = os.path.join(b'uploaded', b'images')
        for screenshot in Screenshot.objects.all():
            if screenshot.image.startswith(prefix):
                screenshot.image = os.path.join(new_prefix, os.path.basename(screenshot.image))
                screenshot.save()