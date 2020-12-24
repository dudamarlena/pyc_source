# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/snapshot.py
# Compiled at: 2020-01-16 09:32:13
# Size of source mod 2**32: 2252 bytes
import shutil, logging
from urllib3.exceptions import HTTPError
from .exceptions import CommError
_LOGGER = logging.getLogger(__name__)

class Snapshot(object):

    def __get_config(self, config_name):
        ret = self.command('configManager.cgi?action=getConfig&name={0}'.format(config_name))
        return ret.content.decode('utf-8')

    @property
    def snapshot_config(self):
        return self._Snapshot__get_config('Snap')

    def snapshot(self, channel=None, path_file=None, timeout=None, stream=True):
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
            raw from http request if stream is True
            response content if stream is False
        """
        cmd = 'snapshot.cgi'
        if channel is not None:
            cmd += '?channel={}'.format(channel)
        ret = self.command(cmd, timeout_cmd=timeout, stream=stream)
        if path_file:
            with open(path_file, 'wb') as (out_file):
                if stream:
                    try:
                        shutil.copyfileobj(ret.raw, out_file)
                    except HTTPError as error:
                        try:
                            _LOGGER.debug('%s Snapshot to file failed due to error: %s', self, repr(error))
                            raise CommError(error)
                        finally:
                            error = None
                            del error

                else:
                    out_file.write(ret.content)
        if stream:
            return ret.raw
        return ret.content