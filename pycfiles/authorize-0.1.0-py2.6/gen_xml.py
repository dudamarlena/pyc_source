# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat64/egg/authorize/gen_xml.py
# Compiled at: 2010-07-20 17:10:05
import re, decimal
from xml.etree.cElementTree import fromstring, tostring
from xml.etree.cElementTree import Element, iselement
from authorize import responses
API_SCHEMA = 'https://api.authorize.net/xml/v1/schema/AnetApiSchema.xsd'
API_SCHEMA_NS = 'AnetApi/xml/v1/schema/AnetApiSchema.xsd'
PREFIX = '{AnetApi/xml/v1/schema/AnetApiSchema.xsd}'
INDIVIDUAL = 'individual'
BUSINESS = 'business'
ECHECK_CCD = 'CCD'
ECHECK_PPD = 'PPD'
ECHECK_TEL = 'TEL'
ECHECK_WEB = 'WEB'
BANK = 'bank'
CREDIT_CARD = 'cc'
ECHECK = 'echeck'
DAYS_INTERVAL = 'days'
MONTHS_INTERVAL = 'months'
VALIDATION_NONE = 'none'
VALIDATION_TEST = 'testMode'
VALIDATION_LIVE = 'liveMode'
ACCOUNT_CHECKING = 'checking'
ACCOUNT_SAVINGS = 'savings'
ACCOUNT_BUSINESS_CHECKING = 'businessChecking'
AUTH_ONLY = 'auth_only'
CAPTURE_ONLY = 'capture_only'
AUTH_CAPTURE = 'auth_capture'
CREDIT = 'credit'
PRIOR_AUTH_CAPTURE = 'prior_auth_capture'
VOID = 'void'

class AuthorizeSystemError(Exception):
    """
    I'm a serious kind of exception and I'm raised when something
    went really bad at a lower level than the application level, like
    when Authorize is down or when they return an unparseable response
    """

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        return 'Exception: %s caused by %s' % self.args

    def __repr__(self):
        return 'AuthorizeSystemError%s' % (self.args,)


c = re.compile('([A-Z]+[a-z_]+)')

def convert(arg):
    """
    Convert an object to its xml representation
    """
    if iselement(arg):
        return arg
    if isinstance(arg, dict_accessor):
        try:
            return arg.text_
        except:
            raise Exception('Cannot serialize %s, missing text_ attribute' % (arg,))

    if isinstance(arg, dict):
        return arg
    if isinstance(arg, unicode):
        return arg
    if isinstance(arg, decimal.Decimal):
        return unicode(arg)
    if arg is True:
        return 'true'
    if arg is False:
        return 'false'
    if isinstance(arg, float):
        return unicode(round(arg, 2))
    if isinstance(arg, (int, long)):
        return unicode(arg)
    if isinstance(arg, str):
        raise Exception("'%s' not unicode: can only accept unicode strings" % (arg,))
    raise Exception('Cannot convert %s of type %s' % (arg, type(arg)))


def utf8convert(arg):
    """
    Further extend L{convert} to return UTF-8 strings instead of unicode.
    """
    value = convert(arg)
    if isinstance(value, unicode):
        return value.encode('utf-8')
    return value


class XMLBuilder(object):
    """
    XMLBuilder tries to be slightly clever in order to be easier for
    the programmer. If you try to add arguments that are None they
    won't be added to the output because empty XML tags are not worth
    the bandwidth and actually mean something different than None.
    """

    def __getattr__(self, key):

        def _wrapper_func(*args):
            converted = [ convert(arg) for arg in args if arg is not None ]
            if not converted:
                return
            else:
                el = Element(key)
                settext = False
                setatts = False
                for arg in converted:
                    if iselement(arg):
                        el.append(arg)
                    elif isinstance(arg, basestring):
                        assert not settext, 'cannot set text twice'
                        el.text = arg
                        settext = True
                    elif isinstance(arg, dict):
                        assert not setatts, 'cannot set attributes twice'
                        for (k, v) in arg.iteritems():
                            el.set(k, v)

                        setatts = True
                    else:
                        raise TypeError('unhandled argument type: %s' % type(arg))

                return el

        return _wrapper_func


