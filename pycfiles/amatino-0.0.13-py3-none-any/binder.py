# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/amathon/binder.py
# Compiled at: 2012-09-19 00:38:09
__doc__ = '\nCreated on 2012/01/13\n\n@author: y42sora\n@requires: Python 3.x\n'
import time, urllib.request, urllib.parse, hmac, hashlib, base64

def bind_api(operation):
    """ making api method
    
    This function make a api method.
    The api method create a Transfer object and call transfer() method.
    This function set a operation name on Transfer and return api method
    """

    class Transfer(object):
        """ translate to amazon
        
        This class translate to amazon using Product Advertising API
        """
        operation_name = operation

        def __init__(self, api, args):
            self.api = api
            self.parameters = args
            if 'AmathonParameterList' in self.parameters:
                for name, param in args['AmathonParameterList']:
                    self.parameters[name] = param

                del self.parameters['AmathonParameterList']

        def buildURL(self):
            """ making url
            
            """
            self.parameters['Service'] = 'AWSECommerceService'
            self.parameters['Operation'] = self.operation_name
            self.parameters['AWSAccessKeyId'] = self.api.access_key
            self.parameters['AssociateTag'] = self.api.aa_tag
            self.parameters['Timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            parameters = sorted(self.parameters.items())
            request = urllib.parse.urlencode(parameters)
            msg = 'GET\n%s\n/onca/xml\n%s' % (self.api.get_url, request)
            sighmac = hmac.new(self.api.secret_key.encode('ascii'), msg.encode('ascii'), hashlib.sha256)
            parameters.append(('Signature', base64.b64encode(sighmac.digest()).decode()))
            return self.api.api_url + '?' + urllib.parse.urlencode(parameters)

        def transfer(self):
            url = self.buildURL()
            opener = urllib.request.build_opener()
            if self.api.proxy_flag:
                proxy_hander = urllib.request.ProxyHandler(self.api.proxy)
                opener.add_handler(proxy_hander)
            return opener.open(url).read()

    def _call(api, **args):
        return Transfer(api, args).transfer()

    return _call