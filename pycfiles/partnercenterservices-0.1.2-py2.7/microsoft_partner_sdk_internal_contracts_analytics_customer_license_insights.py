# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_internal_contracts_analytics_customer_license_insights.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkInternalContractsAnalyticsCustomerLicenseInsights(Model):
    """Business object model that represents License based insights for a customer
    ToDo: get right contract names aligned to Graph/crest apis.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param customer_id: Customer id
    :type customer_id: str
    :param customer_name: Customer Name
    :type customer_name: str
    :param customer_country_code: Customer Country Code
    :type customer_country_code: str
    :param processed_date_time: last Processed date for data
    :type processed_date_time: datetime
    :param licensed_service_products: Service insights of a customer scoped
     under a given partner.
    :type licensed_service_products:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkInternalContractsAnalyticsLicenseServiceProduct]
    :param total_subscription_all_licensed_services: Total subscription for
     license based services.
    :type total_subscription_all_licensed_services: long
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'customer_id': {'key': 'customerId', 'type': 'str'}, 'customer_name': {'key': 'customerName', 'type': 'str'}, 'customer_country_code': {'key': 'customerCountryCode', 'type': 'str'}, 'processed_date_time': {'key': 'processedDateTime', 'type': 'iso-8601'}, 'licensed_service_products': {'key': 'licensedServiceProducts', 'type': '[MicrosoftPartnerSdkInternalContractsAnalyticsLicenseServiceProduct]'}, 'total_subscription_all_licensed_services': {'key': 'totalSubscriptionAllLicensedServices', 'type': 'long'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, customer_id=None, customer_name=None, customer_country_code=None, processed_date_time=None, licensed_service_products=None, total_subscription_all_licensed_services=None):
        super(MicrosoftPartnerSdkInternalContractsAnalyticsCustomerLicenseInsights, self).__init__()
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_country_code = customer_country_code
        self.processed_date_time = processed_date_time
        self.licensed_service_products = licensed_service_products
        self.total_subscription_all_licensed_services = total_subscription_all_licensed_services
        self.attributes = None
        return