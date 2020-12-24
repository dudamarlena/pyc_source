# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/core/management/commands/collecttemplates.py
# Compiled at: 2016-05-20 23:42:06
from __future__ import unicode_literals
import os, shutil
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from future.builtins import input
from future.builtins import int
from wenlincms.utils.importing import path_for_import

class Command(BaseCommand):
    """
    Copies templates from app templates directories, into the
    project's templates directory. Specify 1 or more app names
    listed in INSTALLED_APPS to copy only the templates for those
    apps. Specifying no apps will copy templates for all apps.
    """
    can_import_settings = True
    option_list = BaseCommand.option_list + (
     make_option(b'--noinput', action=b'store_false', dest=b'interactive', default=True, help=b'Do NOT prompt for input of any kind. Existing templates will be overwritten.'),
     make_option(b'-t', b'--template', dest=b'template', help=b'The template name and relative path of a single template '),
     make_option(b'-a', b'--admin', action=b'store_true', dest=b'admin', default=False, help=b'Include admin templates.'))
    usage = lambda foo, bar: b'usage: %prog [appname1] [appname2] [options] \n' + Command.__doc__.rstrip()

    def handle(self, *apps, **options):
        admin = options.get(b'admin')
        single_template = options.get(b'template')
        verbosity = int(options.get(b'verbosity', 1))
        to_dir = settings.TEMPLATE_DIRS[0]
        templates = []
        if apps:
            not_installed = set(apps) - set(settings.INSTALLED_APPS)
            if not_installed:
                raise CommandError(b'Apps are not in INSTALLED_APPS: ' + (b', ').join(not_installed))
        else:
            apps = [ a for a in settings.INSTALLED_APPS if a.split(b'.')[0] in ('wenlincms',
                                                                                'cartridge')
                   ]
        for app in apps:
            from_dir = os.path.join(path_for_import(app), b'templates')
            if os.path.exists(from_dir):
                for dirpath, dirnames, filenames in os.walk(from_dir):
                    for f in filenames:
                        path = os.path.join(dirpath, f)
                        name = path[len(from_dir) + 1:]
                        if single_template and name != single_template:
                            continue
                        if not admin and name.startswith(b'admin' + os.sep):
                            continue
                        templates.append((name, path, app))

        count = 0
        template_src = {}
        for name, path, app in templates:
            dest = os.path.join(to_dir, name)
            if verbosity >= 2:
                self.stdout.write(b'\nCopying: %s\nFrom:    %s\nTo:      %s\n' % (
                 name, path, dest))
            copy = True
            if options.get(b'interactive') and os.path.exists(dest):
                if name in template_src:
                    prev = b' [copied from %s]' % template_src[name]
                else:
                    prev = b''
                self.stdout.write(b'While copying %s [from %s]:\n' % (
                 name, app))
                self.stdout.write(b'Template exists%s.\n' % prev)
                confirm = input(b'Overwrite?  (yes/no/abort): ')
                while confirm not in ('yes', 'no', 'abort'):
                    confirm = input(b"Please enter either 'yes', 'no' or 'abort': ")

                if confirm == b'abort':
                    self.stdout.write(b'Aborted\n')
                    break
                elif confirm == b'no':
                    self.stdout.write(b'[Skipped]\n')
                    copy = False
            if copy:
                try:
                    os.makedirs(os.path.dirname(dest))
                except OSError:
                    pass

                shutil.copy2(path, dest)
                template_src[name] = app
                count += 1

        if verbosity >= 1:
            s = b's' if count != 1 else b''
            self.stdout.write(b'\nCopied %s template%s\n' % (count, s))