# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_account_invoice/party.py
# Compiled at: 2019-01-16 09:41:12
# Size of source mod 2**32: 1326 bytes
from trytond.model import fields
from trytond.pool import PoolMeta
__all__ = [
 'Party', 'Address']

class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    no_send_invoice = fields.Boolean('No send invoice', help='If checked, customer invoices will not be set by default to be mailed to contacts.')
    commercial_item = fields.Many2One('party.category', 'Commercial Item')
    commercial_zone = fields.Many2One('party.category', 'Commercial Zone')

    @staticmethod
    def default_no_send_invoice():
        return False


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    @classmethod
    def validate(cls, addresses):
        super(Address, cls).validate(addresses)
        for address in addresses:
            address.check_invoice_type()

    def check_invoice_type(self):
        if self.invoice:
            addresses = self.search([
             (
              'party', '=', self.party.id),
             ('invoice', '=', True),
             (
              'id', '!=', self.id)])
            if addresses:
                self.raise_user_error('invoice_address')