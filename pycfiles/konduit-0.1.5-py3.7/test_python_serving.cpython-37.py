# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_python_serving.py
# Compiled at: 2020-04-20 03:12:39
# Size of source mod 2**32: 912 bytes
import numpy as np, pytest, random
from konduit import *
from konduit.server import Server
from konduit.utils import is_port_in_use

@pytest.mark.integration
def test_server_start():
    port = random.randint(1000, 65535)
    serving_config = ServingConfig(http_port=port)
    python_config = PythonConfig(python_code='first += 2',
      python_inputs={'first': 'NDARRAY'},
      python_outputs={'first': 'NDARRAY'})
    step = PythonStep().step(python_config)
    server = Server(steps=step, serving_config=serving_config)
    server.start()
    client = server.get_client()
    data_input = {'default': np.load('../data/input-0.npy')}
    assert is_port_in_use(port)
    try:
        predicted = client.predict(data_input)
        print(predicted)
        server.stop()
    except Exception as e:
        try:
            print(e)
            server.stop()
        finally:
            e = None
            del e