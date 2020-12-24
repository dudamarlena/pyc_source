# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/httpplugin.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 1844 bytes
from fastr import exceptions
from fastr.core.ioplugin import IOPlugin
import requests
CHUNK_SIZE = 524288

class HTTPPlugin(IOPlugin):
    __doc__ = '\n    .. warning::\n        This Plugin is still under development and has not been tested at all.\n        example url: https://server.io/path/to/resource\n    '
    scheme = ('https', 'http')

    def __init__(self):
        super(HTTPPlugin, self).__init__()

    def fetch_url(self, inurl, outpath):
        """
        Download file from server.

        :param inurl: url to the file.
        :param outpath: path to store file
        """
        response = requests.get(inurl, allow_redirects=True, stream=True, timeout=60)
        if response.status_code != 200:
            raise exceptions.FastrDataTypeValueError('Problem downloading the file, HTTP status code {}'.format(response.status_code))
        with open(outpath, 'wb') as (output_file):
            for chunk in response.iter_content(CHUNK_SIZE):
                output_file.write(chunk)

        return outpath