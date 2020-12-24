# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_client.py
# Compiled at: 2020-05-07 10:53:43
# Size of source mod 2**32: 931 bytes
import pytest
from konduit import *

@pytest.mark.integration
def test_client_from_server():
    server_id = 'python_server'
    python_config = PythonConfig(python_code='first += 2',
      python_inputs={'first': 'NDARRAY'},
      python_outputs={'first': 'NDARRAY'})
    step = PythonStep().step(python_config)
    server = Server(steps=step, serving_config=(ServingConfig()))
    server.start(server_id)
    try:
        server.get_client()
    finally:
        server.stop(server_id)


@pytest.mark.unit
def test_multipart_regex():
    client = Client(port=1337,
      output_data_format='NUMPY',
      input_names=[
     'partname'],
      output_names=[
     'nobody_cares'])
    test_data = {'partname[0]':'foo', 
     'partname[1]':'bar'}
    client._validate_multi_part(test_data)
    test_data['foo'] = 'baz'
    with pytest.raises(Exception):
        client._validate_multi_part(test_data)