x = XMLBuilder()

def flatten(tree):
    """
    Return a flattened tree in string format encoded in utf-8
    """
    return tostring(tree, 'utf-8')


def purify(s):
    """
    s is an etree.tag and contains also information on the namespace,
    if that information is present try to remove it, then convert the
    camelCaseTags to underscore_notation_more_python_friendly.
    """
    if s.startswith(PREFIX):
        s = s[len(PREFIX):]
    return ('_').join(atom.lower() for atom in c.split(s) if atom)


class dict_accessor(dict):
    """
    Allow accessing a dictionary content also using dot-notation.
    """

    def __getattr__(self, attr):
        return super(dict_accessor, self).__getitem__(attr)

    def __setattr__(self, attr, value):
        super(dict_accessor, self).__setitem__(attr, value)


def parse_node(node):
    """
    Return a dict_accessor representation of the node.
    """
    new = dict_accessor({})
    if node.text and node.text.strip():
        t = node.text
        if isinstance(t, unicode):
            new['text_'] = t
        else:
            new['text_'] = t.decode('utf-8', 'replace')
    if node.attrib:
        new['attrib_'] = dict_accessor(node.attrib)
    for child in node.getchildren():
        tag = purify(child.tag)
        child = parse_node(child)
        if tag not in new:
            new[tag] = child
        else:
            old = new[tag]
            if not isinstance(old, list):
                new[tag] = [
                 old]
            new[tag].append(child)

    return new


def to_dict(s, error_codes, do_raise=True, delimiter=',', encapsulator='', uniform=False):
    """
    Return a dict_accessor representation of the given string, if raise_
    is True an exception is raised when an error code is present.
    """
    try:
        t = fromstring(s)
    except SyntaxError, e:
        raise AuthorizeSystemError(e, s)

    parsed = dict_accessor(parse_node(t))
    try:
        if isinstance(parsed.messages.message, list):
            return parsed
        code = parsed.messages.message.code.text_
        if uniform:
            parsed.messages.message = [
             parsed.messages.message]
    except KeyError:
        return parsed
    else:
        if code in error_codes:
            if do_raise:
                raise error_codes[code]
        dr = None
        if parsed.get('direct_response') is not None:
            dr = parsed.direct_response.text_
        elif parsed.get('validation_direct_response') is not None:
            dr = parsed.validation_direct_response.text_
        if dr is not None:
            parsed.direct_response = parse_direct_response(dr, delimiter, encapsulator)

    return parsed


m = [
 'code', 'subcode', 'reason_code', 'reason_text', 'auth_code',
 'avs', 'trans_id', 'invoice_number', 'description', 'amount', 'method',
 'trans_type', 'customer_id', 'first_name', 'last_name', 'company',
 'address', 'city', 'state', 'zip', 'country', 'phone', 'fax', 'email',
 'ship_first_name', 'ship_last_name', 'ship_company', 'ship_address',
 'ship_city', 'ship_state', 'ship_zip', 'ship_country', 'tax', 'duty',
 'freight', 'tax_exempt', 'po_number', 'md5_hash', 'ccv',
 'holder_verification']

def parse_direct_response(s, delimiter=',', encapsulator=''):
    """
    Very simple format but made of many fields, the most complex ones
    have the following meanings:

        code:
            see L{responses.aim_codes} for all the codes

        avs:
            see L{responses.avs_codes} for all the codes

        method: CC or ECHECK

        trans_type:
            AUTH_CAPTURE
            AUTH_ONLY
            CAPTURE_ONLY
            CREDIT
            PRIOR_AUTH_CAPTURE
            VOID

        tax_exempt: true, false, T, F, YES, NO, Y, N, 1, 0

        ccv:
            see L{responses.ccv_codes} for all the codes

        holder_verification:
            see L{responses.holder_verification_codes} for all the codes
    """
    if not isinstance(s, unicode):
        s = s.decode('utf-8', 'replace')
    e = encapsulator
    d = delimiter
    v = s.split(e + d + e)
    v[0] = v[0].lstrip(e)
    v[-1] = v[(-1)].rstrip(e)
    if not len(v) >= len(m):
        d = dict_accessor({'error': "Couldn't parse the direct response"})
    else:
        d = dict_accessor(dict(zip(m, v)))
    d.original = s
    return d


