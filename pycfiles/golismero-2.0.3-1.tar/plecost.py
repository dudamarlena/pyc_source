# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/scan/plecost.py
# Compiled at: 2014-01-14 19:00:48
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2014\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
import re, os.path, csv
try:
    import cPickle as pickle
except ImportError:
    import pickle

from golismero.api.config import Config
from golismero.api.data.resource.url import FolderUrl
from golismero.api.data.information.html import HTML
from golismero.api.data import discard_data
from golismero.api.data.vulnerability.infrastructure.outdated_software import OutdatedSoftware
from golismero.api.text.wordlist import WordListLoader
from golismero.api.text.matching_analyzer import get_diff_ratio
from golismero.api.net.web_utils import urljoin, download, get_error_page
from golismero.api.net.http import HTTP
from golismero.api.logger import Logger
from golismero.api.plugin import TestingPlugin
base_dir = os.path.split(os.path.abspath(__file__))[0]
plecost_dir = os.path.join(base_dir, 'plecost_plugin')
plecost_plugin_list = os.path.join(plecost_dir, 'plugin_list_500.txt')
plecost_cve_data = os.path.join(plecost_dir, 'cve.dat')
del base_dir

def version_cmp(version1, version2):
    """
    Compare two software versions.

    :param version1: string with version number.
    :type version1: str

    :param version2: string with version number.
    :type version2: str

    :return: 1 if version 1 is greater. -1 if version2 if greater.
    :rtype: int
    """
    tup = lambda x: [ int(y) for y in (x + '.0.0.0.0').split('.') ][:4]
    return cmp(tup(version1), tup(version2))


