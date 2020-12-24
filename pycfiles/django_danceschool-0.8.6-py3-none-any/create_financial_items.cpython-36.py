# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/financial/management/commands/create_financial_items.py
# Compiled at: 2019-04-02 17:22:31
# Size of source mod 2**32: 1491 bytes
from django.core.management.base import BaseCommand
from danceschool.financial.helpers import createExpenseItemsForEvents, createExpenseItemsForVenueRental, createRevenueItemsForRegistrations
from danceschool.core.constants import getConstant

class Command(BaseCommand):
    help = 'Create expense items for recurring expenses and generate revenue items for registrations'

    def handle(self, *args, **options):
        if getConstant('financial__autoGenerateExpensesEventStaff'):
            self.stdout.write('Generating expense items for event staff...')
            createExpenseItemsForEvents()
            self.stdout.write('...done.')
        else:
            self.stdout.write('Generation of expense items for event staff is not enabled.')
        if getConstant('financial__autoGenerateExpensesVenueRental'):
            self.stdout.write('Generating expense items for venue rentals...')
            createExpenseItemsForVenueRental()
            self.stdout.write('...done.')
        else:
            self.stdout.write('Generation of expense items for venue rental is not enabled.')
        if getConstant('financial__autoGenerateRevenueRegistrations'):
            self.stdout.write('Generating revenue items for registrations...')
            createRevenueItemsForRegistrations()
            self.stdout.write('...done.')
        else:
            self.stdout.write('Generation of revnue items for registrations is not enabled.')