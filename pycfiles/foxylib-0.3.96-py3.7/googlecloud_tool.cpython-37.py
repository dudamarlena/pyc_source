# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/google/cloud/googlecloud_tool.py
# Compiled at: 2019-12-01 03:44:10
# Size of source mod 2**32: 2492 bytes
import google, io, os
from google.api_core import operations_v1, operation
from google.longrunning.operations_grpc_pb2 import OperationsStub
from google.longrunning.operations_proto_pb2 import Operation
from google.oauth2 import service_account
from oauth2client.client import GoogleCredentials
from google.cloud import vision
from google.cloud.vision import types
client = vision.ImageAnnotatorClient()
file_name = os.path.abspath('resources/wakeupcat.jpg')
with io.open(file_name, 'rb') as (image_file):
    content = image_file.read()
image = types.Image(content=content)
response = client.label_detection(image=image)
labels = response.label_annotations
print('Labels:')
for label in labels:
    print(label.description)

class GoogleCloudVision:

    @classmethod
    def x(cls):
        credentials = GoogleCredentials.get_application_default()
        speech_service = discovery.build('speech', 'v1', credentials=credentials)

    @classmethod
    def operation_id2track(cls, operation_id):
        SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
        SERVICE_ACCOUNT_FILE = '/path/to/service.json'
        client = vision.ImageAnnotatorClient()
        operation.from_gapic()
        filepath_credential = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        credentials = service_account.Credentials.from_service_account_file(filepath_credential, scopes=SCOPES)
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
        name = 'operations/my-operation'
        request = service.operations().get(name=name)
        response = request.execute()
        api = operations_v1.OperationsClient()
        response = api.get_operation('416926502056aa42')
        client = vision.ImageAnnotatorClient()
        client.async_batch_annotate_files()
        OperationsStub.GetOperation()
        google.longrunning.Operations