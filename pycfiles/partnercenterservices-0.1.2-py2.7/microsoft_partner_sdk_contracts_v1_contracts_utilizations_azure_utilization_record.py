# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_contracts_utilizations_azure_utilization_record.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureUtilizationRecord(Model):
    """Describes the properties of an Azure Utilization Record resource.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param usage_start_time: Gets or sets the start of the usage aggregation
     time range.
     The response is grouped by the time of consumption (when the resource was
     actually used vs. when was it reported to the billing system).
    :type usage_start_time: datetime
    :param usage_end_time: Gets or sets the end of the usage aggregation time
     range.
     The response is grouped by the time of consumption (when the resource was
     actually used vs. when was it reported to the billing system).
    :type usage_end_time: datetime
    :param resource: Gets or sets the Azure resource.
    :type resource:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureResource
    :param quantity: Gets or sets the quantity consumed of the Azure resource.
    :type quantity: float
    :param unit: Gets or sets the type of quantity. (Example : hours, bytes)
    :type unit: str
    :param info_fields: Gets or sets the key-value pairs of instance-level
     details. This object may be empty.
    :type info_fields: dict[str, str]
    :param instance_data: Gets or sets an AzureInstanceData object that
     contains key-value pairs of instance level details.
    :type instance_data:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureInstanceData
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'usage_start_time': {'key': 'usageStartTime', 'type': 'iso-8601'}, 'usage_end_time': {'key': 'usageEndTime', 'type': 'iso-8601'}, 'resource': {'key': 'resource', 'type': 'MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureResource'}, 'quantity': {'key': 'quantity', 'type': 'float'}, 'unit': {'key': 'unit', 'type': 'str'}, 'info_fields': {'key': 'infoFields', 'type': '{str}'}, 'instance_data': {'key': 'instanceData', 'type': 'MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureInstanceData'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, usage_start_time=None, usage_end_time=None, resource=None, quantity=None, unit=None, info_fields=None, instance_data=None):
        super(MicrosoftPartnerSdkContractsV1ContractsUtilizationsAzureUtilizationRecord, self).__init__()
        self.usage_start_time = usage_start_time
        self.usage_end_time = usage_end_time
        self.resource = resource
        self.quantity = quantity
        self.unit = unit
        self.info_fields = info_fields
        self.instance_data = instance_data
        self.attributes = None
        return