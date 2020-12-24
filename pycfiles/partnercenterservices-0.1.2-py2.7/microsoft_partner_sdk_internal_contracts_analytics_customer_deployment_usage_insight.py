# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_internal_contracts_analytics_customer_deployment_usage_insight.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkInternalContractsAnalyticsCustomerDeploymentUsageInsight(Model):
    """Deployment and Usage insight for Customers of a Partner.

    :param customer_licenses_deployment_insight: Customer Licenses Deployment
     Insight
    :type customer_licenses_deployment_insight:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsAnalyticsCustomerLicensesDeploymentInsights
    :param customer_licenses_usage_insights: Collection of
     CustomerWorkloadUsageInsights
    :type customer_licenses_usage_insights:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsAnalyticsCustomerLicensesUsageInsights]
    """
    _attribute_map = {'customer_licenses_deployment_insight': {'key': 'customerLicensesDeploymentInsight', 'type': 'MicrosoftPartnerSdkContractsAnalyticsCustomerLicensesDeploymentInsights'}, 'customer_licenses_usage_insights': {'key': 'customerLicensesUsageInsights', 'type': '[MicrosoftPartnerSdkContractsAnalyticsCustomerLicensesUsageInsights]'}}

    def __init__(self, customer_licenses_deployment_insight=None, customer_licenses_usage_insights=None):
        super(MicrosoftPartnerSdkInternalContractsAnalyticsCustomerDeploymentUsageInsight, self).__init__()
        self.customer_licenses_deployment_insight = customer_licenses_deployment_insight
        self.customer_licenses_usage_insights = customer_licenses_usage_insights