# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/omSipCreator/omSipCreator/mods.py
# Compiled at: 2017-11-01 08:18:27
"""
Module for writing MODS metadata
"""
import logging
from lxml import etree
from . import config
from .kbapi import sru

def createMODS(PPNGroup):
    """Create MODS metadata based on GGC records in KBMDO
    Dublin Core to MODS mapping follows http://www.loc.gov/standards/mods/dcsimple-mods.html
    General structure: bibliographic md is wrapped in relatedItem / type = host element
    """
    resourceTypeMap = {'cd-rom': 'software, multimedia', 
       'dvd-rom': 'software, multimedia', 
       'dvd-video': 'moving image', 
       'cd-audio': 'sound recording'}
    PPN = PPNGroup.PPN
    carrierType = PPNGroup.carrierType
    modsName = etree.QName(config.mods_ns, 'mods')
    mods = etree.Element(modsName, nsmap=config.NSMAP)
    sruSearchString = '"PPN=' + PPN + '"'
    response = sru.search(sruSearchString, 'GGC')
    if not response:
        noGGCRecords = 0
    else:
        noGGCRecords = response.sru.nr_of_records
    noGGCRecords = response.sru.nr_of_records
    if noGGCRecords != 1:
        logging.error('PPN ' + PPN + ': search for PPN=' + PPN + ' returned ' + str(noGGCRecords) + ' catalogue records (expected 1)')
        config.errors += 1
        config.failedPPNs.append(PPN)
    try:
        record = next(response.records)
        titlesMain = record.titlesMain
        titles = record.titles
        if titlesMain != []:
            titles = titlesMain
        creators = record.creators
        contributors = record.contributors
        publishers = record.publishers
        dates = record.dates
        subjectsBrinkman = record.subjectsBrinkman
        annotations = record.annotations
        identifiersURI = record.identifiersURI
        identifiersISBN = record.identifiersISBN
        recordIdentifiersURI = record.recordIdentifiersURI
        collectionIdentifiers = record.collectionIdentifiers
    except StopIteration:
        titles = []
        creators = []
        contributors = []
        publishers = []
        dates = []
        subjectsBrinkman = []
        annotations = []
        identifiersURI = []
        identifiersISBN = []
        recordIdentifiersURI = []
        collectionIdentifiers = []

    for title in titles:
        modsTitleInfo = etree.SubElement(mods, '{%s}titleInfo' % config.mods_ns)
        modsTitle = etree.SubElement(modsTitleInfo, '{%s}title' % config.mods_ns)
        modsTitle.text = title

    for creator in creators:
        modsName = etree.SubElement(mods, '{%s}name' % config.mods_ns)
        modsNamePart = etree.SubElement(modsName, '{%s}namePart' % config.mods_ns)
        modsNamePart.text = creator
        modsRole = etree.SubElement(modsName, '{%s}role' % config.mods_ns)
        modsRoleTerm = etree.SubElement(modsRole, '{%s}roleTerm' % config.mods_ns)
        modsRoleTerm.attrib['type'] = 'text'
        modsRoleTerm.text = 'creator'

    for contributor in contributors:
        modsName = etree.SubElement(mods, '{%s}name' % config.mods_ns)
        modsNamePart = etree.SubElement(modsName, '{%s}namePart' % config.mods_ns)
        modsNamePart.text = contributor
        modsRole = etree.SubElement(modsName, '{%s}role' % config.mods_ns)
        modsRoleTerm = etree.SubElement(modsRole, '{%s}roleTerm' % config.mods_ns)
        modsRoleTerm.attrib['type'] = 'text'
        modsRoleTerm.text = 'contributor'

    for publisher in publishers:
        modsOriginInfo = etree.SubElement(mods, '{%s}originInfo' % config.mods_ns)
        modsOriginInfo.attrib['displayLabel'] = 'publisher'
        modsPublisher = etree.SubElement(modsOriginInfo, '{%s}publisher' % config.mods_ns)
        modsPublisher.text = publisher

    for date in dates:
        modsOriginInfo = etree.SubElement(mods, '{%s}originInfo' % config.mods_ns)
        modsDateIssued = etree.SubElement(modsOriginInfo, '{%s}dateIssued' % config.mods_ns)
        modsDateIssued.text = date

    modsSubject = etree.SubElement(mods, '{%s}subject' % config.mods_ns)
    for subjectBrinkman in subjectsBrinkman:
        modsTopic = etree.SubElement(modsSubject, '{%s}topic' % config.mods_ns)
        modsTopic.text = subjectBrinkman

    modsTypeOfResource = etree.SubElement(mods, '{%s}typeOfResource' % config.mods_ns)
    modsTypeOfResource.text = resourceTypeMap[carrierType]
    for annotation in annotations:
        modsNote = etree.SubElement(mods, '{%s}note' % config.mods_ns)
        modsNote.text = annotation

    modsRelatedItem = etree.SubElement(mods, '{%s}relatedItem' % config.mods_ns)
    modsRelatedItem.attrib['type'] = 'host'
    modsIdentifierPPN = etree.SubElement(modsRelatedItem, '{%s}identifier' % config.mods_ns)
    modsIdentifierPPN.attrib['type'] = 'ppn'
    modsIdentifierPPN.text = PPN
    for identifierURI in identifiersURI:
        modsIdentifierURI = etree.SubElement(modsRelatedItem, '{%s}identifier' % config.mods_ns)
        modsIdentifierURI.attrib['type'] = 'uri'
        modsIdentifierURI.text = identifierURI

    for identifierISBN in identifiersISBN:
        modsIdentifierISBN = etree.SubElement(modsRelatedItem, '{%s}identifier' % config.mods_ns)
        modsIdentifierISBN.attrib['type'] = 'isbn'
        modsIdentifierISBN.text = identifierISBN

    modsRecordInfo = etree.SubElement(mods, '{%s}recordInfo' % config.mods_ns)
    modsRecordOrigin = etree.SubElement(modsRecordInfo, '{%s}recordOrigin' % config.mods_ns)
    originText = 'Automatically generated by ' + config.scriptName + ' v. ' + config.__version__ + ' from records in KB Catalogue.'
    modsRecordOrigin.text = originText
    return mods