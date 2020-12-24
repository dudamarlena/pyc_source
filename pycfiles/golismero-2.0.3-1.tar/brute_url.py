# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/scan/brute_url.py
# Compiled at: 2014-01-14 18:58:51
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: http://golismero-project.com\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.config import Config
from golismero.api.data import discard_data
from golismero.api.data.information.fingerprint import WebServerFingerprint
from golismero.api.data.resource.url import FolderUrl, Url
from golismero.api.data.vulnerability.information_disclosure.url_disclosure import UrlDisclosure
from golismero.api.logger import Logger
from golismero.api.net.http import HTTP
from golismero.api.net.web_utils import ParsedURL, urljoin, get_error_page
from golismero.api.text.matching_analyzer import MatchingAnalyzer, get_diff_ratio
from golismero.api.text.wordlist import WordListLoader
from golismero.api.plugin import TestingPlugin
from functools import partial
__doc__ = "\n\n.. note:\n   Acknowledgments:\n\n   We'd like to thank @capi_x for his idea on how\n   to detect fake 200 responses from servers by\n   issuing known good and bad queries and diffing\n   them to calculate the deviation.\n\n   https://twitter.com/capi_x\n"
severity_vectors = {'suffixes': 4, 
   'prefixes': 3, 
   'file_extensions': 3, 
   'permutations': 3, 
   'predictables': 4, 
   'directories': 2}

class PredictablesDisclosureBruteforcer(TestingPlugin):

    def get_accepted_info(self):
        return [
         FolderUrl]

    def recv_info(self, info):
        m_url = info.url
        Logger.log_more_verbose('Start to process URL: %r' % m_url)
        m_webserver_finger = info.get_associated_informations_by_category(WebServerFingerprint.information_type)
        m_wordlist = set()
        try:
            w = Config.plugin_extra_config['common']
            m_wordlist.update([ l_w for l_w in w.itervalues() ])
        except KeyError:
            Logger.log_error("Can't load common wordlists")

        if m_webserver_finger:
            m_webserver_finger = m_webserver_finger.pop()
            m_server_canonical_name = m_webserver_finger.canonical_name
            m_servers_related = m_webserver_finger.related
            m_wordlist_update = m_wordlist.update
            try:
                w = Config.plugin_extra_config[('%s_predictables' % m_server_canonical_name)]
                m_wordlist_update([ l_w for l_w in w.itervalues() ])
            except KeyError:
                Logger.log_error("Can't load predictables wordlists for server: '%s'." % m_server_canonical_name)

            try:
                for l_servers_related in m_servers_related:
                    w = Config.plugin_extra_config[('%s_predictables' % l_servers_related)]
                    m_wordlist_update([ l_w for l_w in w.itervalues() ])

            except KeyError as e:
                Logger.log_error("Can't load wordlists predictables wordlists for related webserver: '%s'" % e)

        m_urls = set()
        m_urls_update = m_urls.add
        for l_w in m_wordlist:
            l_loaded_wordlist = WordListLoader.get_advanced_wordlist_as_list(l_w)
            for l_wo in l_loaded_wordlist:
                try:
                    l_wo = l_wo[1:] if l_wo.startswith('/') else l_wo
                    tmp_u = urljoin(m_url, l_wo)
                except ValueError as e:
                    Logger.log_error("Failed to parse key, from wordlist, '%s'" % tmp_u)
                    continue

                m_urls_update(tmp_u)

        Logger.log_verbose('Loaded %s URLs to test.' % len(m_urls))
        m_error_response = get_error_page(m_url)
        try:
            m_store_info = MatchingAnalyzer(m_error_response.raw_data, min_ratio=0.65)
        except ValueError as e:
            Logger.log_error("There is not information for analyze when creating the matcher: '%s'" % e)
            return

        _f = partial(process_url, severity_vectors['predictables'], get_http_method(m_url), m_store_info, self.update_status, len(m_urls))
        for i, l_url in enumerate(m_urls):
            _f((i, l_url))

        return generate_results(m_store_info.unique_texts)


