# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/neokami1/Dropbox/Neokami/Code/Bitbucket/neokami-python-sdk/neokami/src/Neokami/TopicDetection.py
# Compiled at: 2015-09-08 06:21:37
""" Copyright 2015 Neokami GmbH. """
from .NeokamiRequest import NeokamiRequest
from .Exceptions.NeokamiParametersException import NeokamiParametersException
from .HttpClients.NeokamiCurl import NeokamiHttpClient
import six
NeokamiHttpClient = NeokamiHttpClient()

class TopicDetection(NeokamiRequest):

    def upload(self, job_id=None):
        """
        Upload the text or text array to be analysed
        :param string job_id:
        :return object NeokamiResponse:
        """
        if self.checkHasAllParameters(['text']):
            return self.uploader('/analyse/text/topic/upload', 'text[]', self.text, job_id)

    def analyse(self, job_id):
        """
        Analyse the text or text array that was uploaded
        :param string job_id:
        :return object NeokamiResponse:
        """
        return self.analyseFromUpload('/analyse/text/topic', job_id)

    def setText(self, text):
        """
        Set text to be analyzed
        :param string or list text:
        :return self:
        """
        if isinstance(text, six.string_types):
            self.text = [
             text]
        elif isinstance(text, list) and len(text) > 0:
            self.text = text
        else:
            raise NeokamiParametersException('The parameter set is not valid.')
        return self

    def getText(self):
        """
        Get the text
        :return string text:
        """
        if hasattr(self, 'text'):
            return self.text
        raise NeokamiParametersException('Parameter not set.')