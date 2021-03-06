# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/appwithlogos.py
# Compiled at: 2015-12-14 11:50:00
from healthvaultlib.utils.xmlutils import XmlUtils
from lxml import etree

class AppWithLogos:

    def __init__(self, info_element=None):
        self.id = None
        self.name = {}
        self.app_auth_required = None
        self.restrict_app_users = None
        self.is_published = None
        self.action_url = None
        self.description = {}
        self.auth_reason = {}
        self.domain_name = None
        self.client_service_token = None
        self.large_logo = {}
        self.small_logo = {}
        self.persistent_tokens = None
        self.online_base_auth_xml = None
        self.offline_base_auth_xml = None
        self.privacy_statement = None
        self.terms_of_use = None
        self.dtc_success_message = None
        self.app_attributes = None
        self.app_type = None
        self.master_app_id = None
        self.master_app_name = None
        self.created_date = None
        self.updated_date = None
        self.valid_ip_prefixes = None
        self.vocabulary_authorizations = None
        self.child_vocabulary_authorizations_ceiling = None
        self.methods = None
        self.supported_record_locations = None
        self.supported_instances = None
        self.meaningful_use_sources = None
        self.meaningful_use_sources_ceiling = None
        if info_element is not None:
            self.parse_xml(info_element)
        return

    def parse_xml(self, info_element):
        pass