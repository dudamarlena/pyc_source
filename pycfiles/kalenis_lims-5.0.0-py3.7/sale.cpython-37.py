# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_sale/sale.py
# Compiled at: 2019-01-16 09:41:13
# Size of source mod 2**32: 3299 bytes
from trytond.model import fields, ModelView
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction
__all__ = [
 'Sale', 'SaleLoadServicesStart', 'SaleLoadServices']

class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._buttons.update({'load_services': {'invisible': Eval('state') != 'draft'}})

    @classmethod
    @ModelView.button_action('lims_sale.wiz_sale_load_services')
    def load_services(cls, sales):
        pass


class SaleLoadServicesStart(ModelView):
    __doc__ = 'Load Services from Entry'
    __name__ = 'sale.load_services.start'
    entry = fields.Many2One('lims.entry', 'Entry', required=True, domain=[
     (
      'invoice_party', '=', Eval('party'))],
      depends=['party'])
    party = fields.Many2One('party.party', 'Party')


class SaleLoadServices(Wizard):
    __doc__ = 'Load Services from Entry'
    __name__ = 'sale.load_services'
    start = StateView('sale.load_services.start', 'lims_sale.sale_load_services_start_view_form', [
     Button('Cancel', 'end', 'tryton-cancel'),
     Button('Load', 'load', 'tryton-ok', default=True)])
    load = StateTransition()

    def default_start(self, fields):
        Sale = Pool().get('sale.sale')
        sale = Sale(Transaction().context['active_id'])
        return {'party': sale.party.id}

    def transition_load(self):
        pool = Pool()
        Service = pool.get('lims.service')
        SaleLine = pool.get('sale.line')
        sale_id = Transaction().context['active_id']
        sale_services = {}
        with Transaction().set_context(_check_access=False):
            services = Service.search([
             (
              'entry', '=', self.start.entry.id),
             ('fraction.type.invoiceable', '=', True),
             ('fraction.cie_fraction_type', '=', False)])
        for service in services:
            if not service.analysis.product:
                continue
            if service.analysis.id not in sale_services:
                sale_services[service.analysis.id] = {'quantity':0,  'unit':service.analysis.product.default_uom.id, 
                 'product':service.analysis.product.id, 
                 'description':service.analysis.rec_name}
            sale_services[service.analysis.id]['quantity'] += 1

        sale_lines = []
        for service in sale_services.values():
            sale_line = SaleLine(quantity=(service['quantity']),
              unit=(service['unit']),
              product=(service['product']),
              description=(service['description']),
              sale=sale_id)
            sale_line.on_change_product()
            sale_lines.append(sale_line)

        SaleLine.save(sale_lines)
        return 'end'