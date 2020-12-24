# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/havenondemand/hodresponseparser.py
# Compiled at: 2016-10-21 10:54:21
import json
from errorcodes import *

class HODResponseParser(object):
    errorsList = HODErrors()

    def get_last_error(self):
        return self.errorsList

    def parse_jobid(self, jsonResponse):
        if jsonResponse.get('jobID'):
            return jsonResponse['jobID']
        else:
            if jsonResponse.get('error'):
                detail = ''
                if 'detail' in jsonResponse:
                    detail = jsonResponse['detail']
                self.__createErrorObject(jsonResponse['error'], jsonResponse['reason'], detail)
                return
            else:
                self.__createErrorObject(ErrorCode.INVALID_HOD_RESPONSE, 'Invalid HOD response', '')
                return

            return

    def parse_payload(self, jsonResponse):
        return self.__parseHODResponse(jsonResponse)

    def __parseHODResponse(self, jsonObj):
        self.errorsList.resetErrorList()
        if 'actions' in jsonObj:
            actions = jsonObj['actions']
            status = actions[0]['status']
            if status == 'queued':
                self.__createErrorObject(ErrorCode.QUEUED, 'Task is queued', '', jsonObj['jobID'])
                return
            if status == 'in progress':
                self.__createErrorObject(ErrorCode.IN_PROGRESS, 'Task is in progress', '', jsonObj['jobID'])
                return
            if status == 'failed':
                errors = actions[0]['errors']
                for error in errors:
                    err = HODErrorObject()
                    err.error = error['error']
                    err.reason = error['reason']
                    if 'detail' in error:
                        err.detail = error['detail']
                    self.errorsList.addError(err)

                return
            return actions[0]['result']
        else:
            if jsonObj.get('error'):
                detail = ''
                if 'detail' in jsonObj:
                    detail = jsonObj['detail']
                self.__createErrorObject(jsonObj['error'], jsonObj['reason'], detail)
                return
            else:
                return jsonObj

        return

    def __createErrorObject(self, code, reason, detail='', jobID=''):
        self.errorsList.resetErrorList()
        err = HODErrorObject()
        err.error = code
        err.reason = reason
        err.detail = detail
        err.jobID = jobID
        self.errorsList.addError(err)