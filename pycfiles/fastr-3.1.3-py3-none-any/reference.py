# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/reference.py
# Compiled at: 2019-06-04 03:03:06
"""
This module contains the Null plugin for fastr
"""
import json, os, fastr
from fastr import typelist, vfs
from fastr.core.ioplugin import IOPlugin
from fastr.data import url
from fastr.datatypes import TypeGroup, URLType

class Reference(IOPlugin):
    """
    The Reference plugin is create to handle ``ref://`` type or URLs. These
    URLs are to make the sink just write a simple reference file to the data.
    The reference file contains the DataType and the value so the result can
    be reconstructed. It for files just leaves the data on disk by reference.
    This plugin is not useful for production, but is used for testing purposes.
    """
    scheme = 'ref'

    def __init__(self):
        super(Reference, self).__init__()

    def push_sink_data(self, value, outurl, datatype=None):
        """
        Write out the sink data from the inpath to the outurl.

        :param str value: the path of the data to be pushed
        :param str outurl: the url to write the data to
        :param DataType datatype: the datatype of the data, used for determining
                                  the total contents of the transfer
        :return: None
        """
        fastr.log.info(('Push sink called with: {}, {}').format(value, outurl))
        self.setup()
        if datatype is None or issubclass(datatype, TypeGroup):
            previous_datatype = datatype.id if datatype is not None else None
            datatype = typelist.guess_type(value, options=datatype)
            fastr.log.info(('Determined specific datatype as {} (based on {})').format(datatype.id, previous_datatype))
        out_path = vfs.url_to_path(outurl, scheme='ref')
        out_dir = os.path.dirname(out_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        if issubclass(datatype, URLType):
            filename = url.basename(value)
            target_path = os.path.join(out_dir, filename)
            value_url = vfs.path_to_url(target_path)
            fastr.vfs.push_sink_data(value, value_url, datatype)
            value = value_url
        result = {'value': value, 
           'datatype': datatype.id}
        with open(out_path, 'w') as (fh_out):
            json.dump(result, fh_out)
        return