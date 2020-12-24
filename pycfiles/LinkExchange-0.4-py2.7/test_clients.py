# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_clients.py
# Compiled at: 2011-04-21 17:48:44
import unittest, re
from linkexchange.tests import ClientLinksTestCaseMixin
from linkexchange.tests import ClientCFTestCaseMixin
from linkexchange.clients.sape import SapeClient, SapeContextClient
from linkexchange.clients.sape import SapeArticlesClient
from linkexchange.clients.sape import SapeTestServer
from linkexchange.clients.sape import SapeArticlesIndexTestServer
from linkexchange.clients.sape import SapeArticlesArticleTestServer
from linkexchange.clients.sape import SapeArticlesTemplateTestServer
from linkexchange.clients.linkfeed import LinkFeedClient
from linkexchange.clients.linkfeed import LinkFeedTestServer
from linkexchange.clients.trustlink import TrustLinkClient
from linkexchange.clients.trustlink import TrustLinkTestServer

class SapeClientXTestCaseMixin(ClientLinksTestCaseMixin):
    """
    Base test case to test SapeClient independent of server format.
    """
    pageLinkMap = {'/': [
           ('http://example1.com', 'example text 1'),
           ('http://example2.com', 'example text 2')], 
       '/path/1': [
                 ('http://example1.com', 'example text 1'),
                 ('http://example2.com', 'example text 2'),
                 ('http://example3.com', 'example text 3'),
                 ('http://example4.com', 'example text 4')]}
    checkCode = '<!--12345-->'
    server_format = None
    cookies = {'sape_cookie': 'user123456789'}
    htmlLinksDelimPattern = '\\. '

    def createServers(cls):
        return [
         SapeTestServer(server_format=cls.server_format)]

    createServers = classmethod(createServers)

    def createClient(cls, server_urls):
        return SapeClient(user='user123456789', db_driver=('mem', ), server_list=[
         server_urls[0]], server_format=cls.server_format)

    createClient = classmethod(createClient)


class SapeClientPHPTestCase(SapeClientXTestCaseMixin, unittest.TestCase):
    """
    Test SapeClient with php server format.
    """
    server_format = 'php'


class SapeClientXMLTestCase(SapeClientXTestCaseMixin, unittest.TestCase):
    """
    Test SapeClient with xml server format.
    """
    server_format = 'xml'


class SapeContextClientXCookiesTestCaseMixin(ClientCFTestCaseMixin):
    """
    Base test case to test SapeContextClient independent of server_format and
    service cookie enabled.
    """
    pageContentMap = {'/': [
           ('This&#x20;text contains\n                    example text 1.', '<sape_index>This&#x20;text contains\n                    <a href="http://example1.com">example text 1</a>.</sape_index><!--12345-->'),
           ('foo <textarea>\n                    example text 1 bar</textarea>', '<sape_index>foo <textarea>\n                    example text 1 bar</textarea></sape_index><!--12345-->'),
           ('<html>\n                    <body>\n                    Full example text 2.\n                    </body>\n                    </html>',
 '<html>\n                    <body><sape_index>\n                    Full <a href="http://example2.com">example text 2</a>.\n                    </sape_index><!--12345--></body>\n                    </html>'),
           ('<html>\n                    <body>\n                    <sape_index>First example text 1.</sape_index>\n                    Second example text 2.\n                    </body>\n                    </html>',
 '<html>\n                    <body>\n                    <sape_index>First <a href="http://example1.com">example text 1</a>.</sape_index><!--12345-->\n                    Second example text 2.\n                    </body>\n                    </html>')]}
    checkCode = '<!--12345-->'
    server_format = None
    cookies = {'sape_cookie': 'user123456789'}

    def createServers(cls):
        return [
         SapeTestServer(server_format=cls.server_format)]

    createServers = classmethod(createServers)

    def createClient(cls, server_urls):
        return SapeContextClient(user='user123456789', db_driver=('mem', ), server_list=[
         server_urls[0]], server_format=cls.server_format)

    createClient = classmethod(createClient)


class SapeContextClientPHPCookiesTestCase(SapeContextClientXCookiesTestCaseMixin, unittest.TestCase):
    server_format = 'php'


class SapeContextClientXMLCookiesTestCase(SapeContextClientXCookiesTestCaseMixin, unittest.TestCase):
    server_format = 'xml'


class SapeContextClientXTestCaseMixin(SapeContextClientXCookiesTestCaseMixin):
    """
    Base test case to test SapeContextClient independent of server_format and
    service cookie disabled.
    """
    pageContentMap = {'/': [
           ('This&#x20;text contains\n                    example text 1.', 'This&#x20;text contains\n                    <a href="http://example1.com">example text 1</a>.'),
           ('foo <textarea>\n                    example text 1 bar</textarea>', 'foo <textarea>\n                    example text 1 bar</textarea>'),
           ('<html>\n                    <body>\n                    Full example text 2.\n                    </body>\n                    </html>',
 '<html>\n                    <body>\n                    Full <a href="http://example2.com">example text 2</a>.\n                    </body>\n                    </html>'),
           ('<html>\n                    <body>\n                    <sape_index>First example text 1.</sape_index>\n                    Second example text 2.\n                    </body>\n                    </html>',
 '<html>\n                    <body>\n                    First <a href="http://example1.com">example text 1</a>.\n                    Second example text 2.\n                    </body>\n                    </html>')]}
    server_format = None
    cookies = None


