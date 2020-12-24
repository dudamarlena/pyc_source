# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/fingerprint_web.py
# Compiled at: 2014-01-14 18:58:51
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.config import Config
from golismero.api.data import discard_data
from golismero.api.data.information.http import HTTP_Raw_Request
from golismero.api.data.information.fingerprint import WebServerFingerprint
from golismero.api.data.resource.url import BaseUrl
from golismero.api.logger import Logger
from golismero.api.net import NetworkException
from golismero.api.net.http import HTTP
from golismero.api.net.web_utils import ParsedURL, urljoin
from golismero.api.plugin import TestingPlugin
from golismero.api.text.wordlist import WordListLoader
from collections import Counter, OrderedDict, defaultdict
from re import compile
SERVER_PATTERN = compile('([\\w\\W\\s\\d]+)[\\s\\/]+([\\d\\w\\.]+)')
__doc__ = '\n\nFingerprint techniques are based on the fantastic paper of httprecon project, and their databases:\n\n- Doc: http://www.computec.ch/projekte/httprecon/?s=documentation\n- Project page: http://www.computec.ch/projekte/httprecon\n\n\nThis plugin try to a fingerprinting over web servers.\n\nStep 1\n------\n\nDefine the methods used:\n\n1 Check the Banner.\n2 Check the order headers in HTTP response.\n3 Check the rest of headers.\n\n\nStep 2\n------\n\nThen assigns a weight to each method:\n\n1. -> 50%\n2. -> 20%\n3. -> 30% (divided by the number of test for each header)\n\n\nStep 3\n------\n\nWe have 9 request with:\n\n1. GET / HTTP/1.1\n2. GET /index.php HTTP/1.1\n3. GET /404_file.html HTTP/1.1\n4. HEAD / HTTP/1.1\n5. OPTIONS / HTTP/1.1\n6. DELETE / HTTP/1.1\n7. TEST / HTTP/1.1\n8. GET / 9.8\n9. GET /<SCRIPT>alert</script> HTTP/1.1 -> Any web attack.\n\nStep 4\n------\n\nFor each type of response analyze the HTTP headers trying to find matches and\nmultiply for their weight.\n\nStep 5\n------\n\nSum de values obtained in step 4, for each test in step 3.\n\nStep 6\n------\n\nGet the 3 highter values os matching.\n\n\nFor example\n-----------\n\nFor an Apache 1.3.26 we will have these results for a normal GET:\n\n- Banner (any of these options):\n\n + Apache/1.3.26 (Linux/SuSE) mod_ssl/2.8.10 OpenSSL/0.9.6g PHP/4.2.2\n + Apache/1.3.26 (UnitedLinux) mod_python/2.7.8 Python/2.2.1 PHP/4.2.2 mod_perl/1.27\n + Apache/1.3.26 (Unix)\n + Apache/1.3.26 (Unix) Debian GNU/Linux mod_ssl/2.8.9 OpenSSL/0.9.6g PHP/4.1.2 mod_webapp/1.2.0-dev\n + Apache/1.3.26 (Unix) Debian GNU/Linux PHP/4.1.2\n + Apache/1.3.26 (Unix) mod_gzip/1.3.19.1a PHP/4.3.11 mod_ssl/2.8.9 OpenSSL/0.9.6\n + MIT Web Server Apache/1.3.26 Mark/1.5 (Unix) mod_ssl/2.8.9 OpenSSL/0.9.7c\n\n- A specific order for the rest of HTTP headers (any of these options):\n\n + Date,Server,Accept-Ranges,Content-Type,Content-Length,Via\n + Date,Server,Connection,Content-Type\n + Date,Server,Keep-Alive,Connection,Transfer-Encoding,Content-Type\n + Date,Server,Last-Modified,ETag,Accept-Ranges,Content-Length,Connection,Content-Type\n + Date,Server,Last-Modified,ETag,Accept-Ranges,Content-Length,Keep-Alive,Connection,Content-Type\n + Date,Server,Set-Cookie,Content-Type,Set-Cookie,Keep-Alive,Connection,Transfer-Encoding\n + Date,Server,X-Powered-By,Keep-Alive,Connection,Transfer-Encoding,Content-Type\n + Date,Server,X-Powered-By,Set-Cookie,Expires,Cache-Control,Pragma,Set-Cookie,Set-Cookie,Keep-Alive,Connection,Transfer-Encoding,Content-Type\n + Date,Server,X-Powered-By,Set-Cookie,Set-Cookie,Expires,Last-Modified,Cache-Control,Pragma,Keep-Alive,Connection,Transfer-Encoding,Content-Type\n\n- The value of the rest of headers must be:\n\n * Content-Type (any of these options):\n\n  + text/html\n  + text/html; charset=iso-8859-1\n  + text/html;charset=ISO-8859-1\n\n * Cache-Control (any of these options):\n\n  + no-store, no-cache, must-revalidate, post-check=0, pre-check=0\n  + post-check=0, pre-check=0\n\n * Connection (any of these options):\n\n  + close\n  + Keep-Alive\n\n * Quotes types must be double for ETag field:\n\n  + ETag: "0", instead of ETag: \'0\'\n\n * E-Tag length (any of these options):\n\n  + 0\n  + 20\n  + 21\n  + 23\n\n * Pragma (any of these options):\n\n  + no-cache\n\n * Format of headers. After a bash, the letter is uncapitalized, for http headers. For example:\n\n  + Content-type, instead of Content-\\*\\*T\\*\\*ype.\n\n * Has spaces between names and values. For example:\n\n  + E-Tag:0; instead of: E-Tag:0\n\n * Protocol name used in request is \'HTTP\'. For example:\n\n  + GET / HTTP/1.1\n\n * The status text for a response of HTTP.\n\n   GET / HTTP/1.1\n   Host: misite.com\n\n   HTTP/1.1 200 \\*\\*OK\\*\\*\n   \\.\\.\\.\\.\n\n * X-Powered-By (any of these options):\n\n  + PHP/4.1.2\n  + PHP/4.2.2\n  + PHP/4.3.11\n'

