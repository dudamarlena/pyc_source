# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/main.py
# Compiled at: 2010-03-24 05:43:08
import sys
from finvoicelib.reader import Reader
from finvoicelib.wrapper import FinvoiceWrapper

def finvoice_info(filename):
    print 'Reading: %s' % filename
    try:
        reader = Reader(filename)
    except Exception, e:
        print 'Fatal error. Cannot continue'
        return
    else:
        msg = reader.messages[0]
        payload = msg.get_payload()
        if not payload:
            print 'No payload!'
        payload.validate()
        print (' Document ').center(71, '=')
        print 'Version: %s' % payload.version
        print
        print 'Errors: %s' % len(payload.get_errors('ERROR'))
        print 'Warnings: %s' % len(payload.get_errors(error_type='WARNING'))
        print
        soap = msg.get_envelope()
        if soap:
            print
            print (' SOAP ENVELOPE ').center(71, '=')
            print
            print 'Sender ID: %s (%s)' % (soap.seller_id,
             soap.seller_intermediator_id)
            print 'Receiver ID: %s (%s)' % (soap.buyer_id,
             soap.buyer_intermediator_id)
        f = FinvoiceWrapper(msg)
        print
        print (' Seller ').center(71, '=')
        payee = f.payee
        print 'Name:\t%s' % (payee.name,)
        print 'Business ID:\t%s' % (payee.business_id,)
        print
        if len(payee.business_id) < 1:
            print 'Invalid payer business id!'
            sys.exit(1)
        print (' Buyer ').center(71, '=')
        payer = f.payer
        print 'Name:\t%s' % (payer.name,)
        print 'Business ID:\t%s' % (payer.business_id,)
        print
        print 'Street:\t%s' % (payer.postal_address.street_name,)
        print 'Town:\t%s' % (payer.postal_address.city,)
        print 'Postal code:\t%s' % (payer.postal_address.postal_code,)
        print 'Country:\t%s' % (payer.postal_address.country,)
        if len(payer.business_id) < 1:
            print 'Invalid payer business id!'
            sys.exit(1)
        print (' Invoice ').center(71, '=')
        invoice = f.invoice
        print 'Type: %s (%s)' % (invoice.typecode, invoice.type_text)
        print 'Date: %s' % invoice.date
        print 'Due date: %s' % invoice.due_date
        print 'Reference: %s' % invoice.reference
        print
        print 'Total (VAT 0%%): %s %s' % (invoice.total_untaxed,
         invoice.total_untaxed_currency)
        print 'Vat: %s %s' % (invoice.vat_amount, invoice.vat_amount_currency)
        print 'Total: %s %s' % (invoice.total_taxed, invoice.total_taxed_currency)
        print
        print (' Rows ').center(71, '=')
        print 'Date       Product         Qty. Unit price Vat        Total'
        print '-' * 71
        for row in f.rows:
            print '%(date)-10s %(name)-15s %(quantity)-04s %(unit_price)-10s %(vat_amount)-10s %(total_taxed)-5s' % row.dict()
            print '-' * 71


def main():
    if len(sys.argv) < 2:
        return
    filename = sys.argv[1]
    print 'Using file: %s' % filename
    finvoice_info(filename)


if __name__ == '__main__':
    main()