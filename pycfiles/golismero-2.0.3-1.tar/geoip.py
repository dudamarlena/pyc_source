# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/plugins/testing/recon/geoip.py
# Compiled at: 2014-01-07 11:03:17
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
from golismero.api.data.information.geolocation import Geolocation
from golismero.api.data.information.traceroute import Traceroute
from golismero.api.data.resource.bssid import BSSID
from golismero.api.data.resource.ip import IP
from golismero.api.data.resource.mac import MAC
from golismero.api.logger import Logger
from golismero.api.plugin import TestingPlugin
from golismero.api.net.web_utils import json_decode
from geopy import geocoders
from shodan.wps import Skyhook
import netaddr, requests, traceback
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class GeoIP(TestingPlugin):
    """
    This plugin tries to geolocate all IP addresses and BSSIDs.
    It also enhances existing geolocation data from other sources.
    """

    def get_accepted_info(self):
        return [
         IP, MAC, BSSID, Traceroute, Geolocation]

    def recv_info(self, info):
        results = []
        if info.is_instance(Geolocation):
            if not info.street_addr:
                street_addr = self.query_google(info.latitude, info.longitude)
                if street_addr:
                    info.street_addr = street_addr
                    Logger.log('Location (%s, %s) is in %s' % (
                     info.latitude, info.longitude, street_addr))
            return
        if info.is_instance(Traceroute):
            addr_to_ip = {}
            for hop in info.hops:
                if hop is not None:
                    if hop.address and hop.address not in addr_to_ip:
                        addr_to_ip[hop.address] = IP(hop.address)

            results.extend(addr_to_ip.itervalues())
            coords_to_geoip = {}
            for res in addr_to_ip.itervalues():
                r = self.recv_info(res)
                if r:
                    for x in r:
                        if not x.is_instance(Geolocation):
                            results.append(x)
                        else:
                            key = (
                             x.latitude, x.longitude)
                            if key not in coords_to_geoip:
                                coords_to_geoip[key] = x
                                results.append(x)
                            else:
                                coords_to_geoip[key].merge(x)

            return results
        if info.is_instance(IP):
            if info.version != 4:
                return
            ip = info.address
            parsed = netaddr.IPAddress(ip)
            if parsed.is_loopback() or parsed.is_private() or parsed.is_link_local():
                return
            kwargs = self.query_freegeoip(ip)
            if not kwargs:
                return
            kwargs.pop('ip')
        else:
            if info.is_instance(BSSID) or info.is_instance(MAC):
                skyhook = self.query_skyhook(info.address)
                if not skyhook:
                    return
                kwargs = {'latitude': skyhook['latitude'], 
                   'longitude': skyhook['longitude'], 
                   'accuracy': skyhook['hpe'], 
                   'country_name': skyhook['country'], 
                   'country_code': skyhook['country_code'], 
                   'region_code': skyhook['state_code'], 
                   'region_name': skyhook['state']}
            else:
                assert False, 'Internal error! Unexpected type: %r' % type(info)
            street_addr = self.query_google(kwargs['latitude'], kwargs['longitude'])
            if street_addr:
                kwargs['street_addr'] = street_addr
            geoip = Geolocation(**kwargs)
            geoip.add_resource(info)
            results.append(geoip)
            try:
                Logger.log_verbose('%s %s is located in %s' % (
                 info.display_name, info.address, geoip))
            except Exception as e:
                fmt = traceback.format_exc()
                Logger.log_error('Error: %s' % str(e))
                Logger.log_error_more_verbose(fmt)

        return results

    @staticmethod
    def query_freegeoip(ip):
        Logger.log_more_verbose('Querying freegeoip.net for: ' + ip)
        try:
            resp = requests.get('http://freegeoip.net/json/' + ip)
            if resp.status_code == 200:
                return json_decode(resp.content)
            if resp.status_code == 404:
                Logger.log_more_verbose('No results from freegeoip.net for IP: ' + ip)
            else:
                Logger.log_more_verbose('Response from freegeoip.net for %s: %s' % (
                 ip, resp.content))
        except Exception:
            raise RuntimeError('Freegeoip.net webservice is not available, possible network error?')

    @staticmethod
    def query_google(latitude, longitude):
        coordinates = '%s, %s' % (latitude, longitude)
        Logger.log_more_verbose('Querying Google Geocoder for: %s' % coordinates)
        try:
            g = geocoders.GoogleV3()
            r = g.reverse(coordinates)
            if r:
                return r[0][0].encode('UTF-8')
        except Exception as e:
            fmt = traceback.format_exc()
            Logger.log_error_verbose('Error: %s' % str(e))
            Logger.log_error_more_verbose(fmt)

    @staticmethod
    def query_skyhook(bssid):
        Logger.log_more_verbose('Querying Skyhook for: %s' % bssid)
        try:
            r = Skyhook().locate(bssid)
            if r:
                xml = ET.fromstring(r)
                ns = '{http://skyhookwireless.com/wps/2005}'
                err = xml.find('.//%serror' % ns)
                if err is not None:
                    Logger.log_error_verbose('Response from Skyhook: %s' % err.text)
                    return
                return {'latitude': float(xml.find('.//%slatitude' % ns).text), 
                   'longitude': float(xml.find('.//%slongitude' % ns).text), 
                   'hpe': float(xml.find('.//%shpe' % ns).text), 
                   'state': xml.find('.//%sstate' % ns).text, 
                   'state_code': xml.find('.//%sstate' % ns).get('code'), 
                   'country': xml.find('.//%scountry' % ns).text, 
                   'country_code': xml.find('.//%scountry' % ns).get('code')}
        except Exception as e:
            fmt = traceback.format_exc()
            Logger.log_error_verbose('Error: %s' % str(e))
            Logger.log_error_more_verbose(fmt)

        return