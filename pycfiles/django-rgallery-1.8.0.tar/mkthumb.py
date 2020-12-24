# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/mkthumb.py
# Compiled at: 2015-02-24 07:27:17
from django.core.management.base import BaseCommand
from django.template import Context, Template
from django.conf import settings as conf
from sorl.thumbnail import get_thumbnail
import rgallery.models as mymodels
from utils import *

class Command(BaseCommand):
    help = '\n    Tool that regenerate the image cache for all the photos:\n\n    ./manage.py mkthumb\n\n    To run this script from a crontab task we should do something like this:\n\n    */30 * * * * cd /path/to/rgallery-project/ ; source env/bin/activate ;                  cd src ; python manage.py mkthumb > /dev/null\n\n    '

    def handle(self, *app_labels, **options):
        """
        The command itself
        """
        print ''
        print '-' * 80
        print ''
        print '[***] Making missing thumbs'
        print ''
        thumbs = conf.RGALLLERY_THUMBS
        conf.THUMBNAIL_DEBUG = True
        allphotos = mymodels.Photo.objects.all()
        for i, p in enumerate(allphotos):
            print '%04d - %s' % (i, p)
            for thumb in thumbs:
                c = Context({'image': p, 'thumb': '%sx%s' % (thumb, thumb)})
                t = Template('{% load thumbnail %}{% thumbnail image thumb crop="top" as img %}{{ img.url }}{% endthumbnail %}')
                t.render(c)
                get_thumbnail(p, '%sx%s' % (thumb, thumb))

        print ''
        print '-' * 80
        print ''
        print '[***] Done'
        print ''
        print '-' * 80