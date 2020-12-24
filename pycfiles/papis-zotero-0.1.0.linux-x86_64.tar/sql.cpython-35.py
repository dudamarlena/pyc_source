# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/papis_zotero/sql.py
# Compiled at: 2019-10-20 15:25:36
# Size of source mod 2**32: 8682 bytes
import sqlite3, yaml, os, shutil, glob, logging, re
excludedTypes = [
 'note']
includedAttachments = {'application/pdf': 'pdf'}
translatedTypes = {'journalArticle': 'article'}
translatedFields = {'DOI': 'doi'}
tagDelimiter = ','
defaultFile = 'info.yaml'

def getTuple(elements):
    """
    Concatenate given strings to SQL tuple of strings
    """
    elementsTuple = '('
    for element in elements:
        if elementsTuple != '(':
            elementsTuple += ','
        elementsTuple += '"' + element + '"'

    elementsTuple += ')'
    return elementsTuple


def getFields(connection, itemId):
    itemFieldQuery = '\n    SELECT\n      fields.fieldName,\n      itemDataValues.value\n    FROM\n      fields,\n      itemData,\n      itemDataValues\n    WHERE\n      itemData.itemID = {itemID} AND\n      fields.fieldID = itemData.fieldID AND\n      itemDataValues.valueID = itemData.valueID\n    '
    fieldCursor = connection.cursor()
    fieldCursor.execute(itemFieldQuery.format(itemID=itemId))
    fields = {}
    for fieldRow in fieldCursor:
        fieldName = translatedFields.get(fieldRow[0], fieldRow[0])
        fieldValue = fieldRow[1]
        fields[fieldName] = fieldValue

    return fields


def getCreators(connection, itemId):
    itemCreatorQuery = '\n    SELECT\n      creatorTypes.creatorType,\n      creators.firstName,\n      creators.lastName\n    FROM\n      creatorTypes,\n      creators,\n      itemCreators\n    WHERE\n      itemCreators.itemID = {itemID} AND\n      creatorTypes.creatorTypeID = itemCreators.creatorTypeID AND\n      creators.creatorID = itemCreators.creatorID\n    ORDER BY\n      creatorTypes.creatorType,\n      itemCreators.orderIndex\n    '
    creatorCursor = connection.cursor()
    creatorCursor.execute(itemCreatorQuery.format(itemID=itemId))
    creators = {}
    for creatorRow in creatorCursor:
        creatorName = creatorRow[0]
        creatorNameList = creatorName + '_list'
        givenName = creatorRow[1]
        surname = creatorRow[2]
        currentCreators = creators.get(creatorName, '')
        if currentCreators != '':
            currentCreators += ' and '
        currentCreators += '{surname}, {givenName}'.format(givenName=givenName, surname=surname)
        creators[creatorName] = currentCreators
        currentCreatorsList = creators.get(creatorNameList, [])
        currentCreatorsList.append({'given_name': givenName, 'surname': surname})
        creators[creatorNameList] = currentCreatorsList

    return creators


def getFiles(connection, itemId, itemKey):
    itemAttachmentQuery = '\n    SELECT\n      items.key,\n      itemAttachments.path,\n      itemAttachments.contentType\n    FROM\n      itemAttachments,\n      items\n    WHERE\n      itemAttachments.parentItemID = {itemID} AND\n      itemAttachments.contentType IN {mimeTypes} AND\n      items.itemID = itemAttachments.itemID\n    '
    mimeTypes = getTuple(includedAttachments.keys())
    attachmentCursor = connection.cursor()
    attachmentCursor.execute(itemAttachmentQuery.format(itemID=itemId, mimeTypes=mimeTypes))
    files = []
    for attachmentRow in attachmentCursor:
        key = attachmentRow[0]
        path = attachmentRow[1]
        mime = attachmentRow[2]
        extension = includedAttachments[mime]
        try:
            importPath = glob.glob(inputPath + '/storage/' + key + '/*.*')[0]
            localPath = os.path.join(outputPath, itemKey, key + '.' + extension)
            shutil.copyfile(importPath, localPath)
            files.append(key + '.' + extension)
        except:
            print('failed to export attachment {key}: {path} ({mime})'.format(key=key, path=path, mime=mime))

    if files == [] and defaultFile:
        files.append(defaultFile)
    return {'files': files}


