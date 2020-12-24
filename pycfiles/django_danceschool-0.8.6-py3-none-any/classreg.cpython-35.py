# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/classreg.py
# Compiled at: 2018-06-22 17:13:11
# Size of source mod 2**32: 30487 bytes
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.views.generic import FormView, RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from braces.views import UserFormKwargsMixin
import logging
from allauth.account.forms import LoginForm, SignupForm
from datetime import timedelta
import json
from .models import Event, Series, PublicEvent, TemporaryRegistration, TemporaryEventRegistration, Invoice, CashPaymentRecord
from .forms import ClassChoiceForm, RegistrationContactForm, DoorAmountForm
from .constants import getConstant, REG_VALIDATION_STR
from .signals import post_student_info, request_discounts, apply_discount, apply_addons, apply_price_adjustments
from .mixins import FinancialContextMixin
logger = logging.getLogger(__name__)

class RegistrationOfflineView(TemplateView):
    __doc__ = '\n    If registration is offline, just say so.\n    '
    template_name = 'core/registration/registration_offline.html'


class ClassRegistrationReferralView(RedirectView):

    def get(self, request, *args, **kwargs):
        self.url = reverse('registration')
        voucher_id = kwargs.pop('voucher_id', None)
        marketing_id = kwargs.pop('marketing_id', None)
        if marketing_id or voucher_id:
            regSession = self.request.session.get(REG_VALIDATION_STR, {})
            regSession['voucher_id'] = voucher_id or regSession.get('voucher_id', None)
            regSession['marketing_id'] = marketing_id or regSession.get('marketing_id', None)
            self.request.session[REG_VALIDATION_STR] = regSession
        return super(ClassRegistrationReferralView, self).get(request, *args, **kwargs)


