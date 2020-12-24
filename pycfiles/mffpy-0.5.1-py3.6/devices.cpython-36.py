# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/devices.py
# Compiled at: 2020-01-29 20:14:20
# Size of source mod 2**32: 927 bytes
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
from os.path import dirname, exists, join
from .xml_files import XML
resources_dir = join(dirname(__file__), 'resources')

def coordinates_and_sensor_layout(device: str):
    xml = {}
    for name in ('coordinates', 'sensorLayout'):
        filename = join(resources_dir, name, device + '.xml')
        assert exists(filename), f"{name} of {device} not available"
        xml[name] = XML.from_file(filename)

    return xml