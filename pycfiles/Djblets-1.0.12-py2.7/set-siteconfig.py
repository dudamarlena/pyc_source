# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/siteconfig/management/commands/set-siteconfig.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.core.management.base import CommandError
from django.utils import six
from django.utils.translation import ugettext as _
from djblets.siteconfig.models import SiteConfiguration
from djblets.util.compat.django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Sets a setting in the site configuration.

    This cannot create new settings. It can only set existing ones.
    """

    def add_arguments(self, parser):
        """Add arguments to the command.

        Args:
            parser (object):
                The argument parser to add to.
        """
        parser.add_argument(b'--key', action=b'store', dest=b'key', help=_(b'The existing key to modify (dot-separated)'))
        parser.add_argument(b'--value', action=b'store', dest=b'value', help=_(b'The value to store'))

    def handle(self, *args, **options):
        siteconfig = SiteConfiguration.objects.get_current()
        key = options[b'key']
        value = options[b'value']
        if key is None:
            raise CommandError(_(b'--key must be provided'))
        if value is None:
            raise CommandError(_(b'--value must be provided'))
        path = key.split(b'.')
        node = siteconfig.settings
        valid_key = True
        for item in path[:-1]:
            try:
                node = node[item]
            except KeyError:
                valid_key = False

        if valid_key:
            key_basename = path[(-1)]
            if key_basename not in node:
                valid_key = False
        if not valid_key:
            raise CommandError(_(b"'%s' is not a valid settings key") % key)
        stored_value = node[key_basename]
        value_type = type(stored_value)
        if value_type not in (six.text_type, six.binary_type, int, bool,
         type(None)):
            raise CommandError(_(b'Cannot set %s keys') % value_type.__name__)
        try:
            if value_type is bool:
                if value not in ('1', '0', 'True', 'true', 'False', 'false'):
                    raise TypeError
                else:
                    value = value in ('1', 'True', 'true')
            elif stored_value is None:
                defaults = siteconfig.get_defaults()
                value_type = type(defaults.get(key_basename, b''))
            if value == b'null':
                norm_value = None
            elif value == b'\\null':
                norm_value = b'null'
            else:
                norm_value = value_type(value)
        except TypeError:
            raise CommandError(_(b"'%(value)s' is not a valid %(type)s") % {b'value': value, 
               b'type': value_type.__name__})

        self.stdout.write(_(b"Setting '%(key)s' to %(value)s") % {b'key': key, 
           b'value': norm_value})
        node[key_basename] = norm_value
        siteconfig.save()
        return