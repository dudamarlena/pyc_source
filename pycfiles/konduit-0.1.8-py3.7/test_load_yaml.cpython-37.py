# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_load_yaml.py
# Compiled at: 2020-05-07 11:49:56
# Size of source mod 2**32: 2668 bytes
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
    try:
        server = server_from_file(file_path, use_yaml=True, start_server=True)
        client = client_from_file(file_path, use_yaml=True)
    finally:
        server.stop()

    del server
    del client


@pytest.mark.integration
def test_json_minimal_loading():
    file_path = 'yaml/konduit_minimal.json'
    try:
        server = server_from_file(file_path, use_yaml=False, start_server=True)
        client = client_from_file(file_path, use_yaml=False)
    finally:
        server.stop()

    del server
    del client


@pytest.mark.unit
def test_keras_serving():
    file_path = 'yaml/konduit_keras.yaml'
    try:
        server = server_from_file(file_path=file_path)
    finally:
        server.stop()

    del server


@pytest.mark.unit
def test_tf_simple_serving():
    file_path = 'yaml/konduit_tf_simple.yaml'
    try:
        server = server_from_file(file_path=file_path)
    finally:
        server.stop()

    del server


@pytest.mark.unit
def test_dl4j_mln_serving():
    file_path = 'yaml/konduit_dl4j_mln.yaml'
    try:
        server = server_from_file(file_path=file_path)
    finally:
        server.stop()

    del server


@pytest.mark.unit
def test_dl4j_cg_serving():
    file_path = 'yaml/konduit_dl4j_cg.yaml'
    try:
        server = server_from_file(file_path=file_path)
    finally:
        server.stop()

    del server


@pytest.mark.unit
def test_dl4j_samediff_serving():
    file_path = 'yaml/konduit_samediff.yaml'
    try:
        server = server_from_file(file_path=file_path)
    finally:
        server.stop()

    del server


@pytest.mark.unit
def test_tensor_flow_serving():
    file_path = 'yaml/konduit_tensorflow.yaml'
    try:
        server = server_from_file(file_path=file_path)
    finally:
        server.stop()

    del server


@pytest.mark.integration
def test_yaml_server_python_prediction():
    try:
        file_path = 'yaml/konduit_python_code.yaml'
        server, client = konduit.load.from_file(file_path, start_server=True)
        client.predict(np.load('../data/input-0.npy'))
    finally:
        server.stop()