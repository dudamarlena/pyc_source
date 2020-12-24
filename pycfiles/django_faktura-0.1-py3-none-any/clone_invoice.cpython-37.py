# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ricco/Projects/SPy/accounting-project/faktura/management/commands/clone_invoice.py
# Compiled at: 2018-12-28 17:46:31
# Size of source mod 2**32: 929 bytes
from django.core.management.base import BaseCommand, CommandError
from faktura.models import Invoice
from faktura.utils import clone_invoice

class Command(BaseCommand):
    help = 'Clone Invoice (in DRAFT state) from existing invoice (any type).'

    def add_arguments(self, parser):
        parser.add_argument('invoices', nargs='+', type=str)

    def handle(self, *args, **options):
        for pk in options['invoices']:
            try:
                invoice = Invoice.objects.get(pk=pk)
            except Invoice.DoesNotExist:
                raise CommandError('Invoice with ID: "%s" does not exist!' % pk)

            try:
                clone_invoice(invoice)
            except ValueError as e:
                try:
                    raise CommandError(e)
                finally:
                    e = None
                    del e

            self.stdout.write(self.style.SUCCESS('Successfully created NEW invoice (in DRAFT state) for existing invoice.'))