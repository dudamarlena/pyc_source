# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/management/commands/loaddb.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import importlib, os, re
from django import db
from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import get_apps
from django.utils.six.moves import input

class Command(BaseCommand):
    """Management command to load data into the database."""
    help = b'Loads data formatted by dumpdb, for migration across types of databases.'

    def handle(self, *args, **options):
        """Handle the command."""
        if len(args) != 1:
            raise CommandError(b'You must specify a filename on the command line.')
        filename = args[0]
        if not os.path.exists(filename):
            raise CommandError(b'%s does not exist.' % filename)
        try:
            importlib.import_module(b'django_reset')
        except ImportError:
            raise CommandError(b"Before using this command, you need to install the 'django-reset' package")

        confirm = input(b'\nThis will wipe out your existing database prior to loading. It is highly\nrecommended that you have a full SQL database dump in case things go wrong.\n\nYou should only use this if you\'re migrating from one type of database to\nanother, with the same version of Review Board on each.\n\nAre you sure you want to continue?"\n\nType \'yes\' to continue, or \'no\' to cancel: ')
        if confirm != b'yes':
            return
        apps = [ app.__name__.split(b'.')[(-2)] for app in get_apps() ]
        os.system(b'./reviewboard/manage.py reset --noinput %s' % (b' ').join(apps))
        transaction_setup = False
        try:
            with open(filename, b'r') as (f):
                line = f.readline()
                m = re.match(b'^# dbdump v(\\d+) - (\\d+) objects$', line)
                if not m:
                    raise CommandError(b'Unknown dump format\n')
                version = int(m.group(1))
                totalobjs = int(m.group(2))
                i = 0
                prev_pct = -1
                if version != 1:
                    raise CommandError(b'Unknown dump version\n')
                transaction.commit_unless_managed()
                transaction.enter_transaction_management()
                transaction.managed(True)
                transaction_setup = True
                self.stdout.write(b'Importing new style dump format (v%s)' % version)
                for line in f:
                    if line[0] == b'{':
                        for obj in serializers.deserialize(b'json', b'[%s]' % line):
                            try:
                                obj.save()
                            except Exception as e:
                                self.stderr.write(b'Error: %s\n' % e)
                                self.stderr.write(b"Line %s: '%s'" % (i, line))

                    elif line[0] != b'#':
                        self.stderr.write(b'Junk data on line %s' % i)
                    db.reset_queries()
                    i += 1
                    pct = i * 100 / totalobjs
                    if pct != prev_pct:
                        self.stdout.write(b'  [%s%%]\r' % pct)
                        self.stdout.flush()
                        prev_pct = pct

            transaction.commit()
            transaction.leave_transaction_management()
        except Exception as e:
            if transaction_setup:
                transaction.rollback()
                transaction.leave_transaction_management()
            raise CommandError(b"Problem installing '%s': %s\n" % (filename, e))

        self.stdout.write(b'\nDone.')