class ServerFingerprinting(TestingPlugin):
    """
    Plugin to fingerprint web servers.
    """

    def get_accepted_info(self):
        return [
         BaseUrl]

    def recv_info(self, info):
        """
        Main function for server fingerprint. Get an URL and return the fingerprint results.

        :param info: Folder URL.
        :type info: FolderUrl

        :return: Fingerprint.
        :rtype: WebServerFingerprint
        """
        m_main_url = info.url
        Logger.log_more_verbose('Starting webserver fingerprinting plugin for site: %s' % m_main_url)
        m_server_name, m_server_version, m_canonical_name, m_webserver_complete_desc, m_related_webservers, m_others = http_simple_analyzer(m_main_url, self.update_status, 5)
        Logger.log_more_verbose('Fingerprint - Server: %s | Version: %s' % (m_server_name, m_server_version))
        m_return = WebServerFingerprint(m_server_name, m_server_version, m_webserver_complete_desc, m_canonical_name, m_related_webservers, m_others)
        m_return.add_resource(info)
        return m_return


def http_simple_analyzer(main_url, update_status_func, number_of_entries=4):
    """Simple method to get fingerprint server info

    :param main_url: Base url to test.
    :type main_url: str

    :param update_status_func: function used to update the status of the process
    :type update_status_func: function

    :param number_of_entries: number of resutls tu return for most probable web servers detected.
    :type number_of_entries: int

    :return: a typle as format: Web server family, Web server version, Web server complete description, related web servers (as a dict('SERVER_RELATED' : set(RELATED_NAMES))), others web server with their probabilities as a dict(CONCRETE_WEB_SERVER, PROBABILITY)
    """
    m_actions = {'GET': {'wordlist': 'Wordlist_get', 'weight': 1, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/'}, 'LONG_GET': {'wordlist': 'Wordlist_get_long', 'weight': 1, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/%s' % ('a' * 200)}, 'NOT_FOUND': {'wordlist': 'Wordlist_get_notfound', 'weight': 2, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/404_NOFOUND__X02KAS'}, 'HEAD': {'wordlist': 'Wordlist_head', 'weight': 3, 'protocol': 'HTTP/1.1', 'method': 'HEAD', 'payload': '/'}, 'OPTIONS': {'wordlist': 'Wordlist_options', 'weight': 2, 'protocol': 'HTTP/1.1', 'method': 'OPTIONS', 'payload': '/'}, 'DELETE': {'wordlist': 'Wordlist_delete', 'weight': 5, 'protocol': 'HTTP/1.1', 'method': 'DELETE', 'payload': '/'}, 'TEST': {'wordlist': 'Wordlist_attack', 'weight': 5, 'protocol': 'HTTP/1.1', 'method': 'TEST', 'payload': '/'}, 'INVALID': {'wordlist': 'Wordlist_wrong_method', 'weight': 5, 'protocol': 'HTTP/9.8', 'method': 'GET', 'payload': '/'}, 'ATTACK': {'wordlist': 'Wordlist_wrong_version', 'weight': 2, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/etc/passwd?format=%%%%&xss="><script>alert(\'xss\');</script>&traversal=../../&sql=\'%20OR%201;'}}
    m_d = ParsedURL(main_url)
    m_hostname = m_d.hostname
    m_port = m_d.port
    m_debug = False
    i = 0
    m_counters = HTTPAnalyzer()
    m_data_len = len(m_actions)
    m_banners_counter = Counter()
    for l_action, v in m_actions.iteritems():
        if m_debug:
            print '###########'
        l_method = v['method']
        l_payload = v['payload']
        l_proto = v['protocol']
        l_weight = v['weight']
        l_raw_request = '%(method)s %(payload)s %(protocol)s\r\nHost: %(host)s\r\n\r\n' % {'method': l_method, 
           'payload': l_payload, 
           'protocol': l_proto, 
           'host': m_hostname, 
           'port': m_port}
        if m_debug:
            print 'REQUEST'
            print l_raw_request
        l_response = None
        try:
            m_raw_request = HTTP_Raw_Request(l_raw_request)
            discard_data(m_raw_request)
            l_response = HTTP.make_raw_request(host=m_hostname, port=m_port, raw_request=m_raw_request, callback=check_raw_response)
            if l_response:
                discard_data(l_response)
        except NetworkException as e:
            Logger.log_error_more_verbose("Server-Fingerprint plugin: No response for URL (%s) with method '%s'. Message: %s" % (m_hostname, l_method, str(e)))
            continue

        if not l_response:
            Logger.log_error_more_verbose("No response for host '%s' with method '%s'." % (m_hostname, l_method))
            continue
        if m_debug:
            print 'RESPONSE'
            print l_response.raw_headers
        update_status_func(float(i) * 100.0 / float(m_data_len))
        Logger.log_more_verbose("Making '%s' test." % l_method)
        i += 1
        try:
            m_banners_counter[l_response.headers['Server']] += l_weight
        except KeyError:
            pass

        l_server_name = None
        try:
            l_server_name = l_response.headers['Server']
        except KeyError:
            continue

        m_counters.simple_inc(l_server_name, l_method, l_weight)

    return parse_analyzer_results(m_counters, m_banners_counter, number_of_entries)


