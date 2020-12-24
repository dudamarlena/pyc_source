# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/splunk/phishmebrandintelligence.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 7013 bytes
"""
Copyright 2013-2017 PhishMe, Inc.  All rights reserved.

This software is provided by PhishMe, Inc. ("PhishMe") on an "as is" basis and any express or implied warranties,
including but not limited to the implied warranties of merchantability and fitness for a particular purpose, are
disclaimed in all aspects.  In no event will PhishMe be liable for any direct, indirect, special, incidental or
consequential damages relating to the use of this software, even if advised of the possibility of such damage. Use of
this software is pursuant to, and permitted only in accordance with, the agreement between you and PhishMe.
"""
import json, logging
from phishme_intelligence.output.base_integration import BaseIntegration
from splunklib import modularinput as smi

class SplunkBrandIntelligence(BaseIntegration):
    __doc__ = '\n\n    '

    def __init__(self, config, product):
        super(SplunkBrandIntelligence, self).__init__(config=config, product=product)
        self.checkpoint_dir = self.config.get('integration_splunk_brandintelligence', 'checkpoint_dir')
        self.input_name = self.config.get('integration_splunk_brandintelligence', 'input_name')
        self.event_writer = smi.EventWriter()
        self.logger = logging.getLogger(__name__)

    def process(self, mrti, threat_id):
        """
        Process JSON formatted data from PhishMe Brand Intelligence.

        :param mrti:
        :param threat_id:
        :return:
        """
        context = {'brands':mrti.brand, 
         'id':mrti.threat_id, 
         'threatDetailURL':mrti.threathq_url, 
         'firstPublished':mrti.first_published, 
         'lastPublished':mrti.last_published, 
         'screenshotURL':mrti.screenshot_url, 
         'language':mrti.language}
        if self.config.getboolean('integration_splunk_brandintelligence', 'output_action_urls'):
            for item in mrti.action_url_list:
                d = {'actionURL': item.json}
                d.update(context)
                d.update({'phishme_brand_intelligence_event_type': 'action_url'})
                event = smi.Event(data=json.dumps(d, sort_keys=True), stanza=(self.input_name))
                self.event_writer.write_event(event)

        if self.config.getboolean('integration_splunk_brandintelligence', 'output_reported_urls'):
            for item in mrti.reported_url_list:
                d = {'reportedURL': item.json}
                d.update(context)
                d.update({'phishme_brand_intelligence_event_type': 'reported_url'})
                event = smi.Event(data=json.dumps(d, sort_keys=True), stanza=(self.input_name))
                self.event_writer.write_event(event)

        for kit in mrti.kits:
            kit_context = {'kit_name':kit.kit_name, 
             'kit_size':kit.size, 
             'kit_md5':kit.md5, 
             'kit_sha1':kit.sha1, 
             'kit_sha224':kit.sha224, 
             'kit_sha256':kit.sha256, 
             'kit_sha384':kit.sha384, 
             'kit_sha512':kit.sha512, 
             'kit_ssdeep':kit.ssdeep}
            for kit_file in kit.kit_files:
                file_context = {'file_name':kit_file.file_name, 
                 'file_size':kit_file.size, 
                 'file_md5':kit_file.md5, 
                 'file_sha1':kit_file.sha1, 
                 'file_sha224':kit_file.sha224, 
                 'file_sha256':kit_file.sha256, 
                 'file_sha384':kit_file.sha384, 
                 'file_sha512':kit_file.sha512, 
                 'file_ssdeep':kit_file.ssdeep}
                for email in kit_file.observed_emails:
                    email_context = {'email_address':email.email_address, 
                     'obfuscation_type':email.obfuscation_type}
                    if self.config.getboolean('integration_splunk_brandintelligence', 'output_kit_file_emails'):
                        email_context.update(context)
                        email_context.update(file_context)
                        email_context.update(kit_context)
                        email_context.update({'phishme_brand_intelligence_event_type': 'kit_file_emails'})
                        event = smi.Event(data=json.dumps(email_context, sort_keys=True), stanza=(self.input_name))
                        self.event_writer.write_event(event)

                if self.config.getboolean('integration_splunk_brandintelligence', 'output_kit_files'):
                    file_context.update(context)
                    file_context.update(kit_context)
                    file_context.update({'phishme_brand_intelligence_event_type': 'kit_files'})
                    event = smi.Event(data=json.dumps(file_context, sort_keys=True), stanza=(self.input_name))
                    self.event_writer.write_event(event)

            if self.config.getboolean('integration_splunk_brandintelligence', 'output_kits'):
                kit_context.update(context)
                kit_context.update({'phishme_brand_intelligence_event_type': 'kits'})
                event = smi.Event(data=json.dumps(kit_context, sort_keys=True), stanza=(self.input_name))
                self.event_writer.write_event(event)

        if self.config.getboolean('integration_splunk_brandintelligence', 'output_web_components'):
            for item in mrti.web_components:
                item.update(context)
                item.update({'phishme_brand_intelligence_event_type': 'web_component'})
                event = smi.Event(data=json.dumps(item, sort_keys=True), stanza=(self.input_name))
                self.event_writer.write_event(event)

        if self.config.getboolean('integration_splunk_brandintelligence', 'output_phish_url'):
            if mrti.phish_url:
                d = {'phishURL': mrti.phish_url.json}
                d.update(context)
                d.update({'phishme_brand_intelligence_event_type': 'phish_url'})
                event = smi.Event(data=json.dumps(d, sort_keys=True), stanza=(self.input_name))
                self.event_writer.write_event(event)