class SuffixesDisclosureBruteforcer(TestingPlugin):
    """
    Testing suffixes: index.php -> index_0.php
    """

    def get_accepted_info(self):
        return [
         Url]

    def recv_info(self, info):
        m_url = info.url
        m_url_parts = info.parsed_url
        if info.parsed_url.extension[1:] in ('css', 'js', 'jpeg', 'jpg', 'png', 'gif',
                                             'svg') or not m_url_parts.extension:
            Logger.log_more_verbose('Skipping URL: %s' % m_url)
            return
        Logger.log_more_verbose('Bruteforcing URL: %s' % m_url)
        m_urls = make_url_with_suffixes(get_list_from_wordlist('common_suffixes'), m_url_parts)
        m_error_response = get_error_page(m_url)
        try:
            m_store_info = MatchingAnalyzer(m_error_response.raw_data, min_ratio=0.65)
        except ValueError as e:
            Logger.log_error("There is not information for analyze when creating the matcher: '%s'" % e)
            return

        _f = partial(process_url, severity_vectors['suffixes'], get_http_method(m_url), m_store_info, self.update_status, len(m_urls))
        for i, l_url in enumerate(m_urls):
            _f((i, l_url))

        return generate_results(m_store_info.unique_texts)


class PrefixesDisclosureBruteforcer(TestingPlugin):
    """
    Testing changing extension of files
    """

    def get_accepted_info(self):
        return [
         Url]

    def recv_info(self, info):
        m_url = info.url
        m_url_parts = info.parsed_url
        if info.parsed_url.extension[1:] in ('css', 'js', 'jpeg', 'jpg', 'png', 'gif',
                                             'svg') or not m_url_parts.extension:
            Logger.log_more_verbose('Skipping URL: %s' % m_url)
            return
        Logger.log_more_verbose('Bruteforcing URL: %s' % m_url)
        m_urls = make_url_with_prefixes(get_list_from_wordlist('common_prefixes'), m_url_parts)
        m_error_response = get_error_page(m_url)
        try:
            m_store_info = MatchingAnalyzer(m_error_response.raw_data, min_ratio=0.65)
        except ValueError as e:
            Logger.log_error("There is not information for analyze when creating the matcher: '%s'" % e)
            return

        _f = partial(process_url, severity_vectors['prefixes'], get_http_method(m_url), m_store_info, self.update_status, len(m_urls))
        for i, l_url in enumerate(m_urls):
            _f((i, l_url))

        return generate_results(m_store_info.unique_texts)


class FileExtensionsDisclosureBruteforcer(TestingPlugin):
    """
    Testing changing extension of files
    """

    def get_accepted_info(self):
        return [
         Url]

    def recv_info(self, info):
        m_url = info.url
        m_url_parts = info.parsed_url
        if info.parsed_url.extension[1:] in ('css', 'js', 'jpeg', 'jpg', 'png', 'gif',
                                             'svg') or not m_url_parts.extension:
            Logger.log_more_verbose('Skipping URL: %s' % m_url)
            return
        Logger.log_more_verbose('Start to process URL: %s' % m_url)
        m_urls = make_url_changing_extensions(get_list_from_wordlist('common_extensions'), m_url_parts)
        m_error_response = get_error_page(m_url)
        try:
            m_store_info = MatchingAnalyzer(m_error_response.raw_data, min_ratio=0.65)
        except ValueError as e:
            Logger.log_error("There is not enough information to analyze when creating the matcher: '%s'" % e)
            return

        _f = partial(process_url, severity_vectors['file_extensions'], get_http_method(m_url), m_store_info, self.update_status, len(m_urls))
        for i, l_url in enumerate(m_urls):
            _f((i, l_url))

        return generate_results(m_store_info.unique_texts)


class PermutationsDisclosureBruteforcer(TestingPlugin):
    """
    Testing filename permutations
    """

    def get_accepted_info(self):
        return [
         Url]

    def recv_info(self, info):
        m_url = info.url
        m_url_parts = info.parsed_url
        if info.parsed_url.extension[1:] in ('css', 'js', 'jpeg', 'jpg', 'png', 'gif',
                                             'svg') or not m_url_parts.extension:
            Logger.log_more_verbose('Skipping URL: %s' % m_url)
            return
        Logger.log_more_verbose("Bruteforcing URL: '%s'" % m_url)
        m_urls = make_url_mutate_filename(m_url_parts)
        m_error_response = get_error_page(m_url)
        try:
            m_store_info = MatchingAnalyzer(m_error_response.raw_data, min_ratio=0.65)
        except ValueError as e:
            Logger.log_error("There is not information for analyze when creating the matcher: '%s'" % e)
            return

        _f = partial(process_url, severity_vectors['permutations'], get_http_method(m_url), m_store_info, self.update_status, len(m_urls))
        for i, l_url in enumerate(m_urls):
            _f((i, l_url))

        return generate_results(m_store_info.unique_texts)