def http_analyzers(main_url, update_status_func, number_of_entries=4):
    """
    Analyze HTTP headers for detect the web server. Return a list with most possible web servers.

    :param main_url: Base url to test.
    :type main_url: str

    :param update_status_func: function used to update the status of the process
    :type update_status_func: function

    :param number_of_entries: number of resutls tu return for most probable web servers detected.
    :type number_of_entries: int

    :return: Web server family, Web server version, Web server complete description, related web servers (as a dict('SERVER_RELATED' : set(RELATED_NAMES))), others web server with their probabilities as a dict(CONCRETE_WEB_SERVER, PROBABILITY)
    """
    m_wordlists_HTTP_fields = {'Accept-Ranges': 'accept-range', 
       'Server': 'banner', 
       'Cache-Control': 'cache-control', 
       'Connection': 'connection', 
       'Content-Type': 'content-type', 
       'WWW-Authenticate': 'htaccess-realm', 
       'Pragma': 'pragma', 
       'X-Powered-By': 'x-powered-by'}
    m_actions = {'GET': {'wordlist': 'Wordlist_get', 'weight': 1, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/'}, 'LONG_GET': {'wordlist': 'Wordlist_get_long', 'weight': 1, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/%s' % ('a' * 200)}, 'NOT_FOUND': {'wordlist': 'Wordlist_get_notfound', 'weight': 2, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/404_NOFOUND__X02KAS'}, 'HEAD': {'wordlist': 'Wordlist_head', 'weight': 3, 'protocol': 'HTTP/1.1', 'method': 'HEAD', 'payload': '/'}, 'OPTIONS': {'wordlist': 'Wordlist_options', 'weight': 2, 'protocol': 'HTTP/1.1', 'method': 'OPTIONS', 'payload': '/'}, 'DELETE': {'wordlist': 'Wordlist_delete', 'weight': 5, 'protocol': 'HTTP/1.1', 'method': 'DELETE', 'payload': '/'}, 'TEST': {'wordlist': 'Wordlist_attack', 'weight': 5, 'protocol': 'HTTP/1.1', 'method': 'TEST', 'payload': '/'}, 'INVALID': {'wordlist': 'Wordlist_wrong_method', 'weight': 5, 'protocol': 'HTTP/9.8', 'method': 'GET', 'payload': '/'}, 'ATTACK': {'wordlist': 'Wordlist_wrong_version', 'weight': 2, 'protocol': 'HTTP/1.1', 'method': 'GET', 'payload': '/etc/passwd?format=%%%%&xss="><script>alert(\'xss\');</script>&traversal=../../&sql=\'%20OR%201;'}}
    m_d = ParsedURL(main_url)
    m_hostname = m_d.hostname
    m_port = m_d.port
    m_debug = False
    m_banners_counter = Counter()
    m_counters = HTTPAnalyzer(debug=m_debug)
    m_data_len = len(m_actions)
    i = 1
    for l_action, v in m_actions.iteritems():
        if m_debug:
            print '###########'
        l_method = v['method']
        l_payload = v['payload']
        l_proto = v['protocol']
        l_wordlist = v['wordlist']
        l_weight = v['weight']
        l_url = urljoin(main_url, l_payload)
        l_raw_request = '%(method)s %(payload)s %(protocol)s\r\nHost: %(host)s\r\n\r\n' % {'method': l_method, 
           'payload': l_payload, 
           'protocol': l_proto, 
           'host': m_hostname, 
           'port': m_port}
        if m_debug:
            print 'REQUEST'
            print l_raw_request
        l_response = None
        try:
            m_raw_request = HTTP_Raw_Request(l_raw_request)
            discard_data(m_raw_request)
            l_response = HTTP.make_raw_request(host=m_hostname, port=m_port, raw_request=m_raw_request, callback=check_raw_response)
            if l_response:
                discard_data(l_response)
        except NetworkException as e:
            Logger.log_error_more_verbose("Server-Fingerprint plugin: No response for URL (%s) '%s'. Message: %s" % (l_method, l_url, str(e)))
            continue

        if not l_response:
            Logger.log_error_more_verbose("No response for URL '%s'." % l_url)
            continue
        if m_debug:
            print 'RESPONSE'
            print l_response.raw_headers
        update_status_func(float(i) * 100.0 / float(m_data_len))
        Logger.log_more_verbose("Making '%s' test." % l_wordlist)
        i += 1
        try:
            m_banners_counter[l_response.headers['Server']] += l_weight
        except KeyError:
            pass

        for l_http_header_name, l_header_wordlist in m_wordlists_HTTP_fields.iteritems():
            if l_http_header_name not in l_response.headers:
                continue
            l_curr_header_value = l_response.headers[l_http_header_name]
            l_wordlist_path = Config.plugin_extra_config[l_wordlist][l_header_wordlist]
            l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(l_wordlist_path)
            l_matches = l_wordlist_instance.matches_by_value(l_curr_header_value)
            m_counters.inc(l_matches, l_action, l_weight, l_http_header_name, message='HTTP field: ' + l_curr_header_value)

        l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['statuscode'])
        l_matches = l_wordlist_instance.matches_by_value(l_response.status)
        m_counters.inc(l_matches, l_action, l_weight, 'statuscode', message='Status code: ' + l_response.status)
        l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['statustext'])
        l_matches = l_wordlist_instance.matches_by_value(l_response.reason)
        m_counters.inc(l_matches, l_action, l_weight, 'statustext', message='Status text: ' + l_response.reason)
        l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['header-space'])
        try:
            l_http_value = l_response.headers[0]
            l_spaces_num = str(abs(len(l_http_value) - len(l_http_value.lstrip())))
            l_matches = l_wordlist_instance.matches_by_value(l_spaces_num)
            m_counters.inc(l_matches, l_action, l_weight, 'header-space', message='Header space: ' + l_spaces_num)
        except IndexError:
            print 'index error header space'

        l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['header-capitalafterdash'])
        l_valid_fields = [ x for x in l_response.headers.iterkeys() if '-' in x ]
        if l_valid_fields:
            l_h = l_valid_fields[0]
            l_value = l_h.split('-')[1]
            l_dush = None
            if l_value[0].isupper():
                l_dush = 1
            else:
                l_dush = 0
            l_matches = l_wordlist_instance.matches_by_value(l_dush)
            m_counters.inc(l_matches, l_action, l_weight, 'header-capitalizedafterdush', message='Capital after dash: %s' % str(l_dush))
        l_header_order = (',').join(l_response.headers.iterkeys())
        l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['header-order'])
        l_matches = l_wordlist_instance.matches_by_value(l_header_order)
        m_counters.inc(l_matches, l_action, l_weight, 'header-order', message='Header order: ' + l_header_order)
        try:
            l_proto = l_response.protocol
            if l_proto:
                l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['protocol-name'])
                l_matches = l_wordlist_instance.matches_by_value(l_proto)
                m_counters.inc(l_matches, l_action, l_weight, 'proto-name', message='Proto name: ' + l_proto)
        except IndexError:
            print 'index error protocol name'

        try:
            l_version = l_response.version
            if l_version:
                l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['protocol-version'])
                l_matches = l_wordlist_instance.matches_by_value(l_version)
                m_counters.inc(l_matches, l_action, l_weight, 'proto-version', message='Proto version: ' + l_version)
        except IndexError:
            print 'index error protocol version'

        if 'ETag' in l_response.headers:
            l_etag_header = l_response.headers['ETag']
            l_etag_len = len(l_etag_header)
            l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['etag-legth'])
            l_matches = l_wordlist_instance.matches_by_value(l_etag_len)
            m_counters.inc(l_matches, l_action, l_weight, 'etag-length', message='ETag length: ' + str(l_etag_len))
            l_etag_striped = l_etag_header.strip()
            if l_etag_striped.startswith('"') or l_etag_striped.startswith("'"):
                l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['etag-quotes'])
                l_matches = l_wordlist_instance.matches_by_value(l_etag_striped[0])
                m_counters.inc(l_matches, l_action, l_weight, 'etag-quotes', message='Etag quotes: ' + l_etag_striped[0])
        if 'Vary' in l_response.headers:
            l_vary_header = l_response.headers['Vary']
            l_var_delimiter = ', ' if l_vary_header.find(', ') else ','
            l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['vary-delimiter'])
            l_matches = l_wordlist_instance.matches_by_value(l_var_delimiter)
            m_counters.inc(l_matches, l_action, l_weight, 'vary-delimiter', message='Vary delimiter: ' + l_var_delimiter)
            l_vary_capitalizer = str(0 if l_vary_header == l_vary_header.lower() else 1)
            l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['vary-capitalize'])
            l_matches = l_wordlist_instance.matches_by_value(l_vary_capitalizer)
            m_counters.inc(l_matches, l_action, l_weight, 'vary-capitalize', message='Vary capitalizer: ' + l_vary_capitalizer)
            l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['vary-order'])
            l_matches = l_wordlist_instance.matches_by_value(l_vary_header)
            m_counters.inc(l_matches, l_action, l_weight, 'vary-order', message='Vary order: ' + l_vary_header)
        if l_action == 'HEAD':
            l_option = l_response.headers.get('Allow')
            if l_option:
                l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['options-public'])
                l_matches = l_wordlist_instance.matches_by_value(l_option)
                m_counters.inc(l_matches, l_action, l_weight, 'options-allow', message='HEAD option: ' + l_option)
        if l_action == 'OPTIONS' or l_action == 'INVALID' or l_action == 'DELETE':
            if 'Allow' in l_response.headers:
                l_option = l_response.headers.get('Allow')
                if l_option:
                    l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['options-public'])
                    l_matches = l_wordlist_instance.matches_by_value(l_option)
                    m_counters.inc(l_matches, l_action, l_weight, 'options-allow', message='OPTIONS allow: ' + l_action + ' # ' + l_option)
                l_option = l_response.headers.get('Allow')
                if l_option:
                    l_var_delimiter = ', ' if l_option.find(', ') else ','
                    l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['options-delimited'])
                    l_matches = l_wordlist_instance.matches_by_value(l_var_delimiter)
                    m_counters.inc(l_matches, l_action, l_weight, 'options-delimiter', message='OPTION allow delimiter ' + l_action + ' # ' + l_option)
            if 'Public' in l_response.headers:
                l_option = l_response.headers.get('Public')
                if l_option:
                    l_wordlist_instance = WordListLoader.get_advanced_wordlist_as_dict(Config.plugin_extra_config[l_wordlist]['options-public'])
                    l_matches = l_wordlist_instance.matches_by_value(l_option)
                    m_counters.inc(l_matches, l_action, l_weight, 'options-public', message='Public response: ' + l_action + ' # ' + l_option)

    if m_debug:
        print 'Common score'
        print m_counters.results_score.most_common(10)
        print 'Common score complete'
        print m_counters.results_score_complete.most_common(10)
        print 'Common count'
        print m_counters.results_count.most_common(10)
        print 'Common count complete'
        print m_counters.results_count_complete.most_common(10)
        print 'Determinators'
        print '============='
        for a in m_counters.results_score_complete.most_common(10):
            k = a[0]
            print ''
            print k
            print '-' * len(k)
            for l, v in m_counters.results_determinator_complete[k].iteritems():
                print '   %s (%s  [ %s ] )' % (l, (',').join(v), str(len(v)))

    return parse_analyzer_results(m_counters, m_banners_counter, number_of_entries)


