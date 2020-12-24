# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/clients/trustlink.py
# Compiled at: 2011-04-26 11:38:59
import urlparse, logging
from linkexchange.clients.sape import SapeLikeClient
from linkexchange.clients.sape import SapeLikeTestServer
from linkexchange.utils import is_plugin_specifier, load_plugin
log = logging.getLogger('linkexchange.clients.trustlink')

class TrustLinkClient(SapeLikeClient):
    """
    TrustLink.ru client.
    """
    server_list = [
     'http://db.trustlink.ru/%(user)s/%(host)s/UTF-8']
    server_format = 'php'
    force_show_code = False
    link_template = '\n    <ul>\n      <li><a href="%(href)s">%(anchor)s</a></li>\n      <li>%(text)s</li>\n      <li>%(host)s</li>\n    </ul>'
    link_template_no_anchor = '\n    <ul>\n      <li>%(text)s</li>\n      <li>%(host)s</li>\n    </ul>'

    def __init__(self, user, db_driver, **kw):
        """
        TrustLinkClient constructor.
        
        The user is hash code string that assigned to user on link exchange
        service.

        The db_driver argument is multihash database driver instance or plugin
        specifier. In second case plugin specifier is used to create new
        instance. The database driver instance is used to store links database.

        @param user: user hash code string on link exchange service
        @param db_driver: multihash database driver instance or plugin specifier
        @keyword server_list: list of servers URLs
        @keyword link_template: template to build particular link
        @keyword link_template_no_anchor: template to build particular link
                                          without anchor
        """
        super(TrustLinkClient, self).__init__(user, **kw)
        if is_plugin_specifier(db_driver):
            db_driver = load_plugin('linkexchange.multihash_drivers', db_driver)
        self.db_driver = db_driver
        for param in ('server_list', 'link_template', 'link_template_no_anchor'):
            if param in kw:
                setattr(self, param, kw[param])

        log.debug('New %s instance:\n%s', self.__class__.__name__, ('\n').join([ '    %s: %s' % (x, repr(getattr(self, x))) for x in ('user',
                                                                                                                                      'db_driver',
                                                                                                                                      'db_lifetime',
                                                                                                                                      'db_reloadtime',
                                                                                                                                      'socket_timeout',
                                                                                                                                      'force_show_code',
                                                                                                                                      'no_query_string',
                                                                                                                                      'server_list',
                                                                                                                                      'server_charset',
                                                                                                                                      'user_agent')
                                                                               ]))

    def load_links_data(self, request):
        return self.load_data(self.db_driver, self.server_list, self.server_format, request)

    def refresh_db(self, request):
        self.refresh_data(self.db_driver, self.server_list, self.server_format, request)

    def parse_param(self, name, value):
        if name == '__trustlink_robots__':
            if type(value) == dict:
                value = value.values()
        return super(TrustLinkClient, self).parse_param(name, value)

    def get_links_for_page(self, data, request, uri):

        def link_to_html(link):
            if type(link) != dict:
                log.error('Link must be a dictionary object: %s', repr(link))
                return ''
            if 'text' not in link or 'url' not in link:
                log.error('Invalid link dictionary: %s', repr(link))
                return ''
            tpl_vars = link.copy()
            tpl_vars['href'] = link.get('punicode_url', '') or link['url']
            tpl_vars['host'] = urlparse.urlsplit(link['url'])[1].split(':')[0].lower()
            if tpl_vars['host'].startswith('www.'):
                tpl_vars['host'] = tpl_vars['host'][len('www.'):]
            if link.get('anchor', ''):
                return self.link_template % tpl_vars
            return self.link_template_no_anchor % tpl_vars

        if self.is_test(data, request):
            try:
                test_link = data['__test_tl_link__']
            except KeyError:
                links = []
            else:
                links = map(link_to_html, [test_link] * 4)

        else:
            links = data.get(uri, [])
        return map(link_to_html, links)

    def get_links_new_page(self, data, request):
        if self.is_check_code_visible(data, request):
            if data.get('__trustlink_start__', '') + data.get('__trustlink_end__', ''):
                return ['']
        return []

    def get_delimiter(self, data, request):
        return data.get('__trustlink_delimiter__', '')

    def is_bot(self, data, request):
        bot_ips = data.get('__trustlink_robots__', [])
        return request.remote_addr and request.remote_addr in bot_ips

    def is_test(self, data, request):
        return request.meta.get('HTTP_TRUSTLINK', '') == self.user

    def transform_code(self, data, request, code):
        if self.is_check_code_visible(data, request):
            start = data.get('__trustlink_start__', '')
            end = data.get('__trustlink_end__', '')
        else:
            start = end = ''
        return start + code + end


class TrustLinkTestServer(SapeLikeTestServer):
    """
    Test server to test TrustLink client.
    """
    data = {'/': [
           dict(url='http://example1.com', anchor='anchor 1', text='text 1'),
           dict(url='http://example2.com', anchor='anchor 2', text='text 2')], 
       '/path/1': [
                 dict(url='http://example1.com', anchor='anchor 1', text='text 1'),
                 dict(url='http://example2.com', anchor='anchor 2', text='text 2'),
                 dict(url='http://example3.com', anchor='anchor 3', text='text 3'),
                 dict(url='http://example4.com', anchor='anchor 4', text='text 4')], 
       '__trustlink_start__': '<!--12345-->', 
       '__trustlink_end__': '<!--12345-->', 
       '__trustlink_delimiter__': '. ', 
       '__trustlink_robots__': [
                              '123.45.67.89']}
    server_format = 'php'


if __name__ == '__main__':
    import doctest
    doctest.testmod()