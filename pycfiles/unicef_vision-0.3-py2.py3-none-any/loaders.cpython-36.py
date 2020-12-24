# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/vision/src/unicef_vision/loaders.py
# Compiled at: 2019-02-05 15:36:20
# Size of source mod 2**32: 2365 bytes
import json, requests
from celery.utils.log import get_task_logger
from django.conf import settings
from unicef_vision.exceptions import VisionException
logger = get_task_logger('vision.synchronize')
VISION_NO_DATA_MESSAGE = 'No Data Available'

class VisionDataLoader:
    __doc__ = 'Base class for Data Loading'
    URL = settings.VISION_URL

    def __init__(self, business_area_code=None, endpoint=None):
        if endpoint is None:
            raise VisionException('You must set the ENDPOINT name')
        separator = '' if self.URL.endswith('/') else '/'
        self.url = '{}{}{}'.format(self.URL, separator, endpoint)
        if business_area_code:
            self.url += '/{}'.format(business_area_code)
        logger.info('About to get data from {}'.format(self.url))

    def get(self):
        response = requests.get((self.url),
          headers={'Content-Type': 'application/json'},
          auth=(
         settings.VISION_USER, settings.VISION_PASSWORD),
          verify=False)
        if response.status_code != 200:
            raise VisionException('Load data failed! Http code: {}'.format(response.status_code))
        json_response = response.json()
        if json_response == VISION_NO_DATA_MESSAGE:
            return []
        else:
            return json_response


class ManualDataLoader(VisionDataLoader):
    __doc__ = '\n    Can be used to sync single objects from VISION url templates:\n    /endpoint if no business_area_code or object_number\n    /endpoint/business_area_code if no object number provided\n    /endpoint/object_number else\n    '

    def __init__(self, business_area_code=None, endpoint=None, object_number=None):
        if not object_number:
            super().__init__(business_area_code=business_area_code, endpoint=endpoint)
        else:
            if endpoint is None:
                raise VisionException('You must set the ENDPOINT name')
            self.url = '{}/{}/{}'.format(self.URL, endpoint, object_number)


class FileDataLoader:
    __doc__ = 'Loader to read json file instead of REST API'

    def __init__(self, filename):
        self.filename = filename

    def get(self):
        data = json.load(open(self.filename))
        return data