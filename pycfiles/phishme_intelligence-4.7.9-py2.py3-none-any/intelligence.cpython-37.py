# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robert.mcmahon@phishme.com/devstage/ise-python-libraries/intelligence/phishme_intelligence/core/intelligence.py
# Compiled at: 2019-06-06 10:09:19
# Size of source mod 2**32: 40252 bytes
from __future__ import unicode_literals, absolute_import

class Malware(object):
    __doc__ = '\n    Malware class holds a single PhishMe Intelligence object.\n    '

    def __init__(self, malware, config=None):
        """
        Initialize Malware object.

        :param str malware:
        :param ConfigParser config:
        """
        self.json = malware
        self.config = config
        self.first_published = self.json.get('firstPublished')
        self.last_published = self.json.get('lastPublished')
        self.active_threat_report = self.json.get('reportURL')
        self.threathq_url = self.json.get('threatDetailURL')
        self.threat_detail_url = self.json.get('threatDetailURL')
        self.threat_id = self.json.get('id')
        self.label = self.json.get('label')
        self.executiveSummary = self.json.get('executiveSummary')
        self.executive_summary = self.json.get('executiveSummary')
        self.active_threat_report_api = None
        self.brand = None
        self.malware_family = None
        self.block_set = None
        self.domain_set = None
        self.executable_set = None
        self.sender_ip_set = None
        self.spam_url_set = None
        self.subject_set = None
        self.sender_email_set = None

    @property
    def active_threat_report_api(self):
        """

        :return:
        """
        return self._active_threat_report_api

    @active_threat_report_api.setter
    def active_threat_report_api(self, value):
        """

        :param value:
        :return:
        """
        if self.config != None:
            normal_base_url = 'https://www.threathq.com/apiv1'
            configured_base_url = self.config.get('pm_api', 'base_url')
            if configured_base_url != normal_base_url:
                self._active_threat_report_api = self.json.get('apiReportURL').replace(normal_base_url, configured_base_url)
            else:
                self._active_threat_report_api = self.json.get('apiReportURL')
        else:
            self._active_threat_report_api = self.json.get('apiReportURL')

    @property
    def malware_family(self):
        """
        :rtype: str
        """
        return self._malware_family

    @malware_family.setter
    def malware_family(self, value):
        """
        :param value:
        :return: None
        """
        if self.json.get('malwareFamilySet'):
            family_temp = []
            for family in self.json.get('malwareFamilySet'):
                family_temp.append(family.get('familyName'))

            self._malware_family = ', '.join(family_temp)
        else:
            self._malware_family = None

    @property
    def brand(self):
        """
        :rtype: str or None
        """
        return self._brand

    @brand.setter
    def brand(self, value):
        """
        :param value:
        :return: None
        """
        if self.json.get('campaignBrandSet'):
            brand_temp = []
            for brand in self.json.get('campaignBrandSet'):
                brand_temp.append(brand.get('brand').get('text'))

            self._brand = ', '.join(brand_temp)
        else:
            self._brand = None

    @property
    def block_set(self):
        """
        :rtype: list of :class:`phishme_intelligence.core.intelligence.Malware.BlockSet`
        """
        return self._block_set

    @block_set.setter
    def block_set(self, value):
        """
        :param value:
        :return: None
        """
        return_list = []
        for item in self.json.get('blockSet'):
            return_list.append(self.BlockSet(item))

        self._block_set = return_list

    @property
    def domain_set(self):
        """
        :rtype: list of :class:`phishme_intelligence.core.intelligence.Malware.DomainSet`
        """
        return self._domain_set

    @domain_set.setter
    def domain_set(self, value):
        """

        :param value:
        :return: None
        """
        return_list = []
        for item in self.json.get('domainSet'):
            return_list.append(self.DomainSet(item))

        self._domain_set = return_list

    @property
    def executable_set(self):
        """
        :rtype: list of :class:`phishme_intelligence.core.intelligence.Malware.ExecutableSet`
        """
        return self._executable_set

    @executable_set.setter
    def executable_set(self, value):
        """

        :param value:
        :return:
        """
        return_list = []
        for item in self.json.get('executableSet'):
            return_list.append(self.ExecutableSet(item))

        self._executable_set = return_list

    @property
    def sender_ip_set(self):
        """
        :rtype: list of :class:`phishme_intelligence.core.intelligence.Malware.SenderIPSet`
        """
        return self._sender_ip_set

    @sender_ip_set.setter
    def sender_ip_set(self, value):
        """

        :param value:
        :return:
        """
        return_list = []
        for item in self.json.get('senderIpSet'):
            return_list.append(self.SenderIPSet(item))

        self._sender_ip_set = return_list

    @property
    def sender_email_set(self):
        """
        :rtype: list of :class:`phishme_intelligence.core.intelligence.Malware.SenderEmailSet`
        """
        return self._sender_email_set

    @sender_email_set.setter
    def sender_email_set(self, value):
        """

        :param value:
        :return:
        """
        return_list = []
        for item in self.json.get('senderEmailSet'):
            return_list.append(self.SenderEmailSet(item))

        self._sender_email_set = return_list

    @property
    def subject_set(self):
        """
        :rtype: list of :class:`phishme_intelligence.core.intelligence.Malware.SubjectSet`
        """
        return self._subject_set

    @subject_set.setter
    def subject_set(self, value):
        """

        :param value:
        :return: None
        """
        return_list = []
        for item in self.json.get('subjectSet'):
            return_list.append(self.SubjectSet(item))

        self._subject_set = return_list

    @property
    def spam_url_set(self):
        """
        :rtype: list of :class:`phishme_intelligence.core.intelligence.Malware.SpamURLSet`
        """
        return self._spam_url_set

    @spam_url_set.setter
    def spam_url_set(self, value):
        """

        :param value:
        :return: None
        """
        return_list = []
        for item in self.json.get('spamUrlSet'):
            return_list.append(self.SpamURLSet(item))

        self._spam_url_set = return_list

    @property
    def block_set(self):
        """

        :return:
        """
        return self._block_set

    @block_set.setter
    def block_set(self, value):
        """

        :param value:
        :return:
        """
        return_list = []
        for item in self.json.get('blockSet'):
            return_list.append(self.BlockSet(item))

        self._block_set = return_list

    @property
    def malware_family(self):
        """

        :param self:
        :return:
        """
        return self._malware_family

    @malware_family.setter
    def malware_family(self, value):
        """
        Return comma-separated list of malware families.

        :param value:
        :return:
        """
        if self.json.get('malwareFamilySet'):
            family_temp = []
            for family in self.json.get('malwareFamilySet'):
                family_temp.append(family.get('familyName'))

            self._malware_family = ', '.join(family_temp)
        else:
            self._malware_family = None

    @property
    def brand(self):
        """

        :return:
        """
        return self._brand

    @brand.setter
    def brand(self, value):
        """
        Return comma-separated list of brands.
        """
        if self.json.get('campaignBrandSet'):
            brand_temp = []
            for brand in self.json.get('campaignBrandSet'):
                brand_temp.append(brand.get('brand').get('text'))

            self._brand = ', '.join(brand_temp)
        else:
            self._brand = None

    class BlockSet(object):
        __doc__ = '\n        .. _block_set:\n\n        Each web location described in the set of watchlist indicators associated with a Threat ID has a series of description fields meant to provide detail about the nature of that indicator. Each of these corresponds to a finite set of possible entries at any given time.\n        '

        def __init__(self, block_set):
            """
            Initialize BlockSet object.

            :param str block_set: The raw JSON used to create the :class:`phishme_intelligence.core.intelligence.Malware.BlockSet` object.
            """
            self.json = block_set
            self.block_type = self.json.get('blockType')
            self.impact = self.json.get('impact')
            self.role = self.json.get('role')
            self.role_description = self.json.get('roleDescription')
            self.malware_family = None
            self.malware_family_description = None
            self.watchlist_ioc = None
            self.watchlist_ioc_host = None
            self.watchlist_ioc_path = None

        @property
        def malware_family(self):
            """
            :rtype: str or None
            """
            return self._malware_family

        @malware_family.setter
        def malware_family(self, value):
            """
            :param value:
            :return: None
            """
            try:
                self._malware_family = self.json.get('malwareFamily').get('familyName')
            except AttributeError as exception:
                try:
                    self._malware_family = None
                finally:
                    exception = None
                    del exception

        @property
        def malware_family_description(self):
            """
            :return: str or None
            """
            return self._malware_family_description

        @malware_family_description.setter
        def malware_family_description(self, value):
            """
            :param value:
            :return: None
            """
            try:
                self._malware_family_description = self.json.get('malwareFamily').get('description')
            except AttributeError as exception:
                try:
                    self._malware_family_description = None
                finally:
                    exception = None
                    del exception

        @property
        def watchlist_ioc(self):
            """
            :return: str
            """
            return self._watchlist_ioc

        @watchlist_ioc.setter
        def watchlist_ioc(self, value):
            """

            :param value:
            :return: None
            """
            if self.block_type == 'URL':
                self._watchlist_ioc = self.json.get('data_1').get('url')
            else:
                self._watchlist_ioc = self.json.get('data_1')

        @property
        def watchlist_ioc_host(self):
            """
            :return: str or None
            """
            return self._watchlist_ioc_host

        @watchlist_ioc_host.setter
        def watchlist_ioc_host(self, value):
            """

            :param value:
            :return: None
            """
            if self.block_type == 'URL':
                self._watchlist_ioc_host = self.json.get('data_1').get('host')
            else:
                self._watchlist_ioc_host = None

        @property
        def watchlist_ioc_path(self):
            """
            :return: str or None
            """
            return self._watchlist_ioc_path

        @watchlist_ioc_path.setter
        def watchlist_ioc_path(self, value):
            """

            :param value:
            :return: None
            """
            if self.block_type == 'URL':
                self._watchlist_ioc_path = self.json.get('data_1').get('path')
            else:
                self._watchlist_ioc_path = None

    class DomainSet(object):
        __doc__ = '\n        .. _domain_set:\n\n        This is the domain name of the sending address or the TO: field. These are highly likely to be spoofed and should not be relied on as the true sender.\n        '

        def __init__(self, domain_set):
            """
            Initialize DomainSet object.
            """
            self.json = domain_set
            self.domain = self.json.get('domain')
            self.total_count = self.json.get('totalCount')

    class ExecutableSet(object):
        __doc__ = '\n        .. _executable_set:\n\n        These are all the files placed on an endpoint during the course of a malware infection.\n        '

        def __init__(self, executable_set):
            """
            Initialize ExecutableSet object
            """
            self.json = executable_set
            self.file_name = executable_set.get('fileName')
            self.type = executable_set.get('type')
            self.md5 = executable_set.get('md5Hex')
            self.sha1 = executable_set.get('sha1Hex')
            self.sha224 = executable_set.get('sha224Hex')
            self.sha256 = executable_set.get('sha256Hex')
            self.sha384 = executable_set.get('sha384Hex')
            self.sha512 = executable_set.get('sha512Hex')
            self.ssdeep = executable_set.get('ssdeep')
            self.malware_family = None
            self.malware_family_description = None
            self.subtype = None
            self.severity = None

        @property
        def severity(self):
            """

            :param self:
            :return:
            """
            return self._severity

        @severity.setter
        def severity(self, value):
            """

            :param self:
            :return:
            """
            try:
                self._severity = self.json.get('severityLevel')
            except AttributeError as exception:
                try:
                    self._severity = 'Major'
                finally:
                    exception = None
                    del exception

        @property
        def subtype(self):
            """
            :rtype: str or None
            """
            return self._subtype

        @subtype.setter
        def subtype(self, value):
            """
            :param value:
            :return: None
            """
            try:
                self._subtype = self.json.get('executableSubtype').get('description')
            except AttributeError as exception:
                try:
                    self._subtype = None
                finally:
                    exception = None
                    del exception

        @property
        def malware_family(self):
            """
            :rtype: str or None
            """
            return self._malware_family

        @malware_family.setter
        def malware_family(self, value):
            """
            :param value:
            :return: None
            """
            try:
                self._malware_family = self.json.get('malwareFamily').get('familyName')
            except AttributeError as exception:
                try:
                    self._malware_family = None
                finally:
                    exception = None
                    del exception

        @property
        def malware_family_description(self):
            """
            :rtype: str or None
            """
            return self._malware_family_description

        @malware_family_description.setter
        def malware_family_description(self, value):
            """
            :param value:
            :return: None
            """
            try:
                self._malware_family_description = self.json.get('malwareFamily').get('description')
            except AttributeError as exception:
                try:
                    self._malware_family_description = None
                finally:
                    exception = None
                    del exception

    class SubjectSet(object):
        __doc__ = '\n        .. _sender_subject_set:\n\n        This is the subject line of all malicious emails determined to be part of this campaign.\n        '

        def __init__(self, subject_set):
            """
            Initialize SubjectSet object
            """
            self.json = subject_set
            self.subject = self.json.get('subject')
            self.total_count = self.json.get('totalCount')

    class SenderIPSet(object):
        __doc__ = '\n        .. _sender_ip_set:\n\n        These are the IP addresses being used to deliver the mail. Due to the nature of mail headers, some of these IPs may be spoofed.\n        '

        def __init__(self, sender_ip_set):
            """
            Initialize SenderIPSet object
            """
            self.json = sender_ip_set
            self.ip = sender_ip_set.get('ip')
            self.total_count = sender_ip_set.get('totalCount')

    class SenderEmailSet(object):
        __doc__ = '\n        .. _sender_email_set:\n\n        These are the email addresses being used to deliver the mail. Due to the nature of mail headers, some of these email addresses may be spoofed.\n        '

        def __init__(self, sender_email_set):
            """
            Initialize SenderEmailSet object
            """
            self.json = sender_email_set
            self.sender_email = sender_email_set.get('senderEmail')
            self.total_count = sender_email_set.get('totalCount')

    class SpamURLSet(object):
        __doc__ = '\n        Spam URLs (if any) associated with a particular campaign.\n        '

        def __init__(self, spam_url_set):
            """
            Initialize SpamURLSet object.
            """
            self.json = spam_url_set
            self.url = URL(self.json.get('url_1'))
            self.total_count = self.json.get('totalCount')