def parse_analyzer_results(analyzer, banner_counter, number_of_entries=4):
    """
    Parse analyzer results and gets the values:

    :param analyzer: a HTTPAnalyzer instance.
    :type analyzer: HTTPAnalyzer

    :param banner_counter: simple Counter with a number of banner for each server
    :type banner_counter: Counter

    :return: a tuple as format (server_family, server_version, canonical_name, complete_server_name, related_servers, other_probability_servers)
    :rtype: tupple
    """
    m_other_servers_prob = OrderedDict()
    m_server_family = None
    m_server_version = None
    m_server_related = None
    m_server_complete = None
    m_server_canonical_name = None
    m_counters = analyzer
    m_banners_counter = banner_counter
    if m_counters.results_score.most_common():
        l_tmp_server_info = m_counters.results_score.most_common(1)[0][0]
        l_tmp_info = l_tmp_server_info.split('-')
        m_server_family = l_tmp_info[0]
        m_server_version = l_tmp_info[1]
        m_server_related = m_counters.related_webservers[l_tmp_server_info]
        m_server_canonical_name = m_counters.canonical_webserver_name[l_tmp_server_info]
        m_base_percent = m_counters.results_score_complete.most_common(1)[0][1]
        for v in m_counters.results_score_complete.most_common(25):
            l_server_name = v[0]
            l_server_prob = v[1]
            if m_server_family.lower() not in l_server_name.lower():
                continue
            if not m_server_complete and m_server_version in l_server_name:
                m_server_complete = l_server_name
            m_other_servers_prob[l_server_name] = float(l_server_prob) / float(m_base_percent)
            if len(m_other_servers_prob) >= number_of_entries:
                break

        if not m_server_complete:
            m_server_complete = 'Unknown'
    else:
        try:
            l_banner = m_banners_counter.most_common(n=1)[0][0]
        except IndexError:
            l_banner = 'Unknown'

        if l_banner:
            m_server_family, m_server_version, m_server_canonical_name, m_server_related = calculate_server_track(l_banner)
            m_server_complete = l_banner
            m_other_servers_prob = dict()
        else:
            m_server_family = 'Unknown'
            m_server_version = 'Unknown'
            m_server_related = set()
            m_server_canonical_name = 'Unknown'
            m_server_complete = 'Unknown web server'
            m_other_servers_prob = dict()
    return (
     m_server_family, m_server_version, m_server_canonical_name, m_server_complete, m_server_related, m_other_servers_prob)