def getTags(connection, itemId):
    itemTagQuery = '\n    SELECT\n      tags.name\n    FROM\n      tags,\n      itemTags\n    WHERE\n      itemTags.itemID = {itemID} AND\n      tags.tagID = itemTags.tagID\n    '
    tagCursor = connection.cursor()
    tagCursor.execute(itemTagQuery.format(itemID=itemId))
    tags = ''
    for tagRow in tagCursor:
        if tags != '':
            tags += tagDelimiter + ' '
        tags += '{tag}'.format(tag=tagRow[0])

    return {'tags': tags}


def getCollections(connection, itemId):
    itemCollectionQuery = '\n      SELECT\n        collections.collectionName\n      FROM\n        collections,\n        collectionItems\n      WHERE\n        collectionItems.itemID = {itemID} AND\n        collections.collectionID = collectionItems.collectionID\n    '
    collectionCursor = connection.cursor()
    collectionCursor.execute(itemCollectionQuery.format(itemID=itemId))
    collections = []
    for collectionRow in collectionCursor:
        collections.append(collectionRow[0])

    return {'project': collections}


def add_from_sql(input_path, output_path):
    """

    :param input_path: path to zotero SQLite database "zoter.sqlite" and
        "storage" to be imported
    :param output_path: path where all items will be exported to created if not
        existing
    """
    global inputPath
    global outputPath
    logger = logging.getLogger('papis_zotero:importer:sql')
    inputPath = input_path
    outputPath = output_path
    connection = sqlite3.connect(os.path.join(inputPath, 'zotero.sqlite'))
    cursor = connection.cursor()
    excludedTypes.append('attachment')
    excludedTypeTuple = getTuple(excludedTypes)
    itemsCountQuery = '\n      SELECT\n        COUNT(item.itemID)\n      FROM\n        items item,\n        itemTypes itemType\n      WHERE\n        itemType.itemTypeID = item.itemTypeID AND\n        itemType.typeName NOT IN {excludedTypeTuple}\n      ORDER BY\n        item.itemID\n    '
    cursor.execute(itemsCountQuery.format(excludedTypeTuple=excludedTypeTuple))
    for row in cursor:
        itemsCount = row[0]

    itemsQuery = '\n      SELECT\n        item.itemID,\n        itemType.typeName,\n        key\n      FROM\n        items item,\n        itemTypes itemType\n      WHERE\n        itemType.itemTypeID = item.itemTypeID AND\n        itemType.typeName NOT IN {excludedTypeTuple}\n      ORDER BY\n        item.itemID\n    '
    cursor.execute(itemsQuery.format(excludedTypeTuple=excludedTypeTuple))
    currentItem = 0
    for row in cursor:
        currentItem += 1
        itemId = row[0]
        itemType = translatedTypes.get(row[1], row[1])
        itemKey = row[2]
        logger.info('exporting item {currentItem}/{itemsCount}: {key}'.format(currentItem=currentItem, itemsCount=itemsCount, key=itemKey))
        path = os.path.join(outputPath, itemKey)
        if not os.path.exists(path):
            os.makedirs(path)
        fields = getFields(connection, itemId)
        extra = fields.get('extra', None)
        ref = itemKey
        if extra:
            matches = re.search('.*Citation Key: (\\w+)', extra)
            if matches:
                ref = matches.group(1)
            logger.info('exporting under ref %s' % ref)
            item = {'ref': ref, 'type': itemType}
            item.update(fields)
            item.update(getCreators(connection, itemId))
            item.update(getTags(connection, itemId))
            item.update(getCollections(connection, itemId))
            item.update(getFiles(connection, itemId, itemKey))
            item.update({'ref': ref})
            with open(os.path.join(path, 'info.yaml'), 'w+') as (itemFile):
                yaml.dump(item, itemFile, default_flow_style=False)

    logger.info('done')