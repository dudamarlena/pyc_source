# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/UniversalAnalytics/Tracker.py
# Compiled at: 2014-12-03 14:59:50
from urllib2 import urlopen, build_opener, install_opener
from urllib2 import Request, HTTPSHandler
from urllib2 import URLError, HTTPError
from urllib import urlencode
import random, datetime, time, uuid, hashlib, socket

def generate_uuid(basedata=None):
    """ Provides a _random_ UUID with no input, or a UUID4-format MD5 checksum of any input data provided """
    if basedata is None:
        return str(uuid.uuid4())
    else:
        if isinstance(basedata, basestring):
            checksum = hashlib.md5(basedata).hexdigest()
            return '%8s-%4s-%4s-%4s-%12s' % (checksum[0:8], checksum[8:12], checksum[12:16], checksum[16:20], checksum[20:32])
        return


class Time(datetime.datetime):
    """ Wrappers and convenience methods for processing various time representations """

    @classmethod
    def from_unix(cls, seconds, milliseconds=0):
        """ Produce a full |datetime.datetime| object from a Unix timestamp """
        base = list(time.gmtime(seconds))[0:6]
        base.append(milliseconds * 1000)
        return cls(*base)

    @classmethod
    def to_unix(cls, timestamp):
        """ Wrapper over time module to produce Unix epoch time as a float """
        if not isinstance(timestamp, datetime.datetime):
            raise TypeError, 'Time.milliseconds expects a datetime object'
        base = time.mktime(timestamp.timetuple())
        return base

    @classmethod
    def milliseconds_offset(cls, timestamp, now=None):
        """ Offset time (in milliseconds) from a |datetime.datetime| object to now """
        if isinstance(timestamp, (int, float)):
            base = timestamp
        else:
            base = cls.to_unix(timestamp)
            base = base + timestamp.microsecond / 1000000
        if now is None:
            now = time.time()
        return (now - base) * 1000


class HTTPRequest(object):
    """ URL Construction and request handling abstraction.
        This is not intended to be used outside this module.

        Automates mapping of persistent state (i.e. query parameters)
        onto transcient datasets for each query.
    """
    endpoint = 'https://www.google-analytics.com/collect'

    @staticmethod
    def debug():
        """ Activate debugging on urllib2 """
        handler = HTTPSHandler(debuglevel=1)
        opener = build_opener(handler)
        install_opener(opener)

    def __init__(self, user_agent=None, *args, **opts):
        self.user_agent = user_agent or 'Analytics Pros - Universal Analytics (Python)'

    @classmethod
    def fixUTF8(cls, data):
        """ Convert all strings to UTF-8 """
        for key in data:
            if isinstance(data[key], basestring):
                data[key] = data[key].encode('utf-8')

        return data

    def send(self, data):
        request = Request(self.endpoint + '?' + urlencode(self.fixUTF8(data)), headers={'User-Agent': self.user_agent})
        self.open(request)

    def open(self, request):
        try:
            return urlopen(request)
        except HTTPError as e:
            return False
        except URLError as e:
            self.cache_request(request)
            return False

    def cache_request(self, request):
        pass


class HTTPPost(HTTPRequest):

    def send(self, data):
        request = Request(self.endpoint, data=urlencode(self.fixUTF8(data)), headers={'User-Agent': self.user_agent})
        self.open(request)