class DirectoriesDisclosureBruteforcer(TestingPlugin):
    """
    Testing changing directories of files
    """

    def get_accepted_info(self):
        return [
         Url]

    def recv_info(self, info):
        m_url = info.url
        m_url_parts = info.parsed_url
        if info.parsed_url.extension[1:] in ('css', 'js', 'jpeg', 'jpg', 'png', 'gif',
                                             'svg') or not m_url_parts.extension:
            Logger.log_more_verbose('Skipping URL: %s' % m_url)
            return
        Logger.log_more_verbose('Bruteforcing URL: %s' % m_url)
        m_urls = make_url_changing_folder_name(m_url_parts)
        m_error_response = get_error_page(m_url)
        try:
            m_store_info = MatchingAnalyzer(m_error_response.raw_data, min_ratio=0.65)
        except ValueError as e:
            Logger.log_error("There is not information for analyze when creating the matcher: '%s'" % e)
            return

        _f = partial(process_url, severity_vectors['directories'], get_http_method(m_url), m_store_info, self.update_status, len(m_urls))
        for i, l_url in enumerate(m_urls):
            _f((i, l_url))

        return generate_results(m_store_info.unique_texts)


def process_url(risk_level, method, matcher, updater_func, total_urls, url):
    """
    Checks if an URL exits.

    :param risk_level: risk level of the tested URL, if discovered.
    :type risk_level: int

    :param method: string with HTTP method used.
    :type method: str

    :param matcher: instance of MatchingAnalyzer object.
    :type matcher: `MatchingAnalyzer`

    :param updater_func: update_status function to send updates
    :type updater_func: update_status

    :param total_urls: total number of URL to globally process.
    :type total_urls: int

    :param url: a tuple with data: (index, the URL to process)
    :type url: tuple(int, str)
    """
    i, url = url
    updater_func(float(i) * 100.0 / float(total_urls))
    p = None
    try:
        p = HTTP.get_url(url, use_cache=False, method=method)
        if p:
            discard_data(p)
    except Exception as e:
        Logger.log_error_more_verbose("Error while processing: '%s': %s" % (url, str(e)))

    if p and p.status == '200':
        if method != 'GET':
            try:
                p = HTTP.get_url(url, use_cache=False, method='GET')
                if p:
                    discard_data(p)
            except Exception as e:
                Logger.log_error_more_verbose("Error while processing: '%s': %s" % (url, str(e)))

        if matcher.analyze(p.raw_response, url=url, risk=risk_level):
            Logger.log_more_verbose("Discovered partial url: '%s'" % url)
    return


def load_wordlists(wordlists):
    """
    Load the with names pased as parameter.

    This function receives a list of names of wordlist, defined in plugin
    configuration file, and return a dict with instances of wordlists.

    :param wordlists: list with wordlists names
    :type wordlists: list

    :returns: A dict with wordlists
    :rtype: dict
    """
    m_tmp_wordlist = {}
    for l_w in wordlists:
        for wordlist_family, l_wordlists in Config.plugin_extra_config.iteritems():
            if wordlist_family.lower() in l_w.lower():
                m_tmp_wordlist[l_w] = l_wordlists

    m_return = {}
    for k, w_paths in m_tmp_wordlist.iteritems():
        m_return[k] = [ WordListLoader.get_wordlist(w) for w in w_paths ]

    return m_return


def get_http_method(url):
    """
    This function determinates if the method HEAD is available. To do that, compare between two responses:
    - One with GET method
    - One with HEAD method

    If both are seem more than 90%, the response are the same and HEAD method are not allowed.
    """
    m_head_response = HTTP.get_url(url, method='HEAD')
    discard_data(m_head_response)
    m_get_response = HTTP.get_url(url)
    discard_data(m_get_response)
    if HTTP_response_headers_analyzer(m_head_response.headers, m_get_response.headers) < 0.9:
        return 'HEAD'
    return 'GET'


