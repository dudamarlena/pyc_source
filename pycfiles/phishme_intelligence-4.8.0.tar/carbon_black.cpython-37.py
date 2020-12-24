# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/carbon_black/carbon_black.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 10753 bytes
import base64, json, logging, sys, os
from phishme_intelligence.core import intelligence
from phishme_intelligence.core import rest_api
from phishme_intelligence.core import sqlite
from phishme_intelligence.output.base_integration import BaseIntegration
PYTHON_MAJOR_VERSION = sys.version_info[0]

class CarbonBlack(BaseIntegration):
    __doc__ = '\n    The PhishMe Intelligence CB Response integration helper class\n    '

    def __init__(self, config, product):
        super(CarbonBlack, self).__init__(config=config, product=product)
        self.logger = logging.getLogger(__name__)
        self.rest_api = rest_api.RestApi(config=(self.config), product=(self.product))
        self.sqlite = sqlite.SQLite(location=(config.get(self.product, 'sqlite_location')), data_retention_days=(config.get(self.product, 'sqlite_data_retention_days')))
        self.headers = {'X-Auth-Token': config.get(self.product, 'api_token')}
        self.reports = []

    def process(self, mrti, threat_id):
        """
        Process PhishMe Intelligence Threat ID information into CB Response (Add PhishMe Intelligence Threat ID information
        into SQLite database)

        :param mrti: PhishMe Intelligence Threat ID information
        :type mrti: :class:`phishme_intelligence.core.intelligence.Malware`
        :param int threat_id: PhishMe Intelligence Threat ID number
        """
        self.sqlite.add_threat_id(intel=mrti)

    def post_run(self, config_file_location):
        """
        Pull threats out of a SQLite database, create a feed file, and synchronize it with CB Response

        :param str config_file_location: Path to PhishMe Intelligence integration configuration file
        """
        for json_data in self.sqlite.get_threats():
            intel = intelligence.Malware(json_data)
            self._create_report(mrti=intel)

        self._write_feed_object()

    def _write_feed_object(self):
        """
        Write all the PhishMe Intelligence reports to a CB Response feed file.

        :return None
        """
        with open(os.path.join(os.path.dirname(__file__), './phishme_logo.png'), 'rb') as (icon_file):
            icon_base64 = base64.b64encode(icon_file.read())
        with open(os.path.join(os.path.dirname(__file__), './phishme_logo_small.png'), 'rb') as (icon_small_file):
            icon_small_base64 = base64.b64encode(icon_small_file.read())
        feed = {}
        feed_info = {}
        feed_info.update(name=(self.config.get(self.product, 'feed_name')))
        feed_info.update(display_name='PhishMe Intelligence')
        feed_info.update(provider_url='http://phishme.com')
        feed_info.update(summary='PhishMe Intelligence is a reliable and timely way to stop dangerous phishing attacks.')
        feed_info.update(tech_data='This feed may not be shared outside your organization.')
        feed_info.update(category='Connectors')
        feed_info.update(icon=(icon_base64.decode('utf8')))
        feed_info.update(icon_small=(icon_small_base64.decode('utf8')))
        feed.update(feedinfo=feed_info)
        feed.update(reports=(self.reports))
        self._write_cb_feed(feed)

    def _write_cb_feed(self, feed):
        """
        Write CB Response feed file to disk

        :param str feed: CB Response feed
        """
        with open(self.config.get(self.product, 'cb_feed'), 'w+') as (file_handler):
            file_handler.write(json.dumps(feed, indent=4, sort_keys=True))

    def _create_report(self, mrti):
        """
        Add PhishMe Intelligence Threat ID data to CB Response feed

        :param mrti: PhishMe Intelligence Threat ID information
        :type mrti: :class:`phishme_intelligence.core.intelligence.Malware`
        :return None
        """
        report_base = {}
        report_base['iocs'] = {}
        report_base.update(timestamp=(int(round(mrti.last_published / 1000.0))))
        report_base.update(link=(mrti.active_threat_report))
        report_major = report_base.copy()
        report_moderate = report_base.copy()
        report_minor = report_base.copy()
        report_none = report_base.copy()
        ipv4_major, ipv4_moderate, ipv4_minor, ipv4_none, dns_major, dns_moderate, dns_minor, dns_none, md5_major, md5_none = ([] for i in range(10))
        for item in mrti.block_set:
            if item.block_type == 'Domain Name':
                if item.impact == 'Major':
                    dns_major.append(item.watchlist_ioc)
                elif item.block_type == 'Domain Name' and item.impact == 'Moderate':
                    dns_moderate.append(item.watchlist_ioc)
                elif item.block_type == 'Domain Name' and item.impact == 'Minor':
                    dns_minor.append(item.watchlist_ioc)
                elif item.block_type == 'Domain Name' and item.impact == 'None':
                    dns_none.append(item.watchlist_ioc)
                elif item.block_type == 'IPv4 Address' and item.impact == 'Major':
                    ipv4_major.append(item.watchlist_ioc)
                elif item.block_type == 'IPv4 Address' and item.impact == 'Moderate':
                    ipv4_moderate.append(item.watchlist_ioc)
                elif item.block_type == 'IPv4 Address' and item.impact == 'Minor':
                    ipv4_minor.append(item.watchlist_ioc)
                elif item.block_type == 'IPv4 Address' and item.impact == 'None':
                    ipv4_none.append(item.watchlist_ioc)
                continue

        excluded_md5 = []
        if self.config.getboolean(self.product, 'excluded_md5_use'):
            excluded_md5 = json.loads(self.config.get(self.product, 'excluded_md5'))
        for item in mrti.executable_set:
            if item.subtype == 'Otherwise benign software application repurposed for use by malware':
                if item.md5 not in md5_none and item.md5 not in excluded_md5:
                    md5_none.append(item.md5)
                elif item.md5 not in md5_major:
                    if item.md5 not in excluded_md5:
                        md5_major.append(item.md5)

        report_major_contains_data = False
        report_moderate_contains_data = False
        report_minor_contains_data = False
        report_none_contains_data = False
        report_major.update(id=(str(mrti.threat_id) + '_Major'))
        report_major.update(title=('ThreatID:' + str(mrti.threat_id) + ' ImpactRating:Major' + ' MalwareFamily:' + mrti.malware_family))
        report_major.update(score=(self.config.getint(self.product, 'impact_major')))
        report_major['iocs'] = {}
        if ipv4_major:
            report_major['iocs']['ipv4'] = ipv4_major
            report_major_contains_data = True
        if dns_major:
            report_major['iocs']['dns'] = dns_major
            report_major_contains_data = True
        if md5_major:
            report_major['iocs']['md5'] = md5_major
            report_major_contains_data = True
        report_moderate.update(id=(str(mrti.threat_id) + '_Moderate'))
        report_moderate.update(title=('ThreatID:' + str(mrti.threat_id) + ' ImpactRating:Moderate' + ' MalwareFamily:' + mrti.malware_family))
        report_moderate.update(score=(self.config.getint(self.product, 'impact_moderate')))
        report_moderate['iocs'] = {}
        if ipv4_moderate:
            report_moderate['iocs']['ipv4'] = ipv4_moderate
            report_moderate_contains_data = True
        if dns_moderate:
            report_moderate['iocs']['dns'] = dns_moderate
            report_moderate_contains_data = True
        report_minor.update(id=(str(mrti.threat_id) + '_Minor'))
        report_minor.update(title=('ThreatID:' + str(mrti.threat_id) + ' ImpactRating:Minor' + ' MalwareFamily:' + mrti.malware_family))
        report_minor.update(score=(self.config.getint(self.product, 'impact_minor')))
        report_minor['iocs'] = {}
        if ipv4_minor:
            report_minor['iocs']['ipv4'] = ipv4_minor
            report_minor_contains_data = True
        if dns_minor:
            report_minor['iocs']['dns'] = dns_minor
            report_minor_contains_data = True
        report_none.update(id=(str(mrti.threat_id) + '_None'))
        report_none.update(title=('ThreatID:' + str(mrti.threat_id) + ' ImpactRating:None' + ' MalwareFamily:' + mrti.malware_family))
        report_none.update(score=(self.config.getint(self.product, 'impact_none')))
        report_none['iocs'] = {}
        if ipv4_none:
            report_none['iocs']['ipv4'] = ipv4_none
            report_none_contains_data = True
        if dns_none:
            report_none['iocs']['dns'] = dns_none
            report_none_contains_data = True
        if md5_none:
            report_none['iocs']['md5'] = md5_none
            report_none_contains_data = True
        if report_major_contains_data:
            self.reports.append(report_major)
        if report_moderate_contains_data:
            self.reports.append(report_moderate)
        if report_minor_contains_data:
            self.reports.append(report_minor)
        if report_none_contains_data:
            self.reports.append(report_none)