class Tracker(object):
    """ Primary tracking interface for Universal Analytics """
    params = None
    parameter_alias = {}
    valid_hittypes = ('pageview', 'event', 'social', 'screenview', 'transaction', 'item',
                      'exception', 'timing')

    @classmethod
    def alias(cls, typemap, base, *names):
        """ Declare an alternate (humane) name for a measurement protocol parameter """
        cls.parameter_alias[base] = (
         typemap, base)
        for i in names:
            cls.parameter_alias[i] = (
             typemap, base)

    @classmethod
    def coerceParameter(cls, name, value=None):
        if isinstance(name, basestring) and name[0] == '&':
            return (name[1:], str(value))
        if name in cls.parameter_alias:
            typecast, param_name = cls.parameter_alias.get(name)
            return (
             param_name, typecast(value))
        raise KeyError, ('Parameter "{0}" is not recognized').format(name)

    def payload(self, data):
        for key, value in data.iteritems():
            try:
                yield self.coerceParameter(key, value)
            except KeyError:
                continue

    option_sequence = {'pageview': [(basestring, 'dp')], 'event': [
               (
                basestring, 'ec'), (basestring, 'ea'), (basestring, 'el'), (int, 'ev')], 
       'social': [
                (
                 basestring, 'sn'), (basestring, 'sa'), (basestring, 'st')], 
       'timing': [
                (
                 basestring, 'utc'), (basestring, 'utv'), (basestring, 'utt'), (basestring, 'utl')]}

    @classmethod
    def consume_options(cls, data, hittype, args):
        """ Interpret sequential arguments related to known hittypes based on declared structures """
        opt_position = 0
        data['t'] = hittype
        if hittype in cls.option_sequence:
            for expected_type, optname in cls.option_sequence[hittype]:
                if opt_position < len(args) and isinstance(args[opt_position], expected_type):
                    data[optname] = args[opt_position]
                opt_position += 1

    @classmethod
    def hittime(cls, timestamp=None, age=None, milliseconds=None):
        """ Returns an integer represeting the milliseconds offset for a given hit (relative to now) """
        if isinstance(timestamp, (int, float)):
            return int(Time.milliseconds_offset(Time.from_unix(timestamp, milliseconds=milliseconds)))
        if isinstance(timestamp, datetime.datetime):
            return int(Time.milliseconds_offset(timestamp))
        if isinstance(age, (int, float)):
            return int(age * 1000) + (milliseconds or 0)

    @property
    def account(self):
        return self.params.get('tid', None)

    def __init__(self, account, name=None, client_id=None, hash_client_id=False, user_id=None, user_agent=None, use_post=True):
        if use_post is False:
            self.http = HTTPRequest(user_agent=user_agent)
        else:
            self.http = HTTPPost(user_agent=user_agent)
        self.params = {'v': 1, 'tid': account}
        if client_id is None:
            client_id = generate_uuid()
        self.params['cid'] = client_id
        self.hash_client_id = hash_client_id
        if user_id is not None:
            self.params['uid'] = user_id
        return

    def set_timestamp(self, data):
        """ Interpret time-related options, apply queue-time parameter as needed """
        if 'hittime' in data:
            data['qt'] = self.hittime(timestamp=data.pop('hittime', None))
        if 'hitage' in data:
            data['qt'] = self.hittime(age=data.pop('hitage', None))
        return

    def send(self, hittype, *args, **data):
        """ Transmit HTTP requests to Google Analytics using the measurement protocol """
        if hittype not in self.valid_hittypes:
            raise KeyError(('Unsupported Universal Analytics Hit Type: {0}').format(repr(hittype)))
        self.set_timestamp(data)
        self.consume_options(data, hittype, args)
        for item in args:
            if isinstance(item, dict):
                for key, val in self.payload(item):
                    data[key] = val

        for k, v in self.params.iteritems():
            if k not in data:
                data[k] = v

        data = dict(self.payload(data))
        if self.hash_client_id:
            data['cid'] = generate_uuid(data['cid'])
        self.http.send(data)

    def set(self, name, value=None):
        if isinstance(name, dict):
            for key, value in name.iteritems():
                try:
                    param, value = self.coerceParameter(key, value)
                    self.params[param] = value
                except KeyError:
                    pass

        elif isinstance(name, basestring):
            try:
                param, value = self.coerceParameter(name, value)
                self.params[param] = value
            except KeyError:
                pass

    def __getitem__(self, name):
        param, value = self.coerceParameter(name, None)
        return self.params.get(param, None)

    def __setitem__(self, name, value):
        param, value = self.coerceParameter(name, value)
        self.params[param] = value

    def __delitem__(self, name):
        param, value = self.coerceParameter(name, None)
        if param in self.params:
            del self.params[param]
        return


def safe_unicode(obj):
    """ Safe convertion to the Unicode string version of the object """
    try:
        return unicode(obj)
    except UnicodeDecodeError:
        return obj.decode('utf-8')


