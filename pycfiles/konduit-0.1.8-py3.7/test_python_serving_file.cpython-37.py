# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_python_serving_file.py
# Compiled at: 2020-04-03 13:49:55
# Size of source mod 2**32: 994 bytes
import numpy as np, os, pytest
from konduit import *
from konduit.client import Client
from konduit.server import Server
from konduit.utils import is_port_in_use, default_python_path

@pytest.mark.integration
def test_python_script_prediction():
    work_dir = os.path.abspath('.')
    python_config = PythonConfig(python_path=(default_python_path(work_dir)),
      python_code_path=(os.path.join(work_dir, 'simple.py')),
      python_inputs={'first': 'NDARRAY'},
      python_outputs={'second': 'NDARRAY'})
    step = PythonStep().step(python_config)
    server = Server(steps=step, serving_config=(ServingConfig()))
    _, port, started = server.start()
    assert started
    assert is_port_in_use(port)
    client = Client(port=port)
    try:
        input_array = np.load('../data/input-0.npy')
        predicted = client.predict(input_array)
        print(predicted)
        server.stop()
    except Exception as e:
        try:
            print(e)
            server.stop()
        finally:
            e = None
            del e