# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ricco/Projects/SPy/accounting-project/faktura/management/commands/generate_invoice_from_proforma.py
# Compiled at: 2018-12-26 17:50:53
# Size of source mod 2**32: 1864 bytes
import datetime
from django.core.management.base import BaseCommand, CommandError
from faktura.models import Invoice, Item

class Command(BaseCommand):
    help = 'Generate Invoice (in DRAFT state) from existing pro forma invoice.'

    def add_arguments(self, parser):
        parser.add_argument('invoices', nargs='+', type=str)

    def handle(self, *args, **options):
        for invoice in options['invoices']:
            try:
                obj = Invoice.objects.get(pk=invoice)
            except Invoice.DoesNotExist:
                raise CommandError('Invoice with ID: "%s" does not exist!' % invoice)

            if not obj.proforma:
                raise CommandError('Invoice with ID: "%s" is not pro forma invoice!' % invoice)
            obj.pk = None
            obj.number = None
            obj.date_of_issue = datetime.date(2016, 3, 8)
            obj.due_date = datetime.date(2016, 3, 8)
            obj.status = Invoice.FINAL
            obj.proforma = False
            obj.invoice_id = None
            obj.note = 'Paiment form (Forma úhrady): Bank Transfer \nOrder number (Číslo objednávky): 3500004744\n\nSPy o.z. bank account:\n\nBank account: 2300870269/8330\nIBAN: SK48 8330 0000 0023 0087 0269\nSWIFT/BIC: FIOZSKBAXXX\n\nFio banka, a.s., pobočka zahraničnej banky\nNám. SNP 21,\nBRATISLAVA 811 01'
            obj.save()
            for item in Item.objects.filter(invoice=invoice):
                item.pk = None
                item.invoice = obj
                item.save()

            i = Invoice.objects.get(pk=invoice)
            i.invoice_id = obj
            i.save()
            self.stdout.write(self.style.SUCCESS('Successfully created NEW invoice (in DRAFT state) for existing pro forma invoice.'))