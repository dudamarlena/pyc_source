# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\utils.py
# Compiled at: 2020-04-20 03:12:39
# Size of source mod 2**32: 597 bytes
import json
from jnius import autoclass

def load_java_tp(tp_json):
    """Just used for testing, users won't need this."""
    string_java = autoclass('java.lang.String')
    java_transform_process = autoclass('org.datavec.api.transform.TransformProcess')
    java_transform_process.fromJson(string_java(tp_json))


def inference_from_json(as_json):
    string_java = autoclass('java.lang.String')
    inference_configuration_java = autoclass('ai.konduit.serving.InferenceConfiguration')
    inference_configuration_java.fromJson(string_java(json.dumps(as_json)))