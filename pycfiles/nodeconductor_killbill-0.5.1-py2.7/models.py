# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_killbill/models.py
# Compiled at: 2016-09-25 09:47:37
from __future__ import unicode_literals
import os, logging, collections, StringIO, xhtml2pdf.pisa as pisa
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.utils.encoding import python_2_unicode_compatible
from nodeconductor.core import models as core_models
from nodeconductor.cost_tracking.models import DefaultPriceListItem
from nodeconductor.logging.loggers import LoggableMixin
from nodeconductor.structure.models import Customer
from .backend import UNIT_PREFIX, KillBillBackend
logger = logging.getLogger(__name__)

@python_2_unicode_compatible
class Invoice(LoggableMixin, core_models.UuidMixin):

    class Permissions(object):
        customer_path = b'customer'

    customer = models.ForeignKey(Customer, related_name=b'killbill_invoices')
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField()
    pdf = models.FileField(upload_to=b'invoices', blank=True, null=True)
    usage_pdf = models.FileField(upload_to=b'invoices', blank=True, null=True)
    backend_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return b'%s %.2f %s' % (self.date, self.amount, self.customer.name)

    def get_log_fields(self):
        return ('uuid', 'customer', 'amount', 'date', 'status')

    def get_billing_backend(self):
        return KillBillBackend(self.customer)

    def get_items(self):
        if self.backend_id:
            backend = self.get_billing_backend()
            return backend.get_invoice_items(self.backend_id)
        else:
            return [
             {b'amount': b'100', 
                b'name': b'storage-1GB'},
             {b'amount': b'7.95', 
                b'name': b'flavor-g1.small1'}]

    def generate_invoice_file_name(self, usage=False):
        name = (b'{}-invoice-{}').format(self.date.strftime(b'%Y-%m-%d'), self.pk)
        if usage:
            name += b'-usage'
        return name + b'.pdf'

    def generate_pdf(self, invoice):
        projects = {}
        for item in invoice[b'items']:
            project = item[b'project']
            resource = b'%s (%s)' % (item[b'resource'], item[b'service'])
            projects.setdefault(project, {b'items': {}, b'amount': 0})
            projects[project][b'amount'] += item[b'amount']
            projects[project][b'items'].setdefault(resource, 0)
            projects[project][b'items'][resource] += item[b'amount']

        number = 0
        projects = collections.OrderedDict(sorted(projects.items()))
        for project in projects:
            resources = []
            for resource, amount in sorted(projects[project][b'items'].items()):
                number += 1
                resources.append((resource, {b'amount': amount, b'number': number}))

            projects[project][b'items'] = collections.OrderedDict(resources)

        if self.pdf is not None:
            self.pdf.delete()
        info = settings.NODECONDUCTOR_KILLBILL.get(b'INVOICE', {})
        logo = info.get(b'logo', None)
        if logo and not logo.startswith(b'/'):
            logo = os.path.join(settings.BASE_DIR, logo)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(render_to_string(b'nodeconductor_killbill/invoice.html', {b'customer': self.customer, 
           b'invoice': invoice, 
           b'projects': projects, 
           b'info': info, 
           b'logo': logo})), result)
        if not pdf.err:
            self.pdf.save(self.generate_invoice_file_name(), ContentFile(result.getvalue()))
            self.save(update_fields=[b'pdf'])
        else:
            logger.error(pdf.err)
        return

    def generate_usage_pdf(self, invoice):
        resources = {}
        pricelist = {p.units.replace(UNIT_PREFIX, b''):p for p in DefaultPriceListItem.objects.all()}
        for item in invoice[b'items']:
            price_item = pricelist.get(item[b'name'])
            if price_item:
                usage = item[b'amount'] / float(price_item.value)
                unit = (b'GB/hour' if price_item.item_type == b'storage' else b'hour') + (b's' if usage > 1 else b'')
                if price_item.item_type == b'storage' and b'MB' in price_item.name:
                    from decimal import Decimal
                    item[b'name'] = price_item.name.replace(b'MB', b'GB')
                    usage /= 1024.0
                    value = price_item.value * Decimal(b'1024.0')
                else:
                    item[b'name'] = price_item.name
                    value = price_item.value
                item[b'usage'] = (b'{:.3f} {} x {:.3f} {}').format(usage, unit, value, item[b'currency'])
            resource = b'%s (%s)' % (item[b'resource'], item[b'service'])
            resources.setdefault(resource, {b'items': [], b'amount': 0})
            resources[resource][b'amount'] += item[b'amount']
            resources[resource][b'items'].append(item)

        resources = collections.OrderedDict(sorted(resources.items()))
        if self.usage_pdf is not None:
            self.usage_pdf.delete()
        info = settings.NODECONDUCTOR_KILLBILL.get(b'INVOICE', {})
        logo = info.get(b'logo', None)
        if logo and not logo.startswith(b'/'):
            logo = os.path.join(settings.BASE_DIR, logo)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(render_to_string(b'nodeconductor_killbill/usage_invoice.html', {b'customer': self.customer, 
           b'invoice': invoice, 
           b'resources': resources, 
           b'logo': logo})), result)
        if not pdf.err:
            self.usage_pdf.save(self.generate_invoice_file_name(usage=True), ContentFile(result.getvalue()))
            self.save(update_fields=[b'usage_pdf'])
        else:
            logger.error(pdf.err)
        return