# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/read.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..elements.elementbase import Attribute
from ..tags.context import DataSetter
from ..reader import ReaderError
from ..compat import text_type

class ReadData(DataSetter):
    """
    Read and process a data file. The [c]path[/c] parameter may be absolute, or relative from the current application.

    let's say we have a file, crew.txt in our [link library#data-section]data directory[/link], which is a text file with a list of names, one per line. For example:

    [code]
    Rygel
    John
    Scorpies
    Ka D'Argo
    [/code]

    We can read the above file and process each line with the following:

    [code xml]
    <read-data format="text/plain" path="crew.txt" dst="crew" />
    <for src="splitlines:crew" dst="characters">
        <echo>${character} is on board</echo>
    </for>
    [/code]

    """

    class Help:
        synopsis = b'read and process data'

    fs = Attribute(b'FS name', required=False, default=b'data')
    path = Attribute(b'Path to data file in data filesystem', required=False)
    _from = Attribute(b'Application', type=b'application', required=False, default=None)
    mimetype = Attribute(b'Mime Type of file (omit to guess based on extension)', required=False, default=None)
    dst = Attribute(b'Destination', type=b'reference', default=None)

    def logic(self, context):
        app = self.get_app(context)
        fs_name, path, mimetype, dst = self.get_parameters(context, b'fs', b'path', b'mimetype', b'dst')
        reader = self.archive.get_reader(fs_name)
        try:
            data = reader.read(path, app=app, mime_type=mimetype)
        except ReaderError as e:
            self.throw(b'read-data.fail', text_type(e))
        else:
            self.set_context(context, dst, data)