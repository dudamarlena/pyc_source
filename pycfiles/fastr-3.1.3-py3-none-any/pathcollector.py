# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/collectorplugins/pathcollector.py
# Compiled at: 2019-06-04 03:03:06
import re, fastr
from fastr import exceptions
from fastr.data import url
from fastr.plugins import FastrInterface

class PathCollector(FastrInterface.collector_plugin_type):
    """
    The PathCollector plugin for the FastrInterface. This plugin uses the
    location fields to find data on the filesystem. To use this plugin the
    method of the output has to be set to ``path``

    The general working is as follows:

    1. The location field is taken from the output
    2. The substitutions are performed on the location field (see below)
    3. The updated location field will be used as a :ref:`regular expression <python:re-syntax>` filter
    4. The filesystem is scanned for all matching files/directory

    The special substitutions performed on the location use the
    Format Specification Mini-Language :ref:`python:formatspec`.
    The predefined fields that can be used are:

    * ``inputs``, an objet with the input values (use like ``{inputs.image[0]}``)
      The input contains the following attributes that you can access:

      * ``.directory`` for the directory name (use like ``input.image[0].directory``)
        The directory is the same as the result of ``os.path.dirname``
      * ``.filename`` is the result of ``os.path.basename`` on the path
      * ``.basename`` for the basename name (use like ``input.image[0].basename``)
        The basename is the same as the result of ``os.path.basename`` and the
        extension stripped. The extension is considered to be everything after
        the first dot in the filename.
      * ``.extension`` for the extension name (use like ``input.image[0].extension``)

    * ``output``, an object with the output values (use like ``{outputs.result[0]}``)
      It contains the same attributes as the input

      * ``special.cardinality``, the index of the current cardinality
      * ``special.extension``, is the extension for the output DataType

    Example use::

      <output ... method="path" location="{output.directory[0]}/TransformParameters.{special.cardinality}.{special.extension}"/>

    Given the output directory ``./nodeid/sampleid/result``, the second sample in the output and
    filetype with a ``txt`` extension, this would be translated into::

      <output ... method="path" location="./nodeid/sampleid/result/TransformParameters.1.txt>

    """

    def __init__(self):
        super(PathCollector, self).__init__()
        self.id = 'path'

    def _collect_results(self, interface, output, result):
        output_data = []
        result.result_data[output.id] = output_data
        location = output.location
        use_cardinality = re.search('\\{special.cardinality(:.*?)??\\}', location) is not None
        if use_cardinality:
            nr = 0
            while True:
                specials, inputs, outputs = interface.get_specials(result.payload, output, nr)
                fastr.log.debug(('input: {}, output: {}, specials: {}').format(inputs, outputs, specials))
                fastr.log.debug(('location: {}').format(location))
                fastr.log.debug(('parsed location: {}').format(location.format(input=inputs, output=outputs, special=specials, input_parts=inputs, output_parts=outputs)))
                value = location.format(input=inputs, output=outputs, special=specials, input_parts=inputs, output_parts=outputs)
                fastr.log.debug(('Searching regexp value {}').format(value))
                if url.isurl(value):
                    value = fastr.vfs.url_to_path(value)
                path_list = self._regexp_path(value)
                if len(path_list) < 1:
                    break
                if len(path_list) > 1:
                    message = ('Found multiple matches for automatic output using {}').format(value)
                    fastr.log.error(message)
                    raise exceptions.FastrCollectorError(message)
                value = path_list[0]
                fastr.log.debug(('Got automatic result: {}').format(value))
                output_data.append(value)
                nr += 1

        else:
            fastr.log.debug('No cardinality branch!')
            specials, inputs, outputs = interface.get_specials(result.payload, output, '')
            value = location.format(input=inputs, output=outputs, special=specials, input_parts=inputs, output_parts=outputs)
            if url.isurl(value):
                value = fastr.vfs.url_to_path(value)
            path_list = self._regexp_path(value)
            output_data.extend(path_list)
        return