# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bhanuproject/ann.py
# Compiled at: 2019-03-07 05:03:59
# Size of source mod 2**32: 1111 bytes
project_id = 'my-pthon-ocr'
compute_region = 'us-central1'
model_id = 'ICN562213433353402781'
file_path = '/home/bhanu/Downloads/stamp/OLIVER JAKOB LUDWIG_MEYER_223_0.jpeg'
score_threshold = '0.50'
from google.cloud import automl_v1beta1 as automl
automl_client = automl.AutoMlClient()
model_full_id = automl_client.model_path(project_id, compute_region, model_id)
prediction_client = automl.PredictionServiceClient()
with open(file_path, 'rb') as (image_file):
    content = image_file.read()
payload = {'image': {'image_bytes': content}}
params = {}
if score_threshold:
    params = {'score_threshold': score_threshold}
response = prediction_client.predict(model_full_id, payload, params)
for result in response.payload:
    print('Predicted class name: {}'.format(result.display_name))
    print('Predicted class score: {}'.format(result.classification.score))