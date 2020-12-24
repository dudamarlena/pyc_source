# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/scan/sslscan.py
# Compiled at: 2014-02-10 15:24:09
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: http://golismero-project.com\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
import re
from BeautifulSoup import BeautifulStoneSoup
from collections import namedtuple
from datetime import datetime
from os.path import join, split, sep
from socket import socket, AF_INET, SOCK_STREAM
from ssl import wrap_socket
from traceback import format_exc
from time import time
from golismero.api.config import Config
from golismero.api.data.db import Database
from golismero.api.data.information.fingerprint import ServiceFingerprint
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.ip import IP
from golismero.api.data.resource.url import BaseUrl
from golismero.api.data.vulnerability.ssl.insecure_algorithm import InsecureAlgorithm
from golismero.api.data.vulnerability.ssl.invalid_certificate import InvalidCertificate
from golismero.api.data.vulnerability.ssl.obsolete_protocol import ObsoleteProtocol
from golismero.api.data.vulnerability.ssl.outdated_certificate import OutdatedCertificate
from golismero.api.data.vulnerability.ssl.weak_key import WeakKey
from golismero.api.data.vulnerability.ssl.invalid_common_name import InvalidCommonName
from golismero.api.external import run_external_tool, tempfile, find_binary_in_path
from golismero.api.logger import Logger
from golismero.api.net import ConnectionSlot
from golismero.api.plugin import ImportPlugin, TestingPlugin

class SSLScanImportPlugin(ImportPlugin):

    def is_supported(self, input_file):
        if input_file and input_file.lower().endswith('.xml'):
            with open(input_file, 'rU') as (fd):
                return 'SSLScan Results' in fd.read(1024)
        return False

    def import_results(self, input_file):
        results, count = SSLScanPlugin.parse_sslscan_results(input_file)
        if results:
            Database.async_add_many(results)
            Logger.log('Loaded %d hosts and %d vulnerabilities from file: %s' % (
             len(results) - count, count, input_file))
        else:
            Logger.log_verbose('No data found in file: %s' % input_file)


class SSLScanPlugin(TestingPlugin):
    Ciphers = namedtuple('Ciphers', ['version', 'bits', 'cipher'])

    def check_params(self):
        if not find_binary_in_path('sslscan'):
            if sep == '\\':
                url = 'https://code.google.com/p/sslscan-win/'
            else:
                url = 'http://sourceforge.net/projects/sslscan/'
            raise RuntimeError('SSLScan not found! You can download it from: %s' % url)
        if Config.audit_config.proxy_addr:
            raise RuntimeError("SSLScan doesn't support scanning from behind a proxy.")
        if sep == '\\':
            from ctypes import windll, c_char_p, c_uint32, c_void_p, byref, create_string_buffer, Structure, sizeof, POINTER

            class VS_FIXEDFILEINFO(Structure):
                _fields_ = [
                 (
                  'dwSignature', c_uint32),
                 (
                  'dwStrucVersion', c_uint32),
                 (
                  'dwFileVersionMS', c_uint32),
                 (
                  'dwFileVersionLS', c_uint32),
                 (
                  'dwProductVersionMS', c_uint32),
                 (
                  'dwProductVersionLS', c_uint32),
                 (
                  'dwFileFlagsMask', c_uint32),
                 (
                  'dwFileFlags', c_uint32),
                 (
                  'dwFileOS', c_uint32),
                 (
                  'dwFileType', c_uint32),
                 (
                  'dwFileSubtype', c_uint32),
                 (
                  'dwFileDateMS', c_uint32),
                 (
                  'dwFileDateLS', c_uint32)]

            def GetFileVersionInfo(lptstrFilename):
                _GetFileVersionInfoA = windll.version.GetFileVersionInfoA
                _GetFileVersionInfoA.argtypes = [
                 c_char_p, c_uint32, c_uint32, c_void_p]
                _GetFileVersionInfoA.restype = bool
                _GetFileVersionInfoSizeA = windll.version.GetFileVersionInfoSizeA
                _GetFileVersionInfoSizeA.argtypes = [c_char_p, c_void_p]
                _GetFileVersionInfoSizeA.restype = c_uint32
                _VerQueryValueA = windll.version.VerQueryValueA
                _VerQueryValueA.argtypes = [
                 c_void_p, c_char_p, c_void_p, POINTER(c_uint32)]
                _VerQueryValueA.restype = bool
                dwLen = _GetFileVersionInfoSizeA(lptstrFilename, None)
                if dwLen:
                    lpData = create_string_buffer(dwLen)
                    success = _GetFileVersionInfoA(lptstrFilename, 0, dwLen, byref(lpData))
                    if success:
                        lpFileInfo = POINTER(VS_FIXEDFILEINFO)()
                        uLen = c_uint32(sizeof(lpFileInfo))
                        success = _VerQueryValueA(lpData, '\\', byref(lpFileInfo), byref(uLen))
                        if success:
                            sFileInfo = lpFileInfo.contents
                            if sFileInfo.dwSignature == 4277077181:
                                return sFileInfo
                return

            def LOWORD(x):
                return x & 65535

            def HIWORD(x):
                return x >> 16 & 65535

            filename = find_binary_in_path('sslscan')[0]
            filename = split(filename)[0]
            filename = join(filename, 'libeay32.dll')
            vinfo = GetFileVersionInfo(filename)
            if not vinfo:
                return
            ms = vinfo.dwFileVersionMS
            ls = vinfo.dwFileVersionLS
            a = HIWORD(ms)
            b = LOWORD(ms)
            c = HIWORD(ls)
            d = LOWORD(ls)
            if not (a > 0 or b > 9 or c > 8 or d >= 20):
                raise RuntimeError('This version of OpenSSL (%s.%s.%s.%s) has a bug on Windows that causes a crash when run from GoLismero, please replace it with a newer version from: https://slproweb.com/products/Win32OpenSSL.html' % (
                 a, b, c, d))

    def get_accepted_info(self):
        return [
         BaseUrl, ServiceFingerprint]

    def recv_info(self, info):
        if info.is_instance(BaseUrl):
            hostname = info.hostname
            if info.is_https:
                port = info.parsed_url.port
            else:
                port = 443
            return self.launch_sslscan(hostname, port)
        if info.is_instance(ServiceFingerprint):
            if info.protocol != 'SSL':
                Logger.log_more_verbose('No SSL services found in fingerprint [%s], aborting.' % info)
                return
            ip_addresses = info.find_linked_data(IP.data_type, IP.data_subtype)
            domains = set()
            for ip in ip_addresses:
                domains.update(ip.find_linked_data(Domain.data_type, Domain.data_subtype))

            results = []
            for domain in domains:
                r = self.launch_sslscan(domain.hostname, info.port)
                if r:
                    results.extend(r)

            return results
        assert False, 'Unexpected data type received: %s' % type(info)

    def launch_sslscan(self, hostname, port):
        """
        Launch SSLScan against the specified hostname and port.

        :param hostname: Hostname to test.
        :type hostname: str

        :param port: TCP port to test.
        :type port: int
        """
        if self.state.put('%s:%d' % (hostname, port), True):
            Logger.log_more_verbose('Host %s:%d already scanned, skipped.' % (
             hostname, port))
            return
        try:
            with ConnectionSlot(hostname):
                s = socket(AF_INET, SOCK_STREAM)
                try:
                    s.settimeout(4.0)
                    s.connect((hostname, port))
                    s = wrap_socket(s)
                    s.shutdown(2)
                finally:
                    s.close()

        except Exception:
            Logger.log_error_more_verbose("Host %s:%d doesn't seem to support SSL, aborting." % (
             hostname, port))
            return

        with tempfile(suffix='.xml') as (output):
            args = [
             '--no-failed',
             '--xml=' + output,
             '%s:%d' % (hostname, port)]
            Logger.log('Launching SSLScan against: %s' % hostname)
            Logger.log_more_verbose('SSLScan arguments: %s' % (' ').join(args))
            with ConnectionSlot(hostname):
                t1 = time()
                code = run_external_tool('sslscan', args, callback=Logger.log_verbose)
                t2 = time()
            if code:
                Logger.log_error('SSLScan execution failed, status code: %d' % code)
            else:
                Logger.log('SSLScan scan finished in %s seconds for target: %s' % (
                 t2 - t1, hostname))
            r, v = self.parse_sslscan_results(output)
            if v:
                Logger.log('Found %s SSL vulnerabilities.' % v)
            else:
                Logger.log('No SSL vulnerabilities found.')
            return r

    @classmethod
    def parse_sslscan_results(cls, output_filename):
        """
        Convert the output of a SSLScan run to the GoLismero data model.

        :param output_filename: Path to the output filename.
            The format should always be XML.
        :type output_filename:

        :returns: Results from the SSLScan scan, and the vulnerability count.
        :rtype: list(Domain|Vulnerability), int
        """
        Ciphers = cls.Ciphers
        results = []
        count = 0
        try:
            with open(output_filename, 'rU') as (f):
                m_info = f.read()
            try:
                m_text = m_info.encode('utf-8')
            except UnicodeDecodeError:
                m_text = m_info.decode('latin-1').encode('utf-8')

            tree = BeautifulStoneSoup(m_text)
            try:
                tags = tree.findAll('ssltest')
            except Exception as e:
                tb = format_exc()
                Logger.log_error('Error parsing XML file: %s' % str(e))
                Logger.log_error_more_verbose(tb)
                return (results, count)

            for t in tags:
                try:
                    info = Domain(t.get('host'))
                    results.append(info)
                    m_t_pk = t.find('pk')
                    if m_t_pk is not None:
                        m_self_signed = m_t_pk.get('error')
                        if m_self_signed:
                            results.append(InvalidCertificate(info))
                            count += 1
                    m_t_cn = t.find('subject')
                    if m_t_cn is not None:
                        m_cn = re.search('(CN=)([0-9a-zA-Z\\.\\*]+)', m_t_cn.text).group(2)
                        if m_cn != info.hostname:
                            results.append(InvalidCommonName(info, m_cn))
                            count += 1
                    m_t_before = t.find('not-valid-before')
                    m_t_after = t.find('not-valid-after')
                    if m_t_before is not None and m_t_after is not None:
                        m_valid_before = re.search('([a-zA-Z:0-9\\s]+)( GMT)', m_t_before.text).group(1)
                        m_valid_after = re.search('([a-zA-Z:0-9\\s]+)( GMT)', m_t_after.text).group(1)
                        m_valid_before_date = datetime.strptime(m_valid_before, '%b %d %H:%M:%S %Y')
                        m_valid_after_date = datetime.strptime(m_valid_after, '%b %d %H:%M:%S %Y')
                        if m_valid_after_date < m_valid_before_date:
                            results.append(OutdatedCertificate(info))
                            count += 1
                    m_ciphers = [ Ciphers(version=c.get('sslversion'), bits=c.get('bits'), cipher=c.get('cipher')) for c in t.findAll('cipher') if c.get('status') == 'accepted'
                                ]
                    c = [ y.cipher for y in m_ciphers if 'CBC' in y.cipher ]
                    if c:
                        results.append(InsecureAlgorithm(info, c))
                        count += 1
                    k = [ int(y.bits) for i in m_ciphers if int(y.bits) <= 56 ]
                    if k:
                        results.append(WeakKey(info, k))
                        count += 1
                    c = [ y.version for y in m_ciphers if 'SSLv1' in y.version ]
                    if c:
                        results.append(ObsoleteProtocol(info, 'SSLv1'))
                        count += 1
                except Exception as e:
                    tb = format_exc()
                    Logger.log_error_verbose(str(e))
                    Logger.log_error_more_verbose(tb)

        except Exception as e:
            tb = format_exc()
            Logger.log_error_verbose(str(e))
            Logger.log_error_more_verbose(tb)

        return (
         results, count)