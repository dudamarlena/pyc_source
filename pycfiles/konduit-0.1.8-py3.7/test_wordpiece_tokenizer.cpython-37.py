# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_wordpiece_tokenizer.py
# Compiled at: 2020-05-03 12:37:34
# Size of source mod 2**32: 728 bytes
import pytest
from konduit import *
from konduit.load import server_from_file, client_from_file
import numpy as np

@pytest.mark.integration
def test_wordpiece_tokenizer_serving_minimal():
    file_path = 'yaml/konduit_wordpiece_tokenizer_minimal.yaml'
    server = server_from_file(file_path)
    try:
        running_server = server_from_file(file_path, start_server=True)
    finally:
        running_server.stop()


@pytest.mark.integration
def test_wordpiece_tokenizer_serving_two_steps():
    file_path = 'yaml/konduit_wordpiece_tokenizer_two_steps.yaml'
    server = server_from_file(file_path)
    try:
        running_server = server_from_file(file_path, start_server=True)
    finally:
        running_server.stop()