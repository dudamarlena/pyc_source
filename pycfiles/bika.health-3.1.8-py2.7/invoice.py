# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bika/health/browser/analysisrequest/invoice.py
# Compiled at: 2015-11-03 03:53:19
from email.utils import formataddr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bika.lims.utils import encode_header
from bika.lims.browser.analysisrequest import InvoiceCreate as BaseClass
from bika.lims.browser.analysisrequest import InvoiceView as InvoiceViewLIMS
from bika.lims.browser.analysisrequest import InvoicePrintView as InvoicePrintViewLIMS

class InvoiceView(InvoiceViewLIMS):
    """ Rewriting the class to add the insurance company stuff in the invoice.
    """
    template = ViewPageTemplateFile('templates/analysisrequest_invoice.pt')
    content = ViewPageTemplateFile('templates/analysisrequest_invoice_content.pt')

    def __call__(self):
        self.insurancenumber = self.context.Schema()['Patient'].get(self.context).getInsuranceNumber()
        return super(InvoiceView, self).__call__()


class InvoicePrintView(InvoiceView):
    template = ViewPageTemplateFile('templates/analysisrequest_invoice_print.pt')

    def __call__(self):
        return InvoiceView.__call__(self)


class InvoiceCreate(BaseClass):
    """
    A class extension to send the invoice to the insurance company.
    """
    print_template = ViewPageTemplateFile('templates/analysisrequest_invoice_print.pt')
    content = ViewPageTemplateFile('templates/analysisrequest_invoice_content.pt')

    def __call__(self):
        self.insurancenumber = self.context.Schema()['Patient'].get(self.context).getInsuranceNumber()
        BaseClass.__call__(self)

    def emailInvoice(self, templateHTML, to=[]):
        """
        Add the patient's insurance number in the receivers
        :param templateHTML: the html to render. We override it.
        :param to: the list with the receivers. Void in this case.
        """
        sendtoinsurance = self.context.Schema()['Patient'].get(self.context).getInvoiceToInsuranceCompany()
        if sendtoinsurance:
            insurancecompany = self.context.Schema()['Patient'].get(self.context).getInsuranceCompany()
            icaddress = insurancecompany.getEmailAddress()
            icname = insurancecompany.getName()
            if icaddress != '':
                to.append(formataddr((encode_header(icname), icaddress)))
        super(InvoiceCreate, self).emailInvoice(templateHTML, to)