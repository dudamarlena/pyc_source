# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_connect_us_advisory_hours_service_request_metadata.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsConnectUsAdvisoryHoursServiceRequestMetadata(Model):
    """Advisory hours service request metadata.

    :param countries: Gets or sets the countries.
    :type countries:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsConnectUsCountry]
    :param languages: Gets or sets the languages.
    :type languages:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsConnectUsLanguage]
    :param technologies: Gets or sets the technologies.
    :type technologies:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsConnectUsTechnology]
    """
    _attribute_map = {'countries': {'key': 'countries', 'type': '[MicrosoftPartnerSdkContractsV1ContractsConnectUsCountry]'}, 'languages': {'key': 'languages', 'type': '[MicrosoftPartnerSdkContractsV1ContractsConnectUsLanguage]'}, 'technologies': {'key': 'technologies', 'type': '[MicrosoftPartnerSdkContractsV1ContractsConnectUsTechnology]'}}

    def __init__(self, countries=None, languages=None, technologies=None):
        super(MicrosoftPartnerSdkContractsV1ContractsConnectUsAdvisoryHoursServiceRequestMetadata, self).__init__()
        self.countries = countries
        self.languages = languages
        self.technologies = technologies