class HTTPAnalyzer(object):

    def __init__(self, debug=False):
        self.__HTTP_fields_weight = {'accept-ranges': 1, 
           'server': 4, 
           'cache-control': 2, 
           'connection': 2, 
           'content-type': 1, 
           'etag-length': 5, 
           'etag-quotes': 2, 
           'header-capitalizedafterdush': 2, 
           'header-order': 10, 
           'header-space': 2, 
           'www-authenticate': 3, 
           'pragma': 2, 
           'proto-name': 1, 
           'proto-version': 2, 
           'statuscode': 4, 
           'statustext': 4, 
           'vary-capitalize': 2, 
           'vary-delimiter': 2, 
           'vary-order': 3, 
           'x-powered-by': 3, 
           'options-allow': 1, 
           'options-public': 2, 
           'options-delimiter': 2}
        self.__debug = debug
        self.__results_score = Counter()
        self.__results_score_complete = Counter()
        self.__results_count = Counter()
        self.__results_count_complete = Counter()
        self.__results_canonical = defaultdict(str)
        self.__results_related = defaultdict(set)
        self.__determinator = defaultdict(lambda : defaultdict(set))
        self.__determinator_complete = defaultdict(lambda : defaultdict(set))

    def inc(self, test_lists, method, method_weight, types, message=''):
        """
        Increment values associated with the fields as parameters.

        :param test_list: List with server informations.
        :type test_list: dict(KEY, list(VALUES))

        :param method: HTTP method used to make the request.
        :type method: str

        :param method_weight: The weight associated to the HTTP method.
        :type method_weight: int

        :param types: HTTP field to process.
        :type types: str

        :param message: Message to debug the method call
        :type message: str

        :return: Don't return anything
        """
        if test_lists:
            l_types = types.lower()
            if self.__debug:
                print '%s: %s' % (message, l_types)
            l_server_splited = [ calculate_server_track(server) for server in test_lists ]
            for u in l_server_splited:
                l_server = '%s-%s' % (u[0], u[1])
                self.__results_count[l_server] += 1 * method_weight
                self.__results_score[l_server] += self.__HTTP_fields_weight[l_types] * method_weight
                self.__results_canonical[l_server] = u[2]
                self.__results_related[l_server].update(u[3])
                self.__determinator[l_server][l_types].add(method)

            for l_full_server_name in test_lists:
                self.__results_count_complete[l_full_server_name] += 1 * method_weight
                self.__results_score_complete[l_full_server_name] += self.__HTTP_fields_weight[l_types] * method_weight
                self.__determinator_complete[l_full_server_name][l_types].add(method)

    def simple_inc(self, server_name, method, method_weight, message=''):
        """
        Increment values associated with the fields as parameters.

        :param server_name: String with the server name
        :type server_name: str

        :param method: HTTP method used to make the request.
        :type method: str

        :param method_weight: The weight associated to the HTTP method.
        :type method_weight: int

        :param message: Message to debug the method call
        :type message: str

        :return: Don't return anything
        """
        if server_name:
            if self.__debug:
                print '%s: %s' % (method, message)
            l_server_splited = calculate_server_track(server_name)
            l_server = '%s-%s' % (l_server_splited[0], l_server_splited[1])
            self.__results_count[l_server] += 1 * method_weight
            self.__results_canonical[l_server] = l_server_splited[2]
            self.__results_related[l_server].update(l_server_splited[3])

    @property
    def results_score(self):
        return self.__results_score

    @property
    def results_score_complete(self):
        return self.__results_score_complete

    @property
    def results_count(self):
        return self.__results_count

    @property
    def results_count_complete(self):
        return self.__results_count_complete

    @property
    def results_determinator(self):
        return self.__determinator

    @property
    def related_webservers(self):
        return self.__results_related

    @property
    def canonical_webserver_name(self):
        return self.__results_canonical

    @property
    def results_determinator_complete(self):
        return self.__determinator_complete