MAX_CUSTOM_DEFINITIONS = 200
MAX_EC_LISTS = 11
MAX_EC_PRODUCTS = 11
MAX_EC_PROMOTIONS = 11
Tracker.alias(int, 'v', 'protocol-version')
Tracker.alias(safe_unicode, 'cid', 'client-id', 'clientId', 'clientid')
Tracker.alias(safe_unicode, 'tid', 'trackingId', 'account')
Tracker.alias(safe_unicode, 'uid', 'user-id', 'userId', 'userid')
Tracker.alias(safe_unicode, 'uip', 'user-ip', 'userIp', 'ipaddr')
Tracker.alias(safe_unicode, 'ua', 'userAgent', 'userAgentOverride', 'user-agent')
Tracker.alias(safe_unicode, 'dp', 'page', 'path')
Tracker.alias(safe_unicode, 'dt', 'title', 'pagetitle', 'pageTitlepage-title')
Tracker.alias(safe_unicode, 'dl', 'location')
Tracker.alias(safe_unicode, 'dh', 'hostname')
Tracker.alias(safe_unicode, 'sc', 'sessioncontrol', 'session-control', 'sessionControl')
Tracker.alias(safe_unicode, 'dr', 'referrer', 'referer')
Tracker.alias(int, 'qt', 'queueTime', 'queue-time')
Tracker.alias(safe_unicode, 't', 'hitType', 'hittype')
Tracker.alias(int, 'aip', 'anonymizeIp', 'anonIp', 'anonymize-ip')
Tracker.alias(safe_unicode, 'cn', 'campaign', 'campaignName', 'campaign-name')
Tracker.alias(safe_unicode, 'cs', 'source', 'campaignSource', 'campaign-source')
Tracker.alias(safe_unicode, 'cm', 'medium', 'campaignMedium', 'campaign-medium')
Tracker.alias(safe_unicode, 'ck', 'keyword', 'campaignKeyword', 'campaign-keyword')
Tracker.alias(safe_unicode, 'cc', 'content', 'campaignContent', 'campaign-content')
Tracker.alias(safe_unicode, 'ci', 'campaignId', 'campaignID', 'campaign-id')
Tracker.alias(safe_unicode, 'sr', 'screenResolution', 'screen-resolution', 'resolution')
Tracker.alias(safe_unicode, 'vp', 'viewport', 'viewportSize', 'viewport-size')
Tracker.alias(safe_unicode, 'de', 'encoding', 'documentEncoding', 'document-encoding')
Tracker.alias(int, 'sd', 'colors', 'screenColors', 'screen-colors')
Tracker.alias(safe_unicode, 'ul', 'language', 'user-language', 'userLanguage')
Tracker.alias(safe_unicode, 'an', 'appName', 'app-name', 'app')
Tracker.alias(safe_unicode, 'cd', 'contentDescription', 'screenName', 'screen-name', 'content-description')
Tracker.alias(safe_unicode, 'av', 'appVersion', 'app-version', 'version')
Tracker.alias(safe_unicode, 'aid', 'appID', 'appId', 'application-id', 'app-id', 'applicationId')
Tracker.alias(safe_unicode, 'aiid', 'appInstallerId', 'app-installer-id')
Tracker.alias(safe_unicode, 'ta', 'affiliation', 'transactionAffiliation', 'transaction-affiliation')
Tracker.alias(safe_unicode, 'ti', 'transaction', 'transactionId', 'transaction-id')
Tracker.alias(float, 'tr', 'revenue', 'transactionRevenue', 'transaction-revenue')
Tracker.alias(float, 'ts', 'shipping', 'transactionShipping', 'transaction-shipping')
Tracker.alias(float, 'tt', 'tax', 'transactionTax', 'transaction-tax')
Tracker.alias(safe_unicode, 'cu', 'currency', 'transactionCurrency', 'transaction-currency')
Tracker.alias(safe_unicode, 'in', 'item-name', 'itemName')
Tracker.alias(float, 'ip', 'item-price', 'itemPrice')
Tracker.alias(float, 'iq', 'item-quantity', 'itemQuantity')
Tracker.alias(safe_unicode, 'ic', 'item-code', 'sku', 'itemCode')
Tracker.alias(safe_unicode, 'iv', 'item-variation', 'item-category', 'itemCategory', 'itemVariation')
Tracker.alias(safe_unicode, 'ec', 'event-category', 'eventCategory', 'category')
Tracker.alias(safe_unicode, 'ea', 'event-action', 'eventAction', 'action')
Tracker.alias(safe_unicode, 'el', 'event-label', 'eventLabel', 'label')
Tracker.alias(int, 'ev', 'event-value', 'eventValue', 'value')
Tracker.alias(int, 'ni', 'noninteractive', 'nonInteractive', 'noninteraction', 'nonInteraction')
Tracker.alias(safe_unicode, 'sa', 'social-action', 'socialAction')
Tracker.alias(safe_unicode, 'sn', 'social-network', 'socialNetwork')
Tracker.alias(safe_unicode, 'st', 'social-target', 'socialTarget')
Tracker.alias(safe_unicode, 'exd', 'exception-description', 'exceptionDescription', 'exDescription')
Tracker.alias(int, 'exf', 'exception-fatal', 'exceptionFatal', 'exFatal')
Tracker.alias(safe_unicode, 'utc', 'timingCategory', 'timing-category')
Tracker.alias(safe_unicode, 'utv', 'timingVariable', 'timing-variable')
Tracker.alias(float, 'utt', 'time', 'timingTime', 'timing-time')
Tracker.alias(safe_unicode, 'utl', 'timingLabel', 'timing-label')
Tracker.alias(float, 'dns', 'timingDNS', 'timing-dns')
Tracker.alias(float, 'pdt', 'timingPageLoad', 'timing-page-load')
Tracker.alias(float, 'rrt', 'timingRedirect', 'timing-redirect')
Tracker.alias(safe_unicode, 'tcp', 'timingTCPConnect', 'timing-tcp-connect')
Tracker.alias(safe_unicode, 'srt', 'timingServerResponse', 'timing-server-response')
for i in range(0, 200):
    Tracker.alias(safe_unicode, ('cd{0}').format(i), ('dimension{0}').format(i))
    Tracker.alias(int, ('cm{0}').format(i), ('metric{0}').format(i))

Tracker.alias(str, 'pa')
Tracker.alias(str, 'tcc')
Tracker.alias(unicode, 'pal')
Tracker.alias(int, 'cos')
Tracker.alias(str, 'col')
Tracker.alias(str, 'promoa')
for product_index in range(1, MAX_EC_PRODUCTS):
    Tracker.alias(str, ('pr{0}id').format(product_index))
    Tracker.alias(unicode, ('pr{0}nm').format(product_index))
    Tracker.alias(unicode, ('pr{0}br').format(product_index))
    Tracker.alias(unicode, ('pr{0}ca').format(product_index))
    Tracker.alias(unicode, ('pr{0}va').format(product_index))
    Tracker.alias(str, ('pr{0}pr').format(product_index))
    Tracker.alias(int, ('pr{0}qt').format(product_index))
    Tracker.alias(str, ('pr{0}cc').format(product_index))
    Tracker.alias(int, ('pr{0}ps').format(product_index))
    for custom_index in range(MAX_CUSTOM_DEFINITIONS):
        Tracker.alias(str, ('pr{0}cd{1}').format(product_index, custom_index))
        Tracker.alias(int, ('pr{0}cm{1}').format(product_index, custom_index))

    for list_index in range(1, MAX_EC_LISTS):
        Tracker.alias(str, ('il{0}pi{1}id').format(list_index, product_index))
        Tracker.alias(unicode, ('il{0}pi{1}nm').format(list_index, product_index))
        Tracker.alias(unicode, ('il{0}pi{1}br').format(list_index, product_index))
        Tracker.alias(unicode, ('il{0}pi{1}ca').format(list_index, product_index))
        Tracker.alias(unicode, ('il{0}pi{1}va').format(list_index, product_index))
        Tracker.alias(int, ('il{0}pi{1}ps').format(list_index, product_index))
        Tracker.alias(int, ('il{0}pi{1}pr').format(list_index, product_index))
        for custom_index in range(MAX_CUSTOM_DEFINITIONS):
            Tracker.alias(str, ('il{0}pi{1}cd{2}').format(list_index, product_index, custom_index))
            Tracker.alias(int, ('il{0}pi{1}cm{2}').format(list_index, product_index, custom_index))

for list_index in range(1, MAX_EC_LISTS):
    Tracker.alias(unicode, ('il{0}nm').format(list_index))

for promotion_index in range(1, MAX_EC_PROMOTIONS):
    Tracker.alias(str, ('promo{0}id').format(promotion_index))
    Tracker.alias(unicode, ('promo{0}nm').format(promotion_index))
    Tracker.alias(str, ('promo{0}cr').format(promotion_index))
    Tracker.alias(str, ('promo{0}ps').format(promotion_index))

def create(account, *args, **kwargs):
    return Tracker(account, *args, **kwargs)