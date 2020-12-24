# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/g_/2y6d621s76jb5t5dk7w7rx5m0000gp/T/pip-install-mithnhjt/phishme-intelligence/phishme_intelligence/output/product/splunk/modules/brand_intelligence.py
# Compiled at: 2019-06-01 13:35:23
# Size of source mod 2**32: 18809 bytes
from __future__ import unicode_literals, absolute_import
import logging

class Phish(object):
    __doc__ = '\n    Phish class holds a single Cofense Brand Intelligence object.\n    '

    def __init__(self, phish):
        """
        Initialize a Cofense Brand Intelligence object.

        :param str phish:
        """
        self.json = phish
        self.confirmed_date = phish.get('confirmedDate')
        self.first_published = phish.get('firstDate')
        self.last_published = phish.get('lastDate')
        self.threathq_url = phish.get('threatDetailURL')
        self.threat_id = phish.get('id')
        self.web_components = phish.get('webComponents')
        self.kits = None
        self.title = phish.get('title')
        self.language = phish.get('language')
        self.reported_url_list = None
        self.phish_url = None
        self.action_url_list = None
        self.screenshot_url = None
        self.brand = None
        self.ip = None

    @property
    def kits(self):
        """

        :return:
        """
        return self._kits

    @kits.setter
    def kits(self, value):
        """

        :param value:
        :return:
        """
        return_list = []
        for item in self.json.get('kits'):
            return_list.append(self.Kit(item))

        self._kits = return_list

    @property
    def ip(self):
        """

        :return:
        """
        return self._ip

    @ip.setter
    def ip(self, value):
        """

        :param value:
        :return:
        """
        if self.json.get('ipDetail'):
            self._ip = IPv4(self.json.get('ipDetail'))
        else:
            self._ip = None

    @property
    def phish_url(self):
        """

        :return:
        """
        return self._phish_url

    @phish_url.setter
    def phish_url(self, value):
        """

        :param value:
        :return:
        """
        if self.json.get('phishingURL_1'):
            self._phish_url = URL(self.json.get('phishingURL_1'))
        else:
            self._phish_url = None

    @property
    def screenshot_url(self):
        """

        :return:
        """
        return self._screenshot_url

    @screenshot_url.setter
    def screenshot_url(self, value):
        """

        :param value:
        :return:
        """
        try:
            self._screenshot_url = URL(self.json.get('screenshot').get('url_1')).url
        except AttributeError as exception:
            try:
                self._screenshot_url = None
            finally:
                exception = None
                del exception

    @property
    def reported_url_list(self):
        """

        :return:
        """
        return self._reported_url_list

    @reported_url_list.setter
    def reported_url_list(self, value):
        """

        :param value:
        :return:
        """
        return_list = []
        for item in self.json.get('reportedURLs_1'):
            return_list.append(URL(item))

        self._reported_url_list = return_list

    @property
    def action_url_list(self):
        """

        :return:
        """
        return self._action_url_list

    @action_url_list.setter
    def action_url_list(self, value):
        """

        :param value:
        :return:
        """
        return_list = []
        for item in self.json.get('actionURLs_1'):
            return_list.append(URL(item))

        self._action_url_list = return_list

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
        brand_temp = []
        if self.json.get('brands'):
            for brand in self.json.get('brands'):
                brand_temp.append(brand.get('text'))

            self._brand = ', '.join(brand_temp)
        else:
            self._brand = None

    class Kit(object):
        __doc__ = '\n        Kit\n        '

        def __init__(self, kit):
            """
            Initialize kit object.
            """
            self.json = kit
            self.kit_name = kit.get('kitName')
            self.size = kit.get('fileSize')
            self.md5 = kit.get('md5')
            self.sha1 = kit.get('sha1')
            self.sha224 = kit.get('sha224')
            self.sha256 = kit.get('sha256')
            self.sha384 = kit.get('sha384')
            self.sha512 = kit.get('sha512')
            self.ssdeep = kit.get('ssdeep')
            self.kit_files = None

        @property
        def kit_files(self):
            """

            :return:
            """
            return self._kit_files

        @kit_files.setter
        def kit_files(self, value):
            """

            :param value:
            :return:
            """
            return_list = []
            for item in self.json.get('files'):
                return_list.append(self.KitFile(item))

            self._kit_files = return_list

        class KitFile(object):
            __doc__ = '\n            KitFile object.\n            '

            def __init__(self, kit_file):
                """
                Initialize kit file.
                """
                self.json = kit_file
                self.file_name = kit_file.get('fileName')
                self.size = kit_file.get('size')
                self.path = kit_file.get('path')
                self.md5 = kit_file.get('md5')
                self.sha1 = kit_file.get('sha1')
                self.sha224 = kit_file.get('sha224')
                self.sha256 = kit_file.get('sha256')
                self.sha384 = kit_file.get('sha384')
                self.sha512 = kit_file.get('sha512')
                self.ssdeep = kit_file.get('ssdeep')
                self.observed_emails = None

            @property
            def observed_emails(self):
                """

                :return:
                """
                return self._emails

            @observed_emails.setter
            def observed_emails(self, value):
                """

                :param value:
                :return:
                """
                return_list = []
                for item in self.json.get('emails'):
                    return_list.append(self.Email(item))

                self._emails = return_list

            class Email(object):
                __doc__ = '\n                Email object.\n                '

                def __init__(self, observed_email):
                    """
                    Initialize email.
                    :return:
                    """
                    self.json = observed_email
                    self.email_address = observed_email.get('email')
                    self.obfuscation_type = observed_email.get('obfuscationType')


class IPv4(object):
    __doc__ = '\n\n    '

    def __init__(self, ipv4):
        """

        :return:
        """
        if ipv4:
            self.json = ipv4
            self.asn = ipv4.get('asn')
            self.asn_organization = ipv4.get('asnOrganization')
            self.continent_code = ipv4.get('continentCode')
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

        :param url:
        :return:
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