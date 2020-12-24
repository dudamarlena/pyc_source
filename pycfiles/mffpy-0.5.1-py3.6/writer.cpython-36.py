# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/writer.py
# Compiled at: 2020-02-14 18:47:56
# Size of source mod 2**32: 4244 bytes
"""
Copyright 2019 Brain Electrophysiology Laboratory Company LLC

Licensed under the ApacheLicense, Version 2.0(the "License");
you may not use this module except in compliance with the License.
You may obtain a copy of the License at:

http: // www.apache.org / licenses / LICENSE - 2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied.
"""
from os import makedirs
from os.path import splitext, exists, join
from subprocess import check_output
import xml.etree.ElementTree as ET
from typing import Dict, Any
from .dict2xml import dict2xml
from .xml_files import XML
from .bin_writer import BinWriter
from .devices import coordinates_and_sensor_layout
import json
__all__ = [
 'Writer', 'BinWriter']

class Writer:

    def __init__(self, filename: str):
        self.filename = filename
        self.files = {}
        self._bin_file_added = False

    def write(self):
        """write contents to .mff/.mfz file"""
        mffdir, ext = splitext(self.filename)
        mffdir += '.mff'
        makedirs(mffdir, exist_ok=False)
        for filename, (content, typ) in self.files.items():
            if '.xml' == splitext(filename)[1]:
                ET.register_namespace('', typ._xmlns[1:-1])
            content.write((join(mffdir, filename)), encoding='UTF-8', xml_declaration=True,
              method='xml')

        if ext == '.mfz':
            check_output(['mff2mfz.py', mffdir])

    def export_to_json(self, data):
        """export data to .json file"""
        with open(self.filename, 'w') as (file):
            json.dump(data, file, indent=4)

    def addxml(self, xmltype, filename=None, **kwargs):
        """Add an .xml file to the collection

        **Parameters**

        *xmltype*: determines to which `XML.todict` the kwargs are passed
        *filename*: (defaults `content['filename']`) filename of the xml file
        """
        content = (XML.todict)(xmltype, **kwargs)
        content_filename = content.pop('filename')
        filename = filename or content_filename
        self.files[filename] = (
         dict2xml(**content), type(XML)._tag_registry[xmltype])

    def addbin(self, binfile: BinWriter, filename=None):
        """Add the .bin file to the collection

        Currently we only allow to add one such files, b/c .mff can only have
        one `epochs` file.  For this we added the flag `self._bin_file_added`.

        **Parameters**

        *binfile*: `class BinWriter` to be added to the collection
        *filename*: (defaults to `binfile.default_filename`) filename of the
            bin file.  It's not recommended to change this default value.
        """
        assert not self._bin_file_added
        self.files[filename or binfile.default_filename] = (
         binfile, type(binfile))
        (self.addxml)(*('dataInfo', ), **binfile.get_info_kwargs())
        self.addxml('epochs', epochs=(binfile.epochs))
        self._bin_file_added = True

    def add_coordinates_and_sensor_layout(self, device: str) -> None:
        """Add coordinates.xml and sensorLayout.xml to the writer

        **Parameters**

        *device*: name string of a device.  Valid choices are in
        "mffpy/resources/coordinates".
        """
        xmls = coordinates_and_sensor_layout(device)
        for name, xml in xmls.items():
            self.files[name + '.xml'] = (
             ET.ElementTree(xml.root), type(xml))

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, fn: str):
        """check filename with .mff/.mfz extension does not exist"""
        base, ext = splitext(fn)
        if not ext in ('.mff', '.mfz', '.json'):
            raise AssertionError
        elif not not exists(fn):
            raise AssertionError(f"File '{fn}' exists already")
        if ext == '.mfz':
            if not not exists(base + '.mff'):
                raise AssertionError
        self._filename = fn