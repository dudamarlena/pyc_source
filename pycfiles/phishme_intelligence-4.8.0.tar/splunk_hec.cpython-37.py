# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/splunk/splunk_hec.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 4524 bytes
import logging, requests, json
from phishme_intelligence.output.base_integration import BaseIntegration
from phishme_intelligence.output.product.splunk.modules.intelligence import Malware

class SplunkHec(BaseIntegration):

    def __init__(self, config, product):
        super(SplunkHec, self).__init__(config=config, product=product)
        self.logger = logging.getLogger(__name__)
        self.hec_token = self.config.get('integration_splunk_hec', 'token')
        self.hec_url = self.config.get('integration_splunk_hec', 'event_url')

    def process(self, mrti, threat_id):
        self.logger.info('[Splunk HEC] processing {}'.format(threat_id))
        self.logger.info('Sending data into splunk via HEC')
        self._process_malware(Malware(mrti.json))

    def _send_to_splunk(self, event_data):
        event = {}
        event['event'] = event_data
        auth_header = {'Authorization': 'Splunk {}'.format(self.hec_token)}
        response = requests.post((self.hec_url), headers=auth_header,
          data=(json.dumps(event)),
          verify=(self.config.getboolean('integration_splunk_hec', 'verify_splunk_ssl')))
        self.logger.info('Got a response of: {}'.format(response.content))

    def _process_malware(self, malware):
        context = {'threatType':malware.get_threat_type(), 
         'brands':malware.get_brand(), 
         'id':malware.get_threat_id(), 
         'reportURL':malware.get_active_threat_report_url(), 
         'threatDetailURL':malware.get_threathq_url(), 
         'firstPublished':malware.get_first_published(), 
         'lastPublished':malware.get_last_published(), 
         'label':malware.get_label()}
        if self.config.getint('integration_splunk_hec', 'json_raw'):
            malware_reduced = malware.get_content()
            malware_reduced.pop('threatType', None)
            malware_reduced.pop('hasReport', None)
            malware_reduced.update({'cofense_event_type': 'json_raw'})
            self._send_to_splunk(malware_reduced)
        if self.config.getint('integration_splunk_hec', 'json_blockset'):
            for item in malware.get_block_set():
                item.update(context)
                item.update({'cofense_event_type': 'blockset'})
                self._send_to_splunk(item)

        if self.config.getint('integration_splunk_hec', 'json_executableset'):
            for item in malware.get_executable_set():
                item.pop('dateEntered', None)
                item.update(context)
                item.update({'cofense_event_type': 'executableset'})
                self._send_to_splunk(item)

        if self.config.getint('integration_splunk_hec', 'json_senderemailset'):
            for item in malware.get_sender_email_set():
                item.update(context)
                item.update({'cofense_event_type': 'senderemailset'})
                self._send_to_splunk(item)

        if self.config.getint('integration_splunk_hec', 'json_sendersubjectset'):
            for item in malware.get_subject_set():
                item.update(context)
                item.update({'cofense_event_type': 'sendersubjectset'})
                self._send_to_splunk(item)