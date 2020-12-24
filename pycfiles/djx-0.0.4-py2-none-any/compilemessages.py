# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/management/commands/compilemessages.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import codecs, glob, os
from django.core.management.base import BaseCommand, CommandError
from django.core.management.utils import find_command, popen_wrapper
from django.utils._os import npath, upath

def has_bom(fn):
    with open(fn, b'rb') as (f):
        sample = f.read(4)
    return sample.startswith((codecs.BOM_UTF8, codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE))


def is_writable(path):
    try:
        with open(path, b'a'):
            os.utime(path, None)
    except (IOError, OSError):
        return False

    return True


class Command(BaseCommand):
    help = b'Compiles .po files to .mo files for use with builtin gettext support.'
    requires_system_checks = False
    leave_locale_alone = True
    program = b'msgfmt'
    program_options = [b'--check-format']

    def add_arguments(self, parser):
        parser.add_argument(b'--locale', b'-l', dest=b'locale', action=b'append', default=[], help=b'Locale(s) to process (e.g. de_AT). Default is to process all. Can be used multiple times.')
        parser.add_argument(b'--exclude', b'-x', dest=b'exclude', action=b'append', default=[], help=b'Locales to exclude. Default is none. Can be used multiple times.')
        parser.add_argument(b'--use-fuzzy', b'-f', dest=b'fuzzy', action=b'store_true', default=False, help=b'Use fuzzy translations.')

    def handle(self, **options):
        locale = options[b'locale']
        exclude = options[b'exclude']
        self.verbosity = options[b'verbosity']
        if options[b'fuzzy']:
            self.program_options = self.program_options + [b'-f']
        if find_command(self.program) is None:
            raise CommandError(b"Can't find %s. Make sure you have GNU gettext tools 0.15 or newer installed." % self.program)
        basedirs = [os.path.join(b'conf', b'locale'), b'locale']
        if os.environ.get(b'DJANGO_SETTINGS_MODULE'):
            from django.conf import settings
            basedirs.extend(upath(path) for path in settings.LOCALE_PATHS)
        for dirpath, dirnames, filenames in os.walk(b'.', topdown=True):
            for dirname in dirnames:
                if dirname == b'locale':
                    basedirs.append(os.path.join(dirpath, dirname))

        basedirs = set(map(os.path.abspath, filter(os.path.isdir, basedirs)))
        if not basedirs:
            raise CommandError(b'This script should be run from the Django Git checkout or your project or app tree, or with the settings module specified.')
        all_locales = []
        for basedir in basedirs:
            locale_dirs = filter(os.path.isdir, glob.glob(b'%s/*' % basedir))
            all_locales.extend(map(os.path.basename, locale_dirs))

        locales = locale or all_locales
        locales = set(locales) - set(exclude)
        for basedir in basedirs:
            if locales:
                dirs = [ os.path.join(basedir, l, b'LC_MESSAGES') for l in locales ]
            else:
                dirs = [
                 basedir]
            locations = []
            for ldir in dirs:
                for dirpath, dirnames, filenames in os.walk(ldir):
                    locations.extend((dirpath, f) for f in filenames if f.endswith(b'.po'))

            if locations:
                self.compile_messages(locations)

        return

    def compile_messages(self, locations):
        """
        Locations is a list of tuples: [(directory, file), ...]
        """
        for i, (dirpath, f) in enumerate(locations):
            if self.verbosity > 0:
                self.stdout.write(b'processing file %s in %s\n' % (f, dirpath))
            po_path = os.path.join(dirpath, f)
            if has_bom(po_path):
                raise CommandError(b'The %s file has a BOM (Byte Order Mark). Django only supports .po files encoded in UTF-8 and without any BOM.' % po_path)
            base_path = os.path.splitext(po_path)[0]
            if i == 0 and not is_writable(npath(base_path + b'.mo')):
                self.stderr.write(b'The po files under %s are in a seemingly not writable location. mo files will not be updated/created.' % dirpath)
                return
            args = [
             self.program] + self.program_options + [
             b'-o', npath(base_path + b'.mo'), npath(base_path + b'.po')]
            output, errors, status = popen_wrapper(args)
            if status:
                if errors:
                    msg = b'Execution of %s failed: %s' % (self.program, errors)
                else:
                    msg = b'Execution of %s failed' % self.program
                raise CommandError(msg)