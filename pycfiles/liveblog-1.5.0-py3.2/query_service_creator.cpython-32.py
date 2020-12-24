# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/media_archive/core/impl/query_service_creator.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Aug 21, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor, Ioan v. Pocol

Creates the service that will be used for multi-plugins queries.
"""
from ally.api.config import service, call, query
from ally.api.extension import IterPart
from ally.api.type import Iter, Scheme
from ally.cdm.spec import ICDM
from ally.support.sqlalchemy.session import SessionSupport
from inspect import isclass
from superdesk.media_archive.api.meta_data import QMetaData, MetaData
from superdesk.media_archive.api.meta_data_info import MetaDataInfo, QMetaDataInfo
from superdesk.media_archive.api.meta_info import QMetaInfo, MetaInfo
from superdesk.media_archive.core.spec import QueryIndexer, IThumbnailManager
from superdesk.media_archive.meta.meta_data import MetaDataMapped

def createService(queryIndexer, cdmArchive, thumbnailManager, searchProvider):
    assert isinstance(queryIndexer, QueryIndexer), 'Invalid query indexer %s' % queryIndexer
    assert isinstance(cdmArchive, ICDM), 'Invalid archive CDM %s' % cdmArchive
    assert isinstance(thumbnailManager, IThumbnailManager), 'Invalid thumbnail manager %s' % thumbnailManager
    assert isinstance(searchProvider, ISearchProvider), 'Invalid search provider %s' % searchProvider
    qMetaInfoClass = type('Compund$QMetaInfo', (QMetaInfo,), queryIndexer.infoCriterias)
    qMetaInfoClass = query(MetaInfo)(qMetaInfoClass)
    qMetaDataClass = type('Compund$QMetaData', (QMetaData,), queryIndexer.dataCriterias)
    qMetaDataClass = query(MetaData)(qMetaDataClass)
    types = (
     Iter(MetaDataInfo), Scheme, int, int, QMetaDataInfo, qMetaInfoClass, qMetaDataClass, str)
    apiClass = type('Generated$IQueryService', (IQueryService,), {})
    apiClass.getMetaInfos = call(*types, webName='Query')(apiClass.getMetaInfos)
    apiClass = service(apiClass)
    return type('Generated$QueryServiceAlchemy', (QueryServiceAlchemy, apiClass), {})(queryIndexer, cdmArchive, thumbnailManager, searchProvider, qMetaInfoClass, qMetaDataClass)


class IQueryService:
    """
    Provides the service methods for the unified multi-plugin criteria query.
    """

    def getMetaInfos(self, scheme, offset=None, limit=10, qa=None, qi=None, qd=None, thumbSize=None):
        """
        Provides the meta data based on unified multi-plugin criteria.
        """
        pass


class ISearchProvider:
    """
    Provides the methods for search related functionality.
    """

    def buildQuery(self, session, scheme, offset, limit, qa=None, qi=None, qd=None):
        """
        Provides the meta data based query on unified multi-plugin criteria.
        """
        pass

    def update(self, MetaInfo, MetaData):
        """
        Provides the update of data on search indexes.
        """
        pass

    def delete(self, idMetaInfo, metaType):
        """
        Provides the delete of data from search indexes.
        """
        pass


class QueryServiceAlchemy(SessionSupport):
    """
    Provides the service methods for the unified multi-plugin criteria query.
    """
    cdmArchive = ICDM
    thumbnailManager = IThumbnailManager
    searchProvider = ISearchProvider

    def __init__(self, queryIndexer, cdmArchive, thumbnailManager, searchProvider, QMetaInfoClass, QMetaDataClass):
        """
        """
        assert isinstance(cdmArchive, ICDM), 'Invalid archive CDM %s' % cdmArchive
        assert isinstance(thumbnailManager, IThumbnailManager), 'Invalid thumbnail manager %s' % thumbnailManager
        assert isinstance(queryIndexer, QueryIndexer), 'Invalid query indexer %s' % queryIndexer
        assert isclass(QMetaInfoClass), 'Invalid meta info class %s' % QMetaInfoClass
        assert isclass(QMetaDataClass), 'Invalid meta data class %s' % QMetaDataClass
        self.cdmArchive = cdmArchive
        self.thumbnailManager = thumbnailManager
        searchProvider.queryIndexer = queryIndexer
        searchProvider.QMetaInfo = QMetaInfoClass
        searchProvider.QMetaData = QMetaDataClass
        self.searchProvider = searchProvider

    def getMetaInfos(self, scheme, offset=None, limit=1000, qa=None, qi=None, qd=None, thumbSize=None):
        """
        Provides the meta data based on unified multi-plugin criteria.
        """
        sql, count = self.searchProvider.buildQuery(self.session(), scheme, offset, limit, qa, qi, qd)
        indexDict = {}
        languageId = None
        if qa and QMetaDataInfo.language in qa:
            languageId = int(qa.language.equal)
        metaDataInfos = list()
        if count == 0:
            return IterPart(metaDataInfos, count, offset, limit)
        else:
            for row in sql.all():
                metaDataMapped = row[0]
                metaInfoMapped = row[1]
                if languageId and metaDataMapped.Id in indexDict:
                    if languageId != metaInfoMapped.Language:
                        continue
                    else:
                        index = indexDict[metaDataMapped.Id]
                        del metaDataInfos[index]
                        count = count - 1
                assert isinstance(metaDataMapped, MetaDataMapped), 'Invalid meta data %s' % metaDataMapped
                metaDataMapped.Content = self.cdmArchive.getURI(metaDataMapped.content, scheme)
                self.thumbnailManager.populate(metaDataMapped, scheme, thumbSize)
                metaDataInfo = MetaDataInfo()
                metaDataInfo.Id = metaDataMapped.Id
                metaDataInfo.Name = metaDataMapped.Name
                metaDataInfo.Type = metaDataMapped.Type
                metaDataInfo.Content = metaDataMapped.Content
                metaDataInfo.Thumbnail = metaDataMapped.Thumbnail
                metaDataInfo.SizeInBytes = metaDataMapped.SizeInBytes
                metaDataInfo.Creator = metaDataMapped.Creator
                metaDataInfo.CreatedOn = metaDataMapped.CreatedOn
                metaDataInfo.Language = metaInfoMapped.Language
                metaDataInfo.Title = metaInfoMapped.Title
                metaDataInfo.Keywords = metaInfoMapped.Keywords
                metaDataInfo.Description = metaInfoMapped.Description
                metaDataInfos.append(metaDataInfo)
                indexDict[metaDataMapped.Id] = count

            return IterPart(metaDataInfos, count, offset, limit)