# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/abhishekram/Documents/work/Research/pyAS2/pyas2_dev/pyas2/management/commands/sendas2message.py
# Compiled at: 2019-03-20 01:39:18
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from pyas2 import models
from pyas2 import as2lib
from pyas2 import as2utils
from pyas2 import pyas2init
import traceback, email.utils, shutil, time, os, sys

class Command(BaseCommand):
    help = _('Send an as2 message to your trading partner')
    args = '<organization_as2name partner_as2name path_to_payload>'

    def add_arguments(self, parser):
        parser.add_argument('organization_as2name', type=str)
        parser.add_argument('partner_as2name', type=str)
        parser.add_argument('path_to_payload', type=str)
        parser.add_argument('--delete', action='store_true', dest='delete', default=False, help=_('Delete source file after processing'))

    def handle(self, *args, **options):
        try:
            org = models.Organization.objects.get(as2_name=options['organization_as2name'])
        except models.Organization.DoesNotExist:
            raise CommandError(_('Organization "%s" does not exist' % options['organization_as2name']))

        try:
            partner = models.Partner.objects.get(as2_name=options['partner_as2name'])
        except models.Partner.DoesNotExist:
            raise CommandError(_('Partner "%s" does not exist' % options['partner_as2name']))

        if not os.path.isfile(options['path_to_payload']):
            raise CommandError(_('Payload at location "%s" does not exist' % options['path_to_payload']))
        if options['delete'] and not os.access(options['path_to_payload'], os.W_OK):
            raise CommandError('Insufficient file permission for payload %s' % options['path_to_payload'])
        output_dir = as2utils.join(pyas2init.gsettings['payload_send_store'], time.strftime('%Y%m%d'))
        as2utils.dirshouldbethere(output_dir)
        outfile = as2utils.join(output_dir, os.path.basename(options['path_to_payload']))
        shutil.copy2(options['path_to_payload'], outfile)
        if options['delete']:
            os.remove(options['path_to_payload'])
        payload = models.Payload.objects.create(name=os.path.basename(options['path_to_payload']), file=outfile, content_type=partner.content_type)
        message = models.Message.objects.create(message_id=email.utils.make_msgid().strip('<>'), partner=partner, organization=org, direction='OUT', status='IP', payload=payload)
        try:
            payload = as2lib.build_message(message)
            as2lib.send_message(message, payload)
        except Exception:
            message.status = 'E'
            txt = traceback.format_exc(None).decode('utf-8', 'ignore')
            message.adv_status = _('Failed to send message, error:\n%(txt)s') % {'txt': txt}
            pyas2init.logger.error(message.adv_status)
            models.Log.objects.create(message=message, status='E', text=message.adv_status)
            message.save()
            as2utils.senderrorreport(message, message.adv_status)
            sys.exit(2)

        sys.exit(0)
        return