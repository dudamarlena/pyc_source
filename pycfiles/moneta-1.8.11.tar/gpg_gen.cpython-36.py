# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/repository/management/commands/gpg_gen.py
# Compiled at: 2018-01-20 07:36:53
# Size of source mod 2**32: 5918 bytes
import os, pwd, re, stat
from argparse import ArgumentParser
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from moneta.repository.signing import get_gpg
__author__ = 'flanker'
if settings.ADMINS:
    if len(settings.ADMINS[0]) == 2:
        default_email = settings.ADMINS[0][1]
else:
    default_email = 'moneta@19pouces.net'
GPG = get_gpg()

class Command(BaseCommand):
    args = '<generate|show|export>'
    help = 'command=generate: Create a new GPG key\n    command=show: Show existing GPG keys\n    command=export: export GPG key'

    def add_arguments(self, parser):
        assert isinstance(parser, ArgumentParser)
        (parser.add_argument('gpg_command', action='store', default=None, choices=['generate', 'show', 'export']),)
        (
         parser.add_argument('--type', action='store', default='RSA', help='Key type, RSA (default) or DSA.', choices=('RSA',
                                                                                                              'DSA')),)
        (
         parser.add_argument('--length', action='store', default=2048, help='Key length (default 2048).', type=int),)
        (parser.add_argument('--name', action='store', default='Moneta GNUPG key', help='Name of the key'),)
        (parser.add_argument('--email', action='store', default=default_email, help='Email address for the user.'),)
        (
         parser.add_argument('--years', action='store', default='10y', help='Expiration date, in number of years (like "10y") or days (like "10d").'),)
        (
         parser.add_argument('--absent', action='store_true', default=False,
           help='Generate keys only when no key already exists.'),)
        (
         parser.add_argument('--onlyid', action='store_true', default=False, help='Only display the ID of the keys (that is the ID expected in the config gile).'),)

    def handle(self, *args, **options):
        command = options['gpg_command']
        if command == 'generate':
            if options['absent']:
                if len(GPG.list_keys(False)) > 0:
                    return
            else:
                year_matcher = re.match('^(\\d+)y$', options['years'])
                day_matcher = re.match('^(\\d+)d$', options['years'])
                today = datetime.date.today()
                if not year_matcher:
                    if not day_matcher:
                        year_matcher = re.match('^(\\d+)y$', '10y')
                if year_matcher:
                    expire = '%s-%02d-%02d' % (today.year + int(year_matcher.group(1)), today.month, today.day)
                    if today.month == 2:
                        if today.day >= 28:
                            expire = '%s-%02d-%02d' % (today.year + int(year_matcher.group(1)), today.month, 28)
                else:
                    today += datetime.timedelta(days=(int(day_matcher.group(1))))
                    expire = '%s-%02d-%02d' % (today.year, today.month, today.day)
            input_data = 'Key-Type: %s\n' % options['type']
            input_data += 'Key-Length: %d\n' % options['length']
            input_data += 'Name-Real: %s\n' % options['name']
            input_data += 'Expire-Date: %s\n' % expire
            input_data += 'Name-Email: %s\n' % options['email']
            input_data += '%no-protection\n'
            input_data += '%commit\n'
            key = GPG.gen_key(input_data)
            self.stdout.write('Fingerprint %s' % key)
        else:
            if command == 'show':
                if options['onlyid']:
                    for key in GPG.list_keys(False):
                        self.stdout.write(('{keyid}'.format)(**key))

                else:
                    self.stdout.write('Available keys:')
                    for key in GPG.list_keys(False):
                        self.stdout.write(('id (GNUPG_KEYID) : {keyid}, length : {length}, fingerprint : {fingerprint}'.format)(**key))

            else:
                if command == 'export':
                    self.stdout.write(GPG.export_keys(settings.GNUPG_KEYID))
        self.check_rights()

    def check_rights(self):
        os_stat = os.stat(settings.GNUPG_HOME)
        must_apply_rights = self.check_mode(os_stat, stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR)
        must_apply_owners = self.check_owner(os_stat)
        for root, dirnames, filenames in os.walk(settings.GNUPG_HOME):
            for filename in filenames:
                if not 'gpg-agent' in filename:
                    if 'pub' in filename or 'daemon' in filename:
                        pass
                    else:
                        os_stat = os.stat(os.path.join(root, filename))
                        must_apply_rights |= self.check_mode(os_stat, stat.S_IRUSR | stat.S_IWUSR)
                        must_apply_owners |= self.check_owner(os_stat)

            for dirname in dirnames:
                os_stat = os.stat(os.path.join(root, dirname))
                must_apply_rights |= self.check_mode(os_stat, stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR)
                must_apply_owners |= self.check_owner(os_stat)

        if must_apply_rights:
            self.stderr.write('Invalid permissions. You should run the following commands to fix them')
            self.stderr.write('chmod 700 "%s"' % settings.GNUPG_HOME)
            self.stderr.write('find "%s" -type d -exec chmod 700 {} \\;' % settings.GNUPG_HOME)
            self.stderr.write('find "%s" -type f -exec chmod 600 {} \\;' % settings.GNUPG_HOME)
        if must_apply_owners:
            user = pwd.getpwuid(os.getuid())
            if user:
                self.stderr.write('Invalid file owners. You should run the following command to fix them')
                self.stderr.write('chown -R "%s" %s' % (settings.GNUPG_HOME, user[0]))

    @staticmethod
    def check_owner(os_stat):
        return os_stat.st_uid != os.getuid()

    @staticmethod
    def check_mode(os_stat, expected):
        mask = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
        current_mode = os_stat.st_mode & mask
        return bool((current_mode & mask) - (current_mode & expected)) or current_mode & expected != expected