class ClassRegistrationView(FinancialContextMixin, FormView):
    __doc__ = '\n    This is the main view that is called from the class registration page.y\n    '
    form_class = ClassChoiceForm
    template_name = 'core/registration/event_registration.html'

    def get(self, request, *args, **kwargs):
        """ Check that registration is online before proceeding """
        regonline = getConstant('registration__registrationEnabled')
        if not regonline:
            return HttpResponseRedirect(reverse('registrationOffline'))
        return super(ClassRegistrationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Add the event and series listing data """
        context = self.get_listing()
        context['showDescriptionRule'] = getConstant('registration__showDescriptionRule') or 'all'
        context.update(kwargs)
        return super(ClassRegistrationView, self).get_context_data(**context)

    def get_form_kwargs(self, **kwargs):
        """ Tell the form which fields to render """
        kwargs = super(ClassRegistrationView, self).get_form_kwargs(**kwargs)
        kwargs['user'] = self.request.user if hasattr(self.request, 'user') else None
        listing = self.get_listing()
        kwargs.update({'openEvents': listing['openEvents'], 
         'closedEvents': listing['closedEvents']})
        return kwargs

    def form_valid(self, form):
        """
        If the form is valid, pass its contents on to the next view.  In order to permit the registration
        form to be overridden flexibly, but without permitting storage of arbitrary data keys that could
        lead to potential security issues, a form class for this view can optionally specify a list of
        keys that are permitted.  If no such list is specified as instance.permitted_event_keys, then
        the default list are used.
        """
        regSession = self.request.session.get(REG_VALIDATION_STR, {})
        expiry = timezone.now() + timedelta(minutes=getConstant('registration__sessionExpiryMinutes'))
        permitted_keys = getattr(form, 'permitted_event_keys', ['role'])
        try:
            event_listing = {int(key.split('_')[(-1)]):{k:v for k, v in json.loads(value[0]).items() if k in permitted_keys} for key, value in form.cleaned_data.items() if 'event' in key and value}
            non_event_listing = {key:value for key, value in form.cleaned_data.items() if 'event' not in key if 'event' not in key}
        except (ValueError, TypeError) as e:
            form.add_error(None, ValidationError(_('Invalid event information passed.'), code='invalid'))
            return super(ClassRegistrationView, self).form_invalid(form)

        associated_events = Event.objects.filter(id__in=[k for k in event_listing.keys()])
        if self.request.user.is_authenticated:
            submissionUser = self.request.user
        else:
            submissionUser = None
        reg = TemporaryRegistration(submissionUser=submissionUser, dateTime=timezone.now(), payAtDoor=non_event_listing.pop('payAtDoor', False), expirationDate=expiry)
        reg.data = non_event_listing or {}
        if regSession.get('marketing_id'):
            reg.data.update({'marketing_id': regSession.pop('marketing_id', None)})
        eventRegs = []
        grossPrice = 0
        for key, value in event_listing.items():
            this_event = associated_events.get(id=key)
            this_role_id = value.get('role', None) if 'role' in permitted_keys else None
            soldOut = this_event.soldOutForRole(role=this_role_id, includeTemporaryRegs=True)
            if soldOut:
                if self.request.user.has_perm('core.override_register_soldout'):
                    messages.warning(self.request, _("Registration for '%s' is sold out. Based on your user permission level, " % this_event.name + 'you may proceed with registration.  However, if you do not wish to exceed ' + 'the listed capacity of the event, please do not proceed.'))
                else:
                    form.add_error(None, ValidationError(_('Registration for "%s" is tentatively sold out while others complete their registration.  Please try again later.' % this_event.name), code='invalid'))
                    return super(ClassRegistrationView, self).form_invalid(form)
                dropInList = [int(k.split('_')[(-1)]) for k, v in value.items() if k.startswith('dropin_') and v is True]
                logger.debug('Creating temporary event registration for: %s' % key)
                if len(dropInList) > 0:
                    tr = TemporaryEventRegistration(event=this_event, dropIn=True, price=this_event.getBasePrice(dropIns=len(dropInList)))
                else:
                    tr = TemporaryEventRegistration(event=this_event, price=this_event.getBasePrice(payAtDoor=reg.payAtDoor), role_id=this_role_id)
                tr.data = {k:v for k, v in value.items() if k in permitted_keys and k != 'role'}
                eventRegs.append(tr)
                grossPrice += tr.price

        reg.priceWithDiscount = grossPrice
        reg.save()
        for er in eventRegs:
            er.registration = reg
            er.save()

        regSession['temporaryRegistrationId'] = reg.id
        regSession['temporaryRegistrationExpiry'] = expiry.strftime('%Y-%m-%dT%H:%M:%S%z')
        self.request.session[REG_VALIDATION_STR] = regSession
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('getStudentInfo')

    def get_allEvents(self):
        """
        Splitting this method out to get the set of events to filter allows
        one to subclass for different subsets of events without copying other
        logic
        """
        if not hasattr(self, 'allEvents'):
            timeFilters = {'endTime__gte': timezone.now()}
            if getConstant('registration__displayLimitDays') or 0 > 0:
                timeFilters['startTime__lte'] = timezone.now() + timedelta(days=getConstant('registration__displayLimitDays'))
            self.allEvents = Event.objects.filter(**timeFilters).filter(Q(instance_of=PublicEvent) | Q(instance_of=Series)).exclude(Q(status=Event.RegStatus.hidden) | Q(status=Event.RegStatus.regHidden) | Q(status=Event.RegStatus.linkOnly)).order_by('year', 'month', 'startTime')
        return self.allEvents

    def get_listing(self):
        """
        This function gets all of the information that we need to either render or
        validate the form.  It is structured to avoid duplicate DB queries
        """
        if not hasattr(self, 'listing'):
            allEvents = self.get_allEvents()
            openEvents = allEvents.filter(registrationOpen=True)
            closedEvents = allEvents.filter(registrationOpen=False)
            publicEvents = allEvents.instance_of(PublicEvent)
            allSeries = allEvents.instance_of(Series)
            self.listing = {'allEvents': allEvents, 
             'openEvents': openEvents, 
             'closedEvents': closedEvents, 
             'publicEvents': publicEvents, 
             'allSeries': allSeries, 
             'regOpenEvents': publicEvents.filter(registrationOpen=True).filter(Q(publicevent__category__isnull=True) | Q(publicevent__category__separateOnRegistrationPage=False)), 
             
             'regClosedEvents': publicEvents.filter(registrationOpen=False).filter(Q(publicevent__category__isnull=True) | Q(publicevent__category__separateOnRegistrationPage=False)), 
             
             'categorySeparateEvents': publicEvents.filter(publicevent__category__separateOnRegistrationPage=True).order_by('publicevent__category'), 
             
             'regOpenSeries': allSeries.filter(registrationOpen=True).filter(Q(series__category__isnull=True) | Q(series__category__separateOnRegistrationPage=False)), 
             
             'regClosedSeries': allSeries.filter(registrationOpen=False).filter(Q(series__category__isnull=True) | Q(series__category__separateOnRegistrationPage=False)), 
             
             'categorySeparateSeries': allSeries.filter(series__category__separateOnRegistrationPage=True).order_by('series__category')}
        return self.listing


class SingleClassRegistrationView(ClassRegistrationView):
    __doc__ = '\n    This view is called only via a link, and it allows a person to register for a single\n    class without seeing all other classes.\n    '
    template_name = 'core/registration/single_event_registration.html'

    def get_allEvents(self):
        try:
            self.allEvents = Event.objects.filter(uuid=self.kwargs.get('uuid', '')).exclude(status=Event.RegStatus.hidden)
        except ValueError:
            raise Http404()

        if not self.allEvents:
            raise Http404()
        return self.allEvents


class RegistrationSummaryView(UserFormKwargsMixin, FinancialContextMixin, FormView):
    template_name = 'core/registration_summary.html'
    form_class = DoorAmountForm

    def dispatch(self, request, *args, **kwargs):
        """ Always check that the temporary registration has not expired """
        regSession = self.request.session.get(REG_VALIDATION_STR, {})
        if not regSession:
            return HttpResponseRedirect(reverse('registration'))
        try:
            reg = TemporaryRegistration.objects.get(id=self.request.session[REG_VALIDATION_STR].get('temporaryRegistrationId'))
        except ObjectDoesNotExist:
            messages.error(request, _('Invalid registration identifier passed to summary view.'))
            return HttpResponseRedirect(reverse('registration'))

        expiry = parse_datetime(self.request.session[REG_VALIDATION_STR].get('temporaryRegistrationExpiry', ''))
        if not expiry or expiry < timezone.now():
            messages.info(request, _('Your registration session has expired. Please try again.'))
            return HttpResponseRedirect(reverse('registration'))
        kwargs.update({'reg': reg})
        return super(RegistrationSummaryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        reg = kwargs.get('reg')
        initial_price = sum([x.price for x in reg.temporaryeventregistration_set.all()])
        discount_responses = request_discounts.send(sender=RegistrationSummaryView, registration=reg)
        discount_responses = [x[1] for x in discount_responses if len(x) > 1 and x[1]]
        discount_codes = []
        discounted_total = initial_price
        total_discount_amount = 0
        try:
            if discount_responses:
                discount_responses.sort(key=lambda k: min([getattr(x, 'net_price', initial_price) for x in k.items] + [initial_price]) if k and hasattr(k, 'items') else initial_price)
                discount_codes = getattr(discount_responses[0], 'items', [])
                if discount_codes:
                    discounted_total = min([getattr(x, 'net_price', initial_price) for x in discount_codes]) + getattr(discount_responses[0], 'ineligible_total', 0)
                    total_discount_amount = initial_price - discounted_total
        except (IndexError, TypeError) as e:
            logger.error('Error in applying discount responses: %s' % e)

        for discount in discount_codes:
            apply_discount.send(sender=RegistrationSummaryView, discount=discount.code, discount_amount=discount.discount_amount, registration=reg)

        addon_responses = apply_addons.send(sender=RegistrationSummaryView, registration=reg)
        addons = []
        for response in addon_responses:
            try:
                if response[1]:
                    addons += list(response[1])
            except (IndexError, TypeError) as e:
                logger.error('Error in applying addons: %s' % e)

        adjustment_responses = apply_price_adjustments.send(sender=RegistrationSummaryView, registration=reg, initial_price=discounted_total)
        adjustment_list = []
        adjustment_amount = 0
        for response in adjustment_responses:
            adjustment_list += response[1][0]
            adjustment_amount += response[1][1]

        total = discounted_total - adjustment_amount
        reg.priceWithDiscount = total
        reg.save()
        regSession = request.session[REG_VALIDATION_STR]
        regSession['temp_reg_id'] = reg.id
        if discount_codes:
            regSession['discount_codes'] = [(x.code.name, x.code.pk, x.discount_amount) for x in discount_codes]
        regSession['total_discount_amount'] = total_discount_amount
        regSession['addons'] = addons
        regSession['voucher_names'] = adjustment_list
        regSession['total_voucher_amount'] = adjustment_amount
        request.session[REG_VALIDATION_STR] = regSession
        return super(RegistrationSummaryView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ Pass the initial kwargs, then update with the needed registration info. """
        context_data = super(RegistrationSummaryView, self).get_context_data(**kwargs)
        regSession = self.request.session[REG_VALIDATION_STR]
        reg_id = regSession['temp_reg_id']
        reg = TemporaryRegistration.objects.get(id=reg_id)
        discount_codes = regSession.get('discount_codes', None)
        discount_amount = regSession.get('total_discount_amount', 0)
        voucher_names = regSession.get('voucher_names', [])
        total_voucher_amount = regSession.get('total_voucher_amount', 0)
        addons = regSession.get('addons', [])
        if reg.priceWithDiscount == 0:
            new_invoice = Invoice.get_or_create_from_registration(reg, status=Invoice.PaymentStatus.paid)
            new_invoice.processPayment(0, 0, forceFinalize=True)
            isFree = True
        else:
            isFree = False
        context_data.update({'registration': reg, 
         'totalPrice': reg.totalPrice, 
         'subtotal': reg.priceWithDiscount, 
         'taxes': reg.addTaxes, 
         'netPrice': reg.priceWithDiscountAndTaxes, 
         'addonItems': addons, 
         'discount_codes': discount_codes, 
         'discount_code_amount': discount_amount, 
         'voucher_names': voucher_names, 
         'total_voucher_amount': total_voucher_amount, 
         'total_discount_amount': discount_amount + total_voucher_amount, 
         'currencyCode': getConstant('general__currencyCode'), 
         'payAtDoor': reg.payAtDoor, 
         'is_free': isFree})
        if self.request.user:
            door_permission = self.request.user.has_perm('core.accept_door_payments')
            invoice_permission = self.request.user.has_perm('core.send_invoices')
            if door_permission or invoice_permission:
                context_data['form'] = DoorAmountForm(user=self.request.user, doorPortion=door_permission, invoicePortion=invoice_permission, payerEmail=reg.email, discountAmount=max(reg.totalPrice - reg.priceWithDiscount, 0))
        return context_data

    def form_valid(self, form):
        regSession = self.request.session[REG_VALIDATION_STR]
        reg_id = regSession['temp_reg_id']
        tr = TemporaryRegistration.objects.get(id=reg_id)
        new_invoice = Invoice.get_or_create_from_registration(tr)
        if form.cleaned_data.get('paid'):
            logger.debug('Form is marked paid. Preparing to process payment.')
            amount = form.cleaned_data['amountPaid']
            submissionUser = form.cleaned_data.get('submissionUser')
            receivedBy = form.cleaned_data.get('receivedBy')
            payerEmail = form.cleaned_data.get('cashPayerEmail')
            this_cash_payment = CashPaymentRecord.objects.create(invoice=new_invoice, submissionUser=submissionUser, amount=amount, payerEmail=payerEmail, collectedByUser=receivedBy, status=CashPaymentRecord.PaymentStatus.needsCollection)
            new_invoice.processPayment(amount, 0, paidOnline=False, methodName='Cash', methodTxn='CASHPAYMENT_%s' % this_cash_payment.recordId, submissionUser=submissionUser, collectedByUser=receivedBy, status=Invoice.PaymentStatus.needsCollection, forceFinalize=True)
        elif form.cleaned_data.get('invoiceSent'):
            payerEmail = form.cleaned_data['invoicePayerEmail']
            tr.expirationDate = tr.lastEndTime
            tr.save()
            new_invoice.sendNotification(payerEmail=payerEmail, newRegistration=True)
        return HttpResponseRedirect(reverse('registration'))


class StudentInfoView(FormView):
    __doc__ = '\n    This page displays a preliminary total of what is being signed up for, and it also\n    collects customer information, either by having the user sign in in an Ajax view, or by\n    manually entering the information.  When the form is submitted, the view just passes\n    everything into the session data and continues on to the next step.  To add additional\n    fields to this form, or to modify existing fields, just override the form class to\n    a form that adds/modifies whatever fields you would like.\n    '
    form_class = RegistrationContactForm
    template_name = 'core/student_info_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Require session data to be set to proceed, otherwise go back to step 1.
        Because they have the same expiration date, this also implies that the
        TemporaryRegistration object is not yet expired.
        """
        if REG_VALIDATION_STR not in request.session:
            return HttpResponseRedirect(reverse('registration'))
            try:
                self.temporaryRegistration = TemporaryRegistration.objects.get(id=self.request.session[REG_VALIDATION_STR].get('temporaryRegistrationId'))
            except ObjectDoesNotExist:
                messages.error(request, _('Invalid registration identifier passed to sign-up form.'))
                return HttpResponseRedirect(reverse('registration'))

            expiry = parse_datetime(self.request.session[REG_VALIDATION_STR].get('temporaryRegistrationExpiry', ''))
            if not expiry or expiry < timezone.now():
                messages.info(request, _('Your registration session has expired. Please try again.'))
                return HttpResponseRedirect(reverse('registration'))
            return super(StudentInfoView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super(StudentInfoView, self).get_context_data(**kwargs)
        reg = self.temporaryRegistration
        initial_price = sum([x.price for x in reg.temporaryeventregistration_set.all()])
        discount_responses = request_discounts.send(sender=StudentInfoView, registration=reg)
        discount_responses = [x[1] for x in discount_responses if len(x) > 1 and x[1]]
        discount_codes = []
        discounted_total = initial_price
        total_discount_amount = 0
        try:
            if discount_responses:
                discount_responses.sort(key=lambda k: min([getattr(x, 'net_price', initial_price) for x in k.items] + [initial_price]) if k and hasattr(k, 'items') else initial_price)
                discount_codes = getattr(discount_responses[0], 'items', [])
                if discount_codes:
                    discounted_total = min([getattr(x, 'net_price', initial_price) for x in discount_codes]) + getattr(discount_responses[0], 'ineligible_total', 0)
                    total_discount_amount = initial_price - discounted_total
        except (IndexError, TypeError) as e:
            logger.error('Error in applying discount responses: %s' % e)

        addon_responses = apply_addons.send(sender=StudentInfoView, registration=reg)
        addons = []
        for response in addon_responses:
            try:
                if response[1]:
                    addons += list(response[1])
            except (IndexError, TypeError) as e:
                logger.error('Error in applying addons: %s' % e)

        context_data.update({'reg': reg, 
         'payAtDoor': reg.payAtDoor, 
         'currencySymbol': getConstant('general__currencySymbol'), 
         'subtotal': initial_price, 
         'addonItems': addons, 
         'discount_codes': discount_codes, 
         'discount_code_amount': total_discount_amount, 
         'discounted_subtotal': discounted_total})
        if reg.payAtDoor or self.request.user.is_authenticated or not getConstant('registration__allowAjaxSignin'):
            context_data['show_ajax_form'] = False
        else:
            context_data.update({'show_ajax_form': True, 
             'login_form': LoginForm(), 
             'signup_form': SignupForm()})
        return context_data

    def get_form_kwargs(self, **kwargs):
        """ Pass along the request data to the form """
        kwargs = super(StudentInfoView, self).get_form_kwargs(**kwargs)
        kwargs['request'] = self.request
        kwargs['registration'] = self.temporaryRegistration
        return kwargs

    def get_success_url(self):
        return reverse('showRegSummary')

    def form_valid(self, form):
        """
        Even if this form is valid, the handlers for this form may have added messages
        to the request.  In that case, then the page should be handled as if the form
        were invalid.  Otherwise, update the session data with the form data and then
        move to the next view
        """
        reg = self.temporaryRegistration
        expiry = timezone.now() + timedelta(minutes=getConstant('registration__sessionExpiryMinutes'))
        self.request.session[REG_VALIDATION_STR]['temporaryRegistrationExpiry'] = expiry.strftime('%Y-%m-%dT%H:%M:%S%z')
        self.request.session.modified = True
        reg.expirationDate = expiry
        reg.firstName = form.cleaned_data.pop('firstName')
        reg.lastName = form.cleaned_data.pop('lastName')
        reg.email = form.cleaned_data.pop('email')
        reg.phone = form.cleaned_data.pop('phone', None)
        reg.student = form.cleaned_data.pop('student', False)
        reg.comments = form.cleaned_data.pop('comments', None)
        reg.howHeardAboutUs = form.cleaned_data.pop('howHeardAboutUs', None)
        reg.data.update(form.cleaned_data)
        reg.save()
        post_student_info.send(sender=StudentInfoView, registration=reg)
        return HttpResponseRedirect(self.get_success_url())