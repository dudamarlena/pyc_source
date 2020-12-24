# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_setup_and_run.py
# Compiled at: 2020-03-18 00:53:14
# Size of source mod 2**32: 895 bytes
import numpy as np, pytest
from konduit import *
from konduit.server import Server
from konduit.utils import is_port_in_use

@pytest.mark.integration
def test_setup_and_run_start():
    python_config = PythonConfig(python_code="def setup(): pass\ndef run(input): {'output': np.array(input + 2)}",
      python_inputs={'input': 'NDARRAY'},
      python_outputs={'output': 'NDARRAY'},
      setup_and_run=True)
    step = PythonStep().step(python_config)
    server = Server(steps=step, serving_config=(ServingConfig()))
    _, port, started = server.start()
    assert started
    assert is_port_in_use(port)
    client = server.get_client()
    data_input = {'default': np.asarray([42.0, 1.0])}
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