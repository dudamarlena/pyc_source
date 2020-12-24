# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test-script-new.py
# Compiled at: 2019-11-27 13:49:26
# Size of source mod 2**32: 966 bytes
import os
from konduit import PythonConfig, ServingConfig, InferenceConfiguration
from konduit.utils import default_python_path
from konduit import PythonStep
from konduit.server import Server
import sys, numpy as np, time
from utils import to_base_64
from konduit.client import Client
from PIL import Image
from utils import to_base_64
python_code = '\nimport numpy as np \noutput = np.array(int("123"))\n'
python_config = PythonConfig(python_code=python_code,
  python_inputs={'int_string': 'STR'},
  python_outputs={'output': 'NDARRAY'})
onnx_step = PythonStep().step(python_config)
server = Server(steps=onnx_step,
  serving_config=ServingConfig(http_port=255))
server.start()
time.sleep(30)
client = Client(input_type='JSON',
  return_output_type='JSON',
  endpoint_output_type='JSON',
  port=255)
a = client.predict({'int_string': '123'})
print(a)
server.stop()