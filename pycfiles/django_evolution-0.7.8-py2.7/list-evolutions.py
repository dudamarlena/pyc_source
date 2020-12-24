# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/management/commands/list-evolutions.py
# Compiled at: 2018-06-14 23:17:51
from django.core.management.base import BaseCommand
from django.db.models import get_apps
from django_evolution.models import Evolution
from django_evolution.utils import get_app_label

class Command(BaseCommand):
    """Lists the applied evolutions for one or more apps."""

    def handle(self, *app_labels, **options):
        if not app_labels:
            app_labels = [ get_app_label(app) for app in get_apps() ]
        for app_label in app_labels:
            evolutions = list(Evolution.objects.filter(app_label=app_label))
            if evolutions:
                print "Applied evolutions for '%s':" % app_label
                for evolution in evolutions:
                    print '    %s' % evolution.label

                print