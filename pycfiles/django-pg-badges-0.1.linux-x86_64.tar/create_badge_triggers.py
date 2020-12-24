# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yohann/Dev/django-pg-badges/demo/venv/lib/python2.7/site-packages/badges/management/commands/create_badge_triggers.py
# Compiled at: 2016-01-24 17:14:32
import json
from django.db import connection
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from os.path import dirname, join
DROP_TEMPLATE = "\nSELECT proname, relname FROM\n    (pg_trigger JOIN pg_class ON tgrelid=pg_class.oid)\nJOIN pg_proc ON (tgfoid=pg_proc.oid) WHERE proname LIKE 'badge_%';\n"

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--file', action='store_true', dest='file', default=None, help='Chose a badge file')
        return

    def handle(self, *args, **options):
        if options['file']:
            fd = options['file']
        elif hasattr(settings, 'BADGES_FILE'):
            fd = settings.BADGES_FILE
        else:
            raise CommandError('You must set the BADGES_FILE location in your settings')
        with open(fd) as (json_file):
            create_triggers(json_file.read())


def validate(badge_dict):
    for key in ['name', 'code', 'condition',
     'trigger_condition', 'trigger_table',
     'user_field']:
        if not badge_dict.get(key):
            raise ValueError(('the badge definition need a {} key').format(key))


def drop_existing_triggers():
    """
    Every badges triggers are prefixed with "badge_"
    So we first get all the existing triggers and delete them.
    One by one... No mercy.
    """
    with connection.cursor() as (cur):
        cur.execute(DROP_TEMPLATE)
        for result in cur.fetchall():
            cur.execute(('DROP TRIGGER {} ON {}').format(result[0], result[1]))


def create_trigger(badge_dict, check_needed=True):
    """
    Create the underlying triggers for the badge process to work
    """
    if check_needed:
        validate(badge_dict)
    with open(join(dirname(__file__), 'trigger.sql')) as (sql):
        with connection.cursor() as (cur):
            cur.execute(sql.read().format(**badge_dict))


def create_triggers(badge_files):
    """
    Create all the triggers in the badges.json file
    """
    badge_dicts = json.loads(badge_files)
    for badge_dict in badge_dicts:
        validate(badge_dict)

    drop_existing_triggers()
    for badge_dict in badge_dicts:
        create_trigger(badge_dict, check_needed=False)