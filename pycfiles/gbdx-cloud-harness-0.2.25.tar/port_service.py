# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/cloud-harness/gbdx_cloud_harness/services/port_service.py
# Compiled at: 2016-10-31 16:11:18
import os
from gbdx_cloud_harness.services.account_storage_service import AccountStorageService
from gbdx_cloud_harness.utils.printer import printer

class PortService(object):

    def __init__(self, task, storage_service=None):
        self._task = task
        if storage_service is None:
            self.storage = AccountStorageService()
        else:
            self.storage = storage_service
        self.s3_root = self.storage.location
        return

    @property
    def task(self):
        return self._task

    def upload_input_ports(self, port_list=None, exclude_list=None):
        """
        Takes the workflow value for each port and does the following:
            * If local filesystem -> Uploads locally files to s3.
                S3 location will be as follows:
                    gbd-customer-data/<acct_id>/<workflow_name>/<task_name>/<port_name>/
            * If S3 url -> do nothing.
        :returns the update workflow with S3 urls.
        """
        input_ports = self._task.input_ports
        for port in input_ports:
            if port_list and port.name not in port_list:
                continue
            if exclude_list and port.name in exclude_list:
                continue
            if not port.value or not os.path.isabs(port.value) or not os.path.isdir(port.value):
                continue
            prefix = ('{run_name}/{port}').format(run_name=self._task.run_name, port=port.name)
            port_files = self._get_port_files(port.value, prefix)
            port.value = '%s/%s' % (self.s3_root, prefix)
            if len(port_files) == 0:
                printer('Port %s is empty, push to S3 skipped' % port.name)
            else:
                self.storage.upload(port_files)
                printer('Port %s pushed to account storage, %s files' % (port.name, len(port_files)))

    @staticmethod
    def _get_port_files(local_path, prefix):
        """
        Find files for the local_path and return tuples of filename and keynames
        :param local_path: the local path to search for files
        :param prefix: the S3 prefix for each key name on S3
        """
        source_files = []
        for root, dirs, files in os.walk(local_path, topdown=False):
            for name in files:
                fname = os.path.join(root, name)
                key_name = '%s/%s' % (prefix, fname[len(local_path) + 1:])
                source_files.append((fname, key_name))

        return source_files