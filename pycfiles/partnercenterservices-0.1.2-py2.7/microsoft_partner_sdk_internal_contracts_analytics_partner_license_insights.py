# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_internal_contracts_analytics_partner_license_insights.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkInternalContractsAnalyticsPartnerLicenseInsights(Model):
    """Business object model that represents License based insights for a partner
    across all customers.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param processed_date_time: last Processed date for data
    :type processed_date_time: datetime
    :param service_name: Service Name like O365
     ToDo: get right terminology from Graph/crest apis
    :type service_name: str
    :param service_insights_type: Service insights type. Possible values
     include: 'none', 'license', 'meter'
    :type service_insights_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param total_customers: Total customers as of processed time stamp.
    :type total_customers: long
    :param total_subscriptions: Total subscription count as of processed time
     stamp.
    :type total_subscriptions: long
    :param total_sold_seats: Total sold seats as of processed time stamp.
    :type total_sold_seats: long
    :param total_deployed_seats_all_channel_all_partner: Total deployed seats
     as of processed time stamp.
    :type total_deployed_seats_all_channel_all_partner: long
    :param total_customer_sold_seats: Total seats sold to all customers (of
     this partner) by all partners as of processed time stamp.
    :type total_customer_sold_seats: long
    :param rolling_metrics: Rolling metrics of this partner as of processed
     time stamp.
    :type rolling_metrics:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkInternalContractsAnalyticsPartnerLicenseRollingServiceInsights
    :param workloads: Workload insights of a customer scoped under a given
     partner, service
     and product.
    :type workloads:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkInternalContractsAnalyticsLicenseWorkload]
    :param deployment_percent: Percentage of licenses deployed by customers of
     this partner
    :type deployment_percent: float
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'processed_date_time': {'key': 'processedDateTime', 'type': 'iso-8601'}, 'service_name': {'key': 'serviceName', 'type': 'str'}, 'service_insights_type': {'key': 'serviceInsightsType', 'type': 'str'}, 'total_customers': {'key': 'totalCustomers', 'type': 'long'}, 'total_subscriptions': {'key': 'totalSubscriptions', 'type': 'long'}, 'total_sold_seats': {'key': 'totalSoldSeats', 'type': 'long'}, 'total_deployed_seats_all_channel_all_partner': {'key': 'totalDeployedSeatsAllChannelAllPartner', 'type': 'long'}, 'total_customer_sold_seats': {'key': 'totalCustomerSoldSeats', 'type': 'long'}, 'rolling_metrics': {'key': 'rollingMetrics', 'type': 'MicrosoftPartnerSdkInternalContractsAnalyticsPartnerLicenseRollingServiceInsights'}, 'workloads': {'key': 'workloads', 'type': '[MicrosoftPartnerSdkInternalContractsAnalyticsLicenseWorkload]'}, 'deployment_percent': {'key': 'deploymentPercent', 'type': 'float'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, processed_date_time=None, service_name=None, service_insights_type=None, total_customers=None, total_subscriptions=None, total_sold_seats=None, total_deployed_seats_all_channel_all_partner=None, total_customer_sold_seats=None, rolling_metrics=None, workloads=None, deployment_percent=None):
        super(MicrosoftPartnerSdkInternalContractsAnalyticsPartnerLicenseInsights, self).__init__()
        self.processed_date_time = processed_date_time
        self.service_name = service_name
        self.service_insights_type = service_insights_type
        self.total_customers = total_customers
        self.total_subscriptions = total_subscriptions
        self.total_sold_seats = total_sold_seats
        self.total_deployed_seats_all_channel_all_partner = total_deployed_seats_all_channel_all_partner
        self.total_customer_sold_seats = total_customer_sold_seats
        self.rolling_metrics = rolling_metrics
        self.workloads = workloads
        self.deployment_percent = deployment_percent
        self.attributes = None
        return