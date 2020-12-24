# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sip\sipclient.py
# Compiled at: 2009-05-31 11:15:46
"""
Created on 2009-5-3

@author: mingqi
"""
import md5, datetime, simplejson as json, urllib, sip, logging
logger = logging.getLogger('sip.sipclient')

class SIPError(Exception):
    """
    The errors of call Alisoft SIP service.
    Attributes
        error_status: error status code
        error_messsage: error messages
    """

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message


class SIPTaobaoBizError(SIPError):
    """
    errors of call taobao's SIP api. It's difference with SIPError.
    This error is business level.
    """
    pass


class SIPClient:

    def __init__(self, app_key, app_secret):
        self.__app_key = app_key
        self.__app_secret = app_secret

    def call_sip(self, api_name, sid=None, **args):
        """
        api_name: the name of calling api
        sid: session id if required.
        format: response format, json or xml. json is default
        """
        sip_args = {}
        sip_args['sip_appkey'] = self.__app_key
        sip_args['sip_apiname'] = api_name
        sip_args['sip_timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sip_args['sip_format'] = 'json'
        if sid:
            sip_args['sip_sessionid'] = sid
        sip_args.update(args)
        sign = self.__app_secret
        for key in sorted(sip_args):
            logger.debug('%s=%s' % (key, sip_args[key]))
            sign = sign + key + sip_args[key]

        sign = md5.new(sign).hexdigest()
        sip_args['sip_sign'] = sign
        url = 'http://sip.alisoft.com/sip/rest?'
        url = url + urllib.urlencode(sip_args)
        logger.debug('url=%s' % url)
        opener = urllib.urlopen(url)
        if not opener:
            raise SIPError(-1, 'Connect to SIP errors')
        sip_status = int(opener.info().getheader('sip_status'))
        if sip_status != 9999:
            raise SIPError(sip_status, opener.info().getheader('sip_error_message'))
        r = opener.read()
        logger.debug('response=%s' % r)
        return r


class TaobaoSIPClient(SIPClient):

    def call_sip(self, api_name, sid=None, **args):
        _args = {}
        _args.update(args)
        _args['v'] = '1.0'
        _args['format'] = 'json'
        _res = SIPClient.call_sip(self, api_name, **_args)
        _json_res = json.loads(_res)
        if _json_res.has_key('error_rsp'):
            _error_code = int(_json_res['error_rsp']['code'])
            _error_msg = _json_res['error_rsp']['msg']
            if _error_code < 500:
                raise SIPError(_error_code, _error_msg)
            raise SIPTaobaoBizError(_error_code, _error_msg)
        return _res


if __name__ == '__main__':
    tb_proxy = TaobaoSIPClient(sip.APP_CODE, sip.APP_SECRET)
    _args = {'fields': 'cid,parent_cid,is_parent,name,status,sort_order', 'datetime': '2009-03-01 00:00:00'}
    print tb_proxy.call_sip('taobao.itemcats.get.v2', None, **_args)