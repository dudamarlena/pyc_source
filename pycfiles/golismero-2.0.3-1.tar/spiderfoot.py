# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/spiderfoot.py
# Compiled at: 2014-01-14 18:58:51
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from collections import defaultdict
from csv import reader
from requests import get, post
from StringIO import StringIO
from time import sleep
from traceback import format_exc
from warnings import warn
from golismero.api.config import Config
from golismero.api.data import Database
from golismero.api.data.information.asn import ASN
from golismero.api.data.information.auth import Password
from golismero.api.data.information.banner import Banner
from golismero.api.data.information.html import HTML
from golismero.api.data.information.http import HTTP_Request, HTTP_Response
from golismero.api.data.information.portscan import Portscan
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.email import Email
from golismero.api.data.resource.ip import IP
from golismero.api.data.resource.url import Url
from golismero.api.data.vulnerability import Vulnerability
from golismero.api.data.vulnerability.malware.defaced import DefacedUrl, DefacedDomain, DefacedIP
from golismero.api.data.vulnerability.malware.malicious import MaliciousIP, MaliciousUrl, MaliciousDomain, MaliciousASN
from golismero.api.data.vulnerability.ssl.invalid_certificate import InvalidCertificate
from golismero.api.data.vulnerability.ssl.outdated_certificate import OutdatedCertificate
from golismero.api.data.vulnerability.suspicious.header import SuspiciousHeader
from golismero.api.logger import Logger
from golismero.api.net.web_utils import parse_url, urljoin
from golismero.api.plugin import TestingPlugin, ImportPlugin

class SpiderFootPlugin(TestingPlugin):

    def check_params(self):
        try:
            raw_url = Config.plugin_args['url']
            assert raw_url, 'Missing URL'
            url = parse_url(raw_url)
            assert url.scheme, 'Invalid URL'
            assert url.host, 'Invalid URL'
        except Exception as e:
            raise ValueError(str(e))

        try:
            resp = get(raw_url)
            assert resp.status_code == 200, 'HTTP error code %d' % resp.status_code
            content = resp.content
            p = content.find('<div id="aboutmodal"')
            assert p >= 0, 'Cannot determine SpiderFoot version.'
            p = content.find('<p>You are running version <b>', p)
            assert p >= 0, 'Cannot determine SpiderFoot version.'
            p += len('<p>You are running version <b>')
            q = content.find('</b>', p)
            assert q > p, 'Cannot determine SpiderFoot version.'
            version = content[p:q]
            assert map(int, version.split('.')) >= (2, 1, 1), 'GoLismero requires SpiderFoot 2.1.1 or newer, found version %s instead.' % version
        except AssertionError:
            raise
        except Exception as e:
            raise RuntimeError('Cannot connect to SpiderFoot, reason: %s' % e)

    def get_accepted_info(self):
        return [
         Domain]

    def recv_info(self, info):
        base_url = Config.plugin_args['url']
        must_delete = Config.audit_config.boolean(Config.plugin_args.get('delete', 'y'))
        scan_id = None
        try:
            resp = post(urljoin(base_url, 'startscan'), {'scanname': Config.audit_name, 
               'scantarget': info.hostname, 
               'modulelist': self.get_list('modulelist', 'module_'), 
               'typelist': self.get_list('typelist', 'type_')})
            if resp.status_code != 200:
                r = resp.content
                p = r.find('<div class="alert alert-error">')
                if p >= 0:
                    p = r.find('<h4>', p) + 4
                    q = r.find('</h4>', p)
                    m = r[p:q].strip()
                    raise RuntimeError('Could not start scan, reason: ' + m)
            try:
                interval = float(Config.plugin_args.get('interval', '5.0'))
            except Exception:
                interval = 5.0

            url_scanlist = urljoin(base_url, 'scanlist')
            last_msg = ''
            is_created = False
            scan_id = None
            while True:
                resp = get(url_scanlist)
                if resp.status_code != 200:
                    status = 'ERROR-FAILED'
                    break
                scanlist = resp.json()
                found = False
                for scan in scanlist:
                    scan_id, scan_name = scan[:2]
                    status, count = scan[-2:]
                    if scan_name == Config.audit_name:
                        found = True
                        break

                if found:
                    is_created = True
                    is_finished = status in ('FINISHED', 'ABORTED', 'ERROR-FAILED')
                    msg = 'Status: %s (%s elements%s)' % (
                     status, count,
                     ' so far' if not is_finished else '')
                    if msg != last_msg:
                        last_msg = msg
                        Logger.log_verbose(msg)
                    if is_finished:
                        break
                elif not is_created:
                    Logger.log_verbose('Status: CREATING')
                else:
                    Logger.log_verbose('Status: DELETED')
                    Logger.log_error('Scan deleted from the SpiderFoot UI, aborting!')
                    return
                sleep(interval)

            results = None
            try:
                has_partial = is_created and int(count) > 0
            except Exception:
                has_partial = is_created

            try:
                if has_partial:
                    Logger.log_error("Scan didn't finish correctly!")
                    Logger.log('Attempting to load partial results...')
                    parser = SpiderFootParser()
                    url = parse_url('scaneventresultexport', base_url)
                    url.query_params = {'id': scan_id, 'type': 'ALL'}
                    resp = get(url.url)
                    if resp.status_code != 200:
                        Logger.log_error('Could not get scan results, error code: %s' % resp.status_code)
                    else:
                        results = parser.parse(StringIO(resp.content))
                        if results:
                            if len(results) == 1:
                                Logger.log('Loaded 1 result.')
                            else:
                                Logger.log('Loaded %d results.' % len(results))
                        else:
                            Logger.log('No results loaded.')
                else:
                    Logger.log_error("Scan didn't finish correctly, aborting!")
            finally:
                try:
                    if is_created and must_delete:
                        url = parse_url('scandelete', base_url)
                        url.query_params = {'id': scan_id, 'confirm': '1'}
                        get(url.url)
                except Exception as e:
                    tb = format_exc()
                    Logger.log_error_verbose(str(e))
                    Logger.log_error_more_verbose(tb)

            return results
        except SystemExit:
            if scan_id is not None:
                try:
                    url = parse_url('stopscan', base_url)
                    url.query_params = {'id': scan_id}
                    get(url.url)
                finally:
                    if must_delete:
                        url = parse_url('scandelete', base_url)
                        url.query_params = {'id': scan_id, 'confirm': '1'}
                        get(url.url)

            raise

        return

    @staticmethod
    def get_list(name, prefix):
        return (',').join(prefix + token.strip() for token in Config.plugin_args.get(name, '').split(','))


