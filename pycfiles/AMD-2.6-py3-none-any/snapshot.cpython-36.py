# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/snapshot.py
# Compiled at: 2019-06-01 23:47:42
# Size of source mod 2**32: 1928 bytes
import shutil
from urllib3.exceptions import HTTPError
from .exceptions import CommError

class Snapshot(object):

    def __get_config(self, config_name):
        ret = self.command('configManager.cgi?action=getConfig&name={0}'.format(config_name))
        return ret.content.decode('utf-8')

    @property
    def snapshot_config(self):
        return self._Snapshot__get_config('Snap')

    def snapshot(self, channel=None, path_file=None, timeout=None):
        """
        Args:

            channel:
                Video input channel number

                If no channel param is used, don't send channel parameter
                so camera will use its default channel

            path_file:
                If path_file is provided, save the snapshot
                in the path

        Return:
            raw from http request
        """
        cmd = 'snapshot.cgi'
        if channel is not None:
            cmd += '?channel={}'.format(channel)
        ret = self.command(cmd, timeout_cmd=timeout, stream=True)
        if path_file:
            try:
                with open(path_file, 'wb') as (out_file):
                    shutil.copyfileobj(ret.raw, out_file)
            except HTTPError as error:
                _LOGGER.debug('%s Snapshot to file failed due to error: %s', self, repr(error))
                raise CommError(error)

        return ret.raw