def check_raw_response(request, response):
    return response.content_length is not None and response.content_length < 200000


def calculate_server_track(server_name):
    """
    from nginx/1.5.1-r2 -> ("nginx", "1.5.1")

    :return: tuple with server family and their version
    :rtype: tuple(SERVER_FAMILY, SERVER_VERSION, FAMILY_CANONICAL_NAME, RELATED_WEBSERVERS=set(str(RELATED_WEBSERVERS)))
    """
    if not server_name:
        raise ValueError('Empty value')
    m_server_version_tmp_search = SERVER_PATTERN.search(server_name)
    if not m_server_version_tmp_search:
        m_server_version = 'Unknown'
    else:
        m_server_version_tmp = m_server_version_tmp_search.group(2)
        try:
            if m_server_version_tmp.count('.') == 1:
                m_server_version = m_server_version_tmp
            else:
                l_i = nindex(m_server_version_tmp, '.', 2)
                if l_i != -1:
                    m_server_version = m_server_version_tmp[:l_i]
                else:
                    m_server_version = m_server_version_tmp
        except ValueError:
            m_server_version = 'Unknown'

        m_servers_keys, m_servers_related_tmp = get_fingerprinting_wordlist(Config.plugin_config['keywords'])
        m_resultsc = Counter()
        for l_family, l_keys in m_servers_keys.iteritems():
            for k in l_keys:
                if k in server_name:
                    m_resultsc[l_family] += 1

        if len(m_resultsc.most_common(10)) == 0:
            m_server_canonical_name = 'unknown'
        else:
            m_server_canonical_name = m_resultsc.most_common(1)[0][0]
        if m_server_version_tmp_search and len(m_server_version_tmp_search.groups()) == 2:
            m_server_name = m_server_version_tmp_search.group(1)
        elif m_server_canonical_name != 'unknown':
            m_server_name = m_server_canonical_name
        else:
            m_server_name = 'unknown'
        try:
            m_servers_related = m_servers_related_tmp[m_server_canonical_name]
        except KeyError:
            m_servers_related = set()

    return (
     m_server_name, m_server_version, m_server_canonical_name, m_servers_related)