class SpiderFootImportPlugin(ImportPlugin):

    def is_supported(self, input_file):
        if input_file and input_file.lower().endswith('.csv'):
            with open(input_file, 'rU') as (fd):
                row = reader(fd).next()
                return row == [
                 'Updated', 'Type', 'Module', 'Source', 'Data']
        return False

    def import_results(self, input_file):
        try:
            with open(input_file, 'rU') as (fd):
                results = SpiderFootParser().parse(fd)
            if results:
                Database.async_add_many(results)
        except Exception as e:
            fmt = format_exc()
            Logger.log_error('Could not load file: %s' % input_file)
            Logger.log_error_verbose(str(e))
            Logger.log_error_more_verbose(fmt)

        if results:
            data_count = len(results)
            vuln_count = sum(1 for x in results if x.is_instance(Vulnerability))
            if vuln_count == 0:
                vuln_msg = ''
            elif vuln_count == 1:
                vuln_msg = ' (1 vulnerability)'
            else:
                vuln_msg = ' (%d vulnerabilities)' % vuln_count
            Logger.log('Loaded %d %s%s from file: %s' % (
             data_count, 'results' if data_count != 1 else 'result',
             vuln_msg, input_file))
        else:
            Logger.log_error('No results found in file: %s' % input_file)


class SpiderFootParser(object):
    """
    Parses the CSV output of SpiderFoot.
    """

    def parse(self, fd):
        self.results = {}
        self.reconstruct_http_code = {}
        self.reconstruct_http_headers = {}
        self.reconstruct_http_data = {}
        self.reconstructed_http = {}
        self.strange_headers = defaultdict(set)
        self.port_scan = defaultdict(set)
        self.allow_external = Config.audit_scope.has_scope
        self.allow_subdomains = Config.audit_config.include_subdomains
        warn_data_lost = True
        iterable = reader(fd)
        assert iterable.next() == [
         'Updated', 'Type', 'Module', 'Source', 'Data'], 'Unsupported file format!'
        for row in iterable:
            try:
                if not row:
                    continue
                assert len(row) == 5, 'Broken CSV file! This may happen when using an old version of SpiderFoot.'
                _, sf_type, sf_module, source, raw_data = row
                method = getattr(self, 'sf_' + sf_type, self.sf_null)
                partial_results = method(sf_module, source, raw_data)
                self.__add_partial_results(partial_results)
            except Exception as e:
                tb = format_exc()
                Logger.log_error_verbose(str(e))
                Logger.log_error_more_verbose(tb)

        for url, headers in self.strange_headers.iteritems():
            try:
                if url in self.reconstructed_http:
                    identity = self.reconstructed_http[url]
                    resp = self.results[identity]
                    for name, value in headers:
                        vulnerability = SuspiciousHeader(resp, name, value)
                        self.__add_partial_results((vulnerability,))

                elif warn_data_lost:
                    warn('Missing information in SpiderFoot results, some data may be lost', RuntimeError)
                    warn_data_lost = False
            except Exception as e:
                tb = format_exc()
                Logger.log_error_verbose(str(e))
                Logger.log_error_more_verbose(tb)

            headers.clear()

        self.strange_headers.clear()
        if warn_data_lost and (self.reconstruct_http_code or self.reconstruct_http_headers or self.reconstruct_http_data):
            warn('Missing information in SpiderFoot results, some data may be lost', RuntimeError)
            warn_data_lost = False
        self.reconstruct_http_code.clear()
        self.reconstruct_http_headers.clear()
        self.reconstruct_http_data.clear()
        self.reconstructed_http.clear()
        for address, ports in self.port_scan:
            try:
                ip = IP(address)
                ps = Portscan(ip, (('OPEN', 'TCP', port) for port in ports))
                self.__add_partial_results((ip, ps))
            except Exception as e:
                tb = format_exc()
                Logger.log_error_verbose(str(e))
                Logger.log_error_more_verbose(tb)

        imported = self.results.values()
        self.results.clear()
        return imported

    def __add_partial_results(self, partial_results):
        if partial_results:
            try:
                iterator = iter(partial_results)
            except TypeError:
                iterator = [
                 partial_results]

            for data in iterator:
                identity = data.identity
                if identity in self.results:
                    self.results[identity].merge(data)
                else:
                    self.results[identity] = data

    def __reconstruct_http(self, raw_url):
        url = Url(raw_url)
        req = HTTP_Request(method='GET', url=raw_url)
        req.add_resource(url)
        resp = HTTP_Response(request=req, status=self.reconstruct_http_code[raw_url], headers=eval(self.reconstruct_http_headers[raw_url]), data=self.reconstruct_http_data[raw_url])
        self.reconstructed_http[raw_url] = resp.identity
        del self.reconstruct_http_code[raw_url]
        del self.reconstruct_http_headers[raw_url]
        del self.reconstruct_http_data[raw_url]
        return (url, req, resp)

    def sf_null(self, sf_module, source, raw_data):
        pass

    def sf_URL_STATIC(self, sf_module, source, raw_data):
        return Url(raw_data)

    def sf_URL_FORM(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source, method='POST')

    def sf_URL_UPLOAD(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source, method='POST')

    def sf_URL_PASSWORD(self, sf_module, source, raw_data):
        url = Url(source)
        password = Password(raw_data)
        url.add_information(password)
        return (url, password)

    def sf_URL_JAVASCRIPT(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)

    def sf_URL_JAVA_APPLET(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)

    def sf_URL_FLASH(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)

    def sf_LINKED_URL_INTERNAL(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)

    def sf_LINKED_URL_EXTERNAL(self, sf_module, source, raw_data):
        if self.allow_external:
            return Url(raw_data, referer=source)

    def sf_PROVIDER_JAVASCRIPT(self, sf_module, source, raw_data):
        return Url(raw_data, referer=source)

    def sf_INITIAL_TARGET(self, sf_module, source, raw_data):
        return Domain(raw_data)

    def sf_SUBDOMAIN(self, sf_module, source, raw_data):
        if self.allow_subdomains:
            return Domain(raw_data)

    def sf_AFFILIATE_DOMAIN(self, sf_module, source, raw_data):
        if self.allow_external:
            return Domain(raw_data)

    def sf_CO_HOSTED_SITE(self, sf_module, source, raw_data):
        if self.allow_external:
            return Domain(raw_data)

    def sf_PROVIDER_DNS(self, sf_module, source, raw_data):
        try:
            return IP(raw_data)
        except ValueError:
            return Domain(raw_data)

    def sf_PROVIDER_MAIL(self, sf_module, source, raw_data):
        try:
            return IP(raw_data)
        except ValueError:
            return Domain(raw_data)

    def sf_SIMILARDOMAIN(self, sf_module, source, raw_data):
        pass

    def sf_IP_ADDRESS(self, sf_module, source, raw_data):
        return IP(raw_data)

    def sf_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            return IP(raw_data)

    def sf_GEOINFO(self, sf_module, source, raw_data):
        pass

    def sf_EMAILADDR(self, sf_module, source, raw_data):
        return Email(raw_data)

    def sf_WEBSERVER_BANNER(self, sf_module, source, raw_data):
        parsed = parse_url(source)
        domain = Domain(parsed.host)
        banner = Banner(domain, raw_data, parsed.port)
        return (domain, banner)

    def sf_TCP_PORT_OPEN(self, sf_module, source, raw_data):
        ip, port = raw_data.split(':')
        ip = ip.strip()
        port = int(port.strip())
        self.port_scan[ip].add(port)

    def sf_TCP_PORT_OPEN_BANNER(self, sf_module, source, raw_data):
        pass

    def sf_HTTP_CODE(self, sf_module, source, raw_data):
        self.reconstruct_http_code[source] = raw_data
        if source in self.reconstruct_http_headers and source in self.reconstruct_http_data:
            return self.__reconstruct_http(source)

    def sf_WEBSERVER_HTTPHEADERS(self, sf_module, source, raw_data):
        self.reconstruct_http_headers[source] = raw_data
        if source in self.reconstruct_http_code and source in self.reconstruct_http_data:
            return self.__reconstruct_http(source)

    def sf_TARGET_WEB_CONTENT(self, sf_module, source, raw_data):
        url = Url(source)
        html = HTML(raw_data)
        url.add_information(html)
        self.reconstruct_http_data[source] = raw_data
        if source in self.reconstruct_http_code and source in self.reconstruct_http_headers:
            return (url, html) + self.__reconstruct_http(source)
        return (
         url, html)

    def sf_RAW_DATA(self, sf_module, source, raw_data):
        if sf_module in ('sfp_spider', 'sfp_xref', 'sfp_googleseach', 'sfp_bingsearch'):
            return self.sf_TARGET_WEB_CONTENT(sf_module, source, raw_data)
        if sf_module == 'sfp_dns':
            return self.sf_RAW_DNS_DATA(sf_module, source, raw_data)
        if sf_module == 'sfp_ripe':
            return self.sf_RAW_RIR_DATA(sf_module, source, raw_data)
        if sf_module == 'sfp_portscan_basic':
            return self.sf_TCP_PORT_OPEN_BANNER(sf_module, source, raw_data)
        if sf_module == 'sfp_sslcert':
            return self.sf_SSL_CERTIFICATE_RAW(sf_module, source, raw_data)

    def sf_AFFILIATE(self, sf_module, source, raw_data):
        if self.allow_external:
            if sf_module in ('sfp_dns', 'sfp_ripe'):
                return self.sf_PROVIDER_DNS(sf_module, source, raw_data)
            if sf_module in ('sfp_crossref', 'sfp_xref'):
                return self.sf_LINKED_URL_INTERNAL(sf_module, source, raw_data)

    def sf_AFFILIATE_WEB_CONTENT(self, sf_module, source, raw_data):
        if self.allow_external and sf_module == 'sfp_crossref':
            return self.sf_TARGET_WEB_CONTENT(sf_module, source, raw_data)

    def sf_SOCIAL_MEDIA(self, sf_module, source, raw_data):
        pass

    def sf_WEBSERVER_TECHNOLOGY(self, sf_module, source, raw_data):
        pass

    def sf_URL_JAVASCRIPT_FRAMEWORK(self, sf_module, source, raw_data):
        pass

    def sf_NETBLOCK(self, sf_module, source, raw_data):
        pass

    def sf_BGP_AS(self, sf_module, source, raw_data):
        return ASN(raw_data)

    def sf_RAW_RIR_DATA(self, sf_module, source, raw_data):
        pass

    def sf_RAW_DNS_DATA(self, sf_module, source, raw_data):
        pass

    def sf_PROVIDER_INTERNET(self, sf_module, source, raw_data):
        pass

    def sf_SSL_CERTIFICATE_ISSUED(self, sf_module, source, raw_data):
        pass

    def sf_SSL_CERTIFICATE_ISSUER(self, sf_module, source, raw_data):
        pass

    def sf_SSL_CERTIFICATE_RAW(self, sf_module, source, raw_data):
        pass

    def sf_SSL_CERTIFICATE_MISMATCH(self, sf_module, source, raw_data):
        domain = Domain(parse_url(source).host)
        vulnerability = InvalidCertificate(domain=domain, tool_id=sf_module)
        return (
         domain, vulnerability)

    def sf_SSL_CERTIFICATE_EXPIRED(self, sf_module, source, raw_data):
        domain = Domain(parse_url(source).host)
        vulnerability = OutdatedCertificate(domain=domain, tool_id=sf_module)
        return (
         domain, vulnerability)

    def sf_BLACKLISTED_IPADDR(self, sf_module, source, raw_data):
        ip = IP(source)
        vulnerability = MaliciousIP(ip=ip, tool_id=sf_module)
        return (
         ip, vulnerability)

    def sf_BLACKLISTED_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            ip = IP(source)
            vulnerability = MaliciousIP(ip=ip, tool_id=sf_module)
            return (
             ip, vulnerability)

    def sf_DEFACED(self, sf_module, source, raw_data):
        url = Url(source)
        vulnerability = DefacedUrl(url=url, tool_id=sf_module)
        return (
         url, vulnerability)

    def sf_DEFACED_COHOST(self, sf_module, source, raw_data):
        if self.allow_external:
            url = Url(source)
            vulnerability = DefacedUrl(url=url, tool_id=sf_module)
            return (
             url, vulnerability)

    def sf_DEFACED_AFFILIATE(self, sf_module, source, raw_data):
        if self.allow_external:
            domain = Domain(source)
            vulnerability = DefacedDomain(domain=domain, tool_id=sf_module)
            return (
             domain, vulnerability)

    def sf_DEFACED_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            ip = IP(source)
            vulnerability = DefacedIP(ip=ip, tool_id=sf_module)
            return (
             ip, vulnerability)

    def sf_MALICIOUS_SUBDOMAIN(self, sf_module, source, raw_data):
        domain = Domain(source)
        vulnerability = MaliciousDomain(domain=domain, tool_id=sf_module)
        return (
         domain, vulnerability)

    def sf_MALICIOUS_AFFILIATE(self, sf_module, source, raw_data):
        if self.allow_external:
            domain = Domain(source)
            vulnerability = MaliciousDomain(domain=domain, tool_id=sf_module)
            return (
             domain, vulnerability)

    def sf_MALICIOUS_COHOST(self, sf_module, source, raw_data):
        if self.allow_external:
            url = Url(source)
            vulnerability = MaliciousUrl(url=url, tool_id=sf_module)
            return (
             url, vulnerability)

    def sf_MALICIOUS_ASN(self, sf_module, source, raw_data):
        asn = ASN(raw_data)
        vulnerability = MaliciousASN(asn=asn, tool_id=sf_module)
        return (
         asn, vulnerability)

    def sf_MALICIOUS_IPADDR(self, sf_module, source, raw_data):
        ip = IP(source)
        vulnerability = MaliciousIP(ip=ip, tool_id=sf_module)
        return (
         ip, vulnerability)

    def sf_MALICIOUS_AFFILIATE_IPADDR(self, sf_module, source, raw_data):
        if self.allow_external:
            ip = IP(source)
            vulnerability = MaliciousIP(ip=ip, tool_id=sf_module)
            return (
             ip, vulnerability)

    def sf_WEBSERVER_STRANGEHEADER(self, sf_module, source, raw_data):
        name, value = raw_data.split(':')
        name = name.strip()
        value = value.strip()
        self.strange_headers[source].add((name, value))