class PlecostPlugin(TestingPlugin):

    def check_params(self):
        plugin_list = Config.plugin_args.get('plugin_list', '')
        if plugin_list == '':
            plugin_list = plecost_plugin_list
        if not os.path.exists(plugin_list):
            raise IOError("Plugin list file not exits: '%s'" % plugin_list)

    def get_accepted_info(self):
        return [
         FolderUrl]

    def recv_info(self, info):
        if not isinstance(info, FolderUrl):
            return
        plugin_list = Config.plugin_args.get('plugin_list', '')
        if plugin_list == '':
            plugin_list = plecost_plugin_list
        find_vulns = Config.plugin_args.get('find_vulns', '')
        if find_vulns == '':
            find_vulns = True
        wordpress_urls = Config.plugin_args.get('wordpress_urls', '')
        if wordpress_urls == '':
            wordpress_urls = 'golismero/wordpress_detector.txt'
        url = info.url
        results = []
        wordpress_found = self.__detect_wordpress_installation(url, wordpress_urls)
        Logger.log_verbose('%s WordPress instalation found.' % 'No' if wordpress_found is False else '')
        if wordpress_found is False:
            return
        current_version, last_verstion = self.__get_wordpress_version(url)
        Logger.log('WordPress installation version found: %s (latest: %s)' % (current_version, last_verstion))
        if current_version != 'unknown':
            if version_cmp(current_version, last_verstion) == -1:
                s = OutdatedSoftware(info, 'cpe:/a:wordpress:wordpress:%s' % current_version, title='Outdated version of WordPress (%s)' % current_version, description='Outdated version of wordpress found. Installed version found: %s. Latest version available: %s' % (
                 current_version, last_verstion))
                results.append(s)
        if find_vulns:
            try:
                CVE_info = pickle.load(open(plecost_cve_data, 'rb'))
            except pickle.PickleError:
                CVE_info = {}

            Logger.log('Looking for installed and outdated plugins.')
            url_parsed = info.parsed_url
            url = '%s://%s%s' % (url_parsed.scheme, url_parsed.host, url_parsed.directory)
            installed_plugins = self.__find_plugins(url, plugin_list, self.update_status)
            for plugin in installed_plugins:
                plugin_name = plugin[0]
                plugin_URL = plugin[1]
                plugin_installed_version = plugin[2]
                plugin_last_version = plugin[3]
                plugin_CVEs = plugin[4]
                if plugin_installed_version != 'unknown':
                    if version_cmp(plugin_installed_version, plugin_last_version) == -1:
                        cve_descriptions = []
                        for cve in plugin_CVEs:
                            try:
                                cve_descriptions.append('%s description: %s' % (cve, CVE_info[cve]))
                            except KeyError:
                                Logger.log_error_more_verbose("CVE '%s' not found in database. Maybe you must update your plecost plugin" % cve)

                        s = OutdatedSoftware(info, 'cpe:/a:wordpress:wordpress:-', title="Outdated version of WordPress plugin '%s'" % plugin_name, description="Outdated version of wordpress found in URL: \n'%s'.\n\n%s" % (
                         plugin_URL, ('\n').join(cve_descriptions)))
                        results.append(s)

        return results

    def __find_plugins(self, url, plugins_wordlist, update_func):
        """
        Try to find available plugins

        :param url: base URL to test.
        :type url: str

        :param plugins_wordlist: path to wordlist with plugins lists.
        :type plugins_wordlist: str

        :param update_func: function to update plugin status.
        :type update_func: function

        :return: list of lists as format:
                 list([PLUGIN_NAME, PLUGIN_URL, PLUGIN_INSTALLED_VERSION, PLUGIN_LAST_VERSION, [CVE1, CVE2...]])
        :type: list(list())
        """
        results = []
        urls_to_test = {'readme.txt': '(Stable tag:[\\svV]*)([0-9\\.]+)', 
           'README.txt': '(Stable tag:[\\svV]*)([0-9\\.]+)'}
        error_response = get_error_page(url).raw_data
        plugins = []
        plugins_append = plugins.append
        with open(plugins_wordlist, 'rU') as (f):
            for x in f:
                plugins_append(x.replace('\n', ''))

        total_plugins = len(plugins)
        csv_info = csv.reader(plugins)
        for i, plugin_row in enumerate(csv_info):
            plugin_URI = plugin_row[0]
            plugin_name = plugin_row[1]
            plugin_last_version = plugin_row[2]
            plugin_CVEs = [] if plugin_row[3] == '' else plugin_row[3].split('|')
            update_func(float(i) * 100.0 / float(total_plugins))
            partial_plugin_url = '%s/%s' % (url, 'wp-content/plugins/%s' % plugin_URI)
            for target, regex in urls_to_test.iteritems():
                plugin_url = '%s/%s' % (partial_plugin_url, target)
                p = None
                try:
                    p = HTTP.get_url(plugin_url, use_cache=False)
                    if p:
                        discard_data(p)
                except Exception as e:
                    Logger.log_error_more_verbose("Error while download: '%s': %s" % (plugin_url, str(e)))
                    continue

                plugin_installed_version = None
                if p.status == '403':
                    plugin_installed_version = 'Unknown'
                elif p.status == '200':
                    if get_diff_ratio(error_response, p.raw_response) < 0.52:
                        tmp_version = re.search(regex, p.raw_response)
                        if tmp_version is not None:
                            plugin_installed_version = tmp_version.group(2)
                if plugin_installed_version is not None:
                    Logger.log("Discovered plugin: '%s (installed version: %s)' (latest version: %s)" % (
                     plugin_name, plugin_installed_version, plugin_last_version))
                    results.append([
                     plugin_name,
                     plugin_url,
                     plugin_installed_version,
                     plugin_last_version,
                     plugin_CVEs])
                    break

        return results

    def __detect_wordpress_installation(self, url, wordpress_urls):
        """
        Try to detect a wordpress instalation in the current path.

        :param url: URL where try to find the WordPress installation.
        :type url: str

        :param wordpress_urls: string with wordlist name with WordPress URLs.
        :type wordpress_urls: str

        :return: True if wordpress installation found. False otherwise.
        :rtype: bool
        """
        Logger.log("Detecting Wordpress instalation in URI: '%s'." % url)
        total_urls = 0
        urls_found = 0
        for u in WordListLoader.get_wordlist(wordpress_urls):
            total_urls += 1
            tmp_url = urljoin(url, u)
            r = HTTP.get_url(tmp_url, use_cache=False)
            if r.status == '200':
                urls_found += 1
            discard_data(r)

        if urls_found / float(total_urls) < 0.85:
            url_wp_admin = urljoin(url, 'wp-admin/')
            try:
                p = HTTP.get_url(url_wp_admin, use_cache=False, allow_redirects=False)
                if p:
                    discard_data(p)
            except Exception as e:
                return False

            if p.status == '302' and 'wp-login.php?redirect_to=' in p.headers.get('Location', ''):
                return True
            return False
        else:
            return True

    def __get_wordpress_version(self, url):
        """
        This function get the current version of wordpress and the last version
        available for download.

        :param url: URL fo target.
        :type url: str.

        :return: a tuple with (CURRENT_VERSION, LAST_AVAILABLE_VERSION)
        :type: tuple(str, str)
        """
        url_version = {'wp-login.php': '(;ver=)([0-9\\.]+)([\\-a-z]*)', 
           'wp-admin/css/wp-admin-rtl.css': '(Version[\\s]+)([0-9\\.]+)', 
           'wp-admin/css/wp-admin.css': '(Version[\\s]+)([0-9\\.]+)'}
        url_current_version = urljoin(url, 'readme.html')
        current_version_content_1 = download(url_current_version)
        if isinstance(current_version_content_1, HTML):
            current_version_method1 = re.search('(<br/>[\\s]*[vV]ersion[\\s]*)([0-9\\.]*)', current_version_content_1.raw_data)
            if current_version_method1 is None:
                current_version_method1 = None
            elif len(current_version_method1.groups()) != 2:
                current_version_method1 = None
            else:
                current_version_method1 = current_version_method1.group(2)
        else:
            current_version_method1 = None
        current_version_content_2 = download(url)
        current_version_method2 = re.search('(<meta name=\\"generator\\" content=\\"WordPress[\\s]+)([0-9\\.]+)', current_version_content_2.raw_data)
        if current_version_method2 is None:
            current_version_method2 = None
        elif len(current_version_method2.groups()) != 2:
            current_version_method2 = None
        else:
            current_version_method2 = current_version_method2.group(2)
        current_version = 'unknown'
        if current_version_method1 is None and current_version_method2 is None:
            current_version = 'unknown'
        elif current_version_method1 is None and current_version_method2 is not None:
            current_version = current_version_method2
        elif current_version_method1 is not None and current_version_method2 is None:
            current_version = current_version_method1
        elif current_version_method1 is not None and current_version_method2 is not None:
            if current_version_method1 != current_version_method2:
                current_version = current_version_method2
            else:
                current_version = current_version_method1
        else:
            current_version = 'unknown'
        if current_version == 'unknown':
            for url_pre, regex in url_version.iteritems():
                url_current_version = urljoin(url, url_pre)
                current_version_content = download(url_current_version)
                discard_data(current_version_content)
                tmp_version = re.search(regex, current_version_content.raw_data)
                if tmp_version is not None:
                    current_version = tmp_version.group(2)
                    break

        url_last_version = 'http://wordpress.org/download/'
        last_version_content = download(url_last_version, allow_out_of_scope=True)
        if isinstance(last_version_content, HTML):
            last_version = re.search('(WordPress&nbsp;)([0-9\\.]*)', last_version_content.raw_data)
            if last_version is None:
                last_version = 'unknown'
            elif len(last_version.groups()) != 2:
                last_version = 'unknown'
            else:
                last_version = last_version.group(2)
        else:
            last_version = 'unknown'
        discard_data(current_version_content_2)
        discard_data(current_version_content_1)
        discard_data(last_version_content)
        return (
         current_version, last_version)