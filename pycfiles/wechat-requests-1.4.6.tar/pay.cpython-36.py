# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\pay.py
# Compiled at: 2018-05-18 06:19:44
# Size of source mod 2**32: 7126 bytes
import re, time
from copy import copy
from .api import Api
from . import settings
from . import sign
from . import utils
__all__ = [
 'for_merchant', 'build_jspay_params']

class Wxpay(Api):
    IMMUTABLE_FIELDS = frozenset(['_appid', '_mchid', '_signkey'])
    API_BASE_URL = 'https://api.mch.weixin.qq.com/pay/'
    SECAPI_BASE_URL = 'https://api.mch.weixin.qq.com/secapi/pay/'

    def __init__(self, appid, mchid, signkey, client_cert, client_key, sign_type=settings.SIGN_TYPE, **kwargs):
        (super(Wxpay, self).__init__)(**kwargs)
        if appid is None or mchid is None or signkey is None:
            raise ValueError('appid, mchid and signkey can not be None')
        object.__setattr__(self, '_appid', appid)
        object.__setattr__(self, '_mchid', mchid)
        object.__setattr__(self, '_signkey', signkey)
        self.sign_type = sign_type
        if client_cert is not None:
            if client_key is not None:
                self.session.cert = (
                 client_cert, client_key)

    def unifiedorder(self, **kwargs):
        """
        `unifiedorder <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1>`_
        """
        kwargs.setdefault('trade_type', settings.TRADE_TYPE_JSAPI)
        body = (self._build_xml_body)(**kwargs)
        return self.post('unifiedorder', data=body)

    def orderquery(self, transaction_id=None, out_trade_no=None):
        """
        `unifiedorder <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2>`_
        """
        if transaction_id is None:
            if out_trade_no is None:
                raise ValueError('transaction_id and out_trade_no be None both')
        else:
            if transaction_id is not None:
                body = self._build_xml_body(transaction_id=transaction_id)
            else:
                body = self._build_xml_body(out_trade_no=out_trade_no)
        return self.post('orderquery', data=body)

    def closeorder(self, out_trade_no):
        """
        `unifiedorder <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_3>`_
        """
        if out_trade_no is None:
            raise ValueError('out_trade_no can not be None')
        body = self._build_xml_body(out_trade_no=out_trade_no)
        return self.post('closeorder', data=body)

    def refund(self, **kwargs):
        """
        `unifiedorder <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_4>`_
        """
        if all(['transaction_id' not in kwargs, 'out_trade_no' not in kwargs]):
            raise ValueError('transaction_id and out_trade_no be None both')
        body = (self._build_xml_body)(**kwargs)
        return self.post((self._build_secapi_path('refund')), data=body)

    def refundquery(self, refund_id=None, out_refund_no=None, transaction_id=None, out_trade_no=None):
        """
        `unifiedorder <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_5>`_
        """
        kwargs = {}
        if refund_id is not None:
            kwargs['refund_id'] = refund_id
        else:
            if out_refund_no is not None:
                kwargs['out_refund_no'] = out_refund_no
            else:
                if transaction_id is not None:
                    kwargs['transaction_id'] = transaction_id
                else:
                    if out_trade_no is not None:
                        kwargs['out_trade_no'] = out_trade_no
                    else:
                        raise ValueError('refund_id,out_refund_no,transaction_id,out_trade_no')
        body = (self._build_xml_body)(**kwargs)
        return self.post('refundquery', data=body)

    def downloadbill(self, **kwargs):
        raise NotImplementedError()

    def downloadfundflow(self):
        raise NotImplementedError()

    def batchquerycomment(self):
        raise NotImplementedError()

    def _sign(self, params_dict):
        params_dict.setdefault('appid', self._appid)
        params_dict.setdefault('mch_id', self._mchid)
        if 'nonce_str' not in params_dict:
            params_dict['nonce_str'] = sign.random_nonce_str(settings.SIGN_NONCE_STR_LEN)
        return (sign.sign_for_pay)((self._signkey), **params_dict)

    def _build_xml_body(self, **kwargs):
        params = copy(kwargs)
        params['sign'] = self._sign(params)
        body_str = (utils.serialize_dict_to_xml)(**params)
        return body_str.encode(settings.ENCODING)

    def _build_secapi_path(self, api_path):
        uri = '{}/{}'.format(self.SECAPI_BASE_URL, api_path)
        return re.sub('(?<!:)//[/]?', '/', uri)


def for_merchant(appid, mchid, signkey, client_cert=None, client_key=None, **kwargs):
    """API证书获取方式：

    微信商户平台(pay.weixin.qq.com)-->账户设置-->API安全-->下载证书

    Args:
      appid: 微信支付分配的公众账号ID
      mchid: 商户号
      signkey: 微信商户平台(pay.weixin.qq.com)-->账户设置-->API安全-->密钥设置
      client_cert: API证书(apiclient_cert.pem)
      client_key: API证书密钥(apiclient_key.pem)
      kwargs: transport options, 支持timeout, headers

    Returns:
      Wxpay instance

    """
    return Wxpay(appid, mchid, signkey, client_cert, client_key, **kwargs)


def build_jspay_params(paysign_key, appid, prepay_id):
    """build weixin JSApi.chooseWXPay params
    """
    _params = {'nonceStr':sign.random_nonce_str(32), 
     'timeStamp':int(time.time()), 
     'package':'prepay_id={}'.format(prepay_id), 
     'signType':'MD5', 
     'appId':appid}
    _params['paySign'] = (sign.sign_for_pay)(paysign_key, **_params)
    return _params