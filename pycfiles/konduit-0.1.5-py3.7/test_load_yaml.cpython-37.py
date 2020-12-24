# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_load_yaml.py
# Compiled at: 2020-04-20 03:12:39
# Size of source mod 2**32: 2365 bytes
import konduit, numpy as np, pytest
from konduit.load import server_from_file, client_from_file

@pytest.mark.integration
def test_yaml_server_loading():
    file_path = 'yaml/konduit.yaml'
    server = server_from_file(file_path)
    try:
        running_server = server_from_file(file_path, start_server=True)
    finally:
        running_server.stop()


@pytest.mark.unit
def test_yaml_client_loading():
    file_path = 'yaml/konduit.yaml'
    client = client_from_file(file_path)


@pytest.mark.integration
def test_yaml_minimal_loading():
    file_path = 'yaml/konduit_minimal.yaml'
    server = server_from_file(file_path, use_yaml=True, start_server=True)
    client = client_from_file(file_path, use_yaml=True)
    del server
    del client


@pytest.mark.integration
def test_json_minimal_loading():
    file_path = 'yaml/konduit_minimal.json'
    server = server_from_file(file_path, use_yaml=False, start_server=True)
    client = client_from_file(file_path, use_yaml=False)
    del server
    del client


@pytest.mark.unit
def test_keras_serving():
    file_path = 'yaml/konduit_keras.yaml'
    server = server_from_file(file_path=file_path)
    del server


@pytest.mark.unit
def test_tf_simple_serving():
    file_path = 'yaml/konduit_tf_simple.yaml'
    server = server_from_file(file_path=file_path)
    del server


@pytest.mark.unit
def test_dl4j_mln_serving():
    file_path = 'yaml/konduit_dl4j_mln.yaml'
    server = server_from_file(file_path=file_path)
    del server


@pytest.mark.unit
def test_dl4j_cg_serving():
    file_path = 'yaml/konduit_dl4j_cg.yaml'
    server = server_from_file(file_path=file_path)
    del server


@pytest.mark.unit
def test_dl4j_samediff_serving():
    file_path = 'yaml/konduit_samediff.yaml'
    server = server_from_file(file_path=file_path)
    del server


@pytest.mark.unit
def test_tensor_flow_serving():
    file_path = 'yaml/konduit_tensorflow.yaml'
    server = server_from_file(file_path=file_path)
    del server


@pytest.mark.integration
def test_yaml_server_python_prediction():
    try:
        file_path = 'yaml/konduit_python_code.yaml'
        server, client = konduit.load.from_file(file_path, start_server=True)
        client.predict(np.load('../data/input-0.npy'))
    finally:
        server.stop()