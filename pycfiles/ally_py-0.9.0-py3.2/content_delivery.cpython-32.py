# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/cdm/processor/content_delivery.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jul 14, 2011

@package: service CDM
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Provides the content delivery handler.
"""
from ally.container.ioc import injected
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.http.spec.codes import METHOD_NOT_AVAILABLE, PATH_NOT_FOUND, PATH_FOUND
from ally.http.spec.server import HTTP_GET
from ally.support.util_io import IInputStream
from ally.zip.util_zip import normOSPath, normZipPath
from mimetypes import guess_type
from os.path import isdir, isfile, join, dirname, normpath, sep
from urllib.parse import unquote
from zipfile import ZipFile
import json, logging, os
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    scheme = requires(str)
    uri = requires(str)
    method = requires(str)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    allows = defines(list, doc='\n    @rtype: list[string]\n    Contains the allow list for the methods.\n    ')


class ResponseContent(Context):
    """
    The response context.
    """
    source = defines(IInputStream, doc='\n    @rtype: IInputStream\n    The stream that provides the response content in bytes.\n    ')
    length = defines(int, doc='\n    @rtype: integer\n    Contains the length for the content.\n    ')
    type = defines(str, doc='\n    @rtype: string\n    The type for the streamed content.\n    ')


@injected
class ContentDeliveryHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that delivers the content based on the URL.
    """
    repositoryPath = str
    defaultContentType = 'application/octet-stream'
    _linkExt = '.link'
    _zipHeader = 'ZIP'
    _fsHeader = 'FS'

    def __init__(self):
        assert isinstance(self.repositoryPath, str), 'Invalid repository path value %s' % self.repositoryPath
        assert isinstance(self.defaultContentType, str), 'Invalid default content type %s' % self.defaultContentType
        self.repositoryPath = normpath(self.repositoryPath)
        if not os.path.exists(self.repositoryPath):
            os.makedirs(self.repositoryPath)
        assert isdir(self.repositoryPath) and os.access(self.repositoryPath, os.R_OK), 'Unable to access the repository directory %s' % self.repositoryPath
        super().__init__()
        self._linkTypes = {self._fsHeader: self._processLink,  self._zipHeader: self._processZiplink}

    def process(self, request: Request, response: Response, responseCnt: ResponseContent, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provide the file content as a response.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContent), 'Invalid response content %s' % responseCnt
        if request.method != HTTP_GET:
            if response.allows is not None:
                response.allows.append(HTTP_GET)
            else:
                response.allows = [
                 HTTP_GET]
            response.code, response.status, response.isSuccess = METHOD_NOT_AVAILABLE
        else:
            entryPath = normOSPath(join(self.repositoryPath, normZipPath(unquote(request.uri))))
            if not entryPath.startswith(self.repositoryPath):
                response.code, response.status, response.isSuccess = PATH_NOT_FOUND
            else:
                rf = None
                if isfile(entryPath):
                    rf, size = open(entryPath, 'rb'), os.path.getsize(entryPath)
                else:
                    linkPath = entryPath
                    while len(linkPath) > len(self.repositoryPath):
                        if isfile(linkPath + self._linkExt):
                            with open(linkPath + self._linkExt) as (f):
                                links = json.load(f)
                            subPath = normOSPath(entryPath[len(linkPath):]).lstrip(sep)
                            for linkType, *data in links:
                                if linkType in self._linkTypes:
                                    if not self._isPathDeleted(join(linkPath, subPath)):
                                        entry = self._linkTypes[linkType](subPath, *data)
                                        if entry is not None:
                                            rf, size = entry
                                            break
                                    else:
                                        continue

                            break
                        subLinkPath = dirname(linkPath)
                        if subLinkPath == linkPath:
                            break
                        linkPath = subLinkPath

        if rf is None:
            response.code, response.status, response.isSuccess = PATH_NOT_FOUND
        else:
            response.code, response.status, response.isSuccess = PATH_FOUND
            responseCnt.source = rf
            responseCnt.length = size
            responseCnt.type, _encoding = guess_type(entryPath)
            if not responseCnt.type:
                responseCnt.type = self.defaultContentType
            return
        return

    def _processLink(self, subPath, linkedFilePath):
        """
        Reads a link description file and returns a file handler to
        the linked file.
        """
        linkedFilePath = normOSPath(linkedFilePath)
        if isdir(linkedFilePath):
            resPath = join(linkedFilePath, subPath)
        else:
            if not subPath:
                resPath = linkedFilePath
            else:
                return
        if isfile(resPath):
            return (open(resPath, 'rb'), os.path.getsize(resPath))
        else:
            return

    def _processZiplink(self, subPath, zipFilePath, inFilePath):
        """
        Reads a link description file and returns a file handler to
        the linked file inside the ZIP archive.
        """
        zipFilePath = normOSPath(zipFilePath)
        inFilePath = normOSPath(inFilePath)
        zipFile = ZipFile(zipFilePath)
        resPath = normZipPath(join(inFilePath, subPath))
        if resPath in zipFile.NameToInfo:
            return (zipFile.open(resPath, 'r'), zipFile.getinfo(resPath).file_size)

    def _isPathDeleted(self, path):
        """
        Returns true if the given path was deleted or was part of a directory
        that was deleted.
        """
        path = normpath(path)
        while len(path) > len(self.repositoryPath):
            if isfile(path + '.deleted'):
                return True
            subPath = dirname(path)
            if subPath == path:
                break
            path = subPath

        return False