def macro(action, login, key, *body):
    """
    Main XML structure re-used by every request.
    """
    return getattr(x, action)({'xmlns': API_SCHEMA_NS}, x.merchantAuthentication(x.name(login), x.transactionKey(key)), *body)


def _address(pre='', kw={}, *extra):
    """
    Basic address components with extension capability.
    """
    return [
     x.firstName(kw.get(pre + 'first_name')),
     x.lastName(kw.get(pre + 'last_name')),
     x.company(kw.get(pre + 'company')),
     x.address(kw.get(pre + 'address')),
     x.city(kw.get(pre + 'city')),
     x.state(kw.get(pre + 'state')),
     x.zip(kw.get(pre + 'zip')),
     x.country(kw.get(pre + 'country'))] + list(extra)


def address(pre='', **kw):
    """
    Simple address with prefixing possibility
    """
    return x.address(*_address(pre, kw))


def address_2(pre='', **kw):
    """
    Extended address with phoneNumber and faxNumber in the same tag
    """
    return x.address(*_address(pre, kw, x.phoneNumber(kw.get(pre + 'phone')), x.faxNumber(kw.get(pre + 'fax'))))


def update_address(**kw):
    return x.address(*_address('ship_', kw, x.phoneNumber(kw.get('ship_phone')), x.faxNumber(kw.get('ship_fax')), x.customerAddressId(kw['customer_address_id'])))


def billTo(**kw):
    return x.billTo(*_address('bill_', kw, x.phoneNumber(kw.get('bill_phone')), x.faxNumber(kw.get('bill_fax'))))


def arbBillTo(**kw):
    kw['bill_first_name']
    kw['bill_last_name']
    return x.billTo(*_address('bill_', kw))


def _shipTo(**kw):
    return _address('ship_', kw, x.phoneNumber(kw.get('ship_phone')), x.faxNumber(kw.get('ship_fax')))


def shipToList(**kw):
    return x.shipToList(*_shipTo(**kw))


def shipTo(**kw):
    return x.shipTo(*_shipTo(**kw))


def payment(**kw):
    profile_type = kw.get('profile_type', CREDIT_CARD)
    if profile_type == CREDIT_CARD:
        return x.payment(x.creditCard(x.cardNumber(kw['card_number']), x.expirationDate(kw['expiration_date'])))
    if profile_type == BANK:
        return x.payment(x.bankAccount(x.accountType(kw.get('account_type')), x.routingNumber(kw['routing_number']), x.accountNumber(kw['account_number']), x.nameOnAccount(kw['name_on_account']), x.echeckType(kw.get('echeck_type')), x.bankName(kw.get('bank_name'))))