class IPv4(object):
    __doc__ = '\n\n    '

    def __init__(self, ipv4):
        """
        Initialize IPv4 object.
        """
        if ipv4:
            self.json = ipv4
            self.asn = ipv4.getint('asn')
            self.asn_organization = ipv4.get('asnOrganization')
            self.continent_code = ipv4.get('continentCode')
            self.continent_name = ipv4.get('continentName')
            self.country_iso_code = ipv4.get('countryIsoCode')
            self.country_name = ipv4.get('countryName')
            self.ip = ipv4.get('ip')
            self.isp = ipv4.get('isp')
            self.latitude = ipv4.get('latitude')
            self.longitude = ipv4.get('longitude')
            self.lookup_on = ipv4.get('lookupOn')
            self.metro_code = ipv4.get('metroCode')
            self.organization = ipv4.get('organization')
            self.postal_code = ipv4.get('postalCode')
            self.subdivision_name = ipv4.get('subdivisionName')
            self.subdivision_iso_code = ipv4.get('subdivisionIsoCode')
            self.time_zone = ipv4.get('timeZone')
            self.user_type = ipv4.get('userType')

    def __getattr__(self, item):
        pass


class URL(object):
    __doc__ = '\n\n    '

    def __init__(self, url):
        """
        Initialize URL object.
        """
        self.json = url
        self.domain = url.get('domain')
        self.host = url.get('host')
        self.path = url.get('path')
        self.protocol = url.get('protocol')
        self.query = url.get('query')
        self.url = url.get('url')

    def __getattr__(self, item):
        pass