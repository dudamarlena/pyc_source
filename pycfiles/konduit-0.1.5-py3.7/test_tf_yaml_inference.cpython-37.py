# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_tf_yaml_inference.py
# Compiled at: 2020-04-20 03:12:39
# Size of source mod 2**32: 762 bytes
import numpy as np, pytest
from konduit.load import server_from_file, client_from_file

@pytest.mark.integration
def test_yaml_server_python_prediction():
    try:
        konduit_yaml_path = 'yaml/konduit_tf_inference.yaml'
        img = np.load('../data/input_layer.npy')
        server = server_from_file(konduit_yaml_path, start_server=True)
        client = client_from_file(konduit_yaml_path)
        predicted = client.predict(data_input={'input_layer': img})
        result = dict(zip(np.arange(10), predicted[0].round(3)))
        assert round(result.get(7) * 1000) == 998
        server.stop()
    finally:
        server.stop()