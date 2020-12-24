# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/shodan.py
# Compiled at: 2014-02-11 14:27:54
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.config import Config
from golismero.api.data import discard_data
from golismero.api.data.information.banner import Banner
from golismero.api.data.information.geolocation import Geolocation
from golismero.api.data.information.html import HTML
from golismero.api.data.resource.domain import Domain
from golismero.api.data.resource.ip import IP
from golismero.api.logger import Logger
from golismero.api.plugin import TestingPlugin
from golismero.api.text.text_utils import to_utf8
from shodan import WebAPI
import datetime, netaddr, traceback

class ShodanPlugin(TestingPlugin):
    """
    This plugin tries to perform passive reconnaissance on a target using
    the Shodan web API.
    """

    def check_params(self):
        self.get_api_key()

    def get_accepted_info(self):
        return [
         IP]

    def get_api_key(self):
        key = Config.plugin_args.get('apikey', None)
        if not key:
            key = Config.plugin_config.get('apikey', None)
        if not key:
            raise ValueError('Missing API key! Get one at: http://www.shodanhq.com/api_doc')
        return key

    def recv_info(self, info):
        results = []
        if info.version != 4:
            return
        else:
            ip = info.address
            parsed = netaddr.IPAddress(ip)
            if parsed.is_loopback() or parsed.is_private() or parsed.is_link_local():
                return
            try:
                key = self.get_api_key()
                api = WebAPI(key)
                shodan = api.host(ip)
            except Exception as e:
                tb = traceback.format_exc()
                Logger.log_error('Error querying Shodan: %s' % str(e))
                Logger.log_error_more_verbose(tb)
                return

            if ip != shodan.get('ip', ip):
                Logger.log_error('Shodan gave us a different IP address... weird!')
                Logger.log_error_verbose('Old IP: %s - New IP: %s' % (ip, shodan['ip']))
                ip = to_utf8(shodan['ip'])
                info = IP(ip)
                results.append(info)
            seen_host = {}
            for hostname in shodan.get('hostnames', []):
                if hostname == ip:
                    continue
                if hostname in seen_host:
                    domain = seen_host[hostname]
                else:
                    try:
                        try:
                            host = IP(hostname)
                        except ValueError:
                            host = Domain(hostname)

                    except Exception:
                        tb = traceback.format_exc()
                        Logger.log_error_more_verbose(tb)

                    seen_host[hostname] = host
                    results.append(host)
                    domain = host
                domain.add_resource(info)

            os = to_utf8(shodan.get('os'))
            if os:
                Logger.log('Host %s is running %s' % (ip, os))
            try:
                latitude = float(shodan['latitude'])
                longitude = float(shodan['longitude'])
            except Exception:
                latitude = None
                longitude = None

            if latitude is not None and longitude is not None:
                area_code = shodan.get('area_code')
                if not area_code:
                    area_code = None
                country_code = shodan.get('country_code')
                if not country_code:
                    country_code = shodan.get('country_code3')
                    if not country_code:
                        country_code = None
                country_name = shodan.get('country_name')
                if not country_name:
                    country_name = None
                city = shodan.get('city')
                if not city:
                    city = None
                dma_code = shodan.get('dma_code')
                if not dma_code:
                    dma_code = None
                postal_code = shodan.get('postal_code')
                if not postal_code:
                    postal_code = None
                region_name = shodan.get('region_name')
                if not region_name:
                    region_name = None
                geoip = Geolocation(latitude, longitude, country_code=country_code, country_name=country_name, region_name=region_name, city=city, zipcode=postal_code, metro_code=dma_code, areacode=area_code)
                results.append(geoip)
                geoip.add_resource(info)
            latest = {}
            for data in shodan.get('data', []):
                if 'banner' not in data or 'ip' not in data or 'port' not in data or 'timestamp' not in data:
                    Logger.log_error('Malformed results from Shodan?')
                    from pprint import pformat
                    Logger.log_error_more_verbose(pformat(data))
                    continue
                key = (data['ip'],
                 data['port'],
                 data['banner'])
                try:
                    timestamp = reversed(map(int, data['timestamp'].split('.', 2)))
                except Exception:
                    continue

                if key not in latest or timestamp > latest[key][0]:
                    latest[key] = (
                     timestamp, data)

            seen_isp_or_org = set()
            seen_html = set()
            for _, data in latest.values():
                for hostname in data.get('domains', []):
                    if hostname not in seen_host:
                        try:
                            domain = Domain(hostname)
                        except Exception:
                            tb = traceback.format_exc()
                            Logger.log_error_more_verbose(tb)
                            continue

                        seen_host[hostname] = domain
                        results.append(domain)

                isp = to_utf8(data.get('isp'))
                org = to_utf8(data.get('org'))
                if org and org not in seen_isp_or_org:
                    seen_isp_or_org.add(org)
                    Logger.log_verbose('Host %s belongs to: %s' % (
                     ip, org))
                if isp and (not org or isp != org) and isp not in seen_isp_or_org:
                    seen_isp_or_org.add(isp)
                    Logger.log_verbose('IP address %s is provided by ISP: %s' % (
                     ip, isp))
                raw_html = to_utf8(data.get('html'))
                if raw_html:
                    hash_raw_html = hash(raw_html)
                    if hash_raw_html not in seen_html:
                        seen_html.add(hash_raw_html)
                        try:
                            html = HTML(raw_html)
                        except Exception:
                            html = None
                            tb = traceback.format_exc()
                            Logger.log_error_more_verbose(tb)

                        if html:
                            html.add_resource(info)
                            results.append(html)
                raw_banner = to_utf8(data.get('banner'))
                try:
                    port = int(data.get('port', '0'))
                except Exception:
                    port = 0

                if raw_banner and port:
                    try:
                        banner = Banner(info, raw_banner, port)
                    except Exception:
                        banner = None
                        tb = traceback.format_exc()
                        Logger.log_error_more_verbose(tb)

                    if banner:
                        results.append(banner)

            for data in reversed(shodan.get('data', [])):
                try:
                    timestamp = reversed(map(int, data['timestamp'].split('.', 2)))
                    old_location = data.get('location')
                    if old_location:
                        old_latitude = old_location.get('latitude', latitude)
                        old_longitude = old_location.get('longitude', longitude)
                        if old_latitude is not None and old_longitude is not None and (old_latitude != latitude or old_longitude != longitude):
                            area_code = old_location.get('area_code')
                            if not area_code:
                                area_code = None
                            country_code = old_location.get('country_code')
                            if not country_code:
                                country_code = old_location.get('country_code3')
                                if not country_code:
                                    country_code = None
                            country_name = old_location.get('country_name')
                            if not country_name:
                                country_name = None
                            city = old_location.get('city')
                            if not city:
                                city = None
                            postal_code = old_location.get('postal_code')
                            if not postal_code:
                                postal_code = None
                            region_name = old_location.get('region_name')
                            if not region_name:
                                region_name = None
                            geoip = Geolocation(latitude, longitude, country_code=country_code, country_name=country_name, region_name=region_name, city=city, zipcode=postal_code, areacode=area_code)
                            if latitude is None or longitude is None:
                                latitude = old_latitude
                                longitude = old_longitude
                                results.append(geoip)
                                geoip.add_resource(info)
                            else:
                                discard_data(geoip)
                                where = str(geoip)
                                when = datetime.date(*timestamp)
                                msg = 'Host %s used to be located at %s on %s.'
                                msg %= (ip, where, when.strftime('%B %d, %Y'))
                                Logger.log_verbose(msg)
                except Exception:
                    tb = traceback.format_exc()
                    Logger.log_error_more_verbose(tb)

            return results