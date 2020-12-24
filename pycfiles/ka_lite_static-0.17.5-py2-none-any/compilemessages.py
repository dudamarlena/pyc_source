# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/core/management/commands/compilemessages.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import codecs, os, sys
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils._os import npath

def has_bom(fn):
    with open(fn, b'rb') as (f):
        sample = f.read(4)
    return sample[:3] == b'\ufeff' or sample.startswith(codecs.BOM_UTF16_LE) or sample.startswith(codecs.BOM_UTF16_BE)


def compile_messages(stderr, locale=None):
    basedirs = [os.path.join(b'conf', b'locale'), b'locale']
    if os.environ.get(b'DJANGO_SETTINGS_MODULE'):
        from django.conf import settings
        basedirs.extend(settings.LOCALE_PATHS)
    basedirs = set(map(os.path.abspath, filter(os.path.isdir, basedirs)))
    if not basedirs:
        raise CommandError(b'This script should be run from the Django Git checkout or your project or app tree, or with the settings module specified.')
    for basedir in basedirs:
        if locale:
            basedir = os.path.join(basedir, locale, b'LC_MESSAGES')
        for dirpath, dirnames, filenames in os.walk(basedir):
            for f in filenames:
                if f.endswith(b'.po'):
                    stderr.write(b'processing file %s in %s\n' % (f, dirpath))
                    fn = os.path.join(dirpath, f)
                    if has_bom(fn):
                        raise CommandError(b'The %s file has a BOM (Byte Order Mark). Django only supports .po files encoded in UTF-8 and without any BOM.' % fn)
                    pf = os.path.splitext(fn)[0]
                    os.environ[b'djangocompilemo'] = npath(pf + b'.mo')
                    os.environ[b'djangocompilepo'] = npath(pf + b'.po')
                    if sys.platform == b'win32':
                        cmd = b'msgfmt --check-format -o "%djangocompilemo%" "%djangocompilepo%"'
                    else:
                        cmd = b'msgfmt --check-format -o "$djangocompilemo" "$djangocompilepo"'
                    os.system(cmd)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option(b'--locale', b'-l', dest=b'locale', help=b'The locale to process. Default is to process all.'),)
    help = b'Compiles .po files to .mo files for use with builtin gettext support.'
    requires_model_validation = False
    can_import_settings = False

    def handle(self, **options):
        locale = options.get(b'locale')
        compile_messages(self.stderr, locale=locale)