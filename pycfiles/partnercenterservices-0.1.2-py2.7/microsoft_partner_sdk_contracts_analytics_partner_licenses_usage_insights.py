# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_analytics_partner_licenses_usage_insights.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsAnalyticsPartnerLicensesUsageInsights(Model):
    """Contains partner level insights about license usage.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param prorated_licenses_usage_percent: The percentage of licenses
     deployed.
    :type prorated_licenses_usage_percent: float
    :param workload_name: The workload name. (Examples : sharepoint, exchange)
    :type workload_name: str
    :param processed_date_time: The date and time when the data was
     aggregated.
    :type processed_date_time: datetime
    :param service_code: The service code of the license.
    :type service_code: str
    :param service_name: The service name. (Example : Office, CRM)
    :type service_name: str
    :param channel: The channel name of the service. (Example : reseller)
    :type channel: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'prorated_licenses_usage_percent': {'key': 'proratedLicensesUsagePercent', 'type': 'float'}, 'workload_name': {'key': 'workloadName', 'type': 'str'}, 'processed_date_time': {'key': 'processedDateTime', 'type': 'iso-8601'}, 'service_code': {'key': 'serviceCode', 'type': 'str'}, 'service_name': {'key': 'serviceName', 'type': 'str'}, 'channel': {'key': 'channel', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, prorated_licenses_usage_percent=None, workload_name=None, processed_date_time=None, service_code=None, service_name=None, channel=None):
        super(MicrosoftPartnerSdkContractsAnalyticsPartnerLicensesUsageInsights, self).__init__()
        self.prorated_licenses_usage_percent = prorated_licenses_usage_percent
        self.workload_name = workload_name
        self.processed_date_time = processed_date_time
        self.service_code = service_code
        self.service_name = service_name
        self.channel = channel
        self.attributes = None
        return