def transaction(**kw):
    assert len(kw.get('line_items', [])) <= 30
    content = [
     x.amount(kw['amount']), x.tax(x.amount(kw.get('tax_amount')), x.name(kw.get('tax_name')), x.description(kw.get('tax_descr'))), x.shipping(x.amount(kw.get('ship_amount')), x.name(kw.get('ship_name')), x.name(kw.get('ship_description'))), x.duty(x.amount(kw.get('duty_amount')), x.name(kw.get('duty_name')), x.description(kw.get('duty_description')))] + list(x.lineItems(x.itemId(line.get('item_id')), x.name(line['name']), x.description(line.get('description')), x.quantity(line.get('quantity')), x.unitPrice(line.get('unit_price')), x.taxable(line.get('taxable'))) for line in kw.get('line_items', [])) + [
     x.customerProfileId(kw['customer_profile_id']),
     x.customerPaymentProfileId(kw['customer_payment_profile_id']),
     x.customerAddressId(kw.get('customer_address_id'))]
    ptype = kw.get('profile_type', AUTH_ONLY)
    if ptype in (AUTH_ONLY, CAPTURE_ONLY, AUTH_CAPTURE, CREDIT):
        content += [
         x.order(x.invoiceNumber(kw.get('invoice_number')), x.description(kw.get('description')), x.purchaseOrderNumber(kw.get('purchase_order_number')))]
    if ptype in (AUTH_ONLY, CAPTURE_ONLY, AUTH_CAPTURE):
        content += [
         x.taxExempt(kw.get('tax_exempt', False)),
         x.recurringBilling(kw.get('recurring', False)),
         x.cardCode(kw.get('ccv'))]
    if ptype == AUTH_ONLY:
        profile_type = x.profileTransAuthOnly(*content)
    elif ptype == CAPTURE_ONLY:
        profile_type = x.profileTransCaptureOnly(*(content + [x.approvalCode(kw['approval_code'])]))
    elif ptype == AUTH_CAPTURE:
        profile_type = x.profileTransAuthCapture(*content)
    elif ptype == PRIOR_AUTH_CAPTURE:
        profile_type = x.profileTransPriorAuthCapture(*(content + [x.transId(kw['trans_id'])]))
    elif ptype == CREDIT:
        profile_type = x.profileTransRefund(*(content + [x.transId(kw['trans_id'])]))
    elif ptype == VOID:
        profile_type = x.profileTransVoid(*(content + [x.transId(kw['trans_id'])]))
    else:
        raise Exception('Unsupported profile type: %r' % (ptype,))
    return x.transaction(profile_type)


def paymentProfiles(**kw):
    return x.paymentProfiles(x.customerType(kw.get('customer_type')), billTo(**kw), payment(**kw))


def update_paymentProfile(**kw):
    return x.paymentProfile(x.customerType(kw.get('customer_type')), billTo(**kw), payment(**kw), x.customerPaymentProfileId(kw['customer_payment_profile_id']))


def paymentProfile(**kw):
    return x.paymentProfile(x.customerType(kw.get('customer_type')), billTo(**kw), payment(**kw))


def profile(**kw):
    content = [
     x.merchantCustomerId(kw['customer_id']),
     x.description(kw.get('description')),
     x.email(kw.get('email'))]
    payment_profiles = kw.get('payment_profiles', None)
    if payment_profiles is not None:
        content = content + list(paymentProfiles(**prof) for prof in payment_profiles)
    elif kw.get('card_number') or kw.get('routing_number'):
        content = content + [paymentProfiles(**kw)]
    return x.profile(*(content + [shipToList(**kw)]))


def subscription(**kw):
    trial_occurrences = kw.get('trial_occurrences')
    trial_amount = None
    if trial_occurrences is not None:
        trial_amount = kw['trial_amount']
    return x.subscription(x.name(kw.get('subscription_name')), x.paymentSchedule(x.interval(x.length(kw.get('interval_length')), x.unit(kw.get('interval_unit'))), x.startDate(kw.get('start_date')), x.totalOccurrences(kw.get('total_occurrences', 9999)), x.trialOccurrences(trial_occurrences)), x.amount(kw.get('amount')), x.trialAmount(trial_amount), payment(**kw), x.order(x.invoiceNumber(kw.get('invoice_number')), x.description(kw.get('description'))), x.customer(x.type(kw.get('customer_type')), x.id(kw.get('customer_id')), x.email(kw.get('customer_email')), x.phoneNumber(kw.get('phone')), x.faxNumber(kw.get('fax')), x.driversLicense(x.number(kw.get('driver_number')), x.state(kw.get('driver_state')), x.dateOfBirth(kw.get('driver_birth'))), x.taxId(kw.get('tax_id'))), arbBillTo(**kw), shipTo(**kw))


def base(action, login, key, kw, *main):
    return flatten(macro(action, login, key, x.refId(kw.get('ref_id')), *main))


__doc__ = 'Please refer to http://www.authorize.net/support/CIM_XML_guide.pdf\nfor documentation on the XML protocol implemented here.\n'