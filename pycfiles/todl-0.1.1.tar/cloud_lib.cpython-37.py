# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/utils/logs/cloud_lib.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1325 bytes
"""Utilities that interact with cloud service.
"""
import requests
GCP_METADATA_URL = 'http://metadata/computeMetadata/v1/instance/hostname'
GCP_METADATA_HEADER = {'Metadata-Flavor': 'Google'}

def on_gcp():
    """Detect whether the current running environment is on GCP."""
    try:
        response = requests.get(GCP_METADATA_URL,
          headers=GCP_METADATA_HEADER, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False