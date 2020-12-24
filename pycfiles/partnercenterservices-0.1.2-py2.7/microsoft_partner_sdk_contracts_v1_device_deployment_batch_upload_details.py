# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_device_deployment_batch_upload_details.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1DeviceDeploymentBatchUploadDetails(Model):
    """Describes the status of a device batch upload of information about each
    device in a list of devices.

    :param batch_tracking_id: Gets or sets the tracking ID, a GUID-formatted
     string that is associated with the batch of devices uploaded.
    :type batch_tracking_id: str
    :param status: Gets or sets the status of the batch upload. Possible
     values include: 'unknown', 'queued', 'processing', 'finished',
     'finished_with_errors'
    :type status: str or ~microsoft.store.partnercenterservices.models.enum
    :param started_time: Gets or sets the date and time that the batch upload
     process started.
    :type started_time: datetime
    :param completed_time: Gets or sets the date and time that the batch
     upload process completed.
    :type completed_time: datetime
    :param devices_status: Gets or sets the device status, an array of objects
     that specify the status of each device information upload.
    :type devices_status:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1DeviceDeploymentDeviceUploadDetails]
    """
    _attribute_map = {'batch_tracking_id': {'key': 'batchTrackingId', 'type': 'str'}, 'status': {'key': 'status', 'type': 'str'}, 'started_time': {'key': 'startedTime', 'type': 'iso-8601'}, 'completed_time': {'key': 'completedTime', 'type': 'iso-8601'}, 'devices_status': {'key': 'devicesStatus', 'type': '[MicrosoftPartnerSdkContractsV1DeviceDeploymentDeviceUploadDetails]'}}

    def __init__(self, batch_tracking_id=None, status=None, started_time=None, completed_time=None, devices_status=None):
        super(MicrosoftPartnerSdkContractsV1DeviceDeploymentBatchUploadDetails, self).__init__()
        self.batch_tracking_id = batch_tracking_id
        self.status = status
        self.started_time = started_time
        self.completed_time = completed_time
        self.devices_status = devices_status