def nindex(str_in, substr, nth):
    """
    From and string get nth ocurrence of substr
    """
    m_slice = str_in
    n = 0
    m_return = None
    while nth:
        try:
            n += m_slice.index(substr) + len(substr)
            m_slice = str_in[n:]
            nth -= 1
        except ValueError:
            break

    try:
        m_return = n - 1
    except ValueError:
        m_return = 0

    return m_return


def get_fingerprinting_wordlist(wordlist):
    """
    Load the wordlist of fingerprints and prepare the info in a dict.

    It using as a keys the name of the server family and, as value, an
    iterable with the keywords related with this web server.

    :return: The results of load of webservers keywords info and related webservers.
    :rtype: tuple(WEBSERVER_KEYWORDS, RELATED_SERVES) <=>  (dict(SERVERNAME: set(str(KEYWORDS))), dict(SERVER_NAME, set(str(RELATED_SERVERS)))
    """
    m_w = WordListLoader.get_advanced_wordlist_as_dict(wordlist, separator=';', smart_load=True)
    already_parsed = set()
    related = defaultdict(set)
    m_webservers_keys = extend_items(m_w, already_parsed, related)
    return (
     m_webservers_keys, related)


def extend_items(all_items, already_parsed, related, ref=None):
    """
    Recursive function to walk the tree of fingerprinting keywords.

    Returns an ordered list with the keywords associated.

    In related dict, stores the relations. For example:

    If you have this keywordlist:

        >>> open("keywords.txt").readlines()
        iis: IIS, ISA
        hyperion: #iis

    The `related` dict would be:

        >>> print related
        defaultdict(<type 'set'>, {'iis': set(['hyperion'])})

    :param all_items: raw wordlist with references.
    :type all_items: dict

    :param already_parsed: tuples with the keys already parsed.
    :type already_parsed: Set

    :param ref: key to explore. Optional param.
    :type ref: str

    :param related: dict to store the related webservers.
    :type related: dict(SERVER_NAME, set(str(RELATED_WEBSERVER)))

    :return: Ordered dict with the discovered info.
    :rtype: OrderedDict
    """
    m_return = defaultdict(set)
    m_return_update = m_return.update
    if ref:
        try:
            if ref not in already_parsed:
                already_parsed.add(ref)
                for l_v in all_items[ref]:
                    if l_v.startswith('#'):
                        m_return_update(extend_items(all_items, already_parsed, related, ref=l_v[1:]))
                        related[l_v[1:]].add(ref)
                    else:
                        m_return[ref].add(l_v)

        except KeyError:
            pass

    else:
        for k, v in all_items.iteritems():
            if k not in already_parsed:
                already_parsed.add(k)
                for l_v in v:
                    if l_v.startswith('#'):
                        m_return_update(extend_items(all_items, already_parsed, related, ref=l_v[1:]))
                        related[l_v[1:]].add(k)
                    else:
                        m_return[k].add(l_v)

    return m_return