# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyqualtrics\mock.py
# Compiled at: 2016-06-20 19:58:59
from collections import OrderedDict

class MockQualtrics(object):
    """ Mock object for unit testing code that uses pyqualtrics library

    """

    def __init__(self, user=None, token=None, api_version='2.5'):
        self.user = user
        self.token = token
        self.api_version = api_version
        self.last_error_message = None
        self.last_url = None
        self.json_response = None
        self.response = None
        self.mock_responses = OrderedDict()
        self.mock_responses_labels = OrderedDict()
        return

    def getResponse(self, SurveyID, ResponseID, Labels=None, **kwargs):
        if Labels == '1':
            return self.mock_responses_labels.get(ResponseID, None)
        else:
            return self.mock_responses.get(ResponseID, None)
            return

    def getLegacyResponseData(self, SurveyID, Labels=None, **kwargs):
        if Labels == '1':
            return self.mock_responses_labels
        else:
            return self.mock_responses