# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/jsonrpc.py
# Compiled at: 2012-08-03 08:35:35
import httplib, base64, json, uuid, urlparse
CLIENT_AGENT = 'snurtle-json-rpc/1.0 OpenGroupware Rocks!'

class JSONRPCClient(object):

    def __init__(self, uri, credentials=None):
        self._uri = uri
        self._online = False
        if credentials:
            self._creds = credentials
        else:
            self._creds = None
        return

    @property
    def account(self):
        return self._account

    def test(self):
        try:
            self._account = self.call('getLoginAccount', [65535], uuid.uuid4().hex)
        except Exception as e:
            print e
            return False

        self._online = True
        return True

    @property
    def online(self):
        return self._online

    def call(self, method, parameters, call_id):
        REQUEST = {'version': '1.1', 'method': method, 
           'id': call_id, 
           'params': parameters}
        PAYLOAD = json.dumps(REQUEST)
        connection = httplib.HTTPConnection(urlparse.urlparse(self._uri).netloc)
        connection.putrequest('POST', urlparse.urlparse(self._uri).path)
        if self._creds:
            coin = ('{0}:{1}').format(self._creds.get('username', ''), self._creds.get('password', ''))
            coin = ('Basic {0}').format(base64.encodestring(coin)[:-1])
            connection.putheader('Authorization', coin)
        connection.putheader('User-Agent', CLIENT_AGENT)
        connection.putheader('Content-Length', str(len(PAYLOAD)))
        connection.putheader('Content-Type', 'application/json')
        connection.endheaders()
        connection.send(PAYLOAD)
        response = connection.getresponse()
        if response.status == 200:
            try:
                data = response.read()
                connection.close()
            except:
                pass
            else:
                data = json.loads(data)
                if data['error']:
                    print ('ERROR: {0}').format(data['error'])
                else:
                    return data['result']
        raise Exception(('RPC Oops! HTTP Response Code#{0}').format(response.status))