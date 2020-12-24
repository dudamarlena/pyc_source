# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/project_parsers/json_project_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 820 bytes
from pyxrd.generic.io import get_case_insensitive_glob
from pyxrd.file_parsers.json_parser import JSONParser
from .namespace import project_parsers

@project_parsers.register_parser()
class JSONProjectParser(JSONParser):
    description = 'Project file *.PYXRD'
    extensions = get_case_insensitive_glob('*.PYXRD')
    mimetypes = ['application/octet-stream', 'application/zip']

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=True):
        project = super(JSONProjectParser, cls)._parse_data(filename, fp, data_objects=data_objects, close=close)
        project.filename = filename
        return project