class SapeContextClientPHPTestCase(SapeContextClientXTestCaseMixin, unittest.TestCase):
    server_format = 'php'


class SapeContextClientXMLTestCase(SapeContextClientXTestCaseMixin, unittest.TestCase):
    server_format = 'xml'


class SapeArticlesClientTestCase(ClientLinksTestCaseMixin, unittest.TestCase):
    pageLinkMap = {'/': [
           ('/articles/1', 'ann link 1'),
           ('/articles/1', 'ann link 2')]}
    checkCode = '<!-- announcements place -->'
    server_format = 'php'
    cookies = {'sape_cookie': 'user123456789'}

    def createServers(cls):
        template_test_server = SapeArticlesTemplateTestServer()
        template_urls = [('1', template_test_server.url)]
        return [SapeArticlesIndexTestServer(template_urls=template_urls),
         SapeArticlesArticleTestServer(),
         template_test_server]

    createServers = classmethod(createServers)

    def createClient(cls, server_urls):
        return SapeArticlesClient(user='user123456789', index_db_driver=('mem', ), article_db_driver=('mem', ), image_db_driver=('mem', ), template_db_driver=('mem', ), index_server_list=[
         server_urls[0]], article_server_list=[
         server_urls[1]])

    createClient = classmethod(createClient)

    def testHandleRequest(self):
        request = self.newRequest(uri='/articles/1')
        response = self.client.handle_request(request)
        self.assertEqual(response.status, 200)
        mime = response.headers['Content-Type'].split(';')[0]
        self.assertEqual(mime, 'text/html')
        title_found = '<title>The article title</title>' in response.body
        self.assertEqual(title_found, True)
        body_found = '<p>The article ' in response.body
        self.assertEqual(body_found, True)
        extlink_re = re.compile('<noindex><a[^>]+href="http://external-link.com"[^>]*>External link</a></noindex>', re.S)
        m = extlink_re.search(response.body)
        self.assertEqual(m is not None, True)
        self.assertEqual('rel="nofollow"' in m.group(0), True)
        self.client.refresh_db(self.newRequest(uri='/'))
        return


class LinkFeedClientXTestCaseMixin(ClientLinksTestCaseMixin):
    """
    Base test case to test LinkFeedClient independent of server format.
    """
    pageLinkMap = {'/': [
           ('http://example1.com', 'example text 1'),
           ('http://example2.com', 'example text 2')], 
       '/path/1': [
                 ('http://example1.com', 'example text 1'),
                 ('http://example2.com', 'example text 2'),
                 ('http://example3.com', 'example text 3'),
                 ('http://example4.com', 'example text 4')]}
    checkCode = '<!--12345-->'
    htmlLinksDelimPattern = '\\. '
    server_format = None
    bot_ip = '123.45.67.89'

    def createServers(cls):
        return [
         LinkFeedTestServer(server_format=cls.server_format)]

    createServers = classmethod(createServers)

    def createClient(cls, server_urls):
        return LinkFeedClient(user='user123456789', db_driver=('mem', ), server_list=[
         server_urls[0]], server_format=cls.server_format)

    createClient = classmethod(createClient)


class LinkFeedClientPHPTestCase(LinkFeedClientXTestCaseMixin, unittest.TestCase):
    """
    Test LinkFeedClient with php server format.
    """
    server_format = 'php'


class LinkFeedClientXMLTestCase(LinkFeedClientXTestCaseMixin, unittest.TestCase):
    """
    Test LinkFeedClient with xml server format.
    """
    server_format = 'xml'


class TrustLinkClientTestCase(ClientLinksTestCaseMixin, unittest.TestCase):
    pageLinkMap = {'/': [
           ('http://example1.com', 'anchor 1'),
           ('http://example2.com', 'anchor 2')], 
       '/path/1': [
                 ('http://example1.com', 'anchor 1'),
                 ('http://example2.com', 'anchor 2'),
                 ('http://example3.com', 'anchor 3'),
                 ('http://example4.com', 'anchor 4')]}
    checkCode = '<!--12345-->'
    htmlLinksDelimPattern = '\\. '
    server_format = None
    bot_ip = '123.45.67.89'

    def createServers(cls):
        return [
         TrustLinkTestServer()]

    createServers = classmethod(createServers)

    def createClient(cls, server_urls):
        link_template = '<a href="%(href)s">%(anchor)s</a> %(text)s'
        return TrustLinkClient(user='user123456789', db_driver=('mem', ), server_list=[
         server_urls[0]], link_template=link_template)

    createClient = classmethod(createClient)