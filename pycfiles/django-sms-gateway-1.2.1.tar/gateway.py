# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matt/Development/django-sms-gateway/sms/models/gateway.py
# Compiled at: 2012-11-26 23:50:25
from django.db import models
import jsonfield, urllib, datetime
from django.utils.translation import ugettext as _
import logging, re, unicodedata
from django.conf import settings

class Gateway(models.Model):
    """
    A Gateway is a sending endpoint, and associated authentication info
    that can be used to send and receive messages.
    """
    name = models.CharField(max_length=128, unique=True)
    base_url = models.URLField()
    settings = jsonfield.fields.JSONField(default={}, help_text=_('A JSON Dictionary of key-value pairs that will be used for every message. Authorisation credentials should go in here, for example.'))
    recipient_keyword = models.CharField(max_length=128, help_text=_('The keyword that is used in the request to identify the recipient number.'))
    content_keyword = models.CharField(max_length=128, help_text=_('The keyword that is used in the request to identify the message content.'))
    uuid_keyword = models.CharField(max_length=128, null=True, blank=True, help_text=_('The keyword used in the request for our message reference id.'))
    success_format = models.CharField(max_length=256, null=True, blank=True, help_text=_('A regular expression that parses the response. May contain named groups for "gateway_message_id", "status_message" and "status_code".'))
    error_format = models.CharField(max_length=256, null=True, blank=True, help_text=_('A regular expression that parses an error response. Must contain named group for "status_message".'))
    status_mapping = jsonfield.JSONField(default={}, help_text=_('A mapping of returned status codes to our status choices. These will be used to match the success_format string to Unsent/Sent/Failed/Delivered.'))
    charge_keyword = models.CharField(max_length=128, null=True, blank=True, help_text=_("Used in status updates: data matching this field indicates how many 'credits' this message cost in the gateway"))
    status_msg_id = models.CharField(max_length=128, null=True, blank=True, help_text=_('The field that contains our message reference id (see uuid_keyword, above).'))
    status_status = models.CharField(max_length=128, null=True, blank=True, help_text=_('The field that contains the status code, used by status_mapping.'))
    status_error_code = models.CharField(max_length=128, null=True, blank=True, help_text=_('The field that contains the error code. May be the same value as status_status, if no seperate error code field is used.'))
    status_date = models.CharField(max_length=128, null=True, blank=True, help_text=_('The field that contains the status update date-string. See status_date_format: that is used by this field for parsing.'))
    status_date_format = models.CharField(max_length=128, null=True, blank=True, help_text=_('Python datetime formatting code representing the format this gateway uses for delivery time reporting. Leaving this blank means that a unix-style timestamp is used.'))
    reply_content = models.CharField(max_length=128, null=True, blank=True)
    reply_sender = models.CharField(max_length=128, null=True, blank=True)
    reply_date = models.CharField(max_length=128, null=True, blank=True)
    reply_date_format = models.CharField(max_length=128, null=True, blank=True, default='%Y-%m-%d %H:%M:%S')
    check_number_url = models.CharField(max_length=256, null=True, blank=True, help_text=_('The URL that can be used to check availability of sending to a number'))
    check_number_field = models.CharField(max_length=65, null=True, blank=True, help_text=_('The keyword that contains the number to check'))
    check_number_response_format = models.CharField(max_length=256, null=True, blank=True, help_text=_('A regular expression that parses the response. Keys: status, charge'))
    check_number_status_mapping = jsonfield.JSONField(null=True, blank=True)
    query_balance_url = models.CharField(max_length=256, null=True, blank=True, help_text=_('The url path that queries for balance'))
    query_balance_params = jsonfield.fields.JSONField(default=[])
    query_balance_response_format = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        app_label = 'sms'

    def __unicode__(self):
        return self.name

    def send(self, message):
        """
        Use this gateway to send a message.
        
        If ``djcelery`` is installed, then we assume they have set up the
        ``celeryd`` server, and we queue for delivery. Otherwise, we will
        send in-process.
        
        .. note::
            It is strongly recommended to run this out of process, 
            especially if you are sending as part of an HttpRequest, as this
            could take ~5 seconds per message that is to be sent.
        """
        if 'djcelery' in settings.INSTALLED_APPS:
            import sms.tasks
            sms.tasks.SendMessage.delay(message.pk, self.pk)
        else:
            self._send(message)

    def _send--- This code section failed: ---

 L. 130         0  LOAD_FAST             1  'message'
                3  LOAD_ATTR             0  'status'
                6  LOAD_CONST               'Unsent'
                9  COMPARE_OP            2  ==
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Re-sending SMS Messages not yet supported.'
               21  RAISE_VARARGS_2       2  None

 L. 133        24  LOAD_FAST             0  'self'
               27  LOAD_FAST             1  'message'
               30  STORE_ATTR            2  'gateway'

 L. 135        33  BUILD_MAP_0           0  None
               36  STORE_FAST            2  'raw_data'

 L. 136        39  LOAD_FAST             0  'self'
               42  LOAD_ATTR             3  'settings'
               45  POP_JUMP_IF_FALSE    67  'to 67'

 L. 137        48  LOAD_FAST             2  'raw_data'
               51  LOAD_ATTR             4  'update'
               54  LOAD_FAST             0  'self'
               57  LOAD_ATTR             3  'settings'
               60  CALL_FUNCTION_KW_0     0  None
               63  POP_TOP          
               64  JUMP_FORWARD          0  'to 67'
             67_0  COME_FROM            64  '64'

 L. 138        67  LOAD_FAST             1  'message'
               70  LOAD_ATTR             5  'recipient_number'
               73  POP_JUMP_IF_FALSE    95  'to 95'

 L. 139        76  LOAD_FAST             1  'message'
               79  LOAD_ATTR             5  'recipient_number'
               82  LOAD_FAST             2  'raw_data'
               85  LOAD_FAST             0  'self'
               88  LOAD_ATTR             6  'recipient_keyword'
               91  STORE_SUBSCR     
               92  JUMP_FORWARD         12  'to 107'

 L. 141        95  LOAD_GLOBAL           7  'ValueError'
               98  LOAD_CONST               'A recipient_number must be supplied'
              101  CALL_FUNCTION_1       1  None
              104  RAISE_VARARGS_1       1  None
            107_0  COME_FROM            92  '92'

 L. 146       107  LOAD_GLOBAL           8  'unicodedata'
              110  LOAD_ATTR             9  'normalize'

 L. 147       113  LOAD_CONST               'NFKD'

 L. 148       116  LOAD_GLOBAL          10  'unicode'
              119  LOAD_FAST             1  'message'
              122  LOAD_ATTR            11  'content'
              125  CALL_FUNCTION_1       1  None
              128  CALL_FUNCTION_2       2  None
              131  LOAD_ATTR            12  'encode'

 L. 149       134  LOAD_CONST               'ascii'
              137  LOAD_CONST               'ignore'
              140  CALL_FUNCTION_2       2  None
              143  LOAD_FAST             2  'raw_data'
              146  LOAD_FAST             0  'self'
              149  LOAD_ATTR            13  'content_keyword'
              152  STORE_SUBSCR     

 L. 150       153  LOAD_FAST             0  'self'
              156  LOAD_ATTR            14  'uuid_keyword'
              159  POP_JUMP_IF_FALSE   199  'to 199'

 L. 151       162  LOAD_FAST             1  'message'
              165  LOAD_ATTR            15  'uuid'
              168  POP_JUMP_IF_TRUE    180  'to 180'
              171  LOAD_ASSERT              AssertionError
              174  LOAD_CONST               'Message must have a valid UUID. Has it been saved?'
              177  RAISE_VARARGS_2       2  None

 L. 152       180  LOAD_FAST             1  'message'
              183  LOAD_ATTR            15  'uuid'
              186  LOAD_FAST             2  'raw_data'
              189  LOAD_FAST             0  'self'
              192  LOAD_ATTR            14  'uuid_keyword'
              195  STORE_SUBSCR     
              196  JUMP_FORWARD          0  'to 199'
            199_0  COME_FROM           196  '196'

 L. 153       199  LOAD_GLOBAL          16  'urllib'
              202  LOAD_ATTR            17  'urlencode'
              205  LOAD_FAST             2  'raw_data'
              208  CALL_FUNCTION_1       1  None
              211  STORE_FAST            3  'data'

 L. 154       214  LOAD_GLOBAL          18  'logging'
              217  LOAD_ATTR            19  'debug'
              220  LOAD_FAST             3  'data'
              223  CALL_FUNCTION_1       1  None
              226  POP_TOP          

 L. 155       227  LOAD_GLOBAL          18  'logging'
              230  LOAD_ATTR            19  'debug'
              233  LOAD_FAST             0  'self'
              236  CALL_FUNCTION_1       1  None
              239  POP_TOP          

 L. 157       240  LOAD_GLOBAL          16  'urllib'
              243  LOAD_ATTR            20  'urlopen'
              246  LOAD_FAST             0  'self'
              249  LOAD_ATTR            21  'base_url'
              252  LOAD_FAST             3  'data'
              255  CALL_FUNCTION_2       2  None
              258  STORE_FAST            4  'res'

 L. 161       261  LOAD_FAST             4  'res'
              264  LOAD_ATTR            22  'read'
              267  CALL_FUNCTION_0       0  None
              270  STORE_FAST            5  'status_msg'

 L. 162       273  LOAD_GLOBAL          18  'logging'
              276  LOAD_ATTR            19  'debug'
              279  LOAD_FAST             5  'status_msg'
              282  CALL_FUNCTION_1       1  None
              285  POP_TOP          

 L. 163       286  LOAD_FAST             0  'self'
              289  LOAD_ATTR            23  'error_format'
              292  POP_JUMP_IF_FALSE   378  'to 378'
              295  LOAD_GLOBAL          24  're'
              298  LOAD_ATTR            25  'match'
              301  LOAD_FAST             0  'self'
              304  LOAD_ATTR            23  'error_format'
              307  LOAD_FAST             5  'status_msg'
              310  CALL_FUNCTION_2       2  None
            313_0  COME_FROM           292  '292'
              313  POP_JUMP_IF_FALSE   378  'to 378'

 L. 164       316  LOAD_CONST               'Failed'
              319  LOAD_FAST             1  'message'
              322  STORE_ATTR            0  'status'

 L. 165       325  LOAD_GLOBAL          24  're'
              328  LOAD_ATTR            25  'match'
              331  LOAD_FAST             0  'self'
              334  LOAD_ATTR            23  'error_format'
              337  LOAD_FAST             5  'status_msg'
              340  CALL_FUNCTION_2       2  None
              343  LOAD_ATTR            26  'groupdict'
              346  CALL_FUNCTION_0       0  None
              349  LOAD_CONST               'status_message'
              352  BINARY_SUBSCR    
              353  LOAD_FAST             1  'message'
              356  STORE_ATTR           27  'status_message'

 L. 166       359  LOAD_GLOBAL          18  'logging'
              362  LOAD_ATTR            28  'warning'
              365  LOAD_FAST             1  'message'
              368  LOAD_ATTR            27  'status_message'
              371  CALL_FUNCTION_1       1  None
              374  POP_TOP          
              375  JUMP_FORWARD        301  'to 679'

 L. 167       378  LOAD_FAST             5  'status_msg'
              381  LOAD_ATTR            29  'startswith'
              384  LOAD_CONST               'ERR'
              387  CALL_FUNCTION_1       1  None
              390  POP_JUMP_IF_TRUE    408  'to 408'
              393  LOAD_FAST             5  'status_msg'
              396  LOAD_ATTR            29  'startswith'
              399  LOAD_CONST               'WARN'
              402  CALL_FUNCTION_1       1  None
            405_0  COME_FROM           390  '390'
              405  POP_JUMP_IF_FALSE   458  'to 458'

 L. 168       408  LOAD_CONST               'Failed'
              411  LOAD_FAST             1  'message'
              414  STORE_ATTR            0  'status'

 L. 169       417  LOAD_FAST             5  'status_msg'
              420  LOAD_ATTR            30  'split'
              423  LOAD_CONST               ': '
              426  CALL_FUNCTION_1       1  None
              429  LOAD_CONST               1
              432  BINARY_SUBSCR    
              433  LOAD_FAST             1  'message'
              436  STORE_ATTR           27  'status_message'

 L. 170       439  LOAD_GLOBAL          18  'logging'
              442  LOAD_ATTR            28  'warning'
              445  LOAD_FAST             1  'message'
              448  LOAD_ATTR            27  'status_message'
              451  CALL_FUNCTION_1       1  None
              454  POP_TOP          
              455  JUMP_FORWARD        221  'to 679'

 L. 172       458  LOAD_CONST               'Sent'
              461  LOAD_FAST             1  'message'
              464  STORE_ATTR            0  'status'

 L. 173       467  LOAD_GLOBAL          24  're'
              470  LOAD_ATTR            25  'match'
              473  LOAD_FAST             0  'self'
              476  LOAD_ATTR            31  'success_format'
              479  LOAD_FAST             5  'status_msg'
              482  CALL_FUNCTION_2       2  None
              485  LOAD_ATTR            26  'groupdict'
              488  CALL_FUNCTION_0       0  None
              491  STORE_FAST            6  'parsed_response'

 L. 174       494  LOAD_CONST               'gateway_message_id'
              497  LOAD_FAST             6  'parsed_response'
              500  COMPARE_OP            6  in
              503  POP_JUMP_IF_FALSE   538  'to 538'
              506  LOAD_FAST             6  'parsed_response'
              509  LOAD_CONST               'gateway_message_id'
              512  BINARY_SUBSCR    
            513_0  COME_FROM           503  '503'
              513  POP_JUMP_IF_FALSE   538  'to 538'

 L. 175       516  LOAD_FAST             6  'parsed_response'
              519  LOAD_CONST               'gateway_message_id'
              522  BINARY_SUBSCR    
              523  LOAD_ATTR            32  'strip'
              526  CALL_FUNCTION_0       0  None
              529  LOAD_FAST             1  'message'
              532  STORE_ATTR           33  'gateway_message_id'
              535  JUMP_FORWARD          0  'to 538'
            538_0  COME_FROM           535  '535'

 L. 176       538  LOAD_CONST               'status_code'
              541  LOAD_FAST             6  'parsed_response'
              544  COMPARE_OP            6  in
              547  POP_JUMP_IF_FALSE   588  'to 588'
              550  LOAD_FAST             6  'parsed_response'
              553  LOAD_CONST               'status_code'
              556  BINARY_SUBSCR    
            557_0  COME_FROM           547  '547'
              557  POP_JUMP_IF_FALSE   588  'to 588'

 L. 177       560  LOAD_FAST             0  'self'
              563  LOAD_ATTR            34  'status_mapping'
              566  LOAD_ATTR            35  'get'
              569  LOAD_FAST             6  'parsed_response'
              572  LOAD_CONST               'status_code'
              575  BINARY_SUBSCR    
              576  CALL_FUNCTION_1       1  None
              579  LOAD_FAST             1  'message'
              582  STORE_ATTR            0  'status'
              585  JUMP_FORWARD          0  'to 588'
            588_0  COME_FROM           585  '585'

 L. 178       588  LOAD_CONST               'status_message'
              591  LOAD_FAST             6  'parsed_response'
              594  COMPARE_OP            6  in
              597  POP_JUMP_IF_FALSE   626  'to 626'
              600  LOAD_FAST             6  'parsed_response'
              603  LOAD_CONST               'status_message'
              606  BINARY_SUBSCR    
            607_0  COME_FROM           597  '597'
              607  POP_JUMP_IF_FALSE   626  'to 626'

 L. 179       610  LOAD_FAST             6  'parsed_response'
              613  LOAD_CONST               'status_message'
              616  BINARY_SUBSCR    
              617  LOAD_FAST             1  'message'
              620  STORE_ATTR           27  'status_message'
              623  JUMP_FORWARD          0  'to 626'
            626_0  COME_FROM           623  '623'

 L. 180       626  LOAD_GLOBAL          18  'logging'
              629  LOAD_ATTR            19  'debug'
              632  LOAD_CONST               'Gateway MSG ID %s [%i]'
              635  LOAD_FAST             1  'message'
              638  LOAD_ATTR            33  'gateway_message_id'
              641  LOAD_GLOBAL          36  'len'
              644  LOAD_FAST             1  'message'
              647  LOAD_ATTR            33  'gateway_message_id'
              650  CALL_FUNCTION_1       1  None
              653  BUILD_TUPLE_2         2 
              656  BINARY_MODULO    
              657  CALL_FUNCTION_1       1  None
              660  POP_TOP          

 L. 181       661  LOAD_GLOBAL          37  'datetime'
              664  LOAD_ATTR            37  'datetime'
              667  LOAD_ATTR            38  'now'
              670  CALL_FUNCTION_0       0  None
              673  LOAD_FAST             1  'message'
              676  STORE_ATTR           39  'send_date'
            679_0  COME_FROM           455  '455'
            679_1  COME_FROM           375  '375'

 L. 183       679  LOAD_FAST             1  'message'
              682  LOAD_ATTR            40  'save'
              685  CALL_FUNCTION_0       0  None
              688  POP_TOP          

 L. 185       689  LOAD_FAST             1  'message'
              692  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 692

    def check_availability_to_send(self, number):
        if not self.check_number_url:
            return
        else:
            raw_data = {}
            raw_data.update(**self.settings)
            raw_data[self.check_number_field] = number
            data = urllib.urlencode(raw_data)
            res = urllib.urlopen(self.check_number_url, data)
            res_data = res.read()
            if self.check_number_response_format:
                parsed_response = re.match(self.check_number_response_format, res_data).groupdict()
                status = self.check_number_status_mapping.get(parsed_response.get('status', None), None)
                charge = self.check_number_status_mapping.get(parsed_response.get('charge', None), None)
                return {'number': number, 
                   'status': status, 
                   'charge': charge}
            return

    def query_balance(self):
        if not self.query_balance_url:
            return
        else:
            raw_data = {}
            for field in self.query_balance_params:
                raw_data[field] = self.settings[field]

            data = urllib.urlencode(raw_data)
            res = urllib.urlopen(self.query_balance_url, data)
            res_data = res.read()
            if self.query_balance_response_format:
                parsed_response = re.match(self.query_balance_response_format, res_data).groupdict()
                return parsed_response.get('balance', None)
            return