# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/handlers.py
# Compiled at: 2019-04-03 22:56:33
# Size of source mod 2**32: 6803 bytes
from django.dispatch import receiver
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from danceschool.core.signals import post_student_info, post_registration, apply_price_adjustments, get_customer_data, check_student_info
from danceschool.core.models import Customer, Series
from danceschool.core.constants import getConstant, REG_VALIDATION_STR
import logging
from .models import Voucher, TemporaryVoucherUse, VoucherUse
from .helpers import awardReferrers, ensureReferralVouchersExist
logger = logging.getLogger(__name__)

@receiver(check_student_info)
def checkVoucherCode(sender, **kwargs):
    """
    Check that the given voucher code is valid
    """
    logger.debug('Signal to check RegistrationContactForm handled by vouchers app.')
    formData = kwargs.get('formData', {})
    request = kwargs.get('request', {})
    registration = kwargs.get('registration', None)
    session = getattr(request, 'session', {}).get(REG_VALIDATION_STR, {})
    id = formData.get('gift', '')
    first = formData.get('firstName')
    last = formData.get('lastName')
    email = formData.get('email')
    session.pop('total_voucher_amount', 0)
    session.pop('voucher_names', None)
    session.pop('gift', None)
    if id == '':
        return
    if not getConstant('vouchers__enableVouchers'):
        raise ValidationError({'gift': _('Vouchers are disabled.')})
    if session.get('gift', '') != '':
        raise ValidationError({'gift': _("Can't have more than one voucher")})
    eventids = [x.event.id for x in registration.temporaryeventregistration_set.exclude(dropIn=True)]
    seriess = Series.objects.filter(id__in=eventids)
    obj = Voucher.objects.filter(voucherId=id).first()
    if not obj:
        raise ValidationError({'gift': _('Invalid Voucher Id')})
    else:
        customer = Customer.objects.filter(first_name=first,
          last_name=last,
          email=email).first()
    try:
        obj.validateForCustomerAndSeriess(customer, seriess)
    except ValidationError as e:
        raise ValidationError({'gift': e})


@receiver(post_student_info)
def applyVoucherCodeTemporarily(sender, **kwargs):
    """
    When the core registration system creates a temporary registration with a voucher code,
    the voucher app looks for vouchers that match that code and creates TemporaryVoucherUse
    objects to keep track of the fact that the voucher may be used.
    """
    logger.debug('Signal fired to apply temporary vouchers.')
    reg = kwargs.pop('registration')
    voucherId = reg.data.get('gift', '')
    try:
        voucher = Voucher.objects.get(voucherId=voucherId)
    except ObjectDoesNotExist:
        logger.debug('No applicable vouchers found.')
        return
    else:
        tvu = TemporaryVoucherUse(voucher=voucher, registration=reg, amount=0)
        tvu.save()
        logger.debug('Temporary voucher use object created.')


@receiver(post_student_info)
def applyReferrerVouchersTemporarily(sender, **kwargs):
    """
    Unlike voucher codes which have to be manually supplied, referrer discounts are
    automatically applied here, assuming that the referral program is enabled.
    """
    if not getConstant('referrals__enableReferralProgram'):
        return
    logger.debug('Signal fired to temporarily apply referrer vouchers.')
    reg = kwargs.pop('registration')
    try:
        c = Customer.objects.get(user__email=(reg.email))
        vouchers = c.getReferralVouchers()
    except ObjectDoesNotExist:
        vouchers = None

    if not vouchers:
        logger.debug('No referral vouchers found.')
        return
    for v in vouchers:
        TemporaryVoucherUse(voucher=v, registration=reg, amount=0).save()


@receiver(apply_price_adjustments)
def applyTemporaryVouchers(sender, **kwargs):
    reg = kwargs.get('registration')
    price = kwargs.get('initial_price')
    logger.debug('Signal fired to apply temporary vouchers.')
    referral_cat = getConstant('referrals__referrerCategory')
    tvus = list(reg.temporaryvoucheruse_set.filter(voucher__category=referral_cat)) + list(reg.temporaryvoucheruse_set.exclude(voucher__category=referral_cat))
    if not tvus:
        logger.debug('No applicable vouchers found.')
        return ([], 0)
    else:
        voucher_names = []
        total_voucher_amount = 0
        remaining_price = price
        while remaining_price > 0 and tvus:
            tvu = tvus.pop()
            if tvu.voucher.maxAmountPerUse:
                amount = min(tvu.voucher.amountLeft, tvu.voucher.maxAmountPerUse)
            else:
                amount = tvu.voucher.amountLeft
            amount = min(remaining_price, amount)
            tvu.amount = amount
            tvu.save()
            remaining_price -= amount
            voucher_names += [tvu.voucher.name]
            total_voucher_amount += amount

        return (voucher_names, total_voucher_amount)


@receiver(post_registration)
def applyVoucherCodesFinal(sender, **kwargs):
    """
    Once a registration has been completed, vouchers are used and referrers are awarded
    """
    logger.debug('Signal fired to mark voucher codes as applied.')
    finalReg = kwargs.pop('registration')
    tr = finalReg.temporaryRegistration
    tvus = TemporaryVoucherUse.objects.filter(registration=tr)
    for tvu in tvus:
        vu = VoucherUse(voucher=(tvu.voucher), registration=finalReg, amount=(tvu.amount))
        vu.save()
        if getConstant('referrals__enableReferralProgram'):
            awardReferrers(vu)


@receiver(get_customer_data)
def provideCustomerReferralCode(sender, **kwargs):
    """
    If the vouchers app is installed and referrals are enabled, then the customer's profile page can show their voucher referral code.
    """
    customer = kwargs.pop('customer')
    if getConstant('vouchers__enableVouchers'):
        if getConstant('referrals__enableReferralProgram'):
            vrd = ensureReferralVouchersExist(customer)
            return {'referralVoucherId': vrd.referreeVoucher.voucherId}