def HTTP_response_headers_analyzer(response_header_1, response_header_2):
    """
    Does a HTTP comparison to determinate if two HTTP response matches with the
    same content without need the body content. To do that, remove some HTTP headers
    (like Date or Cache info).

    Return a value between 0-1 with the level of difference. 0 is lowest and 1 the highest.

    - If response_header_1 is more similar to response_header_2, value will be near to 100.
    - If response_header_1 is more different to response_header_2, value will be near to 0.

    :param response_header_1: text with http response headers.
    :type response_header_1: http headers

    :param response_header_2: text with http response headers.
    :type response_header_2: http headers
    """
    m_invalid_headers = [
     'Date',
     'Expires',
     'Last-Modified']
    m_res1 = ('').join([ '%s:%s' % (k, v) for k, v in response_header_1.iteritems() if k not in m_invalid_headers ])
    m_res2 = ('').join([ '%s:%s' % (k, v) for k, v in response_header_2.iteritems() if k not in m_invalid_headers ])
    return get_diff_ratio(m_res1, m_res2)


def generate_results(unique_texts):
    """
    Generates a list of results from a list of URLs as string format.

    :param unique_texts: list with a list of URL as string.
    :type unique_texts: list(Url)

    :return: a list of Url/UrlDiclosure.
    :type: list(Url|UrlDiclosure)
    """
    m_results = []
    m_results_append = m_results.append
    for l_match in unique_texts:
        l_url = Url(l_match.url)
        l_vuln = UrlDisclosure(l_url)
        l_vuln.risk = l_match.risk
        m_results_append(l_url)
        m_results_append(l_vuln)

    return m_results


def make_url_with_prefixes(wordlist, url_parts):
    """
    Creates a set of URLs with prefixes.

    :param wordlist: Wordlist iterator.
    :type wordlist: WordList

    :param url_parts: Parsed URL to mutate.
    :type url_parts: ParsedURL

    :returns: a set with urls.
    :rtype: set
    """
    if not isinstance(url_parts, ParsedURL):
        raise TypeError('Expected ParsedURL, got %r instead' % type(url_parts))
    if not wordlist:
        raise ValueError('Internal error!')
    m_new = url_parts.copy()
    m_return = set()
    m_return_add = m_return.add
    m_filename = m_new.filename
    for l_suffix in wordlist:
        m_new.filename = '%s_%s' % (l_suffix, m_filename)
        m_return_add(m_new.url)
        m_new.filename = '%s%s' % (l_suffix, m_filename)
        m_return_add(m_new.url)

    return m_return


def make_url_with_suffixes(wordlist, url_parts):
    """
    Creates a set of URLs with suffixes.

    :param wordlist: Wordlist iterator.
    :type wordlist: WordList

    :param url_parts: Parsed URL to mutate.
    :type url_parts: ParsedURL

    :returns: a set with urls.
    :rtype: set
    """
    if not isinstance(url_parts, ParsedURL):
        raise TypeError('Expected ParsedURL, got %r instead' % type(url_parts))
    if not wordlist:
        raise ValueError('Internal error!')
    m_new = url_parts.copy()
    m_return = set()
    m_return_add = m_return.add
    m_filename = m_new.filename
    for l_suffix in wordlist:
        m_new.filename = m_filename + str(l_suffix)
        m_return_add(m_new.url)
        m_new.filename = '%s_%s' % (m_filename, l_suffix)
        m_return_add(m_new.url)

    return m_return


def make_url_mutate_filename(url_parts):
    """
    Creates a set of URLs with mutated filenames.

    :param url_parts: Parsed URL to mutate.
    :type url_parts: ParsedURL

    :return: a set with URLs
    :rtype: set
    """
    if not isinstance(url_parts, ParsedURL):
        raise TypeError('Expected ParsedURL, got %r instead' % type(url_parts))
    m_new = url_parts.copy()
    m_new.all_extensions = m_new.all_extensions.upper()
    m_return = set()
    m_return_add = m_return.add
    m_return_add(m_new.url)
    m_new = url_parts.copy()
    filename = m_new.filename
    for n in xrange(5):
        m_new.filename = filename + str(n)
        m_return_add(m_new.url)
        m_new.filename = '%s_%s' % (filename, str(n))
        m_return_add(m_new.url)

    return m_return


