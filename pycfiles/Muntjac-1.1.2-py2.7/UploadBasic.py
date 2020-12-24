# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/upload/UploadBasic.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.upload import Upload
from muntjac.demo.sampler.features.upload.ImmediateUpload import ImmediateUpload
from muntjac.demo.sampler.features.upload.UploadWithProgressMonitoring import UploadWithProgressMonitoring
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class UploadBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getDescription(self):
        return 'Upload component provides a method to handle files uploaded from clients. In this example we simply be count line breaks of the uploaded file.The data could just as well be saved on the server as file or inserted into a database.'

    def getName(self):
        return 'Basic upload'

    def getRelatedAPI(self):
        return [
         APIResource(Upload)]

    def getRelatedFeatures(self):
        return [
         ImmediateUpload, UploadWithProgressMonitoring]

    def getRelatedResources(self):
        return