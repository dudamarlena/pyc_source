# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: nexmo/libpynexmo/nexmomessage.py
# Compiled at: 2013-07-01 09:48:45
import urllib, urllib2, urlparse, json
BASEURL = 'https://rest.nexmo.com'

class NexmoMessage:

    def __init__(self, details):
        self.sms = details
        self.sms.setdefault('type', 'text')
        self.sms.setdefault('server', BASEURL)
        self.sms.setdefault('reqtype', 'json')
        self.smstypes = [
         'text',
         'binary',
         'wappush',
         'vcal',
         'vcard',
         'unicode']
        self.apireqs = [
         'balance',
         'pricing',
         'numbers']
        self.reqtypes = [
         'json',
         'xml']

    def url_fix(self, s, charset='utf-8'):
        if isinstance(s, unicode):
            s = s.encode(charset, 'ignore')
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')
        qs = urllib.quote_plus(qs, ':&=')
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

    def set_text_info(self, text):
        self.sms['type'] = 'text'
        self.sms['text'] = text

    def set_bin_info(self, body, udh):
        self.sms['type'] = 'binary'
        self.sms['body'] = body
        self.sms['udh'] = udh

    def set_wappush_info(self, title, url, validity=False):
        self.sms['type'] = 'wappush'
        self.sms['title'] = title
        self.sms['url'] = url
        self.sms['validity'] = validity

    def set_vcal_info(self, vcal):
        self.sms['type'] = 'vcal'
        self.sms['vcal'] = vcal

    def set_vcard_info(self, vcard):
        self.sms['type'] = 'vcard'
        self.sms['vcard'] = vcard

    def check_sms(self):
        """ http://www.nexmo.com/documentation/index.html#request
            http://www.nexmo.com/documentation/api/ """
        if not self.sms.get('api_key') or not self.sms.get('api_secret'):
            return False
        if self.sms['type'] in self.apireqs:
            if self.sms['type'] == 'balance' or self.sms['type'] == 'numbers':
                return True
            if self.sms['type'] == 'pricing' and not self.sms.get('country'):
                return False
            return True
        if self.sms['type'] not in self.smstypes:
            return False
        if self.sms['type'] == 'text' and not self.sms.get('text'):
            return False
        if self.sms['type'] == 'binary' and (not self.sms.get('body') or not self.sms.get('udh')):
            return False
        if self.sms['type'] == 'wappush' and (not self.sms.get('title') or not self.sms.get('url')):
            return False
        if self.sms['type'] == 'vcal' and not self.sms.get('vcal'):
            return False
        if self.sms['type'] == 'vcard' and not self.sms.get('vcard'):
            return False
        if not self.sms.get('from') or not self.sms.get('to'):
            return False
        return True

    def build_request(self):
        if not self.check_sms():
            return False
        else:
            if self.sms['type'] in self.apireqs:
                if self.sms['type'] == 'balance':
                    self.request = '%s/account/get-balance/%s/%s' % (BASEURL,
                     self.sms['api_key'], self.sms['api_secret'])
                elif self.sms['type'] == 'pricing':
                    self.request = '%s/account/get-pricing/outbound/%s/%s/%s' % (
                     BASEURL, self.sms['api_key'], self.sms['api_secret'],
                     self.sms['country'])
                elif self.sms['type'] == 'numbers':
                    self.request = '%s/account/numbers/%s/%s' % (BASEURL,
                     self.sms['api_key'], self.sms['api_secret'])
                return self.request
            if self.sms['reqtype'] not in self.reqtypes:
                return False
            params = self.sms.copy()
            params.pop('reqtype')
            params.pop('server')
            server = '%s/sms/%s' % (BASEURL, self.sms['reqtype'])
            self.request = server + '?' + urllib.urlencode(params)
            return self.request

        return False

    def get_details(self):
        return self.sms

    def send_request(self):
        if not self.build_request():
            return False
        if self.sms['reqtype'] == 'json':
            return self.send_request_json(self.request)
        if self.sms['reqtype'] == 'xml':
            return self.send_request_xml(self.request)

    def send_request_json(self, request):
        url = request
        req = urllib2.Request(url=url)
        req.add_header('Accept', 'application/json')
        try:
            return json.load(urllib2.urlopen(req))
        except ValueError:
            return False

    def send_request_xml(self, request):
        return 'XML request not implemented yet.'