def make_url_changing_folder_name(url_parts):
    """
    Creates a set of URLs with prefixes.

    :param url_parts: Parsed URL to mutate.
    :type url_parts: ParsedURL

    :returns: a set with urls.
    :rtype: set
    """
    if not isinstance(url_parts, ParsedURL):
        raise TypeError('Expected ParsedURL, got %r instead' % type(url_parts))
    m_new = url_parts.copy()
    m_return = set()
    m_return_add = m_return.add
    m_directory = m_new.directory
    if len(m_directory.split('/')) > 1:
        for n in xrange(20):
            m_new.directory = '%s%s' % (m_directory, str(n))
            m_return_add(m_new.url)

        return m_return
    return set()


def make_url_with_files_or_folder(wordlist, url_parts):
    """
    Creates a set of URLs with guessed files and subfolders.

    :param wordlist: Wordlist iterator.
    :type wordlist: WordList

    :param url_parts: Parsed URL to mutate.
    :type url_parts: ParsedURL

    :return: a set with URLs
    :rtype: set
    """
    if not isinstance(url_parts, ParsedURL):
        raise TypeError('Expected ParsedURL, got %r instead' % type(url_parts))
    if not wordlist:
        raise ValueError('Internal error!')
    m_wordlist_predictable = wordlist['predictable_files']
    if not m_wordlist_predictable:
        m_wordlist_predictable = set()
    m_wordlist_suffix = wordlist['suffixes']
    if not m_wordlist_suffix:
        m_wordlist_suffix = set()
    m_new = url_parts.copy()
    m_return = set()
    m_return_add = m_return.add
    for l_wordlist in m_wordlist_predictable:
        if not l_wordlist:
            Logger.log_error("Can't load wordlist for category: 'predictable_files'.")
            continue
        for l_path in l_wordlist:
            if l_path.startswith('#'):
                continue
            l_fixed_path = l_path[1:] if l_path.startswith('/') else l_path
            m_new.filename = l_fixed_path
            m_return_add(m_new.url)

    m_new = url_parts.copy()
    m_path = m_new.directory
    if m_path.endswith('/'):
        m_path = m_path[:-1]
    for l_wordlist in m_wordlist_suffix:
        if not l_wordlist:
            Logger.log_error("Can't load wordlist for category: 'suffixes'.")
            continue
        for l_suffix in l_wordlist:
            m_new.path = m_path + l_suffix
            m_return_add(m_new.url)

    return m_return


def make_url_changing_extensions(wordlist, url_parts):
    """
    Creates a set of URLs with alternative file extensions.

    :param wordlist: Wordlist iterator.
    :type wordlist: WordList

    :param url_parts: Parsed URL to mutate.
    :type url_parts: ParsedURL

    :return: a set with the URLs
    :rtype: set
    """
    if not isinstance(url_parts, ParsedURL):
        raise TypeError('Expected ParsedURL, got %r instead' % type(url_parts))
    if not wordlist:
        raise ValueError('Internal error!')
    m_new = url_parts.copy()
    m_return = set()
    m_return_add = m_return.add
    for l_suffix in wordlist:
        m_new.all_extensions = l_suffix
        m_return_add(m_new.url)

    return m_return


def is_folder_url(url_parts):
    """
    Determine if the given URL points to a folder or a file:

    if URL looks like:
    - www.site.com/
    - www.site.com

    then ==> Return True

    if URL looks like:
    - www.site.com/index.php
    - www.site.com/index.php?id=1&name=bb
    - www.site.com/index.php/id=1&name=bb

    then ==> Return False

    :param url_parts: Parsed URL to test.
    :type url_parts: ParsedURL

    :return: True if it's a folder, False otherwise.
    :rtype: bool
    """
    return url_parts.path.endswith('/') and not url_parts.query_char == '/'


def get_list_from_wordlist(wordlist):
    """
    Load the content of the wordlist and return a set with the content.

    :param wordlist: wordlist name.
    :type wordlist: str

    :return: a set with the results.
    :rtype result_output: set
    """
    try:
        m_commom_wordlists = set()
        for v in Config.plugin_extra_config[wordlist].itervalues():
            m_commom_wordlists.update(WordListLoader.get_advanced_wordlist_as_list(v))

        return m_commom_wordlists
    except KeyError as e:
        Logger.log_error_more_verbose(str(e))
        return set()