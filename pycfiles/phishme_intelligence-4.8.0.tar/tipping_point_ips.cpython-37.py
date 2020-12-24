# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/tipping_point_ips/tipping_point_ips.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 4507 bytes
import logging, sys
from datetime import datetime
from phishme_intelligence.core import rest_api
from phishme_intelligence.output.base_integration import BaseIntegration
PYTHON_MAJOR_VERSION = sys.version_info[0]

class TippingPointIps(BaseIntegration):
    __doc__ = '\n    The PhishMe Intelligence TippingPoint IPS integration helper class\n    '

    def __init__(self, config, product):
        super(TippingPointIps, self).__init__(config=config, product=product)
        self.logger = logging.getLogger(__name__)
        self.rest_api = rest_api.RestApi(config=(self.config), product=(self.product))

    def _quarantine(self, watchlist_ioc, watchlist_ioc_type, tag_data):
        """
        Add IOCs to TippingPoint IPS

        :param str watchlist_ioc: IOC value from PhishMe Intelligence
        :param str watchlist_ioc_type: Type of IOC value form PhishMe Intelligence (Domain Name or IPv4 Address)
        :param str tag_data: Tags to use for IOCs
        :return: None
        """
        url = 'https://' + self.config.get(self.product, 'host_with_protocol') + '/repEntries/add'
        params = {'smsuser':self.config.get(self.product, 'user'), 
         'smspass':self.config.get(self.product, 'pass'), 
         'TagData':tag_data}
        if watchlist_ioc_type == 'Domain Name':
            params.update({'dns': watchlist_ioc})
        else:
            if watchlist_ioc_type == 'IPv4 Address':
                params.update({'ip': watchlist_ioc})
            else:
                self.logger.error('Incorrect watchlist type being sent to TippingPoint: ' + watchlist_ioc_type)
        status_code, response = self.rest_api.connect_to_api(verb='GET', url=url, params=params)
        if status_code != 200:
            print(response)

    def process(self, mrti, threat_id):
        """
        Select the correct IOCs to send to TippingPoint and format the correct context to go with them.

        :param str mrti: PhishMe Intelligence Threat ID information
        :param int threat_id: PhishMe Intelligence Threat ID number
        """
        threat_id = str(mrti.threat_id)
        last_published = datetime.fromtimestamp(mrti.last_published / 1000.0).strftime('%Y-%m-%d')
        threat_details = mrti.threathq_url
        active_threat_report = mrti.active_threat_report
        for item in mrti.block_set:
            if item.block_type == 'IPv4 Address' or item.block_type == 'Domain Name':
                impact_rating = item.impact
                tag_data = ''
                tag_data += 'PhishMeIntel_Threat-ID,' + threat_id + ','
                tag_data += 'PhishMeIntel_Malware-Family,' + item.malware_family + ','
                tag_data += 'PhishMeIntel_Impact-Rating,' + impact_rating + ','
                tag_data += 'PhishMeIntel_Role,' + item.role + ','
                tag_data += 'PhishMeIntel_Last-Published,' + last_published
                use_impact = 'impact_' + impact_rating.lower()
                if self.config.getboolean(self.product, use_impact):
                    self._quarantine(watchlist_ioc=(item.watchlist_ioc), watchlist_ioc_type=(item.block_type), tag_data=tag_data)