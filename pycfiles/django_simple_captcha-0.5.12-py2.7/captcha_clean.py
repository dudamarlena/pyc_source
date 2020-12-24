# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/captcha/management/commands/captcha_clean.py
# Compiled at: 2016-09-18 03:26:33
from django.core.management.base import BaseCommand
from django.utils import timezone
import sys

class Command(BaseCommand):
    help = 'Clean up expired captcha hashkeys.'

    def handle(self, **options):
        from captcha.models import CaptchaStore
        verbose = int(options.get('verbosity'))
        expired_keys = CaptchaStore.objects.filter(expiration__lte=timezone.now()).count()
        if verbose >= 1:
            print 'Currently %d expired hashkeys' % expired_keys
        try:
            CaptchaStore.remove_expired()
        except:
            if verbose >= 1:
                print 'Unable to delete expired hashkeys.'
            sys.exit(1)

        if verbose >= 1:
            if expired_keys > 0:
                print '%d expired hashkeys removed.' % expired_keys
            else:
                print 'No keys to remove.'