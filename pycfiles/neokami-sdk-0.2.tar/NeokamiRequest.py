# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/neokami1/Dropbox/Neokami/Code/Bitbucket/neokami-python-sdk/neokami/src/Neokami/NeokamiRequest.py
# Compiled at: 2015-06-18 06:09:42
""" Copyright 2015 Neokami GmbH. """
from .Base import Base
from .HttpClients.NeokamiCurl import NeokamiHttpClient
from .NeokamiResponse import NeokamiResponse
from .Exceptions.NeokamiParametersException import NeokamiParametersException
NeokamiHttpClient = NeokamiHttpClient()

class NeokamiRequest(Base):
    wait = 1
    max_retries = 5
    sleep = 1
    output_type = None
    output_format = 'array'
    apiKey = None
    silentFails = False

    def getOutputFormat(self):
        """
                Get the output format
                :return output_format:
                """
        return self.output_format

    def setOutputFormat(self, output_format):
        """
                Set output format
                :return self:
                """
        self.output_format = output_format
        return self

    def getApiKey(self):
        """
                Get api key
                :return apiKey:
                """
        return self.apiKey

    def setApiKey(self, apiKey):
        """
                Set api key
                :param apiKey:
                :return self:
                """
        self.apiKey = apiKey
        return self

    def getSilentFails(self):
        """
                Get silent fails
                :return bool silentFails:
                """
        return self.silentFails

    def setSilentFails(self, silentFails):
        """
                Set silent fails
                :param bool silentFails:
                """
        self.silentFails = silentFails

    def checkHasAllParameters(self, required):
        """
                Check that our request has all the parameters the server expect
                :param array required:
                :return bool True:
                """
        for req in required:
            if not hasattr(self, req) or getattr(self, req) == None:
                raise NeokamiParametersException('Missing parameter: ' + req + '.')

        return True

    def getWait(self):
        """
                Get wait value
                :return float wait:
                """
        return self.wait

    def setWait(self, wait):
        """
                Set wait value
                :param float wait:
                :return self:
                """
        self.wait = wait
        return self

    def getMaxRetries(self):
        """
                Get max retries value
                :return int max_retries:
                """
        return self.max_retries

    def setMaxRetries(self, max_retries):
        """
                Set max retries value
                :param int max_retries:
                :return self:
                """
        self.max_retries = max_retries
        return self

    def getSleep(self):
        """
                Get sleep value
                :return float sleep:
                """
        return self.sleep

    def setSleep(self, sleep):
        """
                Set sleep value
                :param float sleep:
                :return self:
                """
        self.sleep = sleep
        return self

    def getResult(self, jobId):
        """
                Get results using the job id
                :param string jobId:
                :return object NeokamiResponse:
                """
        response = NeokamiHttpClient.post(self.getUrl('/engine/job/results'), self.apiKey, {'job_id': jobId, 
           'sdk_version': self.SDK_VERSION, 
           'sdk_lang': self.SDK_LANG})
        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())

    def uploader(self, api_url, field_request, data_upload, job_id=None):
        """
                Upload data to the specified endpoint and optionally using the same job_id that a previous upload
                :param string api_url:
                :param string field_request:
                :param mix data_upload:
                :param string job_id:
                :return object NeokamiResponse:
                """
        data = {'wait': self.getWait(), 
           'max_retries': self.getMaxRetries(), 
           'sleep': self.getSleep(), 
           'sdk_version': self.SDK_VERSION, 
           'sdk_lang': self.SDK_LANG, 
           field_request: data_upload}
        if job_id is not None:
            data['job_id'] = job_id
        response = NeokamiHttpClient.post(self.getUrl(api_url), self.apiKey, data)
        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())

    def analyseFromUpload(self, api_url, job_id):
        """
                Analyse uploaded data for the specified job_id
                :param string api_url:
                :param string job_id:
                :return object NeokamiResponse:
                """
        response = NeokamiHttpClient.post(self.getUrl(api_url), self.apiKey, {'job_id': job_id, 
           'sdk_version': self.SDK_VERSION, 
           'sdk_lang': self.SDK_LANG})
        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())

    def getOutputType(self):
        """
                Get output type value
                :return string output_type:
                """
        return self.output_type

    def setOutputType(self, output_type):
        """
                Set output_type
                :param string output_type:
                :return self:
                """
        validTypes = [
         'memory', 'rabbitmq']
        if output_type not in validTypes:
            raise NeokamiParametersException('Specified output is not valid. Valid types are ' + (', ').join(validTypes))
        self.output_type = output_type
        return self