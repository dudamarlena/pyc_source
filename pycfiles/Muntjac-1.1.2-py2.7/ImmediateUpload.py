# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/upload/ImmediateUpload.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Upload, ProgressIndicator
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class ImmediateUpload(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getDescription(self):
        return 'The upload component can be configured to work as a single-click upload, that starts right after the user has selected the file to upload.<br /><br />In this sample the upload is deliberately slow, so that even small files show the progress indicator.'

    def getName(self):
        return 'Single-click upload'

    def getRelatedAPI(self):
        return [
         APIResource(Upload), APIResource(ProgressIndicator)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.upload.UploadBasic import UploadBasic
        from muntjac.demo.sampler.features.upload.UploadWithProgressMonitoring import UploadWithProgressMonitoring
        return [
         UploadBasic, UploadWithProgressMonitoring]

    def getRelatedResources(self):
        return