# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/views.py
# Compiled at: 2018-03-26 19:55:32
# Size of source mod 2**32: 5893 bytes
from django.template import Template, Context
from django.views.generic import FormView
from django.test import RequestFactory
from django.utils.translation import ugettext_lazy as _
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from easy_pdf.views import PDFTemplateView
import re, logging
from danceschool.core.models import Invoice
from danceschool.core.constants import getConstant, INVOICE_VALIDATION_STR
from danceschool.core.mixins import EmailRecipientMixin
from danceschool.core.helpers import emailErrorMessage
from .forms import VoucherCustomizationForm
from .models import Voucher
logger = logging.getLogger(__name__)

class GiftCertificateCustomizeView(FormView):
    template_name = 'cms/forms/display_form_classbased.html'
    form_class = VoucherCustomizationForm

    def dispatch(self, request, *args, **kwargs):
        """
        Check that a valid Invoice ID has been passed in session data,
        and that said invoice is marked as paid.
        """
        paymentSession = request.session.get(INVOICE_VALIDATION_STR, {})
        self.invoiceID = paymentSession.get('invoiceID')
        self.amount = paymentSession.get('amount', 0)
        self.success_url = paymentSession.get('success_url', reverse('registration'))
        try:
            i = Invoice.objects.get(id=self.invoiceID)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest(_('Invalid invoice information passed.'))

        if i.unpaid or i.amountPaid != self.amount:
            return HttpResponseBadRequest(_('Passed invoice is not paid.'))
        return super(GiftCertificateCustomizeView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Create the gift certificate voucher with the indicated information and send
        the email as directed.
        """
        emailTo = form.cleaned_data.get('emailTo')
        emailType = form.cleaned_data.get('emailType')
        recipientName = form.cleaned_data.get('recipientName')
        fromName = form.cleaned_data.get('fromName')
        message = form.cleaned_data.get('message')
        logger.info('Processing gift certificate.')
        try:
            voucher = Voucher.create_new_code(prefix='GC_', name=_('Gift certificate: %s%s for %s' % (getConstant('general__currencySymbol'), self.amount, emailTo)), category=getConstant('vouchers__giftCertCategory'), originalAmount=self.amount, singleUse=False, forFirstTimeCustomersOnly=False, expirationDate=None)
        except IntegrityError:
            logger.error('Error creating gift certificate voucher for Invoice #%s' % self.invoiceId)
            emailErrorMessage(_('Gift certificate transaction not completed'), self.invoiceId)

        template = getConstant('vouchers__giftCertTemplate')
        rf = RequestFactory()
        pdf_request = rf.get('/')
        pdf_kwargs = {'currencySymbol': getConstant('general__currencySymbol'), 
         'businessName': getConstant('contact__businessName'), 
         'certificateAmount': voucher.originalAmount, 
         'certificateCode': voucher.voucherId, 
         'certificateMessage': message, 
         'recipientName': recipientName, 
         'fromName': fromName}
        if recipientName:
            pdf_kwargs.update({})
        attachment = GiftCertificatePDFView(request=pdf_request).get(request=pdf_request, **pdf_kwargs).content or None
        if attachment:
            attachment_name = 'gift_certificate.pdf'
        else:
            attachment_name = None
        email_class = EmailRecipientMixin()
        email_class.email_recipient(subject=template.subject, content=template.content, send_html=template.send_html, html_content=template.html_content, from_address=template.defaultFromAddress, from_name=template.defaultFromName, cc=template.defaultCC, to=emailTo, currencySymbol=getConstant('general__currencySymbol'), businessName=getConstant('contact__businessName'), certificateAmount=voucher.originalAmount, certificateCode=voucher.voucherId, certificateMessage=message, recipientName=recipientName, fromName=fromName, emailType=emailType, recipient_name=recipientName, attachment_name=attachment_name, attachment=attachment)
        self.request.session.pop(INVOICE_VALIDATION_STR, None)
        return HttpResponseRedirect(self.get_success_url())


class GiftCertificatePDFView(PDFTemplateView):
    template_name = 'vouchers/pdf/giftcertificate_template.html'

    def get_context_data(self, **kwargs):
        context = super(GiftCertificatePDFView, self).get_context_data(**kwargs)
        template = getConstant('vouchers__giftCertPDFTemplate')
        content = re.sub('\\{%\\s*((extends)|(load)|(debug)|(include)|(ssi))\\s+.*?\\s*%\\}', '', template.content)
        t = Template(content)
        rendered_content = t.render(Context(context))
        context.update({'header': template.subject, 
         'content': rendered_content})
        return context