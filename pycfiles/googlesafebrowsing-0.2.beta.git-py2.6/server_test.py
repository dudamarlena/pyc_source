# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesafebrowsing/server_test.py
# Compiled at: 2010-12-12 06:19:14
"""These tests run against the prod safebrowsing servers."""
import sblist, server, base64, cgi, hmac, logging, sha, StringIO, sys, unittest, urlparse

class HTTPError(Exception):
    """Fake HTTP error used to test gethash requests that return a 204."""

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return 'HTTPError code:%d' % self.code


class FakeServer(object):
    """Helper class which simulates the SafeBrowsing server."""

    def __init__(self):
        self._responses = []

    def SetResponse(self, url_prefix, params, request, response):
        """Set a fake response for a particular request.

    If a request comes in to the fake server with a url that matches the given
    url_prefix and a request body that matches the given request body and the
    given params are a subset of the request CGI arguments the fake server will
    serve the given baked response or raise an exception if the response is an
    exception object.

    Args:
     url_prefix: url prefix that has to match for the response to be sent.
     params: sub-set of CGI parameters that have to be present for the request
             to be valid and the response to be sent.  Can be None.
             Format: [(arg1, value1), (arg2, value2), ...].
     request: request body that has to be set for the response to be sent.
              Can be None if no request body is expected for a particular
              request.
     response: Response data to send or exception to raise if the conditions
               above are met.
    """
        self._responses.append((url_prefix, params, request, response))

    def _HasExpectedParams(self, url, expected_params):
        """Returns true if the expected CGI parameters are set in the given URL."""
        if expected_params:
            actual_params = cgi.parse_qs(urlparse.urlparse(url)[4])
            for (key, value) in expected_params:
                if key not in actual_params or actual_params[key][0] != value:
                    return False

        return True

    def HandleRequest(self, url, data):
        for (url_prefix, params, request, response) in self._responses:
            if url.startswith(url_prefix) and request == data and self._HasExpectedParams(url, params):
                if isinstance(response, Exception):
                    raise response
                else:
                    return StringIO.StringIO(response)

        raise Exception('No such data: %s' % url)


class ServerTest(unittest.TestCase):

    def setUp(self):
        self._fake_sb_server = FakeServer()
        self._server = server.Server(('safebrowsing.clients.google.com', 80), ('sb-ssl.google.com',
                                                                               443), '/safebrowsing', clientkey='BOGUS_CLIENT_KEY', wrkey='BOGUS_WRAPPED_KEY', apikey='BOGUS_API_KEY', url_request_function=self._fake_sb_server.HandleRequest)
        self._base_url = 'http://safebrowsing.clients.google.com:80/safebrowsing'

    def _Mac(self, data):
        (clientkey, wrkey) = self._server.Keys()
        return base64.urlsafe_b64encode(hmac.new(clientkey, data, sha).digest())

    def testGetLists(self):
        response = 'lista\nlistb\nlistc'
        response = '%s\n%s' % (self._Mac(response), response)
        self._fake_sb_server.SetResponse(url_prefix='%s/list?' % self._base_url, params=[
         ('wrkey', 'BOGUS_WRAPPED_KEY'),
         ('apikey', 'BOGUS_API_KEY')], request=None, response=response)
        self.assertEqual(['lista', 'listb', 'listc'], [ l.Name() for l in self._server.GetLists() ])
        return

    def testKeys(self):
        self.assertEqual(('BOGUS_CLIENT_KEY', 'BOGUS_WRAPPED_KEY'), self._server.Keys())

    def testRekey(self):
        self._fake_sb_server.SetResponse(url_prefix='https://sb-ssl.google.com:443/safebrowsing/newkey?', params=None, request=None, response='clientkey:28:TkVXX0JPR1VTX0NMSUVOVF9LRVk=\n' + 'wrappedkey:15:NEW_BOGUS_WRKEY')
        self.assertEqual(('NEW_BOGUS_CLIENT_KEY', 'NEW_BOGUS_WRKEY'), self._server.Rekey())
        self.assertEqual(('NEW_BOGUS_CLIENT_KEY', 'NEW_BOGUS_WRKEY'), self._server.Keys())
        return

    def testDownload(self):
        lista_a_redirect_response = 'a:10:4:27\n1234\x00' + '5678\x01ABCD' + 'EFGH\x02EFGHIJKL' + 'a:7:4:0\n'
        lista_s_redirect_response = 's:2:4:22\n' + '5678\x01\x00\x00\x00\nABCD' + 'EFGH\x00\x00\x00\x00\n' + 's:3:4:0\n'
        listb_a_redirect_response = 'a:1:6:1546\n' + b'1234\xff%s' % ('').join(map(str, range(100000, 100255))) + '1234\x01100255'
        self._fake_sb_server.SetResponse(url_prefix='http://rd.com/lista-a', params=None, request=None, response=lista_a_redirect_response)
        self._fake_sb_server.SetResponse(url_prefix='http://rd.com/lista-s', params=None, request=None, response=lista_s_redirect_response)
        self._fake_sb_server.SetResponse(url_prefix='http://rd.com/listb-a', params=None, request=None, response=listb_a_redirect_response)
        response = ('\n').join(['n:1800',
         'i:lista',
         'u:rd.com/lista-s,%s' % self._Mac(lista_s_redirect_response),
         'u:rd.com/lista-a,%s' % self._Mac(lista_a_redirect_response),
         'ad:1-2,4-5,7',
         'i:listb',
         'u:rd.com/listb-a,%s' % self._Mac(listb_a_redirect_response),
         'sd:2-6'])
        self._fake_sb_server.SetResponse(url_prefix='%s/downloads?' % self._base_url, params=[
         ('wrkey', 'BOGUS_WRAPPED_KEY'),
         ('apikey', 'BOGUS_API_KEY')], request='s;%d\nlista;mac\nlistb;mac\n' % 1024, response='m:%s\n%s' % (self._Mac(response), response))
        sblists = [
         sblist.List('lista'), sblist.List('listb')]
        response = self._server.Download(sblists, 1048576)
        self.assertEqual(1800, response.min_delay_sec)
        self.assertFalse(response.rekey)
        self.assertFalse(response.reset)
        self.assertEqual(['lista', 'listb'], response.listops.keys())
        self.assertTrue(isinstance(response.listops['lista'][0], server.SubChunk))
        self.assertEqual(2, response.listops['lista'][0]._chunknum)
        self.assertEqual(4, response.listops['lista'][0]._prefixlen)
        self.assertEqual([('ABCD', 10), ('EFGH', 10)], response.listops['lista'][0]._prefixes)
        self.assertTrue(isinstance(response.listops['lista'][1], server.EmptySubChunks))
        self.assertEqual([3], response.listops['lista'][1]._chunknums)
        self.assertTrue(isinstance(response.listops['lista'][2], server.AddChunk))
        self.assertEqual(10, response.listops['lista'][2]._chunknum)
        self.assertEqual(4, response.listops['lista'][2]._prefixlen)
        self.assertEqual(['1234', 'ABCD', 'EFGH', 'IJKL'], response.listops['lista'][2]._prefixes)
        self.assertTrue(isinstance(response.listops['lista'][3], server.EmptyAddChunks))
        self.assertEqual([7], response.listops['lista'][3]._chunknums)
        self.assertTrue(isinstance(response.listops['lista'][4], server.AddDel))
        self.assertEqual([1, 2, 4, 5, 7], list(response.listops['lista'][4]._chunknums))
        self.assertTrue(isinstance(response.listops['listb'][0], server.AddChunk))
        self.assertEqual(1, response.listops['listb'][0]._chunknum)
        self.assertEqual(6, response.listops['listb'][0]._prefixlen)
        self.assertEqual(map(str, range(100000, 100256)), response.listops['listb'][0]._prefixes)
        self.assertTrue(isinstance(response.listops['listb'][1], server.SubDel))
        self.assertEqual([2, 3, 4, 5, 6], list(response.listops['listb'][1]._chunknums))
        return

    def testGetFullHashes(self):
        response = 'lista:123:32\n89AB%s' % (28 * 'A')
        self._fake_sb_server.SetResponse(url_prefix='%s/gethash?' % self._base_url, params=[
         ('wrkey', 'BOGUS_WRAPPED_KEY'),
         ('apikey', 'BOGUS_API_KEY')], request='4:12\n0123456789AB', response='%s\n%s' % (self._Mac(response), response))
        self._fake_sb_server.SetResponse(url_prefix='%s/gethash?' % self._base_url, params=[
         ('wrkey', 'BOGUS_WRAPPED_KEY'),
         ('apikey', 'BOGUS_API_KEY')], request='10:10\n0123456789', response=HTTPError(204))
        resp = self._server.GetFullHashes(['0123', '4567', '89AB'], 4)
        self.assertTrue(isinstance(resp, server.GetHashResponse))
        self.assertFalse(resp.rekey)
        self.assertEqual({'lista': {123: set(['89AB%s' % (28 * 'A')])}}, resp.listmap)
        resp = self._server.GetFullHashes(['0123456789'], 10)
        self.assertTrue(isinstance(resp, server.GetHashResponse))
        self.assertFalse(resp.rekey)
        self.assertEqual({}, resp.listmap)

    def testGetSequence(self):
        chunkseq = server.Server._GetSequence('1-2,4-5,7-10,11')
        expected = [1, 2, 4, 5, 7, 8, 9, 10, 11]
        for i in xrange(0, 5):
            self.assertEqual